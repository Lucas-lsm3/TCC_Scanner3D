import itertools
from scipy.spatial import Delaunay
import math
import numpy as np

def distEuclidiana(a,b):
    return math.sqrt(pow(b[0]-a[0], 2) + pow(b[1]-a[1],2) + pow(b[2]-a[2],2))


def alpha_shapes(pontos, alpha):
    tri = Delaunay(pontos)

    triangles = set()
    for a,b,c,d in tri.simplices:
        a = itertools.combinations([a,b,c,d], 3)
        for i in a:
            j = tuple(np.sort(np.array(i)))
            triangles.add(j)


    finalTriangles = []
    for a,b,c in triangles:
        if distEuclidiana(pontos[a],pontos[b]) < alpha and distEuclidiana(pontos[a],pontos[c]) < alpha and distEuclidiana(pontos[b],pontos[c]) < alpha:
            finalTriangles.append([a,b,c])

    return finalTriangles
