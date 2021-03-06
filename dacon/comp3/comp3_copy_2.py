import os
import json
import numpy as np
from tqdm import tqdm
# import jovian
import numpy as np

def kaeri_metric(y_true, y_pred):
    '''
    y_true: dataframe with true values of X,Y,M,V
    y_pred: dataframe with pred values of X,Y,M,V
    
    return: KAERI metric
    '''
    
    return 0.5 * E1(y_true, y_pred) + 0.5 * E2(y_true, y_pred)


### E1과 E2는 아래에 정의됨 ###

def E1(y_true, y_pred):
    '''
    y_true: dataframe with true values of X,Y,M,V
    y_pred: dataframe with pred values of X,Y,M,V
    
    return: distance error normalized with 2e+04
    '''
    
    _t, _p = np.array(y_true)[:,:2], np.array(y_pred)[:,:2]
    
    return np.mean(np.sum(np.square(_t - _p), axis = 1) / 2e+04)


def E2(y_true, y_pred):
    '''
    y_true: dataframe with true values of X,Y,M,V
    y_pred: dataframe with pred values of X,Y,M,V
    
    return: sum of mass and velocity's mean squared percentage error
    '''
    
    _t, _p = np.array(y_true)[:,2:], np.array(y_pred)[:,2:]
    
    
    return np.mean(np.sum(np.square((_t - _p) / (_t + 1e-06)), axis = 1))

# import matplotlib as plt
import matplotlib.pyplot as plt

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, Flatten,MaxPooling2D,BatchNormalization,Lambda, AveragePooling2D
import keras.backend as K
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
import pandas as pd

# X_data = []
# Y_data = []

X_data = np.loadtxt('./data/dacon/comp3/train_features.csv',skiprows=1,delimiter=',')
# np.loadtxt : loadtxt는 csv, txt 파일 등을 읽기 위한 함수
# - np.loadtxt 는 ("파일경로", 파일ㄹ에서 사용한 구분자, 데이터타임 지정) 등을 이용해 파일을 일거와
# - X_data 라는 변수에 array로 넣어준다
# delimiter : 구분기호 (padnas : sep과 같음)
# skiprows : 특정 행 제거 
# usecols : 특정 컬럼 사용
X_data = X_data[:,1:] # id column은 제외하고 나머지 time, s1 ~ s4 데이터를 X_data로 사용
print("X_data.shape :", X_data.shape) # (1050000, 5) 
     
    
Y_data = np.loadtxt('./data/dacon/comp3/train_target.csv',skiprows=1,delimiter=',')
Y_data = Y_data[:,1:] # id column 제외
print("Y_data.shape :", Y_data.shape) # (2800, 4)

X_data = X_data.reshape((2800,375,5,1)) # Conv2D 사용하기 위해 reshape, 한 아이디당 375개씩 있으므로 375, 5, 1로 reshape
print("X_data.reshape :", X_data.shape) # (2800, 375, 5, 1)

X_data_test = np.loadtxt('./data/dacon/comp3/test_features.csv',skiprows=1,delimiter=',')
# 최종 예측에 사용할 데이터 준비, 역시 슬라이싱과 reshape 을 해 준다
X_data_test = X_data_test[:,1:]
X_data_test = X_data_test.reshape((700,375,5,1))

data_id = 2

plt.figure(figsize=(8,6))

# X_data[data_id, :, 0, 0] -> 세 번째에 0 이 오면 time에 대한 그래프 아닌가?
# 1로 바꿔주고 나머지 2, 3, 4 해야 s1 ~ s4 그래프 같은데
plt.plot(X_data[data_id,:,1,0], label="Sensor #1")
plt.plot(X_data[data_id,:,2,0], label="Sensor #2")
plt.plot(X_data[data_id,:,3,0], label="Sensor #3")
plt.plot(X_data[data_id,:,4,0], label="Sensor #4")

plt.xlabel("Time", labelpad=10, size=20)
plt.ylabel("Acceleration", labelpad=10, size=20)
plt.xticks(size=15)
plt.yticks(size=15)
plt.xlim(0, 400)
plt.legend(loc=1)

# plt.show()

from sklearn.model_selection import train_test_split


