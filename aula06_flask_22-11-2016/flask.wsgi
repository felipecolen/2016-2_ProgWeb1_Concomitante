import sys

# adiciono a localizacao (path) do meu projeto
# na posicao 0, na raiz
sys.path.insert(0, "/var/www/aula06_flask_22-11-2016/")

# do arquivo principal do projeto -> arquivo_flask.py
# importo minha aplicacao -> app como sendo a aplicacao 
from arquivo_flask import app as application

