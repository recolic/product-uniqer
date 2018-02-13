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
    
    def get_meter_per_unit(self): # deprecated
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
    
    def get_meter_per_unit(self): # deprecated
        return self.m_class.get_meter_per_unit()
    
    def get_unit_amount(self, length):
        return self.m_class.get_unit_amount(length)

material_class_list = [
    material_class('扁钢', 2, (lambda args, length: args[0] * args[1] * length), 7850, 6), 
    material_class('圆钢', 1, (lambda args, length: 3.14159265 * args[0] * args[0] * length / 4), 7850, 9), 
    material_class('圆管', 2, (lambda args, length: 3.14159265 * args[0] * (args[1] - args[0]) * length), 7850, 6), 
    material_class('矩形管', 3, (lambda args, length: 2 * args[2] * (args[1]+args[0]+2*args[2]) * length), 7850, 6), 
    material_class( '方管' , 2, (lambda args, length: 4 * args[1] * (args[0]+args[1]) * length), 7850, 6), 
    material_class('不等边角钢', 3, (lambda args, length: args[0] * (args[1]+args[2]-args[0]) * length), 7850, 6), 
    material_class('等边角钢', 3, (lambda args, length: args[0] * (args[1]+args[1]-args[0]) * length), 7850, 6), 
]

'''
material arguments:
name arg1 arg2 ...
扁钢 厚度 宽度
圆钢 直径
圆管 厚度 外直径
矩形管 厚度 a b
角钢 厚度 a b
'''

def material_find_class_obj(class_name):
    global material_class_list
    for cls in material_class_list:
        if cls.name == class_name:
            return cls
    raise KeyError('material class `{}` not found.'.format(class_name))