X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=0.1)
# X_train = X_data
# Y_train = Y_data
print("X_train.shape :", X_train.shape)

weight1 = np.array([1,1,0,0])
weight2 = np.array([0,0,1,1])


def my_loss(y_true, y_pred):
    divResult = Lambda(lambda x: x[0]/x[1])([(y_pred-y_true),(y_true+0.000001)])
    return K.mean(K.square(divResult))


def my_loss_E1(y_true, y_pred):
    return K.mean(K.square(y_true-y_pred)*weight1)/2e+04

def my_loss_E2(y_true, y_pred):
    divResult = Lambda(lambda x: x[0]/x[1])([(y_pred-y_true),(y_true+0.000001)])
    return K.mean(K.square(divResult)*weight2)

# tr_target = 2 

def set_model(train_target):  # 0:x,y, 1:m, 2:v
    
    activation = 'elu'
    padding = 'valid'
    model = Sequential()
    nf = 32
    fs = (4,1)

    model.add(Conv2D(nf,fs, padding=padding, activation=activation,input_shape=(375,5,1)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 1)))

    model.add(Conv2D(nf*2,fs, padding=padding, activation=activation))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 1)))

    model.add(Conv2D(nf*4,fs, padding=padding, activation=activation))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 1)))

    model.add(Conv2D(nf*8,fs, padding=padding, activation=activation))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 1)))

    model.add(Conv2D(nf*16,fs, padding=padding, activation=activation))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 1)))

    model.add(Conv2D(nf*32,fs, padding=padding, activation=activation))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 1)))

    model.add(Flatten())
    model.add(Dense(512, activation ='elu'))
    model.add(Dense(256, activation ='elu'))
    model.add(Dense(128, activation ='elu'))
    model.add(Dense(64, activation ='elu'))
    model.add(Dense(32, activation ='elu'))
    model.add(Dense(16, activation ='elu'))
    model.add(Dense(8, activation ='elu'))

    model.add(Dense(4))

    optimizer = keras.optimizers.Adam()

    global weight2
    if train_target == 1: # only for M
        weight2 = np.array([0,0,1,0])
    else: # only for V
        weight2 = np.array([0,0,0,1])
       
    if train_target==0:
        model.compile(loss=my_loss_E1,
                  optimizer=optimizer,
                 )
    else:
        model.compile(loss=my_loss_E2,
                  optimizer=optimizer,
                 )
       
    model.summary()

    return model

def train(model,X,Y):
    MODEL_SAVE_FOLDER_PATH = './model/'
    if not os.path.exists(MODEL_SAVE_FOLDER_PATH): # os.path.exists : 폴더나 파일이 실제로 존재하는지 확인
        os.mkdir(MODEL_SAVE_FOLDER_PATH) # os.mkdir : 파일 경로를 생성
                                         # 현재 './model/'이 존재하므로 따로 생성하지 않음
                                         # if not 이 쓰인 이유 : MODEL_SAVE_FOLDER_PATH가 존재하지 않는다면
                                         # 디렉토리를 생성하라는 의미
                                         # 원래는
                                         # if os.path.exists(MODEL_SAVE_FOLDER_PATH) == true :
                                         #     print(1)
                                         # else :
                                         #     os.mkdeir(MODEL_SAVE_FOLDER_PATH)
                                         # 이런 식으로 쓰는 건데 if not을 통해서 코드 길이를 줄일 수 있다

    model_path = MODEL_SAVE_FOLDER_PATH + '{epoch:02d}-{val_loss:.4f}.hdf5'
    best_save = ModelCheckpoint('best_m.hdf5', save_best_only=True, monitor='val_loss', mode='min')


    history = model.fit(X, Y,
                  epochs=256,
                  batch_size=128,
                  shuffle=True,
                  validation_split=0.2,
                  verbose = 2,
                  callbacks=[best_save])

    fig, loss_ax = plt.subplots()
    acc_ax = loss_ax.twinx()

    loss_ax.plot(history.history['loss'], 'y', label='train loss')
    loss_ax.plot(history.history['val_loss'], 'r', label='val loss')
    loss_ax.set_xlabel('epoch')
    loss_ax.set_ylabel('loss')
    loss_ax.legend(loc='upper left')
    # plt.show()    
    
    return model

