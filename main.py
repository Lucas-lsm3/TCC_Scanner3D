import cv2 as cv
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import timeit
import PySimpleGUI as sg
import threading
from ExtrairPontosImagens.extrairPontos import *
from GerarNuvemPontos.gerarNuvem import *
from alphaShapes import *


def lerIntervalos(caminho):
    with open(caminho, "r") as arquivo:
        l,c = arquivo.readline().replace('\n','').split(',')
        l = int(l)
        c = int(c)
        intervalos = np.zeros([l,c])
        for n in range(l):
            i,j = arquivo.readline().replace('\n','').split(',')
            intervalos[n] = [i,j]
    return intervalos


def lerArray(caminho):
    with open(caminho, "r") as arquivo:
        l,c = arquivo.readline().replace('\n', '').split(',')
        l = int(l)
        c = int(c)
        A = np.zeros((l,c))
        for i in range(l):
            A[i] = arquivo.readline().replace('\n', '').split(',')
        return A
        

def main():
    
    pontos = []
    passos = 400
                
    ledPin1 = 16
    ledPin2 = 18
    stepPin = 38
    dirPin = 40

    caminho = "/home/ifnmg/Desktop/Final/img/"
    extensao = ".png"

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(ledPin1, GPIO.OUT)
    GPIO.setup(ledPin2, GPIO.OUT)
    GPIO.setup(stepPin, GPIO.OUT)
    GPIO.setup(dirPin, GPIO.OUT)

    camera = PiCamera()
    camera.resolution = (640, 480)

    GPIO.output(dirPin, GPIO.LOW)
    GPIO.output(stepPin, GPIO.LOW)
    GPIO.output(ledPin1, GPIO.LOW)
    GPIO.output(ledPin2, GPIO.LOW)

    #-------------------------------
    #Carregar dados de calibração
    #-------------------------------
    intervalo_pixels_fundo_dir = lerIntervalos("DadosCalibracao/intervalosLaserDirDefault.txt")
    intervalo_pixels_fundo_esq = lerIntervalos("DadosCalibracao/intervalosLaserEsqDefault.txt")

    T = lerArray("DadosCalibracao/Matriz_T.txt")
    C_Dir = lerArray("DadosCalibracao/C_Dir.txt")
    C_Esq = lerArray("DadosCalibracao/C_Esq.txt")
                
    #camera.start_preview()
    GPIO.output(dirPin, GPIO.HIGH)
    
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Estado:', key='texto1'),sg.Text('Aguardando início...',key='texto2',pad=((0,0),(0,0)))],
                [sg.ProgressBar(100,orientation='h',size=(20,20),key='progressbar')],
                [sg.Button('Iniciar',key='bt_IniciarParar',button_color=('green')), sg.Button('Sair')] ]

    window = sg.Window('Escaner 3D', layout)

    while True:
        
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == 'Sair':
                break

            elif event == 'bt_IniciarParar':
                     
                inicio = timeit.default_timer()
                
                for i in range(passos):

                    GPIO.output(ledPin1, GPIO.HIGH)
                    sleep(0.08)
                    camera.capture(f"{caminho}imgDir{i}{extensao}")
                    sleep(0.01)
                    GPIO.output(ledPin1, GPIO.LOW)
                    sleep(0.01)

                    GPIO.output(ledPin2, GPIO.HIGH)
                    sleep(0.08)
                    camera.capture(f"{caminho}imgEsq{i}{extensao}")
                    sleep(0.01)
                    GPIO.output(ledPin2, GPIO.LOW)
                    sleep(0.01)
                    
                    imgDIr = cv.imread(f"{caminho}imgDir{i}{extensao}",1)
                    imgEsq = cv.imread(f"{caminho}imgEsq{i}{extensao}",1)
                    
                    vPontosImgsDir, vPontosImgsEsq = extrairPontos(imgDIr, imgEsq, intervalo_pixels_fundo_dir, intervalo_pixels_fundo_esq, i)

                    pontosTemp =  gerarNuvem(T,C_Dir,C_Esq,vPontosImgsDir,vPontosImgsEsq)

                    for pTemp in pontosTemp:
                        pontos.append(pTemp)
                    
                    #Executar 4 micropassos
                    for j in range(4):
                        sleep(0.01)
                        GPIO.output(stepPin, GPIO.HIGH)
                        sleep(0.01)
                        GPIO.output(stepPin, GPIO.LOW)
                                
                    window['progressbar'].update_bar(int((i+1)/4))
                    window['texto2'].update(str(int((i+1)/4)) + ' %')
                    
                GPIO.output(dirPin, GPIO.LOW)
                #camera.stop_preview()
                GPIO.cleanup()
                
                #Criar uma malha de triangulos utilizando a técnica de AlphShapes
                triangulos = alpha_shapes(pontos, 1.5)
                            
                #Salvar a nuvem de pontos em um arquivo .obj
                with open("obj.obj", "w") as f:
                    for i in range(len(pontos)):
                        f.write(f"v {float(pontos[i][0])} {float(pontos[i][1])} {float(pontos[i][2])}\n")

                    for a,b,c in triangulos:
                        f.write(f"f {a+1} {b+1} {c+1}\n")
                
                
                fim = timeit.default_timer()
                sg.popup_ok(f"Escaneamento concuído com sucesso!\nTempo: {int(fim-inicio)} segundos.\nTempo: {int(fim-inicio)/60} minutos.")
                
    window.close()


main()

