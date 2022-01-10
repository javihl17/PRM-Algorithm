import itertools
import time
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import random as rnd
import math
from A_Star import *

maze = []
maze_rect = []

# Clase de una recta que permite discretizarla
class recta:
    def __init__(self, a, b):
        if a[0] == b[0]:
            self.m = "Infinite"
        else:
            self.m = (b[1] - a[1])/(b[0] - a[0])
        self.p1 = a
        self.p2 = b

    def get_point(self, x):
        if str(self.m) == "Infinite":
            return x
        else:
            return (self.m * (x - self.p1[0])) + self.p1[1]

def distancia(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Función para abrir imágen del maze y crear el array correspondiente
def parse_maze(path):
  img = mpimg.imread(path)
  parsed_img = []
  for x in img:
    line = []
    for y in x:
      if y[0] == 1:
        line.append(1)
      else:
        line.append(0)
    parsed_img.append(line)
  return parsed_img

# Cambio de variable entre sistemas de coordenadas
def coord_to_matrix(x,y):
    return (height-y-1, x)

# Obtener colision entre una recta y el maze. Se puede especificar la precisión de la discretización de la recta
def get_collision(r, precision):
    if r.p1[0] == r.p2[0]:
        order = ()
        if r.p1[1] < r.p2[1]:
            order = (r.p1[1], r.p2[1])
        else:
            order = (r.p2[1], r.p1[1])
        for i in range(order[0], order[1]):
            punto = coord_to_matrix(r.p1[0],i)
            if maze[punto[0]][punto[1]] == 0:
                return True
    else:
        order = ()
        if r.p1[0] < r.p2[0]:
            order = (r.p1[0], r.p2[0])
        else:
            order = (r.p2[0], r.p1[0])
        for i in range(order[0],order[1]):
            for f in range(precision):
                punto = coord_to_matrix(i+(1/precision)*f, int(r.get_point(i+(1/precision)*f)))
                if maze[int(punto[0])][int(punto[1])] == 0:
                    return True
    return False

# Dibujar una recta en el maze a partir de su ecuación
def draw_line(r, precision):
    if r.p1[0] == r.p2[0]:
        order = ()
        if r.p1[1] < r.p2[1]:
            order = (r.p1[1], r.p2[1])
        else:
            order = (r.p2[1], r.p1[1])
        for i in range(order[0],order[1]):
            x,y = coord_to_matrix(r.p1[0], i)
            maze[x][y] = 4
    else:
        order = ()
        if r.p1[0] < r.p2[0]:
            order = (r.p1[0], r.p2[0])
        else:
            order = (r.p2[0], r.p1[0])
        for i in range(order[0],order[1]):
            for f in range(precision):
                x, y = coord_to_matrix(i+(1/precision)*f, int(r.get_point(i+(1/precision)*f)))
                maze[int(x)][int(y)] = 4

# Generar puntos en forma de grid
def generate_points_grid(width, height, factor):
    points = []
    for i in range(1, width, factor):
        for j in range(1, height, factor):
            x, y = coord_to_matrix(i,j)
            if maze[x][y] != 0:
                points.append((i,j))
    return points

# Generar puntos totalmente aleatorios
def generate_points_random(width, height, number):
    points = []
    while len(points) < number:
        candidate = (rnd.randint(0, width-1), rnd.randint(0, height-1))
        x, y = coord_to_matrix(candidate[0], candidate[1])
        if maze[x][y] != 0:
            points.append(candidate)
    return points

# Generar puntos en grid aleatorio
def generate_points_grid_random( width,height, number, factor):
    points = []
    grid_size = (factor, factor)
    points_per_cell = number
    for i in range(1, width-grid_size[0], grid_size[0]):
        for j in range(1, height-grid_size[1], grid_size[1]):
            line = []

            while len(line) < points_per_cell:
                candidate = (rnd.randint(i, i+grid_size[0]-1), rnd.randint(j, j+grid_size[1]-1))

                if candidate[0] < width and candidate[1] < height:
                    x, y = coord_to_matrix(candidate[0], candidate[1])
                    if maze[x][y] != 0:
                        line.append(candidate)
            points = points + line
    return points

# Dibujar los puntos en el maze
def draw_points(points):
    suma = 0
    for p in points:
        x, y = coord_to_matrix(p[0], p[1])
        if maze[x][y] != 0:
            suma = suma + 1
            maze[x][y] = 3


# Variables para maze 1
'''maze_path = 'Mazes/Maze01-01.png'
inicio = (8, 82)
final = (155, 1)'''

# Variables para maze 2
'''maze_path = 'Mazes/Maze01-02.png'
inicio = (212, 0)
final = (213, 213)'''

# Variables para maze 3
maze_path = 'Mazes/Maze01-03.png'
inicio = (8, 430)
final = (8, 410)

maze = parse_maze(maze_path)
width, height = np.shape(maze)[1], np.shape(maze)[0]
print("Dimensiones maze: ", width," " ,height)
precision = 80

# Diferentes tipos de inicialización de puntos
start_time_1 = time.time()
#points = generate_points_grid(width,height,10)
#points = generate_points_random(width, height,100)
points = generate_points_grid_random(width, height, 1, 10)
print("Puntos generados: ",len(points))
print("Tiempo de ejecución: %s segundos" % (time.time() - start_time_1))
print("")

# Diferentes tipos de vecindario y su tamaño
vecindario = True
size_vecindario = 20

points.append(inicio)
points.append(final)

# Primer plot con solamente los puntos
draw_points(points)
x,y = coord_to_matrix(inicio[0], inicio[1])
maze[x][y] = 10
x,y = coord_to_matrix(final[0], final[1])
maze[x][y] = 10
imgplot = plt.imshow(maze)
plt.show()
edges = {}

start_time_2 = time.time()
# Obtener los edges entre los puntos generados
for i in range(len(points)):
    conection = []
    for j in range(len(points)):
        if i != j:
            if vecindario == True:
                if abs(points[i][0] - points[j][0]) < 20 and abs(points[i][1] - points[j][1]) < 20:
                    r = recta(points[i],points[j])
                    if get_collision(r, precision) == False:
                        conection.append(points[j])
                        draw_line(r, precision)
            else:
                r = recta(points[i], points[j])
                if get_collision(r, precision) == False:
                    conection.append(points[j])
                    draw_line(r, precision)
    edges[str(points[i])] = conection

# Segundo plot con puntos y las rectas uniendolos
draw_points(points)
print("Tiempo de ejecución: %s segundos" % (time.time() - start_time_2))
print("")
imgplot = plt.imshow(maze)
plt.show()

start_time_3 = time.time()
# Obtener el path con A*
planificador = a_star(points, edges, inicio, final)
path = planificador.busqueda()

# Tercer plot con la ruta final
maze = parse_maze(maze_path)
if path != None:
    for i in range(len(path) - 1):
        r = recta(path[i], path[i + 1])
        draw_line(r, precision)

coste = 0
if path != None:
    for i in range(len(path) - 1):
        coste = coste + distancia(path[i], path[i + 1])
print("Coste: ", coste)

start_time_4 = time.time()
print("Tiempo de ejecución: %s segundos" % (start_time_4 - start_time_3))
print("")


draw_points(points)
imgplot = plt.imshow(maze)
plt.show()