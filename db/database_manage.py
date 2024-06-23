import sqlite3

from classes.champion import Champion
from classes.comp import Comp


def load_data_from_db(dp_path="tft_helper.db"):
    with sqlite3.connect(dp_path) as conn:
        curr = conn.cursor()

        # 챔피언 데이터 불러오기
        champions = curr.execute("select * from champion").fetchall()
        champion_list = [
            Champion(
                champion[1], champion[2], 2, [champion[3], champion[4], champion[5]]
            )
            for champion in champions
        ]
        champion_dict = {
            champion[1]: Champion(
                champion[1], champion[2], 2, [champion[3], champion[4], champion[5]]
            )
            for champion in champions
        }

        # comp 데이터 불러오기
        comp_list = []
        comps = curr.execute("select * from comp").fetchall()
        for comp in comps:
            comp_id = comp[0]
            comp_name = comp[1]
            champions = curr.execute(
                f"""
                select ch.name 
                from champion as ch 
                inner join comp_champion as co 
                on ch.id = co.champion_id
                where co.comp_id = {comp_id}"""
            ).fetchall()
            comp_list.append(Comp(comp_name, [champion[0] for champion in champions]))

    return champion_list, champion_dict, comp_list


def update_champion_value(champion_name: str, value_list: list) -> None:
    with sqlite3.connect("tft_helper.db") as conn:
        curr = conn.cursor()
        curr.execute(
            """
            update champion
            set value1 = ?, value2 = ?, value3 = ?
            where name = ?
        """,
            (value_list[0], value_list[1], value_list[2], champion_name),
        )


def delete_comp(comp_name) -> None:
    with sqlite3.connect("tft_helper.db") as conn:
        curr = conn.cursor()
        curr.execute(
            """
            delete from comp
            where name = ?
        """,
            (comp_name),
        )
