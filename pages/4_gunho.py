import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
from gunho_data import india_gpd_table, create_choropleth_mapbox

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
"""
)

# 주 별 매출 금액 시각화
fig = create_choropleth_mapbox('Amount', '주 별 매출 금액')
st.plotly_chart(fig)

st.dataframe(india_gpd_table)