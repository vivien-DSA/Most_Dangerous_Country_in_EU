  
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------
# Import the clean data (importing csv into pandas dataframe)
df_assaults = pd.read_csv("Assaults_Ratio_in_EU_2010_2018.csv")
df_intentional_homicide = pd.read_csv("Intentional_Homicide_Ratio_in_EU_2008_2018.csv")
df_car_theft = pd.read_csv("theft_of_motorized_land_vehicle_Ratio_in_EU_2008_2018.csv")
df_robbery = pd.read_csv("Robbery_Ratio_in_EU_2008_2018.csv")
# =============================================================================
# #Computing the mean of Crime in general
# dff_avg = df_assaults.mean(axis =1 ) + df_intentional_homicide.mean(axis =1 ) + df_car_theft.mean(axis =1 ) + df_robber.mean(axis =1 )
# print(df_assaults)
# print(dff_avg)
# =============================================================================

    
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
     html.Div([
             #Header1
             html.Header("MOST COUNTRIES IN EUROPE", style={'text-align': 'center'}),
             html.H1('CRIME MAPS per year for each Country'),
                 dcc.Slider(
                    id="slct_year",
                    min=2010,
                    max=2019,
                    marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(2010, 2019)},
                    value=2018,
                ),   
                html.Div(id='output_container', children=[]),
        
             dbc.Row(
                     
                    [
                        dbc.Col(dcc.Graph(id='assaults', figure={})),
                        dbc.Col(dcc.Graph(id='intentional_homicide', figure={})),
                    ],
                    align="start",
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dcc.Graph(id='car_theft', figure={}))),
                        dbc.Col(html.Div(dcc.Graph(id='robbery', figure={}))),
                    ],
                    align="center",
                ),
                ]),

     html.Div([
             #Header2
             html.Header("MOST DANGEROUS COUNTRY IN EUROPE IN 2018", style={'text-align': 'center'}),
             dcc.Graph(id='treemap_draw'),
             ]),

    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='assaults', component_property='figure'),
     Output(component_id='intentional_homicide', component_property='figure'),
    Output(component_id='car_theft', component_property='figure'),
    Output(component_id='robbery', component_property='figure'),
    Output(component_id='treemap_draw', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):

    #Create copy of dataframes
    dff_assaults = df_assaults.copy()
    dff_intentional_homicide = df_intentional_homicide.copy()
    dff_car_theft = df_car_theft.copy()
    dff_robbery = df_robbery.copy()
    
    # Plotly Express
    fig_assaults = px.choropleth(
        
        data_frame=dff_assaults,
        locations='Country Code',
        hover_name='Country Name',
        scope="europe",
        projection='equirectangular',
        color = str(option_slctd),
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title="Assaults"
    )
    fig_intentional_homicide = px.choropleth(
        
        data_frame=dff_intentional_homicide,
        locations='Country Code',
        hover_name='Country Name',
        scope="europe",
        projection='equirectangular',
        color = str(option_slctd),
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title = 'Intentional Homicide'
    )
    fig_car_theft = px.choropleth(
        
        data_frame=dff_car_theft,
        locations='Country Code',
        hover_name='Country Name',
        scope="europe",
        projection='equirectangular',
        color = str(option_slctd),
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title="Car theft"

    )
    fig_robbery = px.choropleth(
        
        data_frame=dff_robbery,
        locations='Country Code',
        hover_name='Country Name',
        scope="europe",
        projection='equirectangular',
        color = str(option_slctd),
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title = 'Robbery'
    )
    df_robbery["EU"] = "EU" # in order to have a single root node
    fig_3 = px.treemap(df_robbery, path=['EU', 'Country Name'], values='2018',
                  color='Total AVG', color_continuous_scale=px.colors.sequential.YlOrRd )

    return  fig_assaults, fig_intentional_homicide, fig_car_theft, fig_robbery, fig_3


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

