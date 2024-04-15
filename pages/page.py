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
import plotly.graph_objects as go
from math import sqrt
from scipy.stats import chi2_contingency 


# 타이틀 적용 예시
st.title('고객 분석')

# 특수 이모티콘 삽입 예시
# emoji: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

# Header 적용
st.header('Amazon Sales Report 	:money_with_wings: ')

# Subheader 적용
#st.subheader('장바구니 분석')

# text 삽입 
st.subheader('1. 개요\n\n아마존 데이터의 경우 약3개월( ) 간의 판매 데이터로 주문번호, 상품코드, 판매가격, 판매개수 등의 정보를 담고 있다. EDA 를 통하여 이러한 데이터에 대한 설명과 분석을 진행하고 나서 바구니 분석을 통하여 고객들의 구매패턴을 분석해보고자 한다. ')
st.markdown('2. EDA')


# Amazon 데이터프레임 로드 (가정)
# 예시 데이터를 사용합니다.
amazon = pd.read_csv("data/amazon.csv")  # 파일 경로에 맞게 수정해주세요.

##1.EDA
st.subheader("2. EDA(탐색적 데이터 분석)")


def periodic_sales():
    # "date" 열을 datetime 형식으로 변환
    amazon['date'] = pd.to_datetime(amazon['date'])
    # "month" 열 생성
    amazon['month'] = amazon['date'].dt.month_name()
    # 월별 매출 데이터 생성
    monthly_sale = amazon.groupby("month")['order_amount'].sum()

    # 원하는 순서대로 월별 매출 데이터 정렬
    desired_order = ['April', 'May', 'June']
    monthly_sale = monthly_sale.reindex(desired_order)

    # 그래프 생성
    fig = go.Figure(data=[go.Bar(x=monthly_sale.index, y=monthly_sale.values)])

    # 그래프 레이아웃 설정
    fig.update_layout(
                      xaxis_title="Month",
                      yaxis_title="Order Amount")

    # 그래프 출력
    st.title("Periodic Sales")
    st.plotly_chart(fig)
    st.markdown('4,5,6 월 모두 매출액 하락이 나타났다.매출 하락에 영향을 미치는 변수를 찾아보기 위하여 먼저 컬럼간의 관계를 살펴보고자 한다.')

# 크래머 V 계수를 계산하는 함수 정의
def CramerV(var1, var2):
    pivot_tb = pd.crosstab(var1, var2, margins=False)
    chi_sq, _, _, _ = chi2_contingency(pivot_tb) 
    n = len(var1)
    k = len(var1.unique())
    r = len(var2.unique())
    V = sqrt((chi_sq / n) / (min(k - 1, r - 1)))
    return V


