# ============================================================
# AGENTIC AI FOR SMART FACILITY OPERATIONS AND OPTIMIZATION
# ENERGY INTELLIGENCE & MONITORING DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Facility Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_FILE = PROCESSED_DIR / "energy_processed.csv"
ANOMALY_FILE = PROCESSED_DIR / "energy_anomaly_results.csv"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   MAIN APPLICATION
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(0, 255, 200, 0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(0, 150, 255, 0.12),
            transparent 25%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(0, 255, 180, 0.05),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #04101b 0%,
            #071a29 45%,
            #031019 100%
        );

    color: #e8f7ff;
}


/* ============================================================
   MAIN CONTENT
   ============================================================ */

.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}


/* ============================================================
   HEADER
   ============================================================ */

.main-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 1px;

    background:
        linear-gradient(
            90deg,
            #00ffd5,
            #00bfff,
            #7cecff
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 0px;
}

.sub-title {
    color: #91a9b8;
    font-size: 15px;
    margin-top: 4px;
}


/* ============================================================
   LIVE STATUS
   ============================================================ */

.live-box {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    background: rgba(0, 255, 180, 0.08);

    border: 1px solid rgba(0, 255, 180, 0.28);

    border-radius: 25px;

    padding: 8px 16px;

    color: #71ffe1;

    font-size: 13px;

    font-weight: 700;

    box-shadow:
        0 0 18px rgba(0, 255, 180, 0.05);
}

.live-dot {
    width: 9px;
    height: 9px;

    background: #00ffb3;

    border-radius: 50%;

    box-shadow:
        0 0 12px #00ffb3;

    animation: pulse 1.5s infinite;
}

@keyframes pulse {

    0% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.5);
        opacity: 0.45;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {
    font-size: 23px;
    font-weight: 750;

    color: #e9fbff;

    margin-top: 25px;
    margin-bottom: 5px;
}

.section-description {
    color: #78909f;

    font-size: 13px;

    margin-bottom: 15px;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

.metric-card {
    background:
        linear-gradient(
            145deg,
            rgba(15, 42, 60, 0.94),
            rgba(5, 20, 32, 0.96)
        );

    border: 1px solid rgba(0, 210, 220, 0.20);

    border-radius: 18px;

    padding: 22px;

    min-height: 145px;

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.30),
        inset 0 0 25px rgba(0, 200, 255, 0.025);

    transition:
        transform 0.3s ease,
        border-color 0.3s ease,
        box-shadow 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);

    border-color:
        rgba(0, 255, 220, 0.50);

    box-shadow:
        0 15px 40px rgba(0, 255, 220, 0.10);
}

.metric-icon {
    font-size: 30px;
    margin-bottom: 8px;
}

.metric-label {
    color: #8da8b8;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1px;
}

.metric-value {
    color: #f2fbff;

    font-size: 30px;

    font-weight: 800;

    margin-top: 5px;
}

.metric-small {
    color: #6fead2;

    font-size: 12px;

    margin-top: 5px;
}


/* ============================================================
   INFORMATION BOX
   ============================================================ */

.info-box {
    background:
        rgba(0, 180, 220, 0.07);

    border:
        1px solid rgba(0, 210, 220, 0.20);

    border-radius: 14px;

    padding: 16px;

    color: #b8d4df;

    margin-bottom: 15px;
}


/* ============================================================
   RECOMMENDATION CARDS
   ============================================================ */

.recommendation {
    background:
        linear-gradient(
            135deg,
            rgba(0, 200, 170, 0.10),
            rgba(0, 130, 255, 0.07)
        );

    border-left:
        4px solid #00e6bd;

    border-top:
        1px solid rgba(0, 220, 200, 0.08);

    border-right:
        1px solid rgba(0, 220, 200, 0.08);

    border-bottom:
        1px solid rgba(0, 220, 200, 0.08);

    border-radius: 12px;

    padding: 17px 20px;

    margin-bottom: 12px;

    box-shadow:
        0 6px 20px rgba(0, 0, 0, 0.15);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}

.recommendation:hover {
    transform: translateX(4px);

    box-shadow:
        0 10px 25px rgba(0, 220, 190, 0.08);
}

