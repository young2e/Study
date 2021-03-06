# keras14_mlp1을 Sequential 에서 함수형으로 변경
# earlyStopping 적용

#1. 데이터 
import numpy as np
x = np.array([range(1,101), range(311,411), range(100)])
y = np.array([range(101,201), range(711,811), range(100)]) 

print("x.shape :", x.shape)  # (3, 100)
print("y.shape :", y.shape)  # (3, 100)


x = np.transpose(x) 
y = np.transpose(y)

print("x_trans :", x.shape)  # (100, 3)
print("y_trans :", y.shape)  # (100, 3)


from sklearn.model_selection import train_test_split    
x_train, x_test, y_train, y_test = train_test_split(    
    x, y, random_state=77, shuffle=True,
    train_size=0.8 
)   

print(x_test)
print(y_test)

print("x_train.shape :", x_train.shape) # (80, 3)
print("y_test.shape :", y_test.shape)   # (20, 3)


#2. 모델구성                      
from keras.models import Sequential, Model
from keras.layers import Dense, Input

input1 = Input(shape=(3, ))   
dense1_1 = Dense(30, activation = 'relu', name = 'dense1_1')(input1) 
dense1_2 = Dense(60, activation = 'relu', name = 'dense1_2')(dense1_1) 
dense1_3 = Dense(90, activation = 'relu', name = 'dense1_3')(dense1_2) 
dense1_4 = Dense(50, activation = 'relu', name = 'dense1_4')(dense1_3) 

output1 = Dense(20, name = 'output1')(dense1_3)
output1_2 = Dense(10, name = 'output1_2')(output1)
output1_3 = Dense(3, name = 'output1_3')(output1_2)

model = Model(inputs = input1, outputs = output1_3)

model.summary()

#3. 훈련 
model.compile(loss='mse', optimizer='adam', metrics=['mse'])

from keras.callbacks import EarlyStopping # keras에서 제공하는 callbakcs 패키지의 EarlyStopping 모듈을 import!
early_stopping = EarlyStopping(monitor='loss', patience=10, mode = 'auto') 

# 'loss'로 monitor, 관찰하겠다
# 10번 흔들리면 조기종료시키겠다
# mode는 니가 알아서 해 달라 , auto

model.fit(x_train, y_train, epochs=1000, batch_size=32,
           validation_split = 0.2, verbose = 1,
           callbacks=[early_stopping]) 


#4. 평가, 예측
loss, mse = model.evaluate(x_test, y_test, batch_size=32) 
print("loss : ", loss)
print("mse : ", mse)

y_predict = model.predict(x_test)
print(y_predict)

# RMSE 구하기
from sklearn.metrics import mean_squared_error 
def RMSE(y_test, y_predict):                   
    return np.sqrt(mean_squared_error(y_test, y_predict))                                          
print("RMSE : ", RMSE(y_test, y_predict))     


# R2 구하기
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)  
print("R2 : ", r2)

'''
dense1_1 = Dense(30, activation = 'relu', name = 'dense1_1')(input1) 
dense1_2 = Dense(60, activation = 'relu', name = 'dense1_2')(dense1_1) 
dense1_3 = Dense(90, activation = 'relu', name = 'dense1_3')(dense1_2) 
dense1_4 = Dense(50, activation = 'relu', name = 'dense1_4')(dense1_3) 

output1 = Dense(20, name = 'output1')(dense1_3)
output1_2 = Dense(10, name = 'output1_2')(output1)
output1_3 = Dense(3, name = 'output1_3')(output1_2)

epo 1000, es 10, batch 32, val 0.2
RMSE :  0.04171367808786477
R2 :  0.9999976353134654
'''