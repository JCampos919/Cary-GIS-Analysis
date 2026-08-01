import geopandas as gpd
import pandas as pd
import folium
from unicodedata import category

pd.set_option('display.max_columns', None)

# Load data
data = gpd.read_file(r"C:\SHAPEFILES\Cary\residential-boundaries\residential-boundaries.shp")
crime_csv = pd.read_csv(r"C:\SHAPEFILES\Cary\CARY_CRIME\cpd-incidents (4).csv")

crs = "EPSG:32617"
boundaries_proj = data.to_crs(epsg=32617)
boundaries_proj["centroid"] = boundaries_proj.geometry.centroid
boundaries_proj["name"] = boundaries_proj["name"].str.upper()


burglary = crime_csv[(crime_csv["Crime Type"] == "BURGLARY - FORCIBLE ENTRY") | (crime_csv["Crime Type"] == "BURGLARY - NON-FORCED ENTRY")]
burglary["Residential Subdivision"] = burglary["Residential Subdivision"].str.upper()


merged_data = boundaries_proj.merge(burglary, left_on="name", right_on="Residential Subdivision", how="inner")

print(len(merged_data))
print(merged_data.columns.tolist())

point = gpd.GeoDataFrame(merged_data, geometry="centroid", crs=crs)
reprojected_point = point.to_crs(epsg=4326)
reprojected_point = reprojected_point.drop(columns=["geometry"])

cary = folium.Map(location=[35.79, -78.78], zoom_start=12)

folium.GeoJson(
    reprojected_point,
    marker= folium.CircleMarker(
        radius=4,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.8),
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "Crime Type"],
        aliases=["Subdivision Name: ", "Incident Type: "]
    )).add_to(cary)

cary.save("subdivison-burglary-merge.html")


reprojected_point.to_file(r"C:\SHAPEFILES\Cary\Burglary_Crime_map.shp", driver="ESRI Shapefile")
