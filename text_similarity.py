from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
        return None
    except Exception as e:
        print(f"错误: 读取文件 {file_path} 时发生错误: {e}")
        return None


def text_cosine_similarity(file_path1, file_path2):
    text1 = read_text_from_file(file_path1)
    text2 = read_text_from_file(file_path2)

    if text1 is None or text2 is None:
        return None

    # 将文本转换为向量
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    # 计算余弦相似度
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0]


'''
路径示例参考
file_path1 = '日志文本结果/testQ3-yuanbao.py.txt'
file_path2 = '日志文本结果/testQ3-doubao.py.txt'
'''


def compare_text_similarity(file_path1, file_path2):
    # 计算相似度
    similarity = text_cosine_similarity(file_path1, file_path2)
    if similarity is not None:
        print(f"两个文本文件内容的余弦相似度为: {similarity}")


file1 = '日志文本结果/testQ5-deepseek.py.txt'
file2 = '日志文本结果/testQ5-doubao.py.txt'
compare_text_similarity(file1, file2)
