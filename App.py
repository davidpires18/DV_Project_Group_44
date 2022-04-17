import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from raceplotly.plots import barplot
import plotly.express as px

import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Dataset Processing

path = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

data = pd.read_csv(path)
dff = data.copy()
data.date = pd.to_datetime(data.date, format='%Y-%m-%d')
data['year'] = data.date.dt.year
df_1 = data[['date','year','total_cases', 'total_deaths', 'total_vaccinations', 'continent', 'location', 'people_fully_vaccinated', 'population']]
df_1 =df_1.dropna()
df_1 = df_1[df_1['date']>'2021-01-01']
df = df_1.groupby(['location','year']).max().reset_index()
df_2 = df.copy() #df_1.groupby(['location']).max().reset_index()
df_2['%_TFVP'] = df_2['people_fully_vaccinated'] / df_2['population'] * 100
#df_3 = df_2[['total_cases', 'continent', 'location', '%_TFVP']]


dff = dff.groupby(['date', 'location']).max().reset_index()
dff = dff[dff.gdp_per_capita != 0]
dff = dff[dff.total_tests_per_thousand != 0]
dff = dff[dff.total_deaths_per_million != 0]
dff = dff[dff.total_deaths != 0]

dff['perc_fully_vaccinated'] = dff['people_fully_vaccinated'] / dff['population'] * 100

dff['perc_fully_vaccinated'] = dff['perc_fully_vaccinated'].round(1)

dff['not_fully_vac'] = dff['people_vaccinated'] / dff['population'] * 100

dff['not_fully_vac'] = dff['not_fully_vac'].round(1)

dff_1 = dff.copy()

nan_value = float("NaN")

dff_1.replace("", nan_value, inplace=True)

dff_1.dropna(subset=["date", "continent", "location", 'gdp_per_capita', 'population', 'total_deaths_per_million'],
             inplace=True)

dff_1.date = dff_1.date.replace(' ', '')
dff_1.total_deaths_per_million = dff_1.total_deaths_per_million.replace(' ', '')
dff_1.perc_fully_vaccinated = dff_1.perc_fully_vaccinated.replace(' ', '')
dff_1.not_fully_vac = dff_1.not_fully_vac.replace(' ', '')

dff_1['total_deaths'] = dff_1['total_deaths'].fillna(0).astype(int)

dff_3 = dff_1[~(dff_1['date'] < '2020-03-15')]

dff_4 = dff_1[~(dff_1['date'] < '2021-01-12')]

dff_4 = dff_4[['gdp_per_capita', 'perc_fully_vaccinated', 'population', 'continent', 'date', 'location']]

# ----------------------------------

data_f = pd.read_csv("changes-visitors-covid.csv")

data_f = data_f.dropna()

country_options = [
    dict(label=country, value=country)
    for country in data_f['Entity'].unique()]





# Creating images


# Figure 1

fig_scatter = go.Figure(px.scatter(dff_4,

                                   x='gdp_per_capita',

                                   y='perc_fully_vaccinated',

                                   size='population',

                                   facet_col='continent',

                                   color='continent',

                                   title='Deaths per million X Fully vaccinated',

                                   labels={'gdp_per_capita': 'GDP per Capita',

                                           'perc_fully_vaccinated': 'Fully vaccinated'},

                                   log_y=False,

                                   opacity=0.7,

                                   range_y=[0, 100],

                                   range_x=[-25_000, 100_000],

                                   hover_name='location',

                                   animation_frame='date',

                                   height=600,

                                   width=1250,

                                   size_max=50))

fig_scatter.update_traces(
    textposition='middle center',

    textfont={'color': 'black', 'family': 'Helvetica', 'size': 17},

    mode="text+markers")

fig_scatter.update_layout(

    title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},

    yaxis={'title': {'text': 'Percentage of fully vaccinated'}},
    legend={'font': {'size': 18}, 'title': {'font': {'size': 18}}},
    title_text='GDP per Capita and the Evolution of fully vaccinated people across the continents.',

    title_x=0.5

)

fig_scatter.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 100
fig_scatter.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100


# The raceplot

