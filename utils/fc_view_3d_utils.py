import mathutils

from bpy_extras.view3d_utils import region_2d_to_origin_3d
from bpy_extras.view3d_utils import region_2d_to_location_3d

def get_snap_vertex_indizes(view_rot):
    v1 = round(abs(view_rot[0]), 3)
    v2 = round(abs(view_rot[1]), 3)

    # top / bottom
    if (v1== 1.0 and v2 == 0.0) or (v1==0.0 and v2 == 1.0):
        return (0,1)

    # front / back
    if v1== 0.5 and v2 == 0.5:
        return (1,2)

    # left / right
    if (v1 == 0.707 and v2== 0.707) or (v1 == 0.0 and v2 == 0.0):
        return (0,2)

    return None

def get_grid_snap_pos(pos, overlay3d):
    ratio = overlay3d.grid_scale / overlay3d.grid_subdivisions
    ratio_half = ratio / 2.0
    mod = pos % ratio
    if mod < ratio_half:
        mod = -mod
    else:
        mod = (ratio - mod)

    return mod

def get_view_direction(context):
    rv3d      = context.space_data.region_3d
    view_rot  = rv3d.view_rotation

    dir = view_rot @ mathutils.Vector((0,0,-1))
    return dir.normalized()

def get_mouse_3d_vertex(event, context):
    x, y      = event.mouse_region_x, event.mouse_region_y
    region    = context.region
    rv3d      = context.space_data.region_3d
    view_rot  = rv3d.view_rotation
    overlay3d = context.space_data.overlay
    
    dir = get_view_direction(context) * -context.scene.draw_distance    
            
    vec = region_2d_to_location_3d(region, rv3d, (x, y), dir)

    # we are in ortho mode, so we dont snap
    # TODO: Perhaps we also want to snap in perspective mode?
    #       Could be user-defined
    if not rv3d.is_perspective:
            
        # Now check how to snap the cursor
        ind = get_snap_vertex_indizes(view_rot)
        if ind is not None:               
            vec[ind[0]] = vec[ind[0]] + get_grid_snap_pos(vec[ind[0]], overlay3d)
            vec[ind[1]] = vec[ind[1]] + get_grid_snap_pos(vec[ind[1]], overlay3d)

    return vec