from __future__ import print_function

from math import log10
from math import sqrt
from math import pi

from compas.geometry import distance_point_line
from compas.geometry import closest_point_on_line
from compas.geometry import distance_point_point

def make_histogram(room):
    """This function records the energy from rays that intersect spherical
    recievers of a given radius. The energy is stored in watts, as
    fractions of the initial source power W. Sound intensity is calculated
    according to Xiangyang et al.
    """
    dt = room.dt

    #  TODO: do this in a dict comprehension
    histogram = {}  #{rec: {fk: freq[fk]} for fk in freq for rec in room.receivers}
    for reck in room.receivers:
        histogram[reck] = {}
        for frek in room.freq:
            histogram[reck][room.freq[frek]] ={}

    #  TODO: this should be done via dict comprehension
    intensity = {}
    for reck in room.receivers:
        intensity[reck] = {}
        for frek in room.freq:
            intensity[reck][room.freq[frek]] ={}

    for rayk in room.ray_lines:
        time = 0
        for refk in room.ray_lines[rayk]:
            line    = room.ray_lines[rayk][refk]
            time    += room.ray_times[rayk][refk]
            for reck in room.receivers:
                rec_xyz = room.receivers[reck]['xyz']
                rec_r   = room.receivers[reck]['radius']
                rec_v   = room.receivers[reck]['volume']
                is_mic, d = is_line_in_shere(line, rec_xyz, rec_r)
                if is_mic:
                    for frek in room.ray_powers[rayk][refk]:
                        # TODO: There is something not great with freq keys and their serialization
                        w = room.ray_powers[rayk][refk][frek]
                        d_ = distance_point_point(closest_point_on_line(rec_xyz, line), rec_xyz)
                        t = int((d_ / 343.0) * 1000)
                        time_ = time + t

                        timek = str((time_ // int(dt) * int(dt), time_ // int(dt) * int(dt) + dt))
                        insphere = sqrt(rec_r ** 2 - d ** 2) * 2

                        i = (w * insphere) / rec_v
                        histogram[reck][frek][timek] = histogram[reck][frek].get(timek, 0) + w
                        intensity[reck][frek][timek] = intensity[reck][frek].get(timek, 0) + i
    return histogram, intensity

def spl_from_intensity(intensity):
    spl = {}
    for rec in intensity:
        spl[rec] = {}
        for frek in intensity[rec]: 
            ilist = [intensity[rec][frek][t] for t in intensity[rec][frek]]
            i = sum(ilist)
            if i == 0:
                spl[rec][frek] = 0
            else:
                spl[rec][frek] = 120 + 10 * log10(i)
    return spl

def is_line_in_shere(line, cpt, r):
    d = distance_point_line(cpt, line)
    return d <= r, d

if __name__ == '__main__':
    import sys
    sys.path.append('/Users/time/Documents/UW/04_code/compas_roomacoustics/src')

    import os
    import compas_roomacoustics as cra
    from room import Room

    fp = os.path.join(cra.TEMP, 'testing.json')
    r = Room.from_json(fp)
    histo, intsty = make_histogram(r)
    for k in histo:
        print(k, histo[k])
        print('')
