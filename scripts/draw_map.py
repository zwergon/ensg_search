from opensearchpy import OpenSearch

from ensg_search.os_client import get_opensearch_client

import matplotlib.cm as cm
import matplotlib.colors as mcolors

import folium
import math

query = {
    "size": 0,
    "query": {
        "term": {"doc_type": "station"}
    },
    "aggs": {
        "grid": {
            "geotile_grid": {
                "field": "coordinates",
                "precision": 10
            },
            "aggs": {
                "to_observations": {
                    "children": {
                        "type": "observation"
                    },
                    "aggs": {
                        "avg_rain": {
                            "avg": {
                                "field": "pluvio_mean"
                            }
                        }
                    }
                }
            }
        }
    }
}


# ------------------------
# Connexion OpenSearch
# ------------------------
client = get_opensearch_client()

response = client.search(
    index="camp_stations",
    body=query
)

buckets = response["aggregations"]["grid"]["buckets"]

# ------------------------
# Fonction conversion tuile → bbox
# ------------------------


def tile_bounds(tile_key):
    zoom, x, y = map(int, tile_key.split("/"))

    n = 2.0 ** zoom

    lon_min = x / n * 360.0 - 180.0
    lon_max = (x + 1) / n * 360.0 - 180.0

    lat_min_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n)))
    lat_max_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))

    lat_min = math.degrees(lat_min_rad)
    lat_max = math.degrees(lat_max_rad)

    return lat_min, lat_max, lon_min, lon_max


# ------------------------
# Création carte Folium
# ------------------------
m = folium.Map(location=[53, -8], zoom_start=6)


# ------------------------
# Normalisation couleur
# ------------------------
rain_values = [b["to_observations"]["avg_rain"]["value"]
               for b in buckets if b["to_observations"]["avg_rain"]["value"] is not None]

if rain_values:
    norm = mcolors.Normalize(vmin=min(rain_values), vmax=max(rain_values))
    cmap = cm.get_cmap("YlOrRd")  # Yellow → Red
else:
    norm = None


# ------------------------
# Ajout des rectangles
# ------------------------
for bucket in buckets:

    rain = bucket["to_observations"]["avg_rain"]["value"]

    if rain is None:
        continue

    lat_min, lat_max, lon_min, lon_max = tile_bounds(bucket["key"])

    # couleur selon matplotlib
    color_rgb = cmap(norm(rain))[:3]  # tuple (r,g,b)
    color_hex = mcolors.to_hex(color_rgb)

    folium.Rectangle(
        bounds=[[lat_min, lon_min], [lat_max, lon_max]],
        fill=True,
        color=None,
        fill_color=color_hex,
        fill_opacity=0.7,
        tooltip=f"Avg rain: {rain:.2f}"
    ).add_to(m)

# ------------------------
# Sauvegarde HTML
# ------------------------
m.save("rain_heatmap.html")

print("Carte générée : rain_heatmap.html")
