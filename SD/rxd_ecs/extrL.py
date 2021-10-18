import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
outdir = os.path.abspath('tests/963_tW')
fig = go.Figure()
df = pd.read_csv('tests/963_tW/extr_all.csv')

Time = df['t'].unique()
data =  [[] for i in range(14)]
def dist(x2,y2,z2,z1, x1=100,y1=100):
    r=np.sqrt((10**(-6*2)) * ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))
    return r
# Add traces, one for each slider step
THLM=[]
for step in Time:
    filter_t = df['t'] == step
    x=df.loc[filter_t]['x'].values.tolist()
    # print(x)
    y=df.loc[filter_t]['y'].values.tolist()
    z=df.loc[filter_t]['z'].values.tolist()
    v=df.loc[filter_t]['v'].values.tolist()
    id = df.loc[filter_t]['id']
    #name = df.loc[filter_t]['name']
    v_dist = [[] for i in range(14)]#23 = []
    #v_dist4 = []
    #v_dist5 = []
    #v_dist56 = []
    #v_dist6 = []
    lenn=14
    lenV=len(v)
    thlm =[]
    for i in range(len(v)):
        if z[i] > 1000:
            thlm.append(v[i] / dist(x[i], y[i], z[i], 1150))
    for list in range(lenn):
        for i in range(lenV):
            if 850 >= z[i] >= -850:
                v_dist[list].append(v[i] /dist(x[i],y[i],z[i],-850+(list*114)))



        #v_dist23.append( (v[i] /abs(((x[i]-100)**2) + ((y[i]-100)**2) + ((z[i]-points[0])**2)))*(10**6))
        #v_dist4.append( (v[i] / abs(((x[i] - 100) ** 2) + ((y[i] - 100) ** 2) + ((z[i]-points[1]) ** 2))) *(10**6))
        #v_dist5.append( (v[i] / abs(((x[i] - 100) ** 2) + ((y[i] - 100) ** 2) + ((z[i]-points[2]) ** 2)))*(10**6))
        #v_dist56.append( (v[i] / abs(((x[i] - 100) ** 2) + ((y[i] - 100) ** 2) + ((z[i]-points[3]) ** 2))) *(10**6))
        #v_dist6.append( (v[i] / abs(((x[i] - 100) ** 2) + ((y[i] - 100) ** 2) + ((z[i]-points[4]) ** 2)))*(10**6))
        #elif 680<z[i] <=850:
        #    v_dist.append( v[i] / abs(((x[i] - 50) ** 2) + ((y[i] - 50) ** 2) + ((z[i]-points[5]) ** 2)))
    for i in range(lenn):
        data[i].append(sum(v_dist[i]))
    THLM.append(sum(thlm))
    #data23.append(sum(v_dist23))
    #data4.append(sum(v_dist4))
    #data5.append(sum(v_dist5))
    #data56.append(sum(v_dist56))
    #data6.append(sum(v_dist6))
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

#print(data[0])
subplot_titles=["L2-3","L2-3","L2-3","L4", "L4","L4","L5","L5","L5","L5","L5","L6", "L6","L6"]
fig = make_subplots(rows=15, cols=1)#, subplot_titles=("L2-3","L2-3","L2-3","L4", "L4","L4","L5","L5","L5","L5","L5","L6", "L6","L6"))
for i in range(14):
    #print(i)
    fig.add_trace(go.Scatter(x=Time, y=data[i],  name=subplot_titles[i]), row=i+1, col=1)
    #fig.update_yaxes(range=[-1, 1], row=i+1, col=1)
fig.add_trace(go.Scatter(x=Time, y=THLM,  name="thlm"), row=15, col=1)
fig.update_xaxes(matches='x')
fig.update_yaxes(matches='y')
fig.update_xaxes(showticklabels=True)
#fig.update_layout(showlegend=False)
fig.update_layout(height=1000)
fig.show()
fig.write_html(os.path.join(outdir,'mainAll(extracellular).html'))





'''Time = df['t'].unique()

def dist(x2,y2,z2,z1, x1=100,y1=100):
    r=np.sqrt((10**(-6*2)) * ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))
    return r
'''
'''

L2-3 = [-850, -450]

[от, до]

L4 = [-450,-150]


L5 = [-150,350]

L6 = [350,850]

thlm = [1000,1300]
'''

'''V23=[]
V4=[]
V5=[]
V6=[]
THLM=[]
for step in Time:
    filter_t = df['t'] == step

    x=df.loc[filter_t]['x'].values.tolist()
    # print(x)
    y=df.loc[filter_t]['y'].values.tolist()
    z=df.loc[filter_t]['z'].values.tolist()
    v=df.loc[filter_t]['v'].values.tolist()
    #v_dist = [[] for i in range(14)]
    #lenn=14
    v_23 =[]
    v_4=[]
    v_5=[]
    v_6=[]
    thlm =[]
    for i in range(len(v)):


        if -450 > z[i] >= -150:
            v_4.append(v[i] )#/dist(x[i],y[i],z[i],-450+(150/2)))
        elif -850 >= z[i] >= -450:
            v_23.append(v[i] )#/dist(x[i],y[i],z[i],-850+(450/2)))
        elif -150 > z[i] >= 350:
            v_5.append(v[i])# /dist(x[i]),y[i],z[i],-150+(350/2)))
        elif 350 > z[i] >= 850:
            v_5.append(v[i])# /dist(x[i],y[i],z[i],350+(850/2)))
        #elif z[i] > 1000:
        #    thlm.append(v[i]) #/ dist(x[i], y[i], z[i], 1150))
    V23.append(sum(v_23))
    V4.append(sum(v_4))
    V5.append(sum(v_5))
    V6.append(sum(v_6))
    THLM.append(sum(thlm))


#print(data[0])
subplot_titles=["L2-3","L4", "L5","L6"]
fig = make_subplots(rows=4, cols=1)
fig.add_trace(go.Scatter(x=Time, y=V23,  name=subplot_titles[0]), row=1, col=1)
fig.add_trace(go.Scatter(x=Time, y=V4,  name=subplot_titles[1]), row=2, col=1)
fig.add_trace(go.Scatter(x=Time, y=V5,  name=subplot_titles[2]), row=3, col=1)
fig.add_trace(go.Scatter(x=Time, y=V6,  name=subplot_titles[3]), row=4, col=1)
#fig.add_trace(go.Scatter(x=Time, y=THLM,  name="thlm"), row=5, col=1)
fig.update_xaxes(matches='x')
#fig.update_yaxes(matches='y')

fig.update_xaxes(showticklabels=False)
fig.update_xaxes(showticklabels=True, row=4, col=1)
#fig.show()
fig.write_html(os.path.join(outdir,'extracellular.html'))

'''


