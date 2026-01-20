from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # Importando a extensão para login
import pytz  # Biblioteca de timezone
import os


app = Flask(__name__) # Interliga diversas partes do site

app.config['SECRET_KEY'] = '8f258f0a3405ab66b037fc19e3d66496'  # Configuração da chave secreta para segurança dos formulários

# Configurando o caminho LOCAL do banco de dados
if os.getenv("DATABASE_URL"):
    uri = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
#As barras dizem pra criar o banco de dados no mesmo local onde estão os outros arquivos.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)

bcrypt = Bcrypt(app) #Inicializando a senha criptografada

login_manager = LoginManager(app) #Inicializando o login
login_manager.login_message_category = 'alert-info'

login_manager.login_view ="login" # Redireciona o usuario para a página pesquisada após fazer o login
login_manager.login_message_category = 'alert-info'

@app.template_filter('brasilia_time')
def brasilia_time(data):
    if not data:  # Evita erro se vier vazio
        return ''
    
    tz_brasilia = pytz.timezone('America/Sao_Paulo')  # Fuso BR
    data_brasil = data.replace(tzinfo=pytz.utc).astimezone(tz_brasilia)
    
    return data_brasil.strftime('%d/%m/%Y às %H:%M')


from comunidadeimpressionadora import models
from comunidadeimpressionadora import routes

with app.app_context():
    database.create_all()



    # Observações

'''Como pegar o token secreto no proprio python
    - Entrar no terminal do python
    - Digitar Python
    - Digitar import secrets
    - Digitar secrets.token_hex(16)
    - Copiar o token gerado e colar no local da chave secreta
    - Digitar exit() para sair do terminal do python'''



''' Para criar o banco de dados 

1 - Instalar o pip do sqlAlchemy
2 - Passar a configuração do local onde será constuido a rota Ex. SQLALCHEMY_DATABASE_URI
3 - Criar a database usando sqlAlchemy

'''

'''
    
    Criptografando a senha do usuário.

    1 - instalar a biblioteca bcrypt (pip install flask-bcrypt) biblioteca no init
    2 - Importar a biblioteca
    3 - Criar uma instancia do bcrypt no init
    4 - Ir ao Roters e chamar a senha criptografada ao invés da senha normal
    5 - Improtar o bcrypt no routers
    6 - Criar a senha cript no routers na sessão de criar conta
    7 - Importar a senha cripty na sessão de criar conta.
    
    '''
