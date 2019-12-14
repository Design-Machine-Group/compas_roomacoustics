import math
import rhinoscriptsyntax as rs

import room
reload(room)
from room import Room

from math import degrees

def make_scene(source, rec_dict, srf_layer):
    #TODO: add make reflectors function (Absorption coefficients from layer names?)
    #TODO: add min enegy as a room property
    reflectors = reflectors_from_layers(srf_layer)
    if source['type'] == 'fibonacci':
        source = fibonacci_source(source)

    recievers = recs_from_layer(rec_dict)
    room = Room()
    room.reflectors = reflectors
    room.recievers = recievers
    room.source = source
    return room

def reflectors_from_layers(srf_layer):
    global_coeff = {'100':.1, '200':.2, '300':.3}
    srfs = rs.ObjectsByLayer(srf_layer)
    reflectors = {}
    for i, srf in enumerate(srfs):
        reflectors[str(srf)] = {'guid': srf, 'abs_coeff': global_coeff}
    return reflectors

def fibonacci_source(source):
    min_power = .03
    n = int(source['n'])
    pt = rs.ObjectsByLayer(source['layer'])[0]
    src_pt = rs.PointCoordinates(pt)

    rs.AddPoint(src_pt)
    offset = 2. / n
    increment = math.pi * (3. - math.sqrt(5.))
    init_rays = {}
    for i in range(n):
        y = ((i * offset) - 1) + (offset / 2)
        r = math.sqrt(1 - pow(y,2))
        phi = (i % n) * increment
        x = math.cos(phi) * r
        z = math.sin(phi) * r
        init_rays[i] = {'v':[x, y, z], 'power': {}, 'min_power': {}}

    w_dict = source['w']
    for wk in w_dict:
        for rk in init_rays:
            init_rays[rk]['power'][wk] = w_dict[wk] / float(n)
            init_rays[rk]['min_power'][wk] = min_power * (w_dict[wk] / float(n))


    source['init_rays'] = init_rays
    source['src_pt'] = src_pt
    return source

def recs_from_layer(rec_dict):
    pts = rs.ObjectsByLayer(rec_dict['layer'])
    rec_r = rec_dict['rec_r']
    recs = {}
    for pt in pts:
        rec = rs.PointCoordinates(pt)
        recs[str(rec)] = {'r': rec_r, 'xyz': rec, 'v':(4./3.) * math.pi * rec_r ** 3}
    return recs

if __name__ == '__main__':
    for i in range(50): print ''
    if not rs.IsLayer('Scene'):
        rs.AddLayer('Scene', color=(50, 50, 255))
    rs.DeleteObjects(rs.ObjectsByLayer('Scene'))
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))
    rs.CurrentLayer('Scene')

    source = {'type': 'fibonacci',
              'layer': 'source',
              'n': 30e3,
              'w': {'100':.1, '200':.1, '300':.1}}


    rec_dict = {'layer': 'recievers',
                'rec_r': .3}

    srf_layer = 'reflectors'
    scene = make_scene(source, rec_dict, srf_layer)
