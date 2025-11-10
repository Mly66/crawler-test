import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from itertools import combinations

plt.rcParams['font.sans-serif'] = ['SimHei']
# 读取数据和数据预处理
combined_df = pd.read_excel(r'G:\Py2025\1110\Tieba-IntegratedAnalysis\Tieba_finalWork\Tieba_output.xlsx')
combined_df.dropna(subset=['简介'], inplace=True)
# 打乱数据集，并重置索引
combined_df = combined_df.sample(frac=1).reset_index(drop=True)

# 确定特征值和结果
X = combined_df['简介']
y = combined_df['类型']


# 文本预处理：分词
def preprocess_text(text):
    return " ".join(jieba.cut(text))


X = X.apply(preprocess_text)

# 使用TF-IDF向量化文本数据，将文本转化为数值型特征矩阵
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# 训练模型和预测，这里用贝叶斯分类器
clf = MultinomialNB()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# 输出准确度
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# 使用sklearn自带函数输出混淆矩阵
cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)

# 绘制混淆矩阵热图
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=clf.classes_, yticklabels=clf.classes_)
plt.ylabel('真实值')
plt.xlabel('预测值')
plt.title('混淆矩阵热力图')
plt.show()

# 打印详细的分类报告
print("\n分类报告:")
print(classification_report(y_test, y_pred, target_names=clf.classes_))

# 分类，使用combination把类型两两排列组合
categories = y.unique()
category_combinations = list(combinations(categories, 2))
accuracy_results = []

# 遍历每一对类别
for cat1, cat2 in category_combinations:
    subset_df = combined_df[combined_df['类型'].isin([cat1, cat2])]

    # 对选定的子集重复之前的数据预处理和模型训练步骤
    X_subset = subset_df['简介'].apply(preprocess_text)
    y_subset = subset_df['类型']

    vectorizer = TfidfVectorizer()
    X_subset_tfidf = vectorizer.fit_transform(X_subset)

    X_train, X_test, y_train, y_test = train_test_split(
        X_subset_tfidf, y_subset, test_size=0.3, random_state=42, stratify=y_subset)

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    accuracy_results.append(((cat1, cat2), accuracy))

# 按照准确率降序排序
accuracy_results.sort(key=lambda x: x[1], reverse=True)

# 打印结果
print("Pairwise Classification Accuracy:")
for (cat1, cat2), acc in accuracy_results:
    print(f"{cat1} vs {cat2}: {acc:.2f}")

# 创造一个和热力图配对的矩阵
num_categories = len(categories)
accuracy_matrix = np.zeros((num_categories, num_categories))

# 把前面预测出来的数都填到集合中
category_to_index = {category: i for i, category in enumerate(categories)}
for (cat1, cat2), acc in accuracy_results:
    idx1, idx2 = category_to_index[cat1], category_to_index[cat2]
    accuracy_matrix[idx1, idx2] = acc
    accuracy_matrix[idx2, idx1] = acc  # 对称填充整个热力图
# 同类的没有数值
np.fill_diagonal(accuracy_matrix, np.nan)

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(accuracy_matrix, annot=True, fmt='.2f', cmap="Blues",
            xticklabels=categories, yticklabels=categories,
            cbar_kws={'label': 'Accuracy'}, square=True,
            annot_kws={"size": 8})  # 调整注释文字大小以便更好显示
plt.title('两两类别的热力图')
plt.tight_layout()  # 填充整个图像区域
plt.show()