.recommendation-title {
    color: #74ffe3;

    font-size: 15px;

    font-weight: 700;

    margin-bottom: 6px;
}

.recommendation-text {
    color: #aac2ce;

    font-size: 13px;

    line-height: 1.6;
}


/* ============================================================
   NAVIGATION
   ============================================================ */

div[data-testid="stRadio"] > div {

    background:
        rgba(5, 25, 38, 0.88);

    border:
        1px solid rgba(0, 210, 220, 0.20);

    border-radius: 14px;

    padding: 6px;
}

div[data-testid="stRadio"] label {

    color: #a9c5d1 !important;

    font-weight: 600;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    border-radius: 12px;

    border:
        1px solid rgba(0, 235, 200, 0.35);

    background:
        rgba(0, 180, 160, 0.10);

    color: #75ffe6;

    font-weight: 700;

    transition:
        all 0.25s ease;
}

.stButton > button:hover {

    background:
        rgba(0, 235, 200, 0.18);

    border-color:
        #00e6bd;

    transform:
        translateY(-2px);

    box-shadow:
        0 8px 20px rgba(0, 235, 200, 0.08);
}


/* ============================================================
   DATAFRAME
   ============================================================ */

div[data-testid="stDataFrame"] {

    border-radius: 12px;

    overflow: hidden;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    text-align: center;

    color: #536c79;

    font-size: 12px;

    margin-top: 40px;

    padding-top: 20px;

    border-top:
        1px solid rgba(255,255,255,0.06);
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD ENERGY DATA
# ============================================================

@st.cache_data
def load_energy_data():

    if not PROCESSED_FILE.exists():
        return pd.DataFrame()

    data = pd.read_csv(PROCESSED_FILE)

    return data


# ============================================================
# LOAD ANOMALY DATA
# ============================================================

@st.cache_data
def load_anomaly_data():

    if not ANOMALY_FILE.exists():
        return pd.DataFrame()

    data = pd.read_csv(ANOMALY_FILE)

    return data


df = load_energy_data()

anomaly_df = load_anomaly_data()


# ============================================================
# CHECK DATASET
# ============================================================

if df.empty:

    st.error(
        "Energy dataset was not found.\n\n"
        "Expected file:\n"
        "data/processed/energy_processed.csv"
    )

    st.stop()


# ============================================================
# FIND DATASET COLUMNS
# ============================================================

def find_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


energy_col = find_column([
    "Energy_Consumption_kWh",
    "Energy Consumption",
    "Energy_Consumption",
    "energy_consumption"
])


power_col = find_column([
    "Power_Demand_kW",
    "Power Demand",
    "Power_Demand",
    "power_demand"
])


hvac_col = find_column([
    "HVAC_Usage_kWh",
    "HVAC Usage",
    "HVAC_Usage"
])


lighting_col = find_column([
    "Lighting_Usage_kWh",
    "Lighting Usage",
    "Lighting_Usage"
])


water_col = find_column([
    "Water_Consumption_L",
    "Water Consumption",
    "Water_Consumption"
])


temperature_col = find_column([
    "Temperature_C",
    "Temperature",
    "temperature"
])


humidity_col = find_column([
    "Humidity_Percent",
    "Humidity",
    "humidity"
])


occupancy_col = find_column([
    "Occupancy_Count",
    "Occupancy",
    "occupancy"
])


building_col = find_column([
    "Building_ID",
    "Building",
    "building"
])


timestamp_col = find_column([
    "Timestamp",
    "timestamp",
    "Date"
])


# ============================================================
# PREPARE TIMESTAMP
# ============================================================

if timestamp_col:

    df[timestamp_col] = pd.to_datetime(
        df[timestamp_col],
        errors="coerce"
    )

    df = (
        df
        .sort_values(timestamp_col)
        .reset_index(drop=True)
    )


# ============================================================
# SESSION STATE
# ============================================================

if "current_index" not in st.session_state:

    st.session_state.current_index = 0


# ============================================================
# 15-MINUTE AUTO REFRESH
# ============================================================

refresh_count = st_autorefresh(
    interval=15 * 60 * 1000,
    key="energy_15_minute_refresh"
)


# ============================================================
# MOVE TO NEXT READING AUTOMATICALLY
# ============================================================

if refresh_count > 0:

    st.session_state.current_index = (
        refresh_count % len(df)
    )


# ============================================================
# CURRENT INDEX
# ============================================================

current_index = st.session_state.current_index


if current_index >= len(df):

    current_index = 0

    st.session_state.current_index = 0


current_record = df.iloc[current_index]


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [7, 2]
)


