import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
from gunho_data import india_gpd_table, create_choropleth_mapbox

st.title("Amazon Easystore 위치 제안")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
"""
)

col1, col2 = st.columns(2)

with col1:
    plan = st.selectbox('plan',
        ('주 별 매출금액','주 별 인구대비 매출금액', '주 별 인구대비 시골인구수')
    )
    
if plan == '주 별 매출금액':
    # 주 별 매출금액 시각화
    fig = create_choropleth_mapbox('Amount', '매출금액')
    st.plotly_chart(fig)
    st.dataframe(india_gpd_table.sort_values(by='Amount', ascending=True))
    state_name = india_gpd_table.sort_values(by='Amount', ascending=True)
elif plan == '주 별 인구대비 매출금액':
    # 주 별 인구대비 매출금액 시각화
    fig = create_choropleth_mapbox('Amount_population', '매출%')
    st.plotly_chart(fig)
    st.dataframe(india_gpd_table.sort_values(by='Amount_population', ascending=True))
    state_name = india_gpd_table.sort_values(by='Amount_population', ascending=True)
else:
    # 주 별 인구대비 시골인구수
    fig = create_choropleth_mapbox('Rural_ratio', '시골인구%')
    st.plotly_chart(fig)
    st.dataframe(india_gpd_table.sort_values(by='Rural_ratio', ascending=False))
    state_name = india_gpd_table.sort_values(by='Rural_ratio', ascending=False)
    
with col2:
    st.metric(label="추천 위치", value=state_name.index[0])
    