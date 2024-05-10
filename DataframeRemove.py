import pandas as pd
import json as js

df = js.load(open("hotosm_egy_railways_points_geojson_copy.json"))
print(type(df))