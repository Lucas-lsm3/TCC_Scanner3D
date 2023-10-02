import cv2 as cv
import numpy as np


def obterFundo(caminho):
    print('1')
    qtdeLinhas, qtdeColunas = 480, 640
    qtdeImagens = 400
    intervalosLaserDir = np.zeros([qtdeLinhas, 2])#Cada qtdeLinhas dessa matriz é representada como [pci, pcf], ou seja, a propria qtdeLinhas indica a qtdeLinhas na imagem e pci e pcf indicam o intervalo na qtdeLinhas
    intervalosLaserEsq = np.zeros([qtdeLinhas, 2])

    for i in range(qtdeLinhas):
            intervalosLaserDir[i][0] = 9999
            intervalosLaserDir[i][1] = 0
            
            intervalosLaserEsq[i][0] = 9999
            intervalosLaserEsq[i][1] = 0

    print('2')

    #Obtendo os intervalos dos pixels do plano de laser direito
    for n in range(qtdeImagens):
        img = cv.imread(caminho+'/imgDir' + str(n) + '.png', 0)
        img = cv.GaussianBlur(img,(3,3),0)

        l, c = img.shape
        for i in range(l):
            vMax = id_j = 0

            for j in range(c):
                if(img[i][j] > vMax):
                    id_j = j
                    vMax = img[i][j]
            
            if(id_j < intervalosLaserDir[i][0]):
                 intervalosLaserDir[i][0] = id_j-1#O -1 é uma margem de erro
            if(id_j > intervalosLaserDir[i][1]):
                 intervalosLaserDir[i][1] = id_j+1#O +1 é uma margem de erro
            
    print('3')

    #Removendo/reduzindo outliers. Neste caso, o vetor de intervalos é percorrido de cima para baixo, caso o limite avaliado seja muito distante(distancia maior que 30) do limite anterior(limite logo acima), tal limite recebe a média dos limites anteriores.
    for i in range(1,qtdeLinhas):#desconsiderei a primeira linha
        if(abs(intervalosLaserDir[i][0] - intervalosLaserDir[i-1][0]) > 30):
             intervalosLaserDir[i][0] = (intervalosLaserDir[i-1][0]+intervalosLaserDir[i-1][1])/2
        if(abs(intervalosLaserDir[i][1] - intervalosLaserDir[i-1][1]) > 30):
             intervalosLaserDir[i][1] = (intervalosLaserDir[i-1][0]+intervalosLaserDir[i-1][1])/2

    print('4')

    with open("intervalosLaserDirDefault.txt", "w") as arquivo:
        arquivo.write(str(qtdeLinhas) + ',' + str(2) + '\n')
        for i in range(qtdeLinhas):
            arquivo.write(str(int(intervalosLaserDir[i][0])) + "," + str(int(intervalosLaserDir[i][1])) + '\n')

    print('5')

    #Obtendo os intervalos dos pixels do plano de laser esquerdo
    for n in range(qtdeImagens):
        img = cv.imread(caminho+'/imgEsq' + str(n) + '.png', 0)# "n+qtdeImagens" pq as imagens estão no mesmo diretório e em sequencia(as primeiras 400(0 a 399) pro laser direito e as outras 400(400 a 799) pro laser esquerdo)
        img = cv.GaussianBlur(img,(3,3),0)

        l, c = img.shape
        for i in range(l):
            vMax = id_j = 0

            for j in range(c):
                if(img[i][j] > vMax):
                    id_j = j
                    vMax = img[i][j]
            
            if(id_j < intervalosLaserEsq[i][0]):
                 intervalosLaserEsq[i][0] = id_j
            if(id_j > intervalosLaserEsq[i][1]):
                 intervalosLaserEsq[i][1] = id_j
    
    print('6')

    #Removendo/reduzindo outliers. Neste caso, o vetor de intervalos é percorrido de cima para baixo, caso o limite avaliado seja muito distante(distancia maior que 30) do limite anterior(limite logo acima), tal limite recebe a média dos limites anteriores.
    for i in range(1,qtdeLinhas):#desconsiderei a primeira linha
        if(abs(intervalosLaserEsq[i][0] - intervalosLaserEsq[i-1][0]) > 30):
             intervalosLaserEsq[i][0] = (intervalosLaserEsq[i-1][0]+intervalosLaserEsq[i-1][1])/2
        if(abs(intervalosLaserEsq[i][1] - intervalosLaserEsq[i-1][1]) > 30):
             intervalosLaserEsq[i][1] = (intervalosLaserEsq[i-1][0]+intervalosLaserEsq[i-1][1])/2


    print('7')

    with open("intervalosLaserEsqDefault.txt", "w") as arquivo2:
        arquivo2.write(str(qtdeLinhas) + ',' + str(2) + '\n')
        for i in range(qtdeLinhas):
            arquivo2.write(str(int(intervalosLaserEsq[i][0])) + "," + str(int(intervalosLaserEsq[i][1])) + '\n')

    print('8')

    #Abaixo segue a exibição dos intervalos
    intervaloDir = np.zeros([qtdeLinhas, qtdeColunas])
    intervaloEsq = np.zeros([qtdeLinhas, qtdeColunas])

    for i in range(qtdeLinhas):
        intervaloDir[i][int(intervalosLaserDir[i][0])] = 255
        intervaloDir[i][int(intervalosLaserDir[i][1])] = 255

    for i in range(qtdeLinhas):
        intervaloEsq[i][int(intervalosLaserEsq[i][0])] = 255
        intervaloEsq[i][int(intervalosLaserEsq[i][1])] = 255
    

    cv.imshow("Intervalo laser direito", intervaloDir)
    cv.imshow("Intervalo laser esquerdo", intervaloEsq)
    cv.waitKey()
    cv.imwrite('intervalosDir.png', intervaloDir)
    cv.imwrite('intervalosEsq.png', intervaloEsq)




def main():
    obterFundo("fundo")

    
main()