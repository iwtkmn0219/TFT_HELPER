from classes.champion import Champion
from classes.comp import Comp
import pickle


def get_champion_info(ls: list, name: str) -> Champion:
    pass


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


def show_possibillity(ls: list) -> None:
    possible_list = []
    with open("comp_list.pkl", "rb") as file:
        comp_list = pickle.load(file)
        for comp in comp_list:
            possible_score = 0
            for champion in comp.champions:
                for curr in ls:
                    curr_champ = curr.name
                    if champion == curr_champ:
                        if curr.cost == 1:
                            possible_score += 3
                        elif curr.cost == 2:
                            if curr.star == 1:
                                possible_score += 2
                            elif curr.star == 2:
                                possible_score += 5
                        elif curr.cost == 3:
                            possible_score += 3
                        break
            possible_list.append([possible_score, comp])

    possible_list.sort(key=lambda x: x[0], reverse=True)
    for i, pos in enumerate(possible_list):
        if i > 5:
            break
        score, comp = pos
        if score == 0:
            continue
        print(pos)


if __name__ == "__main__":
    print("WELCOME!")
    curr_list = []
    while True:
        mode = input("MODE(0: EXIT, 1: ADD, 2: DEL, 3: EDIT): ")
        if mode == "0":
            break
        elif mode == "1":
            add_champion(curr_list)
        elif mode == "2":
            del_champion(curr_list)
        elif mode == "3":
            edit_champion(curr_list)

        show_pocket(curr_list)
        show_possibillity(curr_list)
