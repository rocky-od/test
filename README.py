# test
test
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from random_word import RandomWords
import pandas as pd
import numpy as np
import plotly.express as px
import json
import dash_table

r = RandomWords()
df_cluster_summary = pd.DataFrame({
    'cluster_number' : [1,2,3,4,5],
    'cluster_x': np.random.random(5),
    'cluster_y': np.random.random(5),
    'cluster_size': [1000, 900, 700, 500, 800],
    'top_words': [
        ['Panzerfaust', 'lyonnaise', 'arguments', 'leching', 'nocua'],
        ['quaestio', 'trial-bar', 'porous', 'unmeaningness', 'xyston'],
        ['Krugerrand', 'holoptic', 'wealth', 'pax-board', 'resistingly'],
        ['retromer', 'transmissable', 'manchettes', 'chirograph', 'hillman'],
        ['write', 'consuetudes', 'gymlike', 'parentally', 'chromatically']
    ],
    'importances': [
        np.random.rand(5),
        np.random.rand(5),
        np.random.rand(5),
        np.random.rand(5),
        np.random.rand(5)
    ]
})

longer_df = pd.concat([df_cluster_summary]*30, ignore_index=True)
longer_df = longer_df[['cluster_number', 'top_words']]

fig1 = px.scatter(data_frame=df_cluster_summary,
                  x='cluster_x', 
                  y='cluster_y',
                  size='cluster_size', 
                  hover_data=['cluster_size', 'cluster_number'],
                  height=600,
                  width=800)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    dcc.Tabs([
            dcc.Tab(label='Tab One', children=[
                html.Div(dcc.Graph(id='size_scatter', figure=fig1), style = {'width':'60%', 'float':'left'}),
                html.Div(dcc.Graph(id='importance_bar', config = {'displayModeBar': False}), style = {'width':'40%', 'float':'right'})]),
            dcc.Tab(label='Tab Two', children=[
                dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in longer_df.columns],
                            data=longer_df.to_dict('records'),
                            page_size=10)])
            ])
)

    
        
        
        
        
        
    


 
@app.callback(
    Output('importance_bar', 'figure'),
    [Input('size_scatter', 'clickData')])

def update_figure(clickData):
    N = int(clickData['points'][0]['customdata'][1])

    x = df_cluster_summary[df_cluster_summary['cluster_number'] == N ]['top_words'].values[0]
    y = sorted(df_cluster_summary[df_cluster_summary['cluster_number'] == N ]['importances'].values[0], reverse=True)
    fig = px.bar(x=x, y=y)
    return fig
  
@app.callback(
    Output('table', 'data'),
    [Input('size_scatter', 'clickData')])
def update_figure(clickData):
    N = clickData['points'][0]['customdata'][1]
    data = longer_df[longer_df['cluster_number'] == N]
    return data.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)



