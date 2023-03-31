import numpy as np

def get_score(_base_value, _coin_count, _coin_value, _front_probability = 0.5):
    #print("get_score(", _base_value, _coin_count, _coin_value, _front_probability,")")
    base_value =_base_value
    coin_count = _coin_count
    coin_value = _coin_value
    front_probability = _front_probability
    
    result_score = base_value

    for i in range(coin_count):
        toss = float(np.random.uniform(0,1))
        if toss < front_probability:
            result_score += coin_value
            #앞면이 한 번 뜰 때마다 기본값에서 코인 가중치를 더해주는 방식
        else:
            pass

    return result_score

  #기본 합을 위해 필요한 코인토스 결과 리턴 함수

def Clash(skill_inform1, skill_inform2):
    #print("Clash (", skill_inform1, skill_inform2, ")")
    base1, coin_quantity1, coin_score1, probability_1 = skill_inform1
    base2, coin_quantity2, coin_score2, probability_2 = skill_inform2

    coin_quantity_temp1 = coin_quantity1
    coin_quantity_temp2 = coin_quantity2

    while coin_quantity_temp1 > 0 and coin_quantity_temp2 > 0:
        result_score1 = get_score(base1, coin_quantity_temp1, coin_score1, probability_1)
        result_score2 = get_score(base2, coin_quantity_temp2, coin_score2, probability_2)

        if result_score1 > result_score2:
            coin_quantity_temp2 -= 1

        elif result_score2 > result_score1:
            coin_quantity_temp1 -= 1

    if coin_quantity_temp1 > 0:
        return "skill 1 win"

    elif coin_quantity_temp1 == 0 and coin_quantity_temp2 == 0:
        return "error : both side skill coins are not remain."

    else:
        return "skill 2 win"

"""
    get_mean_probability

    param = _skill1 : 1번 스킬의 정보
            _skill2 : 2번 스킬의 정보
              스킬의 양식은 [스킬 위력, 스킬 코인 갯수, 코인 위력, 정신력] 으로 통일.

            _clash_repeat : 합 진행 횟수

    결과 : _clash_repeat 번 만큼 합을 진행한 결과를 토대로 skill1이 이길 확률을 반환함.
    
"""

def get_mean_probability(_skill1, _skill2, _clash_repeat):
    skill1 = _skill1
    skill2 = _skill2
    clash_repeat = _clash_repeat
    won_cnt = 0
    
    for i in range(clash_repeat):
        result = Clash(skill1, skill2)
        if result == "skill 1 win":
            won_cnt += 1
    
    return won_cnt / clash_repeat

"""
  get_skill_prob_list
  param = _skill1 = 1번 스킬의 정보 
          _skill2 = 2번 스킬의 정보
          _clash_repeat = 합 진행 횟수
          _mentality_gap_rev = 1 / 정신력 값의 변화량 (정신력 값의 구간 수)

  결과 :
  'x': 1차원 배열, 0부터 1까지 _mentality_gap_rev 만큼의 구간 값을 가짐.
  'y': 1차원 배열, 0부터 1까지 _mentality_gap_rev 만큼의 구간 값을 가짐.
  'z': 2차원 배열, x[_x], y[_y]는 z[_x][_y]와 대응됨

  으로 구성된 dictionary를 반환.
"""


def get_skill_prob_list(_skill1, _skill2, _clash_repeat=100, _mentality_gap_rev = 1000):
    #print("get_skill_prob_list(",_skill1, _skill2, _clash_repeat, _mentality_gap_rev, ")")
    base_value1, coin_count1, coin_value1 = _skill1
    base_value2, coin_count2, coin_value2 = _skill2
    clash_repeat = _clash_repeat
    mentality_gap_rev = _mentality_gap_rev
    
    x = np.linspace(0, 1, mentality_gap_rev+2)
    y = np.linspace(0, 1, mentality_gap_rev+2)
    x = np.delete(x, (0, mentality_gap_rev+1))
    y = np.delete(y, (0, mentality_gap_rev+1))
    #두 스킬의 구성이 완전히 같을 때 코인이 무조건 앞면이거나 뒷면이면 합을 무한히 진행해 무한 루프에 갇힘.

    z = list()
    cnt = 0
    
    for i in range(mentality_gap_rev):
        z.append(list())
        for q in range(mentality_gap_rev):
            skill1 = [base_value1, coin_count1, coin_value1, x[i]]
            skill2 = [base_value2, coin_count2, coin_value2, y[q]]
            z[-1].append(get_mean_probability(skill1, skill2, clash_repeat))
            cnt+=1

    # x,y에 해당하는 확률을 z에 넣어줌. (clash_repeat만큼 반복했을때 얻어지는 확률)
    
    return_dict = dict()
    return_dict['x'] = x
    return_dict['y'] = y
    return_dict['z'] = z
    
    return return_dict