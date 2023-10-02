import numpy as np
import math


def rotacaoEmZ(ponto, angulo, deslocamento_x, deslocamento_y):
    '''
    xTeste = -355
    yTeste = -322
    ponto[0] -= xTeste
    ponto[1] -= yTeste
    '''
    ponto[0] += deslocamento_x
    ponto[1] += deslocamento_y

    m = np.identity(3)
    m[0][0] = math.cos(math.radians(angulo))
    m[0][1] = math.sin(math.radians(angulo))#  (*)
    m[1][0] = -math.sin(math.radians(angulo))# o sinal de '-'(negativo) está aqui para que o angulo seja rotacionado no sentido horário, caso queira mudar para sentido antihorario, remova o sinal de negativo dessa linha e o acrescente na linha marcada com (*), ou seja, na linha acima kk
    m[1][1] = math.cos(math.radians(angulo))
    return m@ponto

def ponto3D(x,y,T,C,angulo, deslocamento_x, deslocamento_y):
    M = np.array([  
                   [  x*T[2][0] - T[0][0],  x*T[2][1] - T[0][1],  x*T[2][2] - T[0][2] ],
                   [  y*T[2][0] - T[1][0],  y*T[2][1] - T[1][1],  y*T[2][2] - T[1][2] ],
                   [  C[0][0],  C[1][0],  C[2][0] ]
                ])

    V = np.array([
                [-x*T[2][3] + T[0][3]],
                [-y*T[2][3] + T[1][3]],
                [-1]
                ])
    
    M_inv = np.linalg.inv(M)
    return rotacaoEmZ(M_inv@V, angulo,deslocamento_x,deslocamento_y)


def gerarNuvem(T,C_Dir,C_Esq,vPontosImgsDir,vPontosImgsEsq):

    pontos = []

    #Mapeando os pontos do plano do laserDireito á câmera do sistema de coordenadas da imagem para pontos no sistema de coordenadas mundial
    for i,j,nImg in vPontosImgsDir:# i é a linha, j é a coluna e nImg é a imagem.
        x,y,z = ponto3D(int(i),int(j),T,C_Dir,int(nImg)*(-0.9),1.6,0.2)#0.9 é o angulo de roltação equivalente a cada passo do motor de passo.
        pontos.append([float(x), float(y), float(z)])

    #Mapeando os pontos do plano do laserEsquerdo á câmera do sistema de coordenadas da imagem para pontos no sistema de coordenadas mundial
    for i,j,nImg in vPontosImgsEsq:# i é a linha, j é a coluna e nImg é a imagem.
        x,y,z = ponto3D(int(i),int(j),T,C_Esq,int(nImg)*(-0.9),0.2,1.6)#0.9 é o angulo de roltação equivalente a cada passo do motor de passo.
        pontos.append([float(x), float(y), float(z)])

    #Salvando a nuvem de pontos em um arquivo .obj
    #with open("obj.obj", "w") as f:
    #    for i in range(len(pontos)):
    #        f.write(f"v {float(pontos[i][0])} {float(pontos[i][1])} {float(pontos[i][2])}\n")

    return pontos
        
    
    