###########################
# Plot a normal line chart
data = dict(type='scatter',
            x=mycountry_dataset['year'],
            y=mycountry_dataset['CO2_emissions']
            )

layout = dict(title=dict(text=mycountry + ' Co2 Emissions'),
              xaxis=dict(title='Years'),
              yaxis=dict(title='Co2 Emissions')
              )

clear_figure = go.Figure(data=data, layout=layout)
figure.show(renderer='iframe')

###########################
# One extra step
amb_data_1 = [dict(type='scatter',
                   y=df.loc[df['continent'] == continent]['CO2_emissions'],
                   x=df.loc[df['continent'] == continent]['year'],
                   text=df.loc[df['continent'] == continent]['country_name'],
                   mode='markers',
                   name=continent
                   )
              for continent in df['continent'].unique()]

###########################
# Ways to modify bar charts
ex3_layout = dict(title=dict(text='Comparison of % sales across all Product categories over last quarter'),
                  yaxis=dict(title='Relative Percentage'),
                  xaxis=dict(title='Product'),
                  barmode='stack'  # It is in the layout that we define the barmode to stacked, by default is as 'group'
                  # try any of these 'stack', 'group', 'overlay', 'relative'
                  )

ex3_fig = go.Figure(data=ex3_data, layout=ex3_layout)

###########################
# More layout options
layout_2 = dict(
    title=dict(
        text='Title',
        x=.5  # This parameter puts the title text in a position from 0 to 1 acording to the x axis,
        # i.e x=.5 is a centered title
        # y=0 --> title goes to the bottom
    ),

    xaxis=dict(
        title='X Axis'
    ),

    yaxis=dict(
        title='Y Axis',
        range=(-1, 1)
    ),

    height=450,
    width=700,
    paper_bgcolor='azure'  # different background color
)

###########################
# Multiple variables graph
x = df['weight']
y = df['acceleration']
color = df['cylinders']  # or even df['origin']
size = df['horsepower'] / 7  # We need to normalize this (to be between 0 and 1)

# This additional variable might seem to much
line_width = df['mpg'] / 10

data_2d = dict(type='scatter',
               x=x,
               y=y,
               mode='markers',
               text=df['name'],
               marker=dict(size=size,
                           color=color,
                           colorbar=dict(title=dict(text='Cylinders')),
                           colorscale='Viridis',
                           showscale=True,
                           line=dict(width=line_width,
                                     color='black',  # df['model_year']
                                     colorscale='inferno'  # Not in use here since our line color is fixed!
                                     )
                           ),
               hovertemplate="Cars Name: <b>%{text}</b> <br><br>" + "Horsepower: %{y} horses<br>",
               name='Scatter Visualization',
               showlegend=False
               )

layout_2d = dict(title=dict(text='MPG Dataset Display'),
                 yaxis=dict(title='Horsepower'),
                 xaxis=dict(title='Acceleration')
                 )

fig_2 = go.Figure(data=data_2d, layout=layout_2d)
fig_2.show(renderer='iframe')


###########################
# Animation with year slider (bar chart)

# Each year defines a new hidden (implies visible=False) trace in our visualization
frames = []

for year in df_continent.columns[1:]:  # we do not include the first frame here
    frames.append(dict(data=dict(type='bar',
                                 x=df_continent.index,
                                 y=df_continent[year],
                                 name=year,
                                 ),
                       layout=go.Layout(title_text='Emissions in the year of ' + year)
                       )
                  )

# First introduction to buttons
fig_bar_layout = dict(title=dict(text='Emissions by region comparison from 1990 until 2014'),
                      yaxis=dict(title='Emissions',
                                 range=[0, 20000]
                                 ),

                      # PLAT BUTTON TO SEE CHANGES THORWGHOUT THE YEARS
                      updatemenus=[dict(type="buttons",
                                        buttons=[dict(label="Play",
                                                      method="animate",
                                                      args=[None])
                                                 ]
                                        )
                                   ]
                      )

initial_data = dict(type='bar',
                    x=df_continent.index,
                    y=df_continent['1990'],
                    name=str(1990))

fig_bar = go.Figure(data=initial_data, layout=fig_bar_layout, frames=frames)

fig_bar.show(renderer='iframe')


###########################
# World globe layout

data_choropleth = dict(type='choropleth',
                       locations=df_emission_0['country_name'],
                       # There are three ways to 'merge' your data with the data pre embedded in the map
                       locationmode='country names',
                       z=np.log(df_emission_0['CO2_emissions']),
                       text=df_emission_0['country_name'],
                       colorscale='inferno'
                       )

layout_choropleth = dict(geo=dict(scope='world',  # default
                                  projection=dict(type='orthographic'
                                                  ),
                                  # showland=True,   # default = True
                                  landcolor='black',
                                  lakecolor='white',
                                  showocean=True,  # default = False
                                  oceancolor='azure'
                                  ),

                         title=dict(text='World CO2 Emissions Choropleth Map',
                                    x=.5  # Title relative position according to the xaxis, range (0,1)
                                    )
                         )


###########################
###########################
###########################
###########################