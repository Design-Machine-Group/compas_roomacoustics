import math

TPL = """
================================================================================
Source summary
================================================================================

- name: {}
- type: {}
- xyz: {}
- power: {} (W)
- number of rays: {}
- frequencies: {} from {}Hz to {}Hz
- min_power: {} %

================================================================================
"""


class Source(object):
    #TODO: from_to
    def __init__(self, name):
        self.name = name
        self.type = None


    def __str__(self):
        s = TPL.format(self.name,
                       self.type,
                       self.xyz,
                       self.power[self.power.keys()[0]],
                       len(self.directions),
                       len(self.freq),
                       min(self.freq.values()),
                       max(self.freq.values()),
                       self.min_power * 100)
        return s

class FibSource(Source):
    """Uniform sound source in all frequencies, using a fibbonacci direction distribution.
    """
    def __init__(self, name, xyz, power, num_rays, freq, min_power):
        self.name = name
        self.type = 'fibbonaci_uniform'
        self.xyz = xyz
        self.freq = freq
        self.min_power = min_power
        self.num_rays =  num_rays
        self.directions = {}
        self.ray_power = {i: {} for i in range(self.num_rays)}
        self.ray_minpower = {i: {} for i in range(self.num_rays)}

        if type(power) == float:
            self.power = {wk:power for wk in self.freq.values()}
        else:
            self.power = power

        offset = 2. / self.num_rays
        increment = math.pi * (3. - math.sqrt(5.))
        for i in range(self.num_rays):
            y = ((i * offset) - 1) + (offset / 2)
            r = math.sqrt(1 - pow(y,2))
            phi = (i % self.num_rays) * increment
            x = math.cos(phi) * r
            z = math.sin(phi) * r
            self.directions[i] = [x, y, z]

        for wk in self.power:
            for rk in self.directions:
                self.ray_power[rk][wk] = self.power[wk] / float(self.num_rays)
                self.ray_minpower[rk][wk] = self.min_power * (self.power[wk] / float(self.num_rays))

    @property
    def data(self):
        """dict : A data dict representing the source for serialisation.
        """
        data = {'name'          : self.name,
                'type'          : self.type,
                'xyz'           : self.xyz,
                'min_power'     : self.min_power,
                'num_rays'      : self.num_rays,
                'freq'          : {},
                'directions'    : {},
                'ray_power'     : {},
                'ray_minpower'  : {}}

        for key in self.freq:
            data['freq'][repr(key)] = self.freq[key]

        for key in self.directions:
            data['directions'][repr(key)] = self.directions[key]

        for rkey in self.ray_power:
            data['ray_power'][repr(rkey)] = {repr(wkey): self.ray_power[rkey][wkey] for wkey in self.ray_power[rkey]}

        for rkey in self.ray_minpower:
            data['ray_minpower'][repr(rkey)] = {repr(wkey): self.ray_minpower[rkey][wkey] for wkey in self.ray_minpower[rkey]}

        return data

if __name__ == '__main__':
    freq = {i: f for i, f in enumerate(range(100, 120))}
    s = FibSource('fib', xyz=[0,0,0], power=.1, num_rays=1000, freq=freq, min_power=.06)
    print s
