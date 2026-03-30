#!/usr/bin/env python
# coding: utf-8

# In[10]:


#%%writefile app_script.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configuration
st.set_page_config(page_title="Davis & Shirtliff Inventory Portal", layout="wide")

st.title("📦 Davis & Shirtliff: Inventory Intelligence")
st.markdown("### Decision Support System for Supply & Logistics")

# 2. Path Logic that works for both local and deployed environments
def load_data():
    # Try different relative paths to find the file
    paths_to_try = [
        'data/processed/inventory_intelligence.csv',
        '../data/processed/inventory_intelligence.csv',
        'inventory_intelligence.csv' # If file is in the same folder
    ]

    for path in paths_to_try:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None

df = load_data()

if df is not None:
    # --- Sidebar Filters ---
    st.sidebar.header("Logistics Filters")
    cat_filter = st.sidebar.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
    source_filter = st.sidebar.multiselect("Origin", df['Source'].unique(), default=df['Source'].unique())

    filtered_df = df[(df['Category'].isin(cat_filter)) & (df['Source'].isin(source_filter))]

    # --- KPI Metrics ---
    col1, col2, col3 = st.columns(3)
    reorder_needed = len(filtered_df[filtered_df['Stock_Status'] == 'REORDER NOW'])

    col1.metric("Items to Reorder", reorder_needed, delta="-Action Required" if reorder_needed > 0 else "Clear")
    col2.metric("Total Portfolio Value", f"${filtered_df['Annual_Consumption_USD'].sum():,.0f}")
    col3.metric("Avg Lead Time", f"{filtered_df['Lead_Time_Days'].mean():.1f} Days")

    # --- Visualization ---
    st.subheader("Inventory Risk Map (Stock vs Lead Time)")
    fig = px.scatter(filtered_df, x="Lead_Time_Days", y="Initial_Stock",
                     size="Annual_Consumption_USD", color="Stock_Status",
                     hover_name="Product_Name", 
                     color_discrete_map={'REORDER NOW': '#ff4b4b', 'HEALTHY': '#28a745'})
    st.plotly_chart(fig, use_container_width=True)

    # --- The Action Table ---
    st.subheader("📋 Procurement Action Plan")
    st.dataframe(filtered_df[filtered_df['Stock_Status'] == 'REORDER NOW'], use_container_width=True)

else:
    st.error("Data file not found. Please ensure Phase 2 has been run and the CSV is in /data/processed/")


# In[9]:


get_ipython().system('streamlit run app_script.py')


# In[ ]:




