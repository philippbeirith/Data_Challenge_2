#Import other functions and data
from dashboard_app.main import app
from dashboard_app import data
from dashboard_app import sql_querries

#Import libraries
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.io as pio
#Set it so graphs created during testing open in a browser
pio.renderers.default='browser'

if __name__ == '__main__':
    #Set up app structure
    app.layout = html.Div([
        #Title
        html.Div(children='Predicting Burglaries in Barnet'),
        
        #Individual graphs
        dcc.Graph(id='burglary_predictions', figure = {}),
        dcc.Graph(id='crime_predictions', figure = {}),
        dcc.Graph(id='demographics', figure = {}),
        dcc.Graph(id='basic', figure = data.generate_heatmap())
        ])
    
    #######################
    # Define interactions #
    #######################
    
    #This plots our prediction of burglaries (thus resource allocation) by means of heatmap
    @app.callback(
        Output('crime_predictions', 'figure'),
        Input('Month', 'value')
    )
    def update_crime_predictions(Month):
        crime_predictions = data.generate_heatmap()
        return crime_predictions
    
    #Add a callback and function to update the parallel coordinate plot based on filter.
    @app.callback(
        Output('crime_predictions', 'figure'),
        Input('Month', 'value')
    )
    def update_crime_predictions(Month):
        return crime_predictions
    
    #Add a callback and function to update the violin plot based on filter.
    @app.callback(
        Output('demographics', 'figure'),
        Input('Month', 'value')
    )
    def update_demographics(Month):
        return demographics



    app.run_server(debug=False, dev_tools_ui=False)
