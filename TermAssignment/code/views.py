from dash import dcc, html

def supplier_layout():
    print('inside views')
    return html.Div([
        html.H1('Supplier Performance'),
        html.Div(id='supplier-count', style={'font-weight': 'bold', 'font-size': '20px', 'display': 'inline-block','border': '1px solid black', 'border-radius': '10px', 'padding':'5px','margin-left': '3%'}),
        html.Button('Email Progress Report', id='btn-notify', n_clicks=0, className='button'),
        dcc.Graph(id='sales-bar-chart'),
        dcc.Graph(id='choropleth-map'),
        dcc.Graph(id='suppliers-line-chart')
    ])

def customer_layout():
    return html.Div([
        html.H1('Customer Analysis'),
        html.Div(id='customer-count', style={'font-weight': 'bold', 'font-size': '20px', 'display': 'inline-block','border': '1px solid black', 'border-radius': '10px', 'padding':'5px','margin-left': '3%'}),
        dcc.Graph(id='jobtitle-carprice-graph'),
        dcc.Graph(id='gender-analysis'),
        dcc.Graph(id='shipments-analysis')
    ])

def car_layout():
    return html.Div([
        html.H1('Car Sales Analysis'),
        html.Div(id='car-maker-count', style={'font-weight': 'bold', 'font-size': '20px', 'display': 'inline-block','border': '1px solid black', 'border-radius': '10px', 'padding':'5px','margin-left': '3%'}),
        dcc.Graph(id='top5carmakers-line-chart'),
        dcc.Graph(id='popular-colors'),
        dcc.Graph(id='carmodel-sales')
    ])
