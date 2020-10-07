import math
import random


class noise:
    def __init__(self, x, y):
        x, y = math.ceil(x) + 1, math.ceil(y) + 1
        self.gradients = []
        for j in range(y):
            self.gradients.append([])
            for i in range(x):
                a = random.uniform(0, 1)
                b = math.sqrt(1 - a ** 2)
                c = [-1, 1][random.randint(0,1)]
                d = [-1, 1][random.randint(0,1)]
                self.gradients[j].append([a * c, b * d])

    def dotGridGradient(self, ix, iy, x, y):
        dx = x - ix
        dy = y - iy
        return dx * self.gradients[iy][ix][0] + dy * self.gradients[iy][ix][1]

    def lerp(self, a0, a1, w):
        return a0 + w * (a1 - a0)

    def perlin(self, x, y):
        x0 = int(x)
        x1 = x0 + 1
        y0 = int(y)
        y1 = y0 + 1

        sx = x - x0
        sy = y - y0

        n0 = self.dotGridGradient(x0, y0, x, y)
        n1 = self.dotGridGradient(x1, y0, x, y)
        ix0 = self.lerp(n0, n1, sx)

        n0 = self.dotGridGradient(x0, y1, x, y)
        n1 = self.dotGridGradient(x1, y1, x, y)
        ix1 = self.lerp(n0, n1, sx)

        value = self.lerp(ix0, ix1, sy)
        return value


frequency = 30
amplitude = 20


############ Land size

width = 150 # map width
length = 100 # map length

n1div = 30 # landmass distribution
n2div = 4 # boulder distribution
n3div = 1 # rock distribution

n1scale = 20 # landmass height
n2scale = 2 # boulder scale
n3scale = 1 # rock scale

noise1 = noise(width / n1div, length / n1div) # landmass / mountains
noise2 = noise(width / n2div, length / n2div) # boulders
noise3 = noise(width / n3div, length / n3div) # rocks


############ Display variables

scale = 6
distance = 100

############ Land size

############ z modifiers

zroot = 2
zpower = 2.5


############ colors

colors = {
    0: 'blue',
    1: 'yellow',
    20: 'green',
    25: 'gray',
    1000: 'white'
    }

############ 3D shapes

points = []
triangles = []

############

def color(a, b, c): # check land type
    z = (points[a][2] + points[b][2] + points[c][2]) / 3 # calculate average height of triangle
    for color in colors:
        if z <= color:
            return colors[color]
            break

for x in range(-int(width/2), int(width/2)):
    for y in range(-int(length/2), int(length/2)):
        x1 = x + width/2 
        y1 = y + length/2
        z = noise1.perlin(x1 / n1div, y1 / n1div) * n1scale # add landmass
        z += noise2.perlin(x1 / n2div, y1 / n2div) * n2scale # add boulders
        z += noise3.perlin(x1 / n3div, y1 / n3div) * n3scale # add rocks
        if z >= 0:
            z = -math.sqrt(z)
        else:
            z = ((-z) ** (1 / zroot)) ** zpower
        points.append([x, y, z]) 

for x in range(width):
    for y in range(length):
        if 0 < x and 0 < y:
            a, b, c = int(x * length + y), int(x * length + y - 1), int((x - 1) * length + y) # find 3 points in triangle
            triangles.append([a, b, c, color(a, b, c)])

        if x < width - 1 and y < length - 1:
            a, b, c, = int(x * length + y), int(x * length + y + 1), int((x + 1) * length + y) # find 3 points in triangle
            triangles.append([a, b, c, color(a, b, c)])


actual_triangles = []
for x, y, z, color in triangles:
    actual_triangles.append([points[x], points[y], points[z], color])


if __name__ == '__main__':
    from flowtrail.app import App
    app = App()
    app.scene.add_triangles(actual_triangles)
    app.run()
