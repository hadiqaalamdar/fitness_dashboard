import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Page configuration
st.set_page_config(page_title="Fitness Tracking Dashboard", layout="wide")

# Initialize geocoder
@st.cache_resource
def get_geocoder():
    return Nominatim(user_agent="fitness_tracker_dashboard")

# Configuration: Set to False to skip geocoding for faster loading
USE_GEOCODING = True  # Set to True if you want real city/country names

# Reverse geocode function with caching
@st.cache_data
def reverse_geocode(lat, lon):
    """Convert latitude/longitude to city, country"""
    if not USE_GEOCODING:
        # Fast fallback: just use coordinate-based location
        return f"Loc ({lat:.2f}, {lon:.2f})"
    
    try:
        geocoder = get_geocoder()
        location = geocoder.reverse(f"{lat}, {lon}", language='en', timeout=3)
        if location and location.raw.get('address'):
            address = location.raw['address']
            # Only get city and country for speed
            city = address.get('city') or address.get('town') or address.get('village') or address.get('municipality') or 'Unknown'
            country = address.get('country', 'Unknown')
            return f"{city}, {country}"
        return f"Loc ({lat:.2f}, {lon:.2f})"
    except (GeocoderTimedOut, GeocoderServiceError):
        return f"Loc ({lat:.2f}, {lon:.2f})"
    except Exception as e:
        return f"Loc ({lat:.2f}, {lon:.2f})"

# Batch reverse geocode function
@st.cache_data
def batch_reverse_geocode(coordinates_list):
    """Batch process unique coordinates"""
    results = {}
    for lat, lon in coordinates_list:
        key = (round(lat, 2), round(lon, 2))  # Round to ~1km accuracy to reduce duplicates significantly
        if key not in results:
            results[key] = reverse_geocode(key[0], key[1])
    return results

# Load data
@st.cache_data
def load_data():
    # Read the CSV file with comma delimiter
    df = pd.read_csv('fitness_data.csv', sep=',')
    
    # Convert date column to datetime and normalize to date only (remove time component)
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
    
    # Create activity type based on duration columns
    def get_activity_type(row):
        activities = []
        if pd.notna(row['Walking duration (ms)']) and row['Walking duration (ms)'] > 0:
            activities.append('Walking')
        if pd.notna(row['Cycling duration (ms)']) and row['Cycling duration (ms)'] > 0:
            activities.append('Cycling')
        if pd.notna(row['Paced walking duration (ms)']) and row['Paced walking duration (ms)'] > 0:
            activities.append('Paced Walking')
        if pd.notna(row['Running duration (ms)']) and row['Running duration (ms)'] > 0:
            activities.append('Running')
        return ', '.join(activities) if activities else 'Inactive'
    
    df['Activity Type'] = df.apply(get_activity_type, axis=1)
    
    # Get location from coordinates using reverse geocoding (optimized)
    # Round coordinates first to reduce unique locations significantly
    df['lat_rounded'] = df['Low latitude (deg)'].round(2)
    df['lon_rounded'] = df['Low longitude (deg)'].round(2)
    
    unique_coords = df[['lat_rounded', 'lon_rounded']].drop_duplicates().dropna().values.tolist()
    
    # Only show spinner if we have many unique locations and geocoding is enabled
    if len(unique_coords) > 3 and USE_GEOCODING:
        with st.spinner(f'Loading location data for {len(unique_coords)} unique locations...'):
            location_map = batch_reverse_geocode(unique_coords)
    else:
        location_map = batch_reverse_geocode(unique_coords)
    
    # Map locations to dataframe
    df['Location'] = df.apply(
        lambda x: location_map.get((round(x['Low latitude (deg)'], 2), round(x['Low longitude (deg)'], 2)), "Unknown Location") 
        if pd.notna(x['Low latitude (deg)']) and pd.notna(x['Low longitude (deg)'])
        else "Unknown Location",
        axis=1
    )
    
    # Drop temporary columns
    df = df.drop(columns=['lat_rounded', 'lon_rounded'])
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Calculate default date range based on available data
# Get the most recent week in the data
max_date = df['Date'].max()
week_start = max_date - timedelta(days=max_date.dayofweek)
week_end = min(week_start + timedelta(days=6), max_date)

# Ensure the default range is within bounds
default_start = max(week_start, df['Date'].min())
default_end = min(week_end, df['Date'].max())

# Date filter - default to the most recent week in data
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(default_start.date(), default_end.date()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max(),
    format="DD/MM/YYYY"
)

# Activity type filter
all_activities = set()
for activities in df['Activity Type'].unique():
    all_activities.update(activities.split(', '))

# Remove 'Inactive' from activity type options
all_activities.discard('Inactive')
all_activities = sorted(list(all_activities))

selected_activities = st.sidebar.multiselect(
    "Activity Type",
    options=all_activities,
    default=all_activities
)

