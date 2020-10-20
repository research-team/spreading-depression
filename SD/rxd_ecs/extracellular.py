import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.express as px
points= [-850,-510,-170,170,510,850] #6
fig = go.Figure()
df = pd.read_csv('volt_extr.csv')
#df.head()
Time = df['t'].unique()
# Add traces, one for each slider step
for step in Time:
    filter_t = df['t'] == step
    x=df.loc[filter_t]['x'].values.tolist()
    # print(x)
    y=df.loc[filter_t]['y'].values.tolist()
    z=df.loc[filter_t]['z'].values.tolist()
    v=df.loc[filter_t]['v'].values.tolist()
    id = df.loc[filter_t]['id']
    name = df.loc[filter_t]['name']
    v_dist = []
    for i in range(len(v)):
        if -850<=z[i]<=-680:
            v_dist.append( v[i]/abs(((x[i]-0)**2) + ((y[i]-0)**2) + ((z[i]-points[0])**2)))
        elif -680<z[i]<=-340:
            v_dist.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[1]) ** 2)))
        elif -340<z[i]<=0:
            v_dist.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[2]) ** 2)))
        elif 0 < z[i] <=340:
            v_dist.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[3]) ** 2)))
        elif 340<z[i]<=680:
            v_dist.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[4]) ** 2)))
        elif 680<z[i] <=850:
            v_dist.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[5]) ** 2)))

    fig.add_trace(
        go.Scatter3d(
            x=x, y=y, z=z, mode='markers',
            text=name,
            marker=dict(symbol="circle",
                             size=4,
                             color=v_dist,
                            colorscale='Jet',
                            showscale=True,
                            cmin=-1/1000000000000,
                            cmax= 1/1000000000000 ,
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

fig.write_html('main_test_wave(extracellular).html')
fig.show()