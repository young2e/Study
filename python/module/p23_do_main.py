# do 파일은 임포트한 거 실행시키는 파일로 설정한다(이름 이유)

import p21_car
import p22_tv



print("======================")

p21_car.drive()
p22_tv.watch()

'''
======================
운전하다
시청하다
'''

# import된 파일들이 실행 되지 않음
# p21에서 조건을 달아놨기 때문에
# 각 import된 파일들의 name이 현재 main이 아니기 때문에 
# 함수가 실행되지 않는다