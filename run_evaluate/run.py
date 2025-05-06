import contextlib
import io
import re
from typing import List
from eval_pipeline.call_api import get_problem, doubao_code, deepseek_code, tongyi_code
from eval_pipeline.rule_pattern import (
    Q1_PATTERN, Q2_PATTERN, Q3_PATTERN, Q4_PATTERN, Q5_PATTERN,
    Q6_PATTERN, Q7_PATTERN, Q8_PATTERN, Q9_PATTERN, Q10_PATTERN
)
from qsim.widgets import (
    QSimLayout, QSimApplication, QSimListWidget, QSimSignal, QSimColor, QSimPixmap, QSimLabel,
    QSimHBoxLayout, QSimVBoxLayout, QSimWidget, QSimFontComboBox, QSimRadioButton, QSimPushButton,
    QSimTabWidget, QSimCheckBox, QSimGroupBox, QSimListWidgetItem, QSimComboBox, QSimTableWidget,
    QSimTableWidgetItem, QSimSpinBox, QSimSlider, QSimFrame, QSimProgressBar, QSimStatusBar,
    QSimHeaderView, QSimLineEdit, Qt, QSimFont, QSimGridLayout
)
from run_evaluate.bleu.codebleu_maintain import compute_codebleu
from run_evaluate.rouge.rouge import compute_rouge
from run_evaluate.passk.custom_evaluator import isPass

"""
三个评估指标：
1.codebleu
2.rouge
3.pass@k
"""


# 日志捕获，但在运行出错时，不终止程序，只是给出一个空的日志返回结果

class LogCaptureSystem:
    def __init__(self):
        self._logs = []
        self._original_logs = None

    def _override_imports(self):
        """劫持组件类的日志记录方法"""
        # 备份原始日志列表
        self._original_logs = QSimLayout._logs
        # 劫持日志存储地址
        QSimLayout._logs = self._logs

    def _restore_imports(self):
        """恢复原始组件引用"""
        QSimLayout._logs = self._original_logs

    @contextlib.contextmanager
    def capture_logs(self, code: str):
        """执行代码并捕获日志的上下文管理器"""
        self._logs.clear()
        self._override_imports()
        try:
            with io.StringIO() as buf:
                with contextlib.redirect_stdout(buf):
                    try:
                        exec(code, globals())
                        if 'app' in globals() and hasattr(globals()['app'], 'exec_'):
                            globals()['app'].exec_()
                    except Exception as e:
                        print(f"执行代码时出现异常: {e}")
                        # 确保出现异常时返回空日志列表
                        self._logs = []
            yield self._logs
        finally:
            self._restore_imports()


