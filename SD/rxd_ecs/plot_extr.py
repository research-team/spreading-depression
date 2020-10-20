import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.express as px

fig = go.Figure()
df = pd.read_csv('volt_extr.csv')
#df.head()
Time = df['t'].unique()
# Add traces, one for each slider step
for step in Time:
    filter_t = df['t'] == step
    x=df.loc[filter_t]['x']
    # print(x)
    y=df.loc[filter_t]['y']
    z=df.loc[filter_t]['z']
    v=df.loc[filter_t]['v']
    id = df.loc[filter_t]['id']
    name = df.loc[filter_t]['name']
    fig.add_trace(
        go.Scatter3d(
            x=x, y=y, z=z, mode='markers',
            text=name,
            marker=dict(symbol="circle",
                             size=6,
                             color=v,
                            colorscale='Jet',
                            showscale=True,
                            cmin = -1/100000000000000,
                            cmax =  1/100000000000000,
                            opacity=0.5
                            #bordercolor = '#111' if id in [1,2,3,7,8,9] else '#555',
                        #borderwidth=1
                        )))

# Make 10th trace visible
fig.data[0].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):

    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Time: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Time: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders,
    scene = dict(
            xaxis = dict(nticks=4, range=[0,100],),
                         yaxis = dict(nticks=4, range=[0,100],),
                         zaxis = dict(nticks=4, range=[850,-850],),), #0-1700 4800-5300
    #width=700,
    #margin=dict(r=20, l=10, b=10, t=10)
    )

fig.write_html('wave(extracellular).html')
fig.show()