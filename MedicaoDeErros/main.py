



def filtro(caminho, coordenada_z, tolerancia):
    pontos = []
    with open(caminho, "r") as arquivo:
        while True:
            l = arquivo.readline()
            if(len(l) <= 1):
                break
            
            id,x,y,z = l.replace('\n','').split(' ')

            if (id == 'v'):
                if(float(z) < coordenada_z+tolerancia and float(z) > coordenada_z-tolerancia):
                    pontos.append([x,y,z])
        
    with open("res.obj", "w") as arquivo:
        for x,y,z in pontos:
            arquivo.write(f"v {x} {y} {z}\n")


def main():
    filtro("obj3.obj", 4, 0.2)

main()