raceplot = barplot(
    dff_3,
    item_column='location',
    value_column='total_deaths',
    time_column='date',
    top_entries=10,

)
raceplot = raceplot.plot(
                    item_label='Top 10 Countries',
                    value_label='Death toll',
                    time_label='Date: ',
                    frame_duration=200,
                    orientation='horizontal',
                    date_format='%d/%m/%Y',
                    )

# Helpful functions

Radio_cases_dpd = dbc.RadioItems(
        id='Radio_cases',
        className='radio',
        options=[
                    {'label': 'Total Cases', 'value': 'total_cases'},
                    {'label': 'Total Deaths', 'value': 'total_deaths'},
                    {'label': 'Total Vaccinations', 'value': 'total_vaccinations'}
                ],
        value='total_cases',
        inline=True
    )

drop_continent = dcc.Dropdown(
        id = 'drop_continent',
        clearable=False,
        searchable=False,
        options=[{'label': 'World', 'value': 'world'},
                {'label': 'Europe', 'value': 'europe'},
                {'label': 'Asia', 'value': 'asia'},
                {'label': 'Africa', 'value': 'africa'},
                {'label': 'North america', 'value': 'north america'},
                {'label': 'South america', 'value': 'south america'},
                {'label': 'Oceania', 'value': 'oceania'}],
        value='world',
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
)

slider_map = dcc.RangeSlider(
                            id='year_slider',
                            min=2020,
                            max=2022,
                            value=[2020, 2022],
                            marks={'2020': 'Year 2020',
                                   '2021': 'Year 2021',
                                   '2022': 'Year 2022',
                                   },
                            step=1
)
#______________________APP________________________

