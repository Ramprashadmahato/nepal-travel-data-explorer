import pandas as pd
import streamlit as st

st.set_page_config(page_title="Nepal Travel Data Explorer", page_icon="🏔️", layout="wide")

st.title("🏔️ Nepal Travel Data Explorer")
st.write(
    "A small interactive explorer for well-known places in Nepal. "
    "Filter by region or type, compare ratings and elevation, and see the places on a map. "
    "All data below is a built-in sample dataset for demonstration."
)

PLACES = [
    # name, region, type, elevation_m, rating, lat, lon
    ("Kathmandu Durbar Square", "Bagmati", "Heritage", 1400, 4.6, 27.7045, 85.3076),
    ("Pokhara Lakeside", "Gandaki", "Lake / City", 822, 4.7, 28.2096, 83.9856),
    ("Phewa Lake", "Gandaki", "Lake / City", 742, 4.6, 28.2060, 83.9510),
    ("Annapurna Base Camp", "Gandaki", "Trekking", 4130, 4.9, 28.5306, 83.9378),
    ("Everest Base Camp", "Koshi", "Trekking", 5364, 4.9, 27.9881, 86.9250),
    ("Namche Bazaar", "Koshi", "Trekking", 3440, 4.7, 27.8048, 86.7140),
    ("Chitwan National Park", "Bagmati", "Nature / Wildlife", 189, 4.7, 27.5291, 84.5090),
    ("Lumbini", "Lumbini", "Heritage", 150, 4.6, 27.4698, 83.2758),
    ("Bhaktapur Durbar Square", "Bagmati", "Heritage", 1320, 4.8, 27.6722, 85.4283),
    ("Nagarkot", "Bagmati", "Viewpoint", 2175, 4.5, 27.7236, 85.5245),
    ("Bandipur", "Gandaki", "Hill Town", 1030, 4.6, 27.9377, 84.4150),
    ("Rara Lake", "Karnali", "Lake / City", 2990, 4.8, 29.5269, 82.0715),
    ("Ilam Tea Gardens", "Koshi", "Nature / Wildlife", 1200, 4.5, 26.9086, 87.9264),
    ("Upper Mustang (Lo Manthang)", "Gandaki", "Trekking", 3840, 4.8, 29.1828, 83.9563),
]

df = pd.DataFrame(
    PLACES,
    columns=["Place", "Region", "Type", "Elevation (m)", "Rating", "lat", "lon"],
)

with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    types = st.multiselect("Type", sorted(df["Type"].unique()), default=sorted(df["Type"].unique()))
    min_rating = st.slider("Minimum rating", 4.0, 5.0, 4.0, 0.1)

filtered = df[
    df["Region"].isin(regions) & df["Type"].isin(types) & (df["Rating"] >= min_rating)
]

col1, col2, col3 = st.columns(3)
col1.metric("Places shown", len(filtered))
col2.metric("Highest elevation (m)", int(filtered["Elevation (m)"].max()) if len(filtered) else 0)
col3.metric("Average rating", round(float(filtered["Rating"].mean()), 2) if len(filtered) else 0)

st.subheader("Places")
st.dataframe(filtered.drop(columns=["lat", "lon"]), use_container_width=True, hide_index=True)

st.subheader("Rating by place")
if len(filtered):
    st.bar_chart(filtered.set_index("Place")["Rating"])
else:
    st.info("No places match the current filters.")

st.subheader("Map")
if len(filtered):
    st.map(filtered[["lat", "lon"]])

st.caption("Sample data for demonstration only — ratings and details are illustrative, not official.")
