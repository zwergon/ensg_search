from opensearchpy import OpenSearch
import folium
from folium.plugins import HeatMap
import math
from ensg_search.os_client import get_opensearch_client

# ------------------------
# Connexion OpenSearch
# ------------------------
client = get_opensearch_client()


# ------------------------
# Requête geotile_grid + children
# ------------------------
query = {
    "size": 0,
    "query": {"term": {"doc_type": "station"}},
    "aggs": {
        "grid": {
            # plus précis
            "geotile_grid": {"field": "coordinates", "precision": 12},
            "aggs": {
                "to_observations": {
                    "children": {"type": "observation"},
                    "aggs": {"avg_rain": {"avg": {"field": "pluvio_mean"}}}
                }
            }
        }
    }
}

response = client.search(index="camp_stations", body=query)
buckets = response["aggregations"]["grid"]["buckets"]

# ------------------------
# Fonction conversion tuile → centre
# ------------------------


def tile_center(tile_key):
    zoom, x, y = map(int, tile_key.split("/"))
    n = 2.0 ** zoom
    lon = (x + 0.5) / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y + 0.5) / n)))
    lat = math.degrees(lat_rad)
    return lat, lon


# ------------------------
# Création carte Folium
# ------------------------
m = folium.Map(location=[53, -8], zoom_start=6)

# ------------------------
# Préparer les points pour HeatMap
# ------------------------
heat_data = []

for bucket in buckets:
    rain = bucket["to_observations"]["avg_rain"]["value"]
    if rain is None:
        continue
    lat, lon = tile_center(bucket["key"])
    heat_data.append([lat, lon, rain])  # [lat, lon, poids]

# ------------------------
# Ajouter HeatMap
# ------------------------
HeatMap(
    heat_data,
    radius=25,        # rayon des points
    max_zoom=10,      # quand le zoom change, recalcul
    blur=15,
    min_opacity=0.4,
    max_val=max([r[2] for r in heat_data])
).add_to(m)

# ------------------------
# Sauvegarde
# ------------------------
m.save("rain_heatmap_dynamic.html")
print("Carte générée : rain_heatmap_dynamic.html")
