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

# --- Key Findings Summary Box (Derived from Visual Analysis) ---
st.subheader("Key Findings Studying Social and Mental Health Risk Factors Among Addicts")

# Metrics derived directly from the uploaded charts:
most_frequent_age_range = "20-25 years"
unmarried_percentage = 67.9 # From Marital Status pie chart
no_family_history_count = "Highest" # From Type of Addiction bar chart (Green bar is tallest)
high_risk_mental_health_group = "Undergrad/Poor MH"

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Most Frequent Age Range", 
    value=f"{most_frequent_age_range}", 
    help="Peak frequency of addiction initiation/diagnosis falls between 20-25 years."
)
col2.metric(
    label="Unmarried Percentage", 
    value=f"{unmarried_percentage}%", 
    help="Percentage of addicts identified as Unmarried (67.9% from Pie Chart)."
)
col3.metric(
    label="Family History of Drug Use", 
    value="Never (Highest Count)", 
    help="Majority of Single Drug addicts reported never having a family history of drug use."
)
col4.metric(
    label="High Risk Group (Education/MH)", 
    value=f"{high_risk_mental_health_group}", 
    help="The Undergraduate/Under Degree group has the highest overall count, with 79 reporting Poor Mental Health."
)

st.markdown("---")

st.success("""Based on the display shown, it shows a summary of the demographic and mental health risk profile of the addict population studied. The data has shown that addiction focuses on 'young adults' with the 'Most Common Age Range' being at the age of '20-25 years' which initially shows that early onset is common. Looking at the social angle, the value achieved, which is 67.9%, is from 'Not Married'. It clearly shows that addiction is very high among those who do not have a partner or are married. In addition, the 'High Risk Group' metric has shown several dangerous factors, namely individuals with an educational level of 'Bachelor's/Undergraduate' have contributed the highest number in the 'Poor Mental Health' category, which is 79 individuals. It is clear that the data shows that there is a great risk among individuals with a low university education level and at the same time facing mental stress problems. Next, the majority have reported 'Never' having a 'Family History of Drug Use' thus showing that risk factors are often personal and not due to heredity""")

# ... (Continue with the visualization code blocks below this line) ...

# Metrics derived directly from the uploaded charts:
most_frequent_age_range = "20-25 years"
unmarried_percentage = 67.9 # From Marital Status pie chart
no_family_history_count = "Highest" # From Type of Addiction bar chart (Green bar is tallest)
high_risk_mental_health_group = "Undergrad/Poor MH"

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Most Frequent Age Range", 
    value=f"{most_frequent_age_range}", 
    help="Peak frequency of addiction initiation/diagnosis falls between 20-25 years."
)
col2.metric(
    label="Unmarried Percentage", 
    value=f"{unmarried_percentage}%", 
    help="Percentage of addicts identified as Unmarried (67.9% from Pie Chart)."
)
col3.metric(
    label="Family History of Drug Use", 
    value="Never (Highest Count)", 
    help="Majority of Single Drug addicts reported never having a family history of drug use."
)
col4.metric(
    label="High Risk Group (Education/MH)", 
    value=f"{high_risk_mental_health_group}", 
    help="The Undergraduate/Under Degree group has the highest overall count, with 79 reporting Poor Mental Health."
)

st.markdown("---")

# ... (Continue with the visualization code blocks below this line) ...

# --- 5. Section 2: Social and Mental Health Risk Factors ---
st.success("Studying Social and Mental Health Risk Factors Among Addicts")

# --- Friends Influence vs. Failure in Life (Bar Chart) ---
st.subheader("Friends Influence vs. Failure in Life")
try:
    fig_bar1 = px.bar(
        df.sort_values(by='friends_influence'),
        x='friends_influence',
        color='failure_in_life_numeric',
        title='Friends Influence vs. Failure in Life',
        labels={'failure_in_life_numeric': 'Failure in Life (1=Yes, 0=No)'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_bar1.update_layout(xaxis_title='Friends Influence', yaxis_title='Count')
    st.plotly_chart(fig_bar1, use_container_width=True)
except KeyError:
    st.warning("One or more columns ('friends_influence', 'failure_in_life_numeric') not found.")

# --- Type of Addiction by Family History of Drug Use (Grouped Bar Plot) ---
st.subheader("Type of Addiction by Family History of Drug Use")
try:
    fig_bar2 = px.bar(
        df.sort_values(by='addicted_with'),
        x='addicted_with',
        color='family_history_of_drug_use',
        title='Type of Addiction by Family History of Drug Use',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_bar2.update_layout(xaxis_title='Type of Addiction', yaxis_title='Count')
    st.plotly_chart(fig_bar2, use_container_width=True)
except KeyError:
    st.warning("One or more columns ('addicted_with', 'family_history_of_drug_use') not found.")

# --- Age of First Use Distribution by Mental/Emotional Problem and Smoking (Box Plot) ---
st.subheader("Age of First Use Distribution by Mental/Emotional Problem and Smoking")
try:
    fig_box1 = px.box(
        df,
        x='mental/emotional_problem',
        y='age_of_first_use_midpoint',
        color='smoking',
        title='Age of First Use Distribution by Mental/Emotional Problem and Smoking',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig_box1.update_xaxes(tickangle=45)
    fig_box1.update_layout(xaxis_title='Mental/Emotional Problem', yaxis_title='Age of First Use (Midpoint)')
    st.plotly_chart(fig_box1, use_container_width=True)
except KeyError:
    st.warning("One or more columns ('mental/emotional_problem', 'age_of_first_use_midpoint', 'smoking') not found.")

st.markdown("---")






