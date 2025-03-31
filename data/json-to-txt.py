import json


def jsonl_to_txt(jsonl_file_path, txt_file_path):
    try:
        with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                for line in jsonl_file:
                    try:
                        data = json.loads(line)
                        # 假设取字典中的所有值拼接成文本
                        text = ' '.join(str(value) for value in data.values())
                        txt_file.write(text + '\n')
                    except json.JSONDecodeError:
                        print(f"错误: 无法解析行 {line}")
    except FileNotFoundError:
        print("错误: 文件未找到!")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")


if __name__ == "__main__":
    jsonl_file_path = 'HumanEvalPlus.jsonl'
    txt_file_path = 'HumanEvalPlus.txt'
    jsonl_to_txt(jsonl_file_path, txt_file_path)