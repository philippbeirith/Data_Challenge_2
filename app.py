#Import other functions and data
from dashboard_app.main import app
from dashboard_app import data
from dashboard_app import XGboost

#Import libraries
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.io as pio
import webbrowser
from threading import Timer
#Set it so graphs created during testing open in a browser
pio.renderers.default='browser'

#pre run model
allocation, df = XGboost.run_model('si')
#######################
#Set up app structure #
#######################

app.layout = html.Div([
    #Title
    html.Div(children='Predicting Burglaries in Barnet'),
        
    #Individual graph(s)
    dcc.Graph(id='crime_predictions_ward', figure = data.generate_heatmap(df)),
    
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
    prevent_initial_call=True
)
def func(n_clicks, ):
    return dcc.send_data_frame(allocation.to_excel, "resource_allocations.xlsx", sheet_name="Allocations")


#This automatically launches a web browser with the dashboard.
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

#######################
#      Run app        #
#######################

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=False, port=8050)
    
