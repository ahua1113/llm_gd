from evalplus.eval.utils import time_limit

from eval_pipeline.logValidator import LogValidator
from eval_pipeline.rule_pattern import Q1_PATTERN
from log_capture import LogCaptureSystem
from qsim.widgets import get_logs


def evaluate_code(problem_id: str, code: str, timeout: int = 5) -> dict:
    # 初始化验证系统
    capturer = LogCaptureSystem()

    # 根据问题ID加载规则
    rules = {
        "Q1": Q1_PATTERN,
        # 其他问题的规则...
    }[problem_id]

    try:
        with time_limit(timeout):
            with capturer.capture_logs(code) as logs:
                pass  # 代码已通过exec执行

        # 执行验证
        validator = LogValidator(
            actual_logs=get_logs(),  # 调用组件库的日志格式化方法
            expected_pattern=rules
        )
        score = validator.validate()

        return {
            "pass": score == 1.0,
            "score": score,
            "logs": logs
        }
    except TimeoutError:
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)}
