# ENSG Opensearch lessons

## Installation Opensearch à partir du Docker Compose

1. Installation de docker avec snap sur ubuntu
1. S'ajouter au [group docker](https://docs.docker.com/engine/install/linux-postinstall/)
1. Modification des [Linux Settings](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/) 
1. Définition d'un mot de passe et création du fichier `.env`
1. Création des volumes dockers `docker volume create`
1. On lance le script `docker compose up -d`



# curl equivalent on Windows

```
src\os_get.ps1 -Uri "https://ensg-search-9642476797.eu-central-1.bonsaisearch.net:443/_cat/nodes?v" -Username "kpwoipavhb" -Password "9nys3us285"

```


# Creation de l'index avec quelques settings


```
PUT /geo_data
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "stno": { "type": "integer" },
      "location": { "type": "text" },
      "county": { "type": "text" },
      "catchment": { "type": "text" },
      "river": { "type": "text" },
      "elevation": { "type": "integer" },
      "open_date": { "type": "date" },
      "coordinates": { "type": "geo_point" }
    }
  }
}
```

