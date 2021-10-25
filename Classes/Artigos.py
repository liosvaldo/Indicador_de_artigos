import os 
import json
import nltk
import string
import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import Image, display

class Artigos():
    
    def __init__(self, raiz = os.getcwd(), biblioteca=['esporte', 'politica', 'tecnologia']):
        
        self.raiz = raiz
        self.biblioteca = biblioteca 
        nltk.download('stopwords')
        self.campo_conteudo = ['assunto', 'texto', 'data', 'titulo']
    
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
    
    def __relacao_entre_textos__(self, texto_artigo1, texto_artigo2):
    
        lista_palavras1 = self.__filtro_palavras__(texto_artigo1)
        lista_palavras2 = self.__filtro_palavras__(texto_artigo2)

        lista_palavras_contidas = list(filter(lambda palavra: palavra in lista_palavras2, lista_palavras1))
        porcentagem_palavras_contidas = len(lista_palavras_contidas)/len(lista_palavras1)

        return porcentagem_palavras_contidas
    
    def __pega_artigos__(self, *campo_solicitado,  biblioteca = []):
        
        biblioteca = self.biblioteca
    
        pacote = []

        for assunto in biblioteca:

            assunto_diretorio = os.path.join(self.raiz, assunto)

            for artigo in os.listdir(assunto_diretorio):

                caminho_artigo = os.path.join(assunto_diretorio, artigo)

                if '.ipynb_checkpoints' not in caminho_artigo:

                    with open(caminho_artigo, 'r') as artigo_json:

                        artigo_dicionario = json.loads(artigo_json.read())
                        
                        
                       
                        for topico in self.campo_conteudo:
                            if topico not in campo_solicitado:
                                artigo_dicionario.pop(topico, None)
                    
                        pacote.append(artigo_dicionario)

        os.chdir(self.raiz)
        return pacote
   
    def __separa_artigos__(self, titulo_artigo, conjuto_artigos):
        
        artigo_referencia = list(filter(lambda artigo: artigo['titulo'] == titulo_artigo, conjuto_artigos))
         
        artigo_referencia = artigo_referencia[0]
        
        demais_artigos = list(filter(lambda artigo: artigo['titulo'] != titulo_artigo, conjuto_artigos))
        
        return artigo_referencia, demais_artigos
    
    
    
    def __pega_porcentagem_entre_textos__(self, titulo_artigo='a vaca amarela'):

        
        conjuto_artigos = self.__pega_artigos__('titulo', 'texto')
        
        artigo_referencia, demais_artigos = self.__separa_artigos__(titulo_artigo = titulo_artigo, conjuto_artigos=conjuto_artigos)
        
        pacote = []
        
        
        for outro_artigo in demais_artigos:
            
            similaridade_com_texto = {}
            porcentagem_relacao = gerenciador.__relacao_entre_textos__(artigo_referencia['texto'], outro_artigo['texto'])
            similaridade_com_texto['titulo'] = outro_artigo['titulo']
            similaridade_com_texto['valor'] = porcentagem_relacao
            pacote.append(similaridade_com_texto)
            
        return pacote    
    
    def melhor_indicacao(self, titulo_artigo='a vaca amarela'):
    
        api = gerenciador.__pega_porcentagem_entre_textos__(titulo_artigo = titulo_artigo)

        indicacoes = sorted(api, key=lambda relacao_artigos: relacao_artigos['valor'])
        return indicacoes[0]
    
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
        
        pacote = self.__pega_artigos__('data', 'titulo', 'assunto')
        api = sorted(pacote, key=lambda artigo: artigo['data'])
        
        if reverse:
            api.reverse()
            return api
        
        else:
            return api

    def criar_grafo(self, titulo_artigo='a vaca amarela'):
    
        grafo = nx.Graph()

        lista_relacoes = self.__pega_porcentagem_entre_textos__(titulo_artigo)

        arestas = []

        for artigo in lista_relacoes:
            dados_relacao = (titulo_artigo, artigo['titulo'], artigo['valor'])
            arestas.append(dados_relacao)

        grafo.add_weighted_edges_from(arestas)

        pos = nx.spring_layout(grafo, seed=42)

        nx.draw(grafo, pos, with_labels=True)

        atributo_arestas = nx.get_edge_attributes(grafo, 'weight')
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=atributo_arestas)
        plt.show()