# Location filter
selected_locations = st.sidebar.multiselect(
    "Location",
    options=sorted(df['Location'].unique()),
    default=df['Location'].unique()
)

# Filter data
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
filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]

# Dashboard title
st.title("Fitness Tracking Dashboard")

# Key Metrics (Selected Date Range)
st.header("Overview")

if len(filtered_df) > 0:
    # Aggregate data by day first
    daily_aggregates = filtered_df.groupby('Date').agg({
        'Step count': 'sum',
        'Calories (kcal)': 'sum',
        'Walking duration (ms)': 'sum',
        'Cycling duration (ms)': 'sum',
        'Paced walking duration (ms)': 'sum',
        'Running duration (ms)': 'sum'
    }).reset_index()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_steps = daily_aggregates['Step count'].mean()
        st.metric("Avg Daily Step Count", f"{avg_steps:.0f}" if pd.notna(avg_steps) else "N/A")
    
    with col2:
        # Calculate total exercise duration per day in minutes
        daily_aggregates['Total Exercise (min)'] = (
            daily_aggregates['Walking duration (ms)'].fillna(0) +
            daily_aggregates['Cycling duration (ms)'].fillna(0) +
            daily_aggregates['Paced walking duration (ms)'].fillna(0) +
            daily_aggregates['Running duration (ms)'].fillna(0)
        ) / 60000
        avg_exercise_min = daily_aggregates['Total Exercise (min)'].mean()
        st.metric("Avg Daily Exercise Duration", f"{avg_exercise_min:.1f} min" if pd.notna(avg_exercise_min) else "N/A")
    
    with col3:
        avg_calories = daily_aggregates['Calories (kcal)'].mean()
        st.metric("Avg Daily Calories Burned", f"{avg_calories:.1f} kcal" if pd.notna(avg_calories) else "N/A")
else:
    st.warning("No data available for selected filters")
    st.stop()

