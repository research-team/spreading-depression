import plotly.graph_objects as go
import pandas as pd
import os
import csv
outdir = os.path.abspath('tests/963_tW')


#df = pd.read_csv('tests/950_tW/spikeE.csv', sep=',')
x = []
y = []
with open('tests/963_tW/spikeI.csv', newline='') as File:
    reader = csv.reader(File)

    for row in reader:
        try:
            for i in row[4:]:
                x.append(int(float(i)))
                y.append(int(float(row[2])))
        except Exception:
            print(Exception)
print(len(y))
print(len(x))
fig = go.Figure(go.Histogram2d(
        x=x,
        y=y,
        xbins=dict(start=0, end=30, size=0.1),
        #autobiny=False,
        ybins=dict(start=-850, end=1300, size=10),
    ))
#fig.show()
fig.write_html(os.path.join(outdir,'spikeI.html'))