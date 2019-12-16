import rhinoscriptsyntax as rs

def visualize_rays(rays, keys=None, ref_order=None, layer='Default', dot=None):
    rs.CurrentLayer(layer)
    if not keys:
        keys = rays.keys()
    for rk in keys:
        lkeys = rays[rk]['reflections']
        if ref_order:
            ref_k = ref_order - 1
            if ref_k in rays[rk]['reflections']:
                u, v = rays[rk]['reflections'][ref_k]['line']
                line = rs.AddLine(u, v)
                key = ref_k
        else:
            for lk in lkeys:
                # print lk, rays[rk]['reflections'][lk]['power']
                u, v = rays[rk]['reflections'][lk]['line']
                line = rs.AddLine(u, v)
                if dot == 'w':
                    w = rays[rk]['reflections'][lk]['power'][100]
                    rs.AddTextDot(str(w), rs.CurveMidPoint(line))
                if dot == 't':
                    t = rays[rk]['reflections'][lk]['time']
                    rs.AddTextDot(str(t), rs.CurveMidPoint(line))
