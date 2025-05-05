import numpy as np
from collections import Counter


def ngram_match(reference, prediction, n):
    ref_ngrams = Counter([tuple(reference[i:i + n]) for i in range(len(reference) - n + 1)])
    pred_ngrams = Counter([tuple(prediction[i:i + n]) for i in range(len(prediction) - n + 1)])
    overlap = sum((ref_ngrams & pred_ngrams).values())
    total = sum(pred_ngrams.values())
    if total == 0:
        return 0
    return overlap / total


def lcs_match(reference, prediction):
    m, n = len(reference), len(prediction)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if reference[i - 1] == prediction[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n] / max(m, n)


def codebleu(reference, prediction, weights=(0.25, 0.25, 0.25, 0.25)):
    unigram = ngram_match(reference, prediction, 1)
    bigram = ngram_match(reference, prediction, 2)
    lcs = lcs_match(reference, prediction)
    # 这里简化加权 n - gram Match 为 Unigram 和 Bigram 的组合
    weighted_ngram = (unigram + bigram) / 2
    scores = [unigram, bigram, lcs, weighted_ngram]
    return np.dot(weights, scores)


# 示例参考代码和生成代码
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

score = codebleu(reference_code, candidate_code)
print(f"CodeBLEU Score: {score}")
