import rasterio as rio
import numpy as np
from rasterio.fill import fillnodata
from pathlib import Path, PurePath

#fills missing values by searching nearest cells
def fill_missing(ras_fn, out_dir, max_search=10):
    fn = Path(ras_fn).stem
    with rio.open(ras_fn) as src:
        arr_meta = src.meta
        arr = src.read(1)
        arr_filled = fillnodata(
            arr,
            mask=src.read_masks(1),
            max_search_distance=max_search
        )
    out_fn = PurePath(out_dir, f'{fn}_filled.tif')
    save_raster(arr_filled, out_fn, arr_meta)
    return out_fn

#save a raster
def save_raster(ras, ras_out, ras_meta):
    with rio.open(ras_out, 'w', **ras_meta) as m:
        m.write(ras)
        m.close()