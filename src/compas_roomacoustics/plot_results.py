import rhinoscriptsyntax as rs

def visualize_rays(rays, keys=None, ref_order=None, layer='Default'):
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
                print rays[rk]['reflections'][ref_k]['power'].values()
                string =  ', '.join("{0} {1}".format(p[0], p[1]) for p in rays[rk]['reflections'][ref_k]['power'].iteritems())
        else:
            for lk in lkeys:
                u, v = rays[rk]['reflections'][lk]['line']
                line = rs.AddLine(u, v)
                string =  ', '.join("{0} {1}".format(p[0], p[1]) for p in rays[rk]['reflections'][lk]['power'].iteritems())
        rs.ObjectName(line, string)