def CramerV_visualization():
    st.title("Cramer's V Coefficients")
    # 업로드된 파일을 데이터프레임으로 읽기
    cramer_df = pd.read_csv('data/cramer_df.csv')

    # 크래머 V 계수를 계산할 컬럼들
    columns = ['ship_status', 'fullfilment', 'ship_service', 'product_category', 'state', 'customer_type', 'promotion', 'Festival Name']

    # 크래머 V 계수를 저장할 행렬 생성
    cramer_matrix = pd.DataFrame(index=columns, columns=columns)

    # 크래머 V 계수 계산
    for column1 in columns:
        for column2 in columns:
            if column1 != column2:
                V = CramerV(cramer_df[column1], cramer_df[column2])
                # 크래머 V 계수를 행렬에 저장할 때, NaN 대신 0으로 변환
                if np.isnan(V):
                    V = 0
                cramer_matrix.loc[column1, column2] = V

    # 시각화 - 히트맵
    plt.figure(figsize=(10, 8))
    sns.heatmap(cramer_matrix.astype(float), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Cramer's V Coefficients")
    fig, ax = plt.subplots()
    ax = sns.heatmap(cramer_matrix.astype(float), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    st.pyplot(fig)

def ols():
    st.image('data/ols.png', caption='선형회귀분석 결과', use_column_width=True)
    
def top_product():
    st.image('data/top_product.png',caption = 'Top4 product_category 매출액 추이', use_column_width= True)

def price():
    st.markdown('카테고리별 가격대를 살펴보자.')

    # 카테고리별 평균 가격 계산
    avg_price_by_category = amazon.groupby('product_category')['sale_amount'].mean().sort_values(ascending=False)

    # 그래프 크기 설정
    plt.figure(figsize=(12, 6))

    # 박스 플롯 그리기
    amazon.boxplot(column='sale_amount', by='product_category', figsize=(12,6), rot=45)

    plt.title("카테고리별 가격 분포")

    # Matplotlib 그래프를 Streamlit에 표시
    st.pyplot(plt)
    st.markdown('평균가격이 높은 순서대로 살펴보면 Set, Saree, Western Dress, Ethnic Dress, Top 등의 카테고리가 높은 가격대를 보였다. 가격대 분포를 살펴보면, Set, Ethnic Dress 의 경우 가격대 분포가 넓게 나타났고, Set,Top Kurta ,Western Dress 의 경우에는 이상치(outlier)가 두드러지게 나타났다. ')


def category():
    st.markdown('판매개수에 해당하는 order_quantity와 판매가격에 해당하는 sale_amount 컬럼을 통하여 order_amount 컬럼을 생성하여 판매액을 도출하고 카테고리별 매출액을 시각화해보았다.')

    # 카테고리별 매출액 계산
    category_sum = amazon.groupby('product_category')['order_amount'].sum().sort_values(ascending=False)

    # 그래프 크기 설정
    plt.figure(figsize=(10, 6))

    # 막대 그래프 그리기
    plt.bar(category_sum.index, category_sum.values,  
            color=('#969696', '#bdbdbd', 'orange', '#d9d9d9', 'grey', 'gray', 'darkgray'))

    # y 축의 눈금 포맷을 정수로 설정합니다.
    plt.gca().yaxis.set_major_formatter('{:.0f}'.format)

    plt.title('카테고리별 매출액 분포')
    plt.xlabel('Category')
    plt.ylabel('판매총액')

    # Matplotlib 그래프를 Streamlit에 표시
    st.pyplot(plt)
    st.markdown("Set,Kurta, Western Dress, Top, Ethnic Dress 순으로 판매액이 높았다. 이러한 제품군을 크게 전통옷과 비전통옷으로 분류해서도 알아보았다. Set, Kurta, Ethnic Dress, Saree, Dupatta 의 경우 전통옷으로 분류하고 나머지는 비전통옷으로 분류해서 매출액 비중을 살펴보았다.")

def tradition():
    # 전통옷 카테고리 정의
    traditional_categories = ['Set', 'kurta', 'Ethnic Dress', 'Saree', 'Dupatta']

    # 전통옷 카테고리에 해당하는 제품을 필터링
    tradition = amazon[amazon['product_category'].isin(traditional_categories)]

    # 비전통옷 카테고리에 해당하는 제품을 필터링
    non_tradition = amazon[~amazon['product_category'].isin(traditional_categories)]

    # 전통옷와 비전통옷 매출액을 계산합니다.
    tradition_sale = tradition['sale_amount'].sum()
    non_tradition_sale = non_tradition['sale_amount'].sum()

    # 각 카테고리별 매출액 계산
    category_sales = [amazon[amazon['product_category'] == 'Set']['order_amount'].sum(),
                      amazon[amazon['product_category'] == 'kurta']['order_amount'].sum(),
                      amazon[amazon['product_category'] == 'Ethnic Dress']['order_amount'].sum()]

    # 전체 매출액 계산
    total_sales = sum(category_sales)

    # 각 카테고리별 매출액 백분율 계산
    category_percentages = [(sales / total_sales) * 100 for sales in category_sales]

    # make figure and assign axis objects
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0.5)  # 각 서브플롯 간의 간격 조정

    # pie chart parameters
    overall_ratios = (tradition_sale, non_tradition_sale)
    labels = ['전통옷', '비전통옷']
    explode = [0.1, 0]  # 첫 번째 조각을 투영
    # rotate so that first wedge is split by the x-axis
    angle = -180 * overall_ratios[0]
    wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                         labels=labels, explode=explode)

    # 바 차트 그리기
    x_positions = x_positions = np.arange(len(category_sales))
    bar_width = 0.4
    bars = ax2.bar(x_positions, category_percentages, width=bar_width, color='grey')
    

    # x 축에 카테고리 레이블 추가
    category_labels = ['Set', 'Kurta', 'Ethnic Dress']
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(category_labels)

    # y 축 레이블과 타이틀 추가
    ax2.set_ylabel('매출액(%)')
    ax2.set_title('카테고리별 매출액')

    # 바 차트에 백분율 표시하기
    for bar, percentage in zip(bars, category_percentages):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, f'{percentage:.1f}%',
                 ha='center', va='bottom')

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r

    # draw top connecting line
    x = r * np.cos(np.deg2rad(theta2)) + center[0]
    y = r * np.sin(np.deg2rad(theta2)) + center[1]
    con = ConnectionPatch(xyA=(0, 0), coordsA=ax2.transAxes,
                          xyB=(x, y), coordsB=ax1.transData,
                          arrowstyle="-")
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.deg2rad(theta1)) + center[0]
    y = r * np.sin(np.deg2rad(theta1)) + center[1]
    con = ConnectionPatch(xyA=(0, 1), coordsA=ax2.transAxes,
                          xyB=(x, y), coordsB=ax1.transData,
                          arrowstyle="-")
    ax2.add_artist(con)

    # Streamlit에 플롯을 표시
    st.pyplot(fig)





if __name__ == "__main__":
    periodic_sales()
    CramerV_visualization()
    ols()
    price()
    category()
    tradition()
    top_product()
