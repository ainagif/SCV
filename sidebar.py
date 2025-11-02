import streamlit as st

st.set_page_config(
    page_title="Student Survey"
)

# --- Define Existing Pages (Unchanged) ---
visualise = st.Page('studentSurvey.py', title='Pencapaian Akademik Pelajar', icon=":material/school:")
home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

# --- Define New Pages ---
# 1. Page for Studying Social and Mental Health Risk Factors
social_factors = st.Page(
    '.py', 
    title='Risk Factors (Social/Mental)', 
    icon=":material/diversity_3:"
)

# 2. Page for Identifying Correlations between Risk and Life Outcome
correlations = st.Page(
    'risk_correlation.py', 
    title='Risk and Life Outcome', 
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