def plot_error(type_id,pred,true):
    print("pred.shape :", pred.shape)

    if type_id == 0:
        _name = 'x_pos'
    elif type_id == 1:
        _name = 'y_pos'
    elif type_id == 2:
        _name = 'mass'
    elif type_id == 3:
        _name = 'velocity'
    elif type_id == 4:
        _name = "distance"
    else:
        _name = 'error'

    x_coord = np.arange(1,pred.shape[0]+1,1)
    if type_id < 2:
        Err_m = (pred[:,type_id] - true[:,type_id])
    elif type_id < 4:
        Err_m = ((pred[:,type_id] - true[:,type_id])/true[:,type_id])*100
    else:
        Err_m = ((pred[:,0]-true[:,0])**2+(pred[:,1]-true[:,1])**2)**0.5


    fig = plt.figure(figsize=(8,6))
    # plt.rcParams["font.family"]="Times New Roman"
    plt.rcParams["font.size"]=15
    plt.scatter(x_coord, Err_m, marker='o')
    plt.title("%s Prediction for Training Data" % _name, size=20)
    plt.xlabel("Data ID", labelpad=10, size=20)
    plt.ylabel("Prediction Error of %s," % _name, labelpad=10, size=20)
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.ylim(-100., 100.)
    plt.xlim(0, pred.shape[0]+1)

    # plt.show()
    
    print("std :", np.std(Err_m))
    print("max :", np.max(Err_m))
    print("min :", np.min(Err_m))
    return Err_m

#  plot_error(type_id,pred,true):

def load_best_model(train_target):
    
    if train_target == 0:
        model = load_model('best_m.hdf5' , custom_objects={'my_loss_E1': my_loss, })
    else:
        model = load_model('best_m.hdf5' , custom_objects={'my_loss_E2': my_loss, })

    score = model.evaluate(X_data, Y_data, verbose=0)
    print('loss:', score)

    pred = model.predict(X_data)

    i=0

    print('정답(original):', Y_data[i])
    print('예측값(original):', pred[i])

    print("E1 :", E1(pred, Y_data))
    print("E2 :", E2(pred, Y_data))
    # print(E2M(pred, Y_data))
    # print(E2V(pred, Y_data))    
    
    if train_target ==0:
        plot_error(4,pred,Y_data)
    elif train_target ==1:
        plot_error(2,pred,Y_data)
    elif train_target ==2:
        plot_error(3,pred,Y_data)    
    
    return model

submit = pd.read_csv('./data/dacon/comp3/sample_submission.csv')

for train_target in range(3):
    model = set_model(train_target)
    train(model,X_train, Y_train)    
    best_model = load_best_model(train_target)

   
    pred_data_test = best_model.predict(X_data_test)
    
    
    if train_target == 0: # x,y 학습
        submit.iloc[:,1] = pred_data_test[:,0]
        submit.iloc[:,2] = pred_data_test[:,1]

    elif train_target == 1: # m 학습
        submit.iloc[:,3] = pred_data_test[:,2]

    elif train_target == 2: # v 학습
        submit.iloc[:,4] = pred_data_test[:,3]

submit.to_csv('./dacon/comp3/submission/0710/comp3_submit_0710_h4.csv', index = False)


'''
############################best
0709 h3 0.0093500874

    activation = 'elu'
    padding = 'valid'
    model = Sequential()
    nf = 32
    fs = (4,1)


    history = model.fit(X, Y,
                  epochs=256,
                  batch_size=128,
                  shuffle=True,
                  validation_split=0.2,
                  verbose = 2,
                  callbacks=[best_save])

loss: 147982002187.70285
정답(original): [   0.  -400.    50.     0.4]
예측값(original): [ 0.4183446  -2.0463593   1.7223222   0.39347672]
E1 : 6.648964977380819
E2 : 6279.345061730964
pred.shape : (2800, 4)
std : 1.1928388305669935
max : 5.4937094449996895
min : -5.755169689655309
'''

