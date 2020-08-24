from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


import plotly.graph_objects as go

import plotly.io as pio
# pio.renderers.default = "firefox"

all = ['CurvesPlotter']

#TODO: How to pick the mic to plot? xyz???

class CurvesPlotter(object):

    def __init__(self, room):
        self.room       = room
        self.layout     = None
        self.fig        = None
        self.data       = []
    
    def show(self, max_time=None):
        data = []
        freq = 4
        rkey = list(self.room.results.keys())[7]
        frequencies = sorted(list(self.room.freq.keys()), key=float)
        for freq in frequencies:
            etc = self.room.results[rkey].etc[freq]
            x, y = [], []
            keys = sorted(list(etc.keys()), key=lambda x: float(x.split(',')[0]))
            if not max_time:
                time = [float(key.split(',')[0]) for key in keys]
                max_time = max(time)
            for key in keys:
                time = float(key.split(',')[0])
                x.append(time)
                y.append(etc[key])
                if time > max_time:
                    break

            bars = go.Bar(x=x,
                           y=y,
                           name='{} Hz'.format(room.freq[freq]),
                           )
            data.append(bars)

            # lines = go.Scatter(x=x,
            #                    y=y,
            #                    mode='lines',
            #                    name='{} Hz'.format(room.freq[freq]),
            #                    line={'width':3,}
            #                   )
            # data.append(lines)

        fig = go.Figure(data)
        fig.update_layout(yaxis_type="log")
        fig.show()


if __name__ == "__main__":

    for i in range(50): print('')

    import os
    import compas_roomacoustics

    from compas_roomacoustics.datastructures import Room

    filename = 'simple_box_out.json'
    # filename = 'simple_box_allrecs_out.json'

    room = Room.from_json(compas_roomacoustics.get(filename))
    v = CurvesPlotter(room)
    v.show()
