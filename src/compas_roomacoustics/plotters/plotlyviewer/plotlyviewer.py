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

all = ['PlotlyViewer']


class PlotlyViewer(object):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, room):
        self.room       = room
        self.layout     = None
        self.fig        = None
        self.data       = []

    def show(self):
        self.make_layout()
        self.add_recdata()
        self.add_surface_edges()
        self.add_source()
        self.fig = go.Figure(data=self.data, layout=self.layout)
        self._show()


    def _show(self):

        for i in range(1, len(self.fig.data)):
            self.fig.data[i].visible = False
        self.fig.data[-1].visible = True
        self.fig.data[-2].visible = True

        steps = []
        freq = sorted(list(self.room.freq.keys()), key=float)
        for f in freq:
            step = {'method':'update',
                    'args':[{'visible': [False] * (len(self.room.freq) + 2)},
                            {'title': 'EDT - {} Hz'.format(self.room.freq[f])}],
                    'label':'{} Hz'.format(self.room.freq[f])}
            step["args"][0]["visible"][f] = True
            step["args"][0]["visible"][-1] = True
            step["args"][0]["visible"][-2] = True
            steps.append(step)

        sliders = [{'active':0,
                    'currentvalue':{'prefix': 'Frequency: '},
                    'pad':{'t': 20},
                    'steps':steps,
                    }]

        self.fig.update_layout(sliders=sliders)
        self.fig.show()


    def add_recdata(self):
        param = 'edt'
        results = self.room.results
        for freq in room.freq:
            values = []
            x, y, z = [], [], []
            for key in results:
                pt = room.receivers[key]['xyz']
                x.append(pt[0])
                y.append(pt[1])
                z.append(pt[2])
                values.append(room.results[key].edt[freq])

            text = []
            for v in values:
                text.append('{} = {}'.format(param.upper(),v))

            points = go.Scatter3d(x=x, y=y, z=z, 
                                  mode='markers',
                                  showlegend= True,
                                #   visible=False,
                                  marker_color=values,
                                  marker_colorbar={'thickness':30},
                                  marker_colorscale='Portland',
                                  # marker_colorscale='Viridis',
                                  # marker_colorscale='Thermal',
                                  text=text,
                                  )

            # key = '{}_{}'.format(param, room.freq[freq])
            self.data.append(points)


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


    def add_surface_edges(self):
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
        lines = go.Scatter3d(x=x, y=y, z=z, 
                             mode='lines',
                             line=line_marker,
                             showlegend=False,)

        self.data.append(lines)


    def add_source(self):
        x, y, z = self.room.source.xyz
        source = go.Scatter3d(x=[x], y=[y], z=[z], 
                              mode='markers+text',
                              marker_color='rgb(255, 255, 255)',
                              marker_size=14,
                              marker_line_width=1,
                              marker_line_color='rgb(50, 50, 50)',
                              showlegend= False,
                              text='S',
                              textposition='middle center',
                              )

        self.data.append(source)

if __name__ == "__main__":

    for i in range(50): print('')

    import os
    import compas_roomacoustics

    from compas_roomacoustics.datastructures import Room

    # filename = 'simple_box_out.json'
    filename = 'simple_box_allrecs_out.json'

    room = Room.from_json(compas_roomacoustics.get(filename))
    v = PlotlyViewer(room)
    v.show()



