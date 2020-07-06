import json
import igraph as ig
import chart_studio.plotly as py
import plotly.graph_objs as go

data = []
with open('data.json', 'r', encoding='utf-8') as fh:
    data = json.loads(fh.read())

print( data.keys())

N=len(data['cells'])
print(N)
'''
Li=len(data['ing'])
Le=len(data['exc'])
Edges_i=[(data['ing'][k]['source'], data['ing'][k]['target']) for k in range(Li)]
Edges_e=[(data['exc'][k]['source'], data['exc'][k]['target']) for k in range(Le)]

Gi=ig.Graph(Edges_i, directed=False)
Ge=ig.Graph(Edges_e, directed=False)

print(data['cells'][0])
'''
color=['red','blue', 'yellow']
#print(data['links'][0])

name=[]
id=[]
num = []
x=[]
y=[]
z=[]
c=[]

x13_1=[]
y13_1=[]
z13_1=[]
x13_0=[]
y13_0=[]
z13_0=[]

for cell in data['cells']:
    name.append(cell['name'])
    id.append(cell['id'])
    num.append(cell['num'])
    x.append(cell['x'])
    y.append(cell['y'])
    z.append(cell['z'])

for c13 in data['pyramidal regular spiking']:
    if c13['id'] == 1:
        s = c13['source']
        t = c13['target']
        x13_1 += [x[num.index(s)], x[num.index(t)], None]
        y13_1 += [y[num.index(s)], y[num.index(t)], None]
        z13_1 += [z[num.index(s)], z[num.index(t)], None]

    elif c13['id'] == 0:
        s = c13['source']
        t = c13['target']
        x13_0 += [x[num.index(s)], x[num.index(t)], None]
        y13_0 += [y[num.index(s)], y[num.index(t)], None]
        z13_0 += [z[num.index(s)], z[num.index(t)], None]

x12_1=[]
y12_1=[]
z12_1=[]
x12_0=[]
y12_0=[]
z12_0=[]
for e in data['pyramidal fast rythmic bursting']:
    if e['id']==1:
        s = e['source']
        t = e['target']
        x12_1 += [x[num.index(s)], x[num.index(t)], None]
        y12_1 += [y[num.index(s)], y[num.index(t)], None]
        z12_1 += [z[num.index(s)], z[num.index(t)], None]

    elif e['id'] == 0:
        s = e['source']
        t = e['target']
        x12_0 += [x[num.index(s)], x[num.index(t)], None]
        y12_0 += [y[num.index(s)], y[num.index(t)], None]
        z12_0 += [z[num.index(s)], z[num.index(t)], None]

x4_1=[]
y4_1=[]
z4_1=[]
x4_0=[]
y4_0=[]
z4_0=[]
for e in data['spiny stellate']:

    if e['id']==1:
        s = e['source']
        t = e['target']
        x4_1 += [x[num.index(s)], x[num.index(t)], None]
        y4_1 += [y[num.index(s)], y[num.index(t)], None]
        z4_1 += [z[num.index(s)], z[num.index(t)], None]

    elif e['id'] == 0:
        s = e['source']
        t = e['target']
        x4_0 += [x[num.index(s)], x[num.index(t)], None]
        y4_0 += [y[num.index(s)], y[num.index(t)], None]
        z4_0 += [z[num.index(s)], z[num.index(t)], None]


x2__1=[]
y2__1=[]
z2__1=[]

for e in data['superficial interneurons axoaxonic']:
    if e['id'] == -1:
        s = e['source']
        t = e['target']
        x2__1 += [x[num.index(s)], x[num.index(t)], None]
        y2__1 += [y[num.index(s)], y[num.index(t)], None]
        z2__1 += [z[num.index(s)], z[num.index(t)], None]


x1__1=[]
y1__1=[]
z1__1=[]

for e in data['superficial interneurons basket']:
    if e['id'] == -1:
        s = e['source']
        t = e['target']
        x1__1 += [x[num.index(s)], x[num.index(t)], None]
        y1__1 += [y[num.index(s)], y[num.index(t)], None]
        z1__1 += [z[num.index(s)], z[num.index(t)], None]


x3__1=[]
y3__1=[]
z3__1=[]

