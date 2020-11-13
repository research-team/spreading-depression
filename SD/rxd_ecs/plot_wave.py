import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.express as px
import os
outdir = os.path.abspath('tests/928_tW')


'''

df = pd.read_csv('volt.csv')
#df.head()
Time = df['t'].unique()
print(0)
fig = make_subplots(rows=10, cols=int(len(Time)/10))

print(1)
#fig["layout"].pop("updatemenus") # optional, drop animation buttons
for i in Time:
    filter_t=df['t']==i
    #print(df.loc[filter_t])
    #x=df.loc[filter_t]['x']
    #print(x)
    #y=df.loc[filter_t]['y']
    #z=df.loc[filter_t]['z']
    #v=df.loc[filter_t]['v']
    fig.add_trace(px.scatter_3d(df.loc[filter_t], x='x', y='y', z='z', color='v'))

print(2)
fig.write_html('wave.html')

'''
fig = go.Figure()
df = pd.read_csv('volt.csv')
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
                            cmin = -80,
                            cmax = 50,
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
            xaxis = dict(nticks=4, range=[0,200],),
                         yaxis = dict(nticks=4, range=[0,200],),
                         zaxis = dict(nticks=4, range=[850,-850],),), #0-1700 4800-5300
    #width=700,
    #margin=dict(r=20, l=10, b=10, t=10)
    )

fig.write_html(os.path.join(outdir,'wave_test(ext).html'))
#fig.show()




#-------------NO gaba----------


fig2 = go.Figure()
df2 = pd.read_csv('volt_gaba.csv')
#df.head()
Time = df2['t'].unique()
# Add traces, one for each slider step
for step in Time:
    filter_t = df2['t'] == step
    x=df2.loc[filter_t]['x']
    # print(x)
    y=df2.loc[filter_t]['y']
    z=df2.loc[filter_t]['z']
    v=df2.loc[filter_t]['v']
    id = df2.loc[filter_t]['id']
    name = df2.loc[filter_t]['name']
    fig2.add_trace(
        go.Scatter3d(
            x=x, y=y, z=z, mode='markers',
            text=name,
            marker=dict(symbol="square",
                             size=3,
                             color=v,
                            colorscale='Jet',
                            showscale=True,
                            cmin = -80,
                            cmax = 50,
                            opacity=0.5
                            #bordercolor = '#111' if id in [1,2,3,7,8,9] else '#555',
                        #borderwidth=1
                        )))

# Make 10th trace visible
fig2.data[0].visible = True

# Create and add slider
steps = []
for i in range(len(fig2.data)):

    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig2.data)},
              {"title": "Time: " + str(i)}],  # layout attribute-0е
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Time: "},
    pad={"t": 50},
    steps=steps
)]

fig2.update_layout(
    sliders=sliders,
    scene = dict(
            xaxis = dict(nticks=4, range=[0,200],),
                         yaxis = dict(nticks=4, range=[0,200],),
                         zaxis = dict(nticks=4, range=[850,-850],),), #0-1700 4800-5300
    #width=700,
    #margin=dict(r=20, l=10, b=10, t=10)
    )

fig2.write_html(os.path.join(outdir,'wave_test(gaba).html')) #wave_test(ext)_thlm.html   wave_test(gaba)_thlm.html