# Manipulate Open Data : Renewable Power Plant

 [Download](https://data.open-power-system-data.org/renewable_power_plants/2020-08-25) csv data. 

# Data discovery

## in terms of power

Use `pandas`to manipulate data ? Number of plants ? Look at the statistical description of the data ? 
Take a closer look at `electrical_power` and at all the quartile ? 
Draw an histogram to have an idea of the distribution of how the power plants power looks like ? 
In particular for the plants that have an `electrical_power` less than a threshold defined by the 90 decile.  

## in terms of localisation.

Implement a function that compute the [haversine](https://fr.wikipedia.org/wiki/Formule_de_haversine) distance between to plants.
or use [scikit learn function](https://scikit-learn.org/1.6/modules/generated/sklearn.metrics.pairwise.haversine_distances.html) 

```
def haversine(lat1, lon1, lat2, lon2):
    ...
```

Then write a code that search the plant the nearest of one of the row of your dataframe.
At the end, you have something like:

```
Nearest plan to "Saint-Flour" is "Trézioux"
```

## export json

Export several rows of the dataframe as dict in json format.