with header_left:

    st.markdown(
        """
        <div class="main-title">
            ⚡ Smart Facility Energy Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
            Agentic AI for Smart Facility Operations and Optimization
        </div>
        """,
        unsafe_allow_html=True
    )


with header_right:

    st.markdown(
        """
        <div style="
            text-align:right;
            margin-top:15px;
        ">
            <span class="live-box">
                <span class="live-dot"></span>
                LIVE MONITORING
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT TIME
# ============================================================

if (
    timestamp_col
    and pd.notna(current_record[timestamp_col])
):

    display_time = (
        current_record[timestamp_col]
        .strftime("%d %b %Y  |  %H:%M")
    )

else:

    display_time = datetime.now().strftime(
        "%d %b %Y  |  %H:%M"
    )


st.caption(
    f"Monitoring interval: 15 minutes  •  "
    f"Current reading: {display_time}"
)


# ============================================================
# TOP NAVIGATION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Navigation
    </div>
    """,
    unsafe_allow_html=True
)


page = st.radio(
    "Select Dashboard Section",

    [
        "Overview",
        "Energy Distribution",
        "Advanced Analytics",
        "Anomaly Detection",
        "Recommendations"
    ],

    horizontal=True,

    label_visibility="collapsed"
)


# ============================================================
# CONTROL AREA
# ============================================================

control_col1, control_col2, control_col3 = st.columns(
    [2, 2, 6]
)


with control_col1:

    if st.button(
        "⚡ Next 15-Min Reading",
        use_container_width=True
    ):

        st.session_state.current_index = (
            st.session_state.current_index + 1
        ) % len(df)

        st.rerun()


with control_col2:

    st.metric(
        "Reading",
        f"{current_index + 1} / {len(df)}"
    )


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_current_value(column):

    if column is None:
        return 0.0

    try:

        return float(
            current_record[column]
        )

    except:

        return 0.0


# ============================================================
# CURRENT VALUES
# ============================================================

current_energy = get_current_value(
    energy_col
)

current_power = get_current_value(
    power_col
)

current_hvac = get_current_value(
    hvac_col
)

current_lighting = get_current_value(
    lighting_col
)

current_water = get_current_value(
    water_col
)

current_temperature = get_current_value(
    temperature_col
)

current_humidity = get_current_value(
    humidity_col
)

