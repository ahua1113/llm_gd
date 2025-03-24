import matplotlib.pyplot as plt
import numpy as np


def plot_radar_chart(scores):
    labels = ['健壮性', '可维护性', '综合']
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)

    # 示例数据（Copilot vs CodeGeeX）
    # TODO: 这里应当是实际的测评结果
    values = {'Copilot': [0.8, 0.7, 0.76], 'CodeGeeX': [0.4, 0.3, 0.36]}

    for model, data in values.items():
        ax.plot(angles, data, label=model)
        ax.fill(angles, data, alpha=0.1)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    plt.legend(loc='upper right')
    plt.savefig("result_radar.png")


# 生成可视化报告
plot_radar_chart()