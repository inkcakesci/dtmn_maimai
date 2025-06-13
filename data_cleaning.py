#!/usr/bin/env python3
# coding: utf-8
"""
analysis.py
-----------

EDA + 回归分析：
  • rating ~ 练习量（play_time_month, play_count）
  • 加入年龄相关变量，检验“天赋”假说

运行：
  python analysis.py
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
from dateutil.relativedelta import relativedelta

DATA_FILE = Path("dataset_clean.csv")
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

# ----------------------------------------------------------------------
# 1. 读取 & 特征工程
# ----------------------------------------------------------------------
df = pd.read_csv(DATA_FILE, parse_dates=["submit_datatime", "player_birthday"])

# 确保两列都是真正的 datetime64[ns]
df["submit_datatime"]  = pd.to_datetime(df["submit_datatime"])
df["player_birthday"]  = pd.to_datetime(df["player_birthday"])

# ① 当前年龄（年）
df["current_age_years"] = (
        (df["submit_datatime"] - df["player_birthday"]).dt.days / 365.25
)

# ② 练习时长（年）
df["play_time_years"]  = df["play_time_month"] / 12.0

# ③ 首次游玩年龄
df["start_age_years"]  = df["current_age_years"] - df["play_time_years"]

# 简单检查
print("\n=== 样本规模 & 缺失情况 ===")
print(df.info(show_counts=True))

# ----------------------------------------------------------------------
# 2. 描述性统计 & 相关系数
# ----------------------------------------------------------------------
desc = df[[
    "player_rating", "current_age_years", "start_age_years",
    "play_time_years", "play_count"
]].describe().T
print("\n=== 描述性统计 ===")
print(desc.round(2))

corr = df[[
    "player_rating", "current_age_years", "start_age_years",
    "play_time_years", "play_count"
]].corr(method="pearson")
print("\n=== 皮尔逊相关矩阵 ===")
print(corr.round(3))

# 热图保存
plt.figure(figsize=(6, 4))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "correlation_matrix.png", dpi=300)
plt.close()

# ----------------------------------------------------------------------
# 3. 可视化示例
# ----------------------------------------------------------------------
# rating vs start_age
sns.scatterplot(data=df, x="start_age_years", y="player_rating", alpha=0.6)
sns.regplot(
    data=df, x="start_age_years", y="player_rating",
    scatter=False, color="red", ci=None
)
plt.xlabel("Start Age (years)")
plt.ylabel("Player Rating")
plt.title("Rating vs. Start Age")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "rating_vs_start_age.png", dpi=300)
plt.close()

# rating vs play_time_years
sns.scatterplot(data=df, x="play_time_years", y="player_rating", alpha=0.6)
sns.regplot(
    data=df, x="play_time_years", y="player_rating",
    scatter=False, color="red", ci=None
)
plt.xlabel("Play Time (years)")
plt.ylabel("Player Rating")
plt.title("Rating vs. Play Time")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "rating_vs_play_time.png", dpi=300)
plt.close()

print(f"\n[OK] 可视化已输出到 {PLOTS_DIR}/")

# ----------------------------------------------------------------------
# 4. 回归模型
# ----------------------------------------------------------------------
# 模型 0：仅练习量
model0 = smf.ols(
    "player_rating ~ play_time_years + play_count",
    data=df
).fit()

# 模型 1：加入年龄项（当前年龄 & 首次游玩年龄），并加二次项捕捉非线性
model1 = smf.ols(
    """player_rating ~ play_time_years + play_count
                     + current_age_years + I(current_age_years**2)
                     + start_age_years""",
    data=df
).fit()

print("\n=== 回归结果（模型 0）===\n")
print(model0.summary())

print("\n=== 回归结果（模型 1, 加入年龄）===\n")
print(model1.summary())

# ----------------------------------------------------------------------
# 5. 结果汇总表
# ----------------------------------------------------------------------
def tidy(sm_res, model_name, y, index_name="player_rating"):
    """
    把 statsmodels 结果整理成 DataFrame，并计算标准化系数 β*
    β* = b * (SD_x / SD_y)，其中 SD_x 来自设计矩阵本身，避免解析失败
    """
    exog_df = pd.DataFrame(
        sm_res.model.exog, columns=sm_res.model.exog_names
    )
    sd_y = y.std()

    rows = []
    for term in sm_res.params.index:
        b       = sm_res.params[term]
        pval    = sm_res.pvalues[term]
        se      = sm_res.bse[term]

        # 拿 exog 里的列直接算 SD_x；Intercept 不算 β*
        beta_std = (
            np.nan if term == "Intercept"
            else b * (exog_df[term].std() / sd_y)
        )

        rows.append(
            {"model": model_name, "term": term, "b": b,
             "beta_std": beta_std, "p": pval, "std_err": se}
        )

    return pd.DataFrame(rows)

# ---------- 调用 ----------
out = pd.concat([
    tidy(model0, "Model0", df["player_rating"]),
    tidy(model1, "Model1", df["player_rating"])
])

# ----------------------------------------------------------------------
# 6. 增益评估
# ----------------------------------------------------------------------
r2_base = model0.rsquared
r2_age = model1.rsquared
delta_r2 = r2_age - r2_base
print(f"\n=== 模型解释力提升 ===")
print(f"R²_base = {r2_base:.3f}")
print(f"R²_age  = {r2_age:.3f}")
print(f"ΔR²     = {delta_r2:.3f}  (年龄变量带来新增解释方差)")

print("\n全部完成，祝你分析顺利！")
