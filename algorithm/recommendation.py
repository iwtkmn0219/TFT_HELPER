import pickle
from db.database_manage import load_data_from_db
from classes.champion import Champion
from classes.comp import Comp

champion_dict = {}
comp_list = []
selected_champion_dict = {}
# 데이터 불러오기
champion_list, champion_dict, comp_list = load_data_from_db()


# comp 추천
def recommend_comps(selected_champions: list) -> list:
    _, _, comp_list = load_data_from_db()
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
            comp_score += piece_value(selected_champion_dict[champion_name])
    return comp_score


# 기물의 가치를 반환하는 함수
def piece_value(champion: Champion) -> int:
    value = 0
    cost = champion.cost
    star = champion.star
    if star == 1:
        return champion.value[0]
    elif star == 2:
        return champion.value[1]
    elif star == 3:
        return champion.value[2]
    return value
