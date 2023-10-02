import numpy as np
import math

def coordHomogen(a, b, tam):#transfere os elementos da string 'a' para o vetor de inteiros 'b' em coordenadas homogeneas
    aAux = a.split(',')
    for i in range(tam):
        b[i] = float(aAux[i])
    b[tam] = 1 #valor da coordenada homogenea

def ler(path):
    with open(path, "r") as arquivo:
        n = int(arquivo.readline())
        pontosMundo = np.zeros([int(n), 4]) #representação em coordenadas homogeneas
        pontosImagem = np.zeros([int(n), 3]) #representação em coordenadas homogeneas

        for i in range(n):
            la = arquivo.readline()
            l = la.replace("\n","").split('-')
            coordHomogen(l[0], pontosMundo[i], 3)
            coordHomogen(l[1], pontosImagem[i], 2)

    return n, pontosMundo, pontosImagem

def gerar(n, pMundo, pImagem):
    A = np.zeros([n*2, 12])
    for i in range(n):
        A[2*i][4] = -1*pMundo[i][0]
        A[2*i][5] = -1*pMundo[i][1]
        A[2*i][6] = -1*pMundo[i][2]
        A[2*i][7] = -1*pMundo[i][3]

        A[2*i][8] = pImagem[i][1]*pMundo[i][0]
        A[2*i][9] = pImagem[i][1]*pMundo[i][1]
        A[2*i][10] = pImagem[i][1]*pMundo[i][2]
        A[2*i][11] = pImagem[i][1]*pMundo[i][3]
    
        A[2*i+1][0] = pMundo[i][0]
        A[2*i+1][1] = pMundo[i][1]
        A[2*i+1][2] = pMundo[i][2]
        A[2*i+1][3] = pMundo[i][3]

        A[2*i+1][8] = -1*pImagem[i][0]*pMundo[i][0]
        A[2*i+1][9] = -1*pImagem[i][0]*pMundo[i][1]
        A[2*i+1][10] = -1*pImagem[i][0]*pMundo[i][2]
        A[2*i+1][11] = -1*pImagem[i][0]*pMundo[i][3]
    return A

def solucao(U):
    # Encontra os autovalores e o autovetor de U(transposta)*U.
    a_vals, a_vets = np.linalg.eig(np.dot(U.T, U))  
    # Extrai o autovetor(coluna) associado ao autovalor mínimo.
    return a_vals[np.argmin(a_vals)], a_vets[:, np.argmin(a_vals)]

def normaEuclidiana(v):
    n = v.shape
    total = 0
    for i in range(n[0]):
        total += v[i]*v[i]
    return math.sqrt(total)

def salvar(caminho, dado):
    l, c = dado.shape
    print(dado.shape)
    
    with open(caminho, "w") as arquivo:
        arquivo.write(str(l) + ',' + str(c) + '\n')
        for i in range(l):
            for j in range(c):
                if(j < c-1):
                    lRes = str(dado[i][j]) + ','
                else:
                    lRes = str(dado[i][j])
                arquivo.write(lRes)
            arquivo.write('\n')

def main(): 
    #Ler o arquivo de correspondencia de pontos, cada linha é formada por x,y,z-i,j, onde x,y,z são os pontos no sistema de coordenadas mundial e i,j representam os pontos(pixels) correspondentes nas imagens. Obs: x,y e z estão na unidade de medida em milímetros(mm).
    n, pMundo, pImagem = ler("pontos.txt")

    #Obtem a matriz A que será utilizada para compont o sistema AX = 0 
    A = gerar(n, pMundo, pImagem)

    #Resolve o sistema homogeneo AX = 0
    a_Val, a_Vet = solucao(A)#a_Vet é o autovetor relacionado ao menor autovalor e é a solução do sistema

    #print(normaEuclidiana(a_Vet))
    print(a_Vet)
    
    m = np.array([
        [a_Vet[0],a_Vet[1],a_Vet[2],a_Vet[3]],
        [a_Vet[4],a_Vet[5],a_Vet[6],a_Vet[7]],
        [a_Vet[8],a_Vet[9],a_Vet[10],a_Vet[11]]
    ])

    salvar('matriz_T.txt', m)


main()