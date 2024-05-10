import geopandas as gpd
import matplotlib.pyplot as plt

# Load GeoJSON files for lines and points
lines_gdf = gpd.read_file('hotosm_egy_railways_lines_geojson.geojson')
points_gdf = gpd.read_file('hotosm_egy_railways_points_geojson.geojson')

# Plot the lines
lines_gdf.plot(ax=plt.gca(), color='blue')

# Plot the points
points_gdf.plot(ax=plt.gca(), color='red', markersize=50)

# Add station labels
for idx, row in points_gdf.iterrows():
    plt.text(row.geometry.x, row.geometry.y, row['station_name'], fontsize=10)

# Specify station 1 and station 2
station1 = points_gdf.iloc[0].geometry  # محطة الشلال
station2 = points_gdf.iloc[1].geometry  # محطة الأشراف

# Plot the journey from station 1 to station 2
plt.plot([station1.x, station2.x], [station1.y, station2.y], color='green', linestyle='--', linewidth=2)

# Add title and show plot
plt.title('Journey from {} to {}'.format(points_gdf.iloc[0]['station_name'], points_gdf.iloc[1]['station_name']))
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()
