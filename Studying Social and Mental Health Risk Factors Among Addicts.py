import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


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

# --- 5. Section 2: Social and Mental Health Risk Factors ---
st.success("Studying Social and Mental Health Risk Factors Among Addicts")

# --- Friends Influence vs. Failure in Life (Bar Chart) ---
st.subheader("Friends Influence vs. Failure in Life")
try:
    fig_bar1 = px.bar(
        art_df.sort_values(by='friends_influence'),
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

