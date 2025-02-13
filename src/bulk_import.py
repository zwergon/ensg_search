import json
import requests
from requests.auth import HTTPBasicAuth

# Configuration du serveur
ES_HOST = "https://localhost:9200"  # Change si nécessaire (https:// si SSL)
ES_INDEX = "mon_index"
ES_USERNAME = "admin"
ES_PASSWORD = "Osearch!2024"

# Fichier contenant les données bulk
BULK_FILE = "bulk_data.json"

# Vérification et chargement des données du fichier
try:
    with open(BULK_FILE, "r", encoding="utf-8") as file:
        bulk_data = file.read()
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    exit(1)

# URL de l'importation bulk
bulk_url = f"{ES_HOST}/_bulk"

# Envoi de la requête HTTP
headers = {"Content-Type": "application/json"}
auth = HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)

try:
    response = requests.post(bulk_url, data=bulk_data,
                             headers=headers, auth=auth)
    response.raise_for_status()  # Lève une erreur si HTTP >= 400
    print("Importation réussie !")
    print(response.json())  # Affiche la réponse JSON de l'ES
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de l'importation: {e}")
