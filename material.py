# Copyright (C) 2018  Recolic Keghart <root@recolic.net>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

class material_class():
    def __init__(self, name, want_args, volume_calculator, density, meter_per_unit):
        '''
        Assume all arguments in SI.
        mass = volume_calculator(arg_list, length) * density
        Example: round_steel_pipe = material_class('圆管', 2, 
            (lambda args,len: math.pi*(args[0]^2-(args[0]-args[1])^2))*len, 7850, 6)
        '''
        self.name = name
        self.want_args = want_args
        self.volume_calculator = volume_calculator
        self.density = density
        self.meter_per_unit = meter_per_unit
    
    def get_weight(self, arg_list, length):
        if len(arg_list) < self.want_args:
            raise AssertionError('material {} must have {} arguments, but gave {}.'.format(self.name, self.want_args, len(arg_list)))
        return self.volume_calculator(arg_list, length) * self.density
    
    def get_meter_per_unit(self):
        return self.meter_per_unit
    
    def get_unit_amount(self, length):
        return length / self.meter_per_unit

class material():
    def __init__(self, m_class, arg_list):
        '''
        Give all arguments in SI please!
        Example: pipe_r40_d8 = material(round_steel_pipe, (40*0.001, 8*0.001))
        '''
        self.m_class = m_class
        self.arg_list = arg_list
   
    def get_weight(self, length):
        return self.m_class.get_weight(self.arg_list, length)
    
    def get_meter_per_unit(self):
        return self.m_class.get_meter_per_unit()
    
    def get_unit_amount(self, length):
        return self.m_class.get_unit_amount(length)

material_class_list = [
    material_class('扁钢', 2, (lambda args, length: 1.0001 * args[0] * args[1] * length), 7850, 6),
    material_class('方钢', 1, (lambda args, length: 1.00000 * args[0] * args[0] * length), 7850, 6),
    material_class('板材', 2, (lambda args, length: 1.00000 * args[0] * args[1] * length), 7850, 6), 
    material_class('圆钢', 1, (lambda args, length: 1.00000*3.14159265*args[0]*args[0]*length/4), 7850, 9), 
    material_class('圆管', 2, (lambda args, length: 1.00000*3.14159265*args[1]*(args[0]-args[1])*length), 7850, 6), 
    material_class('矩形管', 3, (lambda args, length: 1.00000*2*args[0]*(args[1]+args[2]+2*args[0])*length), 7850, 6), 
    material_class( '方管' , 2, (lambda args, length: 1.00000*4*args[0]*(args[0]+args[1])*length), 7850, 6), 
    material_class('不等边角钢', 3, (lambda args, length: 1.01493*args[0]*(args[1]+args[2]-args[0])*length), 7850, 6), 
    material_class('等边角钢', 3, (lambda args, length: 1.01493*args[0]*(args[1]+args[1]-args[0])*length), 7850, 6),
    material_class('三角管', 3, (lambda args, length: 1.00000*arg[0]*(arg[1]-arg[0]/2)*length), 7850, 6),
    material_class('三棱钢', 3, (lambda args, length: 1.00000*arg[0]*1000*length), 1, 6), # Be caution to its density! lambda is giving weight rather than volume!
]

'''
material arguments:
All input length is mm. All input weight is kg.
name arg1 arg2 ...
扁钢 厚度 宽度
方钢 宽度
板材 厚度 宽度
圆钢 直径
圆管 外直径 厚度
矩形管 厚度 a b
方管 厚度 a
不等边角钢 厚度 a b
等边角钢 厚度 a
三角管 厚度 边长
三棱钢 每米质量
'''

def material_find_class_obj(class_name):
    global material_class_list
    for cls in material_class_list:
        if cls.name == class_name:
            return cls
    raise KeyError('material class `{}` not found.'.format(class_name))
