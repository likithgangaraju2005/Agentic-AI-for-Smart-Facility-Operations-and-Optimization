# ============================================================
# SMART FACILITY INTELLIGENCE
# Infosys Virtual Internship 7.0
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Facility Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

ENERGY_FILE = PROCESSED_DIR / "energy_processed.csv"
ANOMALY_FILE = PROCESSED_DIR / "energy_anomaly_results.csv"

MAINTENANCE_FILE = (
    DATA_DIR
    / "maintenance"
    / "processed"
    / "maintenance_agent_results.csv"
)


# ============================================================
# CUSTOM CSS
# IMPORTANT:
# CSS ONLY — NO HTML UI COMPONENTS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(0, 190, 180, 0.12),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 5%,
            rgba(0, 120, 255, 0.10),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #03141f 0%,
            #061f2d 50%,
            #03141f 100%
        );
}

/* Main container */

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #061a26,
        #03131d
    );
    border-right: 1px solid rgba(0,220,210,.18);
}

section[data-testid="stSidebar"] * {
    color: #dffaff;
}

/* Titles */

h1, h2, h3 {
    color: #ecffff !important;
}

/* Metric cards */

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(8,43,57,.95),
        rgba(4,25,37,.96)
    );
    border: 1px solid rgba(0,220,210,.25);
    border-radius: 16px;
    padding: 20px;
    min-height: 145px;
    box-shadow:
        0 12px 30px rgba(0,0,0,.18);
    transition: all .2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: rgba(0,245,220,.65);
    transform: translateY(-3px);
}

div[data-testid="stMetricLabel"] {
    color: #7898a6 !important;
}

div[data-testid="stMetricValue"] {
    color: #f1ffff !important;
    font-weight: 800;
}

/* Buttons */

.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 10px;
    border: 1px solid rgba(0,225,210,.30);
    background: linear-gradient(
        135deg,
        rgba(0,140,150,.35),
        rgba(0,90,150,.30)
    );
    color: #e9ffff;
    font-weight: 700;
}

.stButton > button:hover {
    border-color: rgba(0,250,225,.80);
    color: white;
}

/* Radio navigation */

div[data-testid="stRadio"] > div {
    gap: 8px;
    flex-wrap: wrap;
}

div[data-testid="stRadio"] label {
    background: rgba(7,35,48,.72);
    border: 1px solid rgba(90,180,200,.18);
    border-radius: 12px;
    padding: 7px 12px;
}

div[data-testid="stRadio"] label:hover {
    border-color: rgba(0,235,210,.65);
}

/* Select boxes */

div[data-baseweb="select"] > div {
    background-color: #092b3a;
    border-color: rgba(0,220,210,.25);
}

/* Expander */

div[data-testid="stExpander"] {
    background: rgba(5,30,43,.70);
    border: 1px solid rgba(0,220,210,.16);
    border-radius: 14px;
}

/* Dataframe */

