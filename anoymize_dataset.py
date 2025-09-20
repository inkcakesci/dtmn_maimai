import pandas as pd

# 读取原始清洗后的数据集
df = pd.read_csv("dataset_clean.csv",
                 parse_dates=["player_birthday", "submit_datatime"])

# 1. 时间 & 年龄衍生
df["birth_year"]  = df["player_birthday"].dt.year.astype("Int64")
df["submit_date"] = df["submit_datatime"].dt.date

# 如需：可把 Question2 (“进步最快的那一年”) 按 3 岁分段
# df["q2_bin"] = pd.cut(df["Question2"], bins=[0,12,15,18,21,30],
#                       labels=["<=12","13-15","16-18","19-21","22+"])

# 2. 删除直接或高风险标识符
cols_to_drop = [
    "player_name",
    "player_birthday",
    "submit_datatime",
    "Question3"       # 若需保留可做关键词脱敏或人工审核
]
df_anonym = df.drop(columns=cols_to_drop)

# 3. 导出公开数据
df_anonym.to_csv("dataset_public.csv", index=False)

print("✅ 公开数据集已生成：dataset_public.csv")
