import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# FOR THE PROJECT: ALSO CHECK BOOTSTRAP COMPONENTS !!!

# https://htmlcheatsheet.com/css/ --> get new css classes

#########################################
# Dataset types of conflicts
df_conflicts = pd.read_csv(  # Change this to the path of your computer
    r"https://raw.githubusercontent.com/marianagferreira/WorldWideConclictsPostWWII/master/CSVs/types_of_conflicts.csv")

df_conflicts.drop(columns=['Code'], inplace=True)  # drop the column 'Code' --> not necessary for our analysis

df_conflicts.rename(columns={'Entity': 'world_region',
                             'Year': 'year',
                             'Number of civil conflicts with foreign state intervention': 'Civil-foreign Conflicts',
                             'Number of civil conflicts': 'Civil Conflicts',
                             'Number of conflicts between states': 'Between States Conflicts',
                             'Number of colonial or imperial conflicts': 'Colonial/Imperial Conflicts'}, inplace=True)

df_conflicts['world_region'] = df_conflicts['world_region'].astype('string')

df_conflicts['total number of conflicts'] = df_conflicts['Civil-foreign Conflicts'] + df_conflicts['Civil Conflicts'] + \
                                            df_conflicts['Between States Conflicts'] + df_conflicts[
                                                'Colonial/Imperial Conflicts']

#############################################
# Dataset for world deaths
df_deaths = pd.read_csv(
    r"https://raw.githubusercontent.com/marianagferreira/WorldWideConclictsPostWWII/master/CSVs/deaths-from-conflict-and-terrorism.csv")
df_deaths.drop(columns=['Code'], inplace=True)
df_deaths.rename(columns={'Entity': 'Country',
                          'Year': 'year',
                          'Deaths - Conflict and terrorism - Sex: Both - Age: All Ages (Number)': 'Total Deaths'},
                 inplace=True)

df_deaths['Country'] = df_deaths['Country'].astype('string')

regions = ['World', 'Eastern Mediterranean Region', 'North Africa and Middle East', 'Low SDI',
           'Middle East & North Africa',
           'Eastern Mediterranean Region', 'World Bank Lower Middle Income', 'Middle SDI',
           'South Asia - World Bank region',
           'African Union', 'Sub-Saharan Africa - World Bank region', 'Europe & Central Asia - World Bank region',
           'European Region', 'Low-middle SDI', 'World Bank Low Income', 'High-income Asia Pacific', 'African Region',
           'World Bank High Income', 'World Bank Upper Middle Income', 'Western Pacific Region',
           'Western sub-Saharan Africa',
           'Western Europe', 'South-East Asia Region', 'Commonwealth Middle Income', 'Commonwealth', 'High-middle SDI',
           'Southeast Asia, East Asia, and Oceania', 'Southeast Asia', 'Eastern sub-Saharan Africa', 'G20', 'Europe',
           'Africa', 'Asia', 'Central Europe, Eastern Europe, and Central Asia', 'Central Europe',
           'Region of the Americas',
           'Central Asia', 'Central sub-Saharan Africa', 'OECD Countries', 'Commonwealth Low Income', 'Eastern Europe',
           'High-income', 'America', 'Latin America & Caribbean - World Bank region',
           'East Asia & Pacific - World Bank region',
           'High SDI', 'High-income North America', 'North America']

df_deaths = df_deaths[~df_deaths.Country.isin(regions)]
df_deaths.replace("Democratic Republic of Congo", "DR of Congo", inplace=True)
df_deaths.replace("Bosnia and Herzegovina", "Bosnia and Herz", inplace=True)

cards_data = pd.read_csv(
    r"https://raw.githubusercontent.com/marianagferreira/WorldWideConclictsPostWWII/master/CSVs/deaths-from-conflict-and-terrorism.csv")
cards_data.drop(columns=['Code'], inplace=True)
cards_data.rename(columns={'Entity': 'Country',
                          'Year': 'year',
                          'Deaths - Conflict and terrorism - Sex: Both - Age: All Ages (Number)': 'Total Deaths'},
                 inplace=True)

cards_data['Country'] = cards_data['Country'].astype('string')
cards_data = cards_data[cards_data['Country'] == 'World']

#######################################
colors = ['#B6E880', '#FF97FF', '#FECB52', '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692']

#######################################
# Interactive Components
drop_regions = df_conflicts.loc[df_conflicts['world_region'] != 'World']
world_regions = [dict(label=region, value=region) for region in drop_regions['world_region'].unique()]
# print(world_regions)

list_of_conflicts = ['Civil-foreign Conflicts', 'Civil Conflicts', 'Between States Conflicts',
                     'Colonial/Imperial Conflicts']
types_of_conflicts = [dict(label=conflict, value=conflict) for conflict in list_of_conflicts]

