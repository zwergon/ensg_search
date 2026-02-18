from pathlib import Path
import ensg_search.os_http as os_http
from dotenv import load_dotenv
if __name__ == "__main__":

    load_dotenv()
    root_path = Path(__file__).parent.parent

    os_http.delete("camp_stations")

    os_http.mapping("camp_stations",
                    mapping = {
                        "properties": {
                            "stno": {"type": "keyword"},
                            "location": {"type": "text"},
                            "county": {"type": "text"},
                            "doc_type": {"type": "keyword"},
                            "catchment": {"type": "text"},
                            "river": {"type": "text"},
                            "elevation": {"type": "integer"},
                            "open_date": {"type": "date"},
                            "coordinates": {"type": "geo_point"},
                            "time": {"type": "date"},
                            "station_to_observation": {
                                "type": "join",
                                "relations": {"station": "observation"}
                            },
                            "weather_vector": {
                                "type": "knn_vector",
                                "dimension": 2,
                                "method": {
                                    "name": "hnsw",
                                    "space_type": "l2",
                                    "engine": "nmslib"
                                }
                            }
                        }
                    },
                    setting = { 
                        "index": {
                            "knn": "true"
                            }
                        }
                    )

    os_http.bulk(root_path / "data" / "camp_stations.json")

    os_http.bulk(root_path / "data" / "pluv_bulk.json")
