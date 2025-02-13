# ENSG Opensearch lessons

<<<<<<< HEAD

This is main branch for session 1
=======
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
 PUT /power_plant 
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 2
  },
  "mappings": {
    "properties": {
      "coordinates": { "type": "geo_point" }
    }
  }
}
 ```

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

```
PUT /pluvio 
{
   "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
  ,
  "mappings": {
    "properties": {
      "stno": { "type": "integer" },
      "time": { "type": "date" }
    }
  }
}

```

# CRUD operation

insert a document from a json file with document id 
```
 curl -X PUT "https://localhost:9200/power_plant/_doc/1" -H "Content-Type: application/json" -d @power_plant_0.json -ku admin:$OPENSEARCH_INITIAL_ADMIN_PASSWORD
 ```

 without document_id

 ```
 curl -X POST "https://localhost:9200/power_plant/_doc/" -H "Content-Type: application/json" -d @power_plant_0.json -ku admin:$OPENSEARCH_INITIAL_ADMIN_PASSWORD
 ```

 # Request



 ```
GET /power_plant/_search?size=2
 ```
 L'API _analyze permet de voir comment un champ est transformé en tokens lors de l'indexation.
 ```
GET /power_plant/_analyze
{
  "field": "municipality.keyword",
  "text": "Arbois"
}


L'API _termvectors permet de voir les termes réellement stockés dans l'index inversé pour un document donné.
 ```
GET /power_plant/_termvectors/2
{
  "fields": ["municipality"],
  "offsets": true,
  "positions": true,
  "term_statistics": true
}
 ```


 ```

 ```
 GET power_plant/_search
{
  "size": 2, 
  "query": {
    "bool": {
      "must_not": {
        "match": { "municipality": "Arbois" }  
      },
      "filter": {
        "geo_distance": {
          "distance": "100km",  
          "coordinates": {
            "lat": 46.8944494212,
            "lon": 5.77331567443
          }
        }
      }
    }
  },
  "sort": [
    {
      "_geo_distance": {
        "coordinates": {
          "lat": 46.8944494212,
          "lon": 5.77331567443
        },
        "order": "asc",
        "unit": "km"
      }
    }
  ]
}
 ```


On a une table avec les lieux des stations, une table avec la pluviométrie.
```
SELECT p.time, p.temperature
FROM pluvio p
JOIN geo_camp g ON p.stno = g.stno
WHERE g.location = 'GLENVEAGH NATIONAL PARK'
AND p.time BETWEEN '2025-02-05 00:00:00' AND '2025-02-05 23:59:59'
ORDER BY p.time;
```

Les jointures ne sont possibles dans Opensearch, obligé de scinder en deux la requête.

```
GET /geo_camp/_search
{
  "query": {
    "match": {
      "location": "GLENVEAGH NATIONAL PARK"
    }
  }
}
```

```
GET /pluvio/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "stno": 8185 } },
        {
          "range": {
            "time": {
              "gte": "2025-02-05T00:00:00Z",
              "lte": "2025-02-05T23:59:59Z"
            }
          }
        }
      ]
    }
  }
}
```
>>>>>>> origin/end