current_occupancy = get_current_value(
    occupancy_col
)


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        """
        <div class="section-title">
            Energy Overview
        </div>

        <div class="section-description">
            Real-time simulated facility energy monitoring
            using the processed energy dataset.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MAIN METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    ⚡
                </div>

                <div class="metric-label">
                    CURRENT ENERGY
                </div>

                <div class="metric-value">
                    {current_energy:.2f}
                </div>

                <div class="metric-small">
                    kWh consumption
                </div>

            </div>
            """
        )


    with c2:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🔌
                </div>

                <div class="metric-label">
                    POWER DEMAND
                </div>

                <div class="metric-value">
                    {current_power:.2f}
                </div>

                <div class="metric-small">
                    kW demand
                </div>

            </div>
            """
        )


    with c3:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🌡️
                </div>

                <div class="metric-label">
                    TEMPERATURE
                </div>

                <div class="metric-value">
                    {current_temperature:.1f}°C
                </div>

                <div class="metric-small">
                    Building temperature
                </div>

            </div>
            """
        )


    with c4:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    👥
                </div>

                <div class="metric-label">
                    OCCUPANCY
                </div>

                <div class="metric-value">
                    {current_occupancy:.0f}
                </div>

                <div class="metric-small">
                    People detected
                </div>

            </div>
            """
        )


    # ========================================================
    # FACILITY USAGE
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            Facility Usage
        </div>
        """,
        unsafe_allow_html=True
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    ❄️
                </div>

                <div class="metric-label">
                    HVAC USAGE
                </div>

                <div class="metric-value">
                    {current_hvac:.2f}
                </div>

                <div class="metric-small">
                    kWh
                </div>

            </div>
            """
        )


    with c2:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    💡
                </div>

                <div class="metric-label">
                    LIGHTING
                </div>

                <div class="metric-value">
                    {current_lighting:.2f}
                </div>

                <div class="metric-small">
                    kWh
                </div>

            </div>
            """
        )


    with c3:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    💧
                </div>

                <div class="metric-label">
                    WATER USAGE
                </div>

                <div class="metric-value">
                    {current_water:.2f}
                </div>

                <div class="metric-small">
                    Litres
                </div>

            </div>
            """
        )


    with c4:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    💦
                </div>

                <div class="metric-label">
                    HUMIDITY
                </div>

                <div class="metric-value">
                    {current_humidity:.1f}%
                </div>

                <div class="metric-small">
                    Relative humidity
                </div>

            </div>
            """
        )


    # ========================================================
    # ENERGY TREND
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            Energy Consumption Trend
        </div>
        """,
        unsafe_allow_html=True
    )


    if energy_col:

        chart_df = df.tail(100).copy()


        if timestamp_col:

            fig = px.line(
                chart_df,
                x=timestamp_col,
                y=energy_col,
                title="Energy Consumption Over Time",
                markers=True
            )

        else:

            chart_df["Reading"] = range(
                len(chart_df)
            )

            fig = px.line(
                chart_df,
                x="Reading",
                y=energy_col,
                title="Energy Consumption Over Readings",
                markers=True
            )


        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,20,30,0.5)",
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 2 — ENERGY DISTRIBUTION
# ============================================================

elif page == "Energy Distribution":

    st.markdown(
        """
        <div class="section-title">
            Energy Distribution Analytics
        </div>

        <div class="section-description">
            Analyze how energy is distributed across
            different facility systems.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # COMPONENT DISTRIBUTION
    # ========================================================

    component_values = {}


    if hvac_col:

        component_values["HVAC"] = (
            df[hvac_col].sum()
        )


    if lighting_col:

        component_values["Lighting"] = (
            df[lighting_col].sum()
        )


    if component_values:

        distribution_df = pd.DataFrame(
            {
                "Component":
                    list(component_values.keys()),

                "Energy":
                    list(component_values.values())
            }
        )


        col1, col2 = st.columns(2)


        with col1:

            fig_pie = px.pie(
                distribution_df,
                names="Component",
                values="Energy",
                hole=0.55,
                title="Energy Distribution"
            )


            fig_pie.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                height=430
            )


            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )


        with col2:

            fig_bar = px.bar(
                distribution_df,
                x="Component",
                y="Energy",
                title="Energy Usage by System",
                text_auto=".2f"
            )


            fig_bar.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,20,30,0.5)",
                height=430
            )


            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )


    # ========================================================
    # BUILDING-WISE ENERGY
    # ========================================================

    if building_col and energy_col:

        st.markdown(
            """
            <div class="section-title">
                Building-wise Energy Consumption
            </div>
            """,
            unsafe_allow_html=True
        )


        building_energy = (
            df
            .groupby(building_col)[energy_col]
            .sum()
            .reset_index()
            .sort_values(
                energy_col,
                ascending=False
            )
        )


        fig_building = px.bar(
            building_energy,
            x=building_col,
            y=energy_col,
            title="Total Energy Consumption by Building",
            text_auto=".2f"
        )


        fig_building.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,20,30,0.5)",
            height=450
        )


        st.plotly_chart(
            fig_building,
            use_container_width=True
        )


    # ========================================================
    # ENERGY STATISTICS
    # ========================================================

    if energy_col:

        st.markdown(
            """
            <div class="section-title">
                Energy Statistics
            </div>
            """,
            unsafe_allow_html=True
        )


        avg_energy = df[energy_col].mean()

        max_energy = df[energy_col].max()

        min_energy = df[energy_col].min()

        total_energy = df[energy_col].sum()


        s1, s2, s3, s4 = st.columns(4)


        with s1:

            st.metric(
                "Average Energy",
                f"{avg_energy:.2f} kWh"
            )


        with s2:

            st.metric(
                "Maximum Energy",
                f"{max_energy:.2f} kWh"
            )


        with s3:

            st.metric(
                "Minimum Energy",
                f"{min_energy:.2f} kWh"
            )


        with s4:

            st.metric(
                "Total Energy",
                f"{total_energy:.2f} kWh"
            )


