from recommend_data import test_df, train_df, le_item, le_user
import time
import numpy as np

import tensorflow as tf
import pandas as pd
from tqdm import tqdm

score_matrix = train_df.pivot(columns='parent_asin', index='user_id', values='lables')

# 데이터셋 준비
def prepare_dataset(train, test):
    train_users = train['user_id'].values
    train_items = train['parent_asin'].values
    train_ratings = train['lables'].fillna(0).values

    test_users = test['user_id'].values
    test_items = test['parent_asin'].values
    test_ratings = test['lables'].values
    return train_users, train_items, train_ratings, test_users, test_items, test_ratings

# (user u, item i) 에 대한 선호확률 pred 함수
def predict(user_id, parent_asin, model):
    pred = model.predict([np.array([user_id]), np.array([parent_asin])])
    return pred

# user 한 명에 대한 추천 결과 가져오기
def recommend(user_id, model, score_matrix, N):

    user_id_encoded = le_user.fit_transform([user_id])[0]
    
    # 안 산 상품 추출
    user_rated = score_matrix.loc[user_id_encoded].dropna().index.tolist()
    user_unrated = score_matrix.columns.drop(user_rated).tolist()
    

    # 안 산 상품에 대해서 예측하기
    predictions = model.predict([np.full((len(user_unrated), ), user_id_encoded), np.array(user_unrated)], verbose=0).flatten()
    result = pd.DataFrame({'parent_asin':le_item.inverse_transform(user_unrated), 'pred_rating':predictions})

    # pred값에 따른 정렬해서 결과 띄우기
    top_N = result.sort_values(by='pred_rating', ascending=False)[:N]
    return top_N

# user 한명에 대한 precision, recall 측정
def precision_recall_at_k(target, prediction):
    num_hit = len(set(prediction).intersection(set(target)))
    precision = float(num_hit) / len(prediction) if len(prediction) > 0 else 0.0
    recall = float(num_hit) / len(target) if len(target) > 0 else 0.0
    return precision, recall