# 评估主函数
def run_evaluate():
    # 将对应模型生成的代码用变量存储，采用键值对存储，key为问题id，value为代码
    # 要支持key可重复，因为一个大模型会生成多份代码，但是要保证先后顺序，即先生成的代码排在前面，后生成的代码排在后面
    # 例如：code_doubao["Q1"] = ["代码1", "代码2", "代码3", "代码4", "代码5"]，表示Q1的问题，大模型生成的5份代码，分别是代码1，代码2，代码3，代码4，代码5，

    # 对于每一个问题，每一个大模型调用n次，每次生成m份代码，则需要存储n*m份代码，即n*m个元素，因此需要保证先后顺序，即先生成的代码排在前面，后生成的代码排在后面

    # 若有k个问题，则需要存储k*n*m份代码
    
    # problems 中除第一个元素以外，剩下的元素即为Q1-Q10的问题
    # 即problems[1]表示Q1的内容，因此需要手动给大模型生成的代码的结果存储map中给每个问题的key赋值

    # 再设置大模型的日志结果存储字典，与上述代码列表一一对应，同样要保持先后顺序
    # 例如：log_doubao["Q1"] = ["日志1", "日志2", "日志3", "日志4", "日志5"]，表示Q1的问题，大模型生成的5份代码，分别是日志1，日志2，日志3，日志4，日志5，

    # 上述结果是评估的关键，需要将大模型生成的代码和日志结果存储起来，然后再进行评估，需要分问题评估，得到每个问题的结果，再平均
    # 评估三份指标:需要注意，对于每一个问题都需要得到这三份指标，然后三份指标加权计算单个问题的评估结果，最后再平均得到最终评估结果
    # 1.取大模型生成的代码，计算codebleu指标，评估同一个模型生成的n*m份代码之间的相似度
    # 2.取大模型生成的代码运行后产生的日志，计算ROUGE指标，评估同一个模型n*m份日志结果的相似度
    # 3.取规则匹配结果，计算pass@k

    # 各指标中结果，同样作为字典，为每一份代码计算评估结果，最后再计算平均值

    problems = get_problem()

    code_doubao = {}
    code_deepseek = {}
    code_tongyi = {}

    log_doubao = {}
    log_deepseek = {}
    log_tongyi = {}

    log_capture = LogCaptureSystem()

    # 只测试Q1和Q2，k=2，n=2，m=5，故共20份代码，20份日志结果
    for i in range(1, 2):
        problem_id = f"Q{i}"
        problem = problems[i]

        print(problem)

        code_doubao[problem_id] = []
        code_deepseek[problem_id] = []
        code_tongyi[problem_id] = []

        log_doubao[problem_id] = []
        log_deepseek[problem_id] = []
        log_tongyi[problem_id] = []

        # 每个问题每个模型重复生成 2 次代码，每次生成 5 份代码
        for _ in range(2):
            # 调用 Doubao 生成代码
            doubao_generated_code = doubao_code(problem, 5)

            # 调用 DeepSeek 生成代码
            deepseek_generated_code = deepseek_code(problem, 5)
            
            # 调用 Tongyi 生成代码
            tongyi_generated_code = tongyi_code(problem, 5)

            # 处理代码，去除多余的空格和换行符
            for i in range(len(doubao_generated_code)):
                doubao_generated_code[i] = doubao_generated_code[i].strip()
                deepseek_generated_code[i] = deepseek_generated_code[i].strip()
                tongyi_generated_code[i] = tongyi_generated_code[i].strip()

            # 存储生成的代码，每一个问题对应一个列表，列表中存储的是生成的代码
            # 例如：code_doubao["Q1"] = ["代码1", "代码2", "代码3", "代码4", "代码5"]，表示Q1的问题，大模型生成的5份代码，分别是代码1，代码2，代码3，代码4，代码5，
            code_doubao[problem_id].append(doubao_generated_code)
            code_deepseek[problem_id].append(deepseek_generated_code)
            code_tongyi[problem_id].append(tongyi_generated_code)

            # 捕获日志，循环捕获，对同一个问题，捕获n*m份日志结果
            for i in range(len(doubao_generated_code)):
                # 传入列表中的单个代码元素来捕获日志
                with log_capture.capture_logs(doubao_generated_code[i]) as captured_logs:
                    log_doubao[problem_id].append(str(captured_logs))

                with log_capture.capture_logs(deepseek_generated_code[i]) as captured_logs:
                    log_deepseek[problem_id].append(str(captured_logs))

                with log_capture.capture_logs(tongyi_generated_code[i]) as captured_logs:
                    log_tongyi[problem_id].append(str(captured_logs))

    # 各指标
    codebleu_doubao = {}
    codebleu_deepseek = {}
    codebleu_tongyi = {}

    rouge_doubao = {}
    rouge_deepseek = {}
    rouge_tongyi = {}

    pass_at_k_doubao = {}
    pass_at_k_deepseek = {}
    pass_at_k_tongyi = {}

    # 遍历每个问题，计算每个模型的评估结果
    for problem_id in code_doubao.keys():
        # 1.计算 CodeBLEU 得分
        codebleu_doubao[problem_id] = []
        codebleu_deepseek[problem_id] = []
        codebleu_tongyi[problem_id] = []

        for i in range(20):
            codebleu_doubao[problem_id].append(
                compute_codebleu(code_doubao[problem_id][i], code_doubao[problem_id][i + 1]))
            codebleu_deepseek[problem_id].append(
                compute_codebleu(code_deepseek[problem_id][i], code_deepseek[problem_id][i + 1]))
            codebleu_tongyi[problem_id].append(
                compute_codebleu(code_tongyi[problem_id][i], code_tongyi[problem_id][i + 1]))

        # 2.计算 ROUGE 得分
        '''
        rouge_doubao[problem_id] = []
        rouge_deepseek[problem_id] = []
        rouge_tongyi[problem_id] = []

        for i in range(30):
            rouge_doubao[problem_id].append(compute_rouge(log_doubao[problem_id][i], log_doubao[problem_id][i + 1]))
            rouge_deepseek[problem_id].append(
                compute_rouge(log_deepseek[problem_id][i], log_deepseek[problem_id][i + 1]))
            rouge_tongyi[problem_id].append(compute_rouge(log_tongyi[problem_id][i], log_tongyi[problem_id][i + 1]))
        '''

        # 3.计算 Pass@k 得分
        pass_at_k_doubao[problem_id] = []
        pass_at_k_deepseek[problem_id] = []
        pass_at_k_tongyi[problem_id] = []
        # 为每一个问题计算得分，问题和得分一一对应，一个问题有多份日志，因此一个问题有多个得分
        for i in range(20):
            pass_at_k_doubao[problem_id].append(isPass(problem_id, log_doubao[problem_id][i]))
            pass_at_k_deepseek[problem_id].append(isPass(problem_id, log_deepseek[problem_id][i]))
            pass_at_k_tongyi[problem_id].append(isPass(problem_id, log_tongyi[problem_id][i]))

    # 计算每个模型的平均得分
    avg_codebleu_doubao = sum(sum(codebleu_doubao.values(), [])) / len(sum(codebleu_doubao.values(), []))
    avg_codebleu_deepseek = sum(sum(codebleu_deepseek.values(), [])) / len(sum(codebleu_deepseek.values(), []))
    avg_codebleu_tongyi = sum(sum(codebleu_tongyi.values(), [])) / len(sum(codebleu_tongyi.values(), []))

    '''
    avg_rouge_doubao = sum(sum(rouge_doubao.values(), [])) / len(sum(rouge_doubao.values(), []))
    avg_rouge_deepseek = sum(sum(rouge_deepseek.values(), [])) / len(sum(rouge_deepseek.values(), []))
    avg_rouge_tongyi = sum(sum(rouge_tongyi.values(), [])) / len(sum(rouge_tongyi.values(), []))
    '''

    avg_pass_at_k_doubao = sum(sum(pass_at_k_doubao.values(), [])) / len(sum(pass_at_k_doubao.values(), []))
    avg_pass_at_k_deepseek = sum(sum(pass_at_k_deepseek.values(), [])) / len(sum(pass_at_k_deepseek.values(), []))
    avg_pass_at_k_tongyi = sum(sum(pass_at_k_tongyi.values(), [])) / len(sum(pass_at_k_tongyi.values(), []))

    # 输出结果
    print("CodeBLEU 得分：")
    print("Doubao:", avg_codebleu_doubao)
    print("DeepSeek:", avg_codebleu_deepseek)
    print("Tongyi:", avg_codebleu_tongyi)

    print("ROUGE 得分：")
    '''
    print("Doubao:", avg_rouge_doubao)
    print("DeepSeek:", avg_rouge_deepseek)
    print("Tongyi:", avg_rouge_tongyi)
    '''

    print("Pass@k 得分：")
    print("Doubao:", avg_pass_at_k_doubao)
    print("DeepSeek:", avg_pass_at_k_deepseek)
    print("Tongyi:", avg_pass_at_k_tongyi)


if __name__ == "__main__":
    run_evaluate()
