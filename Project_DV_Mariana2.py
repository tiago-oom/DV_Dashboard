import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# FOR THE PROJECT: ALSO CHECK BOOTSTRAP COMPONENTS !!!

# https://htmlcheatsheet.com/css/ --> get new css classes

#########################################
# Dataset types of conflicts
df_conflicts = pd.read_csv(  # Change this to the path of your computer
    r"C:\Users\Administrador\OneDrive - NOVAIMS\Mestrado\Data Visualization\Project\CSVs\types_of_conflicts.csv")

df_conflicts.drop(columns=['Code'], inplace=True)  # drop the column 'Code' --> not necessary for our analysis

df_conflicts.rename(columns={'Entity': 'world_region',
                             'Year': 'year',
                             'Number of civil conflicts with foreign state intervention': 'civil-foreign conflicts',
                             'Number of civil conflicts': 'civil conflicts',
                             'Number of conflicts between states': 'between states conflicts',
                             'Number of colonial or imperial conflicts': 'colonial/imperial conflicts'}, inplace=True)

df_conflicts['world_region'] = df_conflicts['world_region'].astype('string')

df_conflicts['total number of conflicts'] = df_conflicts['civil-foreign conflicts'] + df_conflicts['civil conflicts'] + \
                                            df_conflicts['between states conflicts'] + df_conflicts[
                                                'colonial/imperial conflicts']

colors = ['#B6E880', '#FF97FF', '#FECB52', '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692']

#############################################
# Dataset for bar chart
# df_conflicts2 = df_conflicts.loc[df_conflicts['world_region'] != 'World']
# df_conflicts2 = df_conflicts.loc[df_conflicts['year'] > 2000]  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#############################################
# Dataset for world deaths
df_deaths = pd.read_csv(
    r"C:\Users\Administrador\OneDrive - NOVAIMS\Mestrado\Data Visualization\Project\CSVs\deaths-from-conflict-and-terrorism.csv")
df_deaths.drop(columns=['Code'], inplace=True)
df_deaths.rename(columns={'Entity': 'Country',
                          'Year': 'year',
                          'Deaths - Conflict and terrorism - Sex: Both - Age: All Ages (Number)': 'Total Deaths'},
                 inplace=True)

df_deaths['Country'] = df_deaths['Country'].astype('string')

regions = ['World', 'Eastern Mediterranean Region', 'North Africa and Middle East', 'Low SDI', 'Middle East & North Africa',
           'Eastern Mediterranean Region', 'World Bank Lower Middle Income', 'Middle SDI', 'South Asia - World Bank region',
           'African Union', 'Sub-Saharan Africa - World Bank region', 'Europe & Central Asia - World Bank region',
           'European Region', 'Low-middle SDI', 'World Bank Low Income', 'High-income Asia Pacific', 'African Region',
           'World Bank High Income', 'World Bank Upper Middle Income', 'Western Pacific Region', 'Western sub-Saharan Africa',
           'Western Europe', 'South-East Asia Region', 'Commonwealth Middle Income', 'Commonwealth', 'High-middle SDI',
           'Southeast Asia, East Asia, and Oceania', 'Southeast Asia', 'Eastern sub-Saharan Africa', 'G20', 'Europe',
           'Africa', 'Asia', 'Central Europe, Eastern Europe, and Central Asia', 'Central Europe', 'Region of the Americas',
           'Central Asia', 'Central sub-Saharan Africa', 'OECD Countries', 'Commonwealth Low Income', 'Eastern Europe',
           'High-income', 'America', 'Latin America & Caribbean - World Bank region', 'East Asia & Pacific - World Bank region',
           'High SDI', 'High-income North America', 'North America']

deaths = df_deaths[~df_deaths.Country.isin(regions)]

deaths_df = pd.pivot_table(deaths, values = 'Total Deaths', index = 'Country', columns = 'year')


#######################################
# Interactive Components
drop_regions = df_conflicts.loc[df_conflicts['world_region'] != 'World']
world_regions = [dict(label=region, value=region) for region in drop_regions['world_region'].unique()]
# print(world_regions)

list_of_conflicts = ['civil-foreign conflicts', 'civil conflicts', 'between states conflicts',
                     'colonial/imperial conflicts']
types_of_conflicts = [dict(label=conflict, value=conflict) for conflict in list_of_conflicts]

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
    id='range_slider',
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

radio_lin_log = dcc.RadioItems(
    id='lin_log',
    options=[dict(label='Linear', value=0), dict(label='log', value=1)],
    value=0
)

radio_projection = dcc.RadioItems(
    id='projection',
    options=[dict(label='Equirectangular', value=0),
             dict(label='Orthographic', value=1)],
    value=0
)

