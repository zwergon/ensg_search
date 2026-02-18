from pathlib import Path
import ensg_search.os_http as os_http
from dotenv import load_dotenv
if __name__ == "__main__":

    load_dotenv()
    root_path = Path(__file__).parent.parent

    os_http.delete("power_plant")

    os_http.mapping("power_plant",
                    {
                        "properties": {
                            "coordinates": {"type": "geo_point"}
                        }
                    })

    os_http.bulk(root_path / "data" / "reneweable_power_plants_bulk.json")
