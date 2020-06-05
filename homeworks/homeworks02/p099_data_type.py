# 4.3 자료형
# 4.3.1 자료형의 종류
# 파이썬의 값은 형(자료형, data type)이라는 개념이 있다
# 자료형은 문자열형(str형), 정수형(int형), 부동소수점형(float형), 리스트형(list형) 등이 있다

# 다른 형끼리의 계산이나 연결을 시도하면 에러가 발생하는 경우가 있다

# height = 177
# print("신장은 " + height + "cm입니다.")
# TypeError: can only concatenate str (not "int") to str

# 이 오류의 해결 방법은 다음 절에서 확인하자 
# 우선은 변수의 자료형을 조사하는 방법을 알아보자
# 변수의 자료형을 알고 싶을 때는 type()을 사용한다
# () 안에 궁금한 자료형의 값을 넣으면 된다

height = 177
print(type(height)) # <class 'int'>

# type()의 () 안에는 하나의 변수만 넣을 수 있으니 주의!

h = 1.7
w = 60

print(type(h)) # <class 'float'>
print(type(w)) # <class 'int'>

bmi = w/h**2
print(bmi) # 20.761245674740486
print(type(bmi)) # <class 'float'>

# 4.3.2 자료형의 변환
# 4.3.1절에서 '자료형의 종류'에서 배운 대로 자료형에는 다양한 형이 존재한다
# 서로 다른 자료형을 계산하거나 결합하려면 형을 변환하여 같은 형으로 만들어야 한다

# 정수형으로 변환하려면 int()를, 소수점을 포함한 수치형으로 변환하려면 float()을, 
# 문자열로 변환하려면 str()을 사용한다
# 소수점을 포함한 수치형을 부동소수점형(float형)이라고 한다

# 부동소수점의 '부동'은 부호, 지수, 가수로 소수점을 나타내는 컴퓨터 특유의 표시 방법이다
# 프로그래밍 실무에서 소수점을 포함하는 숫자는 대부분 float형이다

# 4.3.1절 '자료형의 종류'에서 오류가 발생한 코드를 수정
h = 177
print("신장은 " + str(h) + "cm입니다.") # 신장은 177cm입니다.

# 부동소수점형과 정수형은 엄밀하게 다른 형이지만 둘 다 수치를 취급하는 형이다
# 그러므로 형 변환을 하지 않아도 부동소수점형과 정수형을 혼합한 계산이 가능하다

a = 35.4
b = 10
print(a + b) # 45.4

h = 1.7
w = 60
bmi = w / h**2

print("당신의 bmi는 " + str(bmi) + "입니다.")
# 당신의 bmi는 20.761245674740486입니다.

# 4.3.3 자료형의 이해와 확인
# 프로그래밍에서 자료형은 매우 중요하다
# 정리하자면, 결국 다른 자료형끼리는 결합할 수 없으며, 문자열로 저장된 수치는 계산할 수 없다는 것이다
# 또한 문자열에 수치를 곱하면 문자열이 여러 개 나란히 출력된다

greeting = "hi!"
print(greeting * 2) # hi!hi!

n = "10"
print(n * 3) # 101010
print(type(n * 3)) # <class 'str'>

4
