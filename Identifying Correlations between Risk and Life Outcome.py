import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Re-Load Data within this Page File ---
url = 'https://raw.githubusercontent.com/ainagif/SCV/refs/heads/main/df.csv'

@st.cache_data
def load_data(data_url):
    """Loads the dataframe from the URL."""
    try:
        arts_df = pd.read_csv(data_url)
        return arts_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(url) # The DataFrame must be named 'df' (or the variable you use)

if df.empty:
    st.info("Cannot display visualization: Data failed to load.")
    st.stop()



# --- Key Findings Summary Box (Derived from Visual Analysis) ---
st.subheader("Key Findings Correlations between Risk and Life Outcome")

# Metrics derived directly from the uploaded charts:
most_frequent_age_range = "20 - 25 Years"
unmarried_percentage = "67.9%"
top_mental_risk = "Tension/Anxiety"
education_risk = "Undergrad/Poor MH"

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Peak Age Group", 
    value=f"{most_frequent_age_range}", 
    help="Highest frequency of addiction at age midpoints between 20 and 25."
)
col2.metric(
    label="Prevalence: Unmarried", 
    value=f"{unmarried_percentage}", 
    help="Percentage of addicts categorized as Unmarried (67.9% from Pie Chart)."
)
col3.metric(
    label="Highest Mental Health Risk", 
    value=f"{top_mental_risk}", 
    help="The highest count of a single problem: Unmarried addicts reporting Tension/Anxiety (242)."
)
col4.metric(
    label="Highest Poor MH Group", 
    value=f"{education_risk}", 
    help="The largest number reporting Poor Mental Health is the Undergraduate/Under Degree group (79)."
)

st.markdown("---")

st.success ("""Based on the summary above, the 'Summary of Key Findings' shows a combination of critical insights into the demographic and psychological profiles of the addict population. Looking at the data, it shows that addiction is highest in 'young adults' with the 'Peak Age Group' being '20-25 Years'. It shows that interventions should target this age range aggressively. Looking at the social aspect, the majority of addicts 'Not Married' have reached a value of 67.9% and in conclusion, it shows that marital status is a protective factor. Next, looking at the psychological aspect, the 'Highest Mental Health Risk' that has been identified is "Tension/Anxiety' which has displayed the highest frequency results in the relevant heat map for example Not Married vs. Mental/Emotional Problems. In addition, the 'Highest MH Termseckin Group' which has been identified as the 'Pre-degree/Undergraduate' level, this education group has achieved the highest value in the heat map and as many as 79 individuals 'Weak Mental Health' has outlined a very significant mental health crisis among those with lower levels of higher education.""")


# ... (Continue with the visualization code blocks below this line) ...

# --- 6. Section 3: Correlations between Risk and Life Outcome ---
st.success("Identifying Correlations between Risk and Life Outcome")

# --- Average Age Midpoint by Mental Health Status and Failure in Life (Grouped Bar Chart) ---
st.subheader("Average Age Midpoint by Mental Health Status and Failure in Life")
try:
    fig_bar3 = px.bar(
        df,
        x='mental_health_status',
        y='age_midpoint',
        color='failure_in_life_numeric',
        title='Average Age Midpoint by Mental Health Status and Failure in Life',
        labels={'failure_in_life_numeric': 'Failure in Life (1=Yes, 0=No)'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_bar3.update_layout(xaxis_title='Mental Health Status', yaxis_title='Average Age Midpoint')
    st.plotly_chart(fig_bar3, use_container_width=True)
except KeyError:
    st.warning("One or more columns ('mental_health_status', 'age_midpoint', 'failure_in_life_numeric') not found.")

# --- Marital Status vs. Mental/Emotional Problem (Heatmap) ---
st.subheader("Marital Status vs. Mental/Emotional Problem (Heatmap)")
try:
    crosstab_data_marital_mental = pd.crosstab(df['marital_status'], df['mental/emotional_problem'])

    fig_heatmap2 = go.Figure(data=go.Heatmap(
        z=crosstab_data_marital_mental.values,
        x=crosstab_data_marital_mental.columns,
        y=crosstab_data_marital_mental.index,
        colorscale='Viridis'
    ))
    
    fig_heatmap2.update_layout(
        title='Marital Status vs. Mental/Emotional Problem',
        xaxis_title='Mental/Emotional Problem',
        yaxis_title='Marital Status'
    )
    st.plotly_chart(fig_heatmap2, use_container_width=True)
except KeyError:
    st.warning("Columns 'marital_status' or 'mental/emotional_problem' not found.")
    
# --- Age of First Use Distribution by Religion and Type of Addiction (Box Plot) ---
st.subheader("Age of First Use Distribution by Religion and Type of Addiction")
try:
    fig_box2 = px.box(
        df,
        x='religion',
        y='age_of_first_use_midpoint',
        color='addicted_with',
        title='Age of First Use Distribution by Religion and Type of Addiction',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig_box2.update_xaxes(tickangle=45)
    fig_box2.update_layout(xaxis_title='Religion', yaxis_title='Age of First Use (Midpoint)')
    st.plotly_chart(fig_box2, use_container_width=True)
except KeyError:
    st.warning("One or more columns ('religion', 'age_of_first_use_midpoint', 'addicted_with') not found.")