normal_slider = dcc.Slider(
    id='normal_slider',
    min=df_deaths['year'].min(),
    max=df_deaths['year'].max(),
    marks={str(i): '{}'.format(str(i)) for i in
           [1990, 1995, 2000, 2005, 2010, 2014]},
    value=df_deaths['year'].min(),
    step=1
)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# slider_map = daq.Slider(
#         id = 'slider_map',
#         handleLabel={"showCurrentValue": True,"label": "Year"},
#         marks = {str(i):str(i) for i in [1990,1995,2000,2005,2010,2015]},
#         min = 1990,
#         size=450,
#         color='#4B9072'
#     )

##################################################
# APP
app = dash.Dash(__name__)

server = app.server

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  LAYOUT   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
app.layout = html.Div([

    html.Div([  # left bar with title, text. image, and references (fixed)
        html.H1('WAR AND PEACE'),
        html.Br(),
        html.Label('Text......................'),
        html.Br(),
        # html.Img()
        html.Br(),
        html.Label('Work done by......................'),

    ], className='side_bar'),

    html.Div([  # right part of the dashboard, with all the visualizations and filters

        # Divide horizontally in 5 parts
        ##############################################################
        html.Div([  # create a box in the assets, for the filters !!
            html.Div([  # first part --> dropdown menus (10%)

                html.Div([  # Instructions for the filters
                    html.Br(),
                    html.Label('Choose the world regions you want to examine and also the type of conflict'),
                ], style={'width': '250px', 'padding-left': '20px'}),

                html.Div([  # dropdown Country Choice
                    html.Br(),
                    html.Label('World Region Choice'),
                    dropdown_world_regions,
                ], style={'width': '45%', 'padding-left': '20px'}),

                html.Div([  # dropdown type of conflict
                    html.Br(),
                    html.Label('Type of Conflict Choice'),
                    dropdown_types_of_conflicts,
                ], style={'width': '20%', 'padding-left': '20px'}),

            ], style={'display': 'flex', 'height': '10%', 'padding-left': '200px'}),

            ##############################################################
            html.Div([  # second part --> range slider (10%)
                html.Br(),
                html.Br(),
                range_slider,
            ], style={'height': '10%', 'width': '75%', 'padding-left': '250px'}),  # , 'padding-bottom': '10px'}),

        ]),  # className='box'),

        ####################################################################
        html.Div([  # third part --> line chart and bar chart

            html.Div([  # line chart on the left
                html.Br(),
                html.Br(),
                dcc.Graph(id='line_chart', className="box"),
            ], style={'width': '55%'}),

            html.Div([  # line chart on the left
                html.Br(),
                html.Br(),
                dcc.Graph(id='bar_chart', className="box"),
            ], style={'width': '45%'}),

        ], style={'display': 'flex', 'height': '40%', 'padding-left': '195px'}),


        ####################################################################
        html.Div([  # fourth part --> world map and top_countries graph

            html.Div([  # map on the left
                radio_projection,
                dcc.Graph(id='world_map'),
            ], className="box", style={'width': '65%', 'padding-left': '20px'}),

           html.Div([  # line chart on the left
               dcc.Graph(id='top_countries_graph', className="box"),
           ], style={'width': '35%'}),

        ], style={'display': 'flex', 'height': '35%', 'padding-left': '195px'}),

        ####################################################################
        html.Div([  # fifth part --> normal slider (10%)
            html.Br(),
            html.Br(),
            normal_slider,
        ], style={'height': '10%', 'width': '90%', 'padding-left': '250px'}),  # , 'padding-bottom': '10px'}),

    ], style={'display': 'inline-block', 'height': '65%', 'width': '95%', 'padding-left': '50px'}),
])


