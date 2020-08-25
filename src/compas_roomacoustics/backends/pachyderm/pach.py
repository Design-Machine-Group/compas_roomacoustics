from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

# import math, re, time, clr, os, json
# import Rhino, scriptcontext

import clr

clr.AddReference("Pachyderm_Acoustic")
clr.AddReference("Pachyderm_Acoustic_Universal")
clr.AddReference("Rhino_DotNet")
clr.AddReference("Hare")

from System import Array
import System.Collections.Generic.List as NetList
import Pachyderm_Acoustic as pach
import Pachyderm_Acoustic.Environment as env
import Pachyderm_Acoustic.Utilities.RC_PachTools as pt
import Pachyderm_Acoustic.Utilities.IR_Construction as ir
import Hare.Geometry.Point as hpt

from compas.utilities import geometric_key

from compas_roomacoustics.backends.pachyderm import assign_materials_by_layer
from compas_roomacoustics.backends.pachyderm import pach_sch_int
from compas_roomacoustics.backends.pachyderm import pach_edt
from compas_roomacoustics.backends.pachyderm import pach_t30
from compas_roomacoustics.backends.pachyderm import pach_sti
from compas_roomacoustics.backends.pachyderm import pach_c80
from compas_roomacoustics.backends.pachyderm import add_room_surfaces

from compas_roomacoustics.datastructures import Result

# TODO: Source power is still just a hack!


def pach_run(room):
    rec_keys = list(room.receivers.keys())
    rec = NetList[hpt]()
    for rk in rec_keys:
        x, y, z = room.receivers[rk]['xyz']
        rec.Add(hpt(x, y, z))

    x, y, z = room.source.xyz
    src_h = hpt(x, y, z)
    octaves = Array[int]([0, 7])

    # - Acoustic Simulation ----------------------------------------------------
    # - 3d Scene ------
    scene = pt.Get_Poly_Scene(50, True, 20, 101.325, 0, True)

    PTList = NetList[hpt]()
    PTList.Add(src_h)

    for r in rec:
        PTList.Add(r)
    scene.partition(PTList, 10)
    env.RhCommon_PolygonScene.partition(scene, PTList, 10)

    # source power -------------------------------------------------------------
    swl = []
    for pk in sorted(list(room.source.power), key=float):
        swl.append(room.source.power[pk] * 1000)
    swl = tuple(swl)
    Source = env.GeodesicSource(swl, src_h, 0)
    SourceIE = NetList[type(Source)]()
    SourceIE.Add(Source)
    receiver = pt.GetReceivers(rec, SourceIE, room.num_rays, room.ctime, 0, scene)

    # - Direct Sound Calculation -----------------------------------------------
    D = pach.Direct_Sound(Source, receiver[0], scene, octaves)
    dout = pt.Run_Simulation(D)

    # - Source Image Calculation -----------------------------------------------
    IS = pach.ImageSourceData(Source,receiver[0], D, scene, room.image_order, 0)
    ISout = pt.Run_Simulation(IS)

    # - Ray Tracing  Calculation -----------------------------------------------
    RT = pach.SplitRayTracer(Source,
                             receiver[0],
                             scene,
                             room.ctime,
                             octaves,
                             room.image_order,
                             room.num_rays)

    RTout = pt.Run_Simulation(RT)
    receiver_out = RTout.GetReceiver

    # - Energy Time Curves Calculation -----------------------------------------
    etcs = {}
    start_times = {}
    for i, rk in enumerate(rec_keys):
        etcs[rk] = {}
        start_times[rk] = pach.Direct_Sound.Min_Time(dout, i)
        for oct in range(8):
            etc =  ir.ETCurve(dout, ISout, receiver_out, room.ctime, 1000, oct, i, True)
            etcs[rk][oct] = etc
    return {'etcs': etcs, 'start_times': start_times}

def results_from_pach(room, out_data, param, save_curves=False):
    fdict = {'edt': pach_edt,
             't30': pach_t30,
             'sti': pach_sti,
             'c80': pach_c80}
    etcs = out_data['etcs']
    start_times = out_data['start_times']
    sch_int = pach_sch_int(etcs)
    results = {}
    for fk in fdict:
        func = fdict[fk]
        if fk in ['sti']:
            res = func(etcs, room)
        elif fk in ['c80']:
            res = func(etcs, start_times)
        else:
            res = func(sch_int)
        results[fk] = res
    
    
    for rk in room.receivers:
        r = Result(rk, restype='Pachyderm')
        for key in results:
            if key == 'sti':
                r.parameters[key] = {i:v for i, v in enumerate(results[key][rk])}
            else:
                r.parameters[key] = results[key][rk]

        if save_curves:
            sch = {oct: timecurve_to_timedict(sch_int[rk][oct]) for oct in sch_int[rk]}
            r.curves['sch_int'] =  sch
            etc = {oct: timecurve_to_timedict(etcs[rk][oct]) for oct in etcs[rk]}
            r.curves['etc'] = etc

        room.results[rk] = r

def timecurve_to_timedict(curve):
    t = {'{},{}'.format(i, i + 1): v for i, v in enumerate(curve) if v}
    return t

def room_to_pachyderm(room, save_curves=False):
    add_room_surfaces(room)
    out_data = pach_run(room)
    results_from_pach(room, out_data, ['edt', 't30', 'sti'], save_curves=save_curves)

if __name__ == '__main__':

    import os
    import rhinoscriptsyntax as rs
    
    from compas_roomacoustics.datastructures import Room

    rs.DeleteObjects(rs.AllObjects())

    path = 'c:\\users\\tmendeze\\documents\\uw_code\\compas_roomacoustics\\data'
    filename = 'simple_box_allrecs.json'
    room = Room.from_json(os.path.join(path, filename))
    room.noise = {'62': 55, '125': 50, '250': 55, '500': 40, '1000': 35, '2000': 30, '4000': 25, '8000': 20}
    room.num_rays = 10000
    room.ctime = 2000
    room_to_pachyderm(room, save_curves=False)
    room.to_json(os.path.join(path, 'simple_box_allrecs_out.json'))
