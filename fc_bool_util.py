import bpy
from bpy.props import *

def execute_boolean_op(context, target_obj, bool_method = 0):
    '''
    function for bool operation
    @target_obj : target object of the bool operation
    @bool_method : 0 = difference, 1 = union, 2 = intersect  
    '''

    # store active object
    current_obj = context.object
    
    bpy.ops.object.transform_apply(scale=True)
    
    # make target the active object
    bpy.context.scene.objects.active = target_obj
    
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bool_mod = target_obj.modifiers[-1]
    
    bool_mod.object = current_obj

    method = 'DIFFERENCE'
    
    if bool_method == 1:
        method = 'UNION'
    elif bool_method == 2:
        method = 'INTERSECT'
        
    bool_mod.operation = method
    bool_mod.solver = 'CARVE'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    bpy.context.scene.objects.active = current_obj