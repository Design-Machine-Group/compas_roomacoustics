import json
import math
import rhinoscriptsyntax as rs
from compas.utilities import geometric_key
from compas.geometry import centroid_points

class Room(object):
    """Definition of a room object for room acoustics analysis.

    Attributes
    ----------
    ...
    """
    # TODO: data setting and updating
    # TODO: from/to json
    # TODO: volume from is_boundary property
    # TODO sabine RT
    
    def __init__(self):
        self.tol = '3f'             # tolerance for generating geometric keys
        self.freq = {}              # dictionary of frequencies used in the analysis
        self.num_rays = 1000        # number of rays used in analysis
        self.source_pt = None       # source coordinates
        self.ctime = 1000.          # cuttoff time in miliseconds
        self.min_power = .03        # minimum percentage of power in rays

        self.source = {}            # dict
        self.recievers = {}         # dict
        self.surfaces = {}        # dict
        self.rays = {}              # dict


    # ---------------------------
    # Room acoustic calcultations
    # ---------------------------

    # def compute_room_volume(self):
    #     pass
    #
    # def compute_sabine_rt(self):
    #     pass


    # ---------------------------
    # Room attributes creation
    # ---------------------------

    def add_frequencies(self, freq_list):
        """Creates the frequencies property from list.

        Parameters
        ----------
        freq_list: list
            The sound frequencies in Hz.
        """
        self.freq = {i: f for i, f in enumerate(freq_list)}

    def add_fib_source(self, xyz, power):
        """Creates a uniform point source using fibonacci vector
        distribution.

        Parameters
        ----------
        xyz: list
            Source coordinates.
        power : float or dict
            The power of the source per frequency in watts. If a single float is
            is given, the same power will be attributed to all frequencies.

        Notes:
        ------
        The source power is distributed evenly in all directions.

        """
        self.source['xyz'] = xyz
        self.source['type'] = 'fibbonaci_uniform'

        if type(power) == float:
            self.source['power'] = {wk:power for wk in self.freq.values()}
        else:
            self.source['power'] = power

        offset = 2. / self.num_rays
        increment = math.pi * (3. - math.sqrt(5.))
        init_rays = {}
        for i in range(self.num_rays):
            y = ((i * offset) - 1) + (offset / 2)
            r = math.sqrt(1 - pow(y,2))
            phi = (i % self.num_rays) * increment
            x = math.cos(phi) * r
            z = math.sin(phi) * r
            init_rays[i] = {'v':[x, y, z], 'power': {}, 'min_power': {}}


        for wk in self.source['power']:
            for rk in init_rays:
                init_rays[rk]['power'][wk] = self.source['power'][wk] / float(self.num_rays)
                init_rays[rk]['min_power'][wk] = self.min_power * (self.source['power'][wk] / float(self.num_rays))
        self.source['init_rays'] = init_rays

    def add_spherical_recs(self, pts, radius):
        """Creates a disctionary of spherical recievers.

        Parameters
        ----------
        pts : list
            List of reciever coordinates.
        radius: float
            Radius of all recievers
        """
        for pt in pts:
            gk = geometric_key(pt, self.tol)
            self.recievers[gk] = {'radius': radius,
                                  'xyz': list(pt),
                                  'v':(4./3.) * math.pi * radius ** 3}

    def add_room_surfaces(self, srfs, material, is_boundary=False):
        """Adds sound reflectinc surfaces to the model.

        Parameters
        ----------
        srfs: list
            The guids of the sound relfecting surfaces.
        material: object
            The matwerial object to be assigned to the surface.
        is_boundary: bool
            Is the surface part of the room boundary. Defaults to False.

        Notes
        -----
        These should be rhino nurbs four point surfaces.

        """
        for srf in srfs:
            centroid = centroid_points(rs.SurfacePoints(srf))
            gk = geometric_key(centroid)
            self.surfaces[gk] = {'guid': srf,
                                 'material': material,
                                 'is_boundary': is_boundary}



if __name__ == '__main__':

    from material import Material

    for i in range(50): print ''
    rs.CurrentLayer('Default')
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))

    pts = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer('recievers')]
    srfs = rs.ObjectsByLayer('reflectors')
    srf_ = rs.ObjectsByLayer('back_srf')

    room = Room()
    room.add_frequencies(range(100,120))
    room.add_fib_source([40,20,2], power=.1)
    room.add_spherical_recs(pts, radius=.3)

    m1 = Material()
    m1.absorption = {fk: .2 for fk in room.freq.values()}
    room.add_room_surfaces(srfs, m1, True)

    m2 = Material()
    m2.absorption = {fk: .7 for fk in room.freq.values()}
    room.add_room_surfaces(srf_, m2, True)

    for srf in room.surfaces:
        rs.AddTextDot(room.surfaces[srf]['material'].absorption[110], srf)
