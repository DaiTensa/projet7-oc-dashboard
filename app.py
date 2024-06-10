import dash
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash import dcc
import requests
from dash.dependencies import Output, Input, State
import json
import plotly.graph_objects as go
import pandas as pd

# Test
# id_test = 100038
# shap = requests.get(f'{url_server}/shape/{id_test}')
# Test modification CI 


# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# Local : pour run le dashboard en mode local, run l'API préalablement (voir les instruction dans le dossier projet7-oc-api)
# url_server = 'http://127.0.0.1:5000'

# Server
url_server = 'https://scoringapp.pythonanywhere.com'
liste_ids = requests.get(f'{url_server}/listeidclients')
liste_columns_names = requests.get(f'{url_server}/listecolumnsnames')

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Acceuil Projet", href="https://github.com/DaiTensa/projetscoring")),
        dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/DaiTensa/projet7-oc-dashboard")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Choix...", header=True, href="#"),
                dbc.DropdownMenuItem("Fonctionnalités", header=False, href="#"),
                dbc.DropdownMenuItem("Data Client", header=False, href="https://github.com/DaiTensa/dashboard/blob/main/reduced_test.csv"),
                dbc.DropdownMenuItem("Simulation Crédit", header=False, href="#"),
                ],
            nav=True,
            in_navbar=True,
            label="Fonctionnalités",
            ),
        ],
    brand="ScoringApp",
    brand_href="https://scoringdash.pythonanywhere.com",
    color="primary",
    dark=True,
    )

identification_client_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4('ID Client'),
                        dcc.Dropdown(options=liste_ids.json(), id='dropdown-selection', style={'width': '190px'}, value=100038),
                        html.Br(),
                        html.Div(id='dropdown-id-input'),
                        
                    ]
                    )
                ]
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Identification Client'),
                        dcc.Input(
                            id='nom_input',
                            value='',
                            type='text',
                            placeholder='Nom',
                            debounce=True,
                            ),
                        dcc.Input(
                            id='prenom_input',
                            value='',
                            type='text',
                            placeholder='Prénom',
                            debounce=True,
                            style={'margin-left': '0.5rem'}
                            ),
                        html.Br(),
                        html.Div(id='identification-client-output'),
                        ])
                ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        dcc.Input(
                            id='input-info-3',
                            value='',
                            type='text',
                            placeholder='Info 3',
                            debounce=True
                            ),
                        dcc.Input(
                            id='input-info-4',
                            value='',
                            type='text',
                            placeholder='Info 4',
                            debounce=True,
                            style={'margin-left': '0.5rem'}
                            ),
                        html.Br(),
                        html.Div(id='identification-client-output-2'),
                        ]
                    )
                ]),
        html.Br(),
        dbc.Button("Rechercher", id="example-button", className="me-2", n_clicks=0),
               
                ])

resume_data_client = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Résumé Informations Client'),
                        html.Br(),
                        html.Div(children=[
                            html.P("Résumé"),
                            ],id='resume-data-client-output'),
                        ])
                ]),
        ])

data_du_client = html.Div(children=[
    dash_table.DataTable(
        id="table",
        page_size=10,
        editable=False,
        cell_selectable=True,
        # filter_action="native",
        # sort_action="native",
        style_table={"overflowX": "auto"},
        # row_selectable="multi",
    )],
                          className="dbc-row-selectable", id="data-frame-client"
                          )

shape_values_client = html.Div(children=[
    dash_table.DataTable(
        id="table-shape-values-client",
        page_size=10,
        editable=False,
        cell_selectable=True,
        # filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto", "overflowY": "auto"},
        # row_selectable="multi",
    )],
                               className="dbc-row-selectable", id="shape-data-frame-client"
                               )

describe_data_du_client = html.Div(children=[
    dash_table.DataTable(
        id="table-describe-data-client",
        page_size=3,
        editable=False,
        cell_selectable=False,
        # filter_action="native",
        # sort_action="native",
        style_table={"overflowX": "auto", "overflowY": "scroll"},
        # row_selectable="multi",
    )],
                                   className="dbc-row-selectable", id="describe-data-frame-client"
                                   )

