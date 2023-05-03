from police_api import PoliceAPI
from police_api.forces import Force
from police_api.neighbourhoods import Neighbourhood
from police_api.crime import Crime
import pandas as pd
import json

api = PoliceAPI()

#Get the list of the neighbourhoods served
api.get_forces()
force = Force(api, id = 'hertfordshire')
ids = force.neighbourhoods
ids

#Get neighbourhood events
neighbourhood = Neighbourhood(api, force=force, id = 'E01')
neighbourhood.centre
Crime(api, id = 'hertfordshire')
