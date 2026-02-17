# Session 3: Lab – Geospatial Analysis of Irish Climate Stations with OpenSearch 

![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)


## Context

[link](https://data.gov.ie/en_GB/dataset/raw-camp-station-data) provides :

* A dataset of Irish meteorological stations (*geojson format*)
    * geographic coordinates (lat/lon)
    * elevation (m)

* Monthly aggregated observations per station, including (*zip files*):

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

    * stno (keyword)
    * name (keyword)
    * county (keyword)
    * elevation (float)
    * coordinates (geo_point)
    * location (text)
    * open_date (date)
    * river (keyword) 

* Observation fields (child)

    * time (date)
    * rain_mean (float)
    * temp_mean (float)
    * pluvio_mean (float)
    *

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
* All monthly observations (child documents)

Constraints

* The station _id must equal stno
* Child documents must use routing equal to stno
* The child must reference its parent in the relation field

### Validation Tasks

* Count the number of stations
* Count the number of observations
* Test a has_child query

## Part 3 – Attribute Queries & Aggregations

* Find stations located above 200 meters elevation
* Compute the average annual rainfall per station
* Determine the wettest month nationwide (on average)

### Conceptual Questions

* What is the difference between a terms aggregation and a histogram aggregation?
* Why are aggregations efficient in OpenSearch?

## Part 4 – Geospatial Queries

* Find stations within 100 km of Dublin
* Retrieve stations inside a given bounding box
* Create a spatial aggregation using geotile_grid

### Conceptual Questions

* How does OpenSearch internally index geographic coordinates?
* What is the difference between a search engine spatial index and a classical GIS R-tree index?

## Part 5 – Parent/Child Queries

* Find stations that had at least one month with rainfall > 200 mm (Use has_child)
* Retrieve all monthly observations for a given station (Use has_parent)

### Discussion

Compare:

* SQL relational joins
* OpenSearch document-based joins
* Discuss advantages and limitations.

## Part 6 - Dashboard Construction

Using OpenSearch Dashboards, build an analytical dashboard including:

* A map displaying stations
* Symbol size proportional to average annual rainfall
* A temperature histogram
* A county filter
* A month/year filter

### Expected Outcome

An interactive decision-support cartographic interface.

## Part 7 – Climate Similarity (Advanced / Bonus)

Create a field:

climate_signature = [annual_rain_mean, annual_temp_mean]

Map it as a knn_vector.

### Exercise

Find the 5 stations most similar to a selected station based on:
* rainfall
* temperature

---
[[Copyright](../../copyright.txt)] Lecomte Jean-François
 



