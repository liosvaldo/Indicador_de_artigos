import os 
import json
import nltk
import string

class Artigos():
    
    def __init__(self, raiz = os.getcwd(), biblioteca=['esporte', 'politica', 'tecnologia']):
        
        self.raiz = raiz
        self.biblioteca = biblioteca 
        nltk.download('stopwords')
    
        self.lista_stopwords = nltk.corpus.stopwords.words('portuguese')
        self.lista_pontuacao = string.punctuation

        
        for assunto in biblioteca:
            
            caminho = os.path.join(self.raiz, assunto)
            
            if not os.path.isdir(caminho):
            
                os.mkdir(caminho)
         
    
    def __retira_pontuacao__(self, texto='a vaca, é amarela!!! a a a'):
       
        for pontuacao in self.lista_pontuacao:
            texto = texto.replace(pontuacao, '')
        
        return texto
    
    def __retira_stopwords__(self, texto = "a vaca, é amarela!!!! a a a"):
    
        lista_palavras = texto.split()
        nova_lista_palavras = []
    
        for  palavra in lista_palavras:
        
            palavra = palavra.strip()
        
            eh_stopwords = palavra in self.lista_stopwords
            na_lista = palavra in nova_lista_palavras
            
            if (not eh_stopwords) and (not na_lista):        
                nova_lista_palavras.append(palavra)
    
        return nova_lista_palavras

        
    def __ajuste_titulo__(self, titulo):
        return "_".join(titulo.split(' '))
    
    def __filtro_palavras__(self, texto='a vaca, é amarela!!! a a a'):
        
        texto_sem_pontuacao = self.__retira_pontuacao__(texto = texto)
        lista_palavras = self.__retira_stopwords__(texto = texto_sem_pontuacao)
    
        return lista_palavras
    
    def adicionar_artigo(self, titulo, assunto, data, texto):
        
        if assunto not in self.biblioteca:
            raise AssuntoNotFound
            
        novo_artigo = {}
        
        titulo = titulo.lower()
        
        titulo_sem_espacos = self.__ajuste_titulo__(titulo)
        
        novo_artigo['titulo'] = titulo
        novo_artigo['data'] = data
        novo_artigo['assunto'] = assunto
        novo_artigo['texto'] = texto
        
        arquivo_json = json.dumps(novo_artigo, indent = 4)
        
        diretorio_novo_arquivo = os.path.join(self.raiz, assunto, titulo_sem_espacos + '.txt' )
        
        with open(diretorio_novo_arquivo, 'w') as arquivo:
            arquivo.writelines(arquivo_json)
        
#         print(novo_artigo)
        
        
    def consultar_por_data(self, reverse = False):
        """
        Retorna uma lista contendo todos os artigos em ordem
        """
        pacote = []
        
        for assunto in self.biblioteca:
            
            diretorio_assunto = os.path.join(self.raiz, assunto)

            for artigo in os.listdir(diretorio_assunto):
                
                caminho_artigo = os.path.join(diretorio_assunto, artigo)
               
                if '.ipynb_checkpoints' not in caminho_artigo:
                    
                    with open(caminho_artigo, 'r') as arquivo_json:
                        arquivo_dicionario = json.loads(arquivo_json.read())
                        pacote.append(arquivo_dicionario)
                                        
        os.chdir(self.raiz)
        api = sorted(pacote, key=lambda artigo: artigo['data'])
        if reverse:
            api.reverse()
            return api
        else:
            return api
        