for e in data['superficial interneurons low threshold spiking']:

    if e['id'] == -1:
        s = e['source']
        t = e['target']
        x3__1 += [x[num.index(s)], x[num.index(t)], None]
        y3__1 += [y[num.index(s)], y[num.index(t)], None]
        z3__1 += [z[num.index(s)], z[num.index(t)], None]



x5_1=[]
y5_1=[]
z5_1=[]

x5_0=[]
y5_0=[]
z5_0=[]

for e in data['pyramidal tufted intrinsic bursting']:

    if e['id']==1:
        s = e['source']
        t = e['target']
        x5_1 += [x[num.index(s)], x[num.index(t)], None]
        y5_1 += [y[num.index(s)], y[num.index(t)], None]
        z5_1 += [z[num.index(s)], z[num.index(t)], None]

    elif e['id'] == 0:
        s = e['source']
        t = e['target']
        x5_0 += [x[num.index(s)], x[num.index(t)], None]
        y5_0 += [y[num.index(s)], y[num.index(t)], None]
        z5_0 += [z[num.index(s)], z[num.index(t)], None]

x7__1=[]
y7__1=[]
z7__1=[]

for e in data['deep interneurons basket']:

    if e['id'] == -1:
        s = e['source']
        t = e['target']
        x7__1 += [x[num.index(s)], x[num.index(t)], None]
        y7__1 += [y[num.index(s)], y[num.index(t)], None]
        z7__1 += [z[num.index(s)], z[num.index(t)], None]


x6_1=[]
y6_1=[]
z6_1=[]

for e in data['pyramidal tufted regular spiking']:

    if e['id']==1:
        s = e['source']
        t = e['target']
        x6_1 += [x[num.index(s)], x[num.index(t)], None]
        y6_1 += [y[num.index(s)], y[num.index(t)], None]
        z6_1 += [z[num.index(s)], z[num.index(t)], None]


x10_1=[]
y10_1=[]
z10_1=[]

x10_0=[]
y10_0=[]
z10_0=[]
for e in data['pyramidal nontufted regular spiking']:

    if e['id']==1:
        s = e['source']
        t = e['target']
        x10_1 += [x[num.index(s)], x[num.index(t)], None]
        y10_1 += [y[num.index(s)], y[num.index(t)], None]
        z10_1 += [z[num.index(s)], z[num.index(t)], None]

    elif e['id'] == 0:
        s = e['source']
        t = e['target']
        x10_0 += [x[num.index(s)], x[num.index(t)], None]
        y10_0 += [y[num.index(s)], y[num.index(t)], None]
        z10_0 += [z[num.index(s)], z[num.index(t)], None]

x8__1=[]
y8__1=[]
z8__1=[]

for e in data['deep interneurons axoaxonic']:

    if e['id'] == -1:
        s = e['source']
        t = e['target']
        x8__1 += [x[num.index(s)], x[num.index(t)], None]
        y8__1 += [y[num.index(s)], y[num.index(t)], None]
        z8__1 += [z[num.index(s)], z[num.index(t)], None]


x9__1=[]
y9__1=[]
z9__1=[]

for e in data['deep interneurons low threshold spiking']:

    if e['id'] == -1:
        s = e['source']
        t = e['target']
        x9__1 += [x[num.index(s)], x[num.index(t)], None]
        y9__1 += [y[num.index(s)], y[num.index(t)], None]
        z9__1 += [z[num.index(s)], z[num.index(t)], None]



trace13_1=go.Scatter3d(x=x13_1,
               y=y13_1,
               z=z13_1,
               mode='lines',
               line=dict(color='red', width=1),
               name='pyramidal regular spiking',
               showlegend=True,
               hoverinfo='none'
               )
trace13_0=go.Scatter3d(x=x13_0,
               y=y13_0,
               z=z13_0,
               mode='lines',
               line=dict(color='yellow', width=1),
               name='pyramidal regular spiking',
               showlegend=True,
               hoverinfo='none'
               )
trace12_1=go.Scatter3d(x=x12_1,
               y=y12_1,
               z=z12_1,
               mode='lines',
               line=dict(color='red', width=1),
               name= 'pyramidal fast rythmic bursting',
               hoverinfo='none'
               )
