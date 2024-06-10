from Test.test import get_transition_matrix, get_best_action_and_scores, suggest_best_action
from flask import Flask, json, request

app=Flask(__name__)

# 定义状态名称
states = ["S_1", "S_2", "SF_1", "SF_2", "LF_1", "LF_2", "SB_1", "SB_2", "LB_1", "LB_2", "CB_1", "CB_2", "E/N_1", "E/N_2", "P_1", "P_2"]
# 获取转移矩阵
transition_matrix = get_transition_matrix()

@app.route('/get_result')
def get_result():

    # 输入2号选手的技术动作
    input_action = request.args.get('action','')
    # input_action = "LB_2"

    # 推荐最佳回击技术动作
    best_action, best_score, action_scores = suggest_best_action(input_action, transition_matrix, states)

    # 打印结果
    result = get_best_action_and_scores(input_action, best_action, best_score, action_scores)

    return json.dumps(result, ensure_ascii=False, indent=4)

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port='8000')