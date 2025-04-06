import os
import ee
import geemap
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import random
import pandas as pd

ee.Initialize()

def generate_samples_and_download_images(
    shp_pol_path,
    shp_pt_path=None,
    n_samples_mining=100,
    n_samples_control=100,
    control_bbox=(-75, -10, -50, 5),
    dataset_dir="dataset",
    buffer_meters=256,
    scale=10
):
    os.makedirs(f"{dataset_dir}/mining", exist_ok=True)
    os.makedirs(f"{dataset_dir}/control", exist_ok=True)

    gdf_pol = gpd.read_file(shp_pol_path).to_crs("EPSG:4326")
    mining_points = []

    if shp_pt_path:
        gdf_pt = gpd.read_file(shp_pt_path).to_crs("EPSG:4326")
        mining_points += list(gdf_pt.geometry)

    def generate_points_within_polygons(gdf, n):
        points = []
        while len(points) < n:
            poly = gdf.sample(1).geometry.values[0]
            minx, miny, maxx, maxy = poly.bounds
            p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if poly.contains(p):
                points.append(p)
        return points

    remaining = max(0, n_samples_mining - len(mining_points))
    mining_points += generate_points_within_polygons(gdf_pol, remaining)
    gdf_mining = gpd.GeoDataFrame(geometry=mining_points, crs="EPSG:4326")
    gdf_mining["label"] = "mining"

    # Generate control points outside mining polygons
    minx, miny, maxx, maxy = control_bbox
    control_points = []
    while len(control_points) < n_samples_control:
        x = np.random.uniform(minx, maxx)
        y = np.random.uniform(miny, maxy)
        p = Point(x, y)
        if not gdf_pol.contains(p).any():
            control_points.append(p)

    gdf_control = gpd.GeoDataFrame(geometry=control_points, crs="EPSG:4326")
    gdf_control["label"] = "control"

    # Combine and clean up
    gdf_all = gpd.GeoDataFrame(pd.concat([gdf_mining, gdf_control], ignore_index=True))
    gdf_all = gdf_all[gdf_all.geometry.type == 'Point'].copy()
    gdf_all.reset_index(drop=True, inplace=True)

    def download_sentinel_patch(geometry, label, filename):
        lon, lat = geometry.x, geometry.y
        point = ee.Geometry.Point([lon, lat])
        image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(point) \
            .filterDate('2023-01-01', '2023-12-31') \
            .sort('CLOUD_COVER') \
            .first()
        region = point.buffer(buffer_meters).bounds()

        label_dir = label.strip().lower()
        path = os.path.join(dataset_dir, label_dir, filename)

        try:
            print(f"Saving to: {path}")
            geemap.download_ee_image(
                image=image.select(['B4', 'B3', 'B2']),
                region=region,
                filename=path,
                scale=scale,
                crs='EPSG:4326'
            )
            return True
        except Exception as e:
            print(f"Error saving {path}: {e}")
            return False

    counters = {'mining': 0, 'control': 0}
    limits = {'mining': n_samples_mining, 'control': n_samples_control}
    used_indices = set()

    for i, row in gdf_all.iterrows():
        label = row["label"]
        if counters[label] >= limits[label]:
            continue
        img_name = f"img_{counters[label]:04}.png"
        success = download_sentinel_patch(row.geometry, label, img_name)
        if success:
            counters[label] += 1
            used_indices.add(i)

        if all(counters[l] >= limits[l] for l in limits):
            break

    gdf_all = gdf_all.loc[list(used_indices)].reset_index(drop=True)
    print(f"\n✅ Samples saved: {counters}")
    print(f"📂 Folder: {dataset_dir}")
    return gdf_all