graphique_shape_values = html.Div(children=[
    # html.H1('Graphique des Shape Values'),
    dbc.Label("Nombre de variables à afficher : ", className="bg-transparent"),
    dcc.Dropdown(options=[5,10,15,20,30], id='dropdown-profondeur-shape', style={'width': '190px'}, value=0),
    dcc.Graph(
        id='shape-values-graph',
        figure={
            
                        }
        )
    ],id="graph-shape-values", className="mb-4"
                                  )

############################### Graphiques Client #####################################
graphique_1 = html.Div(children=[

    dcc.Graph(
        id='graph-1',
        figure={
            
                        }
        )
    ],id="div-graph-1", className="mb-4"
                                  )



graphique_2 = html.Div(children=[

    dcc.Graph(
        id='graph-2',
        figure={
            
                        }
        )
    ],id="div-graph-2", className="mb-4"
                                  )

graphique_3 = html.Div(children=[

    dcc.Graph(
        id='graph-3',
        figure={
            
                        }
        )
    ],id="div-graph-3", className="mb-4"
                                  )


#######################################################################################


decision = ""
graphique_jauge_proba = html.Div(
    children=[
        html.H3('Simulation Crédit'),
        html.P(children = f"Le client : {decision}", id="decision-id", style={'textAlign': 'left','color': 'orange','fontSize': 40}),
        dcc.Graph(
            id='proba-solvable',
            figure={

            }
        )
    ],
    id="graph-proba",
)

simulation_data_client = dbc.Container([
    dbc.Row([
        dbc.Col([
            # html.H3('Simulation Crédit'),
            # html.Br(),
            # html.Div(children = [
            #     html.P("Ici Afficher résultat de la prédiction sous forme d'une jauge"),
            #     ],id='simulation-data-client-output'),
            graphique_jauge_proba
        ])
    ]),
])


tab1 = dbc.Tab([data_du_client], label="Table", className="p-4", id="data-client")
tab2 = dbc.Tab([describe_data_du_client], className="p-4", label="Describe", id="describe-data")
tab3 = dbc.Tab([shape_values_client], className="p-4", label="Détail Shape", id="shape-data")
tab4 = dbc.Tab([graphique_shape_values], label="Graph Shape", className="p-4", id="shape-data-graph")

tab5 = dbc.Tab([graphique_1], label="Graph_1", className="p-4", id="tab-graph-1")
tab6 = dbc.Tab([graphique_2], label="Graph_2", className="p-4", id="tab-graph-2")


tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3, tab4]))
tabs_graph = dbc.Card(dbc.Tabs([tab5, tab6]))


resultats_client_container = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('Data Client et résultats'),
            tabs,
            html.Br(),
            html.Div(id='output-data'),
        ])
    ])
])


################################################################

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=liste_columns_names.json(),
                    value="AMT_CREDIT",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=liste_columns_names.json(),
                    value="AMT_ANNUITY",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Nombre de client"),
                dbc.Input(id="cllient-count", type="number", value=0),
            ]
        ),
        html.Div(
            [
                html.Br(),
                dbc.Button("Afficher client", id="afficher-client", className="me-2", n_clicks=0),
            ]
        ),
    ],
    body=True,
) 

resume_data_client_var = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Informations Client Graph'),
                        html.Br(),
                        controls
                        ]),
                
                ]),
        ], fluid=True)


resume_data_client_graph = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Visualisation'),
                        html.Br(),
                        tabs_graph
                        ]),
                
                ]),
        ], fluid=True)


################################################################

#### Séction et lignes #####

left_section = dbc.Container(
    [
        identification_client_container
    ],
    className="mt-2"
)

right_section = dbc.Container(
    [
        simulation_data_client
    ],
    className="mt-2"
)

left_section_down = dbc.Container(
    [
        resume_data_client
    ],
    className="mt-2"
)

right_section_down = dbc.Container(
    [
        resultats_client_container
    ],
    className="mt-2"
)

right_section_down_down = dbc.Container(
    [
        resume_data_client_var
    ],
    className="mt-2"
)

left_section_down_down = dbc.Container(
    [
     resume_data_client_graph   
    ],
    className="mt-2"
)

sections_row = dbc.Row([dbc.Col(left_section, width=4), dbc.Col(right_section, width=7)])
sections_row_down = dbc.Row([dbc.Col(left_section_down, width=4), dbc.Col(right_section_down, width=7)])
sections_row_down_down = dbc.Row([dbc.Col(right_section_down_down, width=4), dbc.Col(left_section_down_down, width=7)])

