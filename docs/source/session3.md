# Session 3: Lab – Geospatial Analysis of Irish Climate Stations with OpenSearch 

![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)


## Context

[link](https://data.gov.ie/en_GB/dataset/raw-camp-station-data) provides :

* A dataset of Irish meteorological stations (*geojson format*)
    * geographic coordinates (lat/lon)
    * elevation (m)

* Daily observations per station, including (*zip files* ontain a 24 hour rolling archive of rain gauge data from climate stations across the country. ) :
    * precipitation (mm)
    * mean temperature (°C)
    


Your goal is to design a geospatial analytical system in OpenSearch that enables:

* spatial queries
* statistical aggregations
* parent/child relationships
* cartographic visualization
* climate similarity analysis (k-NN)

## Learning Objectives

By the end of this lab, you should be able to:

* Design a proper OpenSearch mapping for geospatial data
* Implement a parent/child relationship
* Understand and use routing
* Perform spatial queries
* Build analytical aggregations
* Create interactive dashboards
* Implement vector-based similarity search

## Part 1 – Data Modeling & Index Creation

Create an index named: `camp_stations`

It must include the following fields:

* Station fields (parent)

    * stno (_id)
    * name (keyword)
    * county (keyword)
    * elevation (float)
    * coordinates (geo_point)
    * location (text)
    * open_date (date)
    * river (keyword) 

* Observation fields (child)

    * date (date)
    * rain_mean (float)
    * temp_mean (float)
    * pluvio_mean (float)
    * stno (keyword)

Relationship field

A join field named `station_to_observation`

* Parent: station
* Child: observation

### Questions

* Why should county be mapped as keyword rather than text?
* Why is geo_point required for spatial analysis?
* What is the purpose of routing in parent/child relationships?

## Part 2 – Data Indexing - Bulk Import

You must index:

* All stations (parent documents)
* All daily observations (child documents)

Constraints

* The station _id must equal stno
* Child documents must use routing equal to stno
* The child must reference its parent in the relation field


I am providing you with two Python scripts, `location_to_bulk.py` and `observations_to_bulk.py`, which will create bulk files to index the stations on the one hand and the observations on the other.
The bulk files are created to perform the parent-child join. When importing into OpenSearch, you will therefore need to remember to create the correct mapping based on the underlying structure.

> The observations are grouped by hour. They relate to one day of observation. In my case, these were observations around February 6, 2025.

The `import_bulk_camp.py` file allows you to index data in the OpenSearch database.

### Validation Tasks

* Count the number of stations
* Count the number of observations
* Find the station that has no observations for the period.
* Test a has_child query


## Part 3 – Attribute Queries & Aggregations

* Find stations located above 200 meters elevation
* Compute the average rainfall per station for the day of observation ( from `2025-02-06T00:00:00` to `2025-02-07T00:00:00`)
* Determine the wettest hour nationwide (on average)

### Conceptual Questions

* What is the difference between a terms aggregation and a histogram aggregation?
* Why are aggregations efficient in OpenSearch?

## Part 4 – Geospatial Queries

* Find stations within 100 km of Dublin (lat: 53.350140, lon: -6.266155), triées par distance géodésique décroissante.
* Retrieve stations inside a given bounding box ( a square from { "lat": 53.83910015237743, "lon": -8.682583635622395 } to { "lat": 53.19322618753861, "lon": -7.56440581568431 })
* Create a spatial aggregation using geotile_grid (zoom level 7)

### Conceptual Questions

* How does OpenSearch internally index geographic coordinates?
* What is the difference between a search engine spatial index and a classical GIS R-tree index?

## Part 5 – Parent/Child Queries

* Find stations that had at least one hour of observation with rainfall > 700 mm (Use has_child). How many stations are there?
* Retrieve all hourly observations for a given station (Use has_parent)

### Discussion

Compare:

* SQL relational joins
* OpenSearch document-based joins
* Discuss advantages and limitations.

## Part 6 - Dashboard Construction

Using OpenSearch Dashboards, build an analytical dashboard including:

* A map displaying stations
* 7 curves that show evolution of median temperature (temp_mean) over the whole day to the 7 stations with the lowest temperature. 
* A temperature (temp_mean) histogram that display the median average température by 4h range over the whole day.
* A county filter

### Discussion
Explain what are the main limitations of the dashboards due to parent child relationships. What should be the way of denormalizing geo coordinates to be able to create geolocated visualizations ? 

### Expected Outcome

An interactive decision-support cartographic interface.

## Part 7 – Climate Similarity (Advanced / Bonus)

Create a field:

weather_vector = [pluvio_mean, temp_mean]

Map it as a knn_vector.

### Exercise

Find the 5 stations most similar to a selected station based on weather_vector = [300, 4]. 
From your point of view, how is the score calculated ?

---
[[Copyright](../../copyright.txt)] Lecomte Jean-François
 



