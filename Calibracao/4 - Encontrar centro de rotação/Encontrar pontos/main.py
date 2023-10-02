import cv2
import numpy as np

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
    pontos = encontrar_pontos("img/", 15)
    
    for i,j in pontos:
        print(i,j)

    #with open("pontos.txt", "w") as arquivo:
    #    for 

main()
