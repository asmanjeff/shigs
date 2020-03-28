"""
Chapter 3 is focused on stress and force analysis tools. My initial entry is going to build some vector tools.
"""
from pprint import pprint
from math import sqrt, cos, sin
import numpy as np


class Vector():
    def __init__(self, x, y, z, **kwargs):
        self.name = ''
        self.x = round(x, 3)
        self.y = round(y, 3)
        self.z = round(z, 3)
        self.is_unit_vector = False
        self.i = 1
        self.j = 1
        self.k = 1
        self.magnitude = 0
        self.vector = 0
        self.unit_vector = 0
        self._calculate_magnitude()
        self._calculate_unit_vector()
        self.__dict__.update(**kwargs)
        
    
    def _calculate_magnitude(self):
        self.magnitude = sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.vector = [self.x, self.y, self.z]

        if self.magnitude == 1.0:
            self.is_unit_vector = True
            self.i = self.x
            self.j = self.y
            self.k = self.z
    
    def _calculate_unit_vector(self):
        self.i = round(self.x / self.magnitude, 3)
        self.j = round(self.y / self.magnitude, 3)
        self.k = round(self.z / self.magnitude, 3)
        self.unit_vector = [self.i, self.j, self.k]

    def as_unit_vector(self):
        return (self.i, self.j, self.k)
    
    def as_vector(self):
        return (self.x, self.y, self.z)
    
    def __repr__(self):
        string = '('
        for coord in self.vector:
            string = string + str(coord) + ', '
        string = string[:-2] + ') : {}('.format(round(self.magnitude, 0))
        for coord in self.unit_vector:
            string = string + str(coord) + ', '
        string = string[:-2] + ')'

        return string
        
        
def re_orient_cad(origin, vectors):
    """
    Function Purpose: After obtaining CAD points (x, y, z) this function will re_orient the vectors passed in relative to the origin. 
    
    Inputs:
        origin: tuple (x, y, z) coordinates to be translated to (0, 0, 0)
        vectors: list(tuple1, tuple2, etc) vectors to be translated relative to origin. 
    
    Output:
        output: dict() of {origin: (0,0,0), vector_1: (xnew, ynew, znew), etc}
    """
    output = {'origin': ''}
    if isinstance(origin, Vector):
        output.update({'vectors': list()})
        x_offset = origin.x
        y_offset = origin.y
        z_offset = origin.z
        output.update({'origin': (round(origin.x - x_offset, 3), 
                                  round(origin.y - y_offset, 3), 
                                  round(origin.z - z_offset, 3))})
        for idx, vector in enumerate(vectors):
            output['vectors'].append(Vector(vector.x-x_offset, vector.y-y_offset, vector.z-z_offset, name=str(idx+1)))
    
    else:
        x_offset = origin[0]
        y_offset = origin[1]
        z_offset = origin[2]
        output.update({'origin': (origin[0]-x_offset, origin[1]-y_offset, origin[2]-z_offset)})

        for idx, vector in enumerate(vectors):
            output.update({'vector_{}'.format(idx+1): (round(vector[0]-x_offset, 3), 
                                                       round(vector[1]-y_offset, 3), 
                                                       round(vector[2]-z_offset, 3))})
    
    return output


def cross_product(array_1, array_2):
    return np.cross(array_1, array_2)


def build_x_transform(angle):
    x_trans = [
        [1, 0, 0],
        [0, cos(angle), sin(angle)],
        [0, -sin(angle), cos(angle)]
    ]

    return x_trans

def build_z_transform(angle):
    z_trans = [
        [cos(angle), sin(angle), 0],
        [-sin(angle), cos(angle), 0],
        [0, 0, 1]
    ]

    return z_trans


def euler_coord_system_transform(method, A):
    '''
    Function Purpose: To transform a unit vector in 1 coordinate system to a new coordinate system using Euler angles per:
                      https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-07-dynamics-fall-2009/lecture-notes/MIT16_07F09_Lec03.pdf

    Inputs: method: dict() key is the axis to rotate about, value is the angle to rotate. eg. method={'z': 42, 'x':5, 'z':54}
            A: Vector object

    Outputs: B: tuple (x_new, y_new, z_new) translated into the new coordinate system. 
    '''
    for info in method:
        for idx, axis in enumerate(info):
            angle = info[axis]

            if axis.lower() == 'z':
                transform = build_z_transform(angle)

            elif axis.lower() == 'x':
                transform = build_x_transform(angle)
            if idx == 0:
                T = transform
            
            else:
                T = np.matmul(T, transform)

    
    m = [
        [A.x], 
        [A.y], 
        [A.z]
    ]

    print(m)
    A_prime = np.matmul(T, m)
    return A_prime
    

method = [{'Z': 63.58},
         {'X': -154.8},
         {'Z':87.4}]
    
origin = Vector(439.3, 62.2, -29.1)
vectors = [
    Vector(430.4, 67.7, -24.9),
    Vector(434.7, 58.5, -27.4),
    Vector(428.1, 63.4, -23.5),
    Vector(439.5, 68.0, -29.2),
    Vector(432.7, 70.6, -23.8),
    ]

F_2_3 = Vector(3000*-.725, 3000*.539, 3000*.429)
F_4_5 = Vector(3000*-.75, 3000*.287, 3000*.596)
D_0_2 = Vector(5.96*0.62, 5.96*0.01, 5.96*.78)
D_0_4 = Vector(5.7814*-.43, 5.7814*-.12, 5.7814*-.89)
R = Vector(4251.24, -1154.2, -2403.4)

l = re_orient_cad(origin, vectors)

if __name__ == '__main__':
    origin = (430.4, 67.7, -24.9)
    vectors = [
        (439.3, 62.2, -29.1),
        (432.7, 70.6, -23.8),
        (439.5, 68.0, -29.2),
        (428.1, 63.4, -23.5),
        (434.7, 58.5, -27.4)
    ]

    x = re_orient_cad(origin, vectors)
    pprint(x)