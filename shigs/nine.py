"""
Chapter 9: Focused on permanent joints. These include but are not limited to welds, bonds, and brazing. 
           The first addition to this script is dedicated to weld analysis using geometric unit welds per tables 9-1 and 9-2. 
           If you have anything you'd like to add pull requests are welcome: lint with flake8 + pylint - Jasman
"""
from math import pi
from pprint import pprint

class Weld():
    """
    Base class for welds:
       h = weld size, for example a 1/8 fillet weld would be .125
       t = throat thickness
       l = length of the weld
    """
    def __init__(self, h, t, l):
        self.h = h
        self.t = t
        self.l = l
        self.throat_area = t*l


class TorsionalTools():
    """
    See Table 9-1 for details regarding this class structure
        h = weld size
        b = weld spacing dimension # 1
        d = weld spacing dimension # 2
        r = radius to weld 

        all arguments of __init__ are optional, if omitted a default value of 1 is passed in place.
    """
    def __init__(self, h=1, b=1, d=1, r=1):
        if r!=1:
            print('A radius was specified during object creation')
        if r==1 and b==1 or d==1:
            print('Assumption: default spacings for b and d of the weld structure are set to 1, this can be altered at instantiation')
        self.b = b
        self.d = d
        self.h = h
        self.r = r 
        self.x = 0  # x-vector distance to centroid G
        self.y = 0  # y-vector distance to centroid G
        self.Ju = 0  # Unit Second Polar moment of area
        self.Iu = 0  # Unit second moment of area
        self.J = 0  # Second Polar Moment of area
        self.I = 0  # Second moment of area
        self.A = 0  # throat area
        self.group = None
    
    def __repr__(self):
        pprint(self.__dict__)
        return ''

    def _update_moment_of_areas(self):
        self.J = 0.707 * self.h * self.Ju
        self.I = 0.707 * self.h * self.Iu

    def _update_attributes(self, **kwargs):
        for key in kwargs:
            if key not in self.__dict__.keys():
                print('{} is not a recognized attribute of the TorsionalTools attributes'.format(key))
                print('No key word arguments were updated to the class attributes')
                return None

        self.__dict__.update(**kwargs)

    def get_group_1_attributes(self, **kwargs):
        # Shape: |
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 0.707 * self.h * self.d
        self.x = 0
        self.y = self.d/2
        self.Ju = self.d**3/12
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-1, Group 1'
    
    def get_group_2_attributes(self, **kwargs):
        # Shape: | |
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 1.414 * self.h * self.d
        self.x = self.b / 2
        self.y = self.d / 2
        self.Ju = self.d * (3 * self.b**2 + self.d**2) / 6
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-1, Group 2'        

    def get_group_3_attributes(self, **kwargs):
        # Shape: |_
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 0.707 * self.h * (self.b + self.d)
        self.x = self.b**2 / 2 / (self.b + self.d)
        self.y = self.d**2 / 2 / (self.b + self.d)
        self.Ju = (self.b + self.d)**4 - 6 * self.b**2 * self.d**2 / 12 / (self.b + self.d)
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-1, Group 3'

    def get_group_4_attributes(self, **kwargs):
        # Shape: C or E minus the middle - (C channel)
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 0.707 * self.h * (self.b + self.d)
        self.x = self.b**2 / (2 * self.b + self.d)
        self.y = self.d / 2
        self.Ju = (8 * self.b**3 + 6 * self.b * self.d**2 + self.d**3)/12 - self.b**4 /(2*self.b + self.d)
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-1, Group 4'

    def get_group_5_attributes(self, **kwargs):
        # Shape: Rect~Box []
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 1.414 * self.h * (self.b + self.d)
        self.x = self.b / 2
        self.y = self.d / 2
        self.Ju = (self.b + self.d)**3 / 6
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-1, Group 5'

    def get_group_6_attributes(self, **kwargs):
        # Shape: O
        if kwargs:
            self._update_attributes(**kwargs)
        if self.r == 1:
            print('Group 6 in torsion is a circular weld, the default of r=1 has been recognized.  You can specify the radius input while calling get_group_6_attributes if' 
                   'you would like to change it')

        self.A = 1.414 * pi * self.h * self.r
        self.x = 0
        self.y = 0
        self.Ju = 2 * pi * self.r**3
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-1, Group 6'


