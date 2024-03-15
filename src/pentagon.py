import pyglet
from pyglet import shapes
from rich import print
from random import randint
import numpy as np

# base setup
height, width = 1540, 980
window = pyglet.window.Window(height, width)
batch = pyglet.graphics.Batch()

class Pentagon:
    def __init__(self, x, y, size):
        # position and size
        self.x, self.y = x, y
        self.size = size
        self.vertices = np.array([(i[0] * self.size + self.x, i[1] * self.size + self.y) for i in ((0, 1), (0.951956163, 0.3090169944), (0.5877852523, -0.8090169944), (-0.5877852523, -0.8090169944), (-0.951956163, 0.3090169944))])
        # create pentagon edges
        self.edges = [
            shapes.Line(*self.vertices[0], *self.vertices[1], batch=batch),
            shapes.Line(*self.vertices[1], *self.vertices[2], batch=batch),
            shapes.Line(*self.vertices[2], *self.vertices[3], batch=batch),
            shapes.Line(*self.vertices[3], *self.vertices[4], batch=batch),
            shapes.Line(*self.vertices[4], *self.vertices[0], batch=batch),
        ]
    
class Fractal:
    # colors depending on which vertex is selected
    colors = {
        0: (100,255,255),
        1: (100,255,100),
        2: (100,100,255),
        3: (255,255,100),
        4: (255,100,255),
    }
    
    def __init__(self, pentagon):
        self.p = pentagon
        # holds last generated point
        self.point = np.array((float(self.p.x), float(self.p.y)))
        # holds pyglet shapes of points
        self.points = []
        # amount of points calculated
        self.pointc = 0
        
    def gen_point(self):
        # choose random vertex
        i = randint(0,4)
        vertex = self.p.vertices[i]
        
        # calculate vector between point and vertex
        vector = np.array((vertex[0] - self.point[0], vertex[1] - self.point[1]))
        # calculate new point
        self.point += vector*0.618
        
        # add shape for point
        self.points.append(shapes.Circle(*self.point, radius=1, color=Fractal.colors[i], batch=batch))
        
        self.pointc += 1

p = Pentagon(height//2-30, width//2-30, 500)
f = Fractal(p)

@window.event
def on_draw():
    # generate a few new points if not enough have been already generated
    print(f.pointc, end="\r")
    if f.pointc < 200000:
        for i in range(100):
            f.gen_point()
    # redraw everything
    window.clear()
    batch.draw()
    
    
pyglet.app.run()