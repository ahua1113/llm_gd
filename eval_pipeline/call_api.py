import os
from openai import OpenAI


# 豆包模型
def doubao_code(problem: str) -> str:
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        api_key=os.environ.get("fee2d098-39e0-4598-97e5-ae67e4fd0143"),
    )

    response = client.chat.completions.create(
        model="doubao-1-5-vision-pro-32k-250115",
        messages=[{
            "role": "user",
            "content": f"""
            请严格使用qsim.widgets组件库构建界面，要求：
            1. 类定义必须继承自QWidget
            2. 必须包含setFixedSize调用
            3. 按层级结构创建布局对象
            4. 包含if __name__ == '__main__'启动代码
    
            具体需求：{problem}
            """}],
        temperature=0.1,
        max_tokens=1500
    )

    return response.choices[0].message.content


# deepseek模型
def deepseek_code(problem: str) -> str:
    client = OpenAI(api_key="sk-62fc293a798e4a6d80f9696d6de0ef35", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{
            "role": "user",
            "content": f"""
            请严格使用qsim.widgets组件库构建界面，要求：
            1. 类定义必须继承自QSimWidget
            2. 包含if __name__ == '__main__'启动代码
            3. 回复中只包含代码，不要有多余的文字

            具体需求：{problem}
            """}],
        temperature=0.1,
        max_tokens=1500
    )

    res = response.choices[0].message.content

    # 去掉第一行和最后一行（多余的文字或符号）
    res = res.split('\n', 1)[1].rsplit('\n', 1)[0]

    return res


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


if __name__ == '__main__':
    problems = get_problem()  # 从题库获取问题描述
    # for problem in problems:
    # print(problem)
    # generated_code = deepseek_code(problem)

    problem = problems[1]
    print(problem)

    q1_code_result = deepseek_code(problem)
    print(q1_code_result)
