"""
    Copyright © 2025 IFP Energies nouvelles (IFPEN), Rueil-Malmaison, France.
    This course material was created by IFP Energies nouvelles (IFPEN) and 
    is intended for educational purposes. Unauthorized reproduction, distribution, 
    or modification without explicit permission is prohibited.
"""
import os
import json
import pandas as pd
from datetime import datetime


columns = [
    "TIMESTAMP",
    "RECORD",
    "StationName",
    "PluvioIntensityRT",
    "PluvioAccRT_NRT",
    "PluvioAccNRT",
    "PluvioAccTotalNRT",
    "PluvioBucketRT",
    "PluvioBucketNRT",
    "PluvioLoadCellTemp",
    "PluvioHeatingStatus",
    "PluvioStatus"
]

pluv_index = "pluvio"


def to_bulk(root_path, out_file, n_files=100):

    with open(out_file, "w") as bulk_file:

        for i, f in enumerate(os.listdir(root_path)):
            if n_files is not None and i + 1 > n_files:
                return
            if ".CR3" in f:
                df = pd.read_csv(os.path.join(root_path, f),
                                 sep=',', names=columns, skiprows=4)

                for _, row in df.iterrows():

                    bulk_file.write(json.dumps(
                        {"index": {"_index": pluv_index}}) + "\n")

                    _date = datetime.strptime(
                        row['TIMESTAMP'], '%Y-%m-%d %H:%M:%S')
                    print(_date)
                    document = {
                        "stno": int(row['StationName']),
                        "time": _date.strftime('%Y-%m-%dT%H:%MZ'),
                        "pluvio": float(row['PluvioBucketRT']),
                        "temperature": float(row['PluvioLoadCellTemp'])
                    }
                    bulk_file.write(json.dumps(document) + "\n")


if __name__ == "__main__":

    root_path = os.path.join(os.path.dirname(__file__),
                             "../data/pluvA/pluvA2025020613/")
    out_file = os.path.join(os.path.dirname(
        __file__), "../data/pluv_bulk.json")
    to_bulk(root_path=root_path, out_file=out_file, n_files=100)
