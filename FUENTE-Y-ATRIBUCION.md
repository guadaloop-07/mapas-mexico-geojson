# Fuente y atribución

## Fuente original

- **Productor:** Instituto Nacional de Estadística y Geografía (INEGI).
- **Capa:** Áreas Geoestadísticas Estatales (AGEE), Marco Geoestadístico 2025.
- **Servicio de consulta:** <https://lcidsig.inegi.org.mx/server/rest/services/Hosted/Entidades_federativas_2025/FeatureServer/0/query>
- **Fecha de descarga:** 2026-08-14.
- **Formato de origen:** GeoJSON emitido por el servicio oficial.
- **SHA-256 del archivo fuente:** `195dc5f2b19da2ffc46f245d19a5a93cf305850e5829b2d6e38a09170dda708d`.

## Transformación

1. Se valida que la capa tenga exactamente las 32 entidades, claves `01` a `32`,
   atributos `cvegeo` y `nomgeo`, y geometrías de área válidas.
2. Cada polígono se simplifica con tolerancia de `0.001` grados, aproximadamente
   100 metros, preservando su topología.
3. El archivo de entidades conserva `cve_ent`, `cvegeo`, `nombre_inegi` y
   `nombre_catalogo`; este último normaliza nombres para uso editorial.
4. El contorno nacional se forma con la unión de las geometrías simplificadas, sin
   límites internos.
5. Cada entidad simplificada se distribuye también como un GeoJSON individual para
   facilitar su reutilización como contorno estatal.

Los productos derivados no incluyen colores, etiquetas, valores ni decisiones
editoriales.

## Límite de interpretación

Las AGEE son límites geoestadísticos. INEGI indica que se apegan, en la medida de
lo posible, a los límites político-administrativos; no deben presentarse como una
resolución jurídica de límites territoriales.
