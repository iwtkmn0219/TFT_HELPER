import sqlite3
import pickle
import os

# from classes.comp import Comp
# from classes.champion import Champion

# 데이터베이스 연결 및 테이블 생성
conn = sqlite3.connect("tft_helper.db")
cursor = conn.cursor()

# 테이블 생성
cursor.executescript(
    """
CREATE TABLE IF NOT EXISTS champion (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cost INTEGER NOT NULL,
    value1 INTEGER,
    value2 INTEGER,
    value3 INTEGER
);

CREATE TABLE IF NOT EXISTS comp (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS trait (
    id INTEGER PRIMARY KEY,
    name TEXT,
    activation_levels TEXT
);

CREATE TABLE IF NOT EXISTS champion_trait (
    champion_id INTEGER,
    trait_id INTEGER,
    FOREIGN KEY (champion_id) REFERENCES champion (id),
    FOREIGN KEY (trait_id) REFERENCES trait (id)
);

CREATE TABLE IF NOT EXISTS comp_champion (
    champion_id INTEGER,
    comp_id INTEGER,
    FOREIGN KEY (champion_id) REFERENCES champion (id),
    FOREIGN KEY (comp_id) REFERENCES comp (id)
);
"""
)


def init():
    # 피클에서 데이터 읽기
    with open("champion_list.pkl", "rb") as f:
        champion_data = pickle.load(f)
    with open("comp_list.pkl", "rb") as f:
        comp_data = pickle.load(f)

    for i, champ in enumerate(champion_data):
        print(champ)
        cursor.execute(
            """
        INSERT INTO champion (id, name, cost, value1, value2, value3)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            (i, champ.name, champ.cost, 1, 1, 1),
        )

    for i, comp in enumerate(comp_data):
        cursor.execute(
            """
        INSERT INTO comp (id, name)
        VALUES (?, ?)
        """,
            (i, comp.name),
        )

    conn.commit()
    conn.close()


def insert_trait():
    i = 0
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "거대 괴수", "2/4/6"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "결투가", "2/4/6/8"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "기원자", "2/4/6"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "난동꾼", "2/4/6/8"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "비전 마법사", "2/4/6/8"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "사신", "2/4"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "연인", "1"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "예술가", "1"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "이타심", "2/3/4"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "재주꾼", "2/4"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "저격수", "2/4/6"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "정령 주술사", "1"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "파수꾼", "2/4/6"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "현자", "2/3/4/5"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "호걸", "1"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "도자기", "2/4/6"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "먹그림자", "3/5/7"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "숲지기", "2/4/6"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "신화", "3/5/7/10"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "암영", "2/4/6/9"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "용군주", "2/3/4/5"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "이야기꾼", "3/5/7/10"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "천계", "2/3/4/5/6/7"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "필연", "3/5/7/10"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "행운", "3/5/7"),
    )
    i += 1
    cursor.execute(
        """
    INSERT INTO trait (id, name, activation_levels)
    VALUES (?, ?, ?)
    """,
        (i, "혼령", "2/4/6/8"),
    )
    i += 1
    conn.commit()


def insert_cc(champion_name_list, comp_name):
    for champion_name in champion_name_list:
        cursor.execute(
            """
        INSERT INTO comp_champion (champion_id, comp_id)
        VALUES (
            (SELECT id FROM champion WHERE name = ?),
            (SELECT id FROM comp WHERE name = ?))""",
            (champion_name, comp_name,),
        )
        conn.commit()


def insert_ct(champion_name_list: list, trait_name):
    for champion_name in champion_name_list:
        cursor.execute(
            """
        INSERT INTO champion_trait (champion_id, trait_id)
        VALUES (
            (SELECT id FROM champion WHERE name = ?),
            (SELECT id FROM trait WHERE name = ?))""",
            (champion_name, trait_name,),
        )


def update_comp():
    # 데이터 수정
    cursor.execute(
        """
    UPDATE comp
    SET name = ?
    WHERE id = ?
    """,
        ("파수꾼저격수", 8),
    )

    # 변경사항 저장 (커밋)
    conn.commit()


def show_db(entity):
    cursor.execute(f"select * from {entity}")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


# insert_trait()
# show_db("champion")
# show_db("trait")
# update_comp()

# insert_ct(["초가스", "요릭", "말파이트", "쓰레쉬", "쉔"], "거대 괴수")
# insert_ct(["볼리베어", "다리우스", "키아나", "야스오", "트리스타나"], "결투가")
# insert_ct(["코그모", "알룬", "잔나"], "기원자")
# insert_ct(["아트록스", "렉사이", "탐 켄치", "리븐", "코부코"], "난동꾼")
# insert_ct(["럭스", "니코", "조이", "아리", "일라오이"], "비전 마법사")
# insert_ct(["킨드레드", "요네", "카직스"], "사신")
# insert_ct([""], "연인")
# insert_ct([""], "예술가")
# insert_ct(["리븐", "소라카"], "이타심")
# insert_ct(["바드", "시비르", "티모"], "재주꾼")
# insert_ct(["세나", "코그모", "아펠리오스", "케이틀린"], "저격수")
# insert_ct([""], "정령 주술사")
# insert_ct(["아무무", "잭스", "나르", "가렌", "일라오이"], "파수꾼")
# insert_ct(["다이애나", "자이라"], "현자")
# insert_ct([""], "호걸")

# insert_ct(["럭스", "아무무"], "도자기")
# insert_ct(["볼리베어", "아트록스", "세나", "잭스"], "먹그림자")
# insert_ct(["렉사이", "킨드레드", "나르"], "숲지기")
# insert_ct(["초가스", "코그모", "탐 켄치", "니코", "바드"], "신화")
# insert_ct(["요릭", "다리우스", "알룬", "요네"], "암영")
# insert_ct(["잔나", "다이애나"], "용군주")
# insert_ct(["리븐", "조이", "시비르", "가렌", "자이라"], "이야기꾼")
# insert_ct(["말파이트", "키아나", "니코", "카직스", "소라카"], "천계")
# insert_ct(["쓰레쉬", "야스오", "아리", "킨드레드", "아펠리오스"], "필연")
# insert_ct(["트리스타나", "코부코", "조이", "티모"], "행운")
# insert_ct(["쉔", "아트록스", "일라오이", "케이틀린"], "혼령")
# show_db("champion_trait")

# with open("comp_list.pkl", "rb") as f:
#     comp_data = pickle.load(f)

# for comp in comp_data:
#     # print(comp)
#     insert_cc(comp.champions, comp.name)

# i = 48
# for _ in range(6):
#     cursor.execute("""select ROWID from comp_champion limit 1 OFFSET ?""", (i,))
#     row = cursor.fetchone()
#     rowid = row[0]
#     print(rowid)

#     cursor.execute('''
#         UPDATE comp_champion
#         SET comp_id = ?
#         WHERE ROWID = ?
#         ''', (8, rowid))
#     conn.commit()
#     i += 1


cursor.execute("""
update champion
set value2 = 160
where cost = 1
""")
show_db("champion")

conn.commit()
conn.close()
