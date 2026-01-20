from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime

# Função de encontrar o usuário - Liberando o login do uruário
@login_manager.user_loader # Diz que esta função que carrega o usuário.
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


# Models eh um arquivo específico para o banco de dados


class Usuario(database.Model, UserMixin): 
    __tablename__ = 'usuario'
    id = database.Column(database.Integer, primary_key=True) # Chave primária pra criar um ID único pra cada usuário
    username = database.Column(database.String, nullable=False) # 'nullable' - Ninguém consegue criar uma conta sem nome do usuário.
    senha = database.Column(database.String,nullable=False)
    email = database.Column(database.String, nullable=False, unique=True) # 'unique' email tem q ser único.
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True) # 'backref' Acessa quem criou o post. 'Lazy' Passa todas as informações sobre o autor.
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo =  database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False) # A chave estrangeira sempre deve estar em letra minúscula.
    


    