import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd

# st.set_page_config(layout='wide')
# st.markdown(
#     """
# <style>
# [data-testid="stAppViewBlockContainer"] {
#     padding: 1rem 30rem 5rem 30rem;
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

india_gpd = gpd.read_file('./data/gunho/india_gpd/India_gpd.shp')

india_gpd = india_gpd.drop(1)
india_gpd = india_gpd.set_index('ship_state')

india_gpd['center'] = india_gpd['geometry'].centroid
india_gpd['lon'] = india_gpd['center'].x
india_gpd['lat'] = india_gpd['center'].y

# 주별 인구대비 매출금액
india_gpd['Amount_population'] = india_gpd['Amount'] / india_gpd['Population'] * 100
# 주별 인구대비 시골인구
india_gpd['Rural_ratio'] = india_gpd['Rural'] / india_gpd['Population'] * 100
# 주별 인구대비 도시인구
india_gpd['Urban_ratio'] = india_gpd['Urban'] / india_gpd['Population'] * 100

india_gpd_table = india_gpd[['Qty', 'Amount', 'Population', 'Male', 'Female', 'Rural', 'Urban','Amount_population', 'Rural_ratio']]


def create_choropleth_mapbox(color_col, label_text, color_style):
    fig = px.choropleth_mapbox(data_frame=india_gpd,
                               geojson=india_gpd.geometry,
                               locations=india_gpd.index,
                               color=color_col,
                               color_continuous_scale=color_style,
                               range_color=(india_gpd[color_col].min(), india_gpd[color_col].max()),
                               mapbox_style="carto-positron",
                               zoom=3,
                               center={"lat": india_gpd['lat'].mean(), "lon": india_gpd['lon'].mean()},
                               opacity=0.5,
                               labels={color_col: label_text}
                              )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        # title={
        #     'text': title,
        #     'y': 0.95,
        #     'x': 0.5,
        #     'xanchor': 'center',
        #     'yanchor': 'top',
        #     'font': {'size': 24}
        # }
    )

    return fig

st.title("Amazon Easystore 위치 제안")



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


