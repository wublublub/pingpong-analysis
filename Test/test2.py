import numpy as np

def calculate_scenario_score(scenario_prob, second_step_probs, transition_matrix, states):
    direct_score = scenario_prob * second_step_probs[states.index("P_1")]
    opponent_miss = scenario_prob * second_step_probs[states.index("E/N_2")]

    # 动态读取状态转移矩阵中对应行的P_1的数据
    lf2_miss = second_step_probs[states.index("LF_2")] * transition_matrix[states.index("LF_2"), states.index("P_1")]
    sb2_miss = second_step_probs[states.index("SB_2")] * transition_matrix[states.index("SB_2"), states.index("P_1")]
    lb2_miss = second_step_probs[states.index("LB_2")] * transition_matrix[states.index("LB_2"), states.index("P_1")]

    combined_score = direct_score + opponent_miss + (scenario_prob * lf2_miss) + (scenario_prob * sb2_miss) + (scenario_prob * lb2_miss)
    return combined_score

def suggest_best_action(transition_matrix, states):
    best_action = None
    best_score = -1

    for initial_state_action in ["SF_1", "SF_2", "LF_1", "LF_2", "SB_1", "SB_2", "LB_1", "LB_2"]:
        initial_state = np.zeros(len(states))
        initial_state[states.index(initial_state_action)] = 1

        first_step_probs = np.dot(initial_state, transition_matrix)

        total_score = 0.0
        for i, first_prob in enumerate(first_step_probs):
            if first_prob > 0:
                next_state = np.zeros(len(states))
                next_state[i] = 1
                second_step_probs = np.dot(next_state, transition_matrix)
                total_score += calculate_scenario_score(first_prob, second_step_probs, transition_matrix, states)

        if total_score > best_score:
            best_score = total_score
            best_action = initial_state_action

    return best_action, best_score

# 推荐最佳回击技术动作
best_action, best_score = suggest_best_action(transition_matrix, states)
print(f"\n最佳回击技术动作: {best_action}，预计得分概率: {best_score}")

# 提供接口给外部程序
def get_optimal_strategy(transition_matrix):
    best_action, best_score = suggest_best_action(transition_matrix, states)
    return best_action, best_score

# 示例调用
optimal_action, optimal_score = get_optimal_strategy(transition_matrix)
print(f"\n外部程序调用接口，最佳回击技术动作: {optimal_action}，预计得分概率: {optimal_score}")
