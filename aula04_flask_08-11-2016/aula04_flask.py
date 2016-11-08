import datetime, pymysql
from flask import Flask, redirect
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template

app = Flask(__name__)

# para facilitar, vamos conectar ao banco e deixar aberta essa conexão
# em um projeto real você deve fechar a conexão após as transações.

# conexão mysql
conexao = pymysql.connect(
    # host='127.0.0.1',
    host='172.17.0.2',
    user='root',
    passwd='senhamysql',
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
        )
    """
    conexao_cursor.execute(query_sql)

    return '<h1>Tabela criada com sucesso!!</h1>'


@app.route('/excluir_tabela', methods=['GET'])
def excluir_tabela():

    query_sql = """
        DROP TABLE db_contato_flask.tb_contato;
    """
    conexao_cursor.execute(query_sql)

    return '<h1>Tabela excluída com sucesso!!</h1>'


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