trace12_0=go.Scatter3d(x=x12_0,
               y=y12_0,
               z=z12_0,
               mode='lines',
               line=dict(color='yellow', width=1),
               name= 'pyramidal fast rythmic bursting',
               hoverinfo='none'
               )
trace4_1=go.Scatter3d(x=x4_1,
               y=y4_1,
               z=z4_1,
               mode='lines',
               line=dict(color='red', width=1),
               name='spiny stellate',
               showlegend=True,
               hoverinfo='none'
               )
trace4_0=go.Scatter3d(x=x4_0,
               y=y4_0,
               z=z4_0,
               mode='lines',
               line=dict(color='yellow', width=1),
               name='spiny stellate',
               showlegend=True,
               hoverinfo='none'
               )
trace5_1=go.Scatter3d(x=x5_1,
               y=y5_1,
               z=z5_1,
               mode='lines',
               line=dict(color='red', width=1),
               name='pyramidal tufted intrinsic bursting',
               showlegend=True,
               hoverinfo='none'
               )

trace5_0=go.Scatter3d(x=x5_0,
               y=y5_0,
               z=z5_0,
               mode='lines',
               line=dict(color='yellow', width=1),
               name='pyramidal tufted intrinsic bursting',
               showlegend=True,
               hoverinfo='none'
               )

trace6_1=go.Scatter3d(x=x6_1,
               y=y6_1,
               z=z6_1,
               mode='lines',
               line=dict(color='red', width=1),
               name='pyramidal tufted regular spiking',
               showlegend=True,
               hoverinfo='none'
               )

trace10_1=go.Scatter3d(x=x10_1,
               y=y10_1,
               z=z10_1,
               mode='lines',
               line=dict(color='red', width=1,),
               name='pyramidal nontufted regular spiking',
               showlegend=True,
               hoverinfo='none'
               )

trace10_0=go.Scatter3d(x=x10_0,
               y=y10_0,
               z=z10_0,
               mode='lines',
               line=dict(color='yellow', width=1),
               name='pyramidal nontufted regular spiking',
               showlegend=True,
               hoverinfo='none'
               )
trace2__1=go.Scatter3d(x=x2__1,
               y=y2__1,
               z=z2__1,
               mode='lines',
               line=dict(color='blue', width=1),
               name='superficial interneurons axoaxonic',
               showlegend=True,
               hoverinfo='none'
               )

trace1__1=go.Scatter3d(x=x1__1,
               y=y1__1,
               z=z1__1,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='superficial interneurons basket',
               showlegend=True,
               hoverinfo='none'
               )
trace3__1=go.Scatter3d(x=x3__1,
               y=y3__1,
               z=z3__1,
               mode='lines',
               line=dict(color='blue', width=1),
               name='superficial interneurons low threshold spiking',
               showlegend=True,
               hoverinfo='none'
               )

trace8__1=go.Scatter3d(x=x8__1,
               y=y8__1,
               z=z8__1,
               mode='lines',
               line=dict(color='blue', width=1),
               name='deep interneurons axoaxonic',
               showlegend=True,
               hoverinfo='none'
               )

trace7__1=go.Scatter3d(x=x7__1,
               y=y7__1,
               z=z7__1,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='deep interneurons basket',
               showlegend=True,
               hoverinfo='none'
               )
trace9__1=go.Scatter3d(x=x9__1,
               y=y9__1,
               z=z9__1,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='deep interneurons low threshold spiking',
               showlegend=True,
               hoverinfo='none'
               )


trace=go.Scatter3d(x=x,
               y=y,
               z=z,
               mode='markers',
               name='cells',
               marker=dict(symbol='circle',
                             size=6,
                             color=id,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=name,
               hoverinfo='text'
               )



data=[trace, trace12_0, trace12_1, trace13_0, trace13_1, trace1__1, trace2__1,trace3__1, trace4_0, trace4_1 ,trace5_0, trace5_1, trace6_1,trace7__1, trace8__1, trace9__1, trace10_0, trace10_1]
print(1)
fig=go.Figure(data=data)
print(2)
fig.write_html('net.html')