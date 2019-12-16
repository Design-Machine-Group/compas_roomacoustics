import json
import math

from compas.utilities import geometric_key

from compas.geometry import centroid_points

class Room(object):
    """Definition of a room object for room acoustics analysis.

    Attributes
    ----------
    ...
    """

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

    def add_fib_source(self, power):
        """Creates a uniform point source using fibonacci vector
        distribution.

        Parameters
        ----------
        power : float or dict
            The power of the source per frequency in watts. If a single float is
            is given, the same power will be attributed to all frequencies.

        Notes:
        ------
        The source power is distributed evenly in all directions.

        """
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
            room.recievers[gk] = {'radius': radius,
                                  'xyz': list(pt),
                                  'v':(4./3.) * math.pi * radius ** 3}

    def add_room_surfaces(self, srfs):
        """Adds sound reflectinc surfaces to the model.

        Parameters
        ----------
        srfs: list
            The guids of the sound relfecting surfaces.

        Notes
        -----
        These should be rhino nurbs four point surfaces

        """
        for srf in srfs:
            centroid = centroid_points(rs.SurfacePoints(srf))
            gk = geometric_key(centroid)
            room.surfaces[gk] = {'guid': srf}

    def assign_abs_coeff(self, srfs, coeff_dict):
        """Assigns the absorption cooefficient of a list of surfaces

        Parameters
        ----------
        srfs: list
            The surfaces to assign the absorption to.
        coeff_dict: dict
            The frequency dependent absorption coefficients.
        """

        for srf in srfs:
            centroid = centroid_points(rs.SurfacePoints(srf))
            gk = geometric_key(centroid)
            room.surfaces[gk] = {'abs_coeff': coeff_dict}



if __name__ == '__main__':
    import rhinoscriptsyntax as rs
    for i in range(50): print ''
    rs.CurrentLayer('Default')
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))

    pts = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer('recievers')]
    srfs = rs.ObjectsByLayer('reflectors')
    srf_ = rs.ObjectsByLayer('back_srf')

    room = Room()
    room.add_frequencies(range(100,120))
    room.add_fib_source(power=.1)
    room.add_spherical_recs(pts, radius=.3)
    room.add_room_surfaces(srfs + srf_)
    coeff_dict = {fk: .2 for fk in room.freq.values()}
    room.assign_abs_coeff(srfs, coeff_dict)
    coeff_dict = {fk: .7 for fk in room.freq.values()}
    room.assign_abs_coeff(srf_, coeff_dict)

    for sk in room.surfaces:
        rs.AddTextDot(str(room.surfaces[sk]['abs_coeff'][119]), sk)
