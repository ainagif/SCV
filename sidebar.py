import streamlit as st

st.set_page_config(
    page_title="Student Survey"
)

# --- Define Existing Pages (Unchanged) ---
visualise = st.Page('main.py', title='main', icon=":material/school:")
home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

# --- Define New Pages ---
# 1. Page for Studying Social and Mental Health Risk Factors
social_factors = st.Page(
    'Studying Social and Mental Health Risk Factors Among Addicts.py', 
    title='Studying Social and Mental Health Risk Factors Among Addicts', 
    icon=":material/diversity_3:"
)

# 2. Page for Identifying Correlations between Risk and Life Outcome
correlations = st.Page(
    'Identifying Correlations between Risk and Life Outcome.py', 
    title='Identifying Correlations between Risk and Life Outcome', 
    icon=":material/timeline:"
)


# --- Update Navigation ---
pg = st.navigation(
    {
        "Menu": [home, visualise],
        "Analysis": [social_factors, correlations] # Added new section for the analysis pages
    }
)

pg.run()