# ============================================================
# PAGE 3 — ADVANCED ANALYTICS
# ============================================================

elif page == "Advanced Analytics":

    st.markdown(
        """
        <div class="section-title">
            Advanced Analytics
        </div>

        <div class="section-description">
            Explore relationships between energy,
            occupancy, temperature and facility usage.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ENERGY VS OCCUPANCY
    # ========================================================

    if energy_col and occupancy_col:

        st.markdown(
            """
            <div class="section-title">
                Energy vs Occupancy
            </div>
            """,
            unsafe_allow_html=True
        )


        hover_columns = []

        if building_col:
            hover_columns.append(
                building_col
            )

        if temperature_col:
            hover_columns.append(
                temperature_col
            )

        if humidity_col:
            hover_columns.append(
                humidity_col
            )


        fig_scatter = px.scatter(
            df,
            x=occupancy_col,
            y=energy_col,
            size=power_col
            if power_col
            else None,
            hover_data=hover_columns,
            title="Relationship Between Occupancy and Energy"
        )


        fig_scatter.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,20,30,0.5)",
            height=450
        )


        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )


    # ========================================================
    # TEMPERATURE VS ENERGY
    # ========================================================

    if energy_col and temperature_col:

        st.markdown(
            """
            <div class="section-title">
                Temperature vs Energy
            </div>
            """,
            unsafe_allow_html=True
        )


        fig_temp = px.scatter(
            df,
            x=temperature_col,
            y=energy_col,
            color=occupancy_col
            if occupancy_col
            else None,
            title="Temperature and Energy Relationship"
        )


        fig_temp.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,20,30,0.5)",
            height=450
        )


        st.plotly_chart(
            fig_temp,
            use_container_width=True
        )


    # ========================================================
    # HEXAGON DENSITY
    # ========================================================

    if energy_col and occupancy_col:

        st.markdown(
            """
            <div class="section-title">
                Hexagon Density Analysis
            </div>
            """,
            unsafe_allow_html=True
        )


        st.html(
            """
            <div class="info-box">
                The hexagon density visualization shows
                where energy consumption is concentrated
                across different occupancy levels.
            </div>
            """
        )


        hex_fig = go.Figure()


        hex_fig.add_trace(
            go.Histogram2d(
                x=df[occupancy_col],
                y=df[energy_col],
                colorscale="Viridis",
                nbinsx=12,
                nbinsy=12,
                colorbar=dict(
                    title="Records"
                )
            )
        )


        hex_fig.update_layout(
            title="Energy Concentration by Occupancy",

            xaxis_title="Occupancy Count",

            yaxis_title="Energy Consumption (kWh)",

            template="plotly_dark",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(5,20,30,0.5)",

            height=500
        )


        st.plotly_chart(
            hex_fig,
            use_container_width=True
        )


    # ========================================================
    # CORRELATION MATRIX
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            Correlation Analysis
        </div>
        """,
        unsafe_allow_html=True
    )


    numeric_df = df.select_dtypes(
        include=np.number
    )


    if not numeric_df.empty:

        correlation = numeric_df.corr()


        fig_corr = px.imshow(
            correlation,
            text_auto=".2f",
            aspect="auto",
            title="Feature Correlation Matrix"
        )


        fig_corr.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=600
        )


        st.plotly_chart(
            fig_corr,
            use_container_width=True
        )


# ============================================================
# PAGE 4 — ANOMALY DETECTION
# ============================================================

