import math, re, time, clr, os, json
import Rhino, scriptcontext
import rhinoscriptsyntax as rs

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
import Pachyderm_Acoustic.Utilities.AcousticalMath as pm
import Hare.Geometry.Point as hpt
import wave,struct


def geometric_key(xyz, precision='3f'):
    x, y, z = xyz
    return '{0:.{3}},{1:.{3}},{2:.{3}}'.format(x, y, z, precision)

def make_mic_map(mics):
    m = {geometric_key(mic): {'index':i, 'xyz': mic} for i, mic in enumerate(mics)}
    return m

def pach_assign_material(guid, abs, sct, trn):
    abs = Array[int](abs)
    sct = Array[int](sct)
    trn = Array[int](trn)
    pt.Material_SetByObject(guid, abs, sct, trn)

def etcs_to_json(filepath, etcs):
    for mic in etcs:
        for oct in etcs[mic]:
            etcs[mic][oct] = list(etcs[mic][oct])

    with open(filepath, 'w+') as fp:
        json.dump(etcs, fp)

def assign_materials_by_layer(lay_dict):
    for lay in lay_dict:
        srfs = rs.ObjectsByLayer(lay)
        abs = lay_dict[lay]['abs']
        sct = lay_dict[lay]['sct']
        trn = lay_dict[lay]['trn']
        for srf in srfs:
            pach_assign_material(srf, abs, sct, trn)

def pach_run(src, mics, num_rays=1000, max_duration=2000, image_order=2):

    rec = NetList[hpt]()
    for mic in mics:
        rec.Add(hpt(mic[0], mic[1], mic[2]))

    src_h = hpt(src[0], src[1], src[2])
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
    swl = tuple([100.] * 8)
    Source = env.GeodesicSource(swl, src_h, 0)
    SourceIE = NetList[type(Source)]()
    SourceIE.Add(Source)
    receiver = pt.GetReceivers(rec, SourceIE, num_rays ,max_duration, 0, scene)

    # - Direct Sound Calculation -----------------------------------------------
    D = pach.Direct_Sound(Source, receiver[0], scene,octaves)
    Dout = pt.Run_Simulation(D)

    # - Source Image Calculation -----------------------------------------------
    IS = pach.ImageSourceData(Source,receiver[0], D, scene, image_order, 0)
    ISout = pt.Run_Simulation(IS)

    # - Ray Tracing  Calculation -----------------------------------------------
    RT = pach.SplitRayTracer(Source,
                             receiver[0],
                             scene,
                             max_duration,
                             octaves,
                             image_order,
                             num_rays)

    RTout = pt.Run_Simulation(RT)
    receiver_out = RTout.GetReceiver

    # - Energy Time Curves Calculation -----------------------------------------
    etcs = {}
    for i in range(len(mics)):
        gk = geometric_key(mics[i])
        etcs[gk] ={}
        for oct in range(8):
            etc =  ir.ETCurve(Dout, ISout, receiver_out, max_duration, 1000, oct, i, True)
            etcs[gk][oct] = etc
    return etcs

def pach_sch_int(etcs):
    sch_int = {}
    for rec in etcs:
        sch_int[rec] = {}
        for oct in etcs[rec]:
            etc = Array[float](etcs[rec][oct])
            sch = pm.Schroeder_Integral(etc)
            sch_int[rec][oct] = sch
    return sch_int

def pach_edt(sch_int):
    edt = {}
    for rec in sch_int:
        edt[rec] = {}
        for oct in sch_int[rec]:
            sch = sch_int[rec][oct]
            edt[rec][oct] = pm.EarlyDecayTime(sch, 1000)
    return edt
    
def pach_t30(sch_int):
    t30 = {}
    for rec in sch_int:
        t30[rec] = {}
        for oct in sch_int[rec]:
            sch = sch_int[rec][oct]
            t30[rec][oct] = pm.T_X(sch, 30, 1000)
    return t30

def pach_sti(etcs):
    sti = {}
    for rec in etcs:
        sti[rec] = {}
        etcs_arr = [Array[float](etcs[rec]) for oct in etcs[rec]]
        etc = Array[Array[float]](etcs_arr)
        rho_c = 342.2 * 1000.1
        noise = [40.] * 8
        noise = Array[float](noise)
        samplefreq = 4
        sti[rec] = pm.Speech_Transmission_Index(etc, rho_c, noise, samplefreq)
    return sti

if __name__ == '__main__':
    
    from rhino_to_json import draw_model_from_json

    rs.DeleteObjects(rs.AllObjects())

    # load model from json file ------------------------------------------------

    filepath = 'simple_box.json'

    draw_model_from_json(filepath, mesh=False)
    rs.CurrentLayer('Default')
    # user input ---------------------------------------------------------------
    w = {'abs': [17., 15., 10., 6., 4., 4., 5., 6.], 'sct': [.2] * 8, 'trn': [0] * 8}
    
    lay_dict = {'walls': w}
    
    # run simulation -----------------------------------------------------------
    src = rs.PointCoordinates(rs.ObjectsByLayer('src')[0])
    mics = [rs.PointCoordinates(rpt) for rpt in rs.ObjectsByLayer('mics')]
    
    mic_map = make_mic_map(mics)
    
    
    for k in mic_map:
        rs.AddTextDot(str(mic_map[k]['index']), mic_map[k]['xyz'])
    
    assign_materials_by_layer(lay_dict)
    etcs = pach_run(src, mics, num_rays=10000, max_duration=2000)
    
    filepath = 'etcs.json'
    etcs_to_json(filepath, etcs)
    sch_int = pach_sch_int(etcs)
    edt = pach_edt(sch_int)
    t30 = pach_t30(sch_int)
    sti = pach_sti(etcs)
    names = ['edt', 't30', 'sti']
    
    for i, index in enumerate([edt, t30, sti]):
        print names[i]
        for j in index:
            print index[j]
