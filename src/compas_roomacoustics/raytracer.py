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
    #TODO: Figure out if it is possible to cut ray one reflection short

    init_rays = room.source['init_rays']
    ref_srf = [room.surfaces[gk]['guid'] for gk in room.surfaces]
    ref_map = {room.surfaces[sk]['guid']:sk for sk in room.surfaces}


    rays = {}
    for dk in init_rays:
        dir         = init_rays[dk]['v']
        src_        = room.source['xyz']
        w           = room.source['init_rays'][dk]['power']
        min_w       = room.source['init_rays'][dk]['min_power']
        rays[dk]    = {'dir': dir, 'reflections':{}}
        time        = 0
        i           = 0
        min_power   = False
        while time < room.ctime and not min_power:
            i += 1
            ray = rs.ShootRay(ref_srf, src_, dir, 2)
            srf = rs.PointClosestObject(ray[0], ref_srf)[0]
            mp_list = []
            if i > 0:
                sk = ref_map[srf]
                abs = room.surfaces[sk]['material'].absorption
                for wk in w:
                    w[wk] *= (1 - abs[wk])
                    mp_list.append(w[wk] < min_w[wk])
            min_power = all(mp_list)
            l = distance_point_point(ray[0], ray[1])
            t = int((l / 343.0) * 1000)
            rays[dk]['reflections'][i] = {'time': t,
                                          'length': l,
                                          'power': deepcopy(w),
                                          'line': ((ray[0].X, ray[0].Y, ray[0].Z),
                                                   (ray[1].X, ray[1].Y, ray[1].Z))}
            dir = vector_from_points(ray[1], ray[2])
            src_ = ray[1]
            time += t

    room.rays = rays

# def rays_to_json(rays, filepath):
#     with open(filepath, 'w+') as fp:
#         json.dump(rays, fp)
#
# def recs_to_json(recs, filepath):
#     with open(filepath, 'w+') as fp:
#         json.dump(recs, fp)

if __name__ == '__main__':
    import room
    reload(room)
    from room import Room

    from material import Material
    import rhinoscriptsyntax as rs

    import plot_results
    reload(plot_results)
    from plot_results import visualize_rays

    for i in range(50): print ''
    rs.CurrentLayer('Default')
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))

    pts = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer('recievers')]
    srfs = rs.ObjectsByLayer('reflectors')
    srf_ = rs.ObjectsByLayer('back_srf')

    room = Room()
    room.num_rays= 100
    room.add_frequencies(range(100,120))
    s_xyz = rs.PointCoordinates(rs.ObjectsByLayer('source')[0])
    room.add_fib_source(s_xyz, power=.1)
    room.add_spherical_recs(pts, radius=.3)

    m1 = Material()
    m1.absorption = {fk: .2 for fk in room.freq.values()}
    room.add_room_surfaces(srfs, m1, True)

    m2 = Material()
    m2.absorption = {fk: .99 for fk in room.freq.values()}
    room.add_room_surfaces(srf_, m2, True)

    rs.AddTextDot('s', room.source['xyz'])

    shoot_rays(room)
    visualize_rays(room.rays, keys= [60], ref_order=None, dot='w')
