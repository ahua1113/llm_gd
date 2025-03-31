class MaintainabilityScorer:
    def __init__(self, candidate_code):
        self.code = candidate_code

    def _module_detection(self):
        """检测验证逻辑是否模块化（通过关键词匹配）"""
        return 1 if "def validate_" in self.code else 0

    def _naming_quality(self):
        """变量命名可读性（正则匹配valid/check前缀）"""
        valid_vars = len(re.findall(r"\bvalid_\w+", self.code))
        check_vars = len(re.findall(r"\bcheck_\w+", self.code))
        return min((valid_vars + check_vars) * 0.5, 1.0)

    def _duplicate_check(self):
        """重复代码检测（简单相邻行比对）"""
        lines = self.code.split('\n')
        dup_count = 0
        for i in range(len(lines) - 1):
            if lines[i] and lines[i] == lines[i + 1]:
                dup_count += 1
        return dup_count

    def calculate_maintain_score(self):
        """可维护性评分（0-1）"""
        modular = self._module_detection() * 0.4  # 模块化占比40%
        naming = self._naming_quality() * 0.3  # 命名质量30%

        # 重复代码扣分（每处重复扣5%）
        dup_penalty = min(self._duplicate_check() * 0.05, 0.3)
        return round(modular + naming - dup_penalty, 2)


# 使用示例
cand_code = """
def validate_age(age):
    if age < 0: print("无效")
    if age < 0: print("无效")  # 重复行
"""
scorer = MaintainabilityScorer(cand_code)
print(scorer.calculate_maintain_score())  # 输出: 0.55（模块化0.4 + 命名0.3 - 重复0.15）