### CallBack ###

# update data du client
@app.callback(
    Output(component_id='data-frame-client', component_property='children'),
    [Input(component_id='dropdown-selection', component_property='value')],
)
def update_data_client(value):
    if value:
        response_df_client = requests.get(f'{url_server}/data/{value}')
        df_client_json = response_df_client.json()
        df_client = pd.DataFrame.from_dict(df_client_json)
        table = dash_table.DataTable(
            id="table",
            columns=[{"name": col, "id": col} for col in df_client.columns],
            data=df_client.to_dict("records"),
            page_size=10,
            editable=False,
            cell_selectable=False,
            # filter_action="native",
            # sort_action="native",
            style_table={"overflowX": "auto"},
            # row_selectable="multi",
        )
        return table

# update describe data du client
@app.callback(
    Output('describe-data-frame-client', "children"),
    [Input('dropdown-selection', "value")]
)
def return_info_client(value):
    if value:
        response_df_client = requests.get(f'{url_server}/data/{value}')
        if response_df_client.ok:
            df_client_json = response_df_client.json()
            df_client = pd.DataFrame.from_dict(df_client_json)
            summary = df_client.describe()
            summary = summary.reset_index()
            describe_data_du_client = html.Div(children=[dash_table.DataTable(
                id="table-describe-data-client",
                columns=[{"name": i, "id": i, "deletable": False} for i in summary.columns],
                data=summary.to_dict('records'),
                page_size=3,
                editable=False,
                cell_selectable=False,
                style_table={"overflowX": "auto", "overflowY": "scroll"},
                # row_selectable="multi",
            )],
                className="dbc-row-selectable", id="describe-data-frame-client"
            )
            return describe_data_du_client

# les shap values sous frome de tableau
@app.callback(
    Output('shape-data-frame-client', "children"),
    [Input('dropdown-selection', "value")]
)
def return_shape_client(value):
    if value:
        response_shape_client = requests.get(f'{url_server}/shape/{value}')
        if response_shape_client.ok:
            shape_client_json = response_shape_client.json()
            shape_client = pd.DataFrame.from_dict(shape_client_json)
            shape_data_du_client = html.Div(children=[dash_table.DataTable(
                id="table-describe-data-client",
                columns=[{"name": i, "id": i, "deletable": False} for i in shape_client.columns],
                data=shape_client.to_dict('records'),
                page_size=10,
                editable=False,
                cell_selectable=False,
                sort_action="native",
                style_table={"overflowX": "auto", "overflowY": "auto"},
                # row_selectable="multi",
            )],
                className="dbc-row-selectable", id="shape-data-frame-client"
            )
            return shape_data_du_client

# les shap values sous frome de graph
@app.callback(
    Output('shape-values-graph', "figure"),
    [Input('dropdown-selection', "value")],
    [Input('dropdown-profondeur-shape', "value")]
)
def return_shape_graph_client(value_id, value_deep):
    if value_id:
        response_df_shape_client = requests.get(f'{url_server}/shape/{value_id}')
        if response_df_shape_client.ok:
            df_shape_client_json = response_df_shape_client.json()
            df_shape_client = pd.DataFrame.from_dict(df_shape_client_json)
            df_shape_client = df_shape_client.sort_values(by=["features_importance_abs"], ascending=False)
            df_shape_client = df_shape_client.head(value_deep)
            colors = ['rgb(58, 0, 255)' if val < 0 else 'rgb(255, 0, 0)' for val in df_shape_client['shape_values']]           
            figure={
                'data': [
                    go.Bar(
                        x= df_shape_client['Features'],
                        y= df_shape_client['shape_values'],
                        name='Shape Values',
                        marker=dict(color=colors),
                        # orientation='h'
                        )
                    ],
                'layout': go.Layout(
                    title='Shape Values',
                    xaxis={'title': 'Features'},
                    yaxis={'title': 'Shape Values'}
                    )
                }
            return figure
     
