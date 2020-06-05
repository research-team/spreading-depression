import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.express as px
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
    fig.add_trace(
        go.Scatter3d(
            x=x, y=y, z=z, mode='markers',
            text=id,
            marker=dict(symbol='circle',
                             size=6,
                             color=v,
                            colorscale='Jet',
                            showscale=True,
                            opacity=0.5
                        )))

# Make 10th trace visible
fig.data[0].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):

    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Time: " + str(i*10+10)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)
fig.write_html('wave_test.html')
fig.show()


