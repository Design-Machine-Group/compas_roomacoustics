from math import log10
from math import sqrt
from math import pi

from ast import literal_eval
import json

from geometry import distance_point_line
from geometry import closest_point_on_line
from geometry import distance_point_point


def is_line_in_shere(line, cpt, r):
    d = distance_point_line(cpt, line)
    return d <= r, d


def make_histogram(rays, scene, dt=1, exclude_direct=False):
    """This function records the energy from rays that intersect spherical
    recievers of a given radius. The energy is stored in watts, as
    fractions of the initial source power W. Sound intensity is calculated
    according to Xiangyang et al.
    """
    recs = scene['recs']
    histogram = {str(rec): {} for rec in recs}
    intensity = {str(rec): {} for rec in recs}
    for rk in rays:
        refks = sorted(rays[rk]['reflections'].keys())
        time = 0
        length = 0 ### this line of code is for ISRA only, not real thing!!!!
        for refk in refks:
            if exclude_direct and refk == 0:
                    continue
            # print rk, refk
            ref = rays[rk]['reflections'][refk]
            line = ref['line']
            time += ref['time']
            length += ref['length'] ### this line of code is for ISRA only, not real thing!!!!
            w = ref['power']
            for rec in recs:
                rec_xyz = recs[rec]['xyz']
                rec_r = recs[rec]['r']
                rec_v = recs[rec]['v']
                is_mic, d = is_line_in_shere(line, rec_xyz, rec_r)
                if is_mic:
                    d_ = distance_point_point(closest_point_on_line(rec_xyz, line), rec_xyz)
                    t = int((d_ / 343.0) * 1000)
                    time_ = time + t

                    # length_ = length + d_ ### this line of code is for ISRA only, not real thing!!!!
                    # w /= (length_ ** 2) ### this line of code is for ISRA only, not real thing!!!!

                    timek = str((time_ // int(dt) * int(dt), time_ // int(dt) * int(dt) + dt))
                    insphere = sqrt(rec_r ** 2 - d ** 2) * 2

                    # w *= insphere / (rec_r * 2)
                    i = (w * insphere) / rec_v
                    histogram[rec][timek] = histogram[rec].get(timek, 0) + w
                    intensity[rec][timek] = intensity[rec].get(timek, 0) + i
    return histogram, intensity


def dict_to_json(dictionary, filepath):
    with open(filepath, 'w+') as fp:
        json.dump(dictionary, fp)


def spl_from_intensity(intensity):
    spl = {}
    for rec in intensity:
        ilist = [intensity[rec][p] for p in intensity[rec]]
        i = sum(ilist)
        if i == 0:
            spl[rec] = 0
        else:
            spl[rec] = 120 + 10 * log10(i)
    return spl


def histogram_to_csv(histogram, intensity, filepath, sourcept, dt=3):

    numrec = len(histogram)
    fh = open(str(filepath), "wb")
    fh.write("Diffusion tool results")
    fh.write('\n')
    fh.write('\n')
    fh.write('Number of recievers\n')
    fh.write(str(numrec) + '\n')
    fh.write('Source Point')
    fh.write('\n')
    fh.write('{0},{1},{2}\n'.format(sourcept[0], sourcept[1], sourcept[2]))
    fh.write('\n')
    fh.write('\n')
    maxt = 300  # this value should be generated automatically based on the data
    tkeys = ['({0}, {1})'.format(i, i + dt) for i in range(0, maxt, dt)]


    for rkey in histogram:
        xyz = literal_eval(rkey)
        fh.write('reciever coordinates, {0},{1},{2}\n'.format(xyz[0], xyz[1], xyz[2]))
        fh.write('time window (ms),')
        for tkey in tkeys:
            temp = tkey.split(',')
            fh.write('{0}_{1},'.format(temp[0], temp[1]))
        fh.write('\n')
        fh.write('energy (w),')
        for tkey in tkeys:
            if tkey in histogram[rkey]:
                value = histogram[rkey][tkey]
            else:
                value = 0.
            fh.write('{0},'.format(value))
        fh.write('\n')
        fh.write('intensity (w/m2),')
        for tkey in tkeys:
            if tkey in intensity[rkey]:
                value = intensity[rkey][tkey]
            else:
                value = 0.
            fh.write('{0},'.format(value))

        fh.write('\n')
        fh.write('\n')
    fh.write('\n')

    fh.close()


def spl_to_csv(spl, filepath):
    xyz_list = [literal_eval(key) for key in spl]
    spl_list = [spl[key] for key in spl]

    minspl = min(spl_list)
    maxspl = max(spl_list)
    fh = open(str(filepath), "wb")
    fh.write("Diffusion tool SPL results")
    fh.write('\n')
    fh.write('\n')
    fh.write('min SPL = {0}\n'.format(minspl))
    fh.write('max SPL = {0}\n'.format(maxspl))
    fh.write('\n')

    fh.write('x,')
    for xyz in xyz_list:
        fh.write('{0},'.format(xyz[0]))
    fh.write('\n')

    fh.write('y,')
    for xyz in xyz_list:
        fh.write('{0},'.format(xyz[1]))
    fh.write('\n')

    fh.write('z,')
    for xyz in xyz_list:
        fh.write('{0},'.format(xyz[2]))
    fh.write('\n')

    fh.write('SPL,')
    for s in spl_list:
        fh.write('{0},'.format(s))
    fh.write('\n')

    fh.close()


if __name__ == '__main__':

    import time
    import os

    model_name = 'test'
    dt = 3

    here = os.path.dirname(__file__)
    folder = os.path.join(here, 'results')
    rname = 'rays_{0}.json'.format(model_name)
    recname = 'recs_{0}.json'.format(model_name)
    csvfileapth = os.path.join(folder, 'timecurves_{0}.csv'.format(model_name))
    csvfileapth_ = os.path.join(folder, 'timecurves_nodirect_{0}.csv'.format(model_name))
    spl_filepath = os.path.join(folder, 'spl_{0}.csv'.format(model_name))
    spl_filepath_ = os.path.join(folder, 'spl_nodirect_{0}.csv'.format(model_name))

    with open(os.path.join(folder, rname)) as jf:
        rays = json.load(jf)

    with open(os.path.join(folder, recname)) as jf:
        recs = json.load(jf)

    tic = time.time()
    hist, intensity = make_histogram(rays, recs, dt=dt, exclude_direct=False)
    hist_, intensity_ = make_histogram(rays, recs, dt=dt, exclude_direct=True)

    histogram_to_csv(hist, intensity, csvfileapth, (0, 0, 10.), dt)  # the source should not be guessed...
    histogram_to_csv(hist_, intensity_, csvfileapth_, (0, 0, 10.), dt)

    spl = spl_from_intensity(intensity)
    spl_ = spl_from_intensity(intensity_)
    spl_to_csv(spl, spl_filepath)
    spl_to_csv(spl_, spl_filepath_)

    # iname = os.path.join(folder, 'intensity_{0}.json'.format(model_name))
    splname = os.path.join(folder, 'spl_{0}.json'.format(model_name))
    splname_ = os.path.join(folder, 'spl_nondirect_{0}.json'.format(model_name))

    # dict_to_json(intensity, iname)
    dict_to_json(spl, splname)
    dict_to_json(spl_, splname_)
    toc = time.time()
    print ('calculation time', toc - tic)