class BendingTools(TorsionalTools):
    """
    See table 9-2 for the class definition. This object inherits all code methods from TorsionalTools. 
    """
    def get_group_1_attributes(self, **kwargs):
        # Shape: |
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 0.707 * self.h * self.d
        self.x = 0
        self.y = self.d / 2
        self.Iu = self.d**3 / 12
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 1'
    
    def get_group_2_attributes(self, **kwargs):
        # Shape: | |
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 1.414 * self.h * self.d
        self.x = self.b / 2
        self.y = self.d / 2
        self.Iu = self.d**3 / 6
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 2'
    
    def get_group_3_attributes(self, **kwargs):
        # Shape: =
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 1.414 * self.h * self.b
        self.x = self.b / 2
        self.y = self.d / 2
        self.Iu = self.b * self.d**2 / 2
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 3'
    
    def get_group_4_attributes(self, **kwargs):
        # Shape: C channel
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 0.707 * self.h * (2*self.b + self.d)
        self.x = self.b**2/(2 * self.b + self.d)
        self.y = self.d / 2
        self.Iu = self.d**2/12 * (6 * self.b + self.d)
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 4'
    
    def get_group_5_attributes(self, **kwargs):
        # Shape: |_|
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 0.707 * self.h * (self.b + 2 * self.d)
        self.x = self.b / 2
        self.y = self.d**2 / (self.b + 2 * self.d)
        self.Iu = 2 * self.d**3 / 3 - 2 * self.d**2 * self.y + (self.b + 2 * self.d) * self.y**2
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 5'
    
    def get_group_6_attributes(self, **kwargs):
        # Shape: []
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 1.414 * self.h * (self.b + self.d)
        self.x = self.b / 2
        self.y = self.d / 2
        self.Iu = self.d**2 / 6 * (3 * self.b + self.d)
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 6'
    
    def get_group_7_attributes(self, **kwargs):
        # Shape: T
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 0.707 * self.h * (self.b + 2 * self.d)
        self.x = self.b / 2
        self.y = self.d**2 / (self.b + 2 * self.d)
        self.Iu = 2 * self.d**3 / 3 - 2 * self.d**2 * self.y + (self.b + 2 * self.d) * self.y**2
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 7'
    
    def get_group_8_attributes(self, **kwargs):
        # Shape: I
        if kwargs:
            self._update_attributes(**kwargs)
        self.A = 1.414 * self.h * (self.b + self.d)
        self.x = self.b / 2
        self.y = self.d /2
        self.Iu = self.d**2 / 6 * (3 * self.b + self.d)
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 8'

    def get_group_9_attributes(self, **kwargs):
        # Shape: O
        if kwargs:
            self._update_attributes(**kwargs)
        if self.r == 1:
            print('Group 9 in bending is a circular weld, the default of r=1 has been recognized.  You can specify the radius input while calling get_group_9_attributes if' 
                   'you would like to change it')
        self.A = 1.414 * pi * self.h * self.r
        self.x = 0
        self.y = 0 
        self.Iu = pi * self.r**3
        self._update_moment_of_areas()
        self.group = 'Chapter 9, Table 9-2, Group 9'

class StressCalcs():
    """
    After a torsional or a bending object has been created and has called get_group_X_attributes, this object can be used to perform calculations. 
    """
    def __init__(self, torsion_or_bending_object):
        self.weld_group = torsion_or_bending_object
        self.tau_prime = 0
    
    def __repr__(self):
        print(self.weld_group.__class__)
        self.weld_group.__repr__()
        return ''
        

    def primary_shear(self, force):
        """
        tau prime = V/Atotal 
        """
        self.tau_prime = force/self.weld_group.A
        print('The primary shear seen at all weld locations is: {} units'.format(self.tau_prime))
    
    def secondary_shear(self, list_of_moment_tuples):
        '''
        tau double prime = Mr/I

        list_of_moment_tuples: [(force1, distance1), (force2, distance2)]
            distance: scalar, evaluated as an absolute value
            force: vector, sign convention is up to the programmer
        '''
        M_sum = 0
        for couple in list_of_moment_tuples:
            M_sum += couple[0] * abs(couple[1])

        if M_sum == 0:
            print("Sum of moments about your geometry is equal to 0, there must be symmetry in your structure. Re-evaluate shape and try again")
        
        if self.weld_group.I:
            self.tau_d_prime = M_sum / self.weld_group.I
        elif self.weld_group.J:
            self.tau_d_prime = M_sum / self.weld_group.J
            print("The moment seen at the centroid is: {} units".format(self.tau_d_prime))

    

        