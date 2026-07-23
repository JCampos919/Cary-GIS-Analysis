# Imported modules that aided in project
import pandas
import geopandas as gpd
import pandas as pd
import folium

# Pandas method to display all rows when called
pd.set_option('display.max_columns', None)

# Subdivision data used to perform analysis and create map
residential_boundaries_data = gpd.read_file(r"C:\SHAPEFILES\Cary\residential-boundaries\residential-boundaries.shp")

# Loaded in crime data
pd = pandas
crime_csv = pd.read_csv(r"C:\SHAPEFILES\Cary\CARY_CRIME\cpd-incidents (4).csv")

# below is the name of the burglary for crime_type in crime_csv
forced_burglary = crime_csv[crime_csv["Crime Type"]==["BURGLARY - FORCIBLE ENTRY"]]
unforced_burglary = crime_csv[crime_csv["Crime Type"]==["BURGLARY - NON-FORCIBLE ENTRY"]]


# Both burglary names merged together under one single variable
burglary = crime_csv[(crime_csv["Crime Type"] == "BURGLARY - FORCIBLE ENTRY") | (crime_csv["Crime Type"] == "BURGLARY - NON-FORCED ENTRY")]

# Updated subdivision names in residential_boundaries_data to upper case to match for merge
residential_boundaries_data["name"] = residential_boundaries_data["name"].str.upper()

# Obtain count for total number of burglaries for each subdivision instead of displaying "burglary" as crime type
# Will now show integer value instead
burglary_counts = burglary.groupby("Residential Subdivision")["Crime Type"].count()

# Converts "Residential Subdivision" from a row index back into a standard column,
burglary_counts = burglary_counts.reset_index()

# Updated subdivision names in burglary_counts to upper case to match for merge
burglary_counts["Residential Subdivision"] = burglary_counts["Residential Subdivision"].str.upper()


# left merge for residential_boundaries and burglary_count to show subdivision and crime type as numbered count
all_subdivision_crime_count = residential_boundaries_data.merge(burglary_counts, left_on="name", right_on="Residential Subdivision", how="left")
all_subdivision_crime_count.rename(columns={"Crime Type": "burglary_count"}, inplace=True)

# Replaced missing subdivison crime data with int value of 0
all_subdivision_crime_count["burglary_count"] = all_subdivision_crime_count["burglary_count"].fillna(0)
all_subdivision_crime_count["burglary_count"] = all_subdivision_crime_count["burglary_count"].astype(int)

########## Folium Choropleth #####
# Using folium module to create interactive map on OSM
burglary_map = folium.Map(location=[35.79, -78.78], zoom_start=12, tiles="CartoDB positron")

# Choropleth call to assign color to subdivisions with burlary counts
folium.Choropleth(
    geo_data=all_subdivision_crime_count,
    data=all_subdivision_crime_count,
    columns=["name", "burglary_count"],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity= 0.4,
    line_opacity=0.4,
    legend_name="Burglaries in Subdivisons"
).add_to(burglary_map)


# Updated basemap color to keep it from distracting from subdivision findings
# Tool tip used to update interactive labels on OSM for better understanding
folium.GeoJson(
    all_subdivision_crime_count,
    style_function=lambda  x: {
        "fillColor":"transparent",
        "color": "transparent"
    },
    tooltip = folium.GeoJsonTooltip(
        fields = ["name","burglary_count"],
        aliases = ["Subdivision Name", "Number of Burglaries"]
    )
).add_to(burglary_map)

burglary_map.save("burglary_map.html")
