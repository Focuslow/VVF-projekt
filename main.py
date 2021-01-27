from mnc import mnc
from rmnc import rmnc
import math
import numpy as np
from scipy import signal
import dash
import random as rand
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ALL, MATCH
import dash_html_components as html
import plotly.graph_objects as go
def layout(app):
    main_color = '#016e3f'
    text_color = '#000000'
    return html.Div(children = [
        dcc.RadioItems(id = 'visibility',
            options = [{'label': i, 'value': i} for i in ['Visible', 'Invisible']],
            value = 'Visible', labelStyle={'display': 'inline-block'},
            style={'textAlign': 'center','margin-top': '15px', 'color':main_color}),

        html.Div(id = 'main', className = 'app-div', children = [

            html.Hr(style = {'width': '500px'}),

            html.Div(id = 'param', className = 'app-div', children = [
                dcc.RadioItems(id = 'systFunc',
                options = [{'label': i, 'value': i} for i in ['Sinus', 'Rectangle', 'Triangel']],
                value = 'Sinus', labelStyle={'display': 'inline-block'},
                style={'textAlign': 'center','margin-top': '15px', 'color':text_color}),

                dcc.Input(id = 'amplitude', placeholder='Enter aplitude...',
                        type='number',  debounce=True),

                dcc.Input(id = 'periode', placeholder='Enter periode...',
                        type='number',  debounce=True),

            ],style = {'display':'inline-block'}),
            html.Div(id = 'function', className = 'app-div', children = [
                html.Hr(style = {'width': '500px'}),

                html.P('Type as 1., 4., 1.5, 0.', style = {'color':text_color}),

                dcc.Input(id = 'numerator', placeholder='Enter numerator...',
                        type='text',  debounce=True),

                dcc.Input(id = 'denominator', placeholder='Enter denominator...',
                        type='text',  debounce=True),

            ],style = {'display':'inline-block'}),

            dcc.Input(id = 'time', placeholder='Enter time...',
                type='number',  debounce=True),

            dcc.Input(id = 'timeStep', placeholder='Enter time step...',
                type='number',  debounce=True),

            html.Hr(style = {'width': '500px'}),

            dcc.Dropdown(id='metod', style = {'width': '500px', 'padding-left':'25px'},
                options=[{'label': 'Least squares metod', 'value': 'mnc'},
                {'label': 'Recursive least squares metod', 'value': 'rmnc'}],value='mnc'),

            html.Div(id = 'start_btn',className='butt', children=[
                html.Hr(style = {'width': '500px'}),

                html.P('Start your simulation', style = {'color':text_color}),

                html.A(
                    html.Button(
                        id='start',
                        className='satrt_btn',
                        children="Start",
                        n_clicks=0,
                        style = {'color':'#ffffff', 'background-color': text_color}
                    ),
                ),
                html.Hr(style = {'width': '500px', 'color':main_color}),
            ]),
        ]),
        html.Div(children = [
            dcc.Graph(id="graph", style={'height': '890px'}),
        ],style = {'float': 'right', 'display':'inline-block'}),
    ], style={'height': '890px'})

def callbacks(app):

    @app.callback(
        [Output('main', 'style'),
        Output('graph', 'style')],
        [Input('visibility', 'value')]
    )
    def show_param(x):
        main_color = "#016e3f"
        if x == 'Visible':
            return [{'display':'inline-block','width':'550px', 'borderRadius': '20px',
                'textAlign': 'center', "background-color":main_color},
                {'width':'1300px'}]
        else:
            return [{'display':'none'}, {'width':'1900px'}]
    @app.callback(
        Output('graph','figure'),
        [Input('start', 'n_clicks')],
        [State('metod', 'value'),
        State('systFunc', 'value'),
        State('amplitude', 'value'),
        State('periode', 'value'),
        State('numerator', 'value'),
        State('denominator', 'value'),
        State('time', 'value'),
        State('timeStep', 'value')]
    )
    def show_graph(btnStart, metod, systFunc, ampl, period, numerator, denominator, time, timeStep):
        data = []
        aproxData = []
        numbPoly = 0
        num, den = ownFunction(numerator, denominator)
        num = np.array(num)
        den = np.array(den)
        if systFunc == 'Sinus':
            data = sinusFun(ampl, period, time, timeStep)
        elif systFunc == 'Rectangle':
            data = rectangleFun(ampl, period, time, timeStep)
        else:
            data = triangelFun(ampl, period, time, timeStep)
        tout, yout, x = signal.lsim(signal.lti(num, den), data[1], data[0])
        if metod == 'rmnc':
            aproxData = rmnc(yout, tout, data[1])
        else:
            aproxData = mnc(yout, tout, data[1])

        fig = go.Figure(data = [])
        fig.add_trace(go.Scatter(x=tout, y=data[1], mode = 'lines', name='input'))
        fig.add_trace(go.Scatter(x=tout, y=yout, mode = 'lines', name='system output'))
        fig.add_trace(go.Scatter(x=tout, y=aproxData, mode = 'lines', name='aproximation'))
        return fig

def ownFunction(numerator, denominator):
    l = numerator.split(", ")
    r = denominator.split(", ")
    p, q = [], []
    for i in l:
        p.append(float(i))
    for i in r:
        q.append(float(i))
    return p, q

def sinusFun(ampl, period, time, timeStep):
    data = []
    y = []
    t = []
    i = 0.0
    while i <= time:
        t.append(i)
        y.append(ampl*math.sin(2*math.pi*i/period)+0.3*rand.random()+math.sin(2*math.pi/10*i))
        i += timeStep
    data.append(t)
    data.append(y)
    return data

def rectangleFun(ampl, period, time, timeStep):
    data = []
    y = []
    t = []
    i = 0.0
    while i <= time:
        t.append(i)
        y.append(ampl*np.sign(math.sin(2*math.pi*i/period)))
        i += timeStep
    data.append(t)
    data.append(y)
    return data

def triangelFun(ampl, period, time, timeStep):
    data = []
    y = []
    t = []
    i = 0.0
    while i <= time:
        t.append(i)
        y.append(2*ampl*math.asin(math.sin(2*math.pi*i/period))/math.pi)
        i += timeStep
    data.append(t)
    data.append(y)
    return data

app = dash.Dash(__name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    suppress_callback_exceptions=True)
app.layout = layout(app)
callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)