elif page == "Anomaly Detection":

    st.markdown(
        """
        <div class="section-title">
            🚨 Energy Anomaly Detection
        </div>

        <div class="section-description">
            Identify abnormal energy consumption patterns
            and monitor unusual facility behavior.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # DETERMINE ANOMALY COUNTS
    # ========================================================

    if not anomaly_df.empty:

        anomaly_col = None


        for col in anomaly_df.columns:

            lower = col.lower()


            if (
                "anomaly" in lower
                or "outlier" in lower
                or "abnormal" in lower
            ):

                anomaly_col = col

                break


        if anomaly_col:

            values = anomaly_df[
                anomaly_col
            ]


            def check_anomaly(value):

                if isinstance(
                    value,
                    str
                ):

                    value_lower = (
                        value.lower()
                    )


                    return (
                        "anomaly"
                        in value_lower
                        or
                        "abnormal"
                        in value_lower
                        or
                        value_lower
                        in [
                            "1",
                            "true",
                            "yes"
                        ]
                    )


                return value == 1


            mask = values.apply(
                check_anomaly
            )


            abnormal_count = int(
                mask.sum()
            )


            normal_count = (
                len(anomaly_df)
                - abnormal_count
            )


        else:

            abnormal_count = 0

            normal_count = len(
                anomaly_df
            )


    else:

        if energy_col:

            threshold = (
                df[energy_col].mean()
                +
                2 * df[energy_col].std()
            )


            abnormal_count = int(
                (
                    df[energy_col]
                    > threshold
                ).sum()
            )


            normal_count = (
                len(df)
                -
                abnormal_count
            )

        else:

            abnormal_count = 0

            normal_count = len(df)


    # ========================================================
    # ANOMALY CARDS
    # ========================================================

    a1, a2, a3 = st.columns(3)


    with a1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🟢
                </div>

                <div class="metric-label">
                    NORMAL RECORDS
                </div>

                <div class="metric-value">
                    {normal_count}
                </div>

                <div class="metric-small">
                    Normal energy behavior
                </div>

            </div>
            """
        )


    with a2:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🔴
                </div>

                <div class="metric-label">
                    ABNORMAL RECORDS
                </div>

                <div class="metric-value">
                    {abnormal_count}
                </div>

                <div class="metric-small">
                    Potential anomalies
                </div>

            </div>
            """
        )


    with a3:

        total_records = (
            normal_count
            +
            abnormal_count
        )


        if total_records > 0:

            anomaly_rate = (
                abnormal_count
                /
                total_records
            ) * 100

        else:

            anomaly_rate = 0


        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    📊
                </div>

                <div class="metric-label">
                    ANOMALY RATE
                </div>

                <div class="metric-value">
                    {anomaly_rate:.2f}%
                </div>

                <div class="metric-small">
                    Of monitored records
                </div>

            </div>
            """
        )


    # ========================================================
    # ANOMALY PIE CHART
    # ========================================================

    anomaly_chart_df = pd.DataFrame(
        {
            "Status":
                [
                    "Normal",
                    "Abnormal"
                ],

            "Records":
                [
                    normal_count,
                    abnormal_count
                ]
        }
    )


    fig_anomaly = px.pie(
        anomaly_chart_df,
        names="Status",
        values="Records",
        hole=0.55,
        title="Normal vs Abnormal Energy Records"
    )


    fig_anomaly.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=420
    )


    st.plotly_chart(
        fig_anomaly,
        use_container_width=True
    )


    # ========================================================
    # ANOMALY TREND
    # ========================================================

    if energy_col:

        st.markdown(
            """
            <div class="section-title">
                Energy Anomaly Trend
            </div>
            """,
            unsafe_allow_html=True
        )


        anomaly_plot_df = df.copy()


        threshold = (
            anomaly_plot_df[energy_col].mean()
            +
            2
            *
            anomaly_plot_df[energy_col].std()
        )


        anomaly_plot_df[
            "Threshold"
        ] = threshold


        if timestamp_col:

            fig_anomaly_line = go.Figure()


            fig_anomaly_line.add_trace(
                go.Scatter(
                    x=anomaly_plot_df[
                        timestamp_col
                    ],

                    y=anomaly_plot_df[
                        energy_col
                    ],

                    mode="lines",

                    name="Energy"
                )
            )


            fig_anomaly_line.add_trace(
                go.Scatter(
                    x=anomaly_plot_df[
                        timestamp_col
                    ],

                    y=anomaly_plot_df[
                        "Threshold"
                    ],

                    mode="lines",

                    name="Anomaly Threshold",

                    line=dict(
                        dash="dash"
                    )
                )
            )


            fig_anomaly_line.update_layout(
                title=
                    "Energy Consumption "
                    "and Anomaly Threshold",

                xaxis_title="Time",

                yaxis_title=
                    "Energy (kWh)",

                template="plotly_dark",

                paper_bgcolor=
                    "rgba(0,0,0,0)",

                plot_bgcolor=
                    "rgba(5,20,30,0.5)",

                height=470
            )


            st.plotly_chart(
                fig_anomaly_line,
                use_container_width=True
            )


    # ========================================================
    # ANOMALY RESULTS TABLE
    # ========================================================

    if not anomaly_df.empty:

        st.markdown(
            """
            <div class="section-title">
                Anomaly Detection Results
            </div>
            """,
            unsafe_allow_html=True
        )


        st.dataframe(
            anomaly_df.head(100),

            use_container_width=True,

            height=400
        )


