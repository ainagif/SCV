import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Streamlit App Configuration ---
st.set_page_config(layout="wide")
st.title("💊 Drug Use Demographics and Key Triggers Analysis")

# --- Data Loading ---
url = 'https://raw.githubusercontent.com/ainagif/SCV/refs/heads/main/df.csv'

# Use Streamlit's caching decorator for better performance
@st.cache_data
def load_data(data_url):
    """Loads the dataframe from the URL."""
    try:
        arts_df = pd.read_csv(data_url)
        # Rename df to arts_df to match the original code's data loading variable
        # and ensure compatibility with the plotting logic that uses 'df' in the original.
        return arts_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

arts_df = load_data(url)

# Use 'df' internally for visualization as in the original code, but only if the data loaded successfully.
if not arts_df.empty:
    df = arts_df

    # --- Display Data Preview ---
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    st.success("Analyzing Demographics and Key Triggers of Drug Use")

    # --- Visualization Section (Matplotlib/Seaborn to Plotly) ---

    ## 📊 Distribution of Age Midpoints (Histogram)
    st.subheader("Distribution of Age Midpoints")
    try:
        fig_hist = px.histogram(
            df, 
            x='age_midpoint', 
            nbins=10, 
            title='Distribution of Age Midpoints',
            color_discrete_sequence=px.colors.qualitative.T10,
            marginal='box' # Adds a box plot for better summary
        )
        fig_hist.update_layout(xaxis_title='Age Midpoint', yaxis_title='Frequency')
        st.plotly_chart(fig_hist, use_container_width=True)
    except KeyError:
        st.warning("Column 'age_midpoint' not found in the dataset for the histogram.")


    ## 🎂 Marital Status of Addicts (Pie Chart)
    st.subheader("Marital Status of Addicts")
    try:
        marital_counts = df['marital_status'].value_counts().reset_index()
        marital_counts.columns = ['Marital Status', 'Count']
        
        fig_pie = px.pie(
            marital_counts, 
            values='Count', 
            names='Marital Status', 
            title='Marital Status of Addicts',
            hole=.3 # Optional: makes it a donut chart
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    except KeyError:
        st.warning("Column 'marital_status' not found in the dataset for the pie chart.")


    ## ♨️ Education Level vs. Mental Health Status (Heatmap)
    st.subheader("Education Level vs. Mental Health Status (Heatmap)")
    try:
        # Create a crosstab for the two categorical variables
        crosstab_data = pd.crosstab(df['education_level'], df['mental_health_status'])

        # Create a Plotly Heatmap (go.Heatmap is better for crosstabs)
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=crosstab_data.values,
            x=crosstab_data.columns,
            y=crosstab_data.index,
            colorscale='Viridis', # Matches the original 'viridis' cmap
            hovertemplate="Mental Health Status: %{x}<br>Education Level: %{y}<br>Count: %{z}<extra></extra>"
        ))
        
        fig_heatmap.update_layout(
            title='Education Level vs. Mental Health Status',
            xaxis_title='Mental Health Status',
            yaxis_title='Education Level',
            xaxis={'side': 'bottom'}
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    except KeyError:
        st.warning("Columns 'education_level' or 'mental_health_status' not found in the dataset for the heatmap.")
        
else:
    st.info("Please check the data source URL or file content.")


# Assuming 'df' DataFrame is already loaded (as in previous steps)

st.success("Studying Social and Mental Health Risk Factors Among Addicts")

# --- Visualization Section (Matplotlib/Seaborn to Plotly) ---

## 👥 Friends Influence vs. Failure in Life (Bar Chart)
st.subheader("Friends Influence vs. Failure in Life")
try:
    fig_bar1 = px.bar(
        df.sort_values(by='friends_influence'), # Ensure consistent ordering
        x='friends_influence',
        color='failure_in_life_numeric',
        title='Friends Influence vs. Failure in Life',
        labels={'failure_in_life_numeric': 'Failure in Life (1=Yes, 0=No)'},
        barmode='group', # Grouped bar chart
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_bar1.update_layout(xaxis_title='Friends Influence', yaxis_title='Count')
    st.plotly_chart(fig_bar1, use_container_width=True)
except KeyError:
    st.warning("One or more required columns ('friends_influence', 'failure_in_life_numeric') not found for the first bar chart.")

# ---
st.markdown("---")

## 👨‍👩‍👧‍👦 Type of Addiction by Family History of Drug Use (Grouped Bar Plot)
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
    st.warning("One or more required columns ('addicted_with', 'family_history_of_drug_use') not found for the second bar chart.")

# ---
st.markdown("---")

## 🧠 Age of First Use Distribution by Mental/Emotional Problem and Smoking (Box Plot)
st.subheader("Age of First Use Distribution by Mental/Emotional Problem and Smoking")
try:
    fig_box = px.box(
        df,
        x='mental/emotional_problem',
        y='age_of_first_use_midpoint',
        color='smoking',
        title='Age of First Use Distribution by Mental/Emotional Problem and Smoking',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    # Rotate x-axis labels for readability, similar to plt.xticks(rotation=45)
    fig_box.update_xaxes(tickangle=45)
    fig_box.update_layout(
        xaxis_title='Mental/Emotional Problem',
        yaxis_title='Age of First Use (Midpoint)',
        legend_title='Smoking'
    )
    st.plotly_chart(fig_box, use_container_width=True)
except KeyError:
    st.warning("One or more required columns ('mental/emotional_problem', 'age_of_first_use_midpoint', 'smoking') not found for the box plot.")


# Assuming 'df' DataFrame is already loaded (as in previous steps)

st.success("Identifying Correlations between Risk and Life Outcome")

# --- Visualization Section (Matplotlib/Seaborn to Plotly) ---

## 📊 Average Age Midpoint by Mental Health Status and Failure in Life (Grouped Bar Chart)
st.subheader("Average Age Midpoint by Mental Health Status and Failure in Life")
try:
    # Use Plotly Express to create the grouped bar chart.
    # Plotly automatically calculates the mean/average for the y-variable ('age_midpoint') 
    # when using 'bar' and a categorical x-variable.
    fig_bar = px.bar(
        df,
        x='mental_health_status',
        y='age_midpoint',
        color='failure_in_life_numeric',
        title='Average Age Midpoint by Mental Health Status and Failure in Life',
        labels={'failure_in_life_numeric': 'Failure in Life (1=Yes, 0=No)'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_bar.update_layout(xaxis_title='Mental Health Status', yaxis_title='Average Age Midpoint')
    st.plotly_chart(fig_bar, use_container_width=True)
except KeyError:
    st.warning("One or more required columns ('mental_health_status', 'age_midpoint', 'failure_in_life_numeric') not found for the bar chart.")

# ---
st.markdown("---")

## ♨️ Marital Status vs. Mental/Emotional Problem (Heatmap)
st.subheader("Marital Status vs. Mental/Emotional Problem (Heatmap)")
try:
    # Create a crosstab for the two categorical variables
    crosstab_data_marital_mental = pd.crosstab(df['marital_status'], df['mental/emotional_problem'])

    # Create a Plotly Heatmap
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=crosstab_data_marital_mental.values,
        x=crosstab_data_marital_mental.columns,
        y=crosstab_data_marital_mental.index,
        colorscale='Viridis',
        hovertemplate="Mental/Emotional Problem: %{x}<br>Marital Status: %{y}<br>Count: %{z}<extra></extra>"
    ))
    
    fig_heatmap.update_layout(
        title='Marital Status vs. Mental/Emotional Problem',
        xaxis_title='Mental/Emotional Problem',
        yaxis_title='Marital Status',
        xaxis={'side': 'bottom'}
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
except KeyError:
    st.warning("Columns 'marital_status' or 'mental/emotional_problem' not found for the heatmap.")
    
# ---
st.markdown("---")

## 📦 Age of First Use Distribution by Religion and Type of Addiction (Box Plot)
st.subheader("Age of First Use Distribution by Religion and Type of Addiction")
try:
    fig_box = px.box(
        df,
        x='religion',
        y='age_of_first_use_midpoint',
        color='addicted_with',
        title='Age of First Use Distribution by Religion and Type of Addiction',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    # Rotate x-axis labels for readability
    fig_box.update_xaxes(tickangle=45)
    fig_box.update_layout(
        xaxis_title='Religion',
        yaxis_title='Age of First Use (Midpoint)',
        legend_title='Type of Addiction'
    )
    st.plotly_chart(fig_box, use_container_width=True)
except KeyError:
    st.warning("One or more required columns ('religion', 'age_of_first_use_midpoint', 'addicted_with') not found for the box plot.")

