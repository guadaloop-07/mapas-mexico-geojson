# Mapas de México en GeoJSON

GeoJSON reutilizables de México, basados en el Marco Geoestadístico de INEGI.

## Recursos disponibles

| Archivo | Contenido |
| --- | --- |
| [`nacional/mexico-contorno.geojson`](nacional/mexico-contorno.geojson) | Silueta nacional sin divisiones internas. |
| [`nacional/mexico-entidades.geojson`](nacional/mexico-entidades.geojson) | Las 32 entidades federativas, con claves y nombres. |

Los archivos son GeoJSON `FeatureCollection` y sus coordenadas siguen la convención
WGS 84 del formato GeoJSON. El contorno nacional contiene una sola entidad; el mapa
de entidades conserva `cve_ent`, `cvegeo`, `nombre_inegi` y `nombre_catalogo`.

## Alcance

Las geometrías son una versión simplificada del Marco Geoestadístico 2025 de INEGI
para facilitar su reutilización. Son límites geoestadísticos: no constituyen una
resolución jurídica de límites territoriales.

Consulta [la fuente y el método de procesamiento](FUENTE-Y-ATRIBUCION.md) y los
[términos aplicables a los datos](LICENSE-DATA.md) antes de redistribuirlos.

## Reproducibilidad

El generador está en [`scripts/build_national_maps.py`](scripts/build_national_maps.py).
Con Python 3 y las dependencias de `requirements.txt`, se ejecuta así:

```bash
python scripts/build_national_maps.py --source ruta/al/geojson-oficial.geojson
```

El comando vuelve a generar los dos archivos en `nacional/`.
