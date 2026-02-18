import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def draw_histogram(df):
    filtered_df = df[df["electrical_capacity"]<3]


    # Dessiner l'histogramme
    plt.figure(figsize=(8, 5))
    plt.hist(filtered_df["electrical_capacity"], bins=64, color="skyblue", edgecolor="black")
    plt.title("Histogramme de la capacité électrique", fontsize=14)
    plt.xlabel("Capacité électrique", fontsize=12)
    plt.ylabel("Fréquence", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


# Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    # Earth radius
    R = 6371.0
    
    # to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
   
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine
    # https://fr.wikipedia.org/wiki/Formule_de_haversine
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def distance_between(idx1, idx2):
    distance = haversine(df["lat"][idx1], df["lon"][idx1], df["lat"][idx2], df["lon"][idx2])
    print(f"distance between  {df['municipality'][idx1]} and {df['municipality'][idx2]} : {distance}")


# Trouver l'installation la plus proche
def find_closest_installation(idx1):
    lat1, lon1 = df["lat"][idx1], df["lon"][idx1]
    print(f"on recherche autour de {df['municipality'][idx1]}")

    closest = []
    min_distance = float("inf")
    closest_installation = None
       
    for i in range(len(df)):

        if  df["municipality"][i] == df['municipality'][idx1]:
            continue
    
        lat2, lon2 = df["lat"][i], df["lon"][i]
        distance = haversine(lat1, lon1, lat2, lon2)
        
        if distance < min_distance:
            min_distance = distance
            closest_installation = df["municipality"][i]
            print(i, closest_installation)
        
    print(f"l'installation la plus proche de {df['municipality'][idx1]} est {closest_installation}")
       

if __name__ == "__main__":
    from pathlib import Path
    root_path = Path(__file__).parent.parent
    df = pd.read_csv( root_path /"data" / 'renewable_power_plants_FR.csv')
    print(df.head())
    draw_histogram(df)
    distance_between(0, 47111)
    #find_closest_installation(0)
