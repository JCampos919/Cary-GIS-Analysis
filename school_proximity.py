import geopandas as gpd
import pandas as pd
import folium
from unicodedata import category

pd.set_option('display.max_columns', None)

# Load data
data = gpd.read_file(r"C:\SHAPEFILES\Cary\residential-boundaries\residential-boundaries.shp")
poi = gpd.read_file(r"C:\SHAPEFILES\Cary\points-of-interest\points-of-interest.shp")

# Filter to schools only
schools = poi[poi["featurecode"] == "Education Facility"]

# Reproject both to EPSG:32617 (meters)
boundaries_proj = data.to_crs(epsg=32617)
schools_proj = schools.to_crs(epsg=32617)

# Nearest neighbor spatial join
result = gpd.sjoin_nearest(boundaries_proj, schools_proj, distance_col="distance_to_school")

# Clean up columns
result_clean = result[["name_left", "category", "hoaactive", "name_right", "descript", "fulladdr", "distance_to_school"]]

# Rename columns
result_clean.rename(columns={"name_left": "subdivision_name", "name_right": "nearest_school"}, inplace=True)

# Export
result_clean.to_csv(r"C:\SHAPEFILES\Cary\nearest_school_results.csv", index=False)


distances = result_clean.sort_values(by ="distance_to_school", ascending=False).head(3)
furthest_distance = result_clean["distance_to_school"].max()


# reprojecting your projected layers back to EPSG:4326 and add boundaries_4326 as a GeoJson layer to your cary map
category_avg = result_clean.groupby("category")["distance_to_school"].mean()

cary = folium.Map(location=[35.79, -78.78], zoom_start=12)

schools_EPSG_4326 = schools_proj.to_crs(epsg=4326)
boundaries_ESPS_4326 = boundaries_proj.to_crs(epsg=4326)

folium.GeoJson(boundaries_ESPS_4326).add_to(cary)


# Rewrite  boundaries GeoJson line with a style_function and addedtooltip to your boundaries layer showing:  name — the subdivision name, category — housing type,  hoaactive — HOA status
folium.GeoJson(
    boundaries_ESPS_4326,
    style_function = lambda x:{
        "fillColor": "lightgrey",
        "color": "darkgrey",
        "weight": 1,
        "fillOpacity": 0.4
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "category", "hoaactive"],
        aliases=["Subdivision Name: ", "Residential Type: ", "HOA Status: "])
).add_to(cary)

# Rewrpte schoolsGeoJson line using CircleMarker to make schools stand out clearly against the grey boundaries.


folium.GeoJson(
    schools_EPSG_4326,
    marker= folium.CircleMarker(
        radius=4,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.8
    ),
    tooltip=folium.GeoJsonTooltip(fields=["name", "descript", "fulladdr"],
                                  aliases=["School Name: ", "School Type: ", "Address: "])
).add_to(cary)
