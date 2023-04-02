import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

h = lambda step: 2*np.pi / step
inv = np.linalg.inv

G = lambda h: {
    "f": np.array([[1, h], [-h, 1]]),
    "b": inv(np.array([[1, -h], [h, 1]])),
    "t": inv(np.array([[1, -h/2], [h/2, 1]])) @ np.array([[1, h/2],[-h/2, 1]]),
    "l": np.array([[1, h], [-h, 1-h**2]])
}

V = lambda step: np.zeros([10*step+1, 1])
U = lambda step: np.eye(10*step+1)[:,0]

cx = np.cos(np.arange(0, 10 * 2*np.pi, 0.001))
cy = np.sin(np.arange(0, 10 * 2*np.pi, 0.001))
cxstep = lambda step: np.cos(
    np.arange(0,10 * 2*np.pi + h(step), h(step))
)

mat_type = {
    "Forward Euler": "f",
    "Backward Euler": "b",
    "Trapezoidal": "t",
    "Leapfrog": "l"
}

def solve(step, mat_type):
    v = V(step)
    u = U(step)
    g = G(h(step))[mat_type]
    for i in range(10*step):
        (u[i+1], v[i+1]) = g @ np.array([u[i], v[i]]).T
    return u, v


app = Dash(__name__)

app.layout = html.Div(children = [
    html.H1(
        children="Euler Method for Dynamic Systems", 
        style={'textAlign': 'center'}
    ),
    
    html.Div(
        children="Solutions to the equation u'' + u= 0 with initial conditions u' = 0, u = 1",
        style={'textAlign': 'center'}
    ),

    html.H2(
        children="Phase Space",
        style={'textAlign': 'center'}
    ),

    dcc.Graph(
        id="phase-graph",
        style={
            "width": "30vw",
            "height": "30vw",
            "margin": "0 auto",
        }
    ),
    html.Div(
        
        [html.Div(
            children="Number of Steps:",
            style={'textAlign': 'center'}
        ),

        dcc.Slider(
            10,
            100,
            step=5,
            id="step-slider",
        ),

        html.Div(
            children="Integration type:",
            style={'textAlign': 'center'}
        ),

        dcc.RadioItems(
            ["Forward Euler", "Backward Euler", "Trapezoidal", "Leapfrog"],
            "Forward Euler",
            id="mat-type",
            style={"margin": "0 auto", "textalign": "center"}
        ),],
        style = {"margin": "0 auto", "width": "70vw"}
    ),
    
    html.H2(
        children="Time space",
        style={'textAlign': 'center'}
    ),

    dcc.Graph(
        id="time-graph",
        style={
            "width": "60vw",
            "height": "30vw",
            "margin": "0 auto",
        }
    ),
    
    html.H2(
        children="Error",
        style={'textAlign': 'center'}
    ),

    
    dcc.Graph(
        id="error-graph",
        style={
            "width": "60vw",
            "height": "30vw",
            "margin": "0 auto",
        }
    ),

])

@app.callback(
    Output("phase-graph", "figure"),
    Input("step-slider","value"),
    Input("mat-type","value"))
def update_phase(step, matrix):
    u,v = solve(step, mat_type[matrix])
    fig = px.line(
            x = cx,
            y = cy,
    )
    fig.update_traces(
        line=dict(width=1, color="gray")
    )
    fig.add_trace(
        go.Scatter(
            x=u[0:step+1], y=v.T[0][0:step+1],
            mode="lines", 
            line = go.scatter.Line(width=1.5, color="red"),
            showlegend=False
        )
    )
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1)
    return fig

@app.callback(
    Output("time-graph", "figure"),
    Output("error-graph", "figure"),
    Input("step-slider","value"),
    Input("mat-type","value"))
def update_time(step, matrix):
    u,v = solve(step, mat_type[matrix])
    x = np.arange(0, 10 + h(step)/(2*np.pi), h(step)/(2*np.pi))
    fig = px.line(
            x = np.arange(0,10,0.001/(2*np.pi)),
            y = cx)
    fig.update_traces(
        line=dict(width=1, color="gray")
    )
    fig.add_trace(
        go.Scatter(
            x=x, y=u,
            mode="lines", 
            line = go.scatter.Line(width=1.5, color="red"),
            showlegend=False
        )
    )
    erfig = px.line(
        x=x, y=u - cxstep(step),
    )
    erfig.update_traces(
        line=dict(width=2, color="red")
    )
    return fig, erfig


if __name__ == "__main__":
    app.run_server()
