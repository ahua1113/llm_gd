from typing import List

from eval_pipeline.rule_pattern import Rule


class LogValidator:
    def __init__(self, actual_logs: List[str], expected_pattern: Rule):
        self.actual = actual_logs
        self.expected = expected_pattern

    def _parse_event(self, log_entry: str) -> dict:
        """解析单条日志条目"""
        parts = log_entry.split()
        return {
            "type": parts[0].strip("[]"),
            "params": parts[1:]
        }

    def _match_single(self, actual: dict, expected: dict) -> bool:
        """单个日志条目匹配逻辑"""
        # 类型必须严格匹配
        if actual['type'] != expected['type']:
            return False

        # 类名匹配（如果有指定）
        if 'class' in expected:
            class_param = next((p for p in actual['params'] if p.startswith("QSim")), None)
            if class_param != expected['class']:
                return False

        # 文本内容匹配（正则表达式支持）
        if 'text' in expected:
            import re
            if not any(re.match(expected['text'], param) for param in actual['params']):
                return False

        # 路径深度匹配
        if 'path' in expected:
            actual_path = self._extract_path(actual)
            if len(actual_path) != len(expected['path']):
                return False
            for (a_type, a_idx), (e_type, e_idx) in zip(actual_path, expected['path']):
                if a_type != e_type or (e_idx != '*' and a_idx != e_idx):
                    return False

        return True

    def validate(self) -> float:
        """执行全量验证，返回匹配度（0.0-1.0）"""
        matched = 0
        actual_events = [self._parse_event(e) for e in self.actual]

        for expected in self.expected:
            for actual in actual_events:
                if self._match_single(actual, expected):
                    matched += 1
                    break

        return matched / len(self.expected)