# GradientBoostRegressor 의 output column 문제 해결 
# 방법 1. MultiOutputRegressor 적용 -> dacon_GBR_m 
# 방법 2. Y data에 PCA 적용 -> dacon_GBR_p

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

data = pd.read_csv("./data/dacon/comp1/train.csv", header = 0, index_col = 0)
x_pred = pd.read_csv("./data/dacon/comp1/test.csv", header = 0, index_col = 0)
submit = pd.read_csv("./data/dacon/comp1/sample_submission.csv", header = 0, index_col = 0)

print("train.shape : ", data.shape)     # (10000, 75)    
print("test.shape : ", x_pred.shape)    # (10000, 71)         
print("submit.shape : ", submit.shape)  # (10000, 4)

# 결측치 확인 및 처리
# 각 column 별로 결측치가 얼마나 있는지 알 수 있다
print(data.isnull().sum()) 

# 선형보간법 적용(모든 결측치가 처리 되는 건 아니기 때문에 검사가 필요하다)
data = data.interpolate() 
x_pred = x_pred.interpolate()

# 결측치에 평균을 대입
data = data.fillna(data.mean())
x_pred = x_pred.fillna(x_pred.mean())

# 결측치 모두 처리 됨을 확인
# print(data.isnull().sum()) 
# print(x_pred.isnull().sum()) 


# for feature_importances
x_data = data.iloc[:, :-4]


# npy 변환 및 저장
np.save("./data/dacon/comp1/data.npy", arr = data)
np.save("./data/dacon/comp1/x_pred.npy", arr = x_pred)

# npy data load
data = np.load("./data/dacon/comp1/data.npy",  allow_pickle = True)
x_pred = np.load("./data/dacon/comp1/x_pred.npy", allow_pickle = True)

print("data.shape :", data.shape)     # (10000, 75)
print("x_pred.shape :", x_pred.shape) # (10000, 71)


# 전체 data를 x, y 분리(슬라이싱)
x = data[:, :-4]
y = data[:, -4:]

print("======데이터 슬라이싱=====")
print("x.shape :", x.shape)  # (10000, 71)
print("y.shape :", y.shape)  # (10000, 4)
print()


# y -> PCA
pca = PCA(n_components = 1)
pca.fit(y)
y_pca= pca.transform(y)

print("y_pca.shape :", y_pca.shape)

# PCA 적용한 y에 scaler 사용
# PCA 적용하면서 차원을 강제적으로 축소 -> 예외적인 경우가 발생할 수 있음
# 이상치 등으로 인한 문제를 방지하기 위해 스케일링 작업을 해 준다
scaler = RobustScaler()
scaler.fit(y_pca)
y = scaler.transform(y_pca)


# train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size = 0.2, shuffle = True, random_state = 11
)

# print("x_train.shape :", x_train.shape) # (8000, 71)
# print("x_test.shape :", x_test.shape)   # (2000, 71)
# print("y_train.shape :", y_train.shape) # (8000, 4)
# print("y_test.shape :", y_test.shape)   # (2000, 4)

# PCA
print("x_train.shape :", x_train.shape) # (8000, 71)
print("x_test.shape :", x_test.shape)   # (2000, 71)
print("y_train.shape :", y_train.shape) # (8000, 1)
print("y_test.shape :", y_test.shape)   # (2000, 1)


# 2. 모델 구성

model = GradientBoostingRegressor()

# 3. 훈련
model.fit(x_train, y_train)

# 4. 평가, 예측

# 머신러닝에서 회귀 모델의 score : R2 (자동)
score = model.score(x_test, y_test)

# mae 평가지표에 넣기 위한 y_pred
y_pred = model.predict(x_test)

# x_test를 모델에 넣어 예측한 y_pred와 실젯값 y_test 오차 비교
mae = mean_absolute_error(y_test , y_pred)

print("R2 :", score)
print("MAE :", mae)

'''
R2 : -0.011436525893423255
MAE : 0.6007508773252448
'''

# 주어진 x_pred 데이터로 최종 예측해야 할 y_pred 예측
# 현재 PCA가 적용된 상태 (마지막에 원상 복구를 해야 한다)
submit_pca = model.predict(x_pred)

# shape 오류가 나서, 한 번 데이터 shape 확인
# 벡터 형태이다(PCA 적용된 데이터가 가중치연산 후에 벡터 모양으로 출력됨)
# output 1이니 형태로 맞춰줘야 하므로 아래에서 reshape
print("submit_pca.shape :", submit_pca.shape) # (10000,)
submit_pca = submit_pca.reshape(submit.shape[0], 1)

# pca 적용된 상태이므로 최종 파일에 맞게끔 column을 '4'개로 차원 다시 원상 복구
# pca.inverse_transform(데이터명) 을 쓴다
submit = pca.inverse_transform(submit_pca)
print("submit_recovered :", submit)

# 최종 파일 변환
a = np.arange(10000,20000)
submit= pd.DataFrame(submit, a)
submit.to_csv("./dacon/comp1/submit_GBR_p.csv", header = ["hhb", "hbo2", "ca", "na"], index = True, index_label="id" )

#####################################################################
# GradientBoostingRegressor 모델은
# 벡터 형태의 output을 갖춘 데이터만 가능
# 따라서 column이 4개인 y data를 하나씩 잘라서 훈련 및 평가를 해야 한다
# for문을 통해서 실행
# 컬럼 수 만큼 for문을 실행 : for i in range(len(submit.columns))
# index[0] column fit -> index[0] column test -> score 
# index[3] column 까지 마치면 
# x_pred로 predict을 해서 y_pred 를 만드는데
# y_pred도 컬럼별로 각각 생성되기 때문에
# append 함수를 써서 모두 붙여준다

############################################################
# def boost_fit_mae(y_train, y_test) :
#     y_predict = []
#     for i in range(len(submit.columns)) :
#         print(i)
#         y_train_i = y_train[:, i]
#         model.fit(x_train, y_train_i)

#         y_test_i = y_test[:, i]
#         score = model.score(x_test, y_test_i)
#         print("score :", score)

#         y_pred = model.predict(x_pred)
#         y_predict.append(y_pred)
#         # print(y_predict)
#     return np.array(y_predict)
# ##############################################################

########################### 함수 적용############################
# for문으로 한 컬럼씩 훈련, 평가 시켜서 나중에 append로 모두 붙이는데
# 10000, 4 가 아닌 4, 10000 즉 행과 열이 바뀐 모양으로 만들어진다
# 따라서 reshape

# submit = boost_fit_mae(y_train, y_test)
# print("submit.shape :", submit.shape)

# reshape 
# submit = boost_fit_mae(y_train, y_test).reshape(10000, 4)
# print("submit.shape :", submit.shape)


########################feature_importances####################################
# print(model.feature_importances_)

# def plot_feature_importances_x_data(model) :
#     n_features = x_data.shape[1]
#     plt.barh(np.arange(n_features), model.feature_importances_, align='center')
#     plt.yticks(np.arange(n_features), x_data.columns)
#     plt.xlabel("Feature Importances")
#     plt.ylabel("Features")
#     plt.ylim(-1, n_features)

# plot_feature_importances_x_data(model)
# plt.show()





