import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. UI SETUP
st.set_page_config(page_title="Inventory Intelligence", layout="wide", page_icon="📦")

# Custom CSS for a professional logistics look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #004a99; font-weight: bold; }
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. RESILIENT DATA LOADING
def load_data():
    # Your proven path logic
    paths_to_try = [
        'data/processed/inventory_intelligence.csv',
        '../data/processed/inventory_intelligence.csv',
        'inventory_intelligence.csv'
    ]

    for path in paths_to_try:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['Days_of_Cover'] = (df['Initial_Stock'] / df['Avg_Daily_Demand'].replace(0, 0.001)).round(1)
            df['Current_Stock_Value'] = df['Initial_Stock'] * df['Unit_Cost_USD']
            return df
    return None

df = load_data()

# 3. THE DASHBOARD
if df is not None:
    st.title("📦 Inventory Intelligence")
    st.markdown("### Integrated Inventory Intelligence & Procurement Strategy")

    # Sidebar Filters
    st.sidebar.header("Logistics Controls")
    sources = st.sidebar.multiselect("Shipment Origin", df['Source'].unique(), default=df['Source'].unique())
    categories = st.sidebar.multiselect("Product Sector", df['Category'].unique(), default=df['Category'].unique())

    # Apply filtering
    mask = (df['Source'].isin(sources)) & (df['Category'].isin(categories))
    f_df = df[mask]

    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    reorder_items = f_df[f_df['Stock_Status'] == 'REORDER NOW']

    with c1:
        st.metric("Critical Reorders", len(reorder_items), delta=f"{len(reorder_items)} Pending", delta_color="inverse")
    with c2:
        st.metric("Total Warehouse Value", f"${f_df['Current_Stock_Value'].sum():,.0f}")
    with c3:
        st.metric("Avg. Days of Cover", f"{f_df['Days_of_Cover'].mean():.1f} Days")
    with c4:
        st.metric("Avg. Lead Time", f"{f_df['Lead_Time_Days'].mean():.1f} Days")

    st.divider()

    # Analytics Section
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Inventory Risk Map")
        fig = px.scatter(f_df, x="Days_of_Cover", y="Lead_Time_Days", 
                         size="Current_Stock_Value", color="Stock_Status",
                         hover_name="Product_Name",
                         labels={"Days_of_Cover": "Days until Stockout", "Lead_Time_Days": "Import Time (Days)"},
                         color_discrete_map={'REORDER NOW': '#ff4b4b', 'HEALTHY': '#28a745'},
                         template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Capital Allocation")
        fig_pie = px.pie(f_df, values='Current_Stock_Value', names='Category', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig_pie, use_container_width=True)

    # The Action Table
    st.subheader("Procurement Executive Summary")
    if not reorder_items.empty:
        cols = ['SKU', 'Product_Name', 'Source', 'Initial_Stock', 'Reorder_Point', 'Days_of_Cover', 'Unit_Cost_USD']
        st.dataframe(reorder_items[cols].sort_values('Days_of_Cover'), use_container_width=True)
    else:
        st.success("Logistics health is optimal. No immediate reorders required.")

    # FOOTER
    st.divider()
    st.caption("**Developed by Aklilu Abera** | **Data Analyst & Supply Chain Intelligence**")

else:
    st.error("Data file not found. Ensure 'inventory_intelligence.csv' saved in /data/processed/")