# ============================================================
# PAGE 5 — RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.markdown(
        """
        <div class="section-title">
            🤖 Energy Efficiency Recommendations
        </div>

        <div class="section-description">
            AI-assisted recommendations based on energy
            consumption, occupancy and environmental conditions.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # AVERAGES
    # ========================================================

    avg_energy = (
        df[energy_col].mean()
        if energy_col
        else 0
    )


    avg_occupancy = (
        df[occupancy_col].mean()
        if occupancy_col
        else 0
    )


    avg_temperature = (
        df[temperature_col].mean()
        if temperature_col
        else 0
    )


    avg_hvac = (
        df[hvac_col].mean()
        if hvac_col
        else 0
    )


    # ========================================================
    # RECOMMENDATION 1 — ENERGY
    # ========================================================

    if current_energy > avg_energy:

        st.html(
            f"""
            <div class="recommendation">

                <div class="recommendation-title">
                    ⚡ High Energy Consumption Detected
                </div>

                <div class="recommendation-text">
                    Current energy consumption is
                    <b>{current_energy:.2f} kWh</b>,
                    which is above the dataset average of
                    <b>{avg_energy:.2f} kWh</b>.
                    Consider checking HVAC operation,
                    lighting schedules and unnecessary
                    equipment loads.
                </div>

            </div>
            """
        )

    else:

        st.html(
            f"""
            <div class="recommendation">

                <div class="recommendation-title">
                    ✅ Energy Consumption is Within Normal Range
                </div>

                <div class="recommendation-text">
                    Current consumption of
                    <b>{current_energy:.2f} kWh</b>
                    is at or below the average energy level.
                    Continue monitoring facility usage.
                </div>

            </div>
            """
        )


    # ========================================================
    # RECOMMENDATION 2 — HVAC
    # ========================================================

    if current_hvac > avg_hvac:

        st.html(
            f"""
            <div class="recommendation">

                <div class="recommendation-title">
                    ❄️ HVAC Optimization Recommended
                </div>

                <div class="recommendation-text">
                    HVAC consumption is currently
                    <b>{current_hvac:.2f} kWh</b>.
                    Review temperature settings,
                    HVAC schedules and occupied-zone
                    requirements.
                </div>

            </div>
            """
        )

    else:

        st.html(
            """
            <div class="recommendation">

                <div class="recommendation-title">
                    ❄️ HVAC Performance Appears Stable
                </div>

                <div class="recommendation-text">
                    HVAC consumption is within the
                    observed operating range.
                    Continue monitoring for unexpected
                    increases.
                </div>

            </div>
            """
        )


    # ========================================================
    # RECOMMENDATION 3 — OCCUPANCY
    # ========================================================

    if occupancy_col:

        if current_occupancy < (
            avg_occupancy * 0.5
        ):

            st.html(
                f"""
                <div class="recommendation">

                    <div class="recommendation-title">
                        👥 Low Occupancy Detected
                    </div>

                    <div class="recommendation-text">
                        Current occupancy is only
                        <b>{current_occupancy:.0f}</b>.
                        Consider reducing lighting and
                        HVAC in unused areas.
                    </div>

                </div>
                """
            )

        else:

            st.html(
                """
                <div class="recommendation">

                    <div class="recommendation-title">
                        👥 Occupancy-Based Control
                    </div>

                    <div class="recommendation-text">
                        Facility occupancy is within the
                        normal operating range.
                        Continue using occupancy information
                        to optimize HVAC and lighting.
                    </div>

                </div>
                """
            )


    # ========================================================
    # RECOMMENDATION 4 — TEMPERATURE
    # ========================================================

    if temperature_col:

        if current_temperature > (
            avg_temperature + 2
        ):

            st.html(
                f"""
                <div class="recommendation">

                    <div class="recommendation-title">
                        🌡️ Elevated Temperature
                    </div>

                    <div class="recommendation-text">
                        Current temperature is
                        <b>{current_temperature:.1f}°C</b>,
                        which is above the observed average.
                        HVAC operation should be checked
                        for efficient cooling.
                    </div>

                </div>
                """
            )

        elif current_temperature < (
            avg_temperature - 2
        ):

            st.html(
                f"""
                <div class="recommendation">

                    <div class="recommendation-title">
                        🌡️ Lower Temperature
                    </div>

                    <div class="recommendation-text">
                        Current temperature is
                        <b>{current_temperature:.1f}°C</b>.
                        Avoid excessive heating or cooling
                        to reduce unnecessary energy
                        consumption.
                    </div>

                </div>
                """
            )

        else:

            st.html(
                """
                <div class="recommendation">

                    <div class="recommendation-title">
                        🌡️ Temperature Within Normal Range
                    </div>

                    <div class="recommendation-text">
                        Environmental temperature is
                        relatively stable compared with
                        the observed dataset.
                    </div>

                </div>
                """
            )


    # ========================================================
    # GENERAL ENERGY SAVING ACTIONS
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            General Energy Saving Actions
        </div>
        """,
        unsafe_allow_html=True
    )


    recommendations = [

        (
            "💡 Smart Lighting",

            "Use occupancy-based lighting control "
            "and switch off lights in unoccupied zones."
        ),

        (
            "❄️ HVAC Scheduling",

            "Align HVAC operation with building "
            "occupancy and working hours."
        ),

        (
            "⚡ Peak Demand Management",

            "Monitor high power-demand periods and "
            "shift flexible loads away from peak periods."
        ),

        (
            "📊 Continuous Monitoring",

            "Continue monitoring energy consumption "
            "at 15-minute intervals to identify "
            "abnormal behavior."
        ),

        (
            "🤖 Agentic Decision Support",

            "Use the Energy Agent to analyze incoming "
            "facility data and generate optimization "
            "recommendations."
        )
    ]


    for title, text in recommendations:

        st.html(
            f"""
            <div class="recommendation">

                <div class="recommendation-title">
                    {title}
                </div>

                <div class="recommendation-text">
                    {text}
                </div>

            </div>
            """
        )


# ============================================================
# DATASET INFORMATION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Dataset Information
    </div>
    """,
    unsafe_allow_html=True
)


info1, info2, info3, info4 = st.columns(4)


with info1:

    st.metric(
        "Total Records",
        len(df)
    )


with info2:

    st.metric(
        "Features",
        len(df.columns)
    )


with info3:

    st.metric(
        "Missing Values",
        int(
            df.isnull()
            .sum()
            .sum()
        )
    )


with info4:

    st.metric(
        "Duplicate Records",
        int(
            df.duplicated()
            .sum()
        )
    )


# ============================================================
# CURRENT READING DETAILS
# ============================================================

with st.expander(
    "🔎 View Current Energy Reading"
):

    current_display = (
        current_record
        .to_frame()
        .T
    )


    st.dataframe(
        current_display,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        ⚡ Smart Facility Energy Intelligence
        |

        Agentic AI for Smart Facility Operations
        and Optimization

        |

        Simulated 15-minute energy monitoring

    </div>
    """
)