from classes.champion import Champion
from classes.comp import Comp
from style.style import font
import pickle

champion_cost = {}


# 정수 판별 함수
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# 챔피언을 포켓에 추가하는 함수
def add_champion(dic: dict, name: str) -> None:
    flag = True
    while flag:
        # 파일에서 챔피언 정보를 불러와 리스트에 추가한다.
        with open("champion_list.pkl", "rb") as file:
            champion_list = pickle.load(file)
            for champion in champion_list:
                if champion.name == name:
                    dic[name] = champion
                    flag = False
                    break


# 챔피언을 포켓에서 제거하는 함수
def del_champion(ls: list) -> None:
    while True:
        try:
            index = int(input("INPUT INDEX(-1: CANCEL): "))
            # 입력 취소
            if index < 0:
                return
            ls.pop(index)
            break
        except ValueError:
            print(">> Please input 'int'")
        except IndexError:
            print(">> WRONG INDEX")
        except Exception as e:
            print(f">> {e}")


# 포켓의 챔피언을 수정하는 함수
def edit_champion(pocket: dict, name: str) -> None:
    order = int(input("OPTION(-1: DOWNGRADE, 0: DELETE, 1: UPGRADE): "))
    # 다운그레이드
    if order == -1:
        pocket[name].star = max(pocket[name].star - 1, 1)
    # 삭제
    elif order == 0:
        pocket.pop(name)
    # 업그레이드
    elif order == 1:
        pocket[name].star = min(pocket[name].star + 1, 3)


def show_pocket(ls: list) -> None:
    # show my pocket
    for i, champion in enumerate(ls):
        print(f"[{i} {champion}]", end="")
    print()


def tft_value(champion: Champion) -> int:
    value = 0
    cost = champion.cost
    star = champion.star
    if cost == 1:
        if star == 1:
            value += 1
        elif star == 2:
            value += 3
        elif star == 3:
            value += 9
    elif cost == 2:
        if star == 1:
            value += 2
        if star == 2:
            value += 5
    elif cost == 3:
        if star == 1:
            value += 4
        elif star == 2:
            value += 8
    return value


def calculate_possibillity_score(pocket: dict, comp: list) -> int:
    possible_score = 0
    for champion in comp.champions:
        if champion in pocket:
            possible_score += tft_value(pocket[champion])
    return possible_score


def show_possibillity(dic: dict) -> None:
    possible_list = []
    with open("comp_list.pkl", "rb") as file:
        comp_list = pickle.load(file)
        for comp in comp_list:
            possible_score = calculate_possibillity_score(dic, comp)
            possible_list.append([possible_score, comp])

    possible_list.sort(key=lambda x: x[0], reverse=True)
    prev_score = 0
    for i, pos in enumerate(possible_list):
        if i > 5:
            break
        score, comp = pos
        if score == 0:
            continue
        if score != prev_score:
            score_heart = font("♥" * score, "red")
            print(f"{score_heart} {"=" * (79-score)}")
        print(f"{comp.name:<14}\t:", end=" ")
        for champion in comp.champions:
            if champion_cost[champion] == 1:
                print(f"{champion}", end=" ")
            elif champion_cost[champion] == 2:
                ui = font(champion, "green")
                print(f"{ui}", end=" ")
            elif champion_cost[champion] == 3:
                ui = font(champion, "blue")
                print(f"{ui}", end=" ")
        print()
        prev_score = score
    print("=" * 80)


if __name__ == "__main__":
    print("WELCOME!")
    pocket = {}

    with open("champion_list.pkl", "rb") as file:
        champion_list = pickle.load(file)
        for champion in champion_list:
            champion_cost[champion.name] = champion.cost

    while True:
        try:
            line = input("INPUT CHAMPION'S NAME(-1: EXIT, 0: CLEAR): ")
            input_type = type(line)
            # int인 경우
            if is_integer(line):
                order = int(line)
                # 종료 코드
                if order == -1:
                    print("EXIT")
                    break
                # 포켓 비우기
                if order == 0:
                    print("POCKET CLEAR")
                    pocket = {}
            # str인 경우
            else:
                champion = line
                # 잘못된 이름인 경우
                if champion not in champion_cost:
                    print("WRONG INPUT")
                    continue
                # 이미 포켓에 있는 경우
                if champion in pocket:
                    edit_champion(pocket, champion)
                # 새로운 기물일 경우
                else:
                    add_champion(pocket, champion)
        except Exception as e:
            print(f">> {e}")

        show_pocket(pocket)
        show_possibillity(pocket)
