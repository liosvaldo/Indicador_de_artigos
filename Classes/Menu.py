class Menu():
    def __init__(self, root_dir = os.getcwd()):
        self.artigo = Artigos(root_dir)
        
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
            entrada_sistema = input("Digite um numero") 
            
            entrada_sistema = int(entrada_sistema)
            
            if entrada_sistema == 1:
                print('1')
#                 self.tela_adicionar_artigo()
            
            elif entrada_sistema == 2:
                print('2')
#                 self.tela_consultar_artigo()
            
            elif entrada_sistema == 3:
                print('3')
#                 self.tela_verificar_melhor_indicacao()
                
            elif entrada_sistema == 4:
                print('4')
#                 self.tela_criar_grafo()
                
            elif entrada_sistema == 5:
                deseja_sair = True
            
            else:
                print('Valor incorreto, tente novamente!!')
                
                
