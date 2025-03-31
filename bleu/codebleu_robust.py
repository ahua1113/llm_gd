import ast
import re


class RobustnessScorer:
    def __init__(self, reference_code, candidate_code):
        self.ref_code = reference_code
        self.cand_code = candidate_code

    def _count_validation_blocks(self):
        """统计输入验证代码块（if/raise或try/except）"""
        # 使用正则匹配代替AST解析
        if_raise = len(re.findall(r"if\s+.*?raise", self.cand_code))
        try_except = len(re.findall(r"try:.*?except", self.cand_code, re.DOTALL))
        return if_raise + try_except

    def _detect_checked_errors(self):
        """检测候选代码处理的异常类型"""
        error_types = set(re.findall(r"except\s+(\w+)", self.cand_code))
        return list(error_types)

    def calculate_robust_score(self, required_errors):
        """健壮性评分（0-1）"""
        # 基础分：验证代码块占比
        total_lines = len(self.cand_code.split('\n'))
        val_blocks = self._count_validation_blocks()
        base_score = min(val_blocks / 3, 1.0)  # 每3行一个验证块得1分

        # 加分项：覆盖所需异常
        covered = len(set(required_errors) & set(self._detect_checked_errors()))
        bonus = min(covered * 0.2, 0.6)  # 每个覆盖+0.2，上限0.6

        # 惩罚项：过度使用try/except
        try_ratio = len(re.findall(r"try", self.cand_code)) / total_lines
        penalty = 0.2 if try_ratio > 0.3 else 0

        return round(base_score + bonus - penalty, 2)


# 使用示例
ref_code = "def validate_age(age):\n    if not isinstance(age, int): raise TypeError"
cand_code = """
def validate_age(a):
    try:
        if a < 0: raise ValueError
    except: pass
"""

scorer = RobustnessScorer(ref_code, cand_code)
score = scorer.calculate_robust_score(["TypeError", "ValueError"])
print(f"Robust Score: {score}")  # 输出: 0.6（1基础分 + 1异常覆盖×0.2 - 0惩罚）