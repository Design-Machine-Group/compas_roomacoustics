from __future__ import print_function
#TODO: summary

class Material(object):

    def __init__(self, name, absorption):
        self.name = name
        self.absorption = absorption
        self.scatteting = {}
        self.transparency = {}

    @property
    def data(self):
        """dict : A data dict representing the material for serialisation.
        """
        data = {'name'          : self.name,
                'absorption'    : {},
                'scatteting'    : {},
                'transparency'  : {},
                }

        for key in self.absorption:
            data['absorption'][repr(key)] = self.absorption[key]

        return data

    @data.setter
    def data(self, data):
        self.name           = data.get('name') or {}
        self.scatteting     = data.get('scatteting') or {}
        self.transparency   = data.get('transparency') or {}

        absorption  = data.get('absorption') or {}
        self.absorption = {}
        for akey in absorption:
            self.absorption[repr(akey)] = absorption[akey]

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
        material = cls(name, absorption)
        return material


if __name__ == '__main__':
    pass
