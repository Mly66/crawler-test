import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 读取生成的比例统计数据
proportion_df = pd.read_excel(r'G:\Py2025\1110\Tieba-IntegratedAnalysis\Tieba_finalWork\统计结果_比例.xlsx')

# 提取关注人数区间和发帖数区间的数据
attention_intervals = proportion_df['关注人数区间'].apply(lambda x: [int(i.strip('()')) for i in x.split(', ')])
post_intervals = proportion_df['发帖数量区间'].apply(lambda x: [int(i.strip('()')) for i in x.split(', ')])

# 将区间转换为列表形式
attention_data = [interval for interval in attention_intervals]
post_data = [interval for interval in post_intervals]

# 打印数据列表以检查
print("关注人数区间数据:", attention_data)
print("发帖数区间数据:", post_data)

# 绘制关注人数区间的箱线图
plt.figure(figsize=(12, 6))
plt.boxplot(attention_data, patch_artist=True)
plt.title('关注人数区间分布')
plt.ylabel('关注人数')
plt.xticks([i+1 for i in range(len(proportion_df))], proportion_df['类型'], rotation=45)
plt.show()

# 绘制发帖数区间的箱线图
plt.figure(figsize=(12, 6))
plt.boxplot(post_data, patch_artist=True)
plt.title('发帖数区间分布')
plt.ylabel('发帖数')
plt.xticks([i+1 for i in range(len(proportion_df))], proportion_df['类型'], rotation=45)
plt.show()

types = proportion_df['类型']
avg_posts = proportion_df['平均人均发帖数']
# 创建柱形图
plt.figure(figsize=(10, 6))
plt.bar(types, avg_posts, color='skyblue')

# 添加标题和轴标签
plt.title('各个类型的人均发帖数')
plt.xlabel('类型')
plt.ylabel('平均发帖数')

# 显示数值在柱子上方
for i in range(len(types)):
    plt.text(i, avg_posts[i], f'{avg_posts[i]:.2f}', ha='center', va='bottom')

# 旋转x轴标签以便更好地显示
plt.xticks(rotation=45)

# 显示图表
plt.tight_layout()
plt.show()

# 绘制饼图的函数
def plot_pie_chart(ax, data, title):
    labels = data.index
    sizes = data.values
    explode = [0.1] * len(sizes)  # 使每个部分稍微偏离中心，更好地显示

    wedges, texts, autotexts = ax.pie(
        sizes,
        explode=explode,
        labels=None,  # 不在图上直接显示标签
        autopct='%1.1f%%',
        pctdistance=0.85,  # 调整百分比标签距离
        shadow=True,
        startangle=90
    )

    # 使用图例代替标签
    ax.legend(wedges, labels,
              title="类别",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    ax.set_title(title)  # 设置图标题

# 总数和图标计数
total_plots = len(proportion_df) * 2  # 每种类型有两个饼图（关注人数和帖子数）
num_figures = 4
current_plot = 0  # 当前绘制的饼图索引

# 遍历每个类型，绘制相应的饼图
for fig_index in range(num_figures):
    # 创建新的画布和子图，2行2列
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()  # 扁平化数组以方便迭代

    for i in range(4):  # 每张图中最多4个饼图
        if current_plot >= total_plots:
            break  # 如果所有图都绘制完成，退出()

        # 获取当前行
        row_index = current_plot // 2
        is_follower = current_plot % 2 == 0  # 判断是绘制关注人数还是帖子数

        if is_follower:
            # 准备“关注人数”的数据
            follower_data = {
                '关注<10000比例': proportion_df.iloc[row_index]['关注<10000比例'],
                '关注10000-100000比例': proportion_df.iloc[row_index]['关注10000-100000比例'],
                '关注100000-1000000比例': proportion_df.iloc[row_index]['关注100000-1000000比例'],
                '关注>1000000比例': proportion_df.iloc[row_index]['关注>1000000比例'],
            }
            title = f"{proportion_df.iloc[row_index]['类型']} - 关注人数比例"
        else:
            # 准备“帖子数”的数据
            post_data = {
                '帖子<10000比例': proportion_df.iloc[row_index]['帖子<10000比例'],
                '帖子10000-100000比例': proportion_df.iloc[row_index]['帖子10000-100000比例'],
                '帖子100000-1000000比例': proportion_df.iloc[row_index]['帖子100000-1000000比例'],
                '帖子>1000000比例': proportion_df.iloc[row_index]['帖子>1000000比例'],
            }
            title = f"{proportion_df.iloc[row_index]['类型']} - 帖子数比例"
        # 绘制饼图
        data = pd.Series(follower_data if is_follower else post_data)
        plot_pie_chart(axes[i], data, title)

        # 更新当前绘制的图索引
        current_plot += 1

        # 调整子图的布局
    plt.tight_layout()

    # 显示或保存图形
    plt.show()