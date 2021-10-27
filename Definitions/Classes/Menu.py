from Definitions.Classes.Definitions_classes import *
from Definitions.Classes.Artigos import Artigos 
class Menu():
    def __init__(self, root_dir = os.getcwd()):
        self.classe_artigos = Artigos(root_dir)
        
    def run(self):
        
        deseja_sair = False
        
        while not deseja_sair:
            
            print('Classificador de artigo mais parecido')
            print('O que você deseja fazer?')
            print('1 - Adicionar um artigo')
            print('2 - Consultar artigos por data mais recente?')
            print('3 - Verificar qual a melhor indicação com base no titulo do artigo')
            print('4 - Criar grafo de relaçao com base no titulo do artigo')
            print('5 - Sair do programa')
            entrada_sistema = input("Digite um numero: ") 
            
            entrada_sistema = int(entrada_sistema)
            
            if entrada_sistema == 1:
                print('1')
                self.tela_adicionar_artigo()
            
            elif entrada_sistema == 2:
                print('2')
                self.tela_consultar_data()
            
            elif entrada_sistema == 3:
                print('3')
                self.tela_verificar_melhor_indicacao()
                
            elif entrada_sistema == 4:
                print('4')
                self.tela_criar_grafo()
                
            elif entrada_sistema == 5:
                deseja_sair = True
            
            else:
                print('Valor incorreto, tente novamente!!')
    
    def tela_adicionar_artigo(self):
        print('Iniciando a inserção de novos artigos')
        
        verificado = False
        artigo = {}
        
        while not verificado:
            
            
            artigo['titulo'] = input('Por favor, digite o titulo do artigo: ')
            print('titulo do artigo salvo!')
            
            
            assunto = ''
            validado = False 
            
            while not validado:
            
                validado = True
                print('''Digite o numero do assunto que você deseja salvar:
                         1 - Esporte
                         2 - Tecnologia
                         3 - Política''')
                assunto = input('Agora, Digite o numero do assunto: ')

                if assunto == '1':
                    artigo['assunto'] = 'esporte'

                elif assunto == '2':
                    artigo['assunto'] = 'tecnologia'

                elif assunto == '3':
                    artigo['assunto'] = 'politica'
                
                else:
                    print('Favor, digite um numero valido!!')
                    validado = False
            
            print('assunto do artigo salvo!')
            artigo['data'] = input('Qual foi a data de publicação do artigo? formado(aaaa/mm/dd): ')
            print('data adicionada!')
            print('Digite o artigo:')
            artigo['texto'] = input()
        
            print("\n\nVerifique os dados apresentados!")
            print(f"""titulo: {artigo['titulo']}
                      assunto: {artigo['assunto']}
                      data de publicacao: {artigo['data']}
                      texto: 
                      {artigo['texto']}""")
            
            saida = input('Você confere todos os dados? y/n: ')
            if saida == 'y':
                
                self.classe_artigos.adicionar_artigo(**artigo)
                print('\nartigo salvo na base\n\n')
                verificado = True
        
        return True
    
    
    
    def tela_consultar_data(self):
        
        print('iniciando a consulta por data:')
        print('consultando base de arquivos...')
        
        # aqui você captura a api 
        validado = False
        reverse = False
        
        while not validado:
            
            print('''você deseja obter em ordem crescente ou em ordem decrescente?
1 - mais novo encima
2 - mais antigo encima''')
            resposta = input('sua resposta é: ')
            validado = True
            
            if resposta == '1':
                print('mais novo encima selecionado!')
            
            elif resposta == '2':
                print('mais antigo encima selecionado!')
                reverse = True
            
            else:
                print('por favor, digite um valor valido!!!\n')
                validado = False 
                
        api_artigos = self.classe_artigos.consultar_por_data(reverse=reverse)
        print('Tabela de artigos por data de publicação')
        for artigo in api_artigos:
            print(f'''titulo: {artigo['titulo']};    assunto: {artigo['assunto']};    data publicada: {artigo['data']}''')            
        
        print('fim de lista')
        print('\n\n')
        return True

    def tela_verificar_melhor_indicacao(self):
        print('iniciando o metodo de recomendação de artigos!')
        
        sem_consulta= False 
        
        while not sem_consulta:
            
            sem_consulta = True
            validado = False
            titulo = ''

            while not validado:

                validado = True
                titulo = input('Para começar, digite o nome do artigo desejado: ')

                saida = input(f'''O titulo desejado é: {titulo}
você confirma a resposta? y/n''')

                if saida =='y':
                    print('consultando base de arquivos')
                
                elif saida == 'n':
                    validado = False

                else: 
                    print('resposta incorreta, favor informar uma consulta valida!!!')
            
            api = self.classe_artigos.melhor_indicacao(titulo_artigo=titulo)

            print("artigo recomendo é: ")
            print(f'''titulo: {api['titulo']}
            semelhança[%]: {api['valor']*100}''')


            saida_consulta = input('\n deseja consultar um novo titulo? (y/n)')
            
            if saida =='y':
                print('consultando base de arquivos')

            elif saida == 'n':
                sem_consulta = False
            
            else: 
                print('resposta incorreta, favor informar uma consulta valida!!!')
                sem_consulta = False
        
    def tela_criar_grafo(self):
        
        print('iniciando o processo de criação do grafo!')
        
        validacao = False
        
        while not validacao: 
        
            validacao = True
            
            titulo_artigo = input("Por favor, digite o nome do artigo: ")
            
            saida = input(f'O titulo desejdado e: {titulo_artigo}? (y/n)')
            
            if saida == 'y':
                print("Imprimindo o grafo")
            
            elif saida == 'n':
                print("Favor, corrija o titulo do artigo!")
                validacao = False
            
            else:
                print("Favor, digitar um valor valido!!")
                validacao = False
        
        self.classe_artigos.criar_grafo(titulo_artigo=titulo_artigo)
                
