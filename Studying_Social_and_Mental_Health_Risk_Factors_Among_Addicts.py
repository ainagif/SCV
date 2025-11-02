import streamlit as st
import pandas as pd
import plotly.express as px

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
    
# --- Visualization Code (Corrected) ---

st.success("""Based on the display shown, it shows a summary of the demographic and mental health risk profile of the addict population studied. The data has shown that addiction focuses on 'young adults' with the 'Most Common Age Range' being at the age of '20-25 years' which initially shows that early onset is common. Looking at the social angle, the value achieved, which is 67.9%, is from 'Not Married'. It clearly shows that addiction is very high among those who do not have a partner or are married. In addition, the 'High Risk Group' metric has shown several dangerous factors, namely individuals with an educational level of 'Bachelor's/Undergraduate' have contributed the highest number in the 'Poor Mental Health' category, which is 79 individuals. It is clear that the data shows that there is a great risk among individuals with a low university education level and at the same time facing mental stress problems. Next, the majority have reported 'Never' having a 'Family History of Drug Use' thus showing that risk factors are often personal and not due to heredity""")


st.success("Studying Social and Mental Health Risk Factors Among Addicts")

# The problematic code needs correction. It should use 'df' and be part of a Plotly call.

st.subheader("Friends Influence vs. Failure in Life")
try:
    # CORRECTION: Using 'df.sort_values' within the px.bar call
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
    st.warning("One or more required columns not found for the first bar chart.")

# ... (Include all other charts for this page here) ...

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

