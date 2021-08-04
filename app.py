# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 18:16:33 2021

@author: linds
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('2020_offices.csv')

district_types = df['DistrictType'].unique()
available_parties = df['Party'].unique()
available_indicators = df['Office'].unique()
ops=['no second component','plus', 'minus', 'divided by']

df_graph_empty = pd.DataFrame(columns=['DistrictNumber', 'x_votes', 'y_votes'])

app.layout = html.Div([
    
    html.Div([
        
        html.H4(
            children="Select the type of region for the results:"),

        html.Div([
            dcc.RadioItems(
                id='district-type',
                options=[{'label': i, 'value': i} for i in district_types],
                value='County',
                labelStyle={'display': 'inline-block'}
            )
        ])
    ]),
    
    html.Hr(),        
# x axis

    html.Div([
        html.H4(
            children="X axis:"),

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='President'
            ),
            dcc.RadioItems(
                id='xaxis-party',
                options=[{'label': i, 'value': i} for i in available_parties],
                value='All',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '35%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.RadioItems(
                id='xaxis-operator',
                options=[{'label': i, 'value': i} for i in ops],
                value='no second component',
                labelStyle={'display': 'block', 'text-align':'center', 'margin-right':'auto'}
            )
        ],
        style={'width': '20%', 'display': 'inline-block', 'text-align':'center', 'margin-left':'auto', 'margin-right':'auto'}),
        
        html.Div([
            dcc.Dropdown(
                id='xaxis1-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Auditor'
            ),
            dcc.RadioItems(
                id='xaxis1-party',
                options=[{'label': i, 'value': i} for i in available_parties],
                value='All',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '35%', 'display': 'inline-block'})
        
    ]),        
       
    html.Hr(),
# y axis
    html.Div([
        html.H4(
            children="Y axis:"),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='President'
            ),
            dcc.RadioItems(
                id='yaxis-party',
                options=[{'label': i, 'value': i} for i in available_parties],
                value='All',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '35%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.RadioItems(
                id='yaxis-operator',
                options=[{'label': i, 'value': i} for i in ops],
                value='no second component',
                labelStyle={'display': 'block', 'text-align':'center', 'margin-right':'auto'}
            )
        ],
        style={'width': '20%', 'display': 'inline-block', 'text-align':'center', 'margin-left':'auto', 'margin-right':'auto'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis1-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Auditor'
            ),
            dcc.RadioItems(
                id='yaxis1-party',
                options=[{'label': i, 'value': i} for i in available_parties],
                value='All',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '35%', 'float': 'right', 'display': 'inline-block'})
        
    ]),
        
        
    html.Hr(),
        

    dcc.Graph(id='indicator-graphic')])

#    dcc.Slider(
#        id='year--slider',
#        min=df['Year'].min(),
#        max=df['Year'].max(),
#       value=df['Year'].max(),
#        marks={str(year): str(year) for year in df['Year'].unique()},
#        step=None
#    )
                        


@app.callback(Output('indicator-graphic', 'figure'), 
              Input('xaxis-column', 'value'), 
              Input('xaxis1-column', 'value'), 
              Input('xaxis-party', 'value'), 
              Input('xaxis1-party', 'value'),
              Input('yaxis-column', 'value'), 
              Input('yaxis1-column', 'value'), 
              Input('yaxis-party', 'value'), 
              Input('yaxis1-party', 'value'),
              Input('district-type', 'value'),
              Input('xaxis-operator', 'value'),
              Input('yaxis-operator', 'value'))


def update_graph(xaxis_column_name, xaxis_column_name1,
                 xaxis_party, xaxis_party1,
                 yaxis_column_name, yaxis_column_name1,
                 yaxis_party, yaxis_party1,
                 district_type,
                 xaxis_op,
                 yaxis_op):
    
 # setup a dataframe that will be graphed   
    df_graph_this = df_graph_empty.copy()
    df_district = df[df['DistrictType'] == district_type]
    df_graph_this['DistrictNumber']=df_district['DistrictNumber'].unique()

 #establish the x values
#    dff_x=df_district[df_district['Party']==xaxis_party]
    if xaxis_op==ops[0]:
        dff_x=df_district[df_district['Party']==xaxis_party]
        dff_x_office=dff_x[dff_x['Office']==xaxis_column_name]    
        numbers=list(dff_x_office['DistrictNumber'].unique())
        for num in range(len(numbers)):
            x_num=numbers[num]
            votes=dff_x_office[dff_x_office["DistrictNumber"]==x_num]['Votes'].values[0]
            if votes>0:
                # this way a null doesn't become a zero, but a zero will become a null
                #find the index value at which to insert the vote value
                ind_x=df_graph_this[df_graph_this["DistrictNumber"]==x_num]['x_votes'].index[0]
                df_graph_this.loc[ind_x,'x_votes']=votes
    else:
# narrow df by parties        
       dff_x=df_district[df_district['Party']==xaxis_party]
       dff_x1=df_district[df_district['Party']==xaxis_party1]
# narrow dfs by offices
       dff_x_office=dff_x[dff_x['Office']==xaxis_column_name]    
       dff_x_office1=dff_x1[dff_x1['Office']==xaxis_column_name1]
       assert(len(dff_x_office1)==len(dff_x_office))
