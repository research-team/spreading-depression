import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.express as px

points= [-650,-300,-100,150,600] #5
fig = go.Figure()
df = pd.read_csv('volt_extr.csv')
#df.head()
Time = df['t'].unique()
data23 =[]
data4 =[]
data5 =[]
data56 =[]
data6 =[]
main = [data23, data4, data5, data56,data6 ]
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
    v_dist23 = []
    v_dist4 = []
    v_dist5 = []
    v_dist56 = []
    v_dist6 = []
    for i in range(len(v)):
        if -850<=z[i]<=-450: #2-3
            v_dist23.append( v[i]/abs(((x[i]-0)**2) + ((y[i]-0)**2) + ((z[i]-points[0])**2)))
        elif -450<z[i]<=-150: #4
            v_dist4.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[1]) ** 2)))
        elif -150<z[i]<=50: #5
            v_dist5.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[2]) ** 2)))
        elif 50 < z[i] <=350: #5-6
            v_dist56.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[3]) ** 2)))
        elif 350<z[i]<=850: #6
            v_dist6.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[4]) ** 2)))
        #elif 680<z[i] <=850:
        #    v_dist.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[5]) ** 2)))
    data23.append(sum(v_dist23))
    data4.append(sum(v_dist4))
    data5.append(sum(v_dist5))
    data56.append(sum(v_dist56))
    data6.append(sum(v_dist6))
    #fig.add_trace(
    #    go.Scatter3d(
    #        x=x, y=y, z=z, mode='markers',
    #        text=name,
    #        marker=dict(symbol="circle",
    #                         size=4,
    #                         color=v_dist,
    #                        colorscale='Jet',
    #                        showscale=True,
    #                        cmin=-1/1000000000000,
    #                        cmax= 1/1000000000000 ,
    #                        opacity=0.5
    #                        #bordercolor = '#111' if id in [1,2,3,7,8,9] else '#555',
    #                    #borderwidth=1
    #                    )))


fig = make_subplots(rows=5, cols=1, subplot_titles=("L2-3","L4", "L5", "L5-6", "L6"))
for i in range(1,6):
    #print(i)
    fig.add_trace(go.Scatter(x=list(range(len(Time))), y=main[i-1]), row=i, col=1)
fig.update_xaxes(matches='x')
fig.write_html('main(extracellular).html')
fig.update_layout(showlegend=False)
fig.show()




# Make 10th trace visible
#fig.data[0].visible = True

# Create and add slider
#steps = []
#for i in range(len(fig.data)):
#
#    step = dict(
#        method="update",
#        args=[{"visible": [False] * len(fig.data)},
#              {"title": "Time: " + str(i)}],  # layout attribute
#    )
#    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
#    steps.append(step)
#
#sliders = [dict(
#    active=0,
#    currentvalue={"prefix": "Time: "},
#    pad={"t": 50},
#    steps=steps
#)]
#
#fig.update_layout(
#    sliders=sliders,
#    scene = dict(
#            xaxis = dict(nticks=4, range=[0,100],),
#                         yaxis = dict(nticks=4, range=[0,100],),
#                         zaxis = dict(nticks=4, range=[850,-850],),), #0-1700 4800-5300
#    #width=700,
#    #margin=dict(r=20, l=10, b=10, t=10)
#    )
#
#fig.write_html('main_test_wave(extracellular).html')
#fig.show()