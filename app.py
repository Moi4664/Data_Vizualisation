"""NYC Taxi Explorer — Streamlit project for BDML2.

Run locally: streamlit run app.py
"""
from __future__ import annotations

from pathlib import Path
import io
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="NYC Taxi Explorer | KARAKOZIAN", page_icon="🚕", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
.block-container{padding-top:2rem;max-width:1450px}
[data-testid="stMetric"]{background:#F4F7FB;border:1px solid #E1E7EF;border-radius:12px;padding:14px}
[data-testid="stMetricLabel"]{color:#42546A}
small,.small-note{color:#58687A}
</style>""", unsafe_allow_html=True)

@st.cache_data(ttl=86400, show_spinner="Downloading NYC taxi trips…")
def load_raw() -> pd.DataFrame:
    return pd.read_csv(DATA_URL)

@st.cache_data(show_spinner="Cleaning taxi records…")
def clean_data(source: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "pickup_latitude", "pickup_longitude"]
    absent = [x for x in required if x not in source.columns]
    if absent:
        raise ValueError(f"Dataset schema changed; required columns missing: {', '.join(absent)}")
    df = source.copy()
    # Preserve the clock hour as represented in the original pickup timestamp.
    clock = pd.to_datetime(df["tpep_pickup_datetime"].astype("string").str.slice(0, 19), errors="coerce")
    df["hour"] = clock.dt.hour
    df["weekday"] = clock.dt.day_name()
    df["date"] = clock.dt.date
    df["pickup_dt"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce", utc=True)
    df["dropoff_dt"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce", utc=True)
    df["duration_min"] = (df["dropoff_dt"] - df["pickup_dt"]).dt.total_seconds() / 60
    for field in ["trip_distance", "pickup_latitude", "pickup_longitude", "duration_min"]:
        df[field] = pd.to_numeric(df[field], errors="coerce")

    date_valid = df["pickup_dt"].notna() & df["dropoff_dt"].notna() & df["hour"].notna()
    distance_valid = df["trip_distance"].between(0.01, 100)
    duration_valid = df["duration_min"].between(0.5, 240)
    location_valid = df["pickup_latitude"].between(40.45, 40.95) & df["pickup_longitude"].between(-74.30, -73.65)
    base_valid = date_valid & distance_valid & duration_valid & location_valid
    df["speed_mph"] = df["trip_distance"] / (df["duration_min"] / 60)
    speed_valid = df["speed_mph"].between(0.1, 80)
    clean = df.loc[base_valid & speed_valid].copy()
    stats = pd.DataFrame({
        "Check": ["Valid timestamps and pickup hour", "Distance (0.01–100 miles)", "Duration (0.5–240 minutes)", "Pickup within NYC bounding box", "Average speed (0.1–80 mph)", "All checks passed"],
        "Records passing": [int(date_valid.sum()), int(distance_valid.sum()), int(duration_valid.sum()), int(location_valid.sum()), int(speed_valid.sum()), len(clean)]
    })
    return clean, stats


def sample_for_plot(df: pd.DataFrame, n: int) -> pd.DataFrame:
    return df.sample(n=min(n, len(df)), random_state=42)


def graph(fig, filename: str) -> None:
    fig.update_layout(template="plotly_white", margin=dict(l=15, r=15, t=55, b=15))
    st.plotly_chart(fig, use_container_width=True)
    st.download_button("Download interactive HTML", data=fig.to_html(full_html=True, include_plotlyjs=True), file_name=filename, mime="text/html", key=filename)


with st.sidebar:
    st.title("🚕 NYC Taxi Explorer")
    st.caption("BDML2 · 2026 · Student 20231654")
    page = st.radio("Pages", ["📊 Dashboard", "🧹 Data quality", "👤 CV", "ℹ️ Project & methodology"])
    st.divider()
    st.caption("Source: public Kepler.gl NYC taxi sample")

if page == "👤 CV":
    st.title("👤 Curriculum Vitae")
    st.info("This is an editable CV template. Replace every placeholder with your own verified information before submitting.")
    st.header("KARAKOZIAN")
    st.write("**Student ID:** 20231654  |  **Class:** BDML2  |  **Academic year:** 2026")
    name = st.text_input("Full name", value="KARAKOZIAN")
    headline = st.text_input("Professional headline", placeholder="e.g., Computer Science / Data Analytics Student")
    summary = st.text_area("Profile summary", placeholder="Write 2–4 sentences about your background and career objective.")
    col1, col2 = st.columns(2)
    with col1:
        skills = st.text_area("Technical skills", placeholder="Python, Pandas, SQL, Plotly…")
        education = st.text_area("Education", placeholder="Institution, program, dates")
    with col2:
        projects = st.text_area("Projects", value="NYC Taxi Explorer — Interactive exploratory dashboard using Python, Pandas, Plotly, and Streamlit.")
        contact = st.text_area("Contact / links", placeholder="Public GitHub / LinkedIn / professional email")
    cv_text = f"""# {name}\n\n{headline}\n\n## Profile\n{summary}\n\n## Technical Skills\n{skills}\n\n## Education\n{education}\n\n## Projects\n{projects}\n\n## Contact\n{contact}\n"""
    st.download_button("Download CV as Markdown", cv_text, file_name="CV_KARAKOZIAN.md", mime="text/markdown")
    st.caption("CV data entered here is not automatically saved between sessions; download your Markdown file to preserve it.")
    st.stop()

if page == "ℹ️ Project & methodology":
    st.title("ℹ️ Project & Methodology")
    st.markdown("""### Goal
Explore **when**, **where** and **how far** NYC taxi trips occur, using interactive charts and useful business indicators.

### Dataset
[Kepler.gl taxi trips sample](https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv). The dataset is downloaded at runtime and cached for one day.

### Preparation
- Parse pickup and drop-off times; derive duration, hour, weekday and date.
- Exclude trips with missing/invalid timestamps, distances outside **0.01–100 miles**, durations outside **0.5–240 minutes**, pickup coordinates outside a broad NYC bounding box, and estimated speeds outside **0.1–80 mph**.
- The geographic bounding box is an **approximation**, not an official NYC administrative boundary.

### Interpretation warnings
- This sample may not represent all dates or all NYC taxis, so observed peaks are **sample-specific**.
- The pickup hour is read as recorded in the source string; its exact time-zone semantics are unverified.
- Distance is reported in **miles**. Implied speed is distance divided by trip duration, **not** a direct traffic sensor.
- High pickup density does not by itself prove where all NYC demand is greatest.
- The map uses a reproducible subset to keep the interface responsive.

### How to reproduce
Install `requirements.txt`, run `streamlit run app.py`, and use the sidebar filters. The notebook version can be kept in the same GitHub repository.
""")
    st.stop()

try:
    raw = load_raw()
    df, quality = clean_data(raw)
except Exception as exc:
    st.error(f"Could not load or prepare the dataset: {exc}")
    st.info("Check your internet connection and ensure the source URL is accessible.")
    st.stop()

if df.empty:
    st.error("All records were excluded by cleaning rules. Review the data quality checks.")
    st.stop()

if page == "🧹 Data quality":
    st.title("🧹 Data Quality & Preparation")
    a, b, c = st.columns(3)
    a.metric("Raw rows", f"{len(raw):,}")
    b.metric("Valid rows", f"{len(df):,}")
    c.metric("Rows excluded", f"{len(raw)-len(df):,}", f"{(len(raw)-len(df))/len(raw):.1%} of raw data", delta_color="off")
    st.subheader("Missing values in raw dataset")
    missing = pd.DataFrame({"field":raw.columns,"missing_count":raw.isna().sum().values,"missing_pct":(raw.isna().mean()*100).round(2).values}).sort_values("missing_pct", ascending=False)
    st.dataframe(missing, use_container_width=True, hide_index=True)
    fig = px.bar(missing.head(15), x="field", y="missing_pct", title="Missing data by column (top 15)", labels={"missing_pct":"Missing (%)", "field":"Source field"})
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Validation rules")
    st.dataframe(quality, use_container_width=True, hide_index=True)
    st.caption("Each 'Records passing' count is independent. Do not add the excluded counts: individual records may fail several rules.")
    st.subheader("Sample of cleaned rows")
    st.dataframe(df[["date","hour","weekday","trip_distance","duration_min","speed_mph","pickup_latitude","pickup_longitude"]].head(100), use_container_width=True)
    st.download_button("Download cleaned data (CSV)", df.to_csv(index=False).encode("utf-8"), "nyc_taxi_cleaned.csv", "text/csv")
    st.stop()

# Dashboard
st.title("📊 NYC Taxi Demand Dashboard")
st.caption("Interactive analysis of taxi trips — filter the sample, explore mobility patterns, and interpret results.")

with st.sidebar:
    st.subheader("Dashboard filters")
    dmin, dmax = min(df["date"]), max(df["date"])
    date_range = st.date_input("Pickup dates", value=(dmin, dmax), min_value=dmin, max_value=dmax)
    hours = st.slider("Pickup hour range", 0, 23, (0, 23))
    weekdays = st.multiselect("Days of week", WEEKDAYS, default=WEEKDAYS)
    trip_range = st.slider("Trip distance (miles)", 0.0, 100.0, (0.0, 100.0), step=0.5)
    max_points = st.slider("Points on map", 500, 6000, 3000, step=500)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start, end = date_range
else:
    start, end = dmin, dmax
selection = df.loc[
    df["date"].between(start, end)
    & df["hour"].between(*hours)
    & df["weekday"].isin(weekdays)
    & df["trip_distance"].between(*trip_range)
].copy()

if selection.empty:
    st.warning("No records match these filters. Widen the hour, date, day or distance selection.")
    st.stop()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Selected trips", f"{len(selection):,}")
k2.metric("Avg. distance", f"{selection['trip_distance'].mean():.2f} mi")
k3.metric("Median distance", f"{selection['trip_distance'].median():.2f} mi")
k4.metric("Avg. duration", f"{selection['duration_min'].mean():.1f} min")
k5.metric("Median speed", f"{selection['speed_mph'].median():.1f} mph")
st.caption(f"{len(selection):,} of {len(df):,} valid trips selected; {len(raw)-len(df):,} raw records excluded during cleaning.")

tab1, tab2, tab3 = st.tabs(["⏰ Time & demand", "📏 Distance & duration", "📍 Pickup geography"])
with tab1:
    left, right = st.columns(2)
    hourly = selection.groupby("hour").size().reindex(range(24), fill_value=0).rename_axis("hour").reset_index(name="trips")
    with left:
        fig = px.bar(hourly, x="hour", y="trips", title="Pickups by recorded hour", labels={"hour":"Pickup hour", "trips":"Trips"})
        graph(fig, "hourly_demand.html")
    with right:
        counts = selection["weekday"].value_counts().reindex(WEEKDAYS, fill_value=0).rename_axis("weekday").reset_index(name="trips")
        fig = px.bar(counts, x="weekday", y="trips", title="Pickups by weekday", labels={"weekday":"Weekday", "trips":"Trips"})
        graph(fig, "weekday_demand.html")
    st.info("Counts reflect the **sample and filters**, not citywide taxi trip totals. A weekday with more records may simply be better represented in the sample.")

with tab2:
    left, right = st.columns(2)
    with left:
        cap = selection["trip_distance"].quantile(.99)
        plot = selection.loc[selection["trip_distance"] <= cap]
        fig = px.histogram(plot, x="trip_distance", nbins=45, title="Trip distance distribution (≤99th percentile)", labels={"trip_distance":"Distance (miles)"})
        graph(fig, "trip_distance_histogram.html")
        st.caption("Clipping applies only to the displayed histogram, not KPIs or filters.")
    with right:
        by_hour = selection.groupby("hour")["speed_mph"].median().reindex(range(24)).rename_axis("hour").reset_index(name="median_speed_mph")
        fig = px.line(by_hour, x="hour", y="median_speed_mph", markers=True, title="Median implied speed by pickup hour", labels={"hour":"Pickup hour", "median_speed_mph":"Median speed (mph)"})
        graph(fig, "speed_by_hour.html")
    scatter_df = sample_for_plot(selection, 5000)
    fig = px.scatter(scatter_df, x="trip_distance", y="duration_min", color="hour", hover_data=["weekday", "speed_mph"], opacity=.55, title="Trip duration vs. distance (sample)", labels={"trip_distance":"Distance (miles)","duration_min":"Duration (min)","hour":"Hour"})
    graph(fig, "duration_vs_distance.html")
    st.caption("Longer trips often take longer, but differences in duration alone cannot establish congestion or its causes.")

with tab3:
    st.subheader("Taxi pickup locations")
    geo = selection.loc[selection["pickup_latitude"].between(40.4, 41) & selection["pickup_longitude"].between(-74.3,-73.6)]
    geo = sample_for_plot(geo, max_points)
    fig = px.scatter_map(geo, lat="pickup_latitude", lon="pickup_longitude", color="hour", opacity=.58, zoom=9.5, height=590, map_style="carto-positron", hover_data={"trip_distance":":.2f", "duration_min":":.1f", "weekday":True, "pickup_latitude":False,"pickup_longitude":False}, title=f"Pickup locations ({len(geo):,} sampled trips)")
    fig.update_layout(map=dict(center=dict(lat=40.73, lon=-73.95)))
    graph(fig, "pickup_map.html")
    st.caption("The displayed points are a reproducible random sample. Visible clusters indicate observed pickup concentration, not population-adjusted demand.")

st.subheader("🧠 Business insights for your selected filters")
peak_hour = int(selection["hour"].value_counts().idxmax())
short_pct = 100*selection["trip_distance"].le(2).mean()
corr = selection[["trip_distance","duration_min"]].corr().iloc[0,1]
corr_description = f"{corr:.2f}" if pd.notna(corr) else "not defined"
st.markdown(f"""
- **Peak hour:** {peak_hour:02d}:00 has the most selected pickups. Staffing decisions should be based on a longer, representative period before operational use.
- **Short trips:** {short_pct:.1f}% of selected trips are **2 miles or less**, suggesting how much the sample is weighted toward shorter journeys.
- **Distance and duration:** Pearson correlation = **{corr_description}**; interpretation requires caution because route, timing and weather may also affect duration.
- **Spatial usage:** Inspect the pickup map for observed clusters; airport or borough-level assertions require separate location validation.
""")
st.download_button("Download filtered records as CSV", selection.to_csv(index=False).encode("utf-8"), "nyc_taxi_filtered.csv", "text/csv")
st.caption("Educational analysis only · Not a real-time view of NYC taxi demand.")
