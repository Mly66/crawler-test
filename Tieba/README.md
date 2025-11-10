# 百度贴吧综合分析项目 

本项目是一个集爬虫、数据清洗、统计分析、可视化与机器学习于一体的综合系统，自动采集百度贴吧多个分区数据，并进行深入分析与分类预测，帮助用户理解贴吧生态与内容分布。

---

## 🚀 功能模块

### 🕷️ 数据采集（Scrapy）

- 支持 8 个贴吧分类（音乐、游戏、体育、地区、动漫、小说、明星、社会）
- 自动爬取吧名、关注人数、帖子数、简介、所属类型
- 输出为结构化 Excel 文件：`Tieba_output.xlsx`

### 📊 数据分析（pandas）

- 分区统计贴吧数量、关注人数、帖子数
- 计算人均发帖数与比例分布
- 输出分析结果为：`统计结果_比例.xlsx`

### 📈 可视化展示（matplotlib + seaborn）

- 箱线图：贴吧关注人数与帖子数区间分布
- 柱状图：各类型人均发帖数
- 饼图：各类型关注人数与帖子数比例
- 热力图：分类准确率与混淆矩阵

### 🤖 机器学习分类（scikit-learn）

- 使用 TF-IDF 向量化贴吧简介文本
- 使用朴素贝叶斯进行多分类预测
- 输出准确率、混淆矩阵与分类报告
- 支持类别两两组合分类准确率分析与热力图展示

---

## 🛠️ 使用方法

### 1️⃣ 安装依赖

```bash
conda create -n tieba_insight python=3.10
conda activate tieba_insight
pip install scrapy pandas matplotlib seaborn scikit-learn jieba openpyxl
```
### 2️⃣ 运行爬虫
```bash
scrapy crawl life
```
输出结果将保存在 data/Tieba_output.xlsx

### 3️⃣ 分析数据
```bash
python analyse/proportion_analysis.py
```
输出分析结果为 data/统计结果_比例.xlsx

### 4️⃣ 可视化展示
```bash
python analyse/visualization.py、
```
自动生成箱线图、柱状图、饼图等图表

### 5️⃣ 机器学习分类
```bash
python ml/classifier.py
python ml/pairwise_analysis.py
```
输出分类准确率、混淆矩阵与类别对比热力图

示例图表

📦 贴吧关注人数与帖子数箱线图

🧱 各类型人均发帖数柱状图

🥧 各类型比例饼图

🔥 分类准确率热力图
