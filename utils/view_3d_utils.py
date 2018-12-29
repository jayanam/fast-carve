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