# create a list of all the District Numbers
       numbers=list(dff_x_office['DistrictNumber'].unique())
       for num in range(len(numbers)):
           x_num=numbers[num]
           if xaxis_op==ops[1]:    #plus
               votes=dff_x_office[dff_x_office["DistrictNumber"]==x_num]['Votes'].values[0]+dff_x_office1[dff_x_office1["DistrictNumber"]==x_num]['Votes'].values[0]
           elif xaxis_op==ops[2]:  #minus
               votes=dff_x_office[dff_x_office["DistrictNumber"]==x_num]['Votes'].values[0]-dff_x_office1[dff_x_office1["DistrictNumber"]==x_num]['Votes'].values[0]
           elif xaxis_op==ops[3]: #divided by
               votes=dff_x_office[dff_x_office["DistrictNumber"]==x_num]['Votes'].values[0]/dff_x_office1[dff_x_office1["DistrictNumber"]==x_num]['Votes'].values[0]
           if votes>0:
               # this way a null doesn't become a zero, but a zero will become a null
               #find the index value at which to insert the vote value
               ind_x=df_graph_this[df_graph_this["DistrictNumber"]==x_num]['x_votes'].index[0]
               df_graph_this.loc[ind_x,'x_votes']=votes
    

 #establish the y values
    if yaxis_op==ops[0]:
        dff_y=df_district[df_district['Party']==yaxis_party]
        dff_y_office=dff_y[dff_y['Office']==yaxis_column_name]    
        numbers=list(dff_y_office['DistrictNumber'].unique())
        for num in range(len(numbers)):
            y_num=numbers[num]
            votes=dff_y_office[dff_y_office["DistrictNumber"]==y_num]['Votes'].values[0]
            if votes>0:
                # this way a null doesn't become a zero, but a zero will become a null
                #find the index value at which to insert the vote value
                ind=df_graph_this[df_graph_this["DistrictNumber"]==y_num]['y_votes'].index[0]
                df_graph_this.loc[ind,'y_votes']=votes
            
    else:
# narrow df by parties        
       dff_y=df_district[df_district['Party']==yaxis_party]
       dff_y1=df_district[df_district['Party']==yaxis_party1]
# narrow dfs by offices
       dff_y_office=dff_y[dff_y['Office']==yaxis_column_name]    
       dff_y_office1=dff_y1[dff_y1['Office']==yaxis_column_name1]
       assert(len(dff_y_office1)==len(dff_y_office))
# create a list of all the District Numbers
       numbers=list(dff_y_office['DistrictNumber'].unique())
       for num in range(len(numbers)):
           y_num=numbers[num]
           if yaxis_op==ops[1]:    #plus
               votes=dff_y_office[dff_y_office["DistrictNumber"]==y_num]['Votes'].values[0]+dff_y_office1[dff_y_office1["DistrictNumber"]==y_num]['Votes'].values[0]
           elif yaxis_op==ops[2]:  #minus
               votes=dff_y_office[dff_y_office["DistrictNumber"]==y_num]['Votes'].values[0]-dff_y_office1[dff_y_office1["DistrictNumber"]==y_num]['Votes'].values[0]
           elif yaxis_op==ops[3]: #divided by
               votes=dff_y_office[dff_y_office["DistrictNumber"]==y_num]['Votes'].values[0]/dff_y_office1[dff_y_office1["DistrictNumber"]==y_num]['Votes'].values[0]
           if votes>0:
               # this way a null doesn't become a zero, but a zero will become a null
               #find the index value at which to insert the vote value
               ind=df_graph_this[df_graph_this["DistrictNumber"]==y_num]['y_votes'].index[0]
               df_graph_this.loc[ind,'y_votes']=votes
    
    fig = px.scatter(x=df_graph_this['x_votes'],
#        x=dff_x[dff_x['Office'] == xaxis_column_name]['Votes'],
                     y=df_graph_this['y_votes'],
                     hover_name=df_graph_this['DistrictNumber'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
#    xaxis_label=xaxis_column_name+" ("+xaxis_party+")"
    if xaxis_op==ops[0]: 
        xaxis_label=xaxis_column_name+" ("+xaxis_party+")"
    elif xaxis_op==ops[1]: xaxis_label = xaxis_column_name+" ("+xaxis_party+") + "+xaxis_column_name1+" ("+xaxis_party1+")"
    elif xaxis_op==ops[2]: xaxis_label = xaxis_column_name+" ("+xaxis_party+") - "+xaxis_column_name1+" ("+xaxis_party1+")"
    elif xaxis_op==ops[3]: xaxis_label = xaxis_column_name+" ("+xaxis_party+") / "+xaxis_column_name1+" ("+xaxis_party1+")"
    if yaxis_op==ops[0]: 
        yaxis_label=yaxis_column_name+" ("+yaxis_party+")"
    elif yaxis_op==ops[1]: yaxis_label = yaxis_column_name+" ("+yaxis_party+") + "+yaxis_column_name1+" ("+yaxis_party1+")"
    elif yaxis_op==ops[2]: yaxis_label = yaxis_column_name+" ("+yaxis_party+") - "+yaxis_column_name1+" ("+yaxis_party1+")"
    elif yaxis_op==ops[3]: yaxis_label = yaxis_column_name+" ("+yaxis_party+") / "+yaxis_column_name1+" ("+yaxis_party1+")"
    fig.update_xaxes(title=xaxis_label)

    fig.update_yaxes(title=yaxis_label)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)