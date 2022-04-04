import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# FOR THE PROJECT: ALSO CHECK BOOTSTRAP COMPONENTS !!!

# https://htmlcheatsheet.com/css/ --> get new css classes

######################################################   Data   ##############################################################

#path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'

df = pd.read_csv("C:/Users/tsoom/OneDrive/Documentos/IMS - Data Science/2º Semester/Data Visualization/Project Dashboard/CSVs/Deaths_state_based_conflicts!!.csv")

######################################################  Interactive Components  ############################################

world_regions = [dict(label=region, value=region) for region in df['Entity'].unique()]
#print(world_regions)

deaths_col = 'Deaths in all state-based conflict types'
years = [dict(label=year, value=year) for year in df['Year'].unique()]

dropdown_world_regions = dcc.Dropdown(
    id='world_regions_drop',
    options=world_regions,
    value=['Europe'],
    multi=True
)

slider_year = dcc.Slider(
    id='year_slider',
    min=df['Year'].min(),
    max=df['Year'].max(),
    marks={str(i): '{}'.format(str(i)) for i in
           [1990, 1995, 2000, 2005, 2010, 2014]},
    value=df['Year'].min(),
    step=1
)

# radio_lin_log = dcc.RadioItems(
#     id='lin_log',
#     options=[dict(label='Linear', value=0), dict(label='log', value=1)],
#     value=0
# )


##################################################   APP   ###################################################################

app = dash.Dash(__name__)

server = app.server

# LAYOUT !!
app.layout = html.Div([

    html.Div([
        html.H1('Deaths in state-based conflicts'),
    ], className="box_pretty"),

    html.Div([
        html.Label('Country Choice'),
        dropdown_world_regions,

        dcc.Graph(id='line_chart', className="box_pretty"),
        html.Label('Year Slider'),
        slider_year,
    ]),
])


###################################   Callbacks   ##########################################
@app.callback(
    [
        Output("line_chart", "figure"),
    ],
    [
        Input("year_slider", "value"),
        Input("dropdown_world_regions", "value"),
    ]
)
# first the inputs, then the states, by order
def plots(world_regions, deaths_col):
    ############################################ First Bar Plot ##########################################################
    data_bar = []
    for region in world_regions:
        df_bar = df.loc[(df['Entity'] == region)]

        x_bar = df_bar['Year']
        y_bar = df_bar[deaths_col]

        data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=region))

    layout_bar = dict(title=dict(text='Deaths in all state-based conflict types'),
                      yaxis=dict(title='Deaths'),
                      paper_bgcolor='#f9f9f9'
                      )

    # #############################################Second Choropleth######################################################
    #
    # df_emission_0 = df.loc[df['year'] == year]
    #
    # z = np.log(df_emission_0[gas])
    #
    # data_choropleth = dict(type='choropleth',
    #                        locations=df_emission_0['country_name'],
    #                        # There are three ways to 'merge' your data with the data pre embedded in the map
    #                        locationmode='country names',
    #                        z=z,
    #                        text=df_emission_0['country_name'],
    #                        colorscale='inferno',
    #                        colorbar=dict(title=str(gas.replace('_', ' ')) + ' (log scaled)'),
    #
    #                        hovertemplate='Country: %{text} <br>' + str(gas.replace('_', ' ')) + ': %{z}',
    #                        name=''
    #                        )
    #
    # layout_choropleth = dict(geo=dict(scope='world',  # default
    #                                   projection=dict(type=['equirectangular', 'orthographic'][projection]
    #                                                   ),
    #                                   # showland=True,   # default = True
    #                                   landcolor='black',
    #                                   lakecolor='white',
    #                                   showocean=True,  # default = False
    #                                   oceancolor='azure',
    #                                   bgcolor='#f9f9f9'
    #                                   ),
    #
    #                          title=dict(
    #                              text='World ' + str(gas.replace('_', ' ')) + ' Choropleth Map on the year ' + str(
    #                                  year),
    #                              x=.5  # Title relative position according to the xaxis, range (0,1)
    #
    #                          ),
    #                          paper_bgcolor='#f9f9f9'
    #                          )
    #
    # ############################################Third Scatter Plot######################################################
    #
    # df_loc = df.loc[df['country_name'].isin(countries)].groupby('year').sum().reset_index()
    #
    # data_agg = []
    #
    # for place in sector:
    #     data_agg.append(dict(type='scatter',
    #                          x=df_loc['year'].unique(),
    #                          y=df_loc[place],
    #                          name=place.replace('_', ' '),
    #                          mode='markers'
    #                          )
    #                     )
    #
    # layout_agg = dict(title=dict(text='Aggregate CO2 Emissions by Sector'),
    #                   yaxis=dict(title=['CO2 Emissions', 'CO2 Emissions (log scaled)'][scale],
    #                              type=['linear', 'log'][scale]),
    #                   xaxis=dict(title='Year'),
    #                   paper_bgcolor='#f9f9f9'
    #                   )
    #
    return go.Figure(data=data_bar, layout=layout_bar)
    #        go.Figure(data=data_choropleth, layout=layout_choropleth), \
    #        go.Figure(data=data_agg, layout=layout_agg)


# SECOND APP CALLBACK --> FOR THE LABELS
# @app.callback(
#     [
#         Output("gas_1", "children"),
#         Output("gas_2", "children"),
#         Output("gas_3", "children"),
#         Output("gas_4", "children"),
#         Output("gas_5", "children")
#     ],
#     [
#         Input("country_drop", "value"),
#         Input("year_slider", "value"),
#     ]
# )
# def indicator(countries, year):
#     df_loc = df.loc[df['country_name'].isin(countries)].groupby('year').sum().reset_index()
#
#     value_1 = round(df_loc.loc[df_loc['year'] == year][gas_names[0]].values[0], 2)
#     value_2 = round(df_loc.loc[df_loc['year'] == year][gas_names[1]].values[0], 2)
#     value_3 = round(df_loc.loc[df_loc['year'] == year][gas_names[2]].values[0], 2)
#     value_4 = round(df_loc.loc[df_loc['year'] == year][gas_names[3]].values[0], 2)
#     value_5 = round(df_loc.loc[df_loc['year'] == year][gas_names[4]].values[0], 2)
#
#     return str(gas_names[0]).replace('_', ' ') + ': ' + str(value_1), \
#            str(gas_names[1]).replace('_', ' ') + ': ' + str(value_2), \
#            str(gas_names[2]).replace('_', ' ') + ': ' + str(value_3), \
#            str(gas_names[3]).replace('_', ' ') + ': ' + str(value_4), \
#            str(gas_names[4]).replace('_', ' ') + ': ' + str(value_5),
#

if __name__ == '__main__':
    app.run_server(debug=True)
