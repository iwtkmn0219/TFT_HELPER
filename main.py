from classes.champion import Champion
from classes.comp import Comp
from style.style import font
import pickle
import os

champion_cost = {}
champion_importance = {}
possible_list = []
pocket = {}


# 프롬프트를 지우는 함수
def clear_screen() -> None:
    # Windows 시스템인지 확인하고 'cls' 명령 사용
    if os.name == "nt":
        os.system("cls")
    # Unix/Linux 및 macOS 시스템에서는 'clear' 명령 사용
    else:
        os.system("clear")


# 정수 판별 함수
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# 챔피언을 포켓에 추가하는 함수
def add_champion(name: str) -> None:
    flag = True
    while flag:
        # 파일에서 챔피언 정보를 불러와 리스트에 추가한다.
        with open("champion_list.pkl", "rb") as file:
            champion_list = pickle.load(file)
            for champion in champion_list:
                if champion.name == name:
                    pocket[name] = champion
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
def edit_champion(name: str) -> None:
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


# 현재 포켓을 보여주는 함수
def show_pocket() -> None:
    # show my pocket
    for k, _ in pocket.items():
        if champion_cost[k] == 1:
            ui = k
        elif champion_cost[k] == 2:
            ui = font(k, "green")
        elif champion_cost[k] == 3:
            ui = font(k, "blue")
        print(f"{ui}{'★' * pocket[k].star}", end=" ")
    print()


# 기물의 가치를 계산하는 함수
def tft_value(champion: Champion) -> int:
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


# 현재 포켓의 가치를 계산하는 함수
def calculate_possibillity_score(comp: list) -> int:
    possible_score = 0
    for champion in comp.champions:
        if champion in pocket:
            possible_score += tft_value(pocket[champion])
    return possible_score


def update_possibillity() -> None:
    # 리스트 비우기
    possible_list.clear()
    # comp 읽어오기
    with open("comp_list.pkl", "rb") as file:
        comp_list = pickle.load(file)
        for comp in comp_list:
            possible_score = calculate_possibillity_score(comp)
            possible_list.append([possible_score, comp])
    # 가치기준 정렬
    possible_list.sort(key=lambda x: x[0], reverse=True)
    pass


# 빌드업에 사용할 수 있는 가능성들을 보여주는 함수
def show_possibillity() -> None:
    # 출력부
    prev_score = 0
    for i, pos in enumerate(possible_list):
        score, comp = pos
        if score == 0:
            continue
        if score != prev_score:
            score_heart = font("♥" * score, "red")
            print(f"{score_heart} {"=" * (79-score)}")
        print(f"{comp.name:<14}\t:", end=" ")
        for champion in comp.champions:
            if champion_cost[champion] == 1:
                ui = champion
            elif champion_cost[champion] == 2:
                ui = font(champion, "green")
            elif champion_cost[champion] == 3:
                ui = font(champion, "blue")
            print(f"{ui}", end=" ")
        print()
        prev_score = score
    print("=" * 80)


def update_importance() -> None:
    champion_importance.clear()
    for champion in champion_cost:
        champion_importance[champion] = 0
    # 각 챔피언의 필요도 체크 (필요도: 얼마나 많은 comp에 기용될 수 있는가)
    for score, comp in possible_list:
        if score > 0:
            for champion in comp.champions:
                if champion in champion_importance:
                    champion_importance[champion] += 1


def show_less_important_champions(star: int) -> None:
    for k, v in champion_importance.items():
        if v == 0 and champion_cost[k] == star:
            if star == 1:
                print(k, end=" ")
            if star == 2:
                print(font(k, "green"), end=" ")
            if star == 3:
                print(font(k, "blue"), end=" ")
    print()


def show_importance() -> None:
    ls = list(champion_importance.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    # print(ls)
    prev_importance = 0
    for champion, importance in ls:
        if importance != prev_importance:
            prev_importance = importance
            print(f'\n{importance}:', end=' ')
        print(f"{champion}", end=' ')
    print()


def display() -> None:
    show_pocket()
    update_possibillity()
    show_possibillity()
    update_importance()
    # show_less_important_champions(1)
    show_importance()


if __name__ == "__main__":
    clear_screen()
    print("WELCOME!")

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
                    clear_screen()
                    print("POCKET CLEAR")
                    pocket = {}
            # str인 경우
            else:
                champion = line
                # 올바른 이름인 경우
                if champion in champion_cost:
                    # 이미 포켓에 있는 경우
                    if champion in pocket:
                        edit_champion(champion)
                    # 새로운 기물일 경우
                    else:
                        add_champion(champion)
                clear_screen()
        except Exception as e:
            print(f">> {e}")
        display()
