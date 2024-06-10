from Test.test import (
    get_best_action_and_scores,
    suggest_best_action,
)
from flask import Flask, json, request
from data import PingpongData

app = Flask(__name__)
data = PingpongData()


@app.route("/get_result")
def get_result():
    # 输入2号选手的技术动作
    input_action = request.args.get("action", "")
    # input_action = "LB_2"

    # 推荐最佳回击技术动作
    best_action, best_score, action_scores = suggest_best_action(
        input_action, data.transition_matrix, data.states
    )

    # 打印结果
    result = get_best_action_and_scores(
        input_action, best_action, best_score, action_scores
    )
    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port="8000")
