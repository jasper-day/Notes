import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

x = np.arange(-2,2, 0.02)
xx, yy = np.meshgrid(x,x)

strzz = lambda rot: yy - yy/(xx**2 + yy**2) + rot*np.log(np.sqrt(xx**2 + yy**2))
strfun = lambda rot: np.clip(strzz(rot), -2, 2)

app = Dash(__name__)

app.layout = html.Div(children = [
    html.H1(
        children="Lifting Flow Over A Cylinder", 
        style={'textAlign': 'center'}
    ),
    
    html.Div(
        children="Drag the slider to change the circulation around the cylinder",
        style={'textAlign': 'center'}
    ),

    dcc.Graph(
        id="cylinder-graph",
        style={
            "width": "50vw",
            "height": "50vw",
            "margin": "0 auto",
        }
    ),

    dcc.Slider(
        0,
        5,
        id="rotation-slider",
        
    ),
])

@app.callback(
    Output("cylinder-graph", "figure"),
    Input("rotation-slider","value"))
def update_figure(rotation):
    if rotation == None:
        rotation = 0
    contours = strfun(rotation)
    fig = go.Figure(data = go.Contour(z = contours))
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1)
    return fig


if __name__ == "__main__":
    app.run_server(host= '192.168.0.67', debug = True)