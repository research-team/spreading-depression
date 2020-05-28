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

#print(data['links'][0])

name=[]
id=[]
num = []
x=[]
y=[]
z=[]
c=[]

x13=[]
y13=[]
z13=[]

x12=[]
y12=[]
z12=[]
for cell in data['cells']:
    name.append(cell['name'])
    id.append(cell['id'])
    num.append(cell['num'])
    x.append(cell['x'])
    y.append(cell['y'])
    z.append(cell['z'])

for c13 in data['pyramidal regular spiking']:
    s=c13['source']
    t=c13['target']
    x13+=[x[num.index(s)], x[num.index(t)], None]
    y13 += [y[num.index(s)], y[num.index(t)], None]
    z13 += [z[num.index(s)], z[num.index(t)], None]

for e in data['pyramidal fast rythmic bursting']:
    s=e['source']
    t=e['target']
    x12+=[x[num.index(s)], x[num.index(t)], None]
    y12 += [y[num.index(s)], y[num.index(t)], None]
    z12 += [z[num.index(s)], z[num.index(t)], None]

x4=[]
y4=[]
z4=[]
for e in data['spiny stellate']:
    s=e['source']
    t=e['target']
    x4+=[x[num.index(s)], x[num.index(t)], None]
    y4 += [y[num.index(s)], y[num.index(t)], None]
    z4 += [z[num.index(s)], z[num.index(t)], None]


x2=[]
y2=[]
z2=[]
for e in data['superficial interneurons axoaxonic']:
    s=e['source']
    t=e['target']
    x2+=[x[num.index(s)], x[num.index(t)], None]
    y2 += [y[num.index(s)], y[num.index(t)], None]
    z2 += [z[num.index(s)], z[num.index(t)], None]

x1=[]
y1=[]
z1=[]
for e in data['superficial interneurons basket']:
    s=e['source']
    t=e['target']
    x1+=[x[num.index(s)], x[num.index(t)], None]
    y1 += [y[num.index(s)], y[num.index(t)], None]
    z1 += [z[num.index(s)], z[num.index(t)], None]

x3=[]
y3=[]
z3=[]
for e in data['superficial interneurons low threshold spiking']:
    s=e['source']
    t=e['target']
    x3+=[x[num.index(s)], x[num.index(t)], None]
    y3 += [y[num.index(s)], y[num.index(t)], None]
    z3 += [z[num.index(s)], z[num.index(t)], None]

x5=[]
y5=[]
z5=[]
for e in data['pyramidal tufted intrinsic bursting']:
    s=e['source']
    t=e['target']
    x5+=[x[num.index(s)], x[num.index(t)], None]
    y5 += [y[num.index(s)], y[num.index(t)], None]
    z5 += [z[num.index(s)], z[num.index(t)], None]

x7=[]
y7=[]
z7=[]
for e in data['deep interneurons basket']:
    s=e['source']
    t=e['target']
    x7+=[x[num.index(s)], x[num.index(t)], None]
    y7 += [y[num.index(s)], y[num.index(t)], None]
    z7 += [z[num.index(s)], z[num.index(t)], None]

x6=[]
y6=[]
z6=[]
for e in data['pyramidal tufted regular spiking']:
    s=e['source']
    t=e['target']
    x6+=[x[num.index(s)], x[num.index(t)], None]
    y6 += [y[num.index(s)], y[num.index(t)], None]
    z6 += [z[num.index(s)], z[num.index(t)], None]

x10=[]
y10=[]
z10=[]
for e in data['pyramidal nontufted regular spiking']:
    s=e['source']
    t=e['target']
    x10+=[x[num.index(s)], x[num.index(t)], None]
    y10 += [y[num.index(s)], y[num.index(t)], None]
    z10 += [z[num.index(s)], z[num.index(t)], None]

x8=[]
y8=[]
z8=[]
for e in data['deep interneurons axoaxonic']:
    s=e['source']
    t=e['target']
    x8+=[x[num.index(s)], x[num.index(t)], None]
    y8 += [y[num.index(s)], y[num.index(t)], None]
    z8 += [z[num.index(s)], z[num.index(t)], None]

x9=[]
y9=[]
z9=[]
for e in data['deep interneurons low threshold spiking']:
    s=e['source']
    t=e['target']
    x9+=[x[num.index(s)], x[num.index(t)], None]
    y9 += [y[num.index(s)], y[num.index(t)], None]
    z9 += [z[num.index(s)], z[num.index(t)], None]


trace13=go.Scatter3d(x=x13,
               y=y13,
               z=z13,
               mode='lines',
               line=dict(color='red', width=1,),
               name='pyramidal regular spiking',
               showlegend=True,
               hoverinfo='none'
               )
trace12=go.Scatter3d(x=x12,
               y=y12,
               z=z12,
               mode='lines',
               line=dict(color='red', width=1,),
               name= 'pyramidal fast rythmic bursting',
               hoverinfo='none'
               )
trace4=go.Scatter3d(x=x4,
               y=y4,
               z=z4,
               mode='lines',
               line=dict(color='red', width=1,),
               name='spiny stellate',
               showlegend=True,
               hoverinfo='none'
               )
trace5=go.Scatter3d(x=x5,
               y=y5,
               z=z5,
               mode='lines',
               line=dict(color='red', width=1,),
               name='pyramidal tufted intrinsic bursting',
               showlegend=True,
               hoverinfo='none'
               )

trace6=go.Scatter3d(x=x6,
               y=y6,
               z=z6,
               mode='lines',
               line=dict(color='red', width=1,),
               name='pyramidal tufted regular spiking',
               showlegend=True,
               hoverinfo='none'
               )

trace10=go.Scatter3d(x=x10,
               y=y10,
               z=z10,
               mode='lines',
               line=dict(color='red', width=1,),
               name='pyramidal nontufted regular spiking',
               showlegend=True,
               hoverinfo='none'
               )
trace2=go.Scatter3d(x=x2,
               y=y2,
               z=z2,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='superficial interneurons axoaxonic',
               showlegend=True,
               hoverinfo='none'
               )

trace1=go.Scatter3d(x=x1,
               y=y1,
               z=z1,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='superficial interneurons basket',
               showlegend=True,
               hoverinfo='none'
               )
trace3=go.Scatter3d(x=x3,
               y=y3,
               z=z3,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='superficial interneurons low threshold spiking',
               showlegend=True,
               hoverinfo='none'
               )

trace8=go.Scatter3d(x=x8,
               y=y8,
               z=z8,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='deep interneurons axoaxonic',
               showlegend=True,
               hoverinfo='none'
               )

trace7=go.Scatter3d(x=x7,
               y=y7,
               z=z7,
               mode='lines',
               line=dict(color='blue', width=1,),
               name='deep interneurons basket',
               showlegend=True,
               hoverinfo='none'
               )
trace9=go.Scatter3d(x=x9,
               y=y9,
               z=z9,
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



data=[trace, trace12, trace13,trace1,trace2,trace3, trace4, trace5, trace6,trace7, trace8, trace9, trace10]
print(1)
fig=go.Figure(data=data)
print(2)
fig.write_html('net.html')