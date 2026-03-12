import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("../Tippecc/data/aoi/Integrated_Vaal_basins_UTM35S/Integrated_Vaal_basins_proj_UTM35S.shp")
gdf = gdf.to_crs(epsg=4326)  # Reproject to WGS84 (EPSG:4326)

fig, ax = plt.subplots(
    ncols=2,
    figsize=(15, 8),
    # sharex=True
)

gdf.plot(ax=ax[0], color='blue', edgecolor='black')

ax[0].set_title("Integrated Vaal Basins")
ax[0].set_xlabel("Longitude")
ax[0].set_ylabel("Latitude")

gdf = gpd.read_file("../Tippecc/data/aoi/Kunene_aoi_UTM33S/Kunene_aoi_UTM33S.shp")
gdf = gdf.to_crs(epsg=4326)  # Reproject to WGS84 (EPSG:4326)
gdf.plot(ax=ax[1], color='red', edgecolor='black')

ax[1].set_title("Kunene AOI")
ax[1].set_xlabel("Longitude")
ax[1].set_ylabel("Latitude")

plt.tight_layout()
plt.show()
