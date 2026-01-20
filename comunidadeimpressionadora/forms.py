from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # Importa fotos em um formato específico
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField # Importa os campos necessários do WTForms StringField, PasswordField, SubmitField que significam campos de texto, senha e botão de envio, respectivamente.
from wtforms.validators import DataRequired, Email, EqualTo, Length # Importa os validadores DataRequired, Email e EqualTo do WTForms para garantir que os campos sejam preenchidos corretamente.
from comunidadeimpressionadora.models import Usuario # Importando o usuario para validação de email.
from wtforms.validators import ValidationError
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    #Validando o email do usuário para que nao haja email repetido no banco de dados. Importar a biblioteca no forms.
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro email ou faça login pra continuer')

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'webp'])])  #FileAllowed valida os tipos de arquivos que serão recebidos.

    #Adicionando os cursos
    curso_futebol = BooleanField('Futebol impressionador')
    curso_treino = BooleanField('Treino impressionador')
    curso_ataque = BooleanField('Ataque impressionador')
    curso_corrida = BooleanField('Corrida impressionadora')
    curso_artilheiro = BooleanField('Artilheiro impressionador')
    curso_gol = BooleanField('Gol impressionador')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        #Verificar se o cara mudou de email,
        if current_user.email != email.data:
        
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este email. Cdastre outro e-mail.')

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 144)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')
'''O Flask Já tem os validator para email, senha, confirmação de senha, etc.
Datarequired: Garante que o campo não esteja vazio.
Email: Garante que o campo contenha um endereço de email válido.
EqualTo: Garante que dois campos sejam iguais (usado para confirmação de senha).
Esses validadores podem ser adicionados aos campos do formulário para garantir que os dados inseridos pelos usuários atendam aos critérios especificados.'''


'''
Fazendo login no site

1 - intalar a extensao flask-login
2 - importar a biblioteca no init e criar uma variável 
3 - Importar o login_manager no models
4 - Definir uma função que vai carregar o usuario
5 - Importar uma extensão para definir todas as caracteristicas que o manager precisa - UserMixin
6 - Usar o 'UserMixin' dentro da class usuário
7 - Ir na página do routers e dar o comando pra fazer login, importando o método de fazer login
8 - Construir a lógica na funcao login no routers para o usuario conseguir fazer o login

'''