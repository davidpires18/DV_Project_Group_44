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
data.date = pd.to_datetime(data.date, format='%Y-%m-%d')
data['year'] = data.date.dt.year
df_1 = data[['date','year','total_cases', 'total_deaths', 'total_vaccinations', 'continent', 'location', 'people_fully_vaccinated', 'population']]
df_1 =df_1.dropna()
df = df_1.groupby(['location','year']).max().reset_index()
df_2 = df.copy() #df_1.groupby(['location']).max().reset_index()
df_2['%_TFVP'] = df_2['people_fully_vaccinated'] / df_2['population'] * 100
#df_3 = df_2[['total_cases', 'continent', 'location', '%_TFVP']]


raceplot = barplot(
    df_1,
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
                        html.Label('Totals by continent', style={'font-size':'medium'}),
                        dcc.Graph(id='graph_sunburst'),
                        html.Div([
                            html.P('Choose any continent to have an extra insight of the Cases among its countries.',style={'font-size':'10px'})
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
                                    html.Label('Totals around the world', style={'font-size':'medium'}),
                                    html.Br(),
                                    html.Label('The value shown are according to the Overview chosen above.', style={'font-size':'10px'}),
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
                            # Area3 - RangeSlider
                            html.Div([
                                slider_map
                            ], style={'width': '80%', 'position':'relative', 'top':'-20px'}),
                        ], className='box', style={'padding-bottom': '15px'}),
                    ]),
                ], className='smalltextbox',style={'width': '60%', 'align': 'center', 'justify': 'center', 'vertical-align': 'middle'}),
            ], className='row'),

            #Area 4 - Raceplot
            html.Div([
                    html.Label('Covid death race', style={'font-size': 'medium'}),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(figure=raceplot),
            ], className='box', style={'width': '95%'}),
            html.Div([
                # Area 5 -
                html.Div([
                    html.Label("Colocar o grafico do Marcos2", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Frescurinhaaaaa', style={'font-size': '10px'}),
                    html.Br(),
                    html.Br(),
                    # dcc.Graph(figure=fig_gemissions)
                ], className='box', style={'width': '40%'}),
                # Area 6 -
                html.Div([
                    html.Label("Colocar o gráfico do Tiago2", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Frescurinhaaaaa', style={'font-size': '10px'}),
                    html.Br(),
                    html.Br(),
                    # dcc.Graph(figure=fig_water)
                ], className='box', style={'width': '63%'}),
            ], className='row'),
            #Footer
            html.Div([
                html.Div([
                    html.P(['Group',
                            html.Br(),
                            'David Pires', html.Br(),
                            'Marcos Oliveira',html.Br(),
                            'Tiago Seca'
                            ], style={'font-size':'12px'}),
                ], style={'width':'70%'}),
                html.Div([
                    html.P(['Useful Links ',
                            html.Br(),
                            html.A('Our World in Data', href='https://ourworldindata.org/', target='_blank')], style={'font-size':'12px'})
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
                     colorscale='Hot',
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
        color_continuous_scale=px.colors.sequential.Hot,
        range_color=[0, 100],
        branchvalues="total",
    ))

    fig.update_traces(textinfo='label + percent entry')
    fig.update_layout(margin=dict(t=10, l=0, r=5, b=5), font_family="Gill Sans MT",
                      title_font_family="Gill Sans MT")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