##############################
# First Callback
@app.callback(
    [
        Output("line_chart", "figure"),
        Output("bar_chart", "figure"),
    ],
    [
        Input("world_regions_drop", "value"),
        Input("range_slider", "value"),
        Input('types_of_conflicts_drop', 'value')
    ]
)
# first the inputs, then the states, by order
def plots(region, years, conflict):
    ########################################################################################
    # Filter the dataset based on the range slider
    filter_df = df_conflicts[(df_conflicts['year'] >= years[0]) & (df_conflicts['year'] <= years[1])]
    filter_df = filter_df.loc[filter_df['world_region'] != 'World']

    ########################################################################################
    # First Visualization: Line Chart
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
                                 # font-size='10px', ????????
                                 )
                            )

    layout_scatter = dict(title=dict(text='Total number of conflicts over the years', x=0.5),
                          xaxis=dict(title='Years'),
                          yaxis=dict(title='Total Number of Conflicts'))

    ########################################################################################
    # Second Visualization: Bar Charts
    conflicts_string = "".join(conflict)
    df_bar_graph = filter_df.loc[filter_df['world_region'].isin(region)]
    df_bar_graph = pd.pivot_table(df_bar_graph[['world_region', 'year', conflicts_string]],
                                  values=conflicts_string, index=['world_region'], columns=['year'])

    fig_bar_data = []
    # Each year defines a new hidden (implies visible=False) trace in our visualization
    for year in df_bar_graph.columns:  # year is an integer number
        fig_bar_data.append(dict(data=dict(type='bar',
                                           x=df_bar_graph.index,  # world regions
                                           y=df_bar_graph[year],  # values for that year
                                           name=year,
                                           marker=dict(color='orange'),
                                           showlegend=False
                                           ),
                                 # visible=False,
                                 layout=go.Layout(dict(title_text=f'Number of {conflicts_string} in {str(year)}'))
                                 ))

    fig_bar_layout = dict(
        title=dict(text=f'Total Number of {conflicts_string} between {str(years[0])} and {str(years[1])}'),
        yaxis=dict(title='Number of Conflicts', range=[0, 10]),  # change the range !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # PLAT BUTTON TO SEE CHANGES THROUGHOUT THE YEARS
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None]),
                                   dict(label='Pause',
                                        method="animate",
                                        args=[[None], dict(frame=dict(duration=0, redraw=False),
                                                           # pause button to stop and continue !!!!!!!
                                                           mode="immediate",
                                                           transition=dict(duration=0))])
                                   ],
                          direction='left',  # put both of the buttons side by side
                          x=0.6,  # change position of the buttons
                          y=-0.1)])

    initial_data = dict(type='bar',
                        x=df_bar_graph.index,
                        y=df_bar_graph[2000],  # put the initial data as the year[0] of the range slider
                        marker=dict(color='orange')
                        # name=str(1990)
                        )

    return go.Figure(data=data_scatter, layout=layout_scatter), \
           go.Figure(data=initial_data, layout=fig_bar_layout, frames=fig_bar_data)


#######################################
# Second Callback
@app.callback(
    # [
        Output("world_map", "figure"),
        Output("top_countries_graph", "figure"),
    # ],
    [
        Input("projection", "value"),
        Input('normal_slider', 'value')
    ]
)
# first the inputs, then the states, by order
def plots(projection, year):
    #######################################################################################
    # Third Visualization: World Map
    filter_df2 = df_deaths[(df_deaths['year'] <= year)]
    filter_df2 = filter_df2.groupby('Country').sum()[['Total Deaths']]

    data_choropleth = dict(type='choropleth',
                           locations=filter_df2.index,
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=np.log(filter_df2['Total Deaths']),
                           text=filter_df2.index,
                           colorscale='inferno'
                           )

    layout_choropleth = dict(geo=dict(scope='world',  # default
                                      projection=dict(type=['equirectangular', 'orthographic'][projection]),
                                      # showland=True,   # default = True
                                      landcolor='black',
                                      lakecolor='white',
                                      showocean=True,  # default = False
                                      oceancolor='azure'
                                      ),

                             title=dict(text='Total deaths by conflicts or terrorism',
                                        x=.5  # Title relative position according to the xaxis, range (0,1)
                                        )
                             )
    #######################################################################################
    # Fourth Visualization: Bar Chart 2
    fig_bar_data2 = []

    # Each year defines a new hidden (implies visible=False) trace in our visualization
    for year in deaths_df.columns:  # year is an integer number
        fig_bar_data2.append(dict(data=dict(type='bar',
                                           x=deaths_df.sort_values(by=year, ascending=False).iloc[:5, :].index,
                                           # countries
                                           y=deaths_df.sort_values(by=year, ascending=False).iloc[:5, :][year],
                                           # values for that year
                                           name=year,
                                           marker=dict(color='#9F9F5F'),
                                           showlegend=False
                                           ),
                                 # visible=False,
                                 layout=go.Layout(
                                     dict(title_text=f'Countries with the highest number of deaths in {str(year)}'))
                                 ))

    fig_bar_layout2 = dict(
        title=dict(text=f'Countries with the highest number of deaths'),
        yaxis=dict(title='Number of Deaths', range=[0, 200000]),  # change the range !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    )

    initial_data2 = dict(type='bar',
                        x=deaths_df.sort_values(by=year, ascending=False).iloc[:5, :].index,
                        y=deaths_df.sort_values(by=year, ascending=False).iloc[:5, :][2000],
                        marker=dict(color='orange'),
                        name=str(1990)
                        )

    return go.Figure(data=data_choropleth, layout=layout_choropleth), \
           go.Figure(data=initial_data2, layout=fig_bar_layout2, frames=fig_bar_data2)


############################################################
if __name__ == '__main__':
    app.run_server(debug=True)
