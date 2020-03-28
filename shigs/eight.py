'''
Chapter 8: Fasteners and bolted joints! My first entry is going to be high level tools for quick joint stiffness calculations - Jasman
'''
from two import Material, Message
from pprint import pprint
from math import pi

class Bolt():
    table_8_2 = {
        '0.19': {'24': 0.0175,
                 '32': 0.0200},
        '0.216': {'24': 0.0242,
                 '28': 0.0258},
        '0.25': {'20': 0.0318,
                 '28': 0.0364},
        '0.313': {'18': 0.0524,
                 '24': 0.058},
        '0.375': {'16': 0.0775,
                 '24': 0.0878},
        '0.438': {'14': 0.1063,
                 '20': 0.1187},
        '0.5': {'13': 0.1419,
                 '20': 0.1599},
        '0.563': {'12': 0.182,
                 '18': 0.203},
        '0.625': {'11': 0.226,
                 '18': 0.256},
        '0.75': {'10': 0.334,
                 '16': 0.373},
        '0.875': {'9': 0.462,
                 '14': 0.509},
        '1.0': {'8': 0.606,
                 '12': 0.663},
        '1.25': {'7': 0.969,
                 '12': 1.073},
        '1.5': {'6': 1.405,
                 '12': 1.581}
    }
    def __init__(self, diam, tpi=1, grade=8):
        self.diam = diam
        self.grade = grade
        self.tpi = tpi # threads per inch
        self.A = self.diam ** 2 * pi / 4
        self.torque = 1
        self.desired_preload = 1
        self.tensile_stress = 1
        self.thread_tensile_area = 1
        self._table_8_9()
        self._table_8_2()
    
    def _table_8_9(self):
        '''
        Function Purpose: to lookup allowable criteria based on bolt grade. See table 8-9 on pg 433 for more details
        Units: ksi
        '''
        if self.grade == 1:
            self.min_proof_strength = 33000
            self.min_ten_strength = 60000
            self.min_yield_strength = 36000
        elif self.grade == 2:
            if self.diam < .75:
                self.min_proof_strength = 55000
                self.min_ten_strength = 74000
                self.min_yield_strength = 57000
            elif self.diam > 0.75:
                self.min_proof_strength = 33000
                self.min_ten_strength = 60000
                self.min_yield_strength = 36000
        elif self.grade == 4:
            self.min_proof_strength = 65000
            self.min_ten_strength = 115000
            self.min_yield_strength = 100000
        elif self.grade == 7:
            self.min_proof_strength = 105000
            self.min_ten_strength = 133000
            self.min_yield_strength = 115000
        elif self.grade == 8:
            self.min_proof_strength = 120000
            self.min_ten_strength = 150000
            self.min_yield_strength = 130000

    def _table_8_2(self):
        self.thread_tensile_area = self.table_8_2[str(round(self.diam, 3))][str(self.tpi)]
        
    def change_diam(self, d, tpi=1):
        self.diam = d
        self.tpi = tpi

    def calculate_torque(self, desired_preload):
        self.torque = 0.2 * desired_preload * self.diam
        self.desired_preload = desired_preload
        self.tensile_stress = self.desired_preload / self.A

    def __repr__(self):
        pprint(self.__dict__)
        return ''
        

