# （生成测试用例）
import json
from itertools import product


def inject_robustness_cases(original_file, output_file):
    with open(original_file) as f:
        dataset = [json.loads(line) for line in f]

    # 为每个任务添加3类异常测试用例
    robustness_tests = {
        "type_confusion": ["'123'", "3.14", "[1,2]"],  # 类型混淆
        "boundary_violation": ["-1", "101", "999"],  # 边界越界
        "format_error": ["'user'", "'a@'", "'@.com'"]  # 格式错误
    }

    for item in dataset:
        if "输入验证" in item["prompt"]:  # 仅处理输入验证类题目
            func_name = item["entry_point"]
            args = item["arguments"][0]  # 假设单参数输入

            # 生成异常测试用例
            new_tests = []
            for case_type, values in robustness_tests.items():
                for val in values:
                    test_code = f"assert {func_name}({val}) == ..."
                    new_tests.append({
                        "input": val,
                        "expected": "exception",
                        "type": case_type
                    })

            item["robust_tests"] = new_tests

    with open(output_file, "w") as f:
        for item in dataset:
            f.write(json.dumps(item) + "\n")


# 增强数据集
inject_robustness_cases(".jsonl", ".jsonl")