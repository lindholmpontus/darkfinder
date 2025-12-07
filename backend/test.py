import rasterio

# Path to your file
raster = rasterio.open(r"data\SVDNB_npp_20240101-20241231_00N060E_vcmcfg_v10_c202402062300.cvg.tif")

print("Raster loaded!")
print("Width:", raster.width)
print("Height:", raster.height)
print("Bounds:", raster.bounds)
print("Coordinate reference system:", raster.crs)
