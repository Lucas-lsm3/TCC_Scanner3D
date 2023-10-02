import cv2 as cv
import numpy as np

class ROI: #A ROI está definida em um intervalo aberto, ou seja, o ponto final(pf) junto a sua linha e coluna não estão incluidos na ROI
    def __init__(self, i,j,h,w):
        self.i = i
        self.j = j
        self.h = h
        self.w = w


def removerFundoD(img, intervalos):
    lImg, cImg = img.shape
    for i in range(lImg):
        if img[i][0] <= intervalos[i][1]:
            img[i][0] = -1 #-1 significa que a linha está vazia(não tem pixel de primeiro plano(plano do laser) nela)
    return img


def removerFundoE(img, intervalos):
    lImg, cImg = img.shape
    for i in range(lImg):
        if img[i][0] >= intervalos[i][0]:
            img[i][0] = -1 #-1 significa que a linha está vazia(não tem pixel de primeiro plano(plano do laser) nela)
    return img


def segmentar(img, roi):
    l,c = img.shape
    #imgRes = np.zeros([l,c])
    vRes = np.zeros([l,1])#vetor coluna onde em cada linha tem se o numero da coluna na qual o pixel está

    #Aplicar borramento pra tentar remover ruídos
    img = cv.GaussianBlur(img,(3,3),0)

    #inicializando o vetor de pixels
    for i in range(l):
        vRes[i][0] = -1 #-1 indica que não tem nenhum pixel de primeiro plano na linha

    #Selecionar o pixel de maior intensidade(addumindo que o tal pixel pertence ao plano do laser) em cada linha e que ao mesmo tempo esteja dentro da roi
    for i in range(l):
        limiar = 10 #Este limiar define a intencidade mínima que um pixel deve assumir para que possar ser um candidato ao plano do laser. Obs: Este valor não remove todos os ruídos.
        li = cj = m = 0
        for j in range(c):
            if(img[i][j] > m):
                m = img[i][j]
                li = i
                cj = j
        if((roi.i <= li <= roi.i+roi.h) and (roi.j <= cj <= roi.j+roi.w)):
            if img[li][cj] > limiar:
                vRes[li][0] = cj
            else:
                vRes[li][0] = -1

    return vRes


def extrairPontos(ImagemEntradaLaserDir, ImagemEntradaLaserEsq, intervalo_pixels_fundo_dir, intervalo_pixels_fundo_esq, nImg):#nImg é o número da imagem, que vai ser armazenado no vetor resposta

    roiDir = ROI(1,320, 427, 78)#320 significa que reduzi em 3 por margem de erro, o exato é 323
    roiEsq = ROI(1,245, 427, 78)#O exato é 247, mas foi colocado 245 de margem de erro
    cont = 0

    pontosLaserDirRes = []
    pontosLaserEsqRes = []


    #-----------------------------------------------
    #Tratando a imagem direita
    #-----------------------------------------------
    img = cv.cvtColor(ImagemEntradaLaserDir, cv.COLOR_BGR2GRAY)
            
    #Obter os pontos do feixe de laser direito
    imgTemp = segmentar(img, roiDir)

    #Remover o feixe de laser que não intercepta a superficie do objeto
    imgTemp = removerFundoD(imgTemp, intervalo_pixels_fundo_dir)#Lembrar de passar a roi como parâmetro para evitar operações fora da mesma
            
    s = img.shape
    imgRes = np.zeros(s)
    for i in range(s[0]):
        if imgTemp[i] > -1:
            imgRes[i][int(imgTemp[i])] = 255

    #Obter os pontos do plano do laser junto ao ângulo de rotação na forma (i,j,n) onde i é a linha, j a coluna e n é qual a imagem(valor esse que será multiplicado pelo ângulo de rotação)
    l, c = imgTemp.shape
    for i in range(l):
        if imgTemp[i] > -1:
            pontosLaserDirRes.append([i,int(imgTemp[i]),nImg])
            cont += 1

    #-----------------------------------------------
    #Tratando a imagem esquerda
    #-----------------------------------------------
    cont = 0

    img = cv.cvtColor(ImagemEntradaLaserEsq, cv.COLOR_BGR2GRAY)
            
    #Obter os pontos do feixe de laser esquerdo
    imgTemp = segmentar(img, roiEsq)

    #Remover o feixe de laser que não intercepta a superficie do objeto
    imgTemp = removerFundoE(imgTemp, intervalo_pixels_fundo_esq)#Lembrar de passar a roi como parâmetro para evitar operações fora da mesma
            
    s = img.shape
    imgRes = np.zeros(s)
    for i in range(s[0]):
        if imgTemp[i] > -1:
            imgRes[i][int(imgTemp[i])] = 255

    #Obter os pontos do plano do laser junto ao ângulo de rotação na forma (i,j,n) onde i é a linha, j a coluna e n é qual a imagem(valor esse que será multiplicado pelo ângulo de rotação)
    l, c = imgTemp.shape
    for i in range(l):
        if imgTemp[i] > -1:
            pontosLaserEsqRes.append([i,int(imgTemp[i]),nImg])
            cont += 1


    return pontosLaserDirRes, pontosLaserEsqRes





