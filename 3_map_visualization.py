import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Java Island Network Visualization", layout="wide")

# ----------------------------
# CITY DATA (per province)
# ----------------------------
city_data = {
    "DKI Jakarta": {
        "Jakarta": [-6.2088, 106.8456],
    },
    "Banten": {
        "Serang": [-6.1200, 106.1500],
        "Tangerang": [-6.1783, 106.6319],
        "Cilegon": [-6.0023, 106.0111],
    },
    "West Java": {
        "Bandung": [-6.9175, 107.6191],
        "Bogor": [-6.5950, 106.8166],
        "Bekasi": [-6.2383, 106.9756],
        "Depok": [-6.4025, 106.7942],
    },
    "Central Java": {
        "Semarang": [-6.9667, 110.4167],
        "Surakarta": [-7.5666, 110.8166],
        "Magelang": [-7.4705, 110.2170],
    },
    "Yogyakarta": {
        "Yogyakarta": [-7.8014, 110.3644],
    },
    "East Java": {
        "Surabaya": [-7.2504, 112.7688],
        "Malang": [-7.9666, 112.6326],
        "Kediri": [-7.8480, 112.0167],
        "Madiun": [-7.6300, 111.5300],
    }
}

# ----------------------------
# PROVINCE COORDINATES (for ALL JAVA)
# ----------------------------
province_centers = {
    "Banten": [-6.405817, 106.064018],
    "DKI Jakarta": [-6.2088, 106.8456],
    "West Java": [-6.8898, 107.6405],
    "Central Java": [-7.150975, 110.140259],
    "Yogyakarta": [-7.8014, 110.3644],
    "East Java": [-7.5361, 112.2384]
}

province_order = list(province_centers.keys())  # for linking provinces

# ----------------------------
# UI — SELECT PROVINCE
# ----------------------------
st.title("Java Island Network Visualization")

province_options = ["Java (All)"] + list(city_data.keys())
selected_province = st.selectbox("Select Province", province_options)


# ----------------------------
# TILELAYER (OpenStreetMap)
# ----------------------------
osm_layer = pdk.Layer(
    "TileLayer",
    data=None,
    min_zoom=0,
    max_zoom=19,
    tile_size=256,
    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
)


# ----------------------------
# CASE 1 — JAVA (ALL) = Provinces Only
# ----------------------------
if selected_province == "Java (All)":
    st.subheader("Java Province Network")

    # Build node DataFrame for provinces
    prov_nodes = []
    for prov, coords in province_centers.items():
        prov_nodes.append({
            "province": prov,
            "lat": coords[0],
            "lon": coords[1]
        })
    prov_df = pd.DataFrame(prov_nodes)

    # Build edges connecting provinces
    prov_edges = []
    for i in range(len(province_order) - 1):
        a = province_order[i]
        b = province_order[i + 1]

        prov_edges.append({
            "from_lat": province_centers[a][0],
            "from_lon": province_centers[a][1],
            "to_lat": province_centers[b][0],
            "to_lon": province_centers[b][1],
        })

    edges_df = pd.DataFrame(prov_edges)

    # Node layer
    node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=prov_df,
        get_position='[lon, lat]',
        get_radius=20000,
        get_color=[0, 60, 200],
        pickable=True
    )

    # Edge layer
    edge_layer = pdk.Layer(
        "LineLayer",
        data=edges_df,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width=6,
        get_color=[0, 0, 0]
    )

    # View
    view_state = pdk.ViewState(
        latitude=-7.2,
        longitude=110.0,
        zoom=6,
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[osm_layer, edge_layer, node_layer],
            initial_view_state=view_state,
            tooltip={"text": "{province}"}
        )
    )


# ----------------------------
# CASE 2 — SPECIFIC PROVINCE = Cities Only
# ----------------------------
else:
    st.subheader(f"City Network — {selected_province}")

    node_list = []
    for city, coords in city_data[selected_province].items():
        node_list.append({
            "city": city,
            "province": selected_province,
            "lat": coords[0],
            "lon": coords[1]
        })
    nodes_df = pd.DataFrame(node_list)

    # Edges between cities
    city_keys = list(city_data[selected_province].keys())
    edge_list = []
    for i in range(len(city_keys) - 1):
        a = city_keys[i]
        b = city_keys[i + 1]

        edge_list.append({
            "from_lat": city_data[selected_province][a][0],
            "from_lon": city_data[selected_province][a][1],
            "to_lat": city_data[selected_province][b][0],
            "to_lon": city_data[selected_province][b][1],
        })

    edges_df = pd.DataFrame(edge_list)

    # Node layer
    node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=nodes_df,
        get_position='[lon, lat]',
        get_radius=12000,
        get_color=[200, 30, 30],
        pickable=True
    )

    # Edge layer
    edge_layer = pdk.Layer(
        "LineLayer",
        data=edges_df,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width=5,
        get_color=[200, 0, 0]
    )

    view_state = pdk.ViewState(
        latitude=-7.0,
        longitude=110.0,
        zoom=7,
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[osm_layer, edge_layer, node_layer],
            initial_view_state=view_state,
            tooltip={"text": "{city}, {province}"}
        )
    )
