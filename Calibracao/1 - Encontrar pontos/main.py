'''
Este código tem como objetivo segmentar os pontos de um objeto de calibração 3D. Este código implementa uma adaptação do algoritmo de Harris para detecção de cantos.
Entrada: Uma imagem contendo um objeto de calibração 3D. Para este objeto, é aconselhável que seja um cubo, onde em 3 lados do mesmo devem ser colocados/desenhados/sobrepostos com tabuleiros de xadrez com dimensões conhecidas e de preferência que sejam iguais. Estes 3 lados sobrepostos do cubo devem estar visíveis na imagem.
Saída: Uma imagem binária contendo os pontos formados pelos cantos dos tabuleiros de xadrez sendo representados por pixels de cor branca e o restante(pixels que não são de interesse) em cor preta.
'''

import cv2
import numpy as np


class par:
    def __init__(self):
        self.l = 0
        self.c = 0
        self.n = 0

    def add(self, l, c):
        self.l += l
        self.c += c
        self.n += 1

    def media(self):
        if(self.n == 0):
            return 0
        return int(round(self.l/self.n, 0)), int(round(self.c/self.n, 0)) #retorna o par no formato LINHA x COLUNA


def f(img,li,ci,lf,cf,r):
    if(li >= 0 and li < lf and ci >= 0 and ci < cf):
        if(img[li,ci] == -1):
            img[li,ci] = r
            f(img, li-1, ci-1, lf, cf, r)
            f(img, li-1, ci,   lf, cf, r)
            f(img, li+1, ci+1, lf, cf, r)
            f(img, li-1, ci+1, lf, cf, r)
            f(img, li,   ci+1, lf, cf, r)
            f(img, li+1, ci,   lf, cf, r)
            f(img, li+1, ci-1, lf, cf, r)
            f(img, li,   ci-1, lf, cf, r)


def setPixel(img, l, c, cor):
    img.itemset((l,c,0), cor[0])
    img.itemset((l,c,1), cor[1])
    img.itemset((l,c,2), cor[2])


def main():

    img = cv2.imread('entrada/objeto_3D.png', 1)
    img2 = img.copy()
    l,c,t = img.shape
    bin = np.zeros((l,c))
    pontos = np.zeros((l,c))

    img = cv2.GaussianBlur(img,(3,3),0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    cantos = cv2.cornerHarris(gray, 2, 3, 0.05)
    img[cantos > 0.01 * cantos.max()] = [0, 0, 255]

    #Muda a representação da imagem binária para: 0(representa o fundo) e -1(representa os objetos)
    for i in range(l):
        for j in range(c):
            if(img.item(i,j,0) == 0 and img.item(i,j,1) == 0 and img.item(i,j,2) == 255):
                bin[i,j] = -1

    #Numera as regiões(cantos) da imagem binária, nesse caso cada região vai ser rotulada com um número inteiro diferente
    r = 1 #Contador de regiões e inicia com 1 pois o valor 0 representa o fundo da imagem
    for i in range(l):
        for j in range(c):
            if(bin[i,j] == -1):
                f(bin,i,j,l,c,r)
                r+=1

    ####print('r: ' + str(r))

    #Declara e inicializa o vetor de pixels que irá armazenar os pontos finais do tabuleiro
    v = np.ndarray((r),dtype=par)
    for i in range(r):
        v[i] = par()

    #Varre a imagem e preenche o vetor de pixels 
    for i in range(l):
        for j in range(c):
            if(bin[i,j] > 0):
                v[int(bin[i,j])].add(int(i),int(j))
                
    #Marca os pontos obtidos na imagem de entrada
    for val in range(r-1):
        t =  v[val+1].media()
        setPixel(img2, t[0], t[1],[0,0,255])
        pontos[t[0]][t[1]] = 255

    cv2.imshow('Cantos', img)
    cv2.imshow('Pontos - Bin', pontos)
    cv2.imshow('Pontos', img2)

    cv2.imwrite('saida/bin.png', pontos)
    cv2.imwrite('saida/pontos.png', img2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




main()