class BoltedJoint():
    '''
    class purpose: to allow sizing of bolted joint reference 8-7 on page 435 for further details
                   the class is intended to be flexible to allow for changing of values and re calculating 
                   of attributes. 
                   
                   run ._set(param=value) to change an attribute eg. .set(F_i=56000)
                   run .check_joint() to scan for any properties still set to 1 or 0 
    '''
    def __init__(self, **kwargs):
        self.F_i = 0  # Preload
        self.P_total = 0 # Total external load on the joint
        self.P = 0  #  External Load per bolt
        self.P_b = 0  # Load taken by bolt
        self.P_m = 0  # Load taken by members
        self.F_b = 0  # Resultant bolt load
        self.F_m = 0  # Resultant member load
        self.C_b = 0  # fraction of external load self.P carried by bolt
        self.C_m = 0  # fraction of external load self.P carried by member
        self.n = 1  # number of bolts in the joint
        self.bolt_grip_length = 0
        self.k_b = 1 # bolt stiffness
        self.k_m = 0 # member stiffness
        self._set(**kwargs)
        self._re_calculate()

    def _table_8_12(self):
        if self.bolt_grip_length >= 4:
            self.k_b = 1.37 # Mega * lb / in
            self.k_m = 10.63 # Mega * lb / in
            self.C_b = .114 # %
            self.C_m = .886 # %
        elif self.bolt_grip_length >= 3:
            self.k_b = 1.79 # Mega * lb / in
            self.k_m = 11.33 # Mega * lb / in
            self.C_b = .136 # %
            self.C_m = .864 # %
        elif self.bolt_grip_length >= 2:
            self.k_b = 2.57 # Mega * lb / in
            self.k_m = 12.69 # Mega * lb / in
            self.C_b = .168 # %
            self.C_m = .832 # %

    def _re_calculate(self):
        self._table_8_12()
        self.P = self.P_total/self.n
        self.P_b = self.C_b * self.P
        self.P_m = self.P_b * self.k_m / self.k_b
        self.F_b = self.P_b + self.F_i
        self.F_m = self.P_m - self.F_i
    
    def _set(self, **kwargs):
        bad_keywords = []
        for k in kwargs:
            if k not in self.__dict__:
                bad_keywords.append(k)
            if k in self.__dict__:
                self.__dict__.update({k: kwargs[k]})
        
        if bad_keywords:
            print('Unrecognized keyword argument(s) passed:')
            print(bad_keywords)
            print('')
            print('Allowed options:')
            print(self.__dict__)
        
        self._re_calculate()
    
    def check_joint(self):
        for idx, key in enumerate(self.__dict__):
            if self.__dict__[key] == 1 or self.__dict__[key] == 0:
                if idx == 0:
                    Message('')
                    Message('---------------------------------------------')
                    Message('There are still values to reconcile:')
                else:
                    Message('{key} is still equal to {val}'.format(key=key, val=self.__dict__[key]))
                Message('---------------------------------------------')
            
        if Message._repo:
            for message in Message._repo:
                print(message.message)
            Message._repo = []
        
        else:
            self.__repr__

    def __repr__(self):
        pprint(self.__dict__)
        return ''
        

        
                
def quick_stiffness_estimate(bolt_diameter, member_1_thickness, member_2_thickness=0):
    '''
    Function Purpose: References the exponential emperical study for joint member stiffness estimates see table 8-8 on pg 430 for more information

    Inputs: bolt diameter in inches
            member_1_thickness = member thickness directly under the bolt head
            member_2_thickness = member thickness between member_1 and the nut (optional)
        
    Outputs: k_m = joint stiffness in Mega * lb/in
    '''
    Material('steel', E=30,  A=.78715, B=.62873, poisson=0.291)
    Material('aluminum', E=10.3, A=0.79670, B=.63816, poisson=.334)
    Material('copper', E=17.3, A=0.79568, B=.63553, poisson=.326)
    Material('gray_cast_iron', E=14.5, A=0.77871, B=.61616, poisson=.211)
    Material('general_expression', E=1, A=0.78952, B=.62914, poisson=1)
    table_8_8 = Material._repo
    print('')
    print('------------------------------------------------------------------------------')
    print('If member_1 and member_2 are different materials refer to eqn 8-20 on page 429')
    print('Options:')
    print(table_8_8.keys())
    print('')
    user = input('Which material is your joint made out of?')
    if user.lower().startswith('s'):
        mat = table_8_8['steel']
    elif user.lower().startswith('a'):
        mat = table_8_8['aluminum']
    elif user.lower().startswith('c'):
        mat = table_8_8['copper']
    elif user.lower().startswith('gray'):
        mat = table_8_8['gray_cast_iron']
    elif user.lower().startswith('gen'):
        mat = table_8_8['general_expression']

    k_m = mat.E * bolt_diameter * mat.A ** (mat.B * bolt_diameter / (member_1_thickness+member_2_thickness))
    return k_m
    
    
def calculate_total_stiffness(*args):
    '''
    Function Purpose: to calculate effective stiffness based on k_ms

    Inputs: *args in a list 1/k_mtotal = 1/k_1 + 1/k_2... etc

    Output: effective_stiffness
    '''
    joint_stiffness = 1
    for arg in args:
        joint_stiffness += 1/arg
    return 1/joint_stiffness
