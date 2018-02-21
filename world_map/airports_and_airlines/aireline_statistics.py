"""
Introduction:
The idea is from the following URLs. But when I followed the guide in below URLs, I got some small errors.
This file is a working version, which will visualize the airline statistics.
    -  https://www.dataquest.io/blog/python-data-visualization-libraries/
    -  http://openflights.org/data.html
    -  https://github.com/jpatokal/openflights/tree/master/data   (Need to rename the downloaded .dat file to csv.)
"""
import pandas
import math
import matplotlib.pyplot as plt
import numpy
import time
import seaborn
import pygal
from IPython.display import SVG


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




"""
Part 02:  Making a histogram
"""
def haversine(lon1, lat1, lon2, lat2):
    """
    https://www.geovista.psu.edu/grants/MapStatsKids/MSK_portal/concepts_latlg.html
    http://www.learner.org/jnorth/tm/LongitudeIntro.html
    """
    # Convert coordinates to floats.
    lon1, lat1, lon2, lat2 = [float(lon1), float(lat1), float(lon2), float(lat2)]
    # Convert to radians from degrees.
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # Compute distance.
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km

def calc_dist(row):
    dist = 0
    try:
        # Match source and destination to get coordinates.
        source = airports[airports["id"] == row["source_id"]].iloc[0]
        dest = airports[airports["id"] == row["dest_id"]].iloc[0]
        # Use coordinates to compute distance.
        dist = haversine(dest["longitude"], dest["latitude"], source["longitude"], source["latitude"])
    except (ValueError, IndexError):
        pass
    return dist

print("start to caculate distance. " + str(time.asctime()))
route_lengths = routes.apply(calc_dist, axis=1)
print("caculate distance finished. " + str(time.asctime()))
print(route_lengths.head())
print("======================================")


print("start to plt.  " + str(time.asctime()) )
# https://gist.github.com/smidm/d26d34946af1f59446f0
fig_manager = plt.get_current_fig_manager()
if hasattr(fig_manager, 'window'):
    fig_manager.window.showMaximized()
# %matplotlib inline
plt.hist(route_lengths, bins=20)
plt.show()
print("plt finished.  " + str(time.asctime()) )

"""
Part 03:  Using Seaborn
"""
seaborn.distplot(route_lengths, bins=20)
fig_manager = plt.get_current_fig_manager()
if hasattr(fig_manager, 'window'):
    fig_manager.window.showMaximized()
plt.show()

"""
Part 04:  Bar charts
"""
# Put relevant columns into a dataframe.
route_length_df = pandas.DataFrame({"length": route_lengths, "id": routes["airline_id"]})
# Compute the mean route length per airline.
airline_route_lengths = route_length_df.groupby("id").aggregate(numpy.mean)
# Sort by length so we can make a better chart.
#   -   https://stackoverflow.com/questions/44123874/dataframe-object-has-no-attribute-sort
#   -   http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html
# airline_route_lengths = airline_route_lengths.sort("length", ascending=False)
airline_route_lengths = airline_route_lengths.sort_values("length", ascending=False)

plt.bar(range(airline_route_lengths.shape[0]), airline_route_lengths["length"])

fig_manager = plt.get_current_fig_manager()
if hasattr(fig_manager, 'window'):
    fig_manager.window.showMaximized()
plt.show()


def lookup_name(row):
    try:
        # Match the row id to the id in the airlines dataframe so we can get the name.
        name = airlines["name"][airlines["id"] == row["id"]].iloc[0]
    except (ValueError, IndexError):
        name = ""
    return name

# Add the index (the airline ids) as a column.
airline_route_lengths["id"] = airline_route_lengths.index.copy()
# Find all the airline names.
airline_route_lengths["name"] = airline_route_lengths.apply(lookup_name, axis=1)
# Remove duplicate values in the index.
airline_route_lengths.index = range(airline_route_lengths.shape[0])

"""
Fix me here. 
The following code does not work now because the reason in the following URLs. Need to be fixed.
# https://stackoverflow.com/questions/46486865/bokeh-doesnt-find-bar-chart-modules-on-raspberry-pi
# https://bokeh.github.io/blog/2017/6/13/release-0-12-6/
# http://holoviews.org
# https://github.com/bokeh/bkcharts
# from bkcharts import Bar, show
"""
# output_notebook()
# p = Bar(airline_route_lengths, 'name', values='length', title="Average airline route lengths")
# show(p)

"""
Part 05:  Horizontal bar charts
"""
long_routes = len([k for k in route_lengths if k > 10000]) / len(route_lengths)
medium_routes = len([k for k in route_lengths if k < 10000 and k > 2000]) / len(route_lengths)
short_routes = len([k for k in route_lengths if k < 2000]) / len(route_lengths)

chart = pygal.HorizontalBar()
chart.title = 'Long, medium, and short routes'
chart.add('Long', long_routes * 100)
chart.add('Medium', medium_routes * 100)
chart.add('Short', short_routes * 100)
chart.render_to_file('routes.svg')
SVG(filename='routes.svg')


"""
Part 06:  Scatter plots
"""
name_lengths = airlines["name"].apply(lambda x: len(str(x)))
plt.scatter(airlines["id"].astype(int), name_lengths)
fig_manager = plt.get_current_fig_manager()
if hasattr(fig_manager, 'window'):
    fig_manager.window.showMaximized()
plt.show()

data = pandas.DataFrame({"lengths": name_lengths, "ids": airlines["id"].astype(int)})
seaborn.jointplot(x="ids", y="lengths", data=data)
fig_manager = plt.get_current_fig_manager()
if hasattr(fig_manager, 'window'):
    fig_manager.window.showMaximized()
plt.show()

