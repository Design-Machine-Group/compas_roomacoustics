import json
import math

from compas.utilities import geometric_key

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
        self.reflectors = {}        # dict
        self.rays = {}              # dict


    # ---------------------------
    # Room attributes creation
    # ---------------------------

    def add_frequencies(self, freq_list):
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


    # def add_reflectors_from_layers(srf_layer):
    #     global_coeff = {'100':.1, '200':.2, '300':.3}
    #     srfs = rs.ObjectsByLayer(srf_layer)
    #     reflectors = {}
    #     for i, srf in enumerate(srfs):
    #         reflectors[str(srf)] = {'guid': srf, 'abs_coeff': global_coeff}
    #     return reflectors

if __name__ == '__main__':
    import rhinoscriptsyntax as rs
    for i in range(50): print ''

    pts = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer('recievers')]

    room = Room()
    room.add_frequencies(range(100,120))
    room.add_fib_source(power=.1)
    room.add_spherical_recs(pts, radius=.3)
