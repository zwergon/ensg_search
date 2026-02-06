import os
import base64
import re
import logging
from opensearchpy import OpenSearch, RequestsHttpConnection
from dotenv import load_dotenv
from requests.auth import _basic_auth_str


def get_opensearch_client():
    # Chargement des variables d'environnement à partir du fichier .env
    load_dotenv()

    # Log transport details (optional):
    logging.basicConfig(level=logging.INFO)

    config = {
        'hosts': [{
            "host": os.getenv("OPENSEARCH_HOST"),
            "port": int(os.getenv("OPENSEARCH_PORT"))
        }],

        "http_auth": (
            os.getenv('OPENSEARCH_USER'),
            os.getenv('OPENSEARCH_PW')
        ),
        "connection_class": RequestsHttpConnection
    }
    url_prefix = os.getenv("OPENSEARCH_PREFIX")
    if url_prefix is not None:
        config['url_prefix'] = url_prefix

    proxy = os.getenv("OPENSEARCH_PROXY")
    if proxy is not None:
        config['proxies'] = {"http": proxy, "https": proxy}

    # print(_basic_auth_str(config['http_auth'][0], config['http_auth'][1]))

    return OpenSearch(**config)


if __name__ == "__main__":
    # Utilisation de la méthode pour obtenir le client
    client = get_opensearch_client()

    print(client.info())
