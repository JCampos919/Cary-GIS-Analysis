import geopandas as gpd
import pandas as pd
import folium
import os

# TODO: reproject shapefiles to new CRS

def load_and_reproject(file_path):
    data = gpd.read_file(file_path)
    reprojected_data = data.to_crs(epsg=32617)
    return reprojected_data

folder = r"C:\SHAPEFILES\Cary\CRS_32617"

cary_files = os.listdir(folder)

reprojected_files = {}
for file_name in cary_files:
    if file_name.endswith(".shp"):
        shape_file = file_name
        file_path = os.path.join(folder,file_name)
        reprojected_shp = load_and_reproject(file_path)
        key = file_name.replace(".shp", "")
        reprojected_files[key] = reprojected_shp

test_file = reprojected_files["streets_32617"]
total_rows = len(reprojected_files["streets_32617"].count())


# TODO: #### Summarize ######

def summarize_layer(file, name):
    print(f"Layer name: {name}")
    total_rows = len(file)
    print(f"Rows: {total_rows}")
    print(f"CRS: {file.crs}")
    print(f"Geometry: {file.geometry.geom_type.unique()[0]}")
    columns_list = file.columns
    print(f"Columns: {columns_list}")


# for name, gdf in reprojected_files.items():
#     summarize_layer(gdf, name)
#     print("---")


# TODO: # #### Summarize ######
# path = "C:\SHAPEFILES\Cary\"

for name, gdf in reprojected_files.items():
    output_folder = r"C:\SHAPEFILES\Cary\Automation_Script"
    layer_name = f"{name}.gpkg"
    file_path = os.path.join(output_folder, layer_name)
    gdf.to_file(file_path, driver="GPKG")




