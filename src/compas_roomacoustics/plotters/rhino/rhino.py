from __future__ import print_function
import rhinoscriptsyntax as rs

from compas.utilities.colors import i_to_rgb

def visualize_rays(room, keys=None, ref_order=None, layer='Default', dot=None):

    rs.CurrentLayer(layer)
    if not keys:
        keys = room.ray_lines.keys()
    for rk in keys:
        if ref_order:
            ref_k = ref_order
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
                if dot == 'key':
                    rs.AddTextDot(str(lk), rs.CurveMidPoint(line))

def plot_spl(room, spl, frequency):
    spls = [spl[rec][frequency] for rec in spl]
    minspl = min(spls)
    maxspl = max(spls)
    for rec in spl:
        value = spl[rec][frequency]
        pt = room.receivers[rec]['xyz']
        sph = rs.AddSphere(pt, .2)
        rs.ObjectName(sph, str(value))
        i = (((value - minspl) * (1 - 0)) / (maxspl - minspl)) + 0
        color = i_to_rgb(i)
        # print(minspl, maxspl, value, i, color)
        rs.ObjectColor(sph, color)