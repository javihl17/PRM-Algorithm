import itertools
import time
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import random as rnd
from A_Star import *

maze = []
maze_rect = []

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

def get_collision_pygame(r):
    for m in maze_rect:
        order = ()
        if r.p1[1] < r.p2[1]:
            order = (r.p1[0],r.p2[0])
        else:
            order = (r.p2[0], r.p1[0])
        for x in range(order[0],order[1]):
            if m.collidepoint((x, r.get_point(x))):
                return True
    return False

def coord_to_matrix(x,y):
    return (height-y-1, x)

def get_collision(r):
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
            for f in range(20):
                punto = coord_to_matrix(i+0.05*f, int(r.get_point(i+0.05*f)))
                if maze[int(punto[0])][int(punto[1])] == 0:
                    return True
    return False

def draw_line(r):
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
            for f in range(20):
                x, y = coord_to_matrix(i+0.05*f, int(r.get_point(i+0.05*f)))
                # print(i,r.get_point(i))
                maze[int(x)][int(y)] = 4

def generate_points_grid(width, height, factor):
    points = []
    for i in range(1, height, factor):
        for j in range(1, width, factor):
            x, y = coord_to_matrix(i,j)
            if maze[x][y] != 0:
                points.append((i,j))
    return points

def generate_points_random(width, height, number):
    points = []
    while len(points) < number:
        candidate = (rnd.randint(0, width-1), rnd.randint(0, height-1))
        x, y = coord_to_matrix(candidate[0], candidate[1])
        print(candidate, (x,y))
        if maze[x][y] != 0:
            points.append(candidate)
    return points

#Sin terminar aun
def generate_points_guided(width, height, number):
    points = []
    queue = []
    while len(points) < number:
        candidate = (rnd.randint(0, width - 1), rnd.randint(0, height - 1))
        x, y = coord_to_matrix(candidate[0], candidate[1])
    return points

def generate_points_grid_random(height, width, number, factor):
    points = []
    grid_size = (factor, factor)
    points_per_cell = int(number/(int(width/grid_size[0])*int(height/grid_size[1])))
    print(grid_size, points_per_cell)
    for j in range(1, width, grid_size[0]):
        for i in range(1, height, grid_size[1]):
            line = []
            while len(line) < points_per_cell:
                candidate = (rnd.randint(i, i+grid_size[0]-1), rnd.randint(j, j+grid_size[1]-1))
                print(candidate)
                x, y = coord_to_matrix(candidate[0], candidate[1])
                if x < width and y < height:
                    if maze[x][y] != 0:
                        line.append(candidate)
            points = points + line
    return points

def draw_points(points):
    for p in points:
        x, y = coord_to_matrix(p[0], p[1])
        if maze[x][y] != 0:
            maze[x][y] = 3

maze = parse_maze('Maze01-01.png')
inicio = (8, 82)
final = (155, 1)
tile_size = 3
width, height = np.shape(maze)[1], np.shape(maze)[0]
print((width, height))

#print(maze)

#r = recta(a=(20,19), b=(5,19))
#r = recta(a=(20,5), b=(20,20))
#print(get_collision(r))
#draw_line(r)

# Diferentes tipos de inicialización de puntos
#points = generate_points_grid(height,width,12)
#points = generate_points_random(width, height,100)
points = generate_points_grid_random(width, height, 50, 15)
print(points)

points.append(inicio)
points.append(final)
draw_points(points)
x,y = coord_to_matrix(inicio[0], inicio[1])
print("Punto",x,y)
maze[x][y] = 10
x,y = coord_to_matrix(final[0], final[1])
print("Punto",x,y)
maze[x][y] = 10
imgplot = plt.imshow(maze)
plt.show()
edges = {}

for i in range(len(points)):
    conection = []
    for j in range(len(points)):
        if i != j:
            r = recta(points[i],points[j])
            if get_collision(r) == False:
                conection.append(points[j])
                draw_line(r)
    edges[str(points[i])] = conection
print(edges)

draw_points(points)
imgplot = plt.imshow(maze)
plt.show()

planificador = a_star(points, edges, inicio, final)
path = planificador.busqueda()

print(path)

maze = parse_maze('Maze01-01.png')


if path != None:
    for i in range(len(path) - 1):
        r = recta(path[i], path[i + 1])
        draw_line(r)

    ou = []
    for p in path:
        x, y = coord_to_matrix(p[0], p[1])
        ou.append((x,y))
    print(ou)

draw_points(points)
imgplot = plt.imshow(maze)
plt.show()

'''screen = pg.display.set_mode((width, height))

clock = pg.time.Clock()


background = pg.Surface((width, height))
background.fill((255,255,255))

while True:

    screen.fill((60, 70, 90))
    screen.blit(background, (0, 0))

    color = (255,0,0)
    color_line =(0,0,0)

    # Crear los rectangulos a partir del laberinto
    for i in range(np.shape(maze)[1]):
        for j in range(np.shape(maze)[0]):
            rect = pg.Rect(i*3, j*3, 3, 3)
            color = ()
            if maze[j][i] == 0:
                maze_rect.append(rect)

    r = recta(a=(10,10), b=(500,250))
    pg.draw.line(background, color_line, start_pos=r.p1, end_pos=r.p2)

    grid = generate_points_grid(width, height, 10)
    for i in range(len(grid)):
        for j in range(len(grid)):
            #print((i,j))
            if i != j:
                r = recta(a=grid[i], b=grid[j])
                #if get_collision(r) == False:
                pg.draw.line(background, color_line, start_pos=r.p1, end_pos=r.p2)

    pg.display.flip()

    clock.tick(30)
    time.sleep(4)
pg.quit()'''