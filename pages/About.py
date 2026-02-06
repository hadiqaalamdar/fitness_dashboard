import streamlit as st

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="About • Verve Dashboard",
    # page_icon="📖",
    layout="wide"
)

# Custom CSS to match main dashboard
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0F0F1A 0%, #1A1A2E 50%, #0F0F1A 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #FFFFFF !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #6C63FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #4ECDC4 !important;
        margin-top: 2rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(78, 205, 196, 0.3);
    }
    
    h3 {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #A0A0B0 !important;
    }
    
    p, li, td, th {
        font-family: 'Outfit', sans-serif !important;
        color: #A0A0B0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HEADER
# =============================================================================

st.page_link("dashboard.py", label="← Back to Dashboard", icon="🏠")

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>About This Dashboard</h1>
    <p style="color: #6B6B80; font-size: 1.1rem;">
        Design choices, data sources, and visual encoding rationale
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# DATA SECTION
# =============================================================================

st.markdown("## 📊 Data")

st.markdown("""
The dashboard is based on **personal Google Fit activity data**, recorded as time-series observations.

**Activities tracked**
- Walking
- Running
- Cycling
- Paced walking

**Data characteristics**
- Temporal: recorded at regular 15-minute intervals
- Quantitative: steps, calories burned, distance, heart points, exercise minutes
- Categorical: activity type
- Spatial: latitude and longitude coordinates

**Data preparation**
- Invalid entries were removed to ensure accuracy
- Location data was anonymised by removing exact coordinates and personal identifiers
- Large gaps existed in the original Google Fit export; missing values were **synthetically generated**
  while preserving the **overall trends and patterns** of the original data

This preparation ensures continuity for analysis while maintaining the integrity and intent of the original dataset.
""")

st.markdown("---")

# =============================================================================
# STRUCTURE SECTION
# =============================================================================

st.markdown("## 🏗️ Structure")

st.markdown("""
### Page Structure
**Single Page layout with Parallel facets** — All data views on one scrollable page; sections contain parallel facets. This was chosen because it allows users to explore all metrics in a single session without navigating between pages. 
It also allows for easy comparison between metrics as you can see multiple facets at once. 
### Sections
| Section | Purpose |
|---------|---------|
| 🏆 Hero Stats | Avg + total metrics, step streak gamification |
| 📊 Activity Overview | Activity distribution donut, daily goal bar chart |
| 🔍 Patterns | Week comparison, radial weekly pattern, hourly distribution |
| 🏆 Personal Records | Best steps, distance, calories with dates in a selected time period |
| 🗺️ Location | Geographic activity hotspots on map |
| 📈 Detailed Breakdown | Tabs: Exercise types, Heart health, Calorie trends |
| 🗓️ Calendar | Heatmap for long-term consistency |
""")

st.markdown("---")

# =============================================================================
# VISUAL REPRESENTATIONS SECTION
# =============================================================================

st.markdown("## 📈 Visual Representations")

st.markdown("""
Visual representations were selected to match both the **data type** and the **analytical task**.

| Chart Type | Used In | Why |
|------------|---------|-----|
| **Donut** | Activity distribution, Heart points achievement | Part-to-whole relationships; shows proportions at a glance |
| **Bar** | Daily steps vs goal, Week comparison | Clear comparison against fixed thresholds and between categories |
| **Radial/Polar** | Weekly activity pattern | Highlights cyclical nature of weekly routines |
| **Stacked Area** | Exercise by type over time | Shows trends and composition changes simultaneously |
| **Area** | Heart points over time | Emphasizes trend toward goal threshold |
| **Waterfall** | Daily calorie change | Reveals sequential day-to-day momentum and drops |
| **Heatmap** | Activity calendar | Dense long-term view; reveals consistency patterns |
| **Bubble Map** | Location analysis | Geographic data naturally aligns with spatial layout |

Each chart answers a specific question while minimising cognitive load.
""")

st.markdown("---")

# =============================================================================
# PAGE LAYOUT SECTION
# =============================================================================

st.markdown("## 📐 Page Layout")

st.markdown("""
The layout follows a stratified vertical analytical flow optimised for wide screens. It shows general high-level information like key metric along the top, while showing more detailed information further down.

- High-level summaries appear first to support rapid orientation
- Related metrics are grouped horizontally for comparison
- Cards visually separate analytical tasks
- A sidebar provides global controls without interrupting exploration
""")

st.markdown("---")

# =============================================================================
# SCREENSPACE USE SECTION
# =============================================================================

st.markdown("## 📏 Screenspace Use")

st.markdown("""
Screen space is used to prioritise data visibility and readability. The key metrics are positioned above the fold to support rapid orientation, the rest is displayed further down in the overflow so the user can scroll to see it. 

- Key metrics are positioned above the fold
- Charts use consistent heights to maintain visual rhythm
- Tabs reduce vertical scrolling
- Dense views maximise the data-ink ratio
- White space separates sections and reduces clutter
""")

st.markdown("---")

# =============================================================================
# INTERACTIONS SECTION
# =============================================================================

st.markdown("## 🖱️ Interactions")

st.markdown("""
Interactions support focused exploration without breaking context.

- Date, activity, and location filters allow targeted analysis
- Hover tooltips provide precise values on demand
- Tabs organise detailed views
- Map zoom and pan support spatial exploration

Interactions are additive and preserve a stable mental model of the data.
""")

st.markdown("---")

# =============================================================================
# METADATA SECTION
# =============================================================================

st.markdown("## 🏷️ Meta Data")

st.markdown("""
Metadata provides context and clarity throughout the dashboard.

- Units are explicitly displayed (steps, km, kcal, minutes)
- Dates follow a consistent and readable format
- Goals such as 10,000 steps and 21 heart points are clearly referenced
- Aggregation logic (average vs total) is clearly communicated
- Personal records include dates to contextualise peak performance
""")

st.markdown("---")

# =============================================================================
# COLOR USE SECTION
# =============================================================================

st.markdown("## 🎨 Color Use")

st.markdown("""
Colour is used semantically to reinforce meaning.

- Teal indicates goals met and positive outcomes
- Coral highlights missed goals or underperformance
- Purple supports comparison views
- Gold highlights peaks and standout values
- Blue provides neutral or contextual information

A dark background reduces eye strain and increases contrast, keeping the data visually dominant.
""")

st.markdown("---")