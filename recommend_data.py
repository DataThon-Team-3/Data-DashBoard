import os
import time
import numpy as np
import pandas as pd
import pandas as pd
from tqdm import tqdm

# 데이터 로드
ratingNCF = pd.read_csv('./data/review2022_2023.csv', index_col='Unnamed: 0')

from sklearn.preprocessing import LabelEncoder
 
# 유저와 상품을 고유한 정수로 인코딩
le_user = LabelEncoder()
le_item = LabelEncoder()
ratingNCF['user_id'] = le_user.fit_transform(ratingNCF['user_id'])
ratingNCF['parent_asin'] = le_item.fit_transform(ratingNCF['parent_asin'])
 
# 필요없는 열 제거
ratingNCF.drop(['price', 'year'], axis=1, inplace=True)
ratingNCF.head()
 
# 총 유저, 상품 수
num_user = ratingNCF['user_id'].nunique()
num_item = ratingNCF['parent_asin'].nunique()

# train에서 학습한 유저가 test 세트에서 존재하지 않을 수도 있어서 NCF 논문에서는 leave_one_out 방식으로 데이터를 분리

# 평점이 3 이상인 경우 만족(1), 아닌경우 불만족(0)
ratingNCF['stars'] = (ratingNCF['rating'] >= 3).astype(int)
 
# 유저별로 groupby 한 후에, 가장 첫번째 데이터를 test 세트로 분리한다.
ratingNCF['rank_latest'] = ratingNCF.groupby(['user_id'])['timestamp'].rank(method='first', ascending=False)
 
test_ratings = ratingNCF[ratingNCF['rank_latest'] != 1]
train_ratings = ratingNCF[ratingNCF['rank_latest'] == 1]
 
train_ratings = train_ratings[['user_id', 'parent_asin', 'stars']]
test_ratings = test_ratings[['user_id', 'parent_asin', 'stars']]
 
 # star 열 lables로 이름 변경
train_df = train_ratings.rename({'stars':'lables'}, axis=1)
test_df = test_ratings.rename({'stars':'lables'}, axis=1)

review_rating = ratingNCF.groupby('user_id')['rating'].count().sort_values(ascending=False)

review_ratings = pd.DataFrame(review_rating)

review_ratings.reset_index(inplace=True)

review_ratings['user_id'] = le_user.inverse_transform(review_ratings['user_id'])

