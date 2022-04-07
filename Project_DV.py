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

# path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'

df = pd.read_csv(
    "C:/Users/tsoom/OneDrive/Documentos/IMS - Data Science/2º Semester/Data Visualization/Github/CSVs/types_of_conflicts.csv")

df.drop(columns=['Code'], inplace=True)

df.rename(columns={'Entity': 'world_region',
                   'Year': 'year',
                   'Number of civil conflicts with foreign state intervention': 'civil-foreign conflicts',
                   'Number of civil conflicts': 'civil conflicts',
                   'Number of conflicts between states': 'between states conflicts',
                   'Number of colonial or imperial conflicts': 'colonial/imperial conflicts'}, inplace=True)

df['world_region'] = df['world_region'].astype('string')

df['total number of conflicts'] = df['civil-foreign conflicts'] + df['civil conflicts'] + df[
    'between states conflicts'] + df['colonial/imperial conflicts']

###############################################
df1 = df.drop(['civil-foreign conflicts', 'civil conflicts', 'between states conflicts', 'colonial/imperial conflicts'],
              axis=1)
df1.set_index('world_region', inplace=True)
df1 = pd.pivot_table(df1, values='total number of conflicts', index='world_region', columns='year')
df1.drop('World', axis=0, inplace=True)
colors = ['#B6E880', '#FF97FF', '#FECB52', '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692']

#############################################33
df2 = df.loc[df['world_region'] != 'World']
df2 = df2.loc[df['year'] > 2000]  # !!!!!!!!

######################################################  Interactive Components  ############################################

world_regions = [dict(label=region, value=region) for region in df2['world_region'].unique()]
# print(world_regions)

list_of_conflicts = ['civil-foreign conflicts', 'civil conflicts', 'between states conflicts',
                     'colonial/imperial conflicts']
types_of_conflicts = [dict(label=conflict, value=conflict) for conflict in list_of_conflicts]

# deaths_col = 'Deaths in all state-based conflict types'
# years = [dict(label=year, value=year) for year in df['Year'].unique()]

dropdown_world_regions = dcc.Dropdown(
    id='world_regions_drop',
    options=world_regions,
    value=['Europe', 'Africa', 'Americas'],  # , 'Africa', 'Americas'],
    multi=True  # Start with multiple = True
)

dropdown_types_of_conflicts = dcc.Dropdown(
    id='types_of_conflicts_drop',
    options=types_of_conflicts,
    value=['civil conflicts'],
    multi=False  # Start with multiple = False
)

range_slider = dcc.RangeSlider(  # create a slider for the years
    id='year_slider',
    min=1950,
    max=2020,
    value=[1960, 2010],
    marks={'1950': 'Year 1950',
           '1960': 'Year 1960',
           '1970': 'Year 1970',
           '1980': 'Year 1980',
           '1990': 'Year 1990',
           '2000': 'Year 2000',
           '2010': 'Year 2010',
           '2020': 'Year 2020'},
    step=1
)
# slider_year = dcc.Slider(
#     id='year_slider',
#     min=df2['year'].min(),
#     max=df2['year'].max(),
#     # marks={str(i): '{}'.format(str(i)) for i in
#     #        [1990, 1995, 2000, 2005, 2010, 2014]},
#     value=df2['year'].min(),
#     step=1
# )

##################################################   APP   ###################################################################

app = dash.Dash(__name__)

server = app.server

# !!!!!!!!!!!!!!   LAYOUT   !!!!!!!!!!!!!!
app.layout = html.Div([

    html.Div([  # title !!
        html.H1('Deaths in state-based conflicts'),
    ], className="box_pretty"),

    html.Div([  # gráfico de linhas (esquerda) e gráfico de barras (direita)
        html.Div([
            html.Div([
                html.Label('Country Choice'),
                dropdown_world_regions,  ##############
            ], style={'width': '85%', 'padding-left': '40px'}),
            dcc.Graph(id='line_chart', className="box_pretty"),
            html.Div([
                range_slider,
            ], style={'width': '80%', 'padding-left': '50px'})
        ], style={'width': '60%'}),

        html.Div([
            html.Div([
                html.Label('Type of Conflict Choice'),
                dropdown_types_of_conflicts,  ##############
            ], style={'width': '60%', 'padding-left': '40px'}),
            dcc.Graph(id='bar_chart', className="box_pretty"),  # <-----------------
            # html.Label('Year Slider'),
            # slider_year,  ##############
        ], style={'width': '40%'}),

    ], style={'display': 'flex', "height": '600px'}),

])


