import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import calendar

# =============================================================================
# PAGE CONFIGURATION & CUSTOM STYLING
# =============================================================================

st.set_page_config(
    page_title="Verve • Fitness Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for a beautiful, modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    
    /* Root variables for consistent theming */
    :root {
        --primary-coral: #FF6B6B;
        --primary-teal: #4ECDC4;
        --primary-navy: #1A1A2E;
        --primary-purple: #6C63FF;
        --accent-gold: #FFD93D;
        --accent-pink: #FF8FB1;
        --bg-dark: #0F0F1A;
        --bg-card: #1A1A2E;
        --bg-card-hover: #252542;
        --text-primary: #FFFFFF;
        --text-secondary: #A0A0B0;
        --text-muted: #6B6B80;
        --gradient-1: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        --gradient-2: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        --gradient-3: linear-gradient(135deg, #6C63FF 0%, #4834DF 100%);
        --gradient-4: linear-gradient(135deg, #FFD93D 0%, #FF6B6B 100%);
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(180deg, #0F0F1A 0%, #1A1A2E 50%, #0F0F1A 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide the default page navigation in sidebar */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Keep sidebar toggle button visible */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
    }
    
    button[kind="header"] {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Fix Material Icons rendering */
    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
    }
    
    
    /* Main content area */
    .main .block-container {
        padding: 1rem 3rem 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Reduce top header space */
    header[data-testid="stHeader"] {
        height: 0;
        min-height: 0;
    }
    
    /* Custom headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-primary) !important;
    }
    
    h1 {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #6C63FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-top: 2rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(78, 205, 196, 0.3);
    }
    
    h3 {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }
    
    /* Paragraphs and text */
    p, .stMarkdown, label {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-secondary);
    }
    
    /* Apply Outfit font to content spans only */
    .main span, 
    [data-testid="stSidebar"] .stMarkdown span {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Ensure sidebar toggle button uses default Streamlit icons */
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] * {
        font-family: unset !important;
    }
    
    [data-testid="baseButton-header"],
    [data-testid="baseButton-header"] * {
        font-family: unset !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #0F0F1A 100%);
        border-right: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
        font-family: 'Outfit', sans-serif !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.2rem !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stSidebar"] h1 {
        color: var(--text-primary) !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-secondary);
    }
    
    /* Compact sidebar inputs */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stDateInput {
        margin-bottom: 0.3rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        font-size: 0.8rem !important;
        margin-bottom: 0.1rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        margin-bottom: 0.1rem !important;
    }
    
    /* Reduce vertical gaps between sidebar elements */
    [data-testid="stSidebar"] .stElementContainer {
        margin-bottom: 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        gap: 0.3rem !important;
    }
    
    /* Metric cards styling */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #1A1A2E 0%, #252542 100%);
        border: 1px solid rgba(78, 205, 196, 0.2);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(78, 205, 196, 0.5);
        box-shadow: 0 8px 30px rgba(78, 205, 196, 0.15);
    }
    
    [data-testid="stMetric"] label {
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--gradient-2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(78, 205, 196, 0.4);
    }
    
    /* Selectbox and multiselect styling */
    [data-testid="stMultiSelect"], 
    [data-testid="stSelectbox"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stMultiSelect > div > div,
    .stSelectbox > div > div {
        background: var(--bg-card);
        border: 1px solid rgba(78, 205, 196, 0.3);
        border-radius: 10px;
    }
    
    /* Date input styling */
    .stDateInput > div > div {
        background: var(--bg-card);
        border: 1px solid rgba(78, 205, 196, 0.3);
        border-radius: 10px;
    }
    
    /* Hide the date range presets dropdown in date input */
    [data-testid="stDateInput"] [data-testid="stSelectbox"],
    [data-testid="stDateInput"] [data-baseweb="select"],
    .stDateInput [data-baseweb="select"],
    .stDateInput [role="listbox"],
    [data-testid="stDateInput"] select,
    [data-testid="stDateInput-Popover"] [data-baseweb="select"],
    div[data-testid="stDateInput"] > div > div > div:first-child:has([data-baseweb="select"]) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* Also hide any preset/range selector in the popover */
    [data-baseweb="calendar"] [data-baseweb="select"],
    [data-baseweb="datepicker"] [data-baseweb="select"] {
        display: none !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border-radius: 12px;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card);
        border-radius: 10px;
        color: var(--text-secondary) !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        padding: 10px 20px;
        border: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-2) !important;
        color: white !important;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] div {
        color: white !important;
    }
    
    .stTabs button[aria-selected="true"] {
        color: white !important;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background: var(--bg-card);
        border-radius: 12px;
        border: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    /* Plot container styling */
    .js-plotly-plot {
        border-radius: 16px;
    }
    
    /* Custom card class */
    .custom-card {
        background: linear-gradient(145deg, #1A1A2E 0%, #252542 100%);
        border: 1px solid rgba(78, 205, 196, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Hero stats styling */
    .hero-stat {
        text-align: center;
        padding: 1rem;
    }
    
    .hero-stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-stat-label {
        font-size: 0.9rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }
    
    /* Achievement badge */
    .achievement-badge {
        display: inline-block;
        background: var(--gradient-4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    /* Streak fire animation */
    @keyframes flame {
        0%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(1.1); }
    }
    
    .streak-fire {
        animation: flame 0.5s ease-in-out infinite;
        display: inline-block;
    }
    
    /* Progress ring container */
    .progress-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    
    /* Glow effect */
    .glow-teal {
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
    }
    
    .glow-coral {
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Info boxes */
    .stAlert {
        background: var(--bg-card);
        border: 1px solid rgba(78, 205, 196, 0.3);
        border-radius: 12px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-teal);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-coral);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# COLOR PALETTE & CHART THEME
# =============================================================================

COLORS = {
    'coral': '#FF6B6B',
    'teal': '#4ECDC4',
    'navy': '#1A1A2E',
    'purple': '#6C63FF',
    'gold': '#FFD93D',
    'pink': '#FF8FB1',
    'green': '#44A08D',
    'orange': '#FF8E53',
    'blue': '#5B8DEE',
    'mint': '#6FEDD6',
}

ACTIVITY_COLORS = {
    'Walking': COLORS['teal'],
    'Running': COLORS['coral'],
    'Cycling': COLORS['purple'],
    'Paced Walking': COLORS['gold'],
    'Inactive': COLORS['navy'],
}

# Plotly chart template
CHART_TEMPLATE = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'family': 'Outfit, sans-serif', 'color': '#A0A0B0'},
        'title': {'font': {'size': 18, 'color': '#FFFFFF'}},
        'xaxis': {
            'gridcolor': 'rgba(78, 205, 196, 0.1)',
            'zerolinecolor': 'rgba(78, 205, 196, 0.2)',
        },
        'yaxis': {
            'gridcolor': 'rgba(78, 205, 196, 0.1)',
            'zerolinecolor': 'rgba(78, 205, 196, 0.2)',
        },
        'colorway': [COLORS['teal'], COLORS['coral'], COLORS['purple'], 
                     COLORS['gold'], COLORS['pink'], COLORS['green']],
    }
}

# =============================================================================
# DATA LOADING & PREPROCESSING
# =============================================================================

@st.cache_resource
def get_geocoder():
    return Nominatim(user_agent="Verve_fitness_dashboard")

USE_GEOCODING = True

@st.cache_data
def reverse_geocode(lat, lon):
    """Convert latitude/longitude to city, country"""
    if not USE_GEOCODING:
        return f"Loc ({lat:.2f}, {lon:.2f})"
    
    try:
        geocoder = get_geocoder()
        location = geocoder.reverse(f"{lat}, {lon}", language='en', timeout=3)
        if location and location.raw.get('address'):
            address = location.raw['address']
            city = address.get('city') or address.get('town') or address.get('village') or address.get('municipality') or 'Unknown'
            country = address.get('country', 'Unknown')
            return f"{city}, {country}"
        return f"Loc ({lat:.2f}, {lon:.2f})"
    except:
        return f"Loc ({lat:.2f}, {lon:.2f})"

@st.cache_data
def batch_reverse_geocode(coordinates_list):
    """Batch process unique coordinates"""
    results = {}
    for lat, lon in coordinates_list:
        key = (round(lat, 2), round(lon, 2))
        if key not in results:
            results[key] = reverse_geocode(key[0], key[1])
    return results

@st.cache_data
def load_data():
    """Load and preprocess fitness data"""
    df = pd.read_csv('fitness_data.csv', sep=',')
    
    # Convert date column (CSV uses DD/MM/YY format)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, format='%d/%m/%y').dt.normalize()
    
    # Parse start and end times
    df['Start time'] = pd.to_datetime(df['Start time'], format='%H:%M:%S.%f', errors='coerce')
    df['End time'] = pd.to_datetime(df['End time'], format='%H:%M:%S.%f', errors='coerce')
    
    # Extract hour of day for time analysis
    df['Hour'] = df['Start time'].dt.hour
    
    # Create activity type
    def get_activity_type(row):
        activities = []
        if pd.notna(row.get('Walking duration (ms)', 0)) and row.get('Walking duration (ms)', 0) > 0:
            activities.append('Walking')
        if pd.notna(row.get('Cycling duration (ms)', 0)) and row.get('Cycling duration (ms)', 0) > 0:
            activities.append('Cycling')
        if pd.notna(row.get('Paced walking duration (ms)', 0)) and row.get('Paced walking duration (ms)', 0) > 0:
            activities.append('Paced Walking')
        if pd.notna(row.get('Running duration (ms)', 0)) and row.get('Running duration (ms)', 0) > 0:
            activities.append('Running')
        return ', '.join(activities) if activities else 'Inactive'
    
    df['Activity Type'] = df.apply(get_activity_type, axis=1)
    
    # Get primary activity (the one with most duration)
    def get_primary_activity(row):
        durations = {
            'Walking': row.get('Walking duration (ms)', 0) or 0,
            'Cycling': row.get('Cycling duration (ms)', 0) or 0,
            'Paced Walking': row.get('Paced walking duration (ms)', 0) or 0,
            'Running': row.get('Running duration (ms)', 0) or 0,
        }
        max_activity = max(durations, key=durations.get)
        return max_activity if durations[max_activity] > 0 else 'Inactive'
    
    df['Primary Activity'] = df.apply(get_primary_activity, axis=1)
    
    # Calculate total exercise duration in minutes
    df['Total Exercise (min)'] = (
        df['Walking duration (ms)'].fillna(0) +
        df['Cycling duration (ms)'].fillna(0) +
        df['Paced walking duration (ms)'].fillna(0) +
        df['Running duration (ms)'].fillna(0)
    ) / 60000
    
    # Round coordinates for geocoding
    df['lat_rounded'] = df['Low latitude (deg)'].round(2)
    df['lon_rounded'] = df['Low longitude (deg)'].round(2)
    
    unique_coords = df[['lat_rounded', 'lon_rounded']].drop_duplicates().dropna().values.tolist()
    
    if len(unique_coords) > 3 and USE_GEOCODING:
        with st.spinner(f'🌍 Loading location data for {len(unique_coords)} unique locations...'):
            location_map = batch_reverse_geocode(unique_coords)
    else:
        location_map = batch_reverse_geocode(unique_coords)
    
    df['Location'] = df.apply(
        lambda x: location_map.get((round(x['Low latitude (deg)'], 2), round(x['Low longitude (deg)'], 2)), "Unknown") 
        if pd.notna(x['Low latitude (deg)']) and pd.notna(x['Low longitude (deg)'])
        else "Unknown",
        axis=1
    )
    
    df = df.drop(columns=['lat_rounded', 'lon_rounded'])
    
    # Extract year, month, day of week for analysis
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month Name'] = df['Date'].dt.strftime('%B')
    df['Day of Week'] = df['Date'].dt.dayofweek
    df['Day Name'] = df['Date'].dt.strftime('%A')
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Is Weekend'] = df['Day of Week'].isin([5, 6])  # Saturday=5, Sunday=6
    
    return df

# Load the data
df = load_data()

# =============================================================================
# SIDEBAR - FILTERS & NAVIGATION
# =============================================================================

with st.sidebar:
    # Logo/Brand
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 0 0.5rem 0;">
        <h1 style="font-size: 3rem; margin: 0; background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; letter-spacing: -1px;">⚡ Verve</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    total_days = (df['Date'].max() - df['Date'].min()).days
    years_tracking = total_days / 365.25
    
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1A1A2E, #252542); border-radius: 8px; padding: 0.5rem 0.7rem; margin-bottom: 0.5rem; border: 1px solid rgba(78, 205, 196, 0.2);">
        <p style="color: #6B6B80; font-size: 0.65rem; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">Tracking Since</p>
        <p style="color: #4ECDC4; font-size: 0.95rem; font-weight: 600; margin: 0.1rem 0 0 0;">{df['Date'].min().strftime('%d %b %Y')} <span style="color: #A0A0B0; font-size: 0.75rem;">({years_tracking:.1f} yrs)</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #A0A0B0; font-size: 0.75rem; font-weight: 600; margin: 0.3rem 0 0.2rem 0; text-transform: uppercase; letter-spacing: 0.5px;">Date Filters</p>', unsafe_allow_html=True)
    
    # Date Range Presets
    preset = st.selectbox(
        "Quick Select",
        ["Custom", "Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year", "All Time"],
        index=0
    )
    
    max_date = df['Date'].max()
    min_date = df['Date'].min()
    
    if preset == "Last 7 Days":
        default_start = max_date - timedelta(days=6)  # 7 days including end date
        default_end = max_date
    elif preset == "Last 30 Days":
        default_start = max_date - timedelta(days=29)  # 30 days including end date
        default_end = max_date
    elif preset == "Last 90 Days":
        default_start = max_date - timedelta(days=89)  # 90 days including end date
        default_end = max_date
    elif preset == "This Year":
        default_start = pd.Timestamp(f"{max_date.year}-01-01")
        default_end = max_date
    elif preset == "All Time":
        default_start = min_date
        default_end = max_date
    else:
        # Custom - default to last month
        default_start = max_date - timedelta(days=29)
        default_end = max_date
    
    # Date Range Filter
    date_range = st.date_input(
        "Date Range",
        value=(default_start.date(), default_end.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
        format="DD/MM/YYYY"
    )
    
    # Activity Type Filter
    st.markdown('<p style="color: #A0A0B0; font-size: 0.75rem; font-weight: 600; margin: 0.5rem 0 0.2rem 0; text-transform: uppercase; letter-spacing: 0.5px;">Activities</p>', unsafe_allow_html=True)
    all_activities = ['Walking', 'Cycling', 'Paced Walking', 'Running']
    selected_activities = st.multiselect(
        "Select Activities",
        options=all_activities,
        default=all_activities,
        label_visibility="collapsed"
    )
    
    # Location Filter
    st.markdown('<p style="color: #A0A0B0; font-size: 0.75rem; font-weight: 600; margin: 0.5rem 0 0.2rem 0; text-transform: uppercase; letter-spacing: 0.5px;">Locations</p>', unsafe_allow_html=True)
    unique_locations = sorted([loc for loc in df['Location'].unique() if loc != "Unknown"])
    selected_locations = st.multiselect(
        "Select Locations",
        options=unique_locations,
        default=unique_locations[:10] if len(unique_locations) > 10 else unique_locations,
        label_visibility="collapsed"
    )

# =============================================================================
# FILTER DATA
# =============================================================================

if len(date_range) == 2:
    filtered_df = df[
        (df['Date'] >= pd.Timestamp(date_range[0])) &
        (df['Date'] <= pd.Timestamp(date_range[1]))
    ]
else:
    filtered_df = df.copy()

# Filter by activity type
if selected_activities:
    filtered_df = filtered_df[filtered_df['Activity Type'].apply(
        lambda x: any(act in x for act in selected_activities)
    )]

# Filter by location
if selected_locations:
    filtered_df = filtered_df[
        (filtered_df['Location'].isin(selected_locations)) | 
        (filtered_df['Location'] == "Unknown")
    ]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_progress_ring(value, max_value, label, color, size=150):
    """Create an SVG progress ring"""
    percentage = min(value / max_value * 100, 100) if max_value > 0 else 0
    stroke_dasharray = 2 * 3.14159 * 45
    stroke_dashoffset = stroke_dasharray * (1 - percentage / 100)
    
    return f"""
    <div style="text-align: center;">
        <svg width="{size}" height="{size}" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="45" fill="none" stroke="rgba(78, 205, 196, 0.1)" stroke-width="10"/>
            <circle cx="60" cy="60" r="45" fill="none" stroke="{color}" stroke-width="10"
                    stroke-dasharray="{stroke_dasharray}" stroke-dashoffset="{stroke_dashoffset}"
                    stroke-linecap="round" transform="rotate(-90 60 60)"
                    style="transition: stroke-dashoffset 1s ease-in-out;"/>
            <text x="60" y="55" text-anchor="middle" fill="white" font-size="20" font-weight="700" font-family="Outfit">{value:,.0f}</text>
            <text x="60" y="72" text-anchor="middle" fill="#6B6B80" font-size="9" font-family="Outfit">{label}</text>
        </svg>
    </div>
    """

def format_duration(minutes):
    """Format duration in minutes to human readable string"""
    if minutes < 60:
        return f"{minutes:.0f}m"
    elif minutes < 1440:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:.0f}h {mins:.0f}m"
    else:
        days = minutes // 1440
        hours = (minutes % 1440) // 60
        return f"{days:.0f}d {hours:.0f}h"

def calculate_streak(df):
    """Calculate current and longest workout streaks"""
    if len(df) == 0:
        return 0, 0
    
    active_dates = df[df['Total Exercise (min)'] > 0]['Date'].dt.date.unique()
    active_dates = sorted(active_dates)
    
    if len(active_dates) == 0:
        return 0, 0
    
    # Current streak
    today = datetime.now().date()
    current_streak = 0
    check_date = today
    
    while check_date in active_dates or (check_date == today and today not in active_dates):
        if check_date in active_dates:
            current_streak += 1
        check_date -= timedelta(days=1)
        if current_streak == 0 and check_date not in active_dates:
            break
    
    # Longest streak
    longest_streak = 1
    current_run = 1
    
    for i in range(1, len(active_dates)):
        if (active_dates[i] - active_dates[i-1]).days == 1:
            current_run += 1
            longest_streak = max(longest_streak, current_run)
        else:
            current_run = 1
    
    return current_streak, longest_streak

# =============================================================================
# MAIN DASHBOARD
# =============================================================================

# Header
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1>Your Fitness Journey</h1>
    <p style="color: #A0A0B0; font-size: 1.1rem;">Track, analyze, and celebrate your progress</p>
</div>
""", unsafe_allow_html=True)

if len(filtered_df) == 0:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()

# =============================================================================
# SECTION 1: HERO STATS
# =============================================================================

# Calculate key metrics
daily_agg = filtered_df.groupby('Date').agg({
    'Step count': 'sum',
    'Calories (kcal)': 'sum',
    'Distance (m)': 'sum',
    'Heart Points': 'sum',
    'Total Exercise (min)': 'sum',
}).reset_index()

total_steps = daily_agg['Step count'].sum()
total_calories = daily_agg['Calories (kcal)'].sum()
total_distance = daily_agg['Distance (m)'].sum() / 1000  # Convert to km
total_exercise = daily_agg['Total Exercise (min)'].sum()
total_heart_points = daily_agg['Heart Points'].sum()
avg_daily_steps = daily_agg['Step count'].mean()
active_days = len(daily_agg[daily_agg['Total Exercise (min)'] > 0])
total_days_range = len(daily_agg)

current_streak, longest_streak = calculate_streak(filtered_df)

# Calculate avg daily metrics
avg_daily_distance = total_distance / total_days_range if total_days_range > 0 else 0
avg_daily_calories = total_calories / total_days_range if total_days_range > 0 else 0
avg_daily_exercise = total_exercise / total_days_range if total_days_range > 0 else 0

# Calculate average daily heart points
avg_daily_heart_points = total_heart_points / total_days_range if total_days_range > 0 else 0

# Calculate consecutive days hitting 10,000 steps goal
steps_goal_streak = 0
if len(daily_agg) > 0:
    # Sort by date descending to check from most recent
    sorted_agg = daily_agg.sort_values('Date', ascending=False)
    for _, row in sorted_agg.iterrows():
        if row['Step count'] >= 10000:
            steps_goal_streak += 1
        else:
            break

# Calculate consecutive days hitting 21 heart points goal
heart_goal_streak = 0
if len(daily_agg) > 0:
    for _, row in sorted_agg.iterrows():
        if row['Heart Points'] >= 21:
            heart_goal_streak += 1
        else:
            break

# Hero Stats Row - Custom HTML to avoid delta arrows
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    streak_emoji = "🔥" if steps_goal_streak > 0 else "📈"
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1A1A2E 0%, #252542 100%); border: 1px solid rgba(78, 205, 196, 0.2); border-radius: 16px; padding: 1.2rem 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; min-height: 120px;">
        <p style="color: #6B6B80; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; white-space: nowrap;">Avg Steps/Day</p>
        <p style="color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 0.5rem 0 0.3rem 0; font-family: 'Outfit', sans-serif;">{avg_daily_steps:,.0f}</p>
        <p style="color: #A0A0B0; font-size: 0.85rem; margin: 0;">{streak_emoji} {steps_goal_streak} day 10K streak</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1A1A2E 0%, #252542 100%); border: 1px solid rgba(78, 205, 196, 0.2); border-radius: 16px; padding: 1.2rem 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; min-height: 120px;">
        <p style="color: #6B6B80; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; white-space: nowrap;">Avg Distance/Day</p>
        <p style="color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 0.5rem 0 0.3rem 0; font-family: 'Outfit', sans-serif;">{avg_daily_distance:.1f} km</p>
        <p style="color: #A0A0B0; font-size: 0.85rem; margin: 0;">Total: {total_distance:,.1f} km</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1A1A2E 0%, #252542 100%); border: 1px solid rgba(78, 205, 196, 0.2); border-radius: 16px; padding: 1.2rem 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; min-height: 120px;">
        <p style="color: #6B6B80; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; white-space: nowrap;">Avg Calories/Day</p>
        <p style="color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 0.5rem 0 0.3rem 0; font-family: 'Outfit', sans-serif;">{avg_daily_calories:,.0f}</p>
        <p style="color: #A0A0B0; font-size: 0.85rem; margin: 0;">Total: {total_calories:,.0f} kcal</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1A1A2E 0%, #252542 100%); border: 1px solid rgba(78, 205, 196, 0.2); border-radius: 16px; padding: 1.2rem 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; min-height: 120px;">
        <p style="color: #6B6B80; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; white-space: nowrap;">Avg Active Time/Day</p>
        <p style="color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 0.5rem 0 0.3rem 0; font-family: 'Outfit', sans-serif;">{format_duration(avg_daily_exercise)}</p>
        <p style="color: #A0A0B0; font-size: 0.85rem; margin: 0;">Total: {format_duration(total_exercise)}</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1A1A2E 0%, #252542 100%); border: 1px solid rgba(78, 205, 196, 0.2); border-radius: 16px; padding: 1.2rem 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; min-height: 120px;">
        <p style="color: #6B6B80; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; white-space: nowrap;">Avg Heart Pts/Day</p>
        <p style="color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 0.5rem 0 0.3rem 0; font-family: 'Outfit', sans-serif;">{avg_daily_heart_points:,.0f}</p>
        <p style="color: #A0A0B0; font-size: 0.85rem; margin: 0;">Total: {total_heart_points:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# SECTION 2: ACTIVITY OVERVIEW
# =============================================================================

st.markdown("## Activity Overview")

col1, col2 = st.columns([1, 2])

with col1:
    # Activity Distribution Donut Chart - Fixed to show all activities
    # Calculate minutes for each activity across ALL rows (not just primary)
    activity_minutes = {
        'Walking': filtered_df['Walking duration (ms)'].fillna(0).sum() / 60000,
        'Cycling': filtered_df['Cycling duration (ms)'].fillna(0).sum() / 60000,
        'Paced Walking': filtered_df['Paced walking duration (ms)'].fillna(0).sum() / 60000,
        'Running': filtered_df['Running duration (ms)'].fillna(0).sum() / 60000,
    }
    
    # Remove activities with 0 minutes
    activity_minutes = {k: v for k, v in activity_minutes.items() if v > 0}
    
    if len(activity_minutes) > 0:
        activity_duration = pd.DataFrame([
            {'Activity': k, 'Minutes': v} for k, v in activity_minutes.items()
        ])
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=activity_duration['Activity'],
            values=activity_duration['Minutes'],
            hole=0.65,
            marker=dict(
                colors=[ACTIVITY_COLORS.get(act, COLORS['teal']) for act in activity_duration['Activity']],
                line=dict(color='#0F0F1A', width=3)
            ),
            textinfo='percent',
            textfont=dict(size=14, color='white', family='Outfit'),
            hovertemplate="<b>%{label}</b><br>%{value:.0f} minutes<br>%{percent}<extra></extra>"
        )])
        
        total_activity_mins = activity_duration['Minutes'].sum()
        
        fig_donut.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='#A0A0B0', size=12)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=60),
            height=350,
            annotations=[dict(
                text=f"<b>{total_activity_mins:,.0f}</b><br>minutes",
                x=0.5, y=0.5,
                font=dict(size=16, color='white', family='Outfit'),
                showarrow=False
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("No activity data available")

with col2:
    # Daily Steps Goal Chart (10,000 steps goal) - Updated with coral line and legend
    steps_timeline = daily_agg.copy()
    steps_timeline = steps_timeline.sort_values('Date')
    
    fig_steps = go.Figure()
    
    # Add bars colored by whether goal was met
    colors = [COLORS['teal'] if steps >= 10000 else COLORS['coral'] 
              for steps in steps_timeline['Step count']]
    
    fig_steps.add_trace(go.Bar(
        x=steps_timeline['Date'],
        y=steps_timeline['Step count'],
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        name='Daily Steps',
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>%{y:,.0f} steps<extra></extra>",
        showlegend=False
    ))
    
    # Add 10,000 steps goal line - changed to coral and added to legend
    fig_steps.add_hline(
        y=10000,
        line_dash="dash",
        line_color=COLORS['coral'],
        line_width=2,
        annotation=None  # Remove annotation from line
    )
    
    # Add invisible trace for legend
    fig_steps.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color=COLORS['coral'], width=2, dash='dash'),
        name='10,000 Steps Goal',
        showlegend=True
    ))
    
    fig_steps.update_layout(
        title=dict(text="Daily Steps vs Goal", font=dict(color='white', size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20),
        height=350,
        xaxis=dict(
            gridcolor='rgba(78, 205, 196, 0.1)',
            tickfont=dict(color='#A0A0B0'),
        ),
        yaxis=dict(
            title=dict(text="Steps", font=dict(color='#A0A0B0')),
            gridcolor='rgba(78, 205, 196, 0.1)',
            tickfont=dict(color='#A0A0B0'),
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color='#A0A0B0', size=11)
        ),
        hovermode='x unified'
    )
    st.plotly_chart(fig_steps, use_container_width=True)


# =============================================================================
# SECTION 4: PATTERNS & INSIGHTS
# =============================================================================

st.markdown("## Patterns & Insights")

col1, col2, col3 = st.columns(3)

with col1:
    # This Week vs Last Week Comparison
    st.markdown("### This Week vs Last Week")
    st.markdown("<p style='color: #6B6B80; font-size: 0.8rem; margin: -10px 0 10px 0;'>Compare your average daily activity between the past two weeks</p>", unsafe_allow_html=True)
    
    compare_data = daily_agg[['Date', 'Total Exercise (min)', 'Step count', 'Calories (kcal)']].copy()
    compare_data = compare_data.sort_values('Date')
    
    if len(compare_data) >= 14:
        # Get last 7 days (this week) and previous 7 days (last week)
        last_14 = compare_data.tail(14)
        last_week = last_14.head(7)
        this_week = last_14.tail(7)
        
        # Calculate averages
        this_week_exercise = this_week['Total Exercise (min)'].mean()
        last_week_exercise = last_week['Total Exercise (min)'].mean()
        this_week_steps = this_week['Step count'].mean()
        last_week_steps = last_week['Step count'].mean()
        
        # Calculate percentage changes
        exercise_change = ((this_week_exercise - last_week_exercise) / last_week_exercise * 100) if last_week_exercise > 0 else 0
        steps_change = ((this_week_steps - last_week_steps) / last_week_steps * 100) if last_week_steps > 0 else 0
        
        fig_compare = go.Figure()
        
        metrics = ['Exercise', 'Steps']
        this_week_vals = [this_week_exercise, this_week_steps / 100]  # Scale steps for visibility
        last_week_vals = [last_week_exercise, last_week_steps / 100]
        
        fig_compare.add_trace(go.Bar(
            name='Last Week',
            x=metrics,
            y=last_week_vals,
            marker_color=COLORS['purple'],
            opacity=0.6,
            text=[f"{last_week_exercise:.0f} min", f"{last_week_steps:,.0f}"],
            textposition='outside',
            textfont=dict(color='#A0A0B0', size=10)
        ))
        
        fig_compare.add_trace(go.Bar(
            name='This Week',
            x=metrics,
            y=this_week_vals,
            marker_color=COLORS['teal'],
            text=[f"{this_week_exercise:.0f} min", f"{this_week_steps:,.0f}"],
            textposition='outside',
            textfont=dict(color='#FFFFFF', size=10)
        ))
        
        fig_compare.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=10),
            height=240,
            xaxis=dict(
                tickfont=dict(color='#A0A0B0', size=11),
            ),
            yaxis=dict(
                visible=False,
                range=[0, max(max(this_week_vals), max(last_week_vals)) * 1.25]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color='#A0A0B0', size=10)
            ),
            bargap=0.25
        )
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # Show change indicators
        exercise_color = COLORS['teal'] if exercise_change >= 0 else COLORS['coral']
        steps_color = COLORS['teal'] if steps_change >= 0 else COLORS['coral']
        exercise_arrow = "↑" if exercise_change >= 0 else "↓"
        steps_arrow = "↑" if steps_change >= 0 else "↓"
        
        st.markdown(f"""
        <div style='display: flex; justify-content: space-around; margin-top: -5px;'>
            <span style='color: {exercise_color}; font-size: 0.85rem;'>{exercise_arrow} {abs(exercise_change):.0f}% exercise</span>
            <span style='color: {steps_color}; font-size: 0.85rem;'>{steps_arrow} {abs(steps_change):.0f}% steps</span>
        </div>
        """, unsafe_allow_html=True)
    elif len(compare_data) >= 7:
        # Only have this week's data
        this_week = compare_data.tail(7)
        this_week_exercise = this_week['Total Exercise (min)'].mean()
        this_week_steps = this_week['Step count'].mean()
        
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem;'>
            <p style='color: #A0A0B0; margin: 0.5rem 0;'>This Week's Average</p>
            <p style='color: {COLORS['teal']}; font-size: 1.5rem; font-weight: 700; margin: 0;'>{this_week_exercise:.0f} min/day</p>
            <p style='color: #6B6B80; font-size: 0.9rem; margin: 0.3rem 0;'>{this_week_steps:,.0f} steps/day</p>
            <p style='color: #6B6B80; font-size: 0.75rem; margin-top: 1rem;'>Need 2 weeks of data for comparison</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Need at least 7 days of data")
    

with col2:
    # Weekly Activity Pattern - Radial Chart
    st.markdown("### Weekly Activity Pattern")
    st.markdown("<p style='color: #6B6B80; font-size: 0.8rem; margin: -10px 0 10px 0;'>See which days you're most active throughout the week</p>", unsafe_allow_html=True)
    
    # First aggregate by date to get daily totals, then average by day of week
    daily_totals = filtered_df.groupby(['Date', 'Day Name']).agg({
        'Total Exercise (min)': 'sum',
        'Step count': 'sum',
        'Calories (kcal)': 'sum'
    }).reset_index()
    
    # Now calculate average per day of week
    daily_pattern = daily_totals.groupby('Day Name').agg({
        'Total Exercise (min)': 'mean',
        'Step count': 'mean',
        'Calories (kcal)': 'mean'
    }).reset_index()
    
    # Ensure all days are present and in correct order (use full names for matching)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_pattern['Day Name'] = pd.Categorical(daily_pattern['Day Name'], categories=day_order, ordered=True)
    daily_pattern = daily_pattern.sort_values('Day Name')
    
    # Fill missing days with 0
    all_days = pd.DataFrame({'Day Name': day_order})
    daily_pattern = all_days.merge(daily_pattern, on='Day Name', how='left').fillna(0)
    
    # Map to short day names for display
    day_short = {'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed', 
                 'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'}
    daily_pattern['Day Short'] = daily_pattern['Day Name'].map(day_short)
    
    # Create radial/polar bar chart
    fig_radial = go.Figure()
    
    # Add polar bar trace with reduced opacity for better axis visibility
    fig_radial.add_trace(go.Barpolar(
        r=daily_pattern['Total Exercise (min)'],
        theta=daily_pattern['Day Short'],
        marker=dict(
            color=daily_pattern['Total Exercise (min)'],
            colorscale=[[0, COLORS['purple']], [0.5, COLORS['teal']], [1, COLORS['coral']]],
            line=dict(color='#0F0F1A', width=2),
            opacity=0.85,
            showscale=False
        ),
        hovertemplate="<b>%{theta}</b><br>%{r:.1f} min avg<extra></extra>",
        text=daily_pattern['Total Exercise (min)'].round(1)
    ))
    
    # Calculate a nice max value for the axis
    max_val = daily_pattern['Total Exercise (min)'].max()
    axis_max = max(max_val * 1.3, 10)  # At least 10 for visibility
    
    fig_radial.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showline=True,
                linewidth=2,
                linecolor='rgba(78, 205, 196, 0.5)',
                gridcolor='rgba(78, 205, 196, 0.3)',
                gridwidth=1.5,
                tickfont=dict(color='#FFFFFF', size=10),
                tickangle=45,
                range=[0, axis_max]
            ),
            angularaxis=dict(
                tickfont=dict(color='#FFFFFF', size=12, family='Outfit'),
                gridcolor='rgba(78, 205, 196, 0.25)',
                gridwidth=1,
                linecolor='rgba(78, 205, 196, 0.4)',
                linewidth=2,
                rotation=90,
                direction='clockwise'
            ),
            bgcolor='rgba(26, 26, 46, 0.3)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        height=320,
        showlegend=False
    )
    st.plotly_chart(fig_radial, use_container_width=True)
    
    # Add unit label below the chart
    st.markdown("<p style='text-align: center; color: #6B6B80; font-size: 0.8rem; margin-top: -15px;'>Average minutes per day</p>", unsafe_allow_html=True)
    

with col3:
    # Time of Day Analysis - Fixed legend overlap and night color
    st.markdown("### Time of Day")
    st.markdown("<p style='color: #6B6B80; font-size: 0.8rem; margin: -10px 0 10px 0;'>Discover your peak activity hours throughout the day</p>", unsafe_allow_html=True)
    
    # Filter out rows without valid hour data
    hourly_data = filtered_df[filtered_df['Hour'].notna()].copy()
    
    if len(hourly_data) > 0:
        hourly_pattern = hourly_data.groupby('Hour').agg({
            'Total Exercise (min)': 'sum'
        }).reset_index()
        
        # Ensure all hours are represented
        all_hours = pd.DataFrame({'Hour': range(24)})
        hourly_pattern = all_hours.merge(hourly_pattern, on='Hour', how='left').fillna(0)
        
        # Create time categories
        def get_time_period(hour):
            if 5 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 21:
                return 'Evening'
            else:
                return 'Night'
        
        hourly_pattern['Period'] = hourly_pattern['Hour'].apply(get_time_period)
        
        # Updated night color to be more visible
        period_colors = {
            'Morning': COLORS['gold'],
            'Afternoon': COLORS['coral'],
            'Evening': COLORS['purple'],
            'Night': COLORS['blue']  # Changed from navy to blue for visibility
        }
        
        fig_hourly = go.Figure()
        
        for period in ['Morning', 'Afternoon', 'Evening', 'Night']:
            period_data = hourly_pattern[hourly_pattern['Period'] == period]
            fig_hourly.add_trace(go.Bar(
                x=period_data['Hour'],
                y=period_data['Total Exercise (min)'],
                name=period,
                marker_color=period_colors[period],
                hovertemplate="%{x}:00<br>%{y:.0f} min<extra></extra>"
            ))
        
        fig_hourly.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=30),
            height=300,
            xaxis=dict(
                tickvals=list(range(0, 24, 3)),
                ticktext=['12am', '3am', '6am', '9am', '12pm', '3pm', '6pm', '9pm'],
                tickfont=dict(color='#A0A0B0'),
                gridcolor='rgba(78, 205, 196, 0.1)'
            ),
            yaxis=dict(
                title=dict(text="Minutes", font=dict(color='#A0A0B0')),
                tickfont=dict(color='#A0A0B0'),
                gridcolor='rgba(78, 205, 196, 0.1)'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color='#A0A0B0', size=11)
            ),
            showlegend=True
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
    else:
        st.info("No time-of-day data available")

# =============================================================================
# SECTION 5: PERSONAL RECORDS
# =============================================================================

st.markdown("## Personal Records")

# Calculate records
daily_records = filtered_df.groupby('Date').agg({
    'Step count': 'sum',
    'Calories (kcal)': 'sum',
    'Distance (m)': 'sum',
    'Total Exercise (min)': 'sum',
    'Heart Points': 'sum',
}).reset_index()

col1, col2, col3 = st.columns(3)

with col1:
    max_steps_row = daily_records.loc[daily_records['Step count'].idxmax()] if len(daily_records) > 0 else None
    if max_steps_row is not None and pd.notna(max_steps_row['Step count']):
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1A1A2E, #252542); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(255, 107, 107, 0.3); box-shadow: 0 0 20px rgba(255, 107, 107, 0.1); text-align: center;">
            <p style="color: #FF6B6B; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">🥇 Most Steps</p>
            <p style="color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{max_steps_row['Step count']:,.0f}</p>
            <p style="color: #6B6B80; font-size: 0.85rem; margin: 0;">{max_steps_row['Date'].strftime('%d %b %Y')}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    max_distance_row = daily_records.loc[daily_records['Distance (m)'].idxmax()] if len(daily_records) > 0 else None
    if max_distance_row is not None and pd.notna(max_distance_row['Distance (m)']):
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1A1A2E, #252542); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(78, 205, 196, 0.3); box-shadow: 0 0 20px rgba(78, 205, 196, 0.1); text-align: center;">
            <p style="color: #4ECDC4; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">🥇 Longest Distance</p>
            <p style="color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{max_distance_row['Distance (m)']/1000:.1f} km</p>
            <p style="color: #6B6B80; font-size: 0.85rem; margin: 0;">{max_distance_row['Date'].strftime('%d %b %Y')}</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    max_calories_row = daily_records.loc[daily_records['Calories (kcal)'].idxmax()] if len(daily_records) > 0 else None
    if max_calories_row is not None and pd.notna(max_calories_row['Calories (kcal)']):
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1A1A2E, #252542); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(108, 99, 255, 0.3); box-shadow: 0 0 20px rgba(108, 99, 255, 0.1); text-align: center;">
            <p style="color: #6C63FF; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">🥇 Most Calories</p>
            <p style="color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{max_calories_row['Calories (kcal)']:,.0f}</p>
            <p style="color: #6B6B80; font-size: 0.85rem; margin: 0;">{max_calories_row['Date'].strftime('%d %b %Y')}</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# SECTION 6: LOCATION ANALYSIS
# =============================================================================

st.markdown("## Location Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(108, 99, 255, 0.1) 100%); border-radius: 12px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; border: 1px solid rgba(78, 205, 196, 0.2);">
        <p style="color: white; font-weight: 600; margin: 0; font-size: 1rem;">📍 Your Activity Hotspots</p>
        <p style="color: #A0A0B0; margin: 0.2rem 0 0 0; font-size: 0.8rem;">Explore where you've been most active</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Map visualization
    map_data = filtered_df[
        (filtered_df['Low latitude (deg)'].notna()) & 
        (filtered_df['Low longitude (deg)'].notna())
    ].copy()
    
    if len(map_data) > 0:
        # Aggregate by location
        location_agg = map_data.groupby(['Low latitude (deg)', 'Low longitude (deg)', 'Location']).agg({
            'Total Exercise (min)': 'sum',
            'Calories (kcal)': 'sum',
            'Step count': 'sum'
        }).reset_index()
        
        # Size based on exercise duration
        max_exercise = location_agg['Total Exercise (min)'].max()
        location_agg['size'] = (location_agg['Total Exercise (min)'] / max_exercise * 30 + 5) if max_exercise > 0 else 10
        
        # Create the map with go.Scattermapbox for better color control
        fig_map = go.Figure()
        
        # Normalize colors based on exercise minutes
        min_exercise = location_agg['Total Exercise (min)'].min()
        exercise_range = max_exercise - min_exercise if max_exercise > min_exercise else 1
        
        fig_map.add_trace(go.Scattermapbox(
            lat=location_agg['Low latitude (deg)'],
            lon=location_agg['Low longitude (deg)'],
            mode='markers',
            marker=dict(
                size=location_agg['size'],
                color=location_agg['Total Exercise (min)'],
                colorscale=[[0, COLORS['purple']], [0.5, COLORS['teal']], [1, COLORS['coral']]],
                cmin=min_exercise,
                cmax=max_exercise,
                showscale=True,
                colorbar=dict(
                    title=dict(text="Minutes", font=dict(color='#A0A0B0')),
                    tickfont=dict(color='#A0A0B0'),
                    bgcolor='rgba(0,0,0,0)',
                    x=0.99
                ),
                opacity=0.9
            ),
            text=location_agg['Location'],
            customdata=np.column_stack((
                location_agg['Total Exercise (min)'],
                location_agg['Calories (kcal)'],
                location_agg['Step count']
            )),
            hovertemplate="<b>%{text}</b><br>" +
                          "Exercise: %{customdata[0]:.0f} min<br>" +
                          "Calories: %{customdata[1]:.0f} kcal<br>" +
                          "Steps: %{customdata[2]:,.0f}<extra></extra>"
        ))
        
        fig_map.update_layout(
            mapbox=dict(
                style="carto-darkmatter",
                center=dict(
                    lat=location_agg['Low latitude (deg)'].mean(),
                    lon=location_agg['Low longitude (deg)'].mean()
                ),
                zoom=3
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No location data available for the selected period")

with col2:
    # Top locations
    st.markdown("### Top Locations")
    st.markdown("<p style='color: #6B6B80; font-size: 0.8rem; margin: -10px 0 10px 0;'>Your most visited workout spots ranked by exercise time</p>", unsafe_allow_html=True)
    
    location_stats = filtered_df.groupby('Location').agg({
        'Total Exercise (min)': 'sum',
        'Step count': 'sum',
        'Calories (kcal)': 'sum'
    }).reset_index()
    location_stats = location_stats[location_stats['Location'] != 'Unknown']
    location_stats = location_stats.sort_values('Total Exercise (min)', ascending=False).head(5)
    
    for idx, row in location_stats.iterrows():
        pct = row['Total Exercise (min)'] / location_stats['Total Exercise (min)'].sum() * 100
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1A1A2E, #252542); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; border-left: 3px solid {COLORS['teal']};">
            <p style="color: white; font-weight: 600; margin: 0; font-size: 0.9rem;">{row['Location']}</p>
            <p style="color: #A0A0B0; margin: 0.2rem 0 0 0; font-size: 0.8rem;">{format_duration(row['Total Exercise (min)'])} • {row['Step count']:,.0f} steps</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# SECTION 7: DETAILED BREAKDOWN
# =============================================================================

st.markdown("## Detailed Breakdown")

tab1, tab2, tab3 = st.tabs(["Exercise by Type", "Heart Health", "Calorie Trends"])

with tab1:
    # Stacked area chart for exercise types over time
    st.markdown("<p style='color: #6B6B80; font-size: 0.85rem; margin: 0 0 15px 0;'>Track how your walking, cycling, running, and paced walking activities change over time</p>", unsafe_allow_html=True)
    exercise_by_type = filtered_df.copy()
    exercise_by_type['Walking (min)'] = exercise_by_type['Walking duration (ms)'].fillna(0) / 60000
    exercise_by_type['Cycling (min)'] = exercise_by_type['Cycling duration (ms)'].fillna(0) / 60000
    exercise_by_type['Paced Walking (min)'] = exercise_by_type['Paced walking duration (ms)'].fillna(0) / 60000
    exercise_by_type['Running (min)'] = exercise_by_type['Running duration (ms)'].fillna(0) / 60000
    
    # Check if only one day is selected - use intra-day intervals instead of daily aggregation
    unique_dates = exercise_by_type['Date'].nunique()
    
    if unique_dates == 1 and 'Start time' in exercise_by_type.columns:
        # Single day: show 15-minute interval breakdown
        exercise_by_type = exercise_by_type.dropna(subset=['Start time'])
        exercise_by_type['Time'] = exercise_by_type['Start time'].dt.strftime('%H:%M')
        daily_exercise = exercise_by_type.sort_values('Start time')
        x_col = 'Time'
        x_title = "Time of Day"
    else:
        # Multiple days: aggregate by date
        daily_exercise = exercise_by_type.groupby('Date').agg({
            'Walking (min)': 'sum',
            'Cycling (min)': 'sum',
            'Paced Walking (min)': 'sum',
            'Running (min)': 'sum'
        }).reset_index().sort_values('Date')
        x_col = 'Date'
        x_title = None
    
    fig_stacked = go.Figure()
    
    for activity, color in [('Walking (min)', COLORS['teal']), 
                            ('Cycling (min)', COLORS['purple']),
                            ('Paced Walking (min)', COLORS['gold']),
                            ('Running (min)', COLORS['coral'])]:
        fig_stacked.add_trace(go.Scatter(
            x=daily_exercise[x_col],
            y=daily_exercise[activity],
            mode='lines+markers' if unique_dates == 1 else 'lines',
            name=activity.replace(' (min)', ''),
            stackgroup='one',
            fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.6)',
            line=dict(width=0.5, color=color),
            marker=dict(size=4, color=color) if unique_dates == 1 else None,
            hovertemplate="%{y:.0f} min<extra></extra>"
        ))
    
    fig_stacked.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=40),
        height=400,
        xaxis=dict(
            tickfont=dict(color='#A0A0B0'),
            gridcolor='rgba(78, 205, 196, 0.1)',
            title=dict(text=x_title, font=dict(color='#A0A0B0')) if x_title else None
        ),
        yaxis=dict(
            title=dict(text="Duration (minutes)", font=dict(color='#A0A0B0')),
            tickfont=dict(color='#A0A0B0'),
            gridcolor='rgba(78, 205, 196, 0.1)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color='#A0A0B0')
        ),
        hovermode='x unified'
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

with tab2:
    # Heart Points analysis
    st.markdown("<p style='color: #6B6B80; font-size: 0.85rem; margin: 0 0 15px 0;'>❤️ Monitor your cardiovascular health progress against WHO's recommended 21 heart points per day</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Heart Points over time
        heart_data = daily_agg[['Date', 'Heart Points']].copy()
        heart_data = heart_data.sort_values('Date')
        
        fig_heart = go.Figure()
        
        fig_heart.add_trace(go.Scatter(
            x=heart_data['Date'],
            y=heart_data['Heart Points'],
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.3)',
            line=dict(color=COLORS['coral'], width=2),
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>%{y:.0f} Heart Points<extra></extra>"
        ))
        
        # Add WHO recommended line (150 min/week moderate = ~21/day)
        fig_heart.add_hline(
            y=21, 
            line_dash="dash", 
            line_color=COLORS['teal'],
            annotation_text="WHO Daily Goal (21)",
            annotation_position="top right",
            annotation_font_color=COLORS['teal']
        )
        
        fig_heart.update_layout(
            title=dict(text="Daily Heart Points", font=dict(color='white', size=16)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=40),
            height=350,
            xaxis=dict(tickfont=dict(color='#A0A0B0'), gridcolor='rgba(78, 205, 196, 0.1)'),
            yaxis=dict(
                title=dict(text="Heart Points", font=dict(color='#A0A0B0')),
                tickfont=dict(color='#A0A0B0'),
                gridcolor='rgba(78, 205, 196, 0.1)'
            )
        )
        st.plotly_chart(fig_heart, use_container_width=True)
    
    with col2:
        # Heart Points distribution
        hp_stats = {
            'Below Goal (<21)': len(heart_data[heart_data['Heart Points'] < 21]),
            'Meeting Goal (21-42)': len(heart_data[(heart_data['Heart Points'] >= 21) & (heart_data['Heart Points'] < 42)]),
            'Exceeding Goal (42+)': len(heart_data[heart_data['Heart Points'] >= 42])
        }
        
        total_days_hp = sum(hp_stats.values())
        
        fig_hp_dist = go.Figure(data=[go.Pie(
            labels=list(hp_stats.keys()),
            values=list(hp_stats.values()),
            hole=0.6,
            marker=dict(
                colors=[COLORS['coral'], COLORS['gold'], COLORS['teal']],
                line=dict(color='#0F0F1A', width=3)
            ),
            textinfo='none',
            hovertemplate="<b>%{label}</b><br>%{value} days (%{percent})<extra></extra>"
        )])
        
        fig_hp_dist.update_layout(
            title=dict(text="Heart Points Achievement", font=dict(color='white', size=16)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=80),
            height=350,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.05,
                xanchor="center",
                x=0.5,
                font=dict(color='#A0A0B0', size=11)
            ),
            annotations=[dict(
                text=f"<b>{total_days_hp}</b><br>days",
                x=0.5, y=0.5,
                font=dict(size=18, color='white', family='Outfit'),
                showarrow=False
            )]
        )
        st.plotly_chart(fig_hp_dist, use_container_width=True)
        
        # Show breakdown below chart
        below_pct = hp_stats['Below Goal (<21)'] / total_days_hp * 100 if total_days_hp > 0 else 0
        meeting_pct = hp_stats['Meeting Goal (21-42)'] / total_days_hp * 100 if total_days_hp > 0 else 0
        exceeding_pct = hp_stats['Exceeding Goal (42+)'] / total_days_hp * 100 if total_days_hp > 0 else 0
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-around; text-align: center; margin-top: -10px;">
            <div>
                <p style="color: {COLORS['coral']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{below_pct:.0f}%</p>
                <p style="color: #6B6B80; font-size: 0.7rem; margin: 0;">Below Goal</p>
            </div>
            <div>
                <p style="color: {COLORS['gold']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{meeting_pct:.0f}%</p>
                <p style="color: #6B6B80; font-size: 0.7rem; margin: 0;">Meeting Goal</p>
            </div>
            <div>
                <p style="color: {COLORS['teal']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{exceeding_pct:.0f}%</p>
                <p style="color: #6B6B80; font-size: 0.7rem; margin: 0;">Exceeding</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    # Calorie Trends Analysis
    st.markdown("<p style='color: #6B6B80; font-size: 0.85rem; margin: 0 0 15px 0;'>📈 Analyze your daily calorie burn patterns and see how your energy expenditure changes over time</p>", unsafe_allow_html=True)
    calorie_data = daily_agg[['Date', 'Calories (kcal)']].copy()
    calorie_data = calorie_data.sort_values('Date')
    
    if len(calorie_data) > 1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily Calorie Change from Previous Day
            calorie_change = calorie_data.copy()
            calorie_change['Prev Day Calories'] = calorie_change['Calories (kcal)'].shift(1)
            calorie_change['Change'] = calorie_change['Calories (kcal)'] - calorie_change['Prev Day Calories']
            calorie_change = calorie_change.dropna()
            
            # Color based on increase/decrease
            colors_cal = [COLORS['teal'] if change >= 0 else COLORS['coral'] 
                          for change in calorie_change['Change']]
            
            fig_calorie_change = go.Figure()
            
            fig_calorie_change.add_trace(go.Bar(
                x=calorie_change['Date'],
                y=calorie_change['Change'],
                marker=dict(
                    color=colors_cal,
                    line=dict(width=0)
                ),
                hovertemplate="<b>%{x|%b %d}</b><br>Change: %{y:+,.0f} kcal<extra></extra>"
            ))
            
            # Add zero line
            fig_calorie_change.add_hline(
                y=0,
                line_dash="solid",
                line_color='#6B6B80',
                line_width=1
            )
            
            fig_calorie_change.update_layout(
                title=dict(text="Daily Calorie Change", font=dict(color='white', size=16)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=40),
                height=350,
                xaxis=dict(
                    tickfont=dict(color='#A0A0B0', size=9),
                    gridcolor='rgba(78, 205, 196, 0.1)'
                ),
                yaxis=dict(
                    title=dict(text="kcal vs Previous Day", font=dict(color='#A0A0B0')),
                    tickfont=dict(color='#A0A0B0'),
                    gridcolor='rgba(78, 205, 196, 0.1)',
                    zeroline=False
                ),
                showlegend=False
            )
            st.plotly_chart(fig_calorie_change, use_container_width=True)
        
        with col2:
            # Calorie trend with 7-day rolling average
            calorie_trend = calorie_data.copy()
            if len(calorie_trend) >= 7:
                calorie_trend['Rolling Avg'] = calorie_trend['Calories (kcal)'].rolling(7, min_periods=1).mean()
            
            fig_calorie_trend = go.Figure()
            
            # Daily calories as bars
            fig_calorie_trend.add_trace(go.Bar(
                x=calorie_trend['Date'],
                y=calorie_trend['Calories (kcal)'],
                marker=dict(
                    color=COLORS['purple'],
                    opacity=0.4
                ),
                name='Daily',
                hovertemplate="<b>%{x|%b %d}</b><br>%{y:,.0f} kcal<extra></extra>"
            ))
            
            # Rolling average as line
            if 'Rolling Avg' in calorie_trend.columns:
                fig_calorie_trend.add_trace(go.Scatter(
                    x=calorie_trend['Date'],
                    y=calorie_trend['Rolling Avg'],
                    mode='lines',
                    line=dict(color=COLORS['gold'], width=3),
                    name='7-Day Avg',
                    hovertemplate="%{y:,.0f} kcal<extra></extra>"
                ))
            
            fig_calorie_trend.update_layout(
                title=dict(text="Calorie Burn Trend", font=dict(color='white', size=16)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=40),
                height=350,
                xaxis=dict(tickfont=dict(color='#A0A0B0'), gridcolor='rgba(78, 205, 196, 0.1)'),
                yaxis=dict(
                    title=dict(text="Calories (kcal)", font=dict(color='#A0A0B0')),
                    tickfont=dict(color='#A0A0B0'),
                    gridcolor='rgba(78, 205, 196, 0.1)'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(color='#A0A0B0')
                ),
                barmode='overlay'
            )
            st.plotly_chart(fig_calorie_trend, use_container_width=True)
    else:
        st.info("Insufficient calorie data for the selected period")
# =============================================================================
# SECTION 3: CALENDAR HEATMAP
# =============================================================================

st.markdown("## Activity Calendar")

# Create calendar heatmap data
calendar_data = daily_agg[['Date', 'Step count', 'Total Exercise (min)', 'Calories (kcal)']].copy()
calendar_data['Week'] = calendar_data['Date'].dt.isocalendar().week
calendar_data['Year'] = calendar_data['Date'].dt.year
calendar_data['Day'] = calendar_data['Date'].dt.dayofweek
calendar_data['Month'] = calendar_data['Date'].dt.month

# Select metric for heatmap
heatmap_metric = st.selectbox(
    "Select Metric",
    ["Total Exercise (min)", "Step count", "Calories (kcal)"],
    index=0,
    label_visibility="collapsed"
)

# Get the latest year's data for a cleaner view
latest_year = calendar_data['Year'].max()
year_data = calendar_data[calendar_data['Year'] == latest_year].copy()

if len(year_data) > 0:
    # Create a complete date range for the year
    year_start = pd.Timestamp(f"{latest_year}-01-01")
    year_end = min(pd.Timestamp(f"{latest_year}-12-31"), df['Date'].max())
    all_dates = pd.date_range(start=year_start, end=year_end, freq='D')
    
    complete_calendar = pd.DataFrame({'Date': all_dates})
    complete_calendar['Week'] = complete_calendar['Date'].dt.isocalendar().week
    complete_calendar['Day'] = complete_calendar['Date'].dt.dayofweek
    complete_calendar['Month'] = complete_calendar['Date'].dt.month
    
    # Merge with actual data
    year_data['Date'] = pd.to_datetime(year_data['Date'])
    complete_calendar = complete_calendar.merge(
        year_data[['Date', heatmap_metric]], 
        on='Date', 
        how='left'
    )
    complete_calendar[heatmap_metric] = complete_calendar[heatmap_metric].fillna(0)
    
    # Create heatmap
    # Pivot for heatmap format
    heatmap_pivot = complete_calendar.pivot_table(
        index='Day', 
        columns='Week', 
        values=heatmap_metric, 
        aggfunc='sum'
    )
    
    # Day labels
    day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=day_labels,
        colorscale=[
            [0, '#1A1A2E'],
            [0.25, '#2D4A4A'],
            [0.5, '#3D7A7A'],
            [0.75, '#4ECDC4'],
            [1, '#6FEDD6']
        ],
        hovertemplate="Week %{x}<br>%{y}<br>Value: %{z:,.0f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text=heatmap_metric.split('(')[0].strip(), font=dict(color='#A0A0B0')),
            tickfont=dict(color='#A0A0B0'),
            bgcolor='rgba(0,0,0,0)'
        )
    ))
    
    fig_heatmap.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=20, t=30, b=20),
        height=250,
        xaxis=dict(
            title=dict(text=f"Week of {latest_year}", font=dict(color='#A0A0B0')),
            tickfont=dict(color='#A0A0B0', size=10),
            dtick=4
        ),
        yaxis=dict(
            tickfont=dict(color='#A0A0B0'),
            autorange='reversed'
        )
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
# =============================================================================
# SECTION 8: YEAR COMPARISON
# =============================================================================

# if len(df['Year'].unique()) > 1:
#     st.markdown("## 📅 Year-over-Year Comparison")
    
#     yearly_stats = df.groupby('Year').agg({
#         'Step count': 'sum',
#         'Calories (kcal)': 'sum',
#         'Distance (m)': 'sum',
#         'Total Exercise (min)': 'sum',
#         'Heart Points': 'sum'
#     }).reset_index()
    
#     # Normalize by number of days in each year (for fair comparison)
#     days_per_year = df.groupby('Year')['Date'].nunique().reset_index()
#     days_per_year.columns = ['Year', 'Days']
#     yearly_stats = yearly_stats.merge(days_per_year, on='Year')
    
#     yearly_stats['Avg Daily Steps'] = yearly_stats['Step count'] / yearly_stats['Days']
#     yearly_stats['Avg Daily Exercise (min)'] = yearly_stats['Total Exercise (min)'] / yearly_stats['Days']
#     yearly_stats['Avg Daily Calories'] = yearly_stats['Calories (kcal)'] / yearly_stats['Days']
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         fig_yearly_steps = go.Figure()
        
#         fig_yearly_steps.add_trace(go.Bar(
#             x=yearly_stats['Year'],
#             y=yearly_stats['Avg Daily Steps'],
#             marker=dict(
#                 color=yearly_stats['Avg Daily Steps'],
#                 colorscale=[[0, COLORS['purple']], [0.5, COLORS['teal']], [1, COLORS['coral']]],
#             ),
#             text=yearly_stats['Avg Daily Steps'].round(0),
#             textposition='outside',
#             textfont=dict(color='#A0A0B0'),
#             hovertemplate="<b>%{x}</b><br>%{y:,.0f} avg daily steps<extra></extra>"
#         ))
        
#         fig_yearly_steps.update_layout(
#             title=dict(text="Average Daily Steps by Year", font=dict(color='white', size=16)),
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)',
#             margin=dict(l=20, r=20, t=60, b=40),
#             height=350,
#             xaxis=dict(
#                 tickfont=dict(color='#A0A0B0'),
#                 dtick=1
#             ),
#             yaxis=dict(
#                 title=dict(text="Steps", font=dict(color='#A0A0B0')),
#                 tickfont=dict(color='#A0A0B0'),
#                 gridcolor='rgba(78, 205, 196, 0.1)'
#             ),
#             showlegend=False
#         )
#         st.plotly_chart(fig_yearly_steps, use_container_width=True)
    
#     with col2:
#         fig_yearly_exercise = go.Figure()
        
#         fig_yearly_exercise.add_trace(go.Bar(
#             x=yearly_stats['Year'],
#             y=yearly_stats['Avg Daily Exercise (min)'],
#             marker=dict(
#                 color=yearly_stats['Avg Daily Exercise (min)'],
#                 colorscale=[[0, COLORS['coral']], [0.5, COLORS['gold']], [1, COLORS['teal']]],
#             ),
#             text=yearly_stats['Avg Daily Exercise (min)'].round(0),
#             textposition='outside',
#             textfont=dict(color='#A0A0B0'),
#             hovertemplate="<b>%{x}</b><br>%{y:.0f} min avg daily exercise<extra></extra>"
#         ))
        
#         fig_yearly_exercise.update_layout(
#             title=dict(text="Average Daily Exercise by Year", font=dict(color='white', size=16)),
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)',
#             margin=dict(l=20, r=20, t=60, b=40),
#             height=350,
#             xaxis=dict(
#                 tickfont=dict(color='#A0A0B0'),
#                 dtick=1
#             ),
#             yaxis=dict(
#                 title=dict(text="Minutes", font=dict(color='#A0A0B0')),
#                 tickfont=dict(color='#A0A0B0'),
#                 gridcolor='rgba(78, 205, 196, 0.1)'
#             ),
#             showlegend=False
#         )
#         st.plotly_chart(fig_yearly_exercise, use_container_width=True)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")

# Link to About page
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.page_link("pages/About.py", label="About This Dashboard", icon="ℹ️", use_container_width=True)

st.markdown("""
<div style="text-align: center; padding: 1rem 0 2rem 0;">
    <p style="color: #6B6B80; font-size: 0.85rem;">
        ⚡ <strong style="color: #4ECDC4;">Verve</strong> • Your Fitness Journey Dashboard
    </p>
    <p style="color: #4A4A5A; font-size: 0.75rem;">
        Built with Streamlit & Plotly • Data from Google Fit
    </p>
</div>
""", unsafe_allow_html=True)
