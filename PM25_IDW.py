import os
import xarray as xr
import geopandas as gpd
import pandas as pd
import numpy as np
from rasterio.features import rasterize
from shapely.geometry import box
from tqdm import tqdm
from scipy.spatial import distance
from multiprocessing import Pool, cpu_count
from affine import Affine

def idw_interpolation(points, values, grid_x, grid_y, p=2):
    result = np.zeros((len(grid_y), len(grid_x)))
    for i, y in enumerate(grid_y):
        for j, x in enumerate(grid_x):
            point = np.array([x, y])
            distances = distance.cdist([point], points)[0]
            if np.min(distances) == 0:
                result[i, j] = values[np.argmin(distances)]
            else:
                weights = 1 / (distances ** p)
                weights /= np.sum(weights)
                result[i, j] = np.sum(weights * values)
    return result

def process_kabupaten(args):
    kabupaten, lats, lons, pm25_array, transform, month_id = args
    kabupaten_id = kabupaten["KDBBPS"]
    kabupaten_geom = kabupaten["geometry"]
    bounds = kabupaten_geom.bounds

    # rasterize with shape (rows, cols) = (lat, lon)
    mask = rasterize(
        [(kabupaten_geom, 1)],
        out_shape=(len(lats), len(lons)),
        transform=transform,
        fill=0,
        dtype=np.uint8
    )

    # mask output aligns with [y (rows), x (cols)] = [lat index, lon index]
    lat_indices, lon_indices = np.where(mask == 1)
    if len(lat_indices) == 0:
        return kabupaten_id, np.nan

    pm25_values = []
    lat_points, lon_points = [], []
    weighted_sum = 0
    total_area = 0
    cell_area = abs((lats[1] - lats[0]) * (lons[1] - lons[0]))  # sesuai resolusi

    for i, j in zip(lat_indices, lon_indices):
        # karena NetCDF biasanya [lat, lon], pastikan lats turun → indeks dibalik
        val = pm25_array[i, j]
        if not np.isnan(val):
            lat_points.append(lats[i])
            lon_points.append(lons[j])
            pm25_values.append(val)
            weighted_sum += val * cell_area
            total_area += cell_area

    weighted_avg = weighted_sum / total_area if total_area > 0 else np.nan

    if np.isnan(weighted_avg) and len(pm25_values) > 3:
        try:
            points = np.column_stack((lon_points, lat_points))
            grid_x = np.linspace(bounds[0], bounds[2], 100)
            grid_y = np.linspace(bounds[1], bounds[3], 100)
            interp = idw_interpolation(points, np.array(pm25_values), grid_x, grid_y)
            return kabupaten_id, np.nanmean(interp)
        except:
            return kabupaten_id, np.nan
    else:
        return kabupaten_id, weighted_avg

def monthly_pm25_data_indonesia(nc_file_path, kabupaten_gdf):
    filename = os.path.basename(nc_file_path)
    month_id = filename.split(".")[3].split("-")[0]
    print(f"Processing {month_id}...")

    ds = xr.open_dataset(nc_file_path)
    pm25 = ds['GWRPM25']
    lats = ds['lat'].values
    lons = ds['lon'].values

    # pastikan lats ascending (karena raster pakai dari atas ke bawah)
    if lats[0] > lats[-1]:
        lats = lats[::-1]
        pm25_array = np.flip(pm25.values, axis=0)
    else:
        pm25_array = pm25.values

    res_lon = lons[1] - lons[0]
    res_lat = lats[1] - lats[0]
    transform = Affine.translation(lons[0] - res_lon / 2, lats[0] - res_lat / 2) * Affine.scale(res_lon, res_lat)

    if kabupaten_gdf.crs != "EPSG:4326":
        kabupaten_gdf = kabupaten_gdf.to_crs("EPSG:4326")

    args_list = [
        (row, lats, lons, pm25_array, transform, month_id)
        for _, row in kabupaten_gdf.iterrows()
    ]

    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_kabupaten, args_list), total=len(args_list)))

    kab_pm25 = {k: v for k, v in results}
    return pd.Series(kab_pm25, name=f"pm{month_id}")

def process_pm25_all_month(nc_folder_path, kabupaten_gdb_path, output_csv_path):
    print("Loading kabupaten boundaries...")
    kabupaten_gdf = gpd.read_file(kabupaten_gdb_path)
    kabupaten_gdf = kabupaten_gdf[["KDBBPS", "WADMKK", "geometry"]]

    hasil = kabupaten_gdf.set_index("KDBBPS").copy()
    nc_files = [f for f in os.listdir(nc_folder_path) if f.endswith('.nc') and "V5GL0502.HybridPM25.Asia" in f]
    nc_files.sort()

    for f in nc_files:
        hasil_monthly = monthly_pm25_data_indonesia(os.path.join(nc_folder_path, f), kabupaten_gdf)
        hasil = hasil.join(hasil_monthly)

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    hasil = hasil.drop(columns="geometry", errors="ignore")
    hasil.reset_index().to_csv(output_csv_path, index=False)
    print("Finished.")

if __name__ == "__main__":
    nc_folder_path = "Data/PM2.5"
    kabupaten_gdb_path = "Data/RBI_Indonesia/RBI_PROV_KAB6.shp"
    output_csv_path = "Hasil/Hasil_PM25.csv"
    
    process_pm25_all_month(nc_folder_path, kabupaten_gdb_path, output_csv_path)
