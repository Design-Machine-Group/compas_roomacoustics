from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go
import plotly.io as pio

all = ['PlotlyViewer']


class PlotlyViewer(object):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, room):
        self.room           = room
        self.layout         = None
        self.fig            = None
        self.data           = []
        self.plot_materials = False

    def show(self):
        self.make_layout()
        self.add_recdata()
        self.add_surface_edges()
        if self.plot_materials:
            self.add_materials()
        self.add_source()    
        self.fig = go.Figure(data=self.data, layout=self.layout)
        self._show()


    def _show(self):

        num = len(self.room.freq) + len(self.room.materials) + 2
        num_ = len(self.room.materials) + 3
        if not self.plot_materials:
            num -= len(self.room.materials)
            num_ -= len(self.room.materials)

        for i in range(1, len(self.fig.data)):
            self.fig.data[i].visible = False
        for i in range(1, num_):
            self.fig.data[-i].visible = True

        steps = []
        freq = sorted(list(self.room.freq.keys()), key=float)

        for f in freq:
            step = {'method':'update',
                    'args':[{'visible': [False] * num},
                            {'title': 'EDT - {} Hz'.format(self.room.freq[f])}],
                    'label':'{} Hz'.format(self.room.freq[f])}
            step["args"][0]["visible"][f] = True
            for i in range(1, num_):
                step["args"][0]["visible"][-i] = True

            steps.append(step)

        sliders = [{'active':0,
                    'currentvalue':{'prefix': 'Frequency: '},
                    'pad':{'t': 20},
                    'steps':steps,
                    }]

        self.fig.update_layout(sliders=sliders)
        self.fig.show()


    def add_materials(self):

        srfs = {mat: [] for mat in self.room.materials}
        for srf in self.room.surfaces:
            mat = self.room.surfaces[srf]['material']
            srfs[mat].append(srf)

        for mat in srfs: 
            x, y, z = [], [], []
            i, j, k = [], [], []
            count = 0
            for skey in srfs[mat]:
                pts = self.room.surfaces[skey]['srf_pts']
                x_, y_, z_ = [], [], []
                for pt in pts:
                    x_.append(pt[0])
                    y_.append(pt[1])
                    z_.append(pt[2])
                i.extend((count, count + 2))
                j.extend((count + 1, count + 3))
                k.extend((count + 2, count))
                count += 4
                x.extend(x_)
                y.extend(y_)
                z.extend(z_)
            

            faces = go.Mesh3d(x=x,
                              y=y,
                              z=z,
                              i=i,
                              j=j,
                              k=k,
                              opacity=.5,
                              showlegend=True,
                              name=mat,
                              )
            self.data.append(faces)


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
                                  showlegend= False,
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
                                      xaxis=dict(gridcolor='rgb(255, 255, 255)',
                                                 zerolinecolor='rgb(255, 255, 255)',
                                                 showbackground=True,
                                                 backgroundcolor='rgb(230, 230,230)'),
                                      yaxis=dict(gridcolor='rgb(255, 255, 255)',
                                                 zerolinecolor='rgb(255, 255, 255)',
                                                 showbackground=True,
                                                 backgroundcolor='rgb(230, 230,230)'),
                                      zaxis=dict(gridcolor='rgb(255, 255, 255)',
                                                 zerolinecolor='rgb(255, 255, 255)',
                                                 showbackground=True,
                                                 backgroundcolor='rgb(230, 230,230)')
                                      ),
                          legend=dict(yanchor="top",
                                      y=0.99,
                                      xanchor="left",
                                      x=0.01
                                      ))

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
    v.plot_materials = True
    v.show()



