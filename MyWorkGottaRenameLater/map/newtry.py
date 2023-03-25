import folium
from folium.plugins import HeatMap
import pandas
# Load data
data = pandas.read_csv('archive/df4.csv')


# Create map
m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)


# check if NaN values are present
print(data.isnull().values.any())

# replace NaN values with 0
data = data.fillna(0)

heatmap_data = data[['Latitude', 'Longitude']].values.tolist()


HeatMap(heatmap_data, name='Heatmap', min_opacity=0.5, radius=15, blur=10, max_zoom=1).add_to(m)

folium.LayerControl().add_to(m)

# m.save('heatmap.html')
m