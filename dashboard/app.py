import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import time

# ============================================================
# ENERGY INTELLIGENCE DASHBOARD
# Infosys Virtual Internship 7.0
# Milestone 1 - Energy Intelligence & Monitoring
# ============================================================

st.set_page_config(
    page_title="Energy Intelligence Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_FILE = BASE_DIR / "data" / "processed" / "energy_processed.csv"
ANOMALY_FILE = BASE_DIR / "data" / "processed" / "energy_anomaly_results.csv"
RAW_FILE = BASE_DIR / "data" / "energy_dataset.csv.xlsx"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(0, 255, 200, 0.08), transparent 25%),
            radial-gradient(circle at 90% 20%, rgba(0, 150, 255, 0.08), transparent 25%),
            linear-gradient(135deg, #06141f 0%, #081c2b 45%, #031018 100%);
        color: #eafcff;
    }

    /* Main container */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #06141f 0%, #071d2c 100%);
        border-right: 1px solid rgba(0, 255, 210, 0.15);
    }

    /* Titles */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0;
        background: linear-gradient(90deg, #62fff0, #55bfff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: #8da9b7;
        font-size: 16px;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    /* Live indicator */
    .live-container {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        border-radius: 30px;
        background: rgba(0, 255, 190, 0.07);
        border: 1px solid rgba(0, 255, 190, 0.22);
        width: fit-content;
        margin-bottom: 15px;
    }

    .live-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #00ffc3;
        box-shadow: 0 0 12px #00ffc3;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(0.8);
            opacity: 0.6;
        }
        50% {
            transform: scale(1.25);
            opacity: 1;
        }
        100% {
            transform: scale(0.8);
            opacity: 0.6;
        }
    }

    /* Cards */
    .metric-card {
        background:
            linear-gradient(
                145deg,
                rgba(13, 45, 60, 0.95),
                rgba(5, 25, 38, 0.95)
            );
        border: 1px solid rgba(70, 220, 220, 0.16);
        border-radius: 18px;
        padding: 22px;
        min-height: 145px;
        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.25),
            inset 0 1px rgba(255, 255, 255, 0.03);
        transition: all 0.3s ease;
        animation: cardAppear 0.7s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 220, 0.4);
        box-shadow:
            0 15px 40px rgba(0, 255, 220, 0.12);
    }

    @keyframes cardAppear {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .metric-label {
        color: #89a8b7;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #eaffff;
        font-size: 31px;
        font-weight: 750;
    }

    .metric-unit {
        color: #6d8e9d;
        font-size: 13px;
    }

    .metric-icon {
        font-size: 25px;
        float: right;
    }

    /* Section headers */
    .section-title {
        font-size: 23px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 8px;
        color: #dffcff;
    }

    .section-description {
        color: #7894a2;
        margin-bottom: 18px;
    }

    /* Recommendation */
    .recommendation {
        padding: 18px;
        margin: 10px 0;
        border-radius: 14px;
        background: rgba(0, 255, 200, 0.055);
        border-left: 4px solid #00e6bd;
        color: #c8e9ed;
    }

    /* Status */
    .status-good {
        color: #00ffc3;
        font-weight: 700;
    }

    .status-warning {
        color: #ffc857;
        font-weight: 700;
    }

    .status-danger {
        color: #ff657a;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 220, 0.25);
        background: linear-gradient(
            135deg,
            rgba(0, 180, 170, 0.25),
            rgba(0, 100, 160, 0.25)
        );
        color: #dfffff;
        font-weight: 650;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: #00ffc3;
        box-shadow: 0 8px 25px rgba(0, 255, 210, 0.12);
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background: rgba(6, 29, 42, 0.8);
        border: 1px solid rgba(80, 210, 220, 0.13);
        border-radius: 15px;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #557481;
        padding: 30px 0 10px 0;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data(ttl=30)
def load_processed_data():
    if not PROCESSED_FILE.exists():
        return None

    df = pd.read_csv(PROCESSED_FILE)

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

    return df


@st.cache_data(ttl=30)
def load_anomaly_data():
    if not ANOMALY_FILE.exists():
        return None

    df = pd.read_csv(ANOMALY_FILE)

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

    return df


df = load_processed_data()
anomaly_df = load_anomaly_data()

# ============================================================
# DATA CHECK
# ============================================================

if df is None:
    st.error(
        "energy_processed.csv was not found.\n\n"
        "Please run:\n\n"
        "python scripts/preprocess_data.py"
    )
    st.stop()

# ============================================================
# SESSION STATE
# ============================================================

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

if "auto_mode" not in st.session_state:
    st.session_state.auto_mode = True

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:26px;
            font-weight:800;
            color:#63fff0;
            margin-bottom:5px;">
            ⚡ ENERGY AI
        </div>
        <div style="
            color:#7795a4;
            font-size:13px;
            margin-bottom:25px;">
            Smart Facility Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🎛️ Monitoring Controls")

    building_options = ["All Buildings"]

    if "Building_ID" in df.columns:
        building_options += sorted(
            df["Building_ID"].dropna().unique().tolist()
        )

    selected_building = st.selectbox(
        "Select Building",
        building_options
    )

    st.markdown("---")

    st.session_state.auto_mode = st.toggle(
        "🔄 Auto Monitoring",
        value=True
    )

    refresh_seconds = st.slider(
        "Simulation refresh interval",
        min_value=5,
        max_value=60,
        value=15,
        step=5,
        help="Used for dashboard simulation. Dataset readings represent 15-minute intervals."
    )

    st.markdown("---")

    st.markdown("### 📊 Dataset Information")

    st.write(f"Records: **{len(df):,}**")

    if "Building_ID" in df.columns:
        st.write(
            f"Buildings: **{df['Building_ID'].nunique()}**"
        )

    if "Timestamp" in df.columns:
        st.write(
            f"Time range: **{df['Timestamp'].min().date()} → "
            f"{df['Timestamp'].max().date()}**"
        )

    st.markdown("---")

    if st.button("🔄 Reset Monitoring", use_container_width=True):
        st.session_state.current_index = 0
        st.rerun()

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Energy Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered smart facility energy monitoring, analytics and anomaly intelligence'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# LIVE STATUS
# ============================================================

if st.session_state.auto_mode:

    st.markdown(
        """
        <div class="live-container">
            <div class="live-dot"></div>
            <span style="color:#8ffff0;font-weight:700;">
                LIVE MONITORING
            </span>
            <span style="color:#6c8d99;">
                • Simulated IoT stream
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="live-container">
            <div style="
                width:12px;
                height:12px;
                border-radius:50%;
                background:#ffc857;">
            </div>
            <span style="color:#ffc857;font-weight:700;">
                MONITORING PAUSED
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# BUILD CURRENT VIEW
# ============================================================

display_df = df.copy()

if selected_building != "All Buildings":
    display_df = display_df[
        display_df["Building_ID"] == selected_building
    ].copy()

if display_df.empty:
    st.warning("No data available for the selected building.")
    st.stop()

# ============================================================
# CURRENT READING
# ============================================================

# Keep global index inside bounds
st.session_state.current_index = (
    st.session_state.current_index % len(display_df)
)

current_row = display_df.iloc[
    st.session_state.current_index
]

# ============================================================
# CONTROL BUTTONS
# ============================================================

button_col1, button_col2, button_col3 = st.columns(
    [1, 1, 2]
)

with button_col1:

    if st.button(
        "⚡ Next 15-Min Reading",
        use_container_width=True
    ):
        st.session_state.current_index = (
            st.session_state.current_index + 1
        )
        st.session_state.last_update = datetime.now()
        st.rerun()

with button_col2:

    if st.button(
        "⏭️ Next Reading",
        use_container_width=True
    ):
        st.session_state.current_index = (
            st.session_state.current_index + 1
        )
        st.session_state.last_update = datetime.now()
        st.rerun()

with button_col3:

    timestamp_text = (
        current_row["Timestamp"].strftime(
            "%d %b %Y • %H:%M"
        )
        if "Timestamp" in current_row
        and pd.notna(current_row["Timestamp"])
        else "Unknown"
    )

    st.info(
        f"Current simulated timestamp: **{timestamp_text}**"
    )

# ============================================================
# KPI VALUES
# ============================================================

energy = float(
    current_row.get(
        "Energy_Consumption_kWh",
        0
    )
)

power = float(
    current_row.get(
        "Power_Demand_kW",
        0
    )
)

hvac = float(
    current_row.get(
        "HVAC_Usage_kWh",
        0
    )
)

lighting = float(
    current_row.get(
        "Lighting_Usage_kWh",
        0
    )
)

water = float(
    current_row.get(
        "Water_Consumption_L",
        0
    )
)

temperature = float(
    current_row.get(
        "Temperature_C",
        0
    )
)

humidity = float(
    current_row.get(
        "Humidity_Percent",
        0
    )
)

occupancy = int(
    current_row.get(
        "Occupancy_Count",
        0
    )
)

# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">⚡ Live Facility Status</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-label">
                CURRENT ENERGY
            </div>
            <div class="metric-value">
                {energy:.2f}
            </div>
            <div class="metric-unit">
                kWh
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🔌</div>
            <div class="metric-label">
                POWER DEMAND
            </div>
            <div class="metric-value">
                {power:.2f}
            </div>
            <div class="metric-unit">
                kW
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">❄️</div>
            <div class="metric-label">
                HVAC USAGE
            </div>
            <div class="metric-value">
                {hvac:.2f}
            </div>
            <div class="metric-unit">
                kWh
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-label">
                OCCUPANCY
            </div>
            <div class="metric-value">
                {occupancy}
            </div>
            <div class="metric-unit">
                people
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

k5, k6, k7, k8 = st.columns(4)

with k5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">💡</div>
            <div class="metric-label">
                LIGHTING
            </div>
            <div class="metric-value">
                {lighting:.2f}
            </div>
            <div class="metric-unit">
                kWh
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k6:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🌡️</div>
            <div class="metric-label">
                TEMPERATURE
            </div>
            <div class="metric-value">
                {temperature:.1f}
            </div>
            <div class="metric-unit">
                °C
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k7:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">💧</div>
            <div class="metric-label">
                WATER
            </div>
            <div class="metric-value">
                {water:.1f}
            </div>
            <div class="metric-unit">
                Litres
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k8:

    if energy > display_df["Energy_Consumption_kWh"].quantile(0.9):
        status = "HIGH"
        status_class = "status-warning"
    else:
        status = "NORMAL"
        status_class = "status-good"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🟢</div>
            <div class="metric-label">
                ENERGY STATUS
            </div>
            <div class="metric-value">
                <span class="{status_class}">
                    {status}
                </span>
            </div>
            <div class="metric-unit">
                current condition
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# MAIN ENERGY TREND
# ============================================================

st.markdown(
    '<div class="section-title">📈 Energy Consumption Monitoring</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Real-time simulated energy consumption across the facility.'
    '</div>',
    unsafe_allow_html=True
)

chart_df = display_df.copy()

if len(chart_df) > 100:
    chart_df = chart_df.tail(100)

fig_line = px.line(
    chart_df,
    x="Timestamp",
    y="Energy_Consumption_kWh",
    markers=True,
    title="Energy Consumption Over Time"
)

fig_line.update_traces(
    line=dict(width=3),
    marker=dict(size=5)
)

fig_line.update_layout(
    template="plotly_dark",
    height=430,
    margin=dict(l=20, r=20, t=60, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    hovermode="x unified"
)

st.plotly_chart(
    fig_line,
    use_container_width=True
)

# ============================================================
# BUILDING COMPARISON + ENERGY DISTRIBUTION
# ============================================================

st.markdown(
    '<div class="section-title">🏢 Energy Distribution</div>',
    unsafe_allow_html=True
)

col_a, col_b = st.columns(2)

if "Building_ID" in df.columns:

    building_energy = (
        df.groupby("Building_ID")[
            "Energy_Consumption_kWh"
        ]
        .sum()
        .reset_index()
    )

    with col_a:

        fig_bar = px.bar(
            building_energy,
            x="Building_ID",
            y="Energy_Consumption_kWh",
            title="Total Energy by Building",
            text_auto=".1f"
        )

        fig_bar.update_layout(
            template="plotly_dark",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with col_b:

        fig_pie = px.pie(
            building_energy,
            names="Building_ID",
            values="Energy_Consumption_kWh",
            title="Energy Distribution by Building",
            hole=0.48
        )

        fig_pie.update_layout(
            template="plotly_dark",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

# ============================================================
# ENERGY COMPONENT DISTRIBUTION
# ============================================================

component_values = {
    "HVAC": display_df["HVAC_Usage_kWh"].sum(),
    "Lighting": display_df["Lighting_Usage_kWh"].sum(),
    "Other Energy": max(
        0,
        display_df["Energy_Consumption_kWh"].sum()
        - display_df["HVAC_Usage_kWh"].sum()
        - display_df["Lighting_Usage_kWh"].sum()
    )
}

component_df = pd.DataFrame(
    {
        "Component": list(component_values.keys()),
        "Energy": list(component_values.values())
    }
)

fig_component = px.pie(
    component_df,
    names="Component",
    values="Energy",
    title="Energy Component Distribution",
    hole=0.42
)

fig_component.update_layout(
    template="plotly_dark",
    height=420,
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig_component,
    use_container_width=True
)

# ============================================================
# ADVANCED ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">🔬 Advanced Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Explore deeper relationships between energy, occupancy, HVAC, temperature and power demand.'
    '</div>',
    unsafe_allow_html=True
)

with st.expander(
    "🚀 Open Advanced Energy Analytics",
    expanded=False
):

    # --------------------------------------------------------
    # ENERGY VS OCCUPANCY
    # --------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        fig_scatter = px.scatter(
            display_df,
            x="Occupancy_Count",
            y="Energy_Consumption_kWh",
            size="Power_Demand_kW",
            color="Temperature_C",
            hover_data=[
                "Timestamp",
                "Building_ID"
            ],
            title="Energy vs Occupancy"
        )

        fig_scatter.update_layout(
            template="plotly_dark",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

    # --------------------------------------------------------
    # HVAC VS TEMPERATURE
    # --------------------------------------------------------

    with c2:

        fig_hvac = px.scatter(
            display_df,
            x="Temperature_C",
            y="HVAC_Usage_kWh",
            size="Occupancy_Count",
            color="Humidity_Percent",
            title="HVAC Usage vs Temperature"
        )

        fig_hvac.update_layout(
            template="plotly_dark",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_hvac,
            use_container_width=True
        )

    # --------------------------------------------------------
    # HOURLY ENERGY
    # --------------------------------------------------------

    if "Hour" in display_df.columns:

        hourly_energy = (
            display_df.groupby("Hour")[
                "Energy_Consumption_kWh"
            ]
            .mean()
            .reset_index()
        )

    else:

        hourly_energy = (
            display_df.assign(
                Hour=display_df["Timestamp"].dt.hour
            )
            .groupby("Hour")[
                "Energy_Consumption_kWh"
            ]
            .mean()
            .reset_index()
        )

    fig_hour = px.bar(
        hourly_energy,
        x="Hour",
        y="Energy_Consumption_kWh",
        title="Average Energy Consumption by Hour"
    )

    fig_hour.update_layout(
        template="plotly_dark",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )

    # --------------------------------------------------------
    # HEATMAP / HEXAGON-STYLE ANALYSIS
    # --------------------------------------------------------

    st.markdown("### 🔷 Energy Density / Hexbin Analysis")

    hex_df = display_df[
        [
            "Temperature_C",
            "Occupancy_Count",
            "Energy_Consumption_kWh"
        ]
    ].dropna()

    if len(hex_df) > 10:

        fig_hex = px.density_heatmap(
            hex_df,
            x="Temperature_C",
            y="Occupancy_Count",
            z="Energy_Consumption_kWh",
            nbinsx=12,
            nbinsy=12,
            histfunc="avg",
            title="Energy Density by Temperature and Occupancy",
            color_continuous_scale="Turbo"
        )

        fig_hex.update_layout(
            template="plotly_dark",
            height=500,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_hex,
            use_container_width=True
        )

    # --------------------------------------------------------
    # POWER DEMAND TREND
    # --------------------------------------------------------

    power_df = display_df.tail(100)

    fig_power = px.area(
        power_df,
        x="Timestamp",
        y="Power_Demand_kW",
        title="Power Demand Trend"
    )

    fig_power.update_layout(
        template="plotly_dark",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_power,
        use_container_width=True
    )

    # --------------------------------------------------------
    # HVAC + LIGHTING COMPARISON
    # --------------------------------------------------------

    usage_df = display_df[
        [
            "Timestamp",
            "HVAC_Usage_kWh",
            "Lighting_Usage_kWh"
        ]
    ].tail(100)

    fig_usage = go.Figure()

    fig_usage.add_trace(
        go.Scatter(
            x=usage_df["Timestamp"],
            y=usage_df["HVAC_Usage_kWh"],
            mode="lines",
            name="HVAC"
        )
    )

    fig_usage.add_trace(
        go.Scatter(
            x=usage_df["Timestamp"],
            y=usage_df["Lighting_Usage_kWh"],
            mode="lines",
            name="Lighting"
        )
    )

    fig_usage.update_layout(
        title="HVAC vs Lighting Energy Usage",
        template="plotly_dark",
        height=420,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_usage,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CORRELATION MATRIX
    # --------------------------------------------------------

    numeric_cols = [
        "Energy_Consumption_kWh",
        "Power_Demand_kW",
        "HVAC_Usage_kWh",
        "Lighting_Usage_kWh",
        "Water_Consumption_L",
        "Temperature_C",
        "Humidity_Percent",
        "Occupancy_Count"
    ]

    numeric_cols = [
        c for c in numeric_cols
        if c in display_df.columns
    ]

    if len(numeric_cols) >= 2:

        correlation = display_df[
            numeric_cols
        ].corr()

        fig_corr = px.imshow(
            correlation,
            text_auto=".2f",
            aspect="auto",
            title="Energy Feature Correlation Matrix",
            color_continuous_scale="RdBu_r"
        )

        fig_corr.update_layout(
            template="plotly_dark",
            height=600,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_corr,
            use_container_width=True
        )

# ============================================================
# ANOMALY MONITORING
# ============================================================

st.markdown(
    '<div class="section-title">🚨 Energy Anomaly Monitoring</div>',
    unsafe_allow_html=True
)

if anomaly_df is not None:

    anomaly_status_column = None

    possible_status_columns = [
        "Status",
        "Anomaly",
        "Anomaly_Status"
    ]

    for column in possible_status_columns:

        if column in anomaly_df.columns:
            anomaly_status_column = column
            break

    if anomaly_status_column:

        abnormal = anomaly_df[
            anomaly_df[anomaly_status_column]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "abnormal",
                    "anomaly",
                    "true",
                    "1"
                ]
            )
        ]

        normal_count = len(
            anomaly_df
        ) - len(abnormal)

        abnormal_count = len(abnormal)

    else:

        normal_count = len(anomaly_df)
        abnormal_count = 0

    a1, a2, a3 = st.columns(3)

    with a1:

        st.metric(
            "Normal Records",
            f"{normal_count:,}"
        )

    with a2:

        st.metric(
            "Abnormal Records",
            f"{abnormal_count:,}"
        )

    with a3:

        anomaly_percentage = (
            abnormal_count / len(anomaly_df) * 100
            if len(anomaly_df) > 0
            else 0
        )

        st.metric(
            "Anomaly Rate",
            f"{anomaly_percentage:.2f}%"
        )

    if abnormal_count > 0:

        if "Energy_Consumption_kWh" in abnormal.columns:

            fig_anomaly = px.scatter(
                anomaly_df,
                x="Timestamp",
                y="Energy_Consumption_kWh",
                color=anomaly_status_column,
                title="Energy Anomaly Detection Timeline",
                hover_data=[
                    c for c in [
                        "Building_ID",
                        "Power_Demand_kW",
                        "HVAC_Usage_kWh",
                        "Occupancy_Count"
                    ]
                    if c in anomaly_df.columns
                ]
            )

            fig_anomaly.update_layout(
                template="plotly_dark",
                height=430,
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig_anomaly,
                use_container_width=True
            )

            st.markdown("### ⚠️ Detected Abnormal Records")

            st.dataframe(
                abnormal.tail(25),
                use_container_width=True,
                hide_index=True
            )

    else:

        st.success(
            "No abnormal energy records detected."
        )

else:

    st.info(
        "Anomaly results file is not available. "
        "Run the anomaly detection script first."
    )

# ============================================================
# ENERGY EFFICIENCY ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🌱 Energy Efficiency Recommendations</div>',
    unsafe_allow_html=True
)

avg_energy = display_df[
    "Energy_Consumption_kWh"
].mean()

avg_hvac = display_df[
    "HVAC_Usage_kWh"
].mean()

avg_lighting = display_df[
    "Lighting_Usage_kWh"
].mean()

avg_occupancy = display_df[
    "Occupancy_Count"
].mean()

recommendations = []

if avg_hvac > avg_energy * 0.35:

    recommendations.append(
        "❄️ HVAC consumption is relatively high. "
        "Review HVAC schedules and temperature setpoints."
    )

if avg_lighting > avg_energy * 0.20:

    recommendations.append(
        "💡 Lighting contributes significantly to energy usage. "
        "Consider occupancy-based lighting control."
    )

if avg_occupancy < 20:

    recommendations.append(
        "👥 Average occupancy is low. "
        "Consider automatic HVAC and lighting setback during low-occupancy periods."
    )

if temperature > 27:

    recommendations.append(
        "🌡️ Current temperature is relatively high. "
        "Review cooling requirements and HVAC efficiency."
    )

if not recommendations:

    recommendations.append(
        "✅ Current operating conditions appear reasonably efficient. "
        "Continue monitoring energy trends and anomalies."
    )

for recommendation in recommendations:

    st.markdown(
        f"""
        <div class="recommendation">
            {recommendation}
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# CURRENT DATA RECORD
# ============================================================

with st.expander(
    "📋 View Current 15-Minute Sensor Record"
):

    current_display = current_row.to_frame().T

    st.dataframe(
        current_display,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# MONITORING INFORMATION
# ============================================================

st.markdown("---")

info1, info2, info3 = st.columns(3)

with info1:

    st.write(
        f"**Current record:** "
        f"{st.session_state.current_index + 1} / {len(display_df)}"
    )

with info2:

    st.write(
        f"**Last dashboard update:** "
        f"{st.session_state.last_update.strftime('%H:%M:%S')}"
    )

with info3:

    if "Timestamp" in current_row:

        st.write(
            f"**Dataset timestamp:** "
            f"{current_row['Timestamp']}"
        )

# ============================================================
# AUTOMATIC SIMULATED MONITORING
# ============================================================

if st.session_state.auto_mode:

    # Wait before automatically advancing.
    # This simulates a live monitoring stream.
    time.sleep(refresh_seconds)

    st.session_state.current_index = (
        st.session_state.current_index + 1
    )

    st.session_state.last_update = datetime.now()

    st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    unsafe_allow_html=True
)