import pyglet
from pyglet import shapes
from rich import print
from random import randint
import numpy as np

# base setup
height, width = 1540, 980
window = pyglet.window.Window(height, width)
batch = pyglet.graphics.Batch()

# constanst
colors = {
    "cyan": (100,255,255),
    "magenta": (255,100,255),
    "yellow": (255,255,100),
    "red": (255,100,100),
    "green": (100,255,100),
    "blue": (100,100,255),
    "orange": (255,175,25),
    "greenblue": (25,255,175),
    "greenred": (175,255,25),
    "redblue": (255,25,175),
    "bluered": (175,25,255),
    "bluegreen": (25,175,255),
    "white": (255,255,255),
    "black": (0,0,0),
}

class Triangle:
    def __init__(self, x, y, size, color=False):
        # position and size
        self.x, self.y = x, y
        self.size = size
        self.vertices = np.array([(i[0] * self.size + self.x, i[1] * self.size + self.y) for i in ((0, 1),(0.8660254038, -0.5), (-0.8660254038, -0.5))])
        self.vertices_rel = np.array([(i[0] * self.size, i[1] * self.size) for i in ((0, 1),(0.8660254038, -0.5), (-0.8660254038, -0.5))])
        
        self.color = color or (255,255,255)
        # create triangle edges
        self.edges = [
            shapes.Line(*self.vertices[0], *self.vertices[1], batch=batch, color=self.color),
            shapes.Line(*self.vertices[1], *self.vertices[2], batch=batch, color=self.color),
            shapes.Line(*self.vertices[2], *self.vertices[0], batch=batch, color=self.color),
        ]
        
        if color:
            self.shape = shapes.Triangle(*self.vertices[0], *self.vertices[1], *self.vertices[2], batch=batch, color=self.color);

class Fractal:
    # colors depending on which vertex is selected
    colors = {
        0: (100,255,255),
        1: (255,100,255),
        2: (255,255,100),
        3: (255,100,100),
        4: (100,255,100),
        5: (100,100,255),
        6: (255,175,25),
        7: (25,255,175),
        8: (175,255,25),
        9: (255,25,175),
        10: (175,25,255),
        11: (25,175,255),
    }

    def __init__(self, triangle, fixcolor=False):
        self.t = triangle
        # holds last generated point
        self.point = np.array((float(self.t.x), float(self.t.y)))
        # holds pyglet shapes of triangles
        self.triangles = []
        self.trianglec = 0
        self.n = 0
        
        self.fixcolor = fixcolor
        
    def decode(self, seed, pos):
        return (seed >> (pos*2))%4

    def gen_triangles(self):
        # since we are working in binary well be using each two bits to mark one of the three possible gen_triangles
        # but since this means we have one configuration (11) too much that marks an inexistent triangle, we'll need to filter every
        # fourth triangle out
        i = 0
        # seed for every triangle to decide where it goes
        for seed in range(4**self.n):
            self.gen_triangle(seed)
        self.n += 1
        
    def get_color(self, i):
        if self.fixcolor: return self.fixcolor
        else: return Fractal.colors[i]

    def gen_triangle(self, seed):
        size = .5
        x, y = self.t.x, self.t.y
        multiplier = 1/2
        for i in range(0, self.n):
            # with every generation the size quarters
            size *= .5
            
            vi = self.decode(seed, i)
            if vi == 3: return
            vertex = self.t.vertices_rel[vi]
            x += vertex[0] * multiplier
            y += vertex[1] * multiplier
            multiplier *= 1/2
            
        # add triangle to shapes
        self.triangles.append(shapes.Triangle(x + self.t.vertices_rel[0][0] * size, y - self.t.vertices_rel[0][1] * size,
                                              x + self.t.vertices_rel[1][0] * size, y - self.t.vertices_rel[1][1] * size,
                                              x + self.t.vertices_rel[2][0] * size, y - self.t.vertices_rel[2][1] * size,
                                              color=self.get_color(self.n),batch=batch))
        
        self.trianglec += 1

t = Triangle(height//2, width//2-150, 620, colors["red"])
f = Fractal(t, fixcolor=colors["black"])

@window.event
def on_draw():
    # n will max out at 11 (88573 triangles)
    # if n would be larger there would be too many triangles (12: 265720, 13: 797161, 14: 2391484)
    print(f"n = {f.n-1}\t|\t {f.trianglec} triangles", end="\r")
    # any value above 8 will make the fractal look broken due to the triangles being smaller than the pixels
    if f.n <= 8:
        f.gen_triangles()
    # redraw everything
    window.clear()
    batch.draw()

pyglet.app.run()