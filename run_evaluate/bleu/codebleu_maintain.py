import ast
from nltk.translate.bleu_score import sentence_bleu
import tokenize
from io import BytesIO


def tokenize_code(code):
    """将代码转换为token序列"""
    try:
        tokens = []
        code_bytes = code.encode('utf-8')
        for tok in tokenize.tokenize(BytesIO(code_bytes).readline):
            if tok.type not in (tokenize.ENCODING, tokenize.ENDMARKER):
                tokens.append(tok.string)
        return tokens
    except:
        return []


def get_ast_nodes(code):
    """提取AST节点类型序列"""
    try:
        tree = ast.parse(code)
        return [type(node).__name__ for node in ast.walk(tree)]
    except SyntaxError:
        return []


def compute_codebleu(reference, candidate):
    """
    计算CodeBLEU分数（简化版）
    参数：
        reference: 参考答案代码字符串
        candidate: 待评估代码字符串
    返回：
        综合得分（0-1之间）
    """
    # 计算代码BLEU
    ref_tokens = tokenize_code(reference)
    can_tokens = tokenize_code(candidate)
    code_bleu = sentence_bleu([ref_tokens], can_tokens) if ref_tokens and can_tokens else 0.0

    # 计算AST结构相似度
    ref_ast = get_ast_nodes(reference)
    can_ast = get_ast_nodes(candidate)
    ast_bleu = sentence_bleu([ref_ast], can_ast) if ref_ast and can_ast else 0.0

    # 组合得分（可根据需求调整权重）
    return 0.5 * code_bleu + 0.5 * ast_bleu


# 示例用法
reference_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""

candidate_code = """
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)
"""

print(f"CodeBLEU 分数：{compute_codebleu(reference_code, candidate_code):.4f}")