dropdown_world_regions = dcc.Dropdown(
    id='world_regions_drop',
    options=world_regions,
    value=['Europe', 'Africa', 'Americas', 'Middle East'],
    multi=True,  # Start with multiple = True
    clearable=False,
    searchable=False,
    style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#9F9F5F'}
)

dropdown_types_of_conflicts = dcc.Dropdown(
    id='types_of_conflicts_drop',
    options=types_of_conflicts,
    value='Civil Conflicts',
    multi=False,  # Start with multiple = False
    clearable = False,
    searchable = False,
    style = {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#9F9F5F'}
)

range_slider = dcc.RangeSlider(  # create a slider for the years
    id='range_slider',
    min=1950,
    max=2020,
    value=[1990, 2020],
    marks={'1950': 'Year 1950',
           '1960': 'Year 1960',
           '1970': 'Year 1970',
           '1980': 'Year 1980',
           '1990': 'Year 1990',
           '2000': 'Year 2000',
           '2010': 'Year 2010',
           '2020': 'Year 2020'},
    tooltip={"placement": "bottom", "always_visible": False},
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
           [1990, 1995, 2000, 2005, 2010, 2015, 2019]},
    value=2000,
    tooltip={"placement": "bottom", "always_visible": False},
    step=1,
    included=False
)

##################################################
# APP
app = dash.Dash(__name__)

server = app.server

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  LAYOUT   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
app.layout = html.Div([

    html.Div([  # left bar with title, text. image, and references (fixed)
        html.Div([
            html.H1('WORLDWIDE CONFLICTS POST WWII'),
        ], style={'font-size': '14px'}),
        html.Br(),
        html.Br(),
        html.Div([
            html.Label('Since World War II, the number of large-scale conflicts has drastically reduced globally. Nevertheless, \
                 to these days there have still been several occasions were nations clashed into war and the lives of millions \
                  were affected. Through this visual representation, we intend to take a deeper dive into these events and \
                  understand their repercussions.'),
        ], style={'text-align': 'justify', 'font-size':'17px', 'padding-left':'3%', 'padding-right':'4%' }),
        html.Br(),
        html.Div([
            html.Label('_______'),
        ], style={'text-align': 'center', 'font-family': 'Brush Script MT', 'font-size': '30px', 'color':'#F5F5DC'}),
        html.Br(),
        html.Br(),
        html.Div([
            html.Label('"War does not determine who is right - only who is left."'),
        ], style={'text-align': 'center', 'font-family': 'Brush Script MT', 'font-size': '30px'}),
        html.Br(),
        html.Div([
            html.Label('Bertrand Russell'),
        ], style={'text-align': 'center', 'font-family': 'Brush Script MT', 'font-size': '20px'}),
        html.Br(),
        # html.Img(src=app.get_asset_url('war_soldier.jpg')),
        html.Br(),

    ], className='side_bar'),

    html.Div([  # right part of the dashboard, with all the visualizations and filters

        # Divide horizontally in 5 parts
        ##############################################################
        html.Div([  # create a box in the assets, for the filters !!
            html.Div([  # first part --> dropdown menus (10%)

                html.Div([  # Instructions for the filters
                    html.Br(),
                    html.Label(
                        'Choose the world regions and the type of conflict you want to examine, as well as the range of years (1950 - 2020)'
                    ),
                ], style={'width': '240px', 'padding-left': '15px'}, className='text'),

                html.Div([  # dropdown Country Choice
                    html.Br(),
                    html.Div([
                        html.Label('World Region Choice'),
                    ], style={'font-weight': 'bold', 'padding-bottom': '5px'}),
                    dropdown_world_regions,
                ], style={'width': '53%'}, className='dash-dropdown'),

                html.Div([  # dropdown type of conflict
                    html.Br(),
                    html.Div([
                        html.Label('Type of Conflict Choice'),
                    ], style={'font-weight': 'bold', 'padding-bottom': '5px'}),
                    dropdown_types_of_conflicts,
                ], style={'width': '20%', 'padding-right': '10px'}, className='dash-dropdown'),

            ], style={'display': 'flex', 'height': '7%'}),

            ##############################################################
            html.Div([  # second part --> range slider (10%)
                range_slider,
            ], style={'font-weight': 'bold', 'height': '4%', 'width': '85%', 'padding-left': '90px'},
                className='year_slider'),

        ], style={'height': '5%', 'width': '92%'}, className='box_filters'),

        ####################################################################
        html.Div([  # third part --> line chart and bar chart

            html.Div([  # line chart on the left
                html.Div([
                    html.Div([
                        html.Label(id='title_line_chart'),
                    ], style={'padding-bottom': '5px', 'font-weight':'bold'}),
                    html.Div([
                        html.Label(id='title_line_chart2'),
                    ], style={'padding-bottom': '5px'}),
                    html.Div([
                        dcc.Graph(id='line_chart', config={'displayModeBar': False}),
                    ], style={'height': '65%'}),
                ], className="box")
            ], style={'width': '67%'}),

            html.Div([  # bar chart on the right
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label(id='title_bar_chart1'),
                        ], style={'padding-bottom': '5px', 'font-weight':'bold' }),
                        html.Div([
                            html.Label(id='title_bar_chart2'),
                        ], style={'padding-bottom': '5px'}),
                    ], style={'display': 'block', 'text-align': 'center', 'padding': '1px'}),
                    dcc.Graph(id='bar_chart', config={'displayModeBar': False}),
                ], className="box")
            ], style={'width': '35%'}),

        ], style={'display': 'flex', 'width' : '92%', 'padding-left':'6%'}),

        ####################################################################
        # Label dividing both of the visualizations
        html.Div([
            html.Label('In this second section, it is presented the worst variable that war brings: deaths. Here we can analyse \
             the evolution of deaths due to conflicts over the globe according to two different layouts, as well as the countries \
            with higher values in the range of years selected below.'),
        ], style = {'width':'90%', 'font-size':'14px'}, className='text_comments'),

        ####################################################################
        html.Div([  # fourth part --> world map and top_countries graph

            html.Div([  # map on the left

                html.Div([  # fifth part --> normal slider (10%)
                    html.Label(id = 'title_map'),
                ], style={'text-align': 'center', 'padding-bottom': '7px', 'font-weight':'bold'}),
                html.Div([
                    radio_projection,
                ], style={'text-align': 'center', 'padding-bottom': '7px'}),
                dcc.Graph(id='world_map', config={'displayModeBar': False}),
                html.Br(),
                html.Div([  # fifth part --> normal slider (10%)
                    normal_slider,
                ], style={'width': '95%', 'padding-left': '35px', 'font-weight':'bold'}, className='year_slider2'),
            ], className="box", style={'width': '55%', 'height':'30%'}),

            html.Div([
                html.Div([    # CARD
                    html.Div([
                        html.Label(id='title_card'),
                    ], style={'font-weight': 'bold'}),
                    html.Div([
                        html.Label(id='card'),
                    ], style={'font-size': '29px'}),
                ], style={'height': '50%', 'padding-bottom':'7px', 'padding-top':'7px' }, className='box'),

                html.Div([  # top_countries on the right

                    html.Div([
                        html.Label(id='title_top_countries'),
                    ], style={'padding-bottom': '5px', 'font-weight':'bold'}),
                    dcc.Graph(id='top_countries_graph', config={'displayModeBar': False}),
                ], style={'height': '10%'}, className='box'),
            ], style={'display': 'inline-block', 'height':'50%', 'width':'41%'}),

        ], style={'display': 'flex', 'height': '40%', 'padding-left': '6%'}),

        ####################################################################
        html.Div([
            html.Div([  # last part --> references and authors
                html.Br(),
                html.Label('Group members: Lucas Lopes, Mariana Ferreira and Tiago Sousa'),
            ], style={'display': 'flex', 'padding-left': '400px', 'width': '60%', 'text-align': 'center'}),

            html.Div([  # last part --> references and authors
                html.Br(),
                html.Label('Source: https://ourworldindata.org/war-and-peace')
            ], style={'display': 'flex', 'padding-left': '425px', 'width': '30%', 'text-align': 'center'}),

        ], className='text_comments'),

    ], style={'display': 'inline-block', 'height': '65%', 'width': '86%'}, className='main'),

])


