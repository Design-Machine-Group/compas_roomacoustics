from __future__ import print_function
import json
import math

from ast import literal_eval

from compas.utilities import geometric_key
from compas.geometry import centroid_points

from material import Material
from source import FibSource



TPL = """
================================================================================
Room summary
================================================================================

- name: {}
- surfaces: {}
- materials: {}
- source: {}
- number of rays: {}
- frequencies: {} from {}Hz to {}Hz
- receivers: {}
- ctime: {} (ms)

================================================================================
"""

class Room(object):
    """Definition of a room object for room acoustics analysis.

    Attributes
    ----------
    ...
    """
    # TODO: volume from is_boundary property
    # TODO: sabine RT
    # TODO: check to data, what is going on with power on non solved model
    # TODO: Result object???

 
    def __init__(self):
        self.name           = 'Acoustic_Room'
        self.tol            = '3f' # tolerance for generating geometric keys
        self.num_rays       = 1000 # number of rays used in analysis
        self.ctime          = 1000 # cuttoff time in miliseconds
        self.min_power      = .03 # minimum percentage of power in rays
        self.dt             = 3  # size of time interval for IR in miliseconds
        self.image_order    = 1  # order of reflections for the source image method

        self.source         = {} # dict
        self.receivers      = {} # dict
        self.surfaces       = {} # dict
        self.ray_times      = {} # dict
        self.ray_lengths    = {} # dict
        self.ray_powers     = {} # dict
        self.ray_lines      = {} # dict
        self.freq           = {} # dictionary of frequencies used in the analysis
        self.materials      = {} # dict

    def __str__(self):
        """Print a summary of the room."""
        s = TPL.format(self.name,
                       len(self.surfaces),
                       len(self.materials),
                       self.source.type,
                       self.num_rays,
                       len(self.freq),
                       min(self.freq.values()),
                       max(self.freq.values()),
                       len(self.receivers),
                       self.ctime)
        return s

    @property
    def data(self):
        """dict : A data dict representing the room data structure for serialisation.
        """
        data = {'name'          : self.name,
                'tol'           : self.tol,
                'num_rays'      : self.num_rays,
                'ctime'         : self.ctime,
                'min_power'     : self.min_power,
                'source'        : self.source.data,
                'surfaces'      : self.surfaces,
                'dt'            : self.dt,
                'receivers'     : {},
                'ray_times'     : {},
                'ray_lengths'   : {},
                'ray_powers'    : {},
                'ray_lines'     : {},
                'freq'          : {},
                'materials'     : {}
                }

        for key in self.receivers:
            data['receivers'][repr(key)] = self.receivers[key]

        for key in self.freq:
            data['freq'][repr(key)] = self.freq[key]

        for key in self.materials:
            data['materials'][repr(key)] = self.materials[key].data

        for rk in self.ray_times:
            data['ray_times'][repr(rk)] = {repr(k): self.ray_times[rk][k] for k in self.ray_times[rk]}
            data['ray_lengths'][repr(rk)] = {repr(k): self.ray_lengths[rk][k] for k in self.ray_lengths[rk]}
            data['ray_powers'][repr(rk)] = {repr(k): self.ray_powers[rk][k] for k in self.ray_powers[rk]}
            data['ray_lines'][repr(rk)] = {repr(k): self.ray_lines[rk][k] for k in self.ray_lines[rk]}

        return data

    @data.setter
    def data(self, data):
        tol             = data.get('tol') or {}
        num_rays        = data.get('num_rays') or {}
        ctime           = data.get('ctime') or {}
        min_power       = data.get('min_power') or {}
        source          = data.get('source') or {}
        receivers       = data.get('receivers') or {}
        surfaces        = data.get('surfaces') or {}
        ray_times       = data.get('ray_times') or {}
        ray_lengths     = data.get('ray_lengths') or {}
        ray_powers      = data.get('ray_powers') or {}
        ray_lines       = data.get('ray_lines') or {}
        freq            = data.get('freq') or {}
        materials       = data.get('materials' or {})
        dt              = data.get('dt' or {})

        self.tol        = tol
        self.num_rays   = num_rays
        self.ctime      = ctime
        self.min_power  = min_power
        self.dt         = dt

        self.source = FibSource.from_data(source)
        self.surfaces = surfaces

        self.materials = {}
        for mkey in materials:
            self.materials[literal_eval(mkey)] = Material.from_data(materials[mkey])

        self.freq = {}
        for fkey in freq:
            self.freq[literal_eval(fkey)] = freq[fkey]

        self.receivers = {}
        for rkey in receivers:
            self.receivers[literal_eval(rkey)] = receivers[rkey]

        self.ray_times = {}
        self.ray_lengths = {}
        self.ray_powers = {}
        self.ray_lines = {}
        for rk in ray_times:
            self.ray_times[literal_eval(rk)] = {literal_eval(k): ray_times[rk][k] for k in ray_times[rk]}
            self.ray_lengths[literal_eval(rk)] = {literal_eval(k): ray_lengths[rk][k] for k in ray_lengths[rk]}
            self.ray_powers[literal_eval(rk)] = {literal_eval(k): ray_powers[rk][k] for k in ray_powers[rk]}
            self.ray_lines[literal_eval(rk)] = {literal_eval(k): ray_lines[rk][k] for k in ray_lines[rk]}

    def to_json(self, filepath):
        """Serialise the structured data representing the data structure to json.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        """
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @classmethod
    def from_json(cls, filepath):
        """Construct a room datastructure from structured data contained in a json file.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_json* method.

        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        
        room = cls()
        room.data = data
        return room

    # ---------------------------
    # Room acoustic calcultations
    # ---------------------------

    def compute_room_volume(self):
        pass

    def compute_sabine_rt(self):
        pass

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
        self.source = FibSource('fib',
                                xyz=xyz,
                                power=power,
                                num_rays=self.num_rays,
                                freq=self.freq,
                                min_power=self.min_power)

    def add_spherical_recs(self, pts, radius):
        """Creates a disctionary of spherical receivers.

        Parameters
        ----------
        pts : list
            List of reciever coordinates.
        radius: float
            Radius of all receivers
        """
        for pt in pts:
            gk = geometric_key(pt, self.tol)
            self.receivers[gk] = {'radius': radius,
                                  'xyz': list(pt),
                                  'volume':(4./3.) * math.pi * radius ** 3}

    def add_room_surfaces(self, srfs, material, is_boundary=False):
        """Adds sound reflectinc surfaces to the model.

        Parameters
        ----------
        srfs: list
            The guids of the sound relfecting surfaces.
        material: str, obj
            The material name or object to be assigned to the surface.
        is_boundary: bool
            Is the surface part of the room boundary. Defaults to False.

        Notes
        -----
        These should be rhino nurbs four point surfaces.

        """
        # TODO: make this work, more robust
        # if isinstance(material, Material):
        #     room.materials[material.name] = material
        #     material = material.name

        for srf_pts in srfs:
            centroid = centroid_points(srf_pts)
            gk = geometric_key(centroid)
            self.surfaces[gk] = {'material': material,
                                 'is_boundary': is_boundary,
                                 'srf_pts': srf_pts}

    def add_material(self, name, absorption, scattering, transparency):
        m = Material(name, absorption, scattering, transparency)
        self.materials[name] = m


if __name__ == '__main__':
    for i in range(50): print('')
    rs.CurrentLayer('Default')
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))

    pts = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer('receivers')]
    srfs = rs.ObjectsByLayer('reflectors')
    srf_ = rs.ObjectsByLayer('back_srf')

    room = Room()
    room.add_frequencies(range(100,120))
    room.add_fib_source([40,20,2], power=.1)

    room.add_spherical_recs(pts, radius=.3)

    absorption= {fk: .2 for fk in room.freq.values()}
    room.add_material('mat1', absorption)
    room.add_room_surfaces(srfs, 'mat1', True)

    absorption = {fk: .7 for fk in room.freq.values()}
    room.add_material('mat2', absorption)
    room.add_room_surfaces(srf_, 'mat2', True)

    print(room)
    fp = '/Users/time/Desktop/deleteme.json'
    room.to_json(fp)
    room_ = Room.from_json(fp)
    print(room_)
