import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Streamlit App Configuration & Data Loading ---
st.set_page_config(layout="wide")
st.title("💊 Drug Addiction Risk Factor Analysis Dashboard")

url = 'https://raw.githubusercontent.com/ainagif/SCV/refs/heads/main/df.csv'

# Use Streamlit's caching decorator for better performance
@st.cache_data
def load_data(data_url):
    """Loads the dataframe from the URL."""
    try:
        arts_df = pd.read_csv(data_url)
        return arts_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(url)

if df.empty:
    st.info("The dashboard cannot display visualizations because the data failed to load.")
    st.stop()

# --- 2. Calculate Actual Metrics for Summary Box ---
# These calculations use the actual loaded 'df' to populate the metric boxes.
try:
    median_age = df['age_midpoint'].median().round(0).astype(int)
    most_common_marital = df['marital_status'].value_counts().idxmax()
    
    # Calculate % with Poor/Fair Mental Health (Assuming 'Poor' and 'Fair' are labels)
    poor_mental_health_count = df['mental_health_status'].isin(['Poor', 'Fair']).sum()
    mental_health_percentage = (poor_mental_health_count / len(df) * 100).round(1)
    
    # Identify the key education level (e.g., the one with the highest count)
    key_correlation = df['education_level'].value_counts().idxmax()
    
except KeyError as e:
    st.warning(f"Could not calculate metric: Missing column {e}. Using placeholders.")
    median_age = 29
    most_common_marital = "Single"
    mental_health_percentage = 65.0
    key_correlation = "Missing Data"

st.header("""Analyzing Demographics and Key Triggers of Drug Use""")


# --- 3. Key Findings Summary Box ---
st.subheader("Key Findings Analyzing Demographics and Key Triggers of Drug Use")

col1, col2, col3, col4 = st.columns(4)
    
col1.metric(
    label="Median Age of Addict", 
    value=f"{median_age} years", 
    help="Derived from the 'age_midpoint' distribution."
)
col2.metric(
    label="Most Common Marital Status", 
    value=f"{most_common_marital}", 
    help="Most frequent marital status among respondents."
)
col3.metric(
    label="% with Poor/Fair Mental Health", 
    value=f"{mental_health_percentage}%", 
    help="Prevalence of respondents reporting 'Poor' or 'Fair' mental health status."
)
col4.metric(
    label="Most Common Education Level", 
    value=f"{key_correlation}", 
    help="Most frequent education level reported in the dataset."
)

st.markdown("---")

st.success("""Looking at the summary box displayed, it is based on visualization and summary from streamlit. It has stated several different profiles for the drug addict population studied, among which the analysis shows addiction among those affecting young adults with a Median Age of Addict after reaching the age of 22 years. Looking at the majority of the values ​​obtained, 67.9% are from the unmarried group. Therefore for the Most Common Marital Status. Looking at the risk factors, the value of 16.9% is achieved in the Poor/Moderate Mental Health category. And looking at the education aspect, the Most Common Education Level was Bachelor/Below Degree. In addition, according to the heat map shown, the largest group experiencing mental 'Poor' is 79 individuals. It thus marks a high-risk demographic that requires targeted intervention.
. This metric collectively identifies young unmarried individuals with lower educational attainment and existing mental health problems as a priority focus group""")

# --- 4. Section 1: Demographics and Triggers ---
st.success("Analyzing Demographics and Key Triggers of Drug Use")

# --- Distribution of Age Midpoints (Histogram) ---
st.subheader("Distribution of Age Midpoints")
try:
    fig_hist = px.histogram(
        df, 
        x='age_midpoint', 
        nbins=10, 
        title='Distribution of Age Midpoints',
        color_discrete_sequence=px.colors.qualitative.T10,
        marginal='box'
    )
    fig_hist.update_layout(xaxis_title='Age Midpoint', yaxis_title='Frequency')
    st.plotly_chart(fig_hist, use_container_width=True)
except KeyError:
    st.warning("Column 'age_midpoint' not found.")

# --- Marital Status of Addicts (Pie Chart) ---
st.subheader("Marital Status of Addicts")
try:
    marital_counts = df['marital_status'].value_counts().reset_index()
    marital_counts.columns = ['Marital Status', 'Count']
    
    fig_pie = px.pie(
        marital_counts, 
        values='Count', 
        names='Marital Status', 
        title='Marital Status of Addicts',
        hole=.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)
except KeyError:
    st.warning("Column 'marital_status' not found.")

# --- Education Level vs. Mental Health Status (Heatmap) ---
st.subheader("Education Level vs. Mental Health Status (Heatmap)")
try:
    crosstab_data = pd.crosstab(df['education_level'], df['mental_health_status'])

    fig_heatmap1 = go.Figure(data=go.Heatmap(
        z=crosstab_data.values,
        x=crosstab_data.columns,
        y=crosstab_data.index,
        colorscale='Viridis'
    ))
    
    fig_heatmap1.update_layout(
        title='Education Level vs. Mental Health Status',
        xaxis_title='Mental Health Status',
        yaxis_title='Education Level'
    )
    st.plotly_chart(fig_heatmap1, use_container_width=True)
except KeyError:
    st.warning("Columns 'education_level' or 'mental_health_status' not found.")

st.markdown("---")

# ... (Code above this line, including data loading into 'df', is omitted for brevity)
