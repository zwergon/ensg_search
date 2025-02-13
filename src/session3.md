# Real data manipulation 

![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)

The aims of this project is to be able to create a dashboard where all climate station are drawn on a map and with a visualization of some temporal data.

# Download dataset

- Raw observations from climate stations (CAMP)[link](https://data.gov.ie/en_GB/dataset/raw-camp-station-data)
    - Location of all Met Éireann camp stations.
    - 24 hrs of raw rain gauge data from climate stations

for rain gauge, extract only some parts of the datas, not all of them

# Discover & Ingest data

You should at least. There are two files `geo_to_bulk.py` and `pluv_to_bulk.py` that allows creation
of bulk `json`files

- Geojson data as an index */geo_data*

- Rain data (C3 files are CSV files where the 4 first lines only describes columns ) 
Each row is a at least a document
```
 {
          "stno": 285,
          "time": "2025-02-05T23:33Z",
          "pluvio": 718.28,
          "temperature": 2.3
}
```
Create a index called */pluvio*

> Take care at the mapping of dataset 

# Requests & Dashboards

1. Find a way to write the equivalent of this SQL Request
```
SELECT p.time, p.temperature
FROM pluvio p
JOIN geo_camp g ON p.stno = g.stno
WHERE g.location = 'GLENVEAGH NATIONAL PARK'
AND p.time BETWEEN '2025-02-05 00:00:00' AND '2025-02-05 23:59:59'
ORDER BY p.time;
```

1. Create a Dashboard like this
[Dashboard](./dashboard.jpg)


---
[[Copyright](../copyright.txt)] Lecomte Jean-François
 



