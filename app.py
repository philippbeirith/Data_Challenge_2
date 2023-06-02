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
import webbrowser
from threading import Timer
#Set it so graphs created during testing open in a browser
pio.renderers.default='browser'

#######################
#Set up app structure #
#######################

app.layout = html.Div([
    #Title
    html.Div(children='Predicting Burglaries in Barnet'),
    
    html.Div(children=[

        html.Br(),
        html.Label('Predictions for month of:'),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
            value=5,
        )]),
    
    #LSOA/Ward selector
    dcc.RadioItems(
                ['LSOA Codes', 'Wards'],
                'Linear',
                id='crossfilter_geo_type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            ),
        
    #Individual graph(s)
    dcc.Graph(id='crime_predictions_ward', figure = data.generate_heatmap()),
    
    #Download Button
    html.Div(
    [
        html.Button("Download Resource Allocations (CSV)", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    ]
    ),
    ])

#######################
# Define interactions #
#######################


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return ('hi')#dcc.send_data_frame(df.to_csv, "resource.csv")

#This plots our prediction of burglaries (thus resource allocation) on a heatmap by ward/lsoa
@app.callback(
    Output('crime_predictions_ward', 'figure'),
    Input('Month', 'value')
    Input('crossfilter_geo_type', 'value')
)
def update_crime_predictions(Month, geo_type):
    crime_predictions = data.generate_heatmap(Month, geo_type)
    return crime_predictions

#This automatically launches a web browser with the dashboard.
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

#######################
#      Run app        #
#######################

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=False, port=8050)
    
    
    
    
    
