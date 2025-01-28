# ENSG Opensearch lessons



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

