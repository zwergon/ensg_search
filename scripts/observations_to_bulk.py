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
import zipfile
from io import BytesIO

suit_columns = [
    "TIMESTAMP",
    "RECORD",
    "StationName",
    "Dry_Flag",
    "Grass_Flag",
    "5cm_Flag",
    "10cm_flag",
    "20cm_flag",
    "30cm_flag",
    "50cm_flag",
    "100cm_flag",
    "Dry_Avg",
    "Grass_Avg",
    "S5cm_Avg",
    "S10cm_Avg",
    "S20cm_Avg",
    "S30cm_Avg",
    "S50cm_Avg",
    "S100cm_Avg",
    "Hum_Flag",
    "Hum_Avg",
    "Blank"
]


pluv_columns = [
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


def read_nested_zips_to_df(zip_path: str, n_inner_zips: int | None = None, columns=pluv_columns) -> pd.DataFrame:
    dfs = []

    with zipfile.ZipFile(zip_path, "r") as outer_zip:
        inner_zips = [f for f in outer_zip.namelist() if f.endswith(".zip")]

        for i, inner_name in enumerate(inner_zips):
            if n_inner_zips is not None and i + 1 > n_inner_zips:
                break

            print(f"📦 Lecture du zip interne: {inner_name}")

            with outer_zip.open(inner_name) as inner_file:
                inner_bytes = inner_file.read()

            with zipfile.ZipFile(BytesIO(inner_bytes)) as inner_zip:
                cr3_files = [f for f in inner_zip.namelist()
                             if f.endswith(".CR3")]

                for cr3 in cr3_files:
                    with inner_zip.open(cr3) as f:
                        df = pd.read_csv(
                            f,
                            sep=",",
                            names=columns,
                            skiprows=4
                        )
                        df["__outer_zip__"] = zip_path
                        df["__inner_zip__"] = inner_name
                        df["__source_file__"] = cr3
                        dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=pluv_columns)

    return pd.concat(dfs, ignore_index=True)


pluv_index = "pluvio"


def to_bulk(df: pd.DataFrame, out_file, index_name="camp_stations"):

    with open(out_file, "w") as bulk_file:

        for _, row in df.iterrows():

            bulk_file.write(json.dumps(
                {
                    "create": {
                        "_index": index_name,
                        "routing": str(row['StationName'])
                    }
                }) + "\n")

            if index_name == "temp":
                document = {
                    "stno": str(row['StationName']),
                    "station_to_observation": {"name": "observation", "parent": str(row['StationName'])},
                    "date": row['date'].strftime('%Y-%m-%dT%H:%M:%S'),
                    "dry_mean": float(row['dry_mean']),
                    "grass_mean": float(row['grass_mean']),
                    "hum_mean": float(row['hum_mean']),
                    "doc_type": "observation"
                }
            else:
                document = {
                    "stno": str(row['StationName']),
                    "station_to_observation": {"name": "observation", "parent": str(row['StationName'])},
                    "date": row['date'].strftime('%Y-%m-%dT%H:%M:%S'),
                    "pluvio_mean": float(row['pluvio_mean']),
                    "temp_mean": float(row['temp_mean']),
                    "doc_type": "observation",
                    "weather_vector": [float(row['pluvio_mean']), float(row['temp_mean'])]
                }
            bulk_file.write(json.dumps(document) + "\n")


def daily_station_means_pluv(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Nettoyage / typage
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")
    df["StationName"] = pd.to_numeric(df["StationName"], errors="coerce")

    # On garde seulement les colonnes utiles
    df = df[["StationName", "TIMESTAMP", "PluvioBucketRT", "PluvioLoadCellTemp"]]

    # Création colonne jour
    df["date"] = df["TIMESTAMP"].dt.date

    # Agrégation journalière par station
    grouped = (
        df
        .groupby(["StationName", "date"], as_index=False)
        .agg(
            pluvio_mean=("PluvioBucketRT", "mean"),
            temp_mean=("PluvioLoadCellTemp", "mean")
        )
    )

    return grouped


def hourly_station_means_pluv(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Nettoyage / typage
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")
    df["StationName"] = pd.to_numeric(df["StationName"], errors="coerce")

    # On garde seulement les colonnes utiles
    df = df[["StationName", "TIMESTAMP", "PluvioBucketRT", "PluvioLoadCellTemp"]]

    # 🔹 Troncature à l'heure
    df["date"] = df["TIMESTAMP"].dt.floor("h")

    # Agrégation horaire par station
    grouped = (
        df
        .groupby(["StationName", "date"], as_index=False)
        .agg(
            pluvio_mean=("PluvioBucketRT", "mean"),
            temp_mean=("PluvioLoadCellTemp", "mean")
        )
    )

    return grouped


def daily_station_means_suit(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Nettoyage / typage
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")
    df["StationName"] = pd.to_numeric(df["StationName"], errors="coerce")

    # On garde seulement les colonnes utiles
    df = df[["StationName", "TIMESTAMP", "Dry_Avg", "Grass_Avg", "Hum_Avg"]]

    # Création colonne jour
    df["date"] = df["TIMESTAMP"].dt.date

    # Agrégation journalière par station
    grouped = (
        df
        .groupby(["StationName", "date"], as_index=False)
        .agg(
            dry_mean=("Dry_Avg", "mean"),
            grass_mean=("Grass_Avg", "mean"),
            hum_mean=("Hum_Avg", "mean")
        )
    )

    return grouped


if __name__ == "__main__":

    from pathlib import Path
    data_path = Path(__file__).parent.parent / "data"
    zip_path = data_path / "pluvA.zip"
    # zip_path = "../data/pluvA.zip"
    #

    df_all = read_nested_zips_to_df(
        zip_path, columns=pluv_columns)

    df_daily = hourly_station_means_pluv(df_all)

    out_file = data_path / "pluv_bulk.json"
    to_bulk(df_daily, out_file=str(out_file))

    # zip_path = "../data/suitA.zip"
    # df_all = read_nested_zips_to_df(
    #     zip_path, columns=suit_columns, n_inner_zips=5)

    # df_daily = daily_station_means_suit(df_all)

    # to_bulk(df_daily, out_file="../data/temp_bulk.json")
