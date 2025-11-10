import pandas as pd

# 首先读取Excel文件并进行数据预处理
df = pd.read_excel(r'G:\Py2025\1110\Tieba-IntegratedAnalysis\Tieba_finalWork\Tieba_output.xlsx')
df = df[(df['关注人数'].notna()) & (df['帖子数'].notna()) & (df['关注人数'] > 0) & (df['帖子数'] > 0)]

# 按类型划分数据集
type_groups = df.groupby('类型')

# 用于存放
result_list = []
p_result_list = []

# 定义量级区间和标签
follower_bins = [0, 10000, 100000, 1000000, float('inf')]
post_bins = [0, 10000, 100000, 1000000, float('inf')]
follower_labels = ['<10000', '10000-100000', '100000-1000000', '>1000000']
post_labels = ['<10000', '10000-100000', '100000-1000000', '>1000000']

# 遍历每个类型的数据集
for type_name, group in type_groups:
    # 计算关注人数和帖子数的范围
    followers_range = (group['关注人数'].min(), group['关注人数'].max())
    posts_range = (group['帖子数'].min(), group['帖子数'].max())

    # 使用pd.cut函数根据定义的区间对关注人数和帖子数进行分组
    # include_lowest=True 参数确保最小值被包含在第一个区间内
    follower_cut = pd.cut(group['关注人数'], bins=follower_bins, labels=follower_labels, include_lowest=True)
    post_cut = pd.cut(group['帖子数'], bins=post_bins, labels=post_labels, include_lowest=True)

    # 统计每个区间内的贴吧数量，reindex保证所有标签都在结果中，即使某些区间的计数为0
    follower_counts = follower_cut.value_counts()
    post_counts = post_cut.value_counts()
    # 统计每个类型的贴吧数
    tieba_count = len(group)
    total_followers = group['关注人数'].sum()  # 关注人数总和
    total_posts = group['帖子数'].sum()  # 帖子数总和

    # 计算比例
    proportion_row = {
        '类型': type_name,
        '关注人数区间': followers_range,
        '发帖数量区间': posts_range,
        '关注<10000比例': follower_counts['<10000'] / tieba_count,
        '关注10000-100000比例': follower_counts['10000-100000'] / tieba_count,
        '关注100000-1000000比例': follower_counts['100000-1000000'] / tieba_count,
        '关注>1000000比例': follower_counts['>1000000'] / tieba_count,
        '帖子<10000比例': post_counts['<10000'] / tieba_count,
        '帖子10000-100000比例': post_counts['10000-100000'] / tieba_count,
        '帖子100000-1000000比例': post_counts['100000-1000000'] / tieba_count,
        '帖子>1000000比例': post_counts['>1000000'] / tieba_count,
        '贴吧数': tieba_count,
        '平均人均发帖数': total_posts / total_followers if total_followers > 0 else 0  # 计算人均发帖数
    }
    p_result_list.append(proportion_row)

# 创建最终的DataFrame
proportion_df = pd.DataFrame(p_result_list)

# 输出到Excel
proportion_df.to_excel(r'G:\Py2025\1110\Tieba-IntegratedAnalysis\Tieba_finalWork\统计结果_比例.xlsx', index=False)

# 打印完整的结果
print("比例统计结果：")
print(proportion_df)

# 选择类型和平均人均发帖数，并进行降序排序
average_posts_df = proportion_df[['类型', '平均人均发帖数']]
average_posts_sorted = average_posts_df.sort_values(by='平均人均发帖数', ascending=False)

# 打印降序排序的结果
print("\n降序排序的类型和平均人均发帖数：")
print(average_posts_sorted)