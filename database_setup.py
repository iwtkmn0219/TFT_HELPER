import sqlite3
import pickle
import os

from classes.comp import Comp
from classes.champion import Champion

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
    star INTEGER NOT NULL,
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

# 피클에서 데이터 읽기
with open("champion_list.pkl", "rb") as f:
    champion_data = pickle.load(f)
with open("comp_list.pkl", "rb") as f:
    comp_data = pickle.load(f)

for i, champ in enumerate(champion_data):
    print(champ)
    cursor.execute(
        """
    INSERT INTO champion (id, name, cost, star, value1, value2, value3)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (i, champ.name, champ.cost, champ.star, 1, 1, 1),
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
