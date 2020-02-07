"""
>>> circ = Circle(Coord(200, 100), 100)

>>> rect = Rectangle(Coord(-100, 100), Coord(200, 300))

>>> coords = [Coord(-150, 125),
...           Coord(50, 125),
...           Coord(150, 125),
...           Coord(250, 125),
...           Coord(350, 125)]

# Text if points are in circle
>>> for c in coords:
...     print(c in circ)
...
False
False
True
True
False

# Test if points are in rectangle
>>> for c in coords:
...     print(c in rect)
...
False
True
True
False
False

# Test union
>>> for c in coords:
...     print(c in (circ | rect))
...
False
True
True
True
False

# Test intersection
>>> for c in coords:
...     print(c in (circ & rect))
...
False
False
True
False
False

# Test difference
>>> for c in coords:
...     print(c in (rect - circ))
...
False
True
False
False
False
>>> for c in coords:
...     print(c in (circ - rect))
...
False
False
False
True
False
"""

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

Coord = namedtuple('Coord', ['x', 'y'])


class Shape(ABC):

    def draw(self, canvas_size=(1000, 1000), cmap='binary'):
        canvas = np.zeros(canvas_size)

        midpoint = [i // 2 for i in canvas.shape]
        for i in range(canvas.shape[0]):
            for j in range(canvas.shape[1]):
                coord = Coord(i - midpoint[0], j - midpoint[1])
                canvas[i][j] = int(coord in self)

        plt.imshow(np.rot90(canvas), cmap=cmap)
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def __and__(self, other):
        return Intersection(self, other)

    def __or__(self, other):
        return Union(self, other)

    def __sub__(self, other):
        return Difference(self, other)

    @abstractmethod
    ## define it in other class.
    def __contains__(self,point):
    	pass



class Circle(Shape):
    def __init__(self, center, r):
        self.x = center.x
        self.y = center.y
        self.r = r

    def __contains__(self, point):
        if (int(point[0])-self.x)**2 + (int(point[1])-self.y)**2 >= self.r ** 2:
            return False
        return True


    def __repr__(self):
        return f'Circle(center={self.center},radius={self.radius})'


class Rectangle(Shape):

    def __init__(self, bottom_left,top_right):
        self.x1 = bottom_left.x
        self.y1 = bottom_left.y
        self.x2 = top_right.x
        self.y2 = top_right.y


    def __contains__(self, point):
        if point[0] in range(self.x1, self.x2) and point[1] in range(self.y1, self.y2):
            return True
        return False

    def __repr__(self):
        return f'Rectangle(bottom_left={self.bottom_left}, top_right={self.top_right})'


class Intersection(Shape):

    def __init__(self, shape1, shape2):
        self.shape1 = shape1
        self.shape2 = shape2

    def __contains__(self, point):
        if (point in self.shape1 and point in self.shape2):
        	return True
        else:
        	return False

    def __repr__(self):
        return f'Intersection({self.shape1},{self.shape2})'


class Union(Shape):

    def __init__(self, shape1, shape2):
        self.shape1 = shape1
        self.shape2 = shape2

    def __contains__(self, point):
        if (point in self.shape1 or point in self.shape2):
        	return True
        else:
        	return False

    def __repr__(self):
        return f'Union({self.shape1},{self.shape2})'


class Difference(Shape):
    def __init__(self, shape1, shape2):
        self.shape1 = shape1
        self.shape2 = shape2


    def __contains__(self, point):
        if (point in self.shape1 and point not in self.shape2):
        	return True
        else:
        	return False

    def __repr__(self):
        return f'Difference({self.shape1},{self.shape2})'


if __name__ == '__main__':
    # =====================================================
    # Some samples:
    # =====================================================

    # From doctests
    # -------------

    circ = Circle(Coord(200, 100), 100)
    rect = Rectangle(Coord(-100, 100), Coord(200, 300))

    circ.draw()
    rect.draw()
    (circ | rect).draw()
    (circ & rect).draw()
    (circ - rect).draw()
    (rect - circ).draw()

    # Complex shapes
    # --------------

    # Create a "happy" face by subtracting two eyes and a mouth from a head
    # head = Circle(Coord(0, 0), 200)
    # left_eye = Circle(Coord(-70, 100), 20)
    # right_eye = Circle(Coord(70, 100), 20)
    # mouth = Rectangle(Coord(-90, -80), Coord(90, -60))
    # happy_face = head - left_eye - right_eye - mouth
    # happy_face.draw()

    ## Optical illusion with circles.
    # bigcircle = Circle(0, 0, 240)
    # for x in range(240, 0, -5):
    #    if x % 2:
    #        bigcircle = bigcircle | Circle(0, 0, x - 5)
    #    else:
    #        bigcircle = bigcircle - Circle(0, 0, x - 5)
    # bigcircle.draw()

    ## Optical illusion with squares.
    # bigsquare = Rectangle(-250, -250, 250, 250)
    # for x in range(5, 250, 5):
    #    if x % 2:
    #        bigsquare = bigsquare - Rectangle(-250 + x, -250 + x, 250 - x, 250 - x)
    #    else:
    #        bigsquare = bigsquare | Rectangle(-250 + x, -250 + x, 250 - x, 250 - x)
    # bigsquare.draw()
