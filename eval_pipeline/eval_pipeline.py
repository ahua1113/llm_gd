import json
from codebleu.codebleu_robust import RobustnessScorer
from codebleu.codebleu_maintain import MaintainabilityScorer


def evaluate_model_output(dataset_path, predictions_path):
    # 加载数据
    with open(dataset_path) as f:
        dataset = [json.loads(line) for line in f]

    with open(predictions_path) as f:
        preds = {item["task_id"]: item["prediction"] for line in f for item in [json.loads(line)]}

    results = []
    for item in dataset:
        task_id = item["task_id"]
        if task_id not in preds:
            continue

        # 获取参考答案和预测代码
        ref_code = item["canonical_solution"]
        cand_code = preds[task_id]

        # 计算健壮性
        required_errors = list({test["type"] for test in item.get("robust_tests", [])})
        robust_score = RobustnessScorer(ref_code, cand_code).calculate_robust_score(required_errors)

        # 计算可维护性
        maintain_score = MaintainabilityScorer(cand_code).calculate_maintain_score()

        results.append({
            "task_id": task_id,
            "robustness": robust_score,
            "maintainability": maintain_score,
            "combined_score": 0.6 * robust_score + 0.4 * maintain_score
        })

    # 输出结果分析
    avg_robust = sum(r["robustness"] for r in results) / len(results)
    avg_maintain = sum(r["maintainability"] for r in results) / len(results)
    print(f"平均健壮性: {avg_robust:.2f}, 平均可维护性: {avg_maintain:.2f}")


# 运行评估
evaluate_model_output("data/HumanEvalPlus_Robust.jsonl", "samples/model_predictions.jsonl")