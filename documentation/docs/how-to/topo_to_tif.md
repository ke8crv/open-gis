#Topo Map PDF to Tif

[USTopo2GTIF](https://nationalmap.gov/ustopo/documents/ustopo2gtif_current.pdf)

Assume MN_Grand_Marais_20160511_TM_geo.pdf is the pdf you want to add to the GIS

```bash
gdalinfo MN_Grand_Marais_20160511_TM_geo.pdf --mdd LAYERS

```

Use the list of layers to use in the `GDAL_PDF_LAYERS` command

```bash
gdal_translate MN_Grand_Marais_20160511_TM_geo.pdf marais_contours.tif \
--config GDAL_PDF_LAYERS "Map_Frame.Terrain.Contours" --config GDAL_PDF_BANDS 3 \
--config GDAL_PDF_DPI 400
```