'''
################################ 결과 안 좋음 -> 파일 삭제
comp3_submit_0710_h3
    activation = 'elu'
    padding = 'valid'
    model = Sequential()
    nf = 64
    fs = (3,1)

    history = model.fit(X, Y,
                  epochs=256,
                  batch_size=64,
                  shuffle=True,
                  validation_split=0.2,
                  verbose = 2,
                  callbacks=[best_save])

loss: 502492424215.4057
정답(original): [   0.  -400.    50.     0.4]
예측값(original): [-2.9510462  -5.399749   11.977526    0.40089816]
E1 : 6.6478802832306805
E2 : 170.6961488760792
pred.shape : (2800, 4)
std : 0.5550679719716
max : 5.525135993957514
min : -2.3905992507934624
'''

'''
comp3_submit_0710_h1
    activation = 'elu'
    padding = 'valid'
    model = Sequential()
    nf = 32
    fs = (4,1)

    history = model.fit(X, Y,
                  epochs=256,
                  batch_size=256,
                  shuffle=True,
                  validation_split=0.2,
                  verbose = 2,
                  callbacks=[best_save])
loss: 73212278140.34285
정답(original): [   0.  -400.    50.     0.4]
예측값(original): [ 1.8389965  -0.5837601   3.7048523   0.41317496]
E1 : 6.6499506370683985
E2 : 2459.1919100532714
pred.shape : (2800, 4)
std : 1.4895718940281042
max : 10.707203547159835
min : -9.298837184906002
'''

'''
################################## 0709 best보다 loss 더 적음
comp3_submit_0710_h2

    activation = 'elu'
    padding = 'valid'
    model = Sequential()
    nf = 64
    fs = (4,1)

    history = model.fit(X, Y,
                  epochs=256,
                  batch_size=256,
                  shuffle=True,
                  validation_split=0.2,
                  verbose = 2,
                  callbacks=[best_save])
loss: 110167615300.75429
정답(original): [   0.  -400.    50.     0.4]
예측값(original): [0.4166762  1.6320833  0.44063112 0.44385457]
E1 : 6.649905500936173
E2 : 52046.93152038633
pred.shape : (2800, 4)
std : 1.7525080540227167
max : 10.963642597198481
min : -13.015594085057575
'''

'''
loss 가장 작음

comp3_submit_0710_h3

    activation = 'elu'
    padding = 'valid'
    model = Sequential()
    nf = 32
    fs = (4,1)

    model.add(Dense(512, activation ='elu')) # 레이어 하나 추가
    model.add(Dense(256, activation ='elu'))
    model.add(Dense(128, activation ='elu'))
    model.add(Dense(64, activation ='elu'))
    model.add(Dense(32, activation ='elu'))
    model.add(Dense(16, activation ='elu'))
    model.add(Dense(8, activation ='elu'))

    history = model.fit(X, Y,
                  epochs=256,
                  batch_size=256,
                  shuffle=True,
                  validation_split=0.2,
                  verbose = 2,
                  callbacks=[best_save])

loss: 38956310252.98286
정답(original): [   0.  -400.    50.     0.4]
예측값(original): [ 0.8791442  -0.7561214   1.86538     0.39604646]
E1 : 6.649407347747609
E2 : 341045852.3460761
pred.shape : (2800, 4)
std : 0.6918071030185572
max : 5.2296161651611275
min : -7.384306192398071
'''

'''
comp3_submit_0710_h4
    
    activation = 'elu'
    padding = 'valid'
    model = Sequential()
    nf = 32
    fs = (4,1)

    model.add(Flatten())
    model.add(Dense(512, activation ='elu'))
    model.add(Dense(256, activation ='elu'))
    model.add(Dense(128, activation ='elu'))
    model.add(Dense(64, activation ='elu'))
    model.add(Dense(32, activation ='elu'))
    model.add(Dense(16, activation ='elu'))
    model.add(Dense(8, activation ='elu'))

        history = model.fit(X, Y,
                  epochs=256,
                  batch_size=128,
                  shuffle=True,
                  validation_split=0.2,
                  verbose = 2,
                  callbacks=[best_save])
'''

# h1 loss: 73212278140.34285
# h2 loss: 110167615300.75429
# h3 loss: 38956310252.98286 -> best
# h4 loss: 709736116668.7086

# h1 loss: 147982002187.70285