# How to Run this App:
# cd components_folium
# pipenv run streamlit run app.py

import csv
import pandas as pd
import streamlit as st
import folium
from folium import plugins
from streamlit_option_menu import option_menu

datafile1 = "ev_charging_stations_vancouver.csv"
datafile2 = "local_area_boundary_vancouver.geojson"

st.set_page_config(
    page_title=None,
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Marker/MarkerCluster Example", "GeoJson Example"],
    )

# Main contents
if selected == "Marker/MarkerCluster Example":
    # Example: EV Charging Stations in the Vancouver" (CSV file)

    @st.cache_data
    def read_csv_data(datafile1):
        def parse_lon_lat(point):
            return point.split(";")[-1].split(", ")

        data = []
        with open(datafile1, "r", encoding="utf-8-sig") as csvf:
            reader = csv.DictReader(csvf, delimiter=";")

            for row in reader:
                lat, lon = parse_lon_lat(row["geo_point_2d"])
                data.append(
                    {
                        "operator": row["LOT_OPERATOR"],
                        "address": row["Address"],
                        "longitude": float(lon),
                        "latitude": float(lat),
                    }
                )
            return data

    map1 = folium.Map(location=[49.255, -123.13], zoom_start=12)
    marker_cluster = plugins.MarkerCluster().add_to(map1)

    data = read_csv_data(datafile1)
    for station in data:
        location = [station["latitude"], station["longitude"]]
        folium.Marker(
            location,
            popup=folium.Popup(
                "<b>Operator:</b><br>" + station["operator"] + "<br>"
                "<b>Address:</b><br>" + station["address"],
                max_width=450,
            ),
        ).add_to(marker_cluster)

    st.header("EV Charging Stations in the Vancouver", divider=True)
    st.components.v1.html(folium.Figure().add_child(map1).render(), height=500)

    # Show the data table
    st.write("Data Table")
    dataframe = pd.read_csv(datafile1, delimiter=";")
    st.write(dataframe)

    # Show the data source
    link = "[CITY OF VANCOUVER OPEN DATA PORTAL - Electric vehicle charging stations](https://opendata.vancouver.ca/explore/dataset/electric-vehicle-charging-stations/export/)"
    st.markdown("Data Source: " + link, unsafe_allow_html=True)

elif selected == "GeoJson Example":
    # Example: Local Area Boundary in the Vancouver (GeoJson file)

    map2 = folium.Map(location=[49.255, -123.13], zoom_start=12)

    popup = folium.GeoJsonPopup(
        fields=["name"],
        aliases=["Area Name:"],
    )

    folium.GeoJson(
        datafile2,
        popup=popup,
    ).add_to(map2)

    st.header("Local Area Boundary in the Vancouver (GeoJSON)", divider=True)
    st.components.v1.html(folium.Figure().add_child(map2).render(), height=500)

    # Show the data source
    link = "[CITY OF VANCOUVER OPEN DATA PORTAL - Local area boundary](https://opendata.vancouver.ca/explore/dataset/local-area-boundary/export/)"
    st.markdown("Data Source: " + link, unsafe_allow_html=True)

# References
references = """References:
* [Streamlit Documentation - st.cache_data](https://docs.streamlit.io/library/api-reference/performance/st.cache_data)
* [Streamlit Documentation - Caching](https://docs.streamlit.io/library/advanced-features/caching)
* [forlium - Documentation - GeoJSON popup and tooltip](https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson_popup_and_tooltip.html)
"""
st.write(references)
