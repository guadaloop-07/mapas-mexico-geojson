"""Construye los GeoJSON nacionales y estatales desde la capa AGEE de INEGI."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ENTITY_NAMES = {
    "01": "Aguascalientes",
    "02": "Baja California",
    "03": "Baja California Sur",
    "04": "Campeche",
    "05": "Coahuila",
    "06": "Colima",
    "07": "Chiapas",
    "08": "Chihuahua",
    "09": "Ciudad de México",
    "10": "Durango",
    "11": "Guanajuato",
    "12": "Guerrero",
    "13": "Hidalgo",
    "14": "Jalisco",
    "15": "Estado de México",
    "16": "Michoacán",
    "17": "Morelos",
    "18": "Nayarit",
    "19": "Nuevo León",
    "20": "Oaxaca",
    "21": "Puebla",
    "22": "Querétaro",
    "23": "Quintana Roo",
    "24": "San Luis Potosí",
    "25": "Sinaloa",
    "26": "Sonora",
    "27": "Tabasco",
    "28": "Tamaulipas",
    "29": "Tlaxcala",
    "30": "Veracruz",
    "31": "Yucatán",
    "32": "Zacatecas",
}


def load_source(path: Path) -> dict[str, Any]:
    """Carga y valida la estructura mínima de la capa oficial AGEE."""
    with path.open(encoding="utf-8") as source:
        collection = json.load(source)

    if collection.get("type") != "FeatureCollection":
        raise ValueError("La fuente debe ser un GeoJSON FeatureCollection.")
    features = collection.get("features")
    if not isinstance(features, list) or len(features) != len(ENTITY_NAMES):
        raise ValueError("La fuente debe contener exactamente 32 entidades.")

    codes: list[str] = []
    for feature in features:
        properties = feature.get("properties", {})
        code = properties.get("cve_ent")
        if code not in ENTITY_NAMES:
            raise ValueError(f"Clave de entidad no reconocida: {code}")
        if not properties.get("cvegeo") or not properties.get("nomgeo"):
            raise ValueError(f"Faltan atributos geográficos para la entidad {code}.")

        geometry = shape(feature.get("geometry"))
        if geometry.geom_type not in {"Polygon", "MultiPolygon"}:
            raise ValueError(f"La entidad {code} no tiene una geometría de área.")
        if geometry.is_empty or not geometry.is_valid:
            raise ValueError(f"La entidad {code} tiene una geometría inválida.")
        codes.append(code)

    if set(codes) != set(ENTITY_NAMES) or len(codes) != len(set(codes)):
        raise ValueError("Las claves deben cubrir una vez los valores 01 a 32.")
    return collection


def build_entities(collection: dict[str, Any], tolerance: float) -> dict[str, Any]:
    """Normaliza y simplifica las entidades sin alterar su topología interna."""
    features = []
    for feature in collection["features"]:
        properties = feature["properties"]
        code = properties["cve_ent"]
        geometry = shape(feature["geometry"])
        simplified = geometry.simplify(tolerance, preserve_topology=True)
        if simplified.is_empty or not simplified.is_valid:
            raise ValueError(f"La simplificación produjo una geometría inválida: {code}")
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "cve_ent": code,
                    "cvegeo": properties["cvegeo"],
                    "nombre_inegi": properties["nomgeo"],
                    "nombre_catalogo": ENTITY_NAMES[code],
                },
                "geometry": mapping(simplified),
            }
        )
    return {"type": "FeatureCollection", "features": features}


def build_outline(entities: dict[str, Any]) -> dict[str, Any]:
    """Une las entidades simplificadas en un contorno nacional sin divisiones."""
    outline = unary_union([shape(feature["geometry"]) for feature in entities["features"]])
    if outline.is_empty or not outline.is_valid:
        raise ValueError("La unión nacional produjo una geometría inválida.")
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"nombre": "México", "nivel": "nacional"},
                "geometry": mapping(outline),
            }
        ],
    }


def entity_filename(feature: dict[str, Any]) -> str:
    """Devuelve un nombre de archivo estable y legible para una entidad."""
    properties = feature["properties"]
    normalized = unicodedata.normalize("NFKD", properties["nombre_catalogo"])
    ascii_name = normalized.encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")
    return f"{properties['cve_ent']}-{slug}.geojson"


def build_entity_outlines(entities: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Separa las entidades en GeoJSON individuales sin límites internos."""
    outlines = {}
    for feature in sorted(entities["features"], key=lambda item: item["properties"]["cve_ent"]):
        outlines[entity_filename(feature)] = {
            "type": "FeatureCollection",
            "features": [feature],
        }
    return outlines


def write_geojson(path: Path, collection: dict[str, Any]) -> None:
    """Escribe GeoJSON compacto y UTF-8 para una distribución reproducible."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as output:
        json.dump(collection, output, ensure_ascii=False, separators=(",", ":"))
        output.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="GeoJSON AGEE oficial.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("nacional"),
        help="Directorio de los GeoJSON nacionales (predeterminado: nacional).",
    )
    parser.add_argument(
        "--entity-output-dir",
        type=Path,
        default=Path("entidades"),
        help="Directorio de los GeoJSON por entidad (predeterminado: entidades).",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.001,
        help="Tolerancia de simplificación en grados (predeterminado: 0.001).",
    )
    args = parser.parse_args()

    if args.tolerance <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    source_hash = hashlib.sha256(args.source.read_bytes()).hexdigest()
    print(f"SHA-256 de fuente: {source_hash}")
    collection = load_source(args.source)
    entities = build_entities(collection, args.tolerance)
    outline = build_outline(entities)
    entity_outlines = build_entity_outlines(entities)
    write_geojson(args.output_dir / "mexico-entidades.geojson", entities)
    write_geojson(args.output_dir / "mexico-contorno.geojson", outline)
    for filename, entity_outline in entity_outlines.items():
        write_geojson(args.entity_output_dir / filename, entity_outline)


if __name__ == "__main__":
    main()
