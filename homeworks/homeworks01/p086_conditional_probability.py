# 6장 확률

# 확률 및 관련된 수학적 지식을 어느 정도 갖추지 않고 데이터 과학을 하는 것은 매우 어렵다고 한다,,
# 확률, 기초적인 내용 다룬다

# 확률 , probability 란 어떠한 사건의 공간에서 특정 사건이 선태될 때 발생하는 
# 불확실성을 수치적으로 나타내는 것

# 주사위 던지기를 생각해보자
# 사건의 공간은 주사위를 던졌을 때 나올 수 있는 모든 결과로 이루어져 있다
# 이 공간의 부분 집합을 하나의 사건으로 보면 된다
# 예를 들어 주사위를 던져서 1이 나오는 경우 or 주사위를 던져서 짝수가 나오는 경우
# 이런 것들을 하나의 사건으로 볼 수 있다

# 위와 같은 사건 E에 대한 확률을 P(E)라고 표시하자
# 다양한 모델을 만드는 데 확률이 사용될 예정이고 모델의 성능을 평가할 때도 확률을 사용할 것이다
# 한마디로 확률을 온갖 목적으로 사용한다

# 6.1 종속성과 독립성
# 대략적으로 사건 E 발생 여부가 사건 F의 발생 여부에 대한 정보(혹은 그 반대로)를 제공한다면

# 두 사건 E와 F는 종속 사건(dependent events)으로 볼 수 있다
# 그렇지 않다면 두 사건은 독립 사건(independent events)이다

# 예를 들어 동전을 2번 던졌을 때 첫 번째 동전에서 앞면이 나왔더라도
# 두 번째 동전에서 마찬가지로 앞면이 나올지는 아무도 알 수 없다
# 이 두 사건은 독립사건이다
# 하지만, 첫 번째 동전에서 앞면이 나왔다면 두 동전에서 모두 뒷면이 나오는 경우의 발생 여부에 대해서는 알 수 있다
# 첫 번째 동전에서 앞면이 나와버렸으니까 두 동전에서 모두 뒷면이 나올 경우는 사라지기 때문
# 그렇다면 두 사건은 종속사건이다
# 수학적으로, 사건 E와 F가 동시에 발생할 확률이 각각 사건이 발생할 확률의 곱과 같다면 두 사건은 독립 사건을 의미한다

# P(E,F) = P(E)P(F)

# 동전 던지기 예시를 다시 살펴보면 첫 번째 동전에서 앞면이 나올 확률은 1/2이고
# 두 동전이 모두 뒷면일 확률은 1/4이다 
# 하지만! 첫 번째 동전이 앞면이고 두 동전이 뒷면일 확률은 0이기 때문에 두 사건은 종속사건이다

# 6.2 조건부 확률
# 만약 두 사건이 독립 사건이라면 정의에 따라서 다음과 같은 식을 얻을 수 있다

# P(E,F) = P(E)P(F)

# 또, 두 사건이 반드시 독립 사건이라는 보장이 없고 사건 F의 확률이 0이 아닌 경우
# 사건 E가 발생할 조건부 확률(conditional probability)을 다음과 같이 정의할 수 있다

# P(E|F) = P(E,F)/P(F)

# 즉 조건부 확률이란 사건 F가 발생했을 경우, 사건 E가 발생할 확률이라고 이해할 수 있다

# 위의 식은 다음과도 같다

# P(E,F) = P(E|F)P(E)

# 따라서 사건 E와 F가 독립 사건이라면 다음과 같은 식이 성립함을 알 수 있다

# P(E|F) = P(E

# 위의 식은 사건 F가 발생해도 사건 E의 발생 여부에 관한 추가적인 정보를 알 수 없다는 것을 수학적으로 표현한 식이다

# 이해하기 쉽게 하나의 예를 더 들어보자
# 한 가족 안의 두 아이의 성별을 맞추는 예시이다
# 두 조건을 가정한다
# 1) 각 아이가 딸이거나 아들일 확률은 동일하다
# 2) 둘째의 성별은 첫째의 성별과 독립이다

# 그렇다면 '두 아이가 모두 딸이 아닌 경우'는 1/4의 확률로 발생하며 
# '딸 한명과 아들 한 명인 경우'는 1/2의 확률
# '두 아이가 모두 딸인 경우'는 1/4의 확률로 발생한다

# 그렇다면 첫째가 딸인 경우(사건G), 두 아이가 모두 딸일 사건(B) 확률은 어떻게 될까

# P(B|G) = P(B,G)/P(G) = P(B)/P(G) = 1/2

# 사건 B와 G가 동시에 일어나는 확률(즉, 두 아이가 모두 딸이고 첫째가 딸일 확률)은
# 사건 B가 발생할 확률과 동일하기 때문이다(만약 두 아이가 모두 딸이라면 당연히 첫째는 딸)

# 딸이 최소 한 명인 경우(사건L), 두 아이가 모두 딸일 확률 또한 계산해 볼 수 있다
# 하지만 신기하게 이전과 다른 값이 계산된다
# 사건 B와 L이 동시에 발생할 확률(즉, 두 아이가 모두 딸이고 적어도 하나는 딸인 경우)은
# 사건 B가 발생할 확률과 동일하다, 다음과 같이 계산된다

# P(B|L) = P(B,L)/P(L) = P(B)/P(L) = 1/3

# 어떻게? 
# 만약 딸이 최소 한 명이라면 딸 한명과 아들 한 명일 확률이 두 명이 모두 딸일 확률보다 두 배나 높다
# 수많은 가족들을 '만들어서' 결과를 검증해 볼 수 있다

import enum, random

# Enum을 사용하면 각 항목에 특정 값을 부여할 수 있으며
# 파이썬 코드를 더욱 깔끔하게 만들어준다
class Kid(enum.Enum):
    BOY = 0
    GIRL = 1

def random_kid():
    return random.choice([Kid.BOY, Kid.GIRL])

both_girls = 0
older_girl = 0
either_girl = 0

random.seed(0)

for _ in range(10000) :
    younger = random_kid()
    older = random_kid()
    if older == Kid.GIRL:
        older_girl += 1
    if older == Kid.GIRL and younger == Kid.GIRL:
        both_girls += 1
    if older == Kid.GIRL or younger == Kid.GIRL:
        either_girl += 1

print("P(both | older):", both_girls / older_girl)
print("P(both | either):", both_girls / either_girl)

# P(both | older): 0.5007089325501317
# P(both | either): 0.3311897106109325