from flask import Flask, request, jsonify, Response, render_template
import pickle
import json

from classes.champion import Champion
from classes.comp import Comp
from algorithm.recommendation import recommend_comps

app = Flask(__name__)

# 데이터 불러오기
with open("champion_list.pkl", "rb") as file:
    champion_list = pickle.load(file)
    champion_dict = {champion.name: champion for champion in champion_list}
with open("comp_list.pkl", "rb") as file:
    comp_list = pickle.load(file)


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
    recommended_comps = recommend_comps(selected_champions, comp_list)

    # JSON 변환
    recommend_comps_json = [comp.to_dict() for comp in recommended_comps]
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
