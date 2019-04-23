"""
Introduction:
The idea is from the following URLs. But when I followed the guide in below URLs, I got some errors.
This file is a working version, which will highlight all the airports all over the world in the map.
    -  https://www.dataquest.io/blog/python-data-visualization-libraries/
    -  http://openflights.org/data.html
    -  https://github.com/jpatokal/openflights/tree/master/data   (Need to rename the downloaded .dat file to csv.)
"""
import re
import pandas
import os.path
import time
import folium
import sys

"""
The purpose of the following code is to solve the following error while using the utf-8 airport name.
    - UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 8: ordinal not in range(128)
    - https://stackoverflow.com/questions/10406135/unicodedecodeerror-ascii-codec-cant-decode-byte-0xd1-in-position-2-ordinal
"""
# reload(sys)
# sys.setdefaultencoding('utf-8')


"""
Part 01:  Exploring the dataset
"""
# Read in the airports data.
airports = pandas.read_csv("airports.csv", header=None, dtype=str)
# wang-qs, edited.
#airports.columns = ["id", "name", "city", "country", "code", "icao", "latitude", "longitude", "altitude", "offset", "dst", "timezone"]
airports.columns = ["id", "name", "city", "country", "code", "icao", "latitude", "longitude", "altitude", "offset", "dst", "timezone","airport","OurAirports"]
# Read in the airlines data.
airlines = pandas.read_csv("airlines.csv", header=None, dtype=str)
airlines.columns = ["id", "name", "alias", "iata", "icao", "callsign", "country", "active"]
# Read in the routes data.
routes = pandas.read_csv("routes.csv", header=None, dtype=str)
routes.columns = ["airline", "airline_id", "source", "source_id", "dest", "dest_id", "codeshare", "stops", "equipment"]
# This line ensures that we have only numeric data in the airline_id column.
routes = routes[routes["airline_id"] != "\\N"]

print("======================================")
print(airports.head())
print("======================================")
print(airlines.head())
print("======================================")
print(routes.head())
print("======================================")


print("Start to create airport world map. " + str(time.asctime()))
# Get a basic world map.
airports_map = folium.Map(location=[30, 0],
                          world_copy_jump=True,
                          no_wrap=False,
                          zoom_start=2)

folium.Circle([38.935928, 121.517520],
                    radius=1000,
                    popup='Guess! Where it is?',
                    color='#3186cc',
                    fill=True,
                    fill_color='#3186cc',
                   ).add_to(airports_map)

folium.Marker([38.935928, 121.517520],
              popup='Dalian Zhoushuizi Airport'
             ).add_to(airports_map)

loop = 0
# Draw markers on the map.
for name, row in airports.iterrows():
    loop = loop +1
    if loop > 50:
        pass  # While testing, maybe you would like to break the for loop here.

    # For some reason, this one airport causes issues with the map.
    #if row["name"] != "South Pole Station":
    if row["name"] != "South Pole Station Airport":
        temp_latitude = float(row["latitude"])
        temp_longitude = float(row["longitude"])
        temp_name = row["name"]
        print("Loop " + str(loop) + " : Original name is =>" + temp_name)
        # Without the line below, the html will be blank, and the map will not be shown.
        temp_name = re.sub("[^a-zA-Z0-9\s]+", "", temp_name)
        print("\tNew airport name to display: " +temp_name)
        folium.Circle(location=[temp_latitude, temp_longitude],
                          radius=1000,
                          popup=temp_name,
                          color='#cc1a1a',
                          fill=True,
                          fill_color='#cc1a1a',
                      ).add_to(airports_map)

# Create and show the map.
#airports_map.save(os.path.join('results', 'airports.html'))
airports_map.save(os.path.join('.', 'airports.html'))
print("Airport world map is completed. " + str(time.asctime()))

