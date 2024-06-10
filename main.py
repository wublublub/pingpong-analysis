from Test.test import (
    get_best_action_and_scores,
    suggest_best_action,
)
from data import PingpongData

data = PingpongData()

# 输入2号选手的技术动作
input_action = "LB_2"

# 推荐最佳回击技术动作
best_action, best_score, action_scores = suggest_best_action(
    input_action, data.transition_matrix, data.states
)

# 打印结果
result = get_best_action_and_scores(
    input_action, best_action, best_score, action_scores
)

print(result)
