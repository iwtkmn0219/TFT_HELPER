from classes.champion import Champion
from classes.comp import Comp


# comp 추천
def recommend_comps(selected_champions: list, comp_list: list) -> list:
    recommend_comps = [
        comp
        for comp in comp_list
        if all(champion in comp.champions for champion in selected_champions)
    ]
    # 모든 comp 로드
    # comp 별 가치평가
    # 가치 기준 정렬
    return recommend_comps
