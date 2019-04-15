import folium
import os
import json
import pandas as pd


# get data
df = pd.read_csv('cali_ac_coord.csv')


# Create map object
#37.7699936,-122.4492177
m = folium.Map(location=[37.7599936,-122.4592177], zoom_start=12)

# Global tooltip
tooltip = 'Click For More Info'

# Create custom marker icon
#logoIcon = folium.features.CustomIcon('logo.png', icon_size=(50, 50))

# Vega data
#vis = os.path.join('data', 'vis.json')

# Geojson Data
#overlay = os.path.join('data', 'overlay.json')

# Create markers
for x in range(len(df)): 
    pop = '<strong> location:'+str(x)+'</strong>'
    folium.Marker([df.LATITUDE[x], df.LONGITUD[x]],
                  popup=pop,
                  tooltip=tooltip).add_to(m),

# Circle marker
# folium.CircleMarker(
#    location=[42.466470, -70.942110],
#    radius=50,
#    popup='My Birthplace',
#    color='#428bca',
#    fill=True,
#    fill_color='#428bca'
# ).add_to(m)

# Geojson overlay
#folium.GeoJson(overlay, name='cambridge').add_to(m)

# Generate map
m.save('map.html')