###################################   Callbacks   ##########################################
@app.callback(
    [
        Output("line_chart", "figure"),
        Output("bar_chart", "figure"),
    ],
    [
        # Input("year_slider", "value"),
        Input("world_regions_drop", "value"),
        Input("year_slider", "value"),
        Input('types_of_conflicts_drop', 'value')
    ]
)
# first the inputs, then the states, by order
def plots(region, years, conflict):

    ########################################################################################
    # First: Line Chart
    filter_df = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]
    filter_df = filter_df.loc[filter_df['world_region'] != 'World']

    df_line_graph = filter_df[['world_region', 'year', 'total number of conflicts']].set_index('world_region')
    df_line_graph = pd.pivot_table(df_line_graph, values='total number of conflicts', index='world_region',
                                   columns='year')

    data_scatter = []

    for i, world_region in enumerate(region):
        data_scatter.append(dict(type='scatter',
                                 x=df_line_graph.columns,
                                 y=df_line_graph.loc[world_region],
                                 name=world_region,
                                 line=dict(color=colors[i]),
                                 showlegend=True
                                 )
                            )

    layout_scatter = dict(title=dict(text='Conflicts over the years', x=0.5),
                          xaxis=dict(title='Years'),
                          yaxis=dict(title='Total Number of Conflicts'))

    ########################################################################################
    # Second: Bar Charts
    conflicts_string = "".join(conflict)
    conflict_df = pd.pivot_table(filter_df[['world_region', 'year', conflicts_string]],
                                 values=conflicts_string, index=['world_region'], columns=['year'])

    fig_bar_data = []
    # Each year defines a new hidden (implies visible=False) trace in our visualization
    for year in conflict_df.columns:  # year is an integer number
        fig_bar_data.append(dict(data=dict(type='bar',
                                           x=conflict_df.index,  # world regions
                                           y=conflict_df[year],  # values for that year
                                           name=year,
                                           ),
                                 # marker=dict(color='red'),
                                 # showlegend=False,
                                 # visible=False
                                 layout=go.Layout(title_text=f'Number of {conflicts_string} in {str(year)}')
                                 ))

    fig_bar_layout = dict(title=dict(text=f'Total Number of {conflicts_string} between {str(years[0])} and {str(years[1])}'),
                          yaxis=dict(title='Number of Conflicts', range=[0, 10]),
                          # PLAT BUTTON TO SEE CHANGES THROUGHOUT THE YEARS
                          updatemenus=[dict(type="buttons",
                                            buttons=[dict(label="Play",
                                                          method="animate",
                                                          args=[None])
                                            ])]
                          )

    initial_data = dict(type='bar',
                        x=conflict_df.index,
                        y=conflict_df[2000],
                        # name=str(1990)
                        )

    return go.Figure(data=data_scatter, layout=layout_scatter), \
           go.Figure(data=initial_data, layout=fig_bar_layout, frames=fig_bar_data)


    # # An empty graph object
    # df_aux = df2.loc[df2['world_region'] == region]
    # pivot_table = pd.pivot_table(df_aux[['world_region', 'year', conflict]],
    #                              values=conflict, index=['world_region'], columns=['year'])
    #
    # fig_bar = go.Figure()
    #
    # # Each year defines a new hidden (implies visible=False) trace in our visualization
    # for year in pivot_table.columns:
    #     fig_bar.add_trace(dict(type='bar',
    #                            x=civil_foreign_1.index,  # world regions
    #                            y=civil_foreign_1[year],  # values for that year
    #                            name='civil_foreign conflicts',
    #                            marker=dict(color='red'),
    #                            showlegend=False,
    #                            visible=False
    #                            )
    #
    #                       )
    # #     # civil_2
    # #     fig_bar.add_trace(dict(type='bar',
    # #                  x=civil_2.index,
    # #                  y=civil_2[year],
    # #                  name='civil conflicts',
    # #                  marker=dict(color='black'),
    # #                  showlegend=False,
    # #                  visible=False
    # #                 )
    # #            )
    #
    # # First seen trace
    # fig_bar.data[0].visible = True
    #
    # data_bar = []
    # for region in world_regions:
    #     df_bar = df.loc[(df['Entity'] == region)]
    #
    #     x_bar = df_bar['Year']
    #     y_bar = df_bar[deaths_col]
    #
    #     data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=region))
    #
    # layout_bar = dict(title=dict(text='Deaths in all state-based conflict types'),
    #                   yaxis=dict(title='Deaths'),
    #                   paper_bgcolor='#f9f9f9'
    #                   )

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
    # return go.Figure(data=data_bar, layout=layout_bar)
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
