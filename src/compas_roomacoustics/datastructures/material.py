from __future__ import print_function

from ast import literal_eval

__all__ = ['Material']

class Material(object):

    def __init__(self, name, absorption, scattering, transparency):
        self.name = name
        self.absorption = absorption  # should be between 0 and 1
        self.scattering = scattering  # should be between 0 and 1
        self.transparency = transparency  # should be between 0 and 1

    @property
    def data(self):
        """dict : A data dict representing the material for serialisation.
        """
        data = {'name'          : self.name,
                'absorption'    : {},
                'scattering'    : {},
                'transparency'  : {},
                }

        for key in self.absorption:
            data['absorption'][literal_eval(key)] = self.absorption[key]

        for key in self.scattering:
            data['scattering'][literal_eval(key)] = self.scattering[key]

        for key in self.transparency:
            data['transparency'][literal_eval(key)] = self.transparency[key]

        return data

    @data.setter
    def data(self, data):
        self.name           = data.get('name') or {}
        self.scattering     = data.get('scattering') or {}
        self.transparency   = data.get('transparency') or {}

        absorption  = data.get('absorption') or {}
        self.absorption = {}
        for akey in absorption:
            self.absorption[literal_eval(akey)] = absorption[akey]

        scattering  = data.get('scattering') or {}
        self.scattering = {}
        for akey in scattering:
            self.scattering[literal_eval(akey)] = scattering[akey]

        transparency  = data.get('transparency') or {}
        self.transparency = {}
        for akey in transparency:
            self.transparency[literal_eval(akey)] = transparency[akey]

    @classmethod
    def from_data(cls, data):
        """Construct a material from structured data.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_data* method.
        """
        name = data['name']
        scatteting = data['scatteting']
        transparency = data['transparency']
        absorption = data['absorption']
        material = cls(name, absorption, scatteting, transparency)
        return material


if __name__ == '__main__':
    pass
