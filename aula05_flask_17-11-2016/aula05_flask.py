import datetime, pymysql
from flask import Flask, redirect
from flask.globals import request, session
from flask.helpers import url_for, make_response
from flask.templating import render_template

app = Flask(__name__)

# para facilitar, vamos conectar ao banco e deixar aberta esta conexão
# em um projeto real você deve fechar a conexão após as transações.

# conexão mysql
conexao = pymysql.connect(
    host='localhost',
    user='root',
    passwd='alunoifro',
    db='db_contato_flask'
)
conexao_cursor = conexao.cursor()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # por padrão, os templates tem que estar na pasta templates
    return render_template('index.html')


@app.route('/criar_tabela', methods=['GET'])
def criar_tabela():

    query_sql = """
        CREATE TABLE tb_contato (
          id int(11) NOT NULL AUTO_INCREMENT,
          nome varchar(100) DEFAULT NULL,
          mensagem varchar(500) DEFAULT NULL,
          data_envio datetime DEFAULT NULL,
          PRIMARY KEY (id),
          UNIQUE KEY tb_contato_id_uindex (id)
        );
        CREATE TABLE tb_usuario (
          id int(11) NOT NULL AUTO_INCREMENT,
          usuario varchar(20) NOT NULL,
          nome varchar(100) NOT NULL,
          senha varchar(60) NOT NULL,
          data_cadastro datetime NOT NULL,
          PRIMARY KEY (id)
        );
        CREATE UNIQUE INDEX tb_usuario_id_uindex ON db_contato_flask.tb_usuario (id);
        CREATE UNIQUE INDEX tb_usuario_usuario_uindex ON db_contato_flask.tb_usuario (usuario);
    """
    conexao_cursor.execute(query_sql)

    return '<h1>Tabela criada com sucesso!!</h1>'


@app.route('/excluir_tabela', methods=['GET'])
def excluir_tabela():

    query_sql = """
        DROP TABLE db_contato_flask.tb_contato;
        DROP TABLE db_contato_flask.tb_usuario;
    """
    conexao_cursor.execute(query_sql)

    return '<h1>Tabela excluída com sucesso!!</h1>'


@app.route('/usuarios/', methods=['GET'])
def ver_usuarios():

    # monta o select para pegar todos os registros
    codigo_sql = """
        SELECT * FROM tb_usuario
    """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em 'usuarios' todos os consultados no banco
    usuarios = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('usuarios/ver_usuarios.html', usuarios=usuarios)


@app.route('/usuarios/add', methods=['GET', 'POST'])
def cadastrar_usuario():

    # se clicou no botão "enviar"
    if request.method == 'POST':
        # pega os dados do formulário via request
        nome = request.form['nome']
        usuario = request.form['usuario']
        senha = request.form['senha']
        data_cadastro = datetime.datetime.now()  # pega a data e hora atuais

        # monta o sql para atualizar
        codigo_sql = """
            INSERT INTO tb_usuario (usuario, nome, senha, data_cadastro)
            VALUES ('{}', '{}', '{}', '{}')
        """.format(usuario, nome, senha, data_cadastro)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os usuarios
        return redirect(url_for('ver_usuarios'))

    return render_template('usuarios/add_usuario.html')


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):

    # se clicou no botão "atualizar"
    if request.method == 'POST':
        # pega os dados do formulário via request
        nome = request.form['nome']
        usuario = request.form['usuario']
        senha = request.form['senha']
        data_cadastro = datetime.datetime.now()  # pega a data e hora atuais

        # monta o sql para atualizar
        codigo_sql = """
            UPDATE tb_usuario
            SET usuario='{}', nome='{}', senha='{}', data_cadastro='{}'
            WHERE id='{}'
        """.format(usuario, nome, senha, data_cadastro, id)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os contatos
        return redirect(url_for('ver_usuarios'))

    # se não foi um post então consulta e mostra na página
    # monta o sql para consultar o registro pelo id
    codigo_sql = "SELECT * FROM tb_usuario WHERE id = {}".format(id)

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contato todos os consultados no banco
    usuario = conexao_cursor.fetchall()

    # mostra no template o contato[0], pois vem como uma lista contento 1 elemento apenas
    return render_template('usuarios/editar_usuario.html', usuario=usuario[0])


@app.route('/usuarios/excluir/<int:id>', methods=['GET', 'POST'])
def excluir_usuario(id):

    # se clicou no botão "excluir"
    # monta o código sql para excluir se for o ID tal...
    codigo_sql = "DELETE FROM tb_usuario WHERE id={}".format(id)

    conexao_cursor.execute(codigo_sql)  # executa no banco

    # redireciona para a página com todos os usuarios
    return redirect(url_for('ver_usuarios'))


@app.route('/acessar_cookie', methods=['GET', 'POST'])
def acessar_cookie():

    if request.method == 'POST':
        usuario_digitado = request.form['usuario']
        senha_digitada = request.form['senha']

        # se for um método post, vamos pegar o usuário e senha digitados
        # e pesquisar no banco se existe esse usuário
        codigo_sql = "SELECT * FROM tb_usuario WHERE usuario = '{}'".format(usuario_digitado)

        # executo o sql montado acima
        conexao_cursor.execute(codigo_sql)

        # pego o resultado dessa consulta
        tem_cadastro = conexao_cursor.fetchall()  # lembrando que vem uma "LISTA"

        # agora, verifico se tem algum registro
        if tem_cadastro:
            # se tem, então eu pego o primeiro e único elemento da lista
            dados_usuario_banco = tem_cadastro[0]

            # se tem, então comparamos a senha digitada com a senha salva
            # lembrando que, na posição [0] vem o ID, na [1] o usuário...
            # na [3] a senha
            if dados_usuario_banco[3] == senha_digitada:
                # se chegou aqui, então a senha tá certa
                # crio uma variável de response que vai mudar a página e devolver o cookie para navegador
                # crio o redirecionamento para outra página
                devolver_ao_navegador = app.make_response(
                    redirect(
                        url_for('logado_cookie', usuario=dados_usuario_banco[1])
                    )
                )
                # crio o cookie com o nome de usuário
                devolver_ao_navegador.set_cookie('usuario', dados_usuario_banco[1])
                # retorno o redirecionamento + o cookie
                return devolver_ao_navegador

    return render_template('acessar_cookie.html')


