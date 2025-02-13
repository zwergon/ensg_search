"""
    Copyright © 2025 IFP Energies nouvelles (IFPEN), Rueil-Malmaison, France.
    This course material was created by IFP Energies nouvelles (IFPEN) and 
    is intended for educational purposes. Unauthorized reproduction, distribution, 
    or modification without explicit permission is prohibited.
"""
import os
import json
from datetime import datetime

if __name__ == "__main__":
    directory = os.path.join(os.path.dirname(__file__), "..", "data")
    in_file = os.path.join(directory, "campStationLocations.geojson")
    out_file = os.path.join(directory, "bulk_data.json")

    # Charger le fichier GeoJSON
    with open(in_file, "r") as file:
        geojson_data = json.load(file)

    # Créer le fichier bulk
    with open(out_file, "w") as bulk_file:
        for feature in geojson_data["features"]:
            # Préparer les données
            properties = feature["properties"]
            coordinates = feature["geometry"]["coordinates"]

            # Action metadata
            bulk_file.write(json.dumps(
                {"index": {"_index": "geo_data"}}) + "\n")

            dt = datetime.strptime(properties.get(
                "open_date"), '%d/%m/%Y %H:%M')

            # Document data
            document = {
                "stno": properties.get("stno"),
                "location": properties.get("location"),
                "county": properties.get("County"),
                "catchment": properties.get("catchment"),
                "river": properties.get("river"),
                "elevation": properties.get("elevation"),
                "open_date": dt.strftime('%Y-%m-%dT%H:%MZ'),
                "coordinates": {
                    "lat": coordinates[1],
                    "lon": coordinates[0]
                }
            }
            bulk_file.write(json.dumps(document) + "\n")
