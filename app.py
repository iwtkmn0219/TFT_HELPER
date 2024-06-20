from flask import Flask, request, jsonify, Response, render_template
import pickle
import json
import sqlite3

from classes.champion import Champion
from classes.comp import Comp
from algorithm.recommendation import recommend_comps

app = Flask(__name__)

# 데이터 불러오기
conn = sqlite3.connect("tft_helper.db")
curr = conn.cursor()
champions = curr.execute("select * from champion").fetchall()
champion_list = [
    Champion(champion[1], champion[2], 2, [champion[3], champion[4], champion[5]])
    for champion in champions
]
champion_dict = {
    champion[1]: Champion(
        champion[1], champion[2], 2, [champion[3], champion[4], champion[5]]
    )
    for champion in champions
}

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_comps", methods=["POST"])
def get_comps():
    data = request.json
    selected_champions = data.get("champions", [])

    # 선택된 챔피언들을 객체로 변환
    selected_champion_objects = [
        champion_dict[champion] for champion in selected_champions
    ]
    # comp 추천 알고리즘 호출
    recommended_comps = recommend_comps(selected_champion_objects)

    # JSON 변환
    recommend_comps_json = [
        {"score": comp_and_value[0], "comp": comp_and_value[1].to_dict()}
        for comp_and_value in recommended_comps
    ]
    response = Response(
        json.dumps(recommend_comps_json, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )

    return response


@app.route("/get_champion_list", methods=["GET"])
def get_champion_list():
    champion_list_dicts = [champion.to_dict() for champion in champion_list]
    response = Response(
        json.dumps(champion_list_dicts, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
