from flask import render_template, redirect, url_for, flash, request, abort #Abort trava a tentativa.
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost  # Importa os formulários criados no arquivo forms.py
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets # Função para criar um codigo aleatorio para o tipo da imagem enviada pelo usuário.
import os #Separa o tipo do arquivo foto enviado pelo usuário
from PIL import Image # Biblioteca pra reduzir o tamanho da imagem
from datetime import datetime
import pytz

@app.route('/')
def home(): # renderiza a página inicial
    posts = Post.query.order_by(Post.id.desc()) #Ordenando os posts em ordem decrescente.
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    # renderiza a página de contato
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    # renderiza a página de usuários, passando a lista de nomes para o template
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # cria instâncias dos formulários de login e criar conta
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    # debug opcional para ver erros de validação do login
    if request.method == 'POST':
        print('LOGIN errors antes validar:', form_login.errors)

    # ---- LÓGICA DE LOGIN ----
    # verifica se o formulário de login foi enviado e é válido
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # busca usuário pelo e-mail Informado
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        # se encontrou usuário e a senha bate com o hash armazenado
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # realiza o login e usa o valor do checkbox "lembrar_dados" da INSTÂNCIA do formulário
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso no email: {form_login.email.data}', 'alert-success')
            # Redireciona o uduário para a página que eele queria entrar antes de fazer o login
            par_next = request.args.get('next') 
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            # se não encontrou usuário ou senha incorreta, mostra mensagem de erro
            flash('Falha no login. Email ou senha incorretos.', 'alert-danger')

    # ---- LÓGICA DE CRIAR CONTA ----
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # gera hash da senha digitada
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)

        # cria objeto usuário com dados do formulário
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        
        # adiciona na sessão do banco e grava
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso para o email: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    # renderiza a página de login, passando os dois formulários
    return render_template( 'login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required #Bloqueia a página para que não tenha acesso externo sem o usuario estar logado.
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) #Função pra armazenar a foto perfil do usuário. Puxando a foto do models foto_perfil
    return render_template('perfil.html', foto_perfil=foto_perfil) #Passando a variável foto perfil para o HTML. Deverá ser chamada dentro do perfil HTML

# Função para editar, salvar e armazenar a imagem  

def salvar_imagem(imagem):
    # Adicionar um código aleatório no nome da imagem pra que não hava imagens com o mesmo nome no banco
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename) #Separando o nome da extensão em variáveis
    nome_arquivo = nome + codigo + extensao #juntando as 3 variaveis pra formar o nome do arquivo.
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo) # Juntando o arquivo pra salvar no caminho da pasta

    # Reduzir o tamanho da imagem (instalar o pillow no python)
    tamanho = (400, 400) 
    imagem_reduzida = Image.open(imagem) #abrindo a imagem
    imagem_reduzida.thumbnail(tamanho) #Reduzindo a imagem
     # Salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

# Função para atualizar cursos

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form: # For pra percorrer todos os campos
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text) #Adiciona o texto do campo.label, na lista de cursos
    lista_cursos = ';'.join(lista_cursos)
    if len(lista_cursos) == 0:
        lista_cursos = 'Não Informado'
    return lista_cursos # Join vai percorrer toda lista e apresentar uma nova separada por ';'

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        # Exibindo a foto do perfil
        if form.foto_perfil.data:
        #    Criada uma função para salvar, reduzir a imagem e adicionar a imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        
        current_user.cursos = atualizar_cursos(form)  #Curso recebendo a função atualizar cursos
           

        # Mudar o campo foto_perfil do usuário para o novo nome da imagem.
        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    
    # Deixar o formulário já preenchido c os dados. 
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

        # Deixar preenchido os cursos já salvos pelo usuário.
        if current_user.cursos:
            cursos_usuario = current_user.cursos.split(';')
            for campo in form:
                if campo.type == 'BooleanField':
                    if campo.label.text in cursos_usuario:
                        campo.data = True

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) #Função pra armazenar a foto perfil do usuário. Puxando a foto do models foto_perfil

    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form )
    
    #Deixar o formulario de cursos preenchido ao carregar a página

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home')) #Redireciona o usuario para home
    return render_template('criarpost.html', form=form)

#Rota para que o site exiba post especifico numa nova página

@app.route('/post/<int:post_id>')
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, form=None)

@app.route('/post/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)

    if current_user != post.autor:
        flash('Você não pode editar este post.', 'alert-danger')
        return redirect(url_for('exibir_post', post_id=post.id))

    form = FormCriarPost()

    if request.method == 'GET':
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
    elif form.validate_on_submit():
        post.titulo = form.titulo.data
        post.corpo = form.corpo.data
        database.session.commit()
        flash('Post atualizado com sucesso', 'alert-success')
        return redirect(url_for('exibir_post', post_id=post.id))

    return render_template('post.html', post=post, form=form)


@app.template_filter('brasilia_time')
def brasilia_time(data):
    if not data:
        return ''
    tz_brasilia = pytz.timezone('America/Sao_Paulo')
    data_brasil = data.replace(tzinfo=pytz.utc).astimezone(tz_brasilia)
    return data_brasil.strftime('%d/%m/%Y %H:%M')

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    # Busca o post no banco pelo ID recebido na URL
    post = Post.query.get(post_id)

    # Verifica se o post existe
    if post is None:
        abort(404)  # Retorna erro 404 se o post não for encontrado

    # Verifica se o usuário logado é o autor do post
    if current_user == post.autor:
        database.session.delete(post)  # Remove o post do banco
        database.session.commit()      # Confirma a exclusão

        flash('Post excluído com sucesso', 'alert-danger')  # Mensagem de sucesso
        return redirect(url_for('home'))  # Redireciona para a home
    else:
        abort(403)  # Bloqueia acesso se não for o autor




# Current_use = Usuario atual


'''Url_for permite gerar URLs dinamicamente para funções de visualização com base no nome da função. Isso é útil para evitar a codificação rígida de URLs e facilita a manutenção do código, especialmente quando as rotas podem mudar. Por exemplo, em vez de escrever um link fixo como <a href="/usuarios">Usuários</a>, você pode usar <a href="{{ url_for('usuarios') }}">Usuários</a> no seu template HTML. Isso garante que, se a rota para a função 'usuarios' mudar no futuro, o link será atualizado automaticamente sem a necessidade de alterar o HTML manualmente.
    
    
    '''

'''
    Importações: 
            Flask: cria a aplicação web principal e gerencia configuração, rotas e servidor interno.
            render_template: renderiza arquivos HTML da pasta templates, podendo receber variáveis para uso no Jinja.
            url_for: gera URLs corretas para rotas e arquivos estáticos com base no nome da função de rota.
            request: acessa dados da requisição HTTP, como método, parâmetros de formulário, query string e arquivos enviados.
            flash: registra mensagens de feedback (sucesso, erro, aviso) para serem exibidas na próxima resposta ao usuário.
            redirect: envia o navegador para outra rota/URL após uma ação, como login ou envio de formulário.

    '''