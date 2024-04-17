import streamlit as st
import pandas as pd
from keras.models import load_model
from recommend import score_matrix, recommend
from recommend_data import review_ratings

def main():
    st.title('Neural Collaborative Filtering (NCF)기반 추천 시스템')
    st.caption('*사용자 id를 입력하세요*:sunglasses:')

    rec_model = load_model('models/recommend_model.keras')

    # 측정 결과들 모아두는 df
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame({
            'product_id': [],
            'pre_rating' : []
        })

        st.session_state.df2 = pd.DataFrame({
            'user_id': review_ratings['user_id'],
            'count':review_ratings['rating']
        })

    with st.form(key='문장입력 form'):
        userId = st.text_input("사용자 ID:")
        form_submitted = st.form_submit_button('상품 추천')

    if form_submitted:
        if userId:
            recommend_item = recommend(userId, rec_model, score_matrix, 5)

            st.session_state.df = pd.DataFrame({
                'product_id': recommend_item['parent_asin'],
                'pre_rating' : recommend_item['pred_rating']
            })
            
    
            st.success('성공!')
        else:
            st.write("사용자 ID를 입력하시요.")
            st.error('존재하지 않는 사용자입니다.')

    st.divider()
    col1, col2, col3= st.columns(3)
    
    # df 크기 조절
    col1.checkbox("창 크기조절", value=True, key="use_container_width")

    # df 리셋 버튼
    if col2.button("데이터 리셋하기"):
        st.session_state.df = pd.DataFrame({
            'product_id': [],
            'pre_rating' : []
        })

    # df csv로 다운로드
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False, header=True).encode('cp949')
    csv = convert_df(st.session_state.df)
    col3.download_button(
        label="CSV로 다운받기",
        data=csv,
        file_name='sts_data_outputs.csv',
        mime='text/csv',
    )

    st.dataframe(st.session_state.df, use_container_width=st.session_state.use_container_width)


    st.subheader('User_id 리스트', divider='rainbow')

    st.dataframe(st.session_state.df2, use_container_width=st.session_state.use_container_width)

main()