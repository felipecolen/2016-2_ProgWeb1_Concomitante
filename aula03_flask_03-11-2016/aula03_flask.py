import datetime, pymysql
from flask import Flask
from flask.globals import request
from flask.templating import render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    # por padrão, os templates tem que estar na pasta templates
    return render_template('index.html')


@app.route('/contato', methods=['GET', 'POST'])
def cadastra_contato():

    # se clicou no botão "enviar"
    if request.method == 'POST':
        nome = request.form['nome']
        msg = request.form['mensagem']
        data_e_hora = datetime.datetime.now()  # pega a data e hora atuais

        return """
            <br><br>
            TOP! <br><br>
            DEU CERTO! <br><br>
            ISSO FOI UM POST! <br><br><br>

            Nome: <h1> {} </h1> <br>
            Msg: <h2> {} </h2> <br>
            às {}
        """.format(nome, msg, data_e_hora)


    return render_template('contato.html')


@app.route('/conectar', methods=['GET'])
def conectar_ao_banco():

    # conexão mysql
    conexao = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='alunoifro',
        db='mysql'
    )
    conexao.cursor()

    return "Conectou com Sucesso!!!  :D"


if __name__ == '__main__':
    # enquanto estiver desenvolvendo,
    # utilize o debug=True para visualizar os erros e
    # seu servidor embutido reiniciar automaticamente
    app.run(debug=True)
