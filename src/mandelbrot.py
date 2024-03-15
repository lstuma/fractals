import pyglet
from pyglet import shapes
from rich import print
from random import randint
import numpy as np
import math

# base setup
height, width = 900, 900
rgb_channels, max_color = 3, 255
img_format = 'RGB'

# pixelmap for fractal
screen = np.zeros([height, width, rgb_channels], dtype=np.uint8)
pitch = width * rgb_channels

window = pyglet.window.Window(width, height)

class Fractal:
    # colors depending on which vertex is selected
    colors = {
        0: (255,120,120),
        1: (255,255,100),
        2: (120,255,255),
    }

    def __init__(self, x, y):
        self.x, self.y = x, y
        # holds pyglet shapes of points
        self.points = []
        # amount of points calculated
        self.pointc = 0
        # last generated point
        self.last = [0,0]
        
        self.done = False
        
    def gen_next(self):
        self.last[0] += 1
        if self.last[0] >= width:
            if self.last[1] >= height-1:
                self.done = True
                return
            self.last[1] += 1
            self.last[0] = 0
            
        self.gen_point(*self.last)

    def gen_point(self, x, y):
        # position relative to middle of fractal (coordinates)
        _x = (x - self.x) * .003
        _y = (y - self.y) * .003
        # calculate value for point
        n = self.calc_point(_x-.5, _y)
        #print(_x, _y, n, end="\r")
        # calculate color
        color = (0, 0, 0)
        if n != math.inf and n > 0:
            color = Fractal.colors[n%3]
        elif n == 0:
            color = (255, 255, 255)
        # add shape for point
        set_color(x, y, color=color)
        self.pointc += 1
        
    def calc_point(self, c1, c2):
        z1, z2 = 0, 0
        for i in range(20):
            _z1 = c1+z1*z1-z2*z2       # 0.1²+2*0.1²*i+0.1²*i²
            z2 = c2+2*z1*z2       #
            z1 = _z1
            if math.sqrt(z1*z1+z2*z2) > 2:
                return i
        return math.inf

f = Fractal(width//2, height//2)
#for i in range(300):
#    print(f.calc_point(i*.01, i*.01))

def set_color(x,y,color):
    for c in range(3):
        screen[y, x, c] = color[c]

@window.event
def on_draw():
    # generate a few new points if not enough have been already generated
    print(f.pointc, end="\r")
    if not f.done:
        for i in range(10000):
            f.gen_next()
    # reset pixelmap for drawing
    image_data = pyglet.image.ImageData(
        width, height, img_format, screen.tobytes(), pitch
    )
    data = np.flipud(screen).tobytes()
    image_data.set_data(img_format, pitch, data)
    
    # redraw everything
    window.clear()
    image_data.blit(0, 0)

for j in range(height):
    for i in range(width):
        screen[j, i, 1] = round((j / height) * max_color)
        
pyglet.app.run()
