import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
from gunho_data import india_gpd_table, create_choropleth_mapbox

st.markdown("""
<style>
	[data-testid="stMetricValue"]{
        color: green;
    }
    [data-testid="stText"]{
        color: green;
        font-weight: bold;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Amazon Easystore 위치 제안")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    **Amazon Easystore**란 온라인 쇼핑이 익숙하지 않은 새로운 사용자 대상으로 하는 매장이며, Amazon의 다양한 제품을 작접 체험하고, 
    매장 직원의 도움을 받아 상품을 주문 및 결제할 수 있게 한다.
    이러한 **Amazon Easystore 위치 제안**은 아마존 온라인 쇼핑을 경험하지 못한 미래 고객을 확보하는 것을 목표로한다.
"""
)

col1, col2 = st.columns([7, 3])

with col1:
    plan = st.selectbox('방안',
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
    local_list = []
    for i in range(0,5):
        local_list.append(state_name.index[i])
    # st.subheader('위치 추천')
    # st.text('\n'.join(local_list))
    # st.metric(label="추천 위치", value='\n'.join(local_list))
    st.markdown(f"""
            <div style="font-size:14px; font-weight:bold;">위치 추천</div>
            {''.join([f'<div style="color:green; font-size:14px; font-weight:bold; line-height:1.2">{item}</div>' for item in local_list])}
            <br>
            """, unsafe_allow_html=True)


