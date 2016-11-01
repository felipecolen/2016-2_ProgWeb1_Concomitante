from flask import Flask
from flask.templating import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    # por padrão, os templates tem que estar na pasta templates
    return render_template('index.html')


if __name__ == '__main__':
    # enquanto estiver desenvolvendo,
    # utilize o debug=True para visualizar os erros e
    # seu servidor embutido reiniciar automaticamente
    app.run(debug=True)
