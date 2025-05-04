# 写新的日志
from qsim.widgets import QSimLayout
import os


def writeLogNew(current_file):
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取根目录
    # root_dir = os.path.dirname(current_dir)
    # 构建日志文本结果目录路径
    log_dir = os.path.join(current_dir, '日志结果-new')
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        # 构建完整的文件路径
        file_path = os.path.join(log_dir, current_file + '.txt')

        logs = QSimLayout._logs
        # print(logs)

        with open(file_path, 'w', encoding='utf-8') as file:
            for log in logs:
                file.write(str(log) + '\n')
        print(f"日志已成功写入 {file_path} 文件。")
    except Exception as e:
        print(f"写入日志到文件时出现错误: {e}")