# graphique proba jauge
@app.callback(
    Output('proba-solvable', "figure"),
    Output('decision-id', "children"),
    [Input('dropdown-selection', "value")]
)
def return_jauge_proba(value):
    if value:
        response_pred_client = requests.get(f'{url_server}/proba/{value}')
        if response_pred_client.ok:
            response_json = response_pred_client.json()
            proba = response_json["proba"]
            seuil = response_json["seuil"]
            decision = 'Le client est : Solvable' if proba>seuil else 'Le client est : Insolvable'
            figure=go.Figure(go.Indicator(
                mode = "number+gauge+delta", value = proba,
                domain = {'x': [0, 1], 'y': [0, 1]},
                # title = {'text' :f"{decision}"},
                delta = {'reference': 1},
                gauge = {
                    'shape': "bullet",
                    'axis': {'range': [None, 1]},
                    'threshold': {
                        'line': {'color': "red", 'width': 2},
                        'thickness': 0.75,
                        'value': 0.5},
                    'steps': [
                        {'range': [0, 0.45], 'color': "lightgray"},
                        {'range': [0.45,0.6], 'color': "rgb(249, 148, 11)"},
                        {'range': [0.6,1 ], 'color': "rgb(0, 231, 105)"},
                        
                        ]}))
            figure.update_layout(width = 700 , height = 250)
                            
            return figure, decision

# retrun résumé data client
@app.callback(
    Output('resume-data-client-output', "children"),
    [Input('dropdown-selection', "value")]
)
def return_resume_client(value):
    if value:
        response_df_client = requests.get(f'{url_server}/data/{value}')
        if response_df_client.ok:
            df_client_json = response_df_client.json()
            df_client = pd.DataFrame.from_dict(df_client_json)
            genre = df_client['CODE_GENDER'][0]
            if genre == 0:
                sex = "Femme"
            else:
                sex = "Homme"
            income = df_client['AMT_INCOME_TOTAL'][0]
            credit = df_client['AMT_CREDIT'][0]
            annuity = df_client['AMT_ANNUITY'][0]
            goodsprice = df_client['AMT_GOODS_PRICE'][0]

            return html.Div(children = [
                html.P(f"Genre : {sex}", style={'textAlign': 'left','color': '#9520f9','fontSize': 20}, className="bg-light"),
                html.P(f"Income :  {income}", style={'textAlign': 'left','color': '#9520f9','fontSize': 20}, className="bg-light"),
                html.P(f"AMT_CREDIT :  {credit}", style={'textAlign': 'left','color': '#9520f9','fontSize': 20}, className="bg-light"),
                html.P(f"AMT_ANNUITY :  {annuity}", style={'textAlign': 'left','color': '#9520f9','fontSize': 20}, className="bg-light"),
                html.P(f"AMT_GOODS_PRICE :  {goodsprice}", style={'textAlign': 'left','color': '#9520f9','fontSize': 20}, className="bg-light"),
                ],id='resume-data-client-output')

# client count 
@app.callback(
    Output("graph-1", "figure"),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("cllient-count", "value"),
        Input(component_id='dropdown-selection', component_property='value'),
        Input("afficher-client", "n_clicks")
    ],
)
def make_graph(X, Y, n_cllient,id_client, n_clicks):
    X = str(X)
    Y = str(Y)
    response_df_clients = requests.get(f'{url_server}/dataclients/{n_cllient}')
    df_clients_json = response_df_clients.json()
    df_clients = pd.DataFrame.from_dict(df_clients_json)
    data_to_plot = df_clients.loc[:, [X,Y]]
    figure={
        'data': [
            go.Scatter(
                x= data_to_plot.loc[:, X],
                y= data_to_plot.loc[:, Y],
                name='Données Clients',
                mode="markers",
                marker={"size": 8}, 
                )
            ],
        'layout': go.Layout(
                    title=f'{X}--{Y}',
                    xaxis={'title': X},
                    yaxis={'title': Y}
                    )
                }
    if n_clicks > 0:
        response_df_client = requests.get(f'{url_server}/data/{id_client}')
        df_client_json = response_df_client.json()
        df_client = pd.DataFrame.from_dict(df_client_json)
        df_client_to_plot = df_client.loc[:, [X, Y]]
        graph_client = go.Scatter(
            x=df_client_to_plot[X],
            y=df_client_to_plot[Y],
            name=f'Client : {id_client}',
            mode="markers",
            marker={"size": 10, "symbol": "star"}  # Changer le marker à votre convenance
        )
        figure['data'].append(graph_client)
        
    return figure


        







app.layout = html.Div([
    html.Div(children=[
        header,
        sections_row,
        sections_row_down,
        sections_row_down_down
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
