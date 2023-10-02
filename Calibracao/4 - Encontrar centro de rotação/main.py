import cv2
import numpy as np
import math


def encontrar_pontos(caminho, qtdeimgns):

    pontos = []

    for n in range(qtdeimgns):
        # Carregar a imgem
        img = cv2.imread(caminho + "img" + str(n) + ".png")

        # Converter a imgm para tons de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplicar o detector de cantos de Harris
        corners = cv2.cornerHarris(gray, 2, 3, 0.04)

        # Aumentar a visibilidade dos cantos
        corners = cv2.dilate(corners, None)

        # Definir um limite para filtrar os cantos
        threshold = 0.01 * corners.max()

        # Encontrar as coordenadas (x, y) dos cantos
        corner_coords = np.where(corners > threshold)

        # Calcular o centro dos cantos encontrados
        center_x = int(np.mean(corner_coords[1]))
        center_y = int(np.mean(corner_coords[0]))
        center = (center_x, center_y)

        InvCenter = (center_y, center_x)#Centro no formato (linha, coluna)

        #Adicionar o ponto ao resultado
        pontos.append(InvCenter)

    return pontos

def main():
    qtdeImagens = 15

    Pw = np.zeros([qtdeImagens,3])
    P = np.zeros([qtdeImagens,1])

    pontos = encontrar_pontos("img/", qtdeImagens)

    for n,(i,j) in enumerate(pontos):
        Pw[n] = [-2*i,-2*j,1]
        P[n] = (-math.pow(i,2) - math.pow(j,2))

    Xr = -np.linalg.inv(Pw.transpose()@Pw)@Pw.transpose()
    l, c = Xr.shape
    Xr = Xr@P
    
    print(Xr.shape)
    print(Xr)
    print("linha: " + str(int(Xr[0][0])))
    print("coluna: " + str(int(Xr[1][0])))

    img = cv2.imread("img/img0.png",0)

    l,c = img.shape
    bin = np.zeros([l,c])

    for i,j in pontos:
        bin[i][j] = 255
    
    ll = int(abs(Xr[0][0]))
    cc = int(abs(Xr[1][0]))
    bin[ll][cc] = 255
    print(ll,cc)

    cv2.imshow("lol", bin)
    cv2.waitKey(0)

    with open("centro_rotacao.txt", "w") as arquivo:
        arquivo.write(str(int(abs(Xr[0][0]))) + ',' + str(int(abs(Xr[1][0]))))



main()
