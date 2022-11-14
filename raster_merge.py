# %%
# MERGE
# run in geo_env

from rasterio.plot import show
from rasterio.merge import merge
import rasterio as rio
from pathlib import Path
import glob
import geopandas as gpd
import sys

#folder with dem tifs

in_dir = input("Input directory for raster merge: ")
#r"C:\Users\tfo46\OneDrive - University of Canterbury\Tara_PhD\c_PhD\c_Data\a_source\dem_data\nz_hawkes_bay_LiDAR\lds-hawkes-bay-lidar-1m-dem-2020-GTiff"

out_dir = input("Directory for raster merge (non-existent OK): ")
#r"C:\Users\tfo46\OneDrive - University of Canterbury\Tara_PhD\c_PhD\c_Data\a_source\dem_data\nz_hawkes_bay_LiDAR\1m_mosaic"

path = Path(in_dir)
Path(out_dir).mkdir(exist_ok=True)
output_path = os.path.join(out_dir, 'HBRC_dem_2020.tif')

all_files = in_dir + "/*.tif"
in_tifs = glob.glob(all_files)

raster2mosaic = []
in_tifs [:5]

#TODO# USE FOR INDEX TILES
#import list of index files to merge
#shp_path = r"C:\Users\tfo46\OneDrive - University of Canterbury\Tara_PhD\c_PhD\c_Data\b_derived\mod_model_files\base_v1_20220909\dem_index_tiles.shp"

#index_shp = gpd.read_file(shp_path)
#in_tifs = [os.path.join(in_dir, 'DEM_' + i[:4] +'_2020'+ i[4:] + '.tif') for i in index_shp['tilename']]

#TODO break up into blocks for memory processing

for p in in_tifs:
    raster = rio.open(p)
    raster2mosaic.append(raster)
#raster2mosaic[:5]

# merge rasters
mosaic, output = merge(raster2mosaic)

#copy and create the mosaic metadata
output_meta = raster.meta.copy()
output_meta.update(
    {"driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": output,
    }
)

#save raster to destination
with rio.open(output_path, 'w', **output_meta) as m:
    m.write(mosaic)