div[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Alert boxes */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Horizontal line */

hr {
    border-color: rgba(100,200,210,.12);
}

/* Captions */

.stCaption {
    color: #7897a5 !important;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_energy():

    if not ENERGY_FILE.exists():
        return pd.DataFrame()

    data = pd.read_csv(ENERGY_FILE)

    if "Timestamp" in data.columns:
        data["Timestamp"] = pd.to_datetime(
            data["Timestamp"],
            errors="coerce"
        )

    numeric_columns = [
        "Energy_Consumption_kWh",
        "Power_Demand_kW",
        "HVAC_Usage_kWh",
        "Lighting_Usage_kWh",
        "Water_Consumption_L",
        "Temperature_C",
        "Humidity_Percent",
        "Occupancy_Count"
    ]

    for column in numeric_columns:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    return data.sort_values(
        "Timestamp"
    ).reset_index(drop=True)


@st.cache_data
def load_anomaly():

    if not ANOMALY_FILE.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(ANOMALY_FILE)
    except:
        return pd.DataFrame()


@st.cache_data
def load_maintenance():

    if not MAINTENANCE_FILE.exists():
        return pd.DataFrame()

    try:

        data = pd.read_csv(
            MAINTENANCE_FILE
        )

        if "Timestamp" in data.columns:

            data["Timestamp"] = pd.to_datetime(
                data["Timestamp"],
                errors="coerce"
            )

        return data

    except:
        return pd.DataFrame()


energy_df = load_energy()
anomaly_df = load_anomaly()
maintenance_df = load_maintenance()


# ============================================================
# CHECK ENERGY DATA
# ============================================================

if energy_df.empty:

    st.error(
        "Energy dataset not found."
    )

    st.info(
        "Run the energy preprocessing script first."
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "current_index" not in st.session_state:
    st.session_state.current_index = 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚡ Facility AI")

    st.caption(
        "Smart Facility Intelligence"
    )

    st.divider()

    st.subheader("🎛️ Facility Controls")

    if "Building_ID" in energy_df.columns:

        buildings = sorted(
            energy_df["Building_ID"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    else:

        buildings = []

    selected_building = st.selectbox(
        "Building",
        ["All Buildings"] + buildings
    )

    st.divider()

    st.subheader("🔄 Live Monitoring")

    if st.button(
        "⚡ Next 15-Min Reading",
        key="side_next"
    ):

        st.session_state.current_index = (
            st.session_state.current_index + 1
        ) % len(energy_df)

        st.rerun()


    if st.button(
        "🔄 Reset Monitoring",
        key="side_reset"
    ):

        st.session_state.current_index = 0

        st.rerun()


    st.divider()

    st.subheader("📊 System")

    st.write(
        f"Energy Records: **{len(energy_df):,}**"
    )

    if "Building_ID" in energy_df.columns:

        st.write(
            f"Buildings: **{energy_df['Building_ID'].nunique()}**"
        )

    if not maintenance_df.empty:

        if "Asset_ID" in maintenance_df.columns:

            st.write(
                f"Assets: **{maintenance_df['Asset_ID'].nunique()}**"
            )

    st.divider()

    st.subheader("🤖 AI Modules")

    st.write("⚡ Energy Agent")
    st.write("🔧 Maintenance Agent")
    st.write("📊 Facility Analytics")


# ============================================================
# CURRENT READING
# ============================================================

if st.session_state.current_index >= len(energy_df):

    st.session_state.current_index = 0


current = energy_df.iloc[
    st.session_state.current_index
]


def number(column, default=0):

    if column not in current.index:
        return default

    try:

        value = current[column]

        if pd.isna(value):
            return default

        return float(value)

    except:

        return default


current_energy = number(
    "Energy_Consumption_kWh"
)

current_power = number(
    "Power_Demand_kW"
)

current_hvac = number(
    "HVAC_Usage_kWh"
)

current_lighting = number(
    "Lighting_Usage_kWh"
)

current_water = number(
    "Water_Consumption_L"
)

current_temperature = number(
    "Temperature_C"
)

current_humidity = number(
    "Humidity_Percent"
)

current_occupancy = number(
    "Occupancy_Count"
)

current_timestamp = current.get(
    "Timestamp",
    "N/A"
)


# ============================================================
# FILTER ENERGY DATA
# ============================================================

if selected_building == "All Buildings":

    filtered_df = energy_df.copy()

else:

    filtered_df = energy_df[
        energy_df["Building_ID"]
        .astype(str)
        == str(selected_building)
    ].copy()


# ============================================================
# HEADER
# ============================================================

title_col, live_col = st.columns(
    [5, 1]
)

with title_col:

    st.title(
        "⚡ Smart Facility Intelligence"
    )

    st.caption(
        "AI-powered energy monitoring, predictive maintenance "
        "and facility optimization"
    )

with live_col:

    st.success(
        "● LIVE MONITORING"
    )


st.divider()


# ============================================================
# NAVIGATION
# ============================================================

st.subheader(
    "Dashboard Navigation"
)

st.caption(
    "Select a module to explore the facility."
)


pages = [
    "🏠 Facility Overview",
    "⚡ Energy Distribution",
    "📊 Advanced Analytics",
    "🚨 Anomaly Detection",
    "💡 Energy Recommendations",
    "🔧 Predictive Maintenance"
]


page = st.radio(
    "Navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)


st.divider()


# ============================================================
# PAGE 1
# FACILITY OVERVIEW
# ============================================================

if page == "🏠 Facility Overview":

    st.header(
        "🏠 Facility Overview"
    )

    st.caption(
        "Real-time simulated view of facility energy conditions."
    )


    b1,b2,b3 = st.columns(
        [1,1,2]
    )


    with b1:

        if st.button(
            "⚡ Next 15-Min Reading",
            key="overview_next"
        ):

            st.session_state.current_index = (
                st.session_state.current_index + 1
            ) % len(energy_df)

            st.rerun()


    with b2:

        if st.button(
            "🔄 Reset Monitoring",
            key="overview_reset"
        ):

            st.session_state.current_index = 0

            st.rerun()


    with b3:

        st.info(
            f"Current simulated timestamp: "
            f"**{current_timestamp}**"
        )


    st.write("")


    # --------------------------------------------------------
    # KPI ROW 1
    # --------------------------------------------------------

    c1,c2,c3,c4 = st.columns(4)


    with c1:

        st.metric(
            "⚡ Current Energy",
            f"{current_energy:.2f} kWh",
            "Current consumption"
        )


    with c2:

        st.metric(
            "🔌 Power Demand",
            f"{current_power:.2f} kW",
            "Current demand"
        )


    with c3:

        st.metric(
            "❄️ HVAC Usage",
            f"{current_hvac:.2f} kWh",
            "HVAC consumption"
        )


    with c4:

        st.metric(
            "💡 Lighting",
            f"{current_lighting:.2f} kWh",
            "Lighting consumption"
        )


    st.write("")


    # --------------------------------------------------------
    # KPI ROW 2
    # --------------------------------------------------------

    c5,c6,c7,c8 = st.columns(4)


    with c5:

        st.metric(
            "🌡️ Temperature",
            f"{current_temperature:.1f} °C",
            "Current temperature"
        )


    with c6:

        st.metric(
            "💧 Water",
            f"{current_water:.2f} L",
            "Current usage"
        )


    with c7:

        st.metric(
            "👥 Occupancy",
            f"{current_occupancy:.0f}",
            "People"
        )


    with c8:

        avg_energy = filtered_df[
            "Energy_Consumption_kWh"
        ].mean()

        st.metric(
            "📈 Average Energy",
            f"{avg_energy:.2f} kWh",
            "Facility average"
        )


    st.write("")


    # --------------------------------------------------------
    # ENERGY TREND
    # --------------------------------------------------------

    st.subheader(
        "📡 Energy Monitoring"
    )

    st.caption(
        "Recent energy consumption trend."
    )


    recent = filtered_df.tail(60)


    fig = px.line(
        recent,
        x="Timestamp",
        y="Energy_Consumption_kWh",
        markers=True,
        title="Recent Energy Consumption"
    )


    fig.update_layout(
        template="plotly_dark",
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,20,30,.45)",
        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if current_energy > avg_energy * 1.20:

        st.error(
            "🚨 HIGH ENERGY CONSUMPTION — "
            "Current usage is significantly above average."
        )

    elif current_energy > avg_energy:

        st.warning(
            "⚠️ ABOVE AVERAGE — "
            "Current energy usage is higher than normal."
        )

    else:

        st.success(
            "✅ NORMAL ENERGY CONDITION — "
            "Current consumption is within the expected range."
        )


# ============================================================
# PAGE 2
# ENERGY DISTRIBUTION
# ============================================================

elif page == "⚡ Energy Distribution":

    st.header(
        "⚡ Energy Distribution"
    )

    st.caption(
        "Analyze energy usage across facility systems."
    )


    hvac_total = filtered_df[
        "HVAC_Usage_kWh"
    ].sum()

    lighting_total = filtered_df[
        "Lighting_Usage_kWh"
    ].sum()

    energy_total = filtered_df[
        "Energy_Consumption_kWh"
    ].sum()

    other_total = max(
        energy_total
        - hvac_total
        - lighting_total,
        0
    )


    distribution = pd.DataFrame(
        {
            "System": [
                "HVAC",
                "Lighting",
                "Other"
            ],
            "Energy": [
                hvac_total,
                lighting_total,
                other_total
            ]
        }
    )


    c1,c2 = st.columns(2)


    with c1:

        fig = px.pie(
            distribution,
            names="System",
            values="Energy",
            hole=.55,
            title="Energy Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with c2:

        fig = px.bar(
            distribution,
            x="System",
            y="Energy",
            text_auto=".2f",
            title="Energy Usage by System"
        )

        fig.update_layout(
            template="plotly_dark",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader(
        "🏢 Building Energy Comparison"
    )


    if "Building_ID" in filtered_df.columns:

        building_energy = (
            filtered_df
            .groupby("Building_ID")
            ["Energy_Consumption_kWh"]
            .sum()
            .reset_index()
            .sort_values(
                "Energy_Consumption_kWh",
                ascending=False
            )
        )


        fig = px.bar(
            building_energy,
            x="Building_ID",
            y="Energy_Consumption_kWh",
            text_auto=".2f",
            title="Energy Consumption by Building"
        )


        fig.update_layout(
            template="plotly_dark",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 3
# ADVANCED ANALYTICS
# ============================================================

elif page == "📊 Advanced Analytics":

    st.header(
        "📊 Advanced Analytics"
    )

    st.caption(
        "Analyze relationships between energy, temperature and occupancy."
    )


    avg = filtered_df[
        "Energy_Consumption_kWh"
    ].mean()

    peak = filtered_df[
        "Energy_Consumption_kWh"
    ].max()

    minimum = filtered_df[
        "Energy_Consumption_kWh"
    ].min()

    std = filtered_df[
        "Energy_Consumption_kWh"
    ].std()


    a1,a2,a3,a4 = st.columns(4)


    with a1:
        st.metric(
            "📊 Average Energy",
            f"{avg:.2f} kWh"
        )


    with a2:
        st.metric(
            "⬆️ Peak Energy",
            f"{peak:.2f} kWh"
        )


    with a3:
        st.metric(
            "⬇️ Minimum Energy",
            f"{minimum:.2f} kWh"
        )


    with a4:
        st.metric(
            "📐 Variation",
            f"{std:.2f} kWh"
        )


    st.write("")


    # Temperature vs Energy

    st.subheader(
        "🌡️ Temperature vs Energy"
    )


    fig = px.scatter(
        filtered_df,
        x="Temperature_C",
        y="Energy_Consumption_kWh",
        size="Occupancy_Count",
        color="Building_ID"
        if "Building_ID" in filtered_df.columns
        else None,
        title="Temperature vs Energy Consumption"
    )


    fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    c1,c2 = st.columns(2)


    with c1:

        fig = px.scatter(
            filtered_df,
            x="Occupancy_Count",
            y="Energy_Consumption_kWh",
            color="Building_ID"
            if "Building_ID" in filtered_df.columns
            else None,
            title="Energy vs Occupancy"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with c2:

        temp = filtered_df.copy()

        if "Hour" not in temp.columns:

            temp["Hour"] = (
                temp["Timestamp"].dt.hour
            )

        hourly = (
            temp
            .groupby("Hour")
            ["Energy_Consumption_kWh"]
            .mean()
            .reset_index()
        )


        fig = px.bar(
            hourly,
            x="Hour",
            y="Energy_Consumption_kWh",
            title="Average Energy by Hour"
        )


        fig.update_layout(
            template="plotly_dark",
            height=420,
            paper_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Heatmap

    st.subheader(
        "🔥 Energy Usage by Day and Hour"
    )


    heat = filtered_df.copy()

    heat["Hour"] = heat[
        "Timestamp"
    ].dt.hour

    heat["Day"] = heat[
        "Timestamp"
    ].dt.day_name()


    pivot = heat.pivot_table(
        values="Energy_Consumption_kWh",
        index="Day",
        columns="Hour",
        aggfunc="mean"
    )


    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]


    pivot = pivot.reindex(
        [
            day
            for day in days
            if day in pivot.index
        ]
    )


    fig = px.imshow(
        pivot,
        aspect="auto",
        title="Energy Usage Heatmap"
    )


    fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 4
# ANOMALY DETECTION
# ============================================================

elif page == "🚨 Anomaly Detection":

    st.header(
        "🚨 Anomaly Detection"
    )

    st.caption(
        "Identify unusual energy consumption behaviour."
    )


    mean_energy = filtered_df[
        "Energy_Consumption_kWh"
    ].mean()

    std_energy = filtered_df[
        "Energy_Consumption_kWh"
    ].std()


    threshold = (
        mean_energy
        + 2 * std_energy
    )


    abnormal = filtered_df[
        filtered_df[
            "Energy_Consumption_kWh"
        ] > threshold
    ]


    normal_count = (
        len(filtered_df)
        - len(abnormal)
    )

    abnormal_count = len(abnormal)


    c1,c2,c3 = st.columns(3)


    with c1:

        st.metric(
            "🚨 Abnormal Records",
            f"{abnormal_count}"
        )


    with c2:

        st.metric(
            "✅ Normal Records",
            f"{normal_count}"
        )


    with c3:

        anomaly_rate = (
            abnormal_count
            / max(len(filtered_df),1)
        ) * 100

        st.metric(
            "📈 Anomaly Rate",
            f"{anomaly_rate:.2f}%"
        )


    st.write("")


    status_data = pd.DataFrame(
        {
            "Status": [
                "Normal",
                "Abnormal"
            ],
            "Records": [
                normal_count,
                abnormal_count
            ]
        }
    )


    fig = px.pie(
        status_data,
        names="Status",
        values="Records",
        hole=.55,
        title="Normal vs Abnormal Records"
    )


    fig.update_layout(
        template="plotly_dark",
        height=420,
        paper_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader(
        "📈 Anomaly Trend"
    )


    plot_df = filtered_df.copy()

    plot_df["Threshold"] = threshold


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=plot_df["Timestamp"],
            y=plot_df[
                "Energy_Consumption_kWh"
            ],
            mode="lines",
            name="Energy"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=plot_df["Timestamp"],
            y=plot_df["Threshold"],
            mode="lines",
            name="Anomaly Threshold",
            line=dict(
                dash="dash"
            )
        )
    )


    fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,20,30,.45)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    if abnormal_count > 0:

        st.subheader(
            "🚨 Detected Abnormal Readings"
        )

        st.dataframe(
            abnormal.head(100),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE 5
# ENERGY RECOMMENDATIONS
# ============================================================

elif page == "💡 Energy Recommendations":

    st.header(
        "💡 Energy Recommendations"
    )

    st.caption(
        "AI-assisted recommendations based on facility conditions."
    )


    average_energy = filtered_df[
        "Energy_Consumption_kWh"
    ].mean()

    average_hvac = filtered_df[
        "HVAC_Usage_kWh"
    ].mean()

    average_occupancy = filtered_df[
        "Occupancy_Count"
    ].mean()


    # Recommendation 1

    if current_energy > average_energy:

        st.warning(
            "⚡ **High Energy Consumption**\n\n"
            f"Current consumption is "
            f"**{current_energy:.2f} kWh**, "
            f"which is above the average of "
            f"**{average_energy:.2f} kWh**. "
            "Review HVAC schedules, lighting and "
            "unnecessary equipment loads."
        )

    else:

        st.success(
            "✅ **Energy Consumption Normal**\n\n"
            "Current energy usage is within "
            "the expected operating range."
        )


    # Recommendation 2

    if current_hvac > average_hvac:

        st.info(
            "❄️ **HVAC Optimization**\n\n"
            f"Current HVAC usage is "
            f"**{current_hvac:.2f} kWh**. "
            "Review temperature setpoints and "
            "HVAC operating schedules."
        )


    # Recommendation 3

    if current_occupancy < average_occupancy:

        st.info(
            "👥 **Occupancy-Based Control**\n\n"
            f"Current occupancy is "
            f"**{current_occupancy:.0f} people**. "
            "Consider reducing HVAC and lighting "
            "in low-occupancy zones."
        )


    # Recommendation 4

    if current_temperature > 28:

        st.error(
            "🌡️ **Temperature Alert**\n\n"
            f"Current temperature is "
            f"**{current_temperature:.1f} °C**. "
            "High temperature may increase cooling demand."
        )


    st.subheader(
        "🌱 Potential Energy Saving"
    )


    saving = current_energy * 0.10


    c1,c2 = st.columns(2)


    with c1:

        st.metric(
            "🌱 Potential Saving",
            f"{saving:.2f} kWh",
            "10% reduction"
        )


    with c2:

        annual = saving * 4 * 24 * 365

        st.metric(
            "📅 Annualized Estimate",
            f"{annual:,.0f} kWh",
            "Illustrative estimate"
        )


# ============================================================
# PAGE 6
# PREDICTIVE MAINTENANCE
# ============================================================

elif page == "🔧 Predictive Maintenance":

    st.header(
        "🔧 Predictive Maintenance"
    )

    st.caption(
        "AI-driven equipment health monitoring and maintenance alerts."
    )


    if maintenance_df.empty:

        st.warning(
            "Maintenance Agent results were not found."
        )

        st.info(
            "Run: python agents/maintenance_agent.py"
        )

        st.stop()


    maintenance = maintenance_df.copy()


    # --------------------------------------------------------
    # FILTER BUILDING
    # --------------------------------------------------------

    if (
        selected_building != "All Buildings"
        and "Building_ID" in maintenance.columns
    ):

        maintenance = maintenance[
            maintenance["Building_ID"]
            .astype(str)
            == str(selected_building)
        ]


    # --------------------------------------------------------
    # COLUMN DETECTION
    # --------------------------------------------------------

    def find_column(names):

        for name in names:

            if name in maintenance.columns:
                return name

        return None


    asset_col = find_column(
        [
            "Asset_ID",
            "Asset"
        ]
    )


    equipment_col = find_column(
        [
            "Equipment_Type",
            "Equipment"
        ]
    )


    decision_col = find_column(
        [
            "Agent_Decision",
            "Decision",
            "Maintenance_Decision"
        ]
    )


    priority_col = find_column(
        [
            "Maintenance_Priority",
            "Priority"
        ]
    )


    health_col = find_column(
        [
            "Equipment_Health_Score",
            "Health_Score"
        ]
    )


    alert_col = find_column(
        [
            "Agent_Alert",
            "Alert",
            "Maintenance_Alert"
        ]
    )


    schedule_col = find_column(
        [
            "Recommended_Schedule",
            "Maintenance_Schedule",
            "Schedule"
        ]
    )


    # --------------------------------------------------------
    # MAINTENANCE KPIs
    # --------------------------------------------------------

    if asset_col:

        asset_count = maintenance[
            asset_col
        ].nunique()

    else:

        asset_count = len(maintenance)


    immediate = 0
    scheduled = 0
    high_priority = 0


    if decision_col:

        immediate = int(
            maintenance[
                decision_col
            ]
            .astype(str)
            .str.contains(
                "Immediate",
                case=False,
                na=False
            )
            .sum()
        )


        scheduled = int(
            maintenance[
                decision_col
            ]
            .astype(str)
            .str.contains(
                "Schedule",
                case=False,
                na=False
            )
            .sum()
        )


    if priority_col:

        high_priority = int(
            (
                maintenance[
                    priority_col
                ]
                .astype(str)
                .str.upper()
                == "HIGH"
            ).sum()
        )


    k1,k2,k3,k4 = st.columns(4)


    with k1:

        st.metric(
            "🏭 Monitored Assets",
            f"{asset_count}"
        )


    with k2:

        st.metric(
            "🚨 Immediate Maintenance",
            f"{immediate}"
        )


    with k3:

        st.metric(
            "⚠️ Maintenance Soon",
            f"{scheduled}"
        )


    with k4:

        st.metric(
            "🔴 High Priority",
            f"{high_priority}"
        )


    st.write("")


    # --------------------------------------------------------
    # DECISION DISTRIBUTION
    # --------------------------------------------------------

    if decision_col:

        st.subheader(
            "🤖 Maintenance Agent Decisions"
        )

        st.caption(
            "Decisions generated by the Maintenance Agent."
        )


        decision_counts = (
            maintenance[
                decision_col
            ]
            .value_counts()
            .reset_index()
        )


        decision_counts.columns = [
            "Decision",
            "Count"
        ]


        fig = px.bar(
            decision_counts,
            x="Decision",
            y="Count",
            text_auto=True,
            title="Maintenance Decision Distribution"
        )


        fig.update_layout(
            template="plotly_dark",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # HEALTH SCORE
    # --------------------------------------------------------

    if health_col:

        health_values = pd.to_numeric(
            maintenance[
                health_col
            ],
            errors="coerce"
        ).dropna()


        st.subheader(
            "❤️ Equipment Health"
        )


        h1,h2,h3,h4 = st.columns(4)


        with h1:

            st.metric(
                "❤️ Average Health",
                f"{health_values.mean():.1f}/100"
            )


        with h2:

            st.metric(
                "🟢 Best Health",
                f"{health_values.max():.1f}/100"
            )


        with h3:

            st.metric(
                "🔻 Lowest Health",
                f"{health_values.min():.1f}/100"
            )


        with h4:

            critical = int(
                (health_values < 30).sum()
            )

            st.metric(
                "🚨 Critical",
                f"{critical}"
            )


        fig = px.histogram(
            maintenance,
            x=health_col,
            nbins=20,
            title="Equipment Health Distribution"
        )


        fig.update_layout(
            template="plotly_dark",
            height=420,
            paper_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # ALERTS
    # --------------------------------------------------------

    st.subheader(
        "🚨 Maintenance Alerts"
    )


    if alert_col:

        alerts = maintenance[
            maintenance[
                alert_col
            ]
            .astype(str)
            .str.upper()
            .isin(
                [
                    "URGENT ALERT",
                    "MAINTENANCE WARNING"
                ]
            )
        ]

    elif decision_col:

        alerts = maintenance[
            maintenance[
                decision_col
            ]
            .astype(str)
            .str.contains(
                "Immediate|Schedule",
                case=False,
                regex=True,
                na=False
            )
        ]

    else:

        alerts = pd.DataFrame()


    if alerts.empty:

        st.success(
            "✅ No urgent maintenance alerts."
        )

    else:

        for _, row in alerts.head(15).iterrows():

            asset = (
                row[asset_col]
                if asset_col
                else "Equipment"
            )


            equipment = (
                row[equipment_col]
                if equipment_col
                else "Facility Equipment"
            )


            priority = (
                str(row[priority_col]).upper()
                if priority_col
                else "MEDIUM"
            )


            if priority == "HIGH":

                st.error(
                    f"🚨 **{asset} — {equipment}**\n\n"
                    f"Priority: **{priority}**"
                )

            elif priority == "MEDIUM":

                st.warning(
                    f"⚠️ **{asset} — {equipment}**\n\n"
                    f"Priority: **{priority}**"
                )

            else:

                st.info(
                    f"🔧 **{asset} — {equipment}**\n\n"
                    f"Priority: **{priority}**"
                )


            if alert_col:

                st.caption(
                    f"Alert: {row[alert_col]}"
                )


            if schedule_col:

                st.caption(
                    f"Recommended schedule: "
                    f"{row[schedule_col]}"
                )


    # --------------------------------------------------------
    # RESULTS TABLE
    # --------------------------------------------------------

    with st.expander(
        "📋 View Maintenance Agent Results"
    ):

        st.dataframe(
            maintenance,
            use_container_width=True,
            hide_index=True,
            height=450
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚡ Smart Facility Intelligence Dashboard | "
    "Infosys Virtual Internship 7.0 | "
    "Agentic AI for Smart Facility Operations and Optimization"
)