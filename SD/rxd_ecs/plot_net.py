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

Li=len(data['ing'])
Le=len(data['exc'])
Edges_i=[(data['ing'][k]['source'], data['ing'][k]['target']) for k in range(Li)]
Edges_e=[(data['exc'][k]['source'], data['exc'][k]['target']) for k in range(Le)]

Gi=ig.Graph(Edges_i, directed=False)
Ge=ig.Graph(Edges_e, directed=False)

print(data['cells'][0])
#print(data['links'][0])

name=[]
id=[]
num = []
x=[]
y=[]
z=[]
c=[]
xi=[]
yi=[]
zi=[]

xe=[]
ye=[]
ze=[]
for cell in data['cells']:
    name.append(cell['name'])
    id.append(cell['id'])
    num.append(cell['num'])
    x.append(cell['x'])
    y.append(cell['y'])
    z.append(cell['z'])

for e in data['ing']:
    s=e['source']
    t=e['target']
    xi+=[x[num.index(s)], x[num.index(t)], None]
    yi += [y[num.index(s)], y[num.index(t)], None]
    zi += [z[num.index(s)], z[num.index(t)], None]

for e in data['exc']:
    s=e['source']
    t=e['target']
    xe+=[x[num.index(s)], x[num.index(t)], None]
    ye += [y[num.index(s)], y[num.index(t)], None]
    ze += [z[num.index(s)], z[num.index(t)], None]

trace1=go.Scatter3d(x=xi,
               y=yi,
               z=zi,
               mode='lines',
               line=dict(color='red', width=1,),
               name='ing',
               showlegend=True,
               hoverinfo='none'
               )

trace3=go.Scatter3d(x=xe,
               y=ye,
               z=ze,
               mode='lines',
               line=dict(color='blue', width=1,),
               name= 'exc',
               hoverinfo='none'
               )
trace2=go.Scatter3d(x=x,
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
               text=num,
               hoverinfo='text'
               )



data=[trace1, trace2, trace3]
print(1)
fig=go.Figure(data=data)
print(2)
fig.write_html('net.html')