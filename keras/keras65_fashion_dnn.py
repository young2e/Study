# 과제 2
# Sequential형으로 작성하시오
import numpy as np
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import np_utils
from keras.callbacks import EarlyStopping

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

print("x_train[0] : ", x_train[0])
print("y_train[0] : ", y_train[0])

print("x_train.shape : ", x_train.shape)   # (60000, 28, 28)
print("x_test.shape : ", x_test.shape)     # (10000, 28, 28)
print("y_train.shape : ", y_train.shape)   # (60000,)
print("y_test.shape : ", y_test.shape)     # (10000,)

# 데이터 전처리
# one hot encoding
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
print(y_train.shape)

# 정규화

x_train = x_train.reshape(60000, 28*28).astype('float32') / 255.0
x_test = x_test.reshape(10000, 28*28).astype('float32') / 255.0

# 2. 모델 구성

model = Sequential()
model.add(Dense(111, input_shape = (28*28, )))
model.add(Dropout(0.3))          
model.add(Dense(133, activation = 'relu'))
model.add(Dropout(0.3)) 
model.add(Dense(155, activation = 'relu'))
model.add(Dropout(0.4))     
model.add(Dense(77, activation = 'relu'))
model.add(Dropout(0.2)) 
model.add(Dense(10, activation = 'softmax'))

model.summary()

# 3. 컴파일, 훈련
# from keras.callbacks import EarlyStopping
# early_stopping = EarlyStopping(monitor = 'loss', patience = 10, mode = 'max')

model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['acc'])
model.fit(x_train, y_train, epochs = 70, batch_size = 100, validation_split = 0.3, verbose = 1)

# 4. 평가, 예측
loss, acc = model.evaluate(x_train, y_train, batch_size = 100)

print('loss : ', loss)
print('acc : ', acc)

y_pred = model.predict(x_test)

# print(y_pred)
print(np.argmax(y_pred, axis = 1))
# print(y_pred.shape)

'''
model.add(Dense(111, input_shape = (28*28, )))
model.add(Dropout(0.3))          
model.add(Dense(133, activation = 'relu'))
model.add(Dropout(0.3)) 
model.add(Dense(155, activation = 'relu'))
model.add(Dropout(0.4))     
model.add(Dense(77, activation = 'relu'))
model.add(Dropout(0.2)) 
model.add(Dense(10, activation = 'softmax'))
epochs = 70, batch_size = 100
acc :  0.9035666584968567
'''