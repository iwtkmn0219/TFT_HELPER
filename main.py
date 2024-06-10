from classes.champion import Champion
from classes.comp import Comp
from style.style import font
import pickle

champion_cost = {}


def add_champion(ls: list) -> None:
    flag = True
    while flag:
        name = input("NAME(0: CANCEL): ")
        if name == "0":
            break
        for champion in ls:
            if champion.name == name:
                print(">> OVERLAP")
                return

        # 파일에서 챔피언 정보를 불러와 리스트에 추가한다.
        with open("champion_list.pkl", "rb") as file:
            champion_list = pickle.load(file)
            for champion in champion_list:
                if champion.name == name:
                    ls.append(champion)
                    flag = False
                    break
        # 잘못된 이름인경우 경고 메시지를 출력한다.
        if flag:
            print(">> WRONG NAME")


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


def edit_champion(ls: list) -> None:
    while True:
        try:
            i, star = map(int, input("INDEX, STAR(0 0: CANCEL): ").split())
            if i == 0 and star == 0:
                return
            if star <= 3:
                break
            print(">> STAR MUST BE LESS THAN 4")
        except ValueError:
            print(">> Please input int, int")
        except IndexError:
            print(">> WROND INDEX")
        except Exception as e:
            print(f">> {e}")
    ls[i].star = star


def show_pocket(ls: list) -> None:
    # show my pocket
    for i, champion in enumerate(curr_list):
        print(f"[{i} {champion}]", end="")
    print()


def tft_value(champion: Champion) -> int:
    value = 0
    cost = champion.cost
    star = champion.star
    if cost == 1:
        value += 3
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


def calculate_possibillity_score(pocket: list, comp: list) -> int:
    possible_score = 0
    for champion in comp.champions:
        for live_champ in pocket:
            if champion == live_champ.name:
                possible_score += tft_value(live_champ)
                break
    return possible_score


def show_possibillity(ls: list) -> None:
    possible_list = []
    with open("comp_list.pkl", "rb") as file:
        comp_list = pickle.load(file)
        for comp in comp_list:
            possible_score = calculate_possibillity_score(ls, comp)
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
    curr_list = []

    with open("champion_list.pkl", "rb") as file:
        champion_list = pickle.load(file)
        for champion in champion_list:
            champion_cost[champion.name] = champion.cost

    while True:
        mode = input("MODE(0: EXIT, 1: ADD, 2: DEL, 3: EDIT, 4: CLEAR): ")
        if mode == "0":
            break
        elif mode == "1":
            add_champion(curr_list)
        elif mode == "2":
            del_champion(curr_list)
        elif mode == "3":
            edit_champion(curr_list)
        elif mode == "4":
            curr_list = []

        show_pocket(curr_list)
        show_possibillity(curr_list)
