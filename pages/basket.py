import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import plotly.express as px
import matplotlib
matplotlib.rcParams['font.family']='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False
import seaborn as sns

# 텍스트 삽입
st.markdown('## 3. 장바구니 분석')

def basket():
    st.image('data/basket.jpg', caption='장바구니 분석', use_column_width=True)
    st.markdown("장바구니 : 시스템 내에 존재하는 유지되는 상품의 집합")
    st.markdown("장바구니 분석을 통해 알 수 있는 것: 가격 개선, 쿠폰과 할인 추천, 위치 배치")

def basket_processing():
    st.subheader("장바구니 분석 가능한 데이터 정제")

    sample_code = '''
    basket = amazon.copy()
    basket1 = basket[basket['order_quantity'] > 0]
    basket1.drop(columns=['date', 'ship_status', 'fullfilment', 'ship_service',
                       'sku', 'product_category', 'size', 'asin', 'courier_status',
                       'order_quantity', 'sale_amount', 'city', 'state', 'zip', 'promotion',
                       'customer_type', 'month', 'latitude', 'longitude', 'order_amount'], inplace=True)
    '''
    st.code(sample_code, language="python")

    sample_code2 = '''
    order_ID_list = basket1['order_ID'].tolist()
    from tqdm import tqdm

    style_list = []
    # tqdm 함수로 반복문 감싸기
    for num in tqdm(list(set(basket1['order_ID'].tolist()))):
        # 하나의 order_ID로 필터링
        tmp_df = basket1[basket1['order_ID'] == num]
        # style 컬럼에서 style item 추출해서 리스트로 변환
        tmp_items = tmp_df['style'].tolist()
        # style_list 에 append 하기
        style_list.append(tmp_items)
    '''
    st.code(sample_code2, language="python")

def single_item():
    st.subheader("style_list에서 1개의 아이템만 존재하는 경우 알아보기")
    st.markdown("단일 상품 및 복수 상품 구매 비율")
    st.markdown("#108,151 건의 거래(unique한 order_id) 와 1371 개의 상품 존재 ")
    st.markdown("single_item_list: 101977")
    st.markdown("단일 상품만 구매하는 경우: 94.3%")

def mlxtend():
    st.subheader("mlxtend 라이브러리를 활용하여 장바구니 분석")
    # 여기에 mlxtend 라이브러리 활용 예시 코드를 넣어주세요.
    st.markdown("1. 데이터 전처리 : mlxtend를 사용하여 데이터 인코딩하여 True/False 값을 갖는 데이터 프레임 형태로 변환")
    st.markdown(""" 이와 같은 형태로 반환
    [[1, 0, 1, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1]]
    """)
    st.markdown("2.Apriori 알고리즘 : frequent itemsets 을 main memory 에서 찾기 위한 multi-pass algorithm")
    st.markdown(""" 
    key idea : Pruning(가지치기)
    - 아이템셋 {B, D}가 frequent 할 경우, {B},{D} 도 그렇다.
    - 아이템셋 {B}가 frequent 하지 않을 경우 {B,D} 또한 frequent 하지 않다.             
    """)
    sample_code3 = '''
    #최소 지지도를 0.001 로 설정하기
    mod_minsupport = mlxtend.frequent_patterns.apriori(basket_encoder_df, min_support=0.01)

    #지지도 값이 최소 지지도 값보다 큰 모든 아이템을 포함하고 있음 
    mod_colnames_minsupport = mlxtend.frequent_patterns.apriori(basket_encoder_df, 
                                                            min_support=0.01,
                                                            use_colnames = True)
    mod_colnames_minsupport
    '''
    st.code(sample_code3, language="python")
    st.image('data/support.png', caption='지지도', use_column_width=True)


if __name__ == "__main__":
    basket()
    basket_processing()
    single_item()
    mlxtend()
