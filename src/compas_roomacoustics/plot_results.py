import rhinoscriptsyntax as rs

def visualize_rays(room, keys=None, ref_order=None, layer='Default', dot=None):
    rs.CurrentLayer(layer)
    if not keys:
        keys = room.ray_lines.keys()
    for rk in keys:
        if ref_order:
            ref_k = ref_order - 1
            if ref_k in room.ray_lines[rk]:
                u, v = room.ray_lines[rk][ref_k]
                line = rs.AddLine(u, v)
        else:
            lkeys = room.ray_lines[rk]
            for lk in lkeys:
                u, v = room.ray_lines[rk][lk]
                line = rs.AddLine(u, v)
                if dot == 'w':
                    w = room.ray_powers[rk][lk][100] # this needs to be better, user given
                    rs.AddTextDot(str(w), rs.CurveMidPoint(line))
                if dot == 't':
                    t = room.ray_times[rk][lk]
                    rs.AddTextDot(str(t), rs.CurveMidPoint(line))
