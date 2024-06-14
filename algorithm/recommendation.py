import pickle
from classes.champion import Champion
from classes.comp import Comp

champion_dict = {}
comp_list = []
selected_champion_dict = {}
# 데이터 불러오기
with open("champion_list.pkl", "rb") as file:
    champion_list = pickle.load(file)
    champion_dict = {champion.name: champion for champion in champion_list}
with open("comp_list.pkl", "rb") as file:
    comp_list = pickle.load(file)


# comp 추천
def recommend_comps(selected_champions: list) -> list:
    selected_champion_dict.clear()
    for champion in selected_champions:
        selected_champion_dict[champion.name] = champion
    # comp 별 가치가 평가된 리스트 생성
    comp_value_list = []
    for comp in comp_list:
        # 각 comp 별 가치를 계산한 후 comp_value_list에 추가
        comp_score = calculate_comp_score(comp)
        if comp_score == 0:
            continue
        comp_value_list.append([comp_score, comp])
    # 가치 기준 정렬
    comp_value_list.sort(key=lambda x: x[0], reverse=True)
    recommend_comps = [ls for ls in comp_value_list]
    return recommend_comps


# comp 의 가치를 계산하는 함수
def calculate_comp_score(comp: Comp) -> int:
    comp_score = 0
    for champion_name in comp.champions:
        if champion_name in selected_champion_dict:
            comp_score += piece_value(champion_dict[champion_name])
    return comp_score


# 기물의 가치를 반환하는 함수
def piece_value(champion: Champion) -> int:
    value = 0
    cost = champion.cost
    star = champion.star
    if cost == 1:
        if star == 1:
            value += 1
        elif star == 2:
            value += 4
        elif star == 3:
            value += 9
    elif cost == 2:
        if star == 1:
            value += 1
        elif star == 2:
            value += 5
        elif star == 3:
            value += 17
    elif cost == 3:
        if star == 1:
            value += 3
        elif star == 2:
            value += 8
        elif star == 3:
            value += 26
    return value
