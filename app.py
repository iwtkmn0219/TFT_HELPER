from flask import Flask, request, jsonify, Response, render_template
import pickle
import json

from classes.champion import Champion
from classes.comp import Comp

app = Flask(__name__)

# 데이터 불러오기
with open("champion_list.pkl", "rb") as file:
    champion_list = pickle.load(file)
with open("comp_list.pkl", "rb") as file:
    comp_list = pickle.load(file)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_comps", methods=["POST"])
def get_comps():
    data = request.json
    pocket = data.get("champions", [])

    # 조합 필터링 로직
    valid_comps = [
        comp
        for comp in comp_list
        if all(champion in comp.champions for champion in pocket)
    ]

    # JSON 변환
    valid_comps_json = [comp.to_dict() for comp in valid_comps]
    response = Response(
        json.dumps(valid_comps_json, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )

    return response

@app.route('/get_champion_list', methods=['GET'])
def get_champion_list():
    champion_list_dicts = [champion.to_dict() for champion in champion_list]
    response = Response(json.dumps(champion_list_dicts, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return response


if __name__ == "__main__":
    app.run(debug=True)
