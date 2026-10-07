# Mapas de México en GeoJSON

GeoJSON reutilizables de México, basados en el Marco Geoestadístico 2025 de INEGI.

El repositorio reúne geometrías nacionales y estatales simplificadas para
visualización, análisis y generación de imágenes asistida por IA.

## Recursos

| Recurso | Contenido |
| --- | --- |
| [`nacional/mexico-contorno.geojson`](nacional/mexico-contorno.geojson) | Silueta de México sin divisiones ni trazos internos. Conserva costa e islas. |
| [`nacional/mexico-entidades.geojson`](nacional/mexico-entidades.geojson) | Mapa de México con las 32 entidades federativas. |
| [`entidades/`](entidades/) | 32 archivos: un contorno por entidad federativa. |

Todos los archivos son GeoJSON `FeatureCollection` y usan coordenadas geográficas
WGS 84.

## Atributos

El mapa nacional con entidades y cada archivo individual incluyen:

| Campo | Descripción |
| --- | --- |
| `cve_ent` | Clave geoestadística estatal de dos dígitos. |
| `cvegeo` | Clave geográfica original de INEGI. |
| `nombre_inegi` | Nombre oficial de la entidad en INEGI. |
| `nombre_catalogo` | Nombre normalizado para uso editorial. |

## Uso

Puedes descargar y reutilizar los archivos en herramientas cartográficas,
visualizaciones, proyectos web o como archivos de referencia en chats que generen
imágenes.

Los archivos están simplificados para facilitar su uso visual. Si necesitas
precisión jurídica, técnica o de escala local, consulta directamente la fuente
oficial.

## Fuente y atribución

Los archivos derivan de las Áreas Geoestadísticas Estatales del Marco
Geoestadístico 2025 de INEGI.

Crédito sugerido:

> Fuente: INEGI, Marco Geoestadístico 2025. Versión simplificada por Mapas de
> México en GeoJSON.

Consulta el detalle de la fuente, transformación y alcance en
[FUENTE-Y-ATRIBUCION.md](FUENTE-Y-ATRIBUCION.md). Los datos están sujetos a los
[Términos de Libre Uso de la Información del INEGI](https://www.inegi.org.mx/inegi/terminos.html).

## Reproducibilidad

El script [`scripts/build_national_maps.py`](scripts/build_national_maps.py) genera
los recursos a partir de la capa oficial de INEGI.

```bash
python scripts/build_national_maps.py --source ruta/al/geojson-oficial.geojson
```

## Licencia

El código y la documentación originales se distribuyen bajo licencia MIT. Los
GeoJSON derivados se rigen por los términos aplicables de INEGI, descritos en
[LICENSE-DATA.md](LICENSE-DATA.md).
