import numpy as np

def get_transition_matrix():
    # 示例转移矩阵，可以根据需要进行修改或输入新的转移矩阵
    return np.array([
        [0.00, 0.56, 0.00, 0.08, 0.00, 0.20, 0.00, 0.16, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # S_1
        [0.68, 0.00, 0.12, 0.00, 0.16, 0.00, 0.04, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # S_2
        [0.00, 0.00, 0.00, 0.3158, 0.00, 0.0526, 0.00, 0.4737, 0.00, 0.00, 0.00, 0.0526, 0.00, 0.1053],  # SF_1
        [0.00, 0.00, 0.50, 0.00, 0.00, 0.00, 0.375, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0625, 0.0625],  # SF_2
        [0.00, 0.00, 0.00, 0.2813, 0.00, 0.00, 0.00, 0.50, 0.00, 0.00, 0.00, 0.00, 0.0625, 0.1563],  # LF_1
        [0.00, 0.00, 0.125, 0.00, 0.00, 0.00, 0.75, 0.00, 0.00, 0.00, 0.00, 0.00, 0.075, 0.05],  # LF_2
        [0.00, 0.50, 0.00, 0.25, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # SB_1
        [0.3333, 0.00, 0.1667, 0.00, 0.00, 0.00, 0.3333, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.1667],  # SB_2
        [0.00, 0.00, 0.00, 0.35, 0.00, 0.00, 0.00, 0.35, 0.00, 0.00, 0.00, 0.00, 0.0167, 0.2833],  # LB_1
        [0.00, 0.00, 0.383, 0.00, 0.00, 0.00, 0.3962, 0.00, 0.0755, 0.00, 0.00, 0.00, 0.1698, 0.0755],  # LB_2
        [0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.50, 0.00, 0.00, 0.00, 0.00, 0.00, 0.25],  # CB_1
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # CB_2
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # E/N_1
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],  # E/N_2
        # [0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00], # P_1
        # [0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  1.00] # P_2
    ])

def calculate_scenario_score(second_step_probs, transition_matrix, states):
    # 计算每种情景下的得分概率
    direct_score = second_step_probs[states.index("P_1")-2]
    # 动态读取状态转移矩阵中对应行的P_1的数据
    lf2_miss = second_step_probs[states.index("LF_2")-2] * transition_matrix[states.index("LF_2")-2, 13]
    sb2_miss = second_step_probs[states.index("SB_2")-2] * transition_matrix[states.index("SB_2")-2, 13]
    lb2_miss = second_step_probs[states.index("LB_2")-2] * transition_matrix[states.index("LB_2")-2, 13]
    sf2_miss = second_step_probs[states.index("SF_2")-2] * transition_matrix[states.index("SF_2")-2, 13]
    en2_miss = second_step_probs[states.index("E/N_2")-2] * transition_matrix[states.index("E/N_2")-2, 13]
    cb2_miss = second_step_probs[states.index("CB_2")-2] * transition_matrix[states.index("CB_2")-2, 13]

    combined_score = direct_score + lf2_miss + sb2_miss + lb2_miss + sf2_miss + en2_miss + cb2_miss
    return combined_score

def suggest_best_action(input_action, transition_matrix, states):
    action_scores = {}
    best_action = None
    best_score = -1

    initial_state_index = states.index(input_action)
    first_step_probs = transition_matrix[initial_state_index]

    for i, first_prob in enumerate(first_step_probs):
        if first_prob > 0 and i < len(states)-4:
            second_step_probs = transition_matrix[i+2]##去除S_1和S_2
            scenario_score = calculate_scenario_score(second_step_probs, transition_matrix, states)
            total_score = scenario_score
            if states[i] == 'S_1':
                continue
            if states[i] == 'S_2':
                continue
            action_scores[states[i+2]] = total_score
            if total_score > best_score:
                best_score = total_score
                best_action = states[i]

    return best_action, best_score, action_scores

def get_best_action_and_scores(input_action, best_action, best_score, action_scores):
    result = {
        "input_action": input_action,
        "best_action": best_action,
        "best_score": best_score,
        "other_action_scores": [
            {"action": action, "score": score} for action, score in action_scores.items()
        ]
    }

    # print(result)
    return result
