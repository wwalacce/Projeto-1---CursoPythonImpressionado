from main import app, database
from models import Usuario, Post

# with app.app_context():
#   database.create_all()

with app.app_context():
#     usuario = Usuario(username="Barboza", email="bbarbozza@gmail.com", senha="123456")
#     usuario2 = Usuario(username="Walace", email="wwalacce@gmail.com", senha="123456")

#     database.session.add(usuario)
#     database.session.add(usuario2)

#     database.session.commit()

  meus_usuarios = Usuario.query.all()
  print(meus_usuarios)
  primeiro_usuario = Usuario.query.first()

  print(primeiro_usuario.username)
  print(primeiro_usuario.email)
  print(primeiro_usuario.senha)