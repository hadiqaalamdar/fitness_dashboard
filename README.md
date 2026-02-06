# ⚡ Verve — Fitness Dashboard

A beautiful, interactive fitness dashboard built with Streamlit that transforms Google Fit data into actionable insights.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Overview

Verve visualizes personal fitness data collected from Google Fit, helping users understand their activity patterns, track goal achievement, and celebrate personal records. The dashboard features a modern dark theme with vibrant gradients and smooth animations.

### Key Features

- **📊 Hero Stats** — Average and total metrics with step streak gamification
- **🏃 Activity Distribution** — Donut charts showing activity type breakdown
- **📈 Pattern Analysis** — Weekly/hourly activity patterns with radial charts
- **🏆 Personal Records** — Best steps, distance, and calories with dates
- **🗺️ Location Insights** — Geographic activity hotspots on an interactive map
- **📅 Calendar Heatmap** — GitHub-style visualization for long-term consistency
- **💓 Health Metrics** — Heart points and calorie trend analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fitness_dashboard.git
   cd fitness_dashboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

5. **Open in browser**
   
   The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
fitness_dashboard/
├── dashboard.py          # Main dashboard application
├── pages/
│   └── About.py          # About page with design rationale
├── fitness_data.csv      # Fitness data (Google Fit export)
├── requirements.txt      # Python dependencies
└── README.md
```

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web app framework |
| **Pandas** | Data manipulation |
| **Plotly** | Interactive visualizations |
| **NumPy** | Numerical operations |
| **Geopy** | Reverse geocoding for location names |

---

<p align="center">
  Built with ❤️ using Streamlit
</p>
