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
trace=go.Scatter3d(x=x,
               y=y,
               z=z,
               mode='markers',
               name='actors',
               marker=dict(symbol='circle',
                             size=6,
                             color=id,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=name,
               hoverinfo='text'
               )



data=[trace, trace12, trace13]
print(1)
fig=go.Figure(data=data)
print(2)
fig.write_html('net.html')