##############################
# First Callback
@app.callback(
    [
        Output('title_line_chart', 'children'),
        Output('title_line_chart2', 'children'),
        Output("line_chart", "figure"),
        Output('title_bar_chart1', 'children'),
        Output('title_bar_chart2', 'children'),
        Output("bar_chart", "figure"),
    ],
    [
        Input("world_regions_drop", "value"),
        Input('types_of_conflicts_drop', 'value'),
        Input("range_slider", "value"),
    ]
)
# first the inputs, then the states, by order
def plots(region, conflict, years):
    ########################################################################################
    # Filter the dataset based on the range slider
    filter_df = df_conflicts[(df_conflicts['year'] >= years[0]) & (df_conflicts['year'] <= years[1])]
    filter_df = filter_df.loc[filter_df['world_region'] != 'World']

    ########################################################################################
    # First Visualization: Line Chart
    title_line = 'Total number of conflicts over the years'
    title_line2 = f'({str(years[0])}-{str(years[1])})'


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

    layout_line = dict(plot_bgcolor='#F5F5DC',
                       margin=dict(l=15, r=35, t=35, b=35),
                       xaxis=dict(title='Years'),
                       yaxis=dict(title='Total Number of Conflicts', gridwidth=0.2),
                       hovermode='x',  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       )

    ########################################################################################
    # Second Visualization: Bar Charts
    title_bar1 = f'Number of {conflict} '
    title_bar2 = f'({str(years[0])}-{str(years[1])})'

    df_bar_graph = filter_df.loc[filter_df['world_region'].isin(region)]
    df_bar_graph = pd.pivot_table(df_bar_graph[['world_region', 'year', conflict]],
                                  values=conflict, index=['world_region'], columns=['year'])

    fig_bar_data = []
    # Each year defines a new hidden (implies visible=False) trace in our visualization
    for year in df_bar_graph.columns:  # year is an integer number
        fig_bar_data.append(dict(data=dict(type='bar',
                                           x=df_bar_graph.index,  # world regions
                                           y=df_bar_graph[year],  # values for that year
                                           name=year,
                                           text=df_bar_graph[year],
                                           marker=dict(color='#9F9F5F'),
                                           showlegend=False
                                           ),
                                 # visible=False,
                                 layout=go.Layout(dict(title_text=f'<b>Year: {str(year)}<b>')),
                                 ))

    fig_bar_layout = dict(plot_bgcolor='#F5F5DC',
                          margin=dict(l=20, r=20, t=5, b=5),
                          yaxis=dict(title='Number of Conflicts', range=[0, 20]),
                          # change the range !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
                                            x=1,  # change position of the buttons
                                            y=1.15)])

    initial_data = dict(type='bar',
                        x=df_bar_graph.index,
                        y=df_bar_graph[1990],  # put the initial data as the year[0] of the range slider
                        marker=dict(color='#9F9F5F'),
                        text=df_bar_graph[year]
                        # name=str(1990)
                        )

    return title_line, \
           title_line2, \
           go.Figure(data=data_scatter, layout=layout_line), \
           title_bar1, \
           title_bar2, \
           go.Figure(data=initial_data, layout=fig_bar_layout, frames=fig_bar_data)


