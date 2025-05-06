import re

from eval_pipeline.rule_pattern import (Q1_PATTERN, Q2_PATTERN, Q5_PATTERN, Q4_PATTERN, Q3_PATTERN, Q9_PATTERN,
                                        Q8_PATTERN, Q7_PATTERN, Q6_PATTERN, Q10_PATTERN)

# 定义问题与正则模式的映射关系
pattern_mapping = {
    1: Q1_PATTERN,
    2: Q2_PATTERN,
    3: Q3_PATTERN,
    4: Q4_PATTERN,
    5: Q5_PATTERN,
    6: Q6_PATTERN,
    7: Q7_PATTERN,
    8: Q8_PATTERN,
    9: Q9_PATTERN,
    10: Q10_PATTERN
}


# pass@k评估函数，传入问题id和日志字符串，返回匹配程度
def isPass(problem_id, logs_str):
    """评估日志字符串在指定问题上的匹配程度"""
    patterns = pattern_mapping.get(problem_id, {})
    if not patterns:
        return 0.0

    matched_count = 0
    total_patterns = len(patterns)
    compiled_patterns = {key: re.compile(pattern) for key, pattern in patterns.items()}

    for line in logs_str.split('\n'):
        for key, pattern_obj in compiled_patterns.items():
            if pattern_obj.search(line):
                matched_count += 1
                # 一旦某个模式匹配成功，就不再对该模式进行后续匹配
                del compiled_patterns[key]
                if len(compiled_patterns) == 0:
                    break
        if len(compiled_patterns) == 0:
            break

    return matched_count / total_patterns if total_patterns > 0 else 0.0
