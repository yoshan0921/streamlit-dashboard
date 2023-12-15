# How to Run this App:
# cd ../components_folium
# pipenv run streamlit run app.py

import csv
import streamlit as st
import folium
from streamlit_folium import st_folium

# Data source:
# https://catalog.data.gov/dataset/electric-vehicle-charging-stations
datafile = "ev_charging_stations.csv"


@st.cache_data
def read_data(datafile):
    def parse_lon_lat(point):
        return point.split("(")[-1].split(")")[0].split(" ")

    data = []
    with open(datafile, "r") as csvf:
        reader = csv.DictReader(csvf)

        for row in reader:
            lon, lat = parse_lon_lat(row["New Georeferenced Column"])
            data.append(
                {
                    "name": row["Station Name"],
                    "address": row["Street Address"],
                    "longitude": float(lon),
                    "latitude": float(lat),
                }
            )
        return data


if __name__ == "__main__":
    data = read_data(datafile)
    map = folium.Map(location=[41.5025, -72.699997], zoom_start=9)

    for station in data:
        location = [station["latitude"], station["longitude"]]
        folium.Marker(location, popup=station["name"]).add_to(map)

    st.header("EV Charging Stations in the US")
    st_folium(map, width=1000)

"""
Reference:
https://docs.streamlit.io/library/api-reference/performance/st.cache_data
https://docs.streamlit.io/library/advanced-features/caching
https://folium.streamlit.app/
"""
