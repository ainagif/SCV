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