@app.route('/logado_cookie/<string:usuario>', methods=['GET', 'POST'])
def logado_cookie(usuario):

    # para saber se o usuário e a senha foram inseridos corretamente
    # verificamos se existe o cookie
    if request.cookies.get('usuario') == usuario:
        return 'logado com sucesso - utilizando cookies'


@app.route('/acessar_sessao', methods=['GET', 'POST'])
def acessar_sessao():

    if request.method == 'POST':
        usuario_digitado = request.form['usuario']
        senha_digitada = request.form['senha']

        # se for um método post, vamos pegar o usuário e senha digitados
        # e pesquisar no banco se existe esse usuário
        codigo_sql = "SELECT * FROM tb_usuario WHERE usuario = '{}'".format(usuario_digitado)

        # executo o sql montado acima
        conexao_cursor.execute(codigo_sql)

        # pego o resultado dessa consulta
        tem_cadastro = conexao_cursor.fetchall()  # lembrando que vem uma "LISTA"

        # agora, verifico se tem algum registro
        if tem_cadastro:
            # se tem, então eu pego o primeiro e único elemento da lista
            dados_usuario_banco = tem_cadastro[0]

            # se tem, então comparamos a senha digitada com a senha salva
            # lembrando que, na posição [0] vem o ID, na [1] o usuário...
            # na [3] a senha
            if dados_usuario_banco[3] == senha_digitada:
                # se chegou aqui, então a senha tá certa
                # crio uma sessão com o nome do usuário
                # e automaticamente vai criar um cookie seguro
                session['usuario'] = dados_usuario_banco[1]
                return redirect(url_for('logado_sessao'))

    return render_template('acessar_sessao.html')


# lembrando que é preciso criar uma chave secreta para seu projeto
# essa chave será usada para gerar um código criptografado no cookie
app.secret_key = 'umachavesecretaTIPOHASH000lhdjsahkjsahdkjhahdlkjxyczuy'


@app.route('/logado_sessao/', methods=['GET', 'POST'])
def logado_sessao():

    # para saber se o usuário e a senha foram inseridos corretamente
    # verificamos se existe o usuário na sessão
    if 'usuario' in session:
        return '<h1>logado com sucesso - utilizando sessões <br>' \
               ' Usuário: {}</h1>'.format(session['usuario'])


@app.route('/encerrar_sessao')
def encerrar_sessao():
    # remove o usuário logado da sessão atual
    session.pop('usuario', None)
    return redirect(url_for('acessar_sessao'))


############################# FIM USUÁRIOS #############################################

# CONTATOS INÍCIO


@app.route('/contatos/', methods=['GET'])
def ver_contatos():

    # monta o select para pegar todos os registros
    codigo_sql = """
        SELECT * FROM tb_contato
    """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    contatos = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('contatos/ver_contatos.html', contatos=contatos)


@app.route('/contatos/adicionar', methods=['GET', 'POST'])
def cadastra_contato():

    # se clicou no botão "enviar"
    if request.method == 'POST':
        # pega os dados do formulário via request
        nome = request.form['nome']
        msg = request.form['mensagem']
        data_envio = datetime.datetime.now()  # pega a data e hora atuais

        # monta o sql para atualizar
        codigo_sql = """
            INSERT INTO tb_contato (nome, mensagem, data_envio)
            VALUES ('{}', '{}', '{}')
        """.format(nome, msg, data_envio)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os contatos
        return redirect(url_for('ver_contatos'))

    return render_template('contatos/adicionar_contato.html')


@app.route('/contatos/editar/<int:id>', methods=['GET', 'POST'])
def editar_contato(id):

    # se clicou no botão "atualizar"
    if request.method == 'POST':
        # pega os dados do formulário via request
        nome = request.form['nome']
        msg = request.form['mensagem']
        data_envio = datetime.datetime.now()  # pega a data e hora atuais

        # monta o sql para atualizar
        codigo_sql = """
            UPDATE tb_contato
            SET nome='{}', mensagem='{}', data_envio='{}'
            WHERE id='{}'
        """.format(nome, msg, data_envio, id)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os contatos
        return redirect(url_for('ver_contatos'))

    # se não foi um post então consulta e mostra na página
    # monta o sql para consultar o registro pelo id
    codigo_sql = "SELECT * FROM tb_contato WHERE id = {}".format(id)

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contato todos os consultados no banco
    contato = conexao_cursor.fetchall()

    # mostra no template o contato[0], pois vem como uma lista contento 1 elemento apenas
    return render_template('contatos/editar_contato.html', contato=contato[0])


@app.route('/contatos/excluir/<int:id>', methods=['GET', 'POST'])
def excluir_contato(id):

    # se clicou no botão "excluir"
    # monta o código sql para excluir se for o ID tal...
    codigo_sql = "DELETE FROM tb_contato WHERE id={}".format(id)

    conexao_cursor.execute(codigo_sql)  # executa no banco

    # redireciona para a página com todos os contatos
    return redirect(url_for('ver_contatos'))


if __name__ == '__main__':
    # enquanto estiver desenvolvendo,
    # utilize o debug=True para visualizar os erros e
    # seu servidor embutido reiniciar automaticamente
    app.run(debug=True)
