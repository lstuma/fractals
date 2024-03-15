import pyglet
from pyglet import shapes
from rich import print
from random import randint
import numpy as np
import math
import argparse

# base setup
height, width = 900, 900
rgb_channels, max_color = 3, 255
img_format = 'RGB'

# pixelmap for fractal
screen = np.zeros([height, width, rgb_channels], dtype=np.uint8)
pitch = width * rgb_channels

window = pyglet.window.Window(width, height)

class Fractal:
    def __init__(self, x, y, clarity, colors):
        self.x, self.y = x, y
        # amount of points calculated
        self.pointc = 0
        # last generated point
        self.last = [0,0]

        # for prerender
        self.pixelsize = 10
        
        self.done = False

        self.offset = [0, 0]
        self.zoom = 1

        self.colors = colors
        self.colorc = len(self.colors)

        self.clarity = clarity

        self.rerender()

    def move(self, x, y):
        self.offset[0] += x
        self.offset[1] += y
        self.rerender()

    def rerender(self):
        # reset rendering status
        self.pointc = 0
        self.done = False
        self.last = [0,0]

        # for prerender
        self.pixelsize = 20

        
    def gen_row(self):
        while(self.last[0] <= width-self.pixelsize):
            self.gen_point(*self.last)
            self.last[0] += self.pixelsize    

        self.last[1] += self.pixelsize
        self.last[0] = 0
        
        if self.last[1] >= height-self.pixelsize+1:
            if self.pixelsize > 1:
                self.pixelsize //= 4
                self.last = [0,0]
            else:
                self.done = True
            

    def gen_point(self, x, y):
        # position relative to middle of fractal (coordinates)
        _x = (x - self.x + self.offset[0]) * .003 * self.zoom
        _y = (y - self.y - self.offset[1]) * .003 * self.zoom
        # calculate value for point
        n = self.calc_point(_x-.5, _y)
        # calculate color
        color = (0, 0, 0)
        if n != math.inf and n > 0:
            color = self.colors[n%self.colorc]
        elif n == 0:
            color = (255, 255, 255)
        for i in range(self.pixelsize):
            for j in range(self.pixelsize):
                # add shape for point
                set_color(x+i, y+j, color=color)
        self.pointc += 1
    
    def calc_point(self, c1, c2):
        z1, z2 = 0, 0
        for i in range(self.clarity):
            _z1 = c1+z1*z1-z2*z2       # 0.1²+2*0.1²*i+0.1²*i²
            z2 = c2+2*z1*z2       #
            z1 = _z1
            if math.sqrt(z1*z1+z2*z2) > 2:
                return i
        return math.inf

def set_color(x,y,color):
    for c in range(3):
        screen[y, x, c] = color[c]

@window.event
def on_key_press(symbol, modifiers):
    match(symbol):
        # left
        case 65361:
            f.move(-70, 0)
        # up
        case 65362:
            f.move(0, 70)
        # right
        case 65363:
            f.move(70, 0)
        # down
        case 65364:
            f.move(0, -70)
        # plus +
        case 43:
            f.zoom *= 0.5
            f.move(f.offset[0], f.offset[1])
        # minus -
        case 45:
            f.zoom *= 2
            f.move(-f.offset[0]*.5, -f.offset[1]*.5)

@window.event
def on_draw():
    # generate a few new points if not enough have been already generated
    for i in range(50):
        if not f.done:
            f.gen_row()
    # reset pixelmap for drawing
    image_data = pyglet.image.ImageData(
        width, height, img_format, screen.tobytes(), pitch
    )
    data = np.flipud(screen).tobytes()
    image_data.set_data(img_format, pitch, data)
    
    # redraw everything
    window.clear()
    image_data.blit(0, 0)
        
# alternate colormaps
colormaps = (
    ((255,120,200),(255,255,100),(120,255,255)), # magenta, yellow, cyan
    ((255, 100, 100),(255, 200, 100),(255, 255, 100),(100, 255, 100),(100, 255, 255),(100, 100, 255), (200, 100, 255), (255, 100, 255)), # red, orange, yellow, green, cyan, blue, purple, magenta, 
    ((255, 100, 100),(255, 200, 100),(255, 255, 100)), # red, orange, yellow
    ((250,100, 100),(210, 120, 120),(170,140,140), (130, 160, 160),(90, 180, 180),(130, 160, 160),(170, 140, 140),(210, 120, 120)), # all red and cyan
    ((250, 200, 100),(200, 100, 250),(100, 250, 200), (200, 250, 100),(100, 200, 250)),
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest="n", metavar='n', type=int, help='how many iterations should be run on every pixel (recommended ~ 20)', default=15)
    parser.add_argument('-c', dest="c", metavar='c', type=int, choices=range(len(colormaps)), help='which colormap to use', default=1)
    args = parser.parse_args()

    # set beginning gradient
    for j in range(height):
        for i in range(width):
            screen[j, i, 1] = round((j / height) * max_color)

    f = Fractal(width//2, height//2, args.n, colormaps[args.c])

    pyglet.app.run()
