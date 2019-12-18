
#TODO: from_to
#TODO: summary

class Material(object):

    def __init__(self, name):
        self.name = name
        self.absorption = {}
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


if __name__ == '__main__':
    pass
