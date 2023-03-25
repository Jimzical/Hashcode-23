import pandas
import plotly.express as px


def get_location(df):
    # fig = px.scatter_mapbox(df4, lat="Latitude", lon="Longitude", hover_name="Short Address", hover_data=["AverageCost"], color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig = px.density_mapbox(df, lat="Latitude", lon="Longitude", z="AverageCost",color_continuous_scale='Turbo', mapbox_style="stamen-terrain",opacity=0.45,height=900,width=900)
    # can you make the map bigger?
    # fig.update_layout(width=100, height=100)
    fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=11, mapbox_center_lat = 12.9716, mapbox_center_lon = 77.5946)
    # can you make the color
    fig.show(width=9000, height=9000)

if __name__ == '__main__':
    df = pandas.read_csv('archive/df4.csv')
    df = df.set_index('ID')

    cuisine = 'North Indian'
    df_cuisines = df[df['Cuisines'].str.contains(cuisine)]



    get_location(df_cuisines)