app = dash.Dash(__name__)
server = app.server
app.title = 'COVID Impact Analysis'
app.layout = html.Div([

    html.Div([
        #main
        html.Div([
            #Title
            html.Div([
                    html.H1(children='COVID Analysis'),
                    html.Label('This Dashboard aims to allow the user to have an overview of COVID cases around the world and also gather further information on how this virus have impacted our day-to-day lives.',
                                style={'color':'rgb(33 36 35)'}),
                ], className='side_bar'),
            #Area1 - Radio options
            html.Div([
                html.Label('Select the overview of COVID cases:'),
                html.Br(),
                html.Br(),
                Radio_cases_dpd
            ], className='box', style={'margin': '10px', 'padding-top':'15px', 'padding-bottom':'15px'}),
            #Big BOX1 - 2 Graphs
            html.Div([
                #Area2 - Sunburst graph - 40%
                html.Div([
                    html.Div([
                        html.Label('Sunburst of Totals', style={'font-size':'medium'}),
                        dcc.Graph(id='graph_sunburst'),
                        html.Div([
                            html.P(' %_TFVP - % of totally vaccinated people',style={'font-size':'10px'})
                        ], className='box_comment'),
                    ], className='box', style={'padding-bottom':'45px'}),
                ], className='smalltextbox',style={'width': '40%', 'align': 'center', 'justify': 'center', 'vertical-align': 'middle'}),
                #Area3 - Choroplet Graph - 60%
                html.Div([
                    html.Div([
                        html.Div([
                            #Area3 - Title box
                            html.Div([
                                html.Div([
                                    html.Label('Totals Around the World', style={'font-size':'medium'}),
                                    html.Br(),
                                    html.Label('The values shown are according to the overview chosen above. You may also select the region you would like to see with the button on the right.', style={'font-size':'10px'}),
                                ], style={'width': '70%'}),
                                html.Div([], style={'width': '5%'}),
                                html.Div([
                                    drop_continent,
                                    html.Br(),
                                    html.Br(),
                                ], style={'width': '25%'}),
                            ], className='row'),
                            #Area3 - Graph
                            dcc.Graph(id='Choro_graph', style={'position':'relative', 'top':'-10px'}),
                            ], className='box'),
                    ]),
                ], className='smalltextbox',style={'width': '60%', 'align': 'center', 'justify': 'center', 'vertical-align': 'middle'}),
            ], className='row'),

            html.Div([
                slider_map
            ], className='box'),

            #Area 4 - Raceplot
            html.Div([
                    html.Label('Animated Scatterplot for Vaccinations X GDP per Capita X Size of Population ', style={'font-size': 'medium'}),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(figure=fig_scatter),
            ], className='box', style={'width': '95%'}),
            html.Div([
                # Area 5 -
                html.Div([
                    html.Label("Covid Death Race", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('In the graphic below its possible to see the top 10 countries with the most deaths variating with the time.yo', style={'font-size': '10px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(figure=raceplot),
                ], className='box', style={'width': '40%'}),
                # Area 6 -
                html.Div([
                    html.H4('Variation of visitor numbers to specific categories of location during the pandemic'),
                    html.P("Select a country:"),
                    dcc.Dropdown(
                        id='selection',
                        options=country_options,
                        value='Portugal',
                    ),
                    dcc.Graph(id="graph")], className='box', style = {'width': '60%'}),
            ], className='row'),
            #Footer
            html.Div([
                html.Div([
                    html.P(['Authors:',
                            html.Br(),
                            'David Pires (m20211008) | m20211008@novaims.unl.pt', html.Br(),
                            'Marcos Oliveira (m20210593) | m20210593@novaims.unl.pt',html.Br(),
                            'Tiago Seca (m20210564)| m20210564@novaims.unl.pt'
                            ], style={'font-size':'12px'}),
                ], style={'width':'70%'}),
                html.Div([
                    html.P(['Useful Links ',
                            html.Br(),
                            html.A('Our World in Data - Coronavirus Pandemic (COVID-19)', href='https://ourworldindata.org/coronavirus', target='_blank')], style={'font-size':'12px'})
                ], style={'width':'30%'}),
            ], className = 'footer', style={'display':'flex'}),
        ], className='main'),
    ]),
])
#______________________Callbacks________________________
@app.callback(
    Output('Choro_graph', 'figure'),
    [Input('Radio_cases', 'value'),
     Input('year_slider', 'value'),
     Input('drop_continent', 'value')]
)
def update_graph(opt, year, continent):
    filtered_by_year_df = df[(df['year'] >= year[0]) & (df['year'] <= year[1])]
    choro_data = []

    temp_data = dict(type='choropleth',
                     locations=filtered_by_year_df['location'],
                     locationmode='country names',
                     z=np.log(filtered_by_year_df[opt]),
                     colorscale='Sunsetdark',
                     colorbar=dict(title='{} (log scaled)'.format(opt)),
                     customdata=filtered_by_year_df[opt],
                     hovertemplate="Country: <b>%{location}</b> <br>" +
                                   "%{customdata} in Total <br><extra></extra>",
                     )

    choro_data.append(temp_data)

    choro_layout = dict(geo=dict(scope=continent,
                                   projection={'type': 'natural earth'},
                                   bgcolor='rgba(0,0,0,0)'),
                          margin=dict(l=0,
                                      r=0,
                                      b=0,
                                      t=30,
                                      pad=0),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                        )

    choro_fig = go.Figure(data=choro_data, layout=choro_layout)
    choro_fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), font_family="Gill Sans MT",
                                 title_font_family="Gill Sans MT")
    return choro_fig
@app.callback(
    Output('graph_sunburst', 'figure'),
    [Input('Radio_cases', 'value'),
     Input('year_slider', 'value')]
)
def update_graph2(opt, year):
    filtered_by_year_df = df_2[(df_2['year'] >= year[0]) & (df_2['year'] <= year[1])]
    suburst_data = []

    # Sunburst Graph
    fig = go.Figure(px.sunburst(
        data_frame=filtered_by_year_df,
        path=["continent", 'location'],  # Root, branches, leaves
        values=opt,
        color="%_TFVP",
        color_continuous_scale = 'Sunsetdark',
        range_color=[0, 100],
        branchvalues="total",
    ))

    fig.update_traces(textinfo='label + percent entry')
    fig.update_layout(margin=dict(t=10, l=0, r=5, b=5), font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT")
    return fig

@app.callback(
    Output("graph", "figure"),
    Input("selection", "value"))
def display_animated_graph(selection):
    fig = px.line(data_f.loc[data_f.Entity == selection], x='Day',
                  y=['retail_and_recreation', 'grocery_and_pharmacy', 'residential', 'transit_stations', 'parks',
                     'workplaces'], title='Time Series with Rangeslider'


                  )

    fig.update_xaxes(rangeslider_visible=True)

    # Edit the layout
    fig.update_layout(
                      xaxis_title='Date',
                      yaxis_title='% Variation')

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
