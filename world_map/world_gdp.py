"""
Similar example as the following file, but about the GDP by countries.
https://github.com/wang-qs/ForChildren/blob/master/world_map/world_population.py
"""
import json
from pygal.maps.world import World
from pygal_maps_world.i18n import COUNTRIES
from pygal.style import RotateStyle as RS, LightColorizedStyle as LCS

def get_country_code(country_name):
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    return None

# Download from:  https://datahub.io/core/gdp
filename = 'gdp_json.json'

with open(filename) as f:
    pop_data = json.load(f)

gdps = {}
cc_gdps_1,cc_gdps_2, cc_gdps_3,cc_gdps_4,cc_gdps_5, cc_gdps_6, = {},{},{},{},{},{}

for pop_dict in pop_data:
    year = int(pop_dict['Year'])
    if year == 2016:
        country_name = pop_dict['Country Name']
        value = int(float(pop_dict['Value']))

        code = get_country_code(country_name)
        if code:
            gdps[code] = value
        else:
            pass


for cc, gdp in gdps.items():
    if   gdp < 1000000000:
        cc_gdps_1[cc]=gdp
    elif gdp < 10000000000:
        cc_gdps_2[cc]=gdp
    elif gdp < 100000000000:
        cc_gdps_3[cc]=gdp
    elif gdp < 1000000000000:
        cc_gdps_4[cc]=gdp
    elif gdp < 10000000000000:
        cc_gdps_5[cc]=gdp
    else:
        cc_gdps_6[cc]=gdp

#wm_style = RS('#336699')
#wm_style = LCS
wm_style = RS('#336699',base_style=LCS)

wm = World(style=wm_style)
wm.title = 'World GDP in 2016, by Country'
#wm.add('2010',cc_population)
wm.add('6th, 0 - 10 b',cc_gdps_1)
wm.add('5th, < 100 b',cc_gdps_2)
wm.add('4th, < 1000 b',cc_gdps_3)
wm.add('3rd, < 10000 b',cc_gdps_4)
wm.add('2nd, < 100000 b',cc_gdps_5)
wm.add('1st, > 100000 b',cc_gdps_6)


wm.render_to_file('world_gdp.svg')
