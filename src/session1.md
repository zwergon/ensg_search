
# Installing OpenSearch 

## with Docker Compose

1. Install Docker using Snap on Ubuntu
1. (Optional) Add yourself to the [Docker group](https://docs.docker.com/engine/install/linux-postinstall/)
1. Modify the  [Linux Settings](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/) 
1. Set a password and create the .env file
1. Create Docker volumes using docker volume create
1. Run the script with docker compose up -d


## With Bonsai

[Managed Service](https://bonsai.io/) for free. Some limitation but usefull


# Install a python environment 

Some module are required (see `requirements.txt`)

1. Use the python available on your laptop. 
1. Use google collab or whatever you want. 



# curl equivalent on Windows

```
src\os_get.ps1 -Uri "https://ensg-search-9642476797.eu-central-1.bonsaisearch.net:443/_cat/nodes?v" -Username "kpwoipavhb" -Password "9nys3us285"

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
