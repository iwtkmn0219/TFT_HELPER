from flask import Flask, request, jsonify, Response, render_template
import pickle
import json
import sqlite3

from classes.champion import Champion
from classes.comp import Comp
from algorithm.recommendation import recommend_comps
from db.database_manage import load_data_from_db

app = Flask(__name__)

# 데이터 불러오기
champion_list, champion_dict, comp_list = load_data_from_db()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/get_comps", methods=["POST"])
def get_comps():
    data = request.json
    selected_champions = data.get("champions", [])

    # 선택된 챔피언들을 객체로 변환
    selected_champion_objects = [
        # champion_dict[champion] for champion in selected_champions
        Champion(
            champion["name"],
            champion_dict[champion["name"]].cost,
            champion["star"],
            champion_dict[champion["name"]].value,
        )
        for champion in selected_champions
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