# Row 1: Pie Chart and Line Chart
st.header("Activity Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Activity/Inactivity Timeshare")
    # Calculate total active time across all days in the selected range
    total_active = (
        filtered_df['Walking duration (ms)'].fillna(0).sum() +
        filtered_df['Cycling duration (ms)'].fillna(0).sum() +
        filtered_df['Paced walking duration (ms)'].fillna(0).sum() +
        filtered_df['Running duration (ms)'].fillna(0).sum()
    )
    
    # Calculate total time in the selected date range
    num_days = (filtered_df['Date'].max() - filtered_df['Date'].min()).days + 1
    total_time_ms = num_days * 24 * 60 * 60 * 1000  # Total milliseconds in the date range
    total_inactive = total_time_ms - total_active
    
    # Ensure inactive time is not negative
    if total_inactive < 0:
        total_inactive = 0
    
    pie_data = pd.DataFrame({
        'Type': ['Active', 'Inactive'],
        'Duration (hours)': [total_active / 3600000, total_inactive / 3600000]
    })
    
    fig_pie = px.pie(pie_data, values='Duration (hours)', names='Type')
    
    # Explicitly set colors: Active = green, Inactive = red
    fig_pie.update_traces(
        marker=dict(colors=['#2ecc71', '#e74c3c'])
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Daily Heart Points by Exercise Type")
    # Prepare data for heart points - allocate based on exercise duration
    heart_points_data = []
    
    for _, row in filtered_df.iterrows():
        if pd.notna(row['Heart Points']) and row['Heart Points'] > 0:
            # Handle NaN values for scalar row values
            walking_dur = row['Walking duration (ms)'] if pd.notna(row['Walking duration (ms)']) else 0
            cycling_dur = row['Cycling duration (ms)'] if pd.notna(row['Cycling duration (ms)']) else 0
            running_dur = row['Running duration (ms)'] if pd.notna(row['Running duration (ms)']) else 0
            paced_walking_dur = row['Paced walking duration (ms)'] if pd.notna(row['Paced walking duration (ms)']) else 0
            
            total_duration = walking_dur + cycling_dur + running_dur + paced_walking_dur
            
            if total_duration > 0:
                # Allocate heart points proportionally to each exercise type
                if walking_dur > 0:
                    heart_points_data.append({
                        'Date': row['Date'], 
                        'Exercise': 'Walking', 
                        'Heart Points': row['Heart Points'] * (walking_dur / total_duration)
                    })
                if cycling_dur > 0:
                    heart_points_data.append({
                        'Date': row['Date'], 
                        'Exercise': 'Cycling', 
                        'Heart Points': row['Heart Points'] * (cycling_dur / total_duration)
                    })
                if running_dur > 0:
                    heart_points_data.append({
                        'Date': row['Date'], 
                        'Exercise': 'Running', 
                        'Heart Points': row['Heart Points'] * (running_dur / total_duration)
                    })
                if paced_walking_dur > 0:
                    heart_points_data.append({
                        'Date': row['Date'], 
                        'Exercise': 'Paced Walking', 
                        'Heart Points': row['Heart Points'] * (paced_walking_dur / total_duration)
                    })
    
    if heart_points_data:
        hp_df = pd.DataFrame(heart_points_data)
        # Ensure Date is normalized to date only (no time component)
        hp_df['Date'] = pd.to_datetime(hp_df['Date']).dt.date
        # Aggregate by Date and Exercise type to sum up heart points for each day
        hp_df = hp_df.groupby(['Date', 'Exercise'], as_index=False)['Heart Points'].sum()
        # Convert back to datetime for proper plotting
        hp_df['Date'] = pd.to_datetime(hp_df['Date'])
        # Sort by date to ensure proper line plotting
        hp_df = hp_df.sort_values('Date')
        
        # Calculate number of days in range for date display logic
        num_days = (hp_df['Date'].max() - hp_df['Date'].min()).days + 1
        
        # Create line chart with different colored lines for each exercise type
        fig_line = px.line(hp_df, x='Date', y='Heart Points', color='Exercise',
                          markers=True,
                          labels={'Heart Points': 'Total Heart Points', 'Date': 'Date'},
                          color_discrete_map={
                              'Walking': '#3498db',
                              'Cycling': '#e74c3c',
                              'Running': '#9b59b6',
                              'Paced Walking': '#f39c12'
                          })
        
        # Configure x-axis to show all dates for reasonable ranges
        if num_days <= 31:
            # Show all dates for ranges up to 31 days
            fig_line.update_xaxes(
                tickformat="%d/%m/%Y",
                dtick=86400000.0,  # 1 day in milliseconds
                tickangle=-45
            )
        else:
            # For longer ranges, show dates but allow plotly to choose interval
            fig_line.update_xaxes(tickformat="%d/%m/%Y", tickangle=-45)
            
        fig_line.update_layout(
            xaxis_title="Date", 
            yaxis_title="Total Heart Points",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No heart points data available for selected filters")

# Row 2: Waterfall Chart and Stacked Bar Chart
st.header("Calorie and Exercise Duration Breakdown")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Change in Calories Burned")
    # Prepare waterfall data - aggregate by day
    daily_calories = filtered_df.groupby('Date')['Calories (kcal)'].sum().reset_index()
    daily_calories = daily_calories.sort_values('Date')
    
    if len(daily_calories) > 0:
        # Calculate day-by-day changes
        changes = [daily_calories.iloc[0]['Calories (kcal)']]
        for i in range(1, len(daily_calories)):
            changes.append(daily_calories.iloc[i]['Calories (kcal)'] - daily_calories.iloc[i-1]['Calories (kcal)'])
        
        # Format dates as dd/mm/yyyy
        num_days = len(daily_calories)
        
        fig_waterfall = go.Figure(go.Waterfall(
            x=[d.strftime('%d/%m/%Y') for d in daily_calories['Date']],
            y=changes,
            text=[f"{c:.0f}" for c in changes],
            textposition="outside",
            cliponaxis=False,  # Prevent labels from being clipped
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#2ecc71"}},
            decreasing={"marker": {"color": "#e74c3c"}},
            totals={"marker": {"color": "#3498db"}}
        ))
        
        # Configure x-axis
        xaxis_config = dict(title="Date", automargin=True)
        if num_days <= 31:
            xaxis_config['tickangle'] = -45
        else:
            xaxis_config['tickangle'] = -45
            
        fig_waterfall.update_layout(
            showlegend=False, 
            xaxis=xaxis_config,
            yaxis=dict(
                title="Calories (kcal)",
                automargin=True
            ),
            margin=dict(l=50, r=50, t=80, b=80),  # Increased margins to prevent cut-off
            height=450  # Slightly increased height
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
    else:
        st.info("No calorie data available for selected date range")

with col2:
    st.subheader("Daily Exercise Duration by Type")
    # Prepare stacked bar data using filtered data
    exercise_duration = filtered_df.copy()
    exercise_duration['Walking (min)'] = exercise_duration['Walking duration (ms)'].fillna(0) / 60000
    exercise_duration['Cycling (min)'] = exercise_duration['Cycling duration (ms)'].fillna(0) / 60000
    exercise_duration['Paced Walking (min)'] = exercise_duration['Paced walking duration (ms)'].fillna(0) / 60000
    exercise_duration['Running (min)'] = exercise_duration['Running duration (ms)'].fillna(0) / 60000
    
    # Aggregate by date (sum all entries per day)
    exercise_agg = exercise_duration.groupby('Date').agg({
        'Walking (min)': 'sum',
        'Cycling (min)': 'sum',
        'Paced Walking (min)': 'sum',
        'Running (min)': 'sum'
    }).reset_index()
    
    # Sort by date to ensure proper ordering
    exercise_agg = exercise_agg.sort_values('Date')
    
    # Calculate number of days for date display logic
    num_days = len(exercise_agg)
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(name='Walking', x=exercise_agg['Date'], y=exercise_agg['Walking (min)'], marker_color='#3498db'))
    fig_bar.add_trace(go.Bar(name='Cycling', x=exercise_agg['Date'], y=exercise_agg['Cycling (min)'], marker_color='#e74c3c'))
    fig_bar.add_trace(go.Bar(name='Paced Walking', x=exercise_agg['Date'], y=exercise_agg['Paced Walking (min)'], marker_color='#f39c12'))
    fig_bar.add_trace(go.Bar(name='Running', x=exercise_agg['Date'], y=exercise_agg['Running (min)'], marker_color='#9b59b6'))
    
    # Configure x-axis to show all dates for reasonable ranges
    if num_days <= 31:
        fig_bar.update_xaxes(
            tickformat="%d/%m/%Y",
            dtick=86400000.0,  # 1 day in milliseconds
            tickangle=-45
        )
    else:
        fig_bar.update_xaxes(tickformat="%d/%m/%Y", tickangle=-45)
    
    fig_bar.update_layout(
        barmode='stack', 
        xaxis_title="Date", 
        yaxis_title="Duration (minutes)",
        margin=dict(l=20, r=20, t=40, b=60),
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Row 3: Bubble Chart - Exercise Duration by Location
st.header("Exercise Duration by Location")

# Aggregate data by location
location_data = filtered_df.groupby('Location').agg({
    'Walking duration (ms)': 'sum',
    'Cycling duration (ms)': 'sum',
    'Running duration (ms)': 'sum',
    'Paced walking duration (ms)': 'sum',
    'Calories (kcal)': 'sum'
}).reset_index()

# Calculate total exercise duration in minutes
location_data['Total Duration (min)'] = (
    location_data['Walking duration (ms)'].fillna(0) +
    location_data['Cycling duration (ms)'].fillna(0) +
    location_data['Running duration (ms)'].fillna(0) +
    location_data['Paced walking duration (ms)'].fillna(0)
) / 60000

# Sort by duration for better visualization
location_data = location_data.sort_values('Total Duration (min)', ascending=False)

# Create simple bubble chart without meaningful x/y axes
fig_bubble = go.Figure()

# Position bubbles in a simple horizontal layout
n_locations = len(location_data)
if n_locations > 0:
    # Space bubbles evenly across the chart
    x_positions = list(range(n_locations))
    
    # Define color palette for different locations
    color_palette = ['#3498db', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#e74c3c', '#2ecc71', '#34495e']
    
    for idx, (_, row) in enumerate(location_data.iterrows()):
        # Scale bubble size proportionally but keep it reasonable
        max_duration = location_data['Total Duration (min)'].max()
        if max_duration > 0:
            # Normalize size between 80 and 200
            bubble_size = 80 + (row['Total Duration (min)'] / max_duration) * 120
        else:
            bubble_size = 80
        
        # Assign different color to each bubble
        bubble_color = color_palette[idx % len(color_palette)]
            
        fig_bubble.add_trace(go.Scatter(
            x=[x_positions[idx]],
            y=[0],  # All bubbles on same y level
            mode='markers+text',
            marker=dict(
                size=bubble_size,
                color=bubble_color,
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            text=[f"{row['Location']}<br>{row['Total Duration (min)']:.0f} min"],
            textposition="middle center",
            textfont=dict(size=10, color='white', family='Arial Black'),
            hovertemplate=f"<b>{row['Location']}</b><br>" +
                         f"Duration: {row['Total Duration (min)']:.1f} min<br>" +
                         f"Calories: {row['Calories (kcal)']:.1f} kcal<br>" +
                         "<extra></extra>",
            showlegend=False
        ))

# Remove axes and make it clean
fig_bubble.update_layout(
    xaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False,
        range=[-0.5, max(n_locations - 0.5, 0.5)] if n_locations > 0 else [-0.5, 0.5]
    ),
    yaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False,
        range=[-0.8, 0.8]  # Reduced range to fit bubbles better
    ),
    height=300,  # Reduced height
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=20, b=20)  # Reduced margins
)

st.plotly_chart(fig_bubble, use_container_width=True)

# # Data table
# st.header("📋 Detailed Data")
# display_cols = ['Date', 'Activity Type', 'Location', 'Step count', 'Calories (kcal)', 
#                 'Heart Points', 'Distance (m)']
# # Format the data for display
# display_df = filtered_df[display_cols].sort_values('Date', ascending=False).copy()
# display_df['Date'] = display_df['Date'].dt.strftime('%d/%m/%Y')
# st.dataframe(display_df, use_container_width=True)