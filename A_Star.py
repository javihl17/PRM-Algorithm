# Código basado en el pseudocódigo de Patrick Lester https://homepage.cs.uri.edu/faculty/hamel/courses/2010/spring2010/csc481/lecture-notes/ln015.pdf

import math
import sys

class nodo:
    def __init__(self, posicion, padre):
        self.posicion = posicion
        self.padre = padre
        self.f = 0
        self.g = 0
        self.h = 0

    def distancia(self, n):
        return math.sqrt((n.posicion[0] - self.posicion[0])**2 + (n.posicion[1] - self.posicion[1])**2)

class a_star:
    def __init__(self, puntos, conexiones, inicio, final):
        self.conexiones = conexiones
        self.inicio = nodo(inicio, None)
        self.final = nodo(final, None)
        self.nodos = []
        for x in puntos:
            self.nodos.append(nodo(x, None))
        self.nodos_abiertos = [self.inicio]
        self.nodos_cerrados = []

    def nodo_actual(self):
        output = None
        valor_mínimo = sys.maxsize * 2 + 1

        for n in self.nodos_abiertos:
            print(n.posicion, n.f)
            if n.f < valor_mínimo:
                valor_mínimo = n.f
                output = n
        self.nodos_abiertos.remove(output)
        return output

    def hijos(self, n):
        try:
            posiciones = self.conexiones[str(n.posicion)]
        except:
            return []
        hijos = []
        for n in self.nodos:
            if n.posicion in posiciones:
                hijos.append(n)
        if self.final.posicion in posiciones:
            hijos.append(self.final)
        return hijos

    def devolver_camino(self):
        camino_reves = []
        siguiente_nodo = self.final
        while siguiente_nodo != None:
            print(siguiente_nodo.posicion)
            camino_reves.append(siguiente_nodo.posicion)
            siguiente_nodo = siguiente_nodo.padre
        camino_reves.reverse()
        return camino_reves

    def busqueda(self):
        while len(self.nodos_abiertos) > 0:
            n_actual = self.nodo_actual()
            self.nodos_cerrados.append(n_actual)
            if n_actual == self.final:
                return self.devolver_camino()
            print("Abiertos: ",self.nodos_abiertos)
            print("Cerrados: ",self.nodos_cerrados)
            print("N Actual: ", n_actual.posicion)
            print("Hijos: ",self.hijos(n_actual))
            for c in self.hijos(n_actual):
                if c not in self.nodos_cerrados:
                    if c not in self.nodos_abiertos:
                        c.g = n_actual.g + c.distancia(n_actual)
                        c.h = c.distancia(self.final)
                        c.f = c.g + c.h
                        c.padre = n_actual
                        self.nodos_abiertos.append(c)
                    if c in self.nodos_abiertos:
                        if c.g > n_actual.g + c.distancia(n_actual):
                            c.g = n_actual.g + c.distancia(n_actual)
                            c.h = c.distancia(self.final)
                            c.f = c.g + c.h
                            c.padre = n_actual

if __name__ == "__main__":
    orquestador = a_star(puntos = [(2,2), (3,2), (2,3), (3,3)], conexiones = {'(1, 1)':[(3,2), (2,3), (2,2)],'(2, 2)':[(3,3)] ,'(2, 3)':[(4,4)], '(3, 3)':[(4,4)]},inicio = (1,1), final=  (4,4))

    print(orquestador.hijos(orquestador.nodos[3]))
    print(orquestador.busqueda())