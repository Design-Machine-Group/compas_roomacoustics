from __future__ import print_function
import rhinoscriptsyntax as rs
import json

from compas.geometry import distance_point_point
from compas.geometry import vector_from_points

from copy import deepcopy


def shoot_rays(room):
    """Performs the raytracing process using the room properties. Calculates
    all reflections, including geometry, times and energy values per segment.

    Parameters
    ----------
    room: object
        The room object to be analyzed.

    """
    # TODO: Figure out if it is possible to cut ray one reflection short.
    # TODO: how to get rid of deepcopy? it is super slow.
    # TODO: should propably use some generators, is that possible?

    directions = room.source.directions
    ref_srf = [room.surfaces[gk]['guid'] for gk in room.surfaces]
    ref_map = {room.surfaces[sk]['guid']:sk for sk in room.surfaces}

    room.ray_times = {dk: {} for dk in directions}
    room.ray_lengths = {dk: {} for dk in directions}
    room.ray_powers = {dk: {} for dk in directions}
    room.ray_lines = {dk: {} for dk in directions}

    for dk in directions:
        dir         = directions[dk]
        src_        = room.source.xyz
        w           = room.source.ray_power[dk]
        min_w       = room.source.ray_minpower[dk]
        time        = 0
        i           = 0
        min_power   = False
        while time < room.ctime and not min_power:
            i += 1
            ray = rs.ShootRay(ref_srf, src_, dir, 2)
            srf = rs.PointClosestObject(ray[0], ref_srf)[0]
            mp_list = []
            if i > 0:
                sk = ref_map[str(srf)]
                abs = room.materials[room.surfaces[sk]['material']].absorption
                for wk in w:
                    w[wk] *= (1 - abs[wk])
                    mp_list.append(w[wk] < min_w[wk])
            min_power = all(mp_list)
            l = distance_point_point(ray[0], ray[1])
            t = int((l / 343.0) * 1000)
            room.ray_times[dk][i] = t
            room.ray_lengths[dk][i] = l
            room.ray_powers[dk][i] = deepcopy(w)
            room.ray_lines[dk][i] = ((ray[0].X, ray[0].Y, ray[0].Z),(ray[1].X, ray[1].Y, ray[1].Z))
            dir = vector_from_points(ray[1], ray[2])
            src_ = ray[1]
            time += t


if __name__ == '__main__':
    import os
    import compas_roomacoustics as cra
    import room
    reload(room)
    from room import Room

    import material
    reload(material)
    from material import Material

    import plot_results
    reload(plot_results)
    from plot_results import visualize_rays

    for i in range(50): print('')
    rs.CurrentLayer('Default')
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))

    pts = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer('receivers')]
    srfs = rs.ObjectsByLayer('reflectors')
    srf_ = rs.ObjectsByLayer('back_srf')

    r = Room()
    r.num_rays = 100
    r.add_frequencies(range(100,120))
    srcpt = list(rs.PointCoordinates(rs.ObjectsByLayer('source')[0]))
    r.add_fib_source(srcpt, power=.1)

    r.add_spherical_recs(pts, radius=.3)

    absorption= {fk: .2 for fk in r.freq.values()}
    r.add_material('mat1', absorption)
    r.add_room_surfaces(srfs, 'mat1', True)

    absorption = {fk: .7 for fk in r.freq.values()}
    r.add_material('mat2', absorption)
    r.add_room_surfaces(srf_, 'mat2', True)

    shoot_rays(r)
    # visualize_rays(r, keys= None, ref_order=None, layer='Default', dot=None)
    fp = os.path.join(cra.TEMP, 'testing.json')
    r.to_json(fp)
