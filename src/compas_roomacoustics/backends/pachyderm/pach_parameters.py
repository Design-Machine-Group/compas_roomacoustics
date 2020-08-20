from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from System import Array
import Pachyderm_Acoustic.Utilities.AcousticalMath as pm


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

def pach_sti(etcs, room):
    sti = {}
    for rec in etcs:
        sti[rec] = {}
        etcs_arr = [Array[float](etcs[rec]) for oct in etcs[rec]]
        etc = Array[Array[float]](etcs_arr)
        rho_c = 342.2 * 1000.1
        noise = [room.noise[nk] for nk in sorted(list(room.noise.keys()), key=float)]
        noise = Array[float](noise)
        samplefreq = 4
        sti[rec] = pm.Speech_Transmission_Index(etc, rho_c, noise, samplefreq)
    return sti