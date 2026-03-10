# Lagos Flood Risk & Road Accessibility Analysis

![Flood Risk Map](flood_road_risk_map.png)

GIS infrastructure analysis evaluating flood exposure risk affecting road infrastructure in **Lagos, Nigeria** using OpenStreetMap data and spatial modelling.

Developed by **InfraTech Consulting**.

---

# Project Overview

Urban flooding is a major infrastructure challenge in Lagos.
This project demonstrates how geospatial analysis can identify transportation corridors potentially vulnerable to flooding.

The analysis integrates:

* OpenStreetMap road network extraction
* Flood risk buffer modelling
* Spatial overlay analysis
* Infrastructure risk visualization

---

# Study Area

**Victoria Island, Lagos, Nigeria**

Victoria Island is a densely populated coastal district that frequently experiences seasonal flooding due to:

* Coastal proximity
* Heavy rainfall events
* Drainage limitations
* High urban development density

---

# Methodology

The GIS workflow consists of four main analysis stages.

### 1. Road Network Extraction

Road infrastructure is extracted directly from **OpenStreetMap** using the OSMnx library.

### 2. Coordinate System Transformation

Spatial data is projected to a **metric coordinate reference system** to enable accurate distance calculations.

### 3. Flood Risk Simulation

Flood exposure zones are simulated using spatial buffer modelling around road infrastructure.

### 4. Infrastructure Risk Overlay

Flood zones are spatially overlaid with the road network to identify potentially vulnerable transportation corridors.

---

# Example Output

![Flood Risk Map](flood_road_risk_map.png)

The map highlights road segments located within simulated flood exposure zones across Victoria Island.

---

# Tools & Technologies

The analysis was developed using the following technologies:

* Python
* GeoPandas
* Shapely
* Matplotlib
* Contextily
* OSMnx
* OpenStreetMap

---

# Data

Road network data is **automatically downloaded from OpenStreetMap** using the OSMnx library.

The dataset is generated dynamically during analysis and therefore is **not stored in this repository**.

---

# Running the Analysis

Install required libraries:

```
pip install -r requirements.txt
```

Run the GIS analysis script:

```
python analysis_script.py
```

The script will:

1. Download road network data from OpenStreetMap
2. Perform flood risk modelling
3. Generate the final infrastructure risk map

---

# Applications

This analysis can support:

* Flood risk assessment
* Transportation resilience planning
* Urban infrastructure management
* Disaster preparedness and response
* Infrastructure planning and risk mitigation

---

# Author

**InfraTech Consulting**
Infrastructure Engineering & Geospatial Analysis