#######################################
# Second Callback
@app.callback(
    [
        Output("title_map", "children"),
        Output("world_map", "figure"),
        Output("title_card", "children"),
        Output("card", "children"),
        Output('title_top_countries', 'children'),
        Output("top_countries_graph", "figure")

    ],
    [
        Input("projection", "value"),
        Input('normal_slider', 'value')
    ]
)
# first the inputs, then the states, by order
def plots(projection, year):
    #######################################################################################
    # Third Visualization: World Map
    filter_df2 = df_deaths[(df_deaths['year'] == year)]
    #filter_df2 = filter_df2.groupby('Country').sum()[['Total Deaths']]

    title_map = f'Total deaths by conflicts or terrorism in {year}'
    data_choropleth = dict(type='choropleth',
                           locations=filter_df2['Country'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=filter_df2['Total Deaths'],
                           text=filter_df2['Country'],
                           colorscale='Electric',  # change the color scale !!!!!!!!!!!!!!!!!!!!!!!!!
                           reversescale=True,
                           )

    layout_choropleth = dict(geo=dict(scope='world',  # default
                                      projection=dict(type=['equirectangular', 'orthographic'][projection]),
                                      # showland=True,   # default = True
                                      landcolor='white',
                                      lakecolor='#ADD8E6',
                                      showocean=True,  # default = False
                                      oceancolor='azure'
                                      ),
                             margin=dict(l=20, r=20, t=10, b=5)
                             )

    #######################################################################################
    # Fourth Visualization: Card
    filter_cards = cards_data[(cards_data['year'] == year)]

    title_card = f'Total World deaths in {year}'
    card = round(filter_cards['Total Deaths'], 2)

    #######################################################################################
    # Fifth Visualization: Bar Chart 2
    title_top_count = f'Countries with the highest number of deaths in {year}'

    bar_chart2 = (
        dict(data=dict(type='bar', y=filter_df2.sort_values(by='Total Deaths', ascending=False).iloc[:5, :]['Country'],
                       x=filter_df2.sort_values(by='Total Deaths', ascending=False).iloc[:5, :]['Total Deaths'],
                       orientation='h', marker=dict(color='#9F9F5F'), text=filter_df2.sort_values(by='Total Deaths', ascending=False).iloc[:5, :]['Total Deaths']
                       ),
             # visible=False,
             ))

    fig_bar_layout2 = dict(
        plot_bgcolor='#F5F5DC',
        # yaxis=dict(autorange='reversed'),
        # dict(categoryorder='total descending'), !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        xaxis=dict(title='Number of Deaths', range=[0, 200000]),  # change the range !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        margin=dict(l=20, r=20, t=5, b=5)
    )


    return title_map, \
           go.Figure(data=data_choropleth, layout=layout_choropleth), \
           title_card,\
           card, \
           title_top_count, \
           go.Figure(data=bar_chart2, layout=fig_bar_layout2)


############################################################
if __name__ == '__main__':
    app.run_server(debug=True)
