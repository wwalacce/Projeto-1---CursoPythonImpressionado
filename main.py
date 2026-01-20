from comunidadeimpressionadora import app # Faz referência ao app da pasta comunidade impressionadora dentro do arquivo __init__. Por ser do arquivo __init__ não é preciso referenciar este arquivo.
from comunidadeimpressionadora import routes #Executa o arquivo para colocar os links que estão na página routes no ar.


if __name__ == '__main__': # Executa o aplicativo Flask
        app.run(debug=True) # Ativa o modo de depuração para desenvolvimento. O site funciona de forma automática ao salvar alterações no código.



#Obs. A importação do routes precisa ser feita embaixo para que rode a criação do app no __init__ primeiro.