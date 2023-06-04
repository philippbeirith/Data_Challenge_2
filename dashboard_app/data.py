import pandas as pd
import numpy as np
import pyproj
import json
import ast
import plotly.express as px

def generate_heatmap(df):
    with open("data/lsoa_coordinates.geojson", "r") as data:
        lsoa_codes_dict = json.loads(data.read())

    # Define the source and target coordinate systems
    source_proj = pyproj.CRS("EPSG:27700")  
    target_proj = pyproj.CRS("EPSG:4326")  

    # Coordinate transformation function
    transformer = pyproj.Transformer.from_crs(source_proj, target_proj, always_xy=True)

    # Convert the coordinates for each feature in the GeoJSON
    for feature in lsoa_codes_dict["features"]:
        geometry = feature.get("geometry")
        if geometry and geometry["type"] == "Polygon":
            coordinates = geometry.get("coordinates")
            if coordinates:
                # Handle different coordinate representations
                if isinstance(coordinates[0], float):
                    # Single coordinate representation
                    coordinates = [coordinates]
                elif isinstance(coordinates[0], (list, tuple)) and isinstance(coordinates[0][0], float):
                    # List of coordinate tuples representation
                    coordinates = [coordinates]
                elif isinstance(coordinates[0], (list, tuple)) and isinstance(coordinates[0][0], (list, tuple)):
                    # Nested list of coordinate tuples representation
                    coordinates = coordinates[0]

                # Perform the coordinate transformation
                transformed_coords = []
                for lon, lat in coordinates:
                    transformed_coords.append(transformer.transform(lon, lat))

                # Update the coordinates with the transformed values
                geometry["coordinates"] = [transformed_coords]


    # Data with latitude/longitude and values
    df['LSOA_code'] = df['LSOAencoded'].astype(str)
    df.drop(labels = ['LSOAencoded'], inplace = True, axis = 1)
    df = df.groupby(['LSOA_code'])['predictions'].sum().reset_index(name='Predicted_Crime')

    fig = px.choropleth_mapbox(df, 
                               geojson=lsoa_codes_dict, 
                               locations=df.LSOA_code, 
                               featureidkey="properties.LSOA21CD",
                               color=df.Predicted_Crime,
                               color_continuous_scale="Viridis",
                               mapbox_style="carto-positron",
                               zoom=10,
                               opacity=0.5,
                               center = {'lat': 51.632510, 'lon': -0.169120}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return(fig)