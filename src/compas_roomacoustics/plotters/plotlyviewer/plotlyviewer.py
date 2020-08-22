from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go
from compas.utilities import i_to_rgb

import plotly.io as pio
# pio.renderers.default = "firefox"

all = ['PlotlyViewer']


class PlotlyViewer(object):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, room):
        self.room       = room
        self.layout     = None
        self.fig        = None
        self.data       = {}

    def show(self):
        self.make_layout()
        self.plot_surface_edges()
        self.plot_recdata()

        data = [self.data[key] for key in self.data]
        fig = go.Figure(data=data, layout=self.layout)
        fig.show()

    def plot_recdata(self):
        results = self.room.results
        x, y, z = [], [],  []
        
        values = []
        for key in results:
            pt = room.receivers[key]['xyz']
            x.append(pt[0])
            y.append(pt[1])
            z.append(pt[2])
            values.append(room.results[key].edt[5])

        vmax = max(values)
        vmin = min(values)
        color = []
        text = []
        for v in values:
            r, g, b = i_to_rgb((v - vmin)/(vmax - vmin))
            color.append('rgb({0},{1},{2})'.format(r, g, b))
            text.append('EDT = {}'.format(v))

        # marker = {'color':color, 'size':8, 'text':values}

        points = go.Scatter3d(x=x, y=y, z=z, 
                              mode='markers',
                              marker_color=color,
                              text=text)
        self.data['data_points'] = points


    def make_layout(self):
        name = self.room.name
        title = '{} - compas roomacoustics'.format(name)
        
        layout = go.Layout(title=title,
                          scene=dict(aspectmode='data',
                                    xaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    yaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    zaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)')
                                    ),
                          showlegend=False,
                            )
        self.layout = layout


    def plot_surface_edges(self):
        srfs = self.room.surfaces
        lines = []
        for skey in srfs:
            for i in range(len(srfs[skey]['srf_pts'])):
                lines.append([srfs[skey]['srf_pts'][-i], srfs[skey]['srf_pts'][-i - 1]])

        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        x, y, z = [], [],  []
        for u, v in lines:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])
        lines = go.Scatter3d(x=x, y=y, z=z, mode='lines', line=line_marker)
        self.data['surface_edges'] = lines



if __name__ == "__main__":

    for i in range(50): print('')

    import os
    import compas_roomacoustics

    from compas_roomacoustics.datastructures import Room

    filename = 'simple_box_out.json'
    # filename = 'simple_box_allrecs_out.json'

    room = Room.from_json(compas_roomacoustics.get(filename))
    v = PlotlyViewer(room)
    v.show()



