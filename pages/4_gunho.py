import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
from gunho_data import india_gpd_table, create_choropleth_mapbox

st.title("Amazon Easystore 위치 제안")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    **Amazon Easystore**란 온라인 쇼핑이 익숙하지 않은 새로운 사용자 대상으로 하는 매장이며, Amazon의 다양한 제품을 작접 체험하고, 
    매장 직원의 도움을 받아 상품을 주문 및 결제할 수 있게 함.<br>
    이러한, **Amazon Easystore 위치 제안**은 온라인 쇼핑을 경험하지 못한 미래 고객 확보를 목표로함.
"""
, unsafe_allow_html=True)

col1, col2, col3 = st.columns([6.5, 1, 2.5])

with col1:
    plan = st.selectbox('Plan',
        ('plan1','plan2', 'plan3')
    )
    if plan == 'plan1':
        st.markdown('<div style="font-size:18px; font-weight:bold;">주 별 매출금액이 낮은 지역에 위치 제안</div>', unsafe_allow_html=True)
    elif plan == 'plan2':
        st.markdown('<div style="font-size:18px; font-weight:bold;">주 별 인구대비 매출비율이 낮은 지역에 위치 제안</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:18px; font-weight:bold;">주 별 인구대비 시골인구비율이 높은 지역에 위치 제안</div>', unsafe_allow_html=True)
    
if plan == 'plan1':
    # 주 별 매출금액 시각화
    fig = create_choropleth_mapbox('Amount', '매출금액', 'Turbo')
    st.plotly_chart(fig)
    st.dataframe(india_gpd_table.sort_values(by='Amount', ascending=True))
    state_name = india_gpd_table.sort_values(by='Amount', ascending=True)
elif plan == 'plan2':
    # 주 별 인구대비 매출금액 시각화
    fig = create_choropleth_mapbox('Amount_population', '매출%', 'Turbo')
    st.plotly_chart(fig)
    st.dataframe(india_gpd_table.sort_values(by='Amount_population', ascending=True))
    state_name = india_gpd_table.sort_values(by='Amount_population', ascending=True)
else:
    # 주 별 인구대비 시골인구수
    fig = create_choropleth_mapbox('Rural_ratio', '시골인구%', 'Turbo')
    st.plotly_chart(fig)
    st.dataframe(india_gpd_table.sort_values(by='Rural_ratio', ascending=False))
    state_name = india_gpd_table.sort_values(by='Rural_ratio', ascending=False)
    
with col3:
    local_list = []
    for i in range(0,5):
        local_list.append(state_name.index[i])
    st.markdown(
        f"""
            <div style="font-size:14px; font-weight:bold;">위치 추천</div>
            {''.join([f'<div style="color:green; font-size:14px; font-weight:bold; line-height:1.2">{item}</div>' for item in local_list])}
        <br>
        """, unsafe_allow_html=True)


