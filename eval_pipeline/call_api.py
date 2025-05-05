import os

from openai import OpenAI
from volcenginesdkarkruntime import Ark


# 豆包模型
def doubao_code(problem: str) -> str:
    client = Ark(api_key="fee2d098-39e0-4598-97e5-ae67e4fd0143", base_url="https://ark.cn-beijing.volces.com/api/v3",)

    response = client.chat.completions.create(
        model="doubao-1-5-pro-32k-250115",
        messages=[{
            "role": "user",
            "content": f"""
            请严格使用qsim.widgets组件库构建界面，要求：
            1. 类定义必须继承自QSimWidget
            2. 包含if __name__ == '__main__'启动代码
            3. 回复中只包含代码，不要有多余的文字
            4. 最后循环启动，不需要退出返回码即用app.exec_()而非sys.exit(app.exec_())
            具体需求：{problem}
            """}],
        temperature=0.1,
        max_tokens=1500
    )

    # 去掉第一行和最后一行（多余的文字或符号）
    res = response.choices[0].message.content
    # res = res.split('\n', 1)[1].rsplit('\n', 1)[0]

    return res


# deepseek模型
def deepseek_code(problem: str) -> str:
    client = OpenAI(api_key="sk-62fc293a798e4a6d80f9696d6de0ef35", base_url="https://api.deepseek.com")

    # 代码末尾循环启动，不需要退出返回码
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{
            "role": "user",
            "content": f"""
            请严格使用qsim.widgets组件库构建界面，要求：
            1. 类定义必须继承自QSimWidget
            2. 包含if __name__ == '__main__'启动代码
            3. 回复中只包含代码，不要有多余的文字
            4. 最后循环启动，不需要退出返回码即用app.exec_()而非sys.exit(app.exec_())
            具体需求：{problem}
            """}],
        temperature=0.1,
        max_tokens=1500
    )

    res = response.choices[0].message.content

    # 去掉第一行和最后一行（多余的文字或符号）
    res = res.split('\n', 1)[1].rsplit('\n', 1)[0]

    return res


# 通义千问模型
def tongyi_code(problem: str) -> str:
    client = OpenAI(api_key="sk-6ba774ea4bf7413c807028e765123481", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    # 代码末尾循环启动，不需要退出返回码
    response = client.chat.completions.create(
        model="qwq-plus",
        messages=[{
            "role": "user",
            "content": f"""
            请严格使用qsim.widgets组件库构建界面，要求：
            1. 类定义必须继承自QSimWidget
            2. 包含if __name__ == '__main__'启动代码
            3. 回复中只包含代码，不要有多余的文字
            4. 最后循环启动，不需要退出返回码即用app.exec_()而非sys.exit(app.exec_())
            具体需求：{problem}
            """}],
        temperature=0.1,
        max_tokens=1500
    )

    res = response.choices[0].message.content

    return res
    

# 取问题集
def get_problem():
    file_path = r'f:\桌面\llm_gd\data\QUI-old.txt'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 分割问题
            problems = []
            lines = content.split('\n')
            problem_start = False
            current_problem = ""
            for line in lines:
                if line.startswith('Q') and '/' in line:
                    if current_problem:
                        problems.append(current_problem.strip())
                    current_problem = line + '\n'
                    problem_start = True
                elif problem_start:
                    current_problem += line + '\n'
            if current_problem:
                problems.append(current_problem.strip())
            return problems
    except FileNotFoundError:
        print(f"未找到文件: {file_path}")
        return []


# 将生成的代码写入文件，如果文件已存在，则在末尾添加内容
def write_code_to_file(code, file_path):
    with open(file_path, 'a', encoding='utf-8') as file:  # 使用'a'模式以追加方式写入
        file.write(code + '\n')  # 写入代码并换行
        print(f"代码已写入文件: {file_path}")


if __name__ == '__main__':
    problems = get_problem()  # 从题库获取问题描述
    # for problem in problems:
    # print(problem)
    # generated_code = deepseek_code(problem)

    problem = problems[1]
    print(problem)

    q1_code_result = doubao_code(problem)

    # 将生成的代码写入文件
    write_code_to_file(q1_code_result, 'res.txt')
