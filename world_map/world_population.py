import json
from pygal.maps.world import World
from pygal_maps_world.i18n import COUNTRIES
from pygal.style import RotateStyle as RS, LightColorizedStyle as LCS

"""
This example is from the book "Python Crash Course". Here are related URLs
- https://nostarch.com/pythoncrashcourse
- https://github.com/ehmatthes/pcc
- https://github.com/ehmatthes/pcc/blob/master/chapter_16/world_population.py
- https://github.com/ehmatthes/pcc/blob/master/chapter_16/population_data.json
"""

def get_country_code(country_name):
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    return None

filename = 'population_data.json'
cc_population = {}
cc_pops_1,cc_pops_2, cc_pops_3 = {},{},{}

with open(filename) as f:
    pop_data = json.load(f)

for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        code = get_country_code(country_name)
        if code:
            cc_population[code] = population
        else:
            pass


for cc, pop in cc_population.items():
    if pop < 10000000:
        cc_pops_1[cc]=pop
    elif pop < 1000000000:
        cc_pops_2[cc]=pop
    else:
        cc_pops_3[cc]=pop

#wm_style = RotateStyle('#336699')
#wm_style = LightColorizedStyle
wm_style = RS('#336699',base_style=LCS)

wm = World(style=wm_style)
wm.title = 'World population in 2010, by Country'
#wm.add('2010',cc_population)
wm.add('0-10m',cc_pops_1)
wm.add('10m-1b',cc_pops_2)
wm.add('>1b',cc_pops_3)

wm.render_to_file('world_population.svg')
