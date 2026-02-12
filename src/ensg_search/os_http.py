"""
    Copyright © 2025 IFP Energies nouvelles (IFPEN), Rueil-Malmaison, France.
    This course material was created by IFP Energies nouvelles (IFPEN) and
    is intended for educational purposes. Unauthorized reproduction, distribution,
    or modification without explicit permission is prohibited.
"""
import json
import requests
from requests import Response
from requests.auth import HTTPBasicAuth
import os

from enum import IntEnum


class CmdType(IntEnum):
    GET = 0
    PUT = 1
    DELETE = 2
    POST = 3


def http_request(type: CmdType, cmd: str = "", body: dict = {}):

    host = os.getenv("OPENSEARCH_HOST")
    port = os.getenv("OPENSEARCH_PORT")
    user = os.getenv("OPENSEARCH_USER")
    password = os.getenv("OPENSEARCH_PW")
    ES_HOST = f"http://{host}:{port}/os"

    url = f"{ES_HOST}/{cmd}"
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(user, password)

    function = {
        CmdType.GET: requests.get,
        CmdType.PUT: requests.put,
        CmdType.DELETE: requests.delete,
        CmdType.POST: requests.post
    }[type]

    try:

        response: Response = function(url,
                                      data=json.dumps(body) if isinstance(
                                          body, dict) else body,
                                      headers=headers,
                                      auth=auth
                                      )
        response.raise_for_status()  # Lève une erreur si HTTP >= 400
        print(f"Requête '{url}' réussie !")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête '{cmd}': {e}")
        exit(1)

    return response.json()


def bulk(filename: str):

    cmd = "_bulk"

    # Vérification et chargement des données du fichier
    try:
        with open(filename, "r", encoding="utf-8") as file:
            bulk_data = file.read()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        exit(1)

    return http_request(CmdType.POST, cmd=cmd, body=bulk_data)


def compter(index: str):
    response = http_request(CmdType.GET, cmd=f"{index}/_count")
    return response.get("count", 0)


def mapping(index: str, body: dict):
    cmd = f"{index}"
    return http_request(CmdType.PUT, cmd=cmd, body={"mappings": body})


def search_all(index: str, size: int = 10):
    cmd = f"{index}/_search"
    body = {
        "query": {
            "match_all": {}
        },
        "size": size
    }
    return http_request(CmdType.POST, cmd=cmd, body=body)


def delete(index: str):
    cmd = f"{index}"
    return http_request(CmdType.DELETE, cmd=cmd)
