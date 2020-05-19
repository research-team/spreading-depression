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

L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges, directed=False)

print(data['cells'][0])

name=[]
id=[]
num = []
x=[]
y=[]
z=[]
for cell in data['cells']:
    name.append(cell['name'])
    id.append(cell['id'])
    num.append(cell['num'])
    x.append(cell['x'])
    y.append(cell['y'])
    z.append(cell['z'])

trace1=go.Scatter3d(x=x,
               y=y,
               z=z,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
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

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = go.Layout(
         title="Network (3D visualization)",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text="kek",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )

data=[trace1, trace2]
print(1)
fig=go.Figure(data=data, layout=layout)
print(2)
fig.write_html('net.html')