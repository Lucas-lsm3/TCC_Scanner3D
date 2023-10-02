import numpy as np

def obterPontos(caminho):
    with open(caminho, "r") as arquivo:
        n = int(arquivo.readline())
        M = np.zeros((n,3))
        for i in range(n):
            #Linha no formato i(linha na imagem),j(coluna na imagem),x,y,z com os 3 últimos medidos em milímetros.
            l = arquivo.readline().replace('\n', '').replace('-', ' ').replace(',', ' ').split(' ')
            #Adiciona em M apenas os valores das posições 2,3,4 de o vetor l, ou seja, os valores de x,y,z
            M[i] = l[2:]
    return M

def salvar(nomeArquivo, dado):
    l, c = dado.shape
    with open(nomeArquivo, "w") as arquivo:
        arquivo.write(str(l) + ',' + str(c) + '\n')
        for i in range(l):
            arquivo.write(str(dado[i][0]) + '\n')


def gerarC(caminho,nomeArquivoSaida):

    P = obterPontos(caminho)

    C = -np.linalg.inv(P.transpose()@P)@P.transpose()
    l, c = C.shape
    C = C@np.ones((c,1))

    print(C)

    salvar(nomeArquivoSaida, C)
    pass


def main():
    gerarC("pontos_Plano_Dir.txt","C_Dir.txt")
    gerarC("pontos_Plano_Esq.txt","C_Esq.txt")

main()