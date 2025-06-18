import pandas as pd
from pathlib import Path

RAW_FILE  = Path("dataset_raw.xlsx")      # 输入文件
CLEAN_XLS = Path("dataset_clean.xlsx")    # 输出 Excel
CLEAN_CSV = Path("dataset_clean.csv")     # 输出 CSV

def main():
    # 读取
    df = pd.read_excel(RAW_FILE)

    # ---- 1. play_time_month：年→月 ----
    if "play_time_month" not in df.columns:
        raise SystemExit("列 'play_time_month' 不存在，请检查列名。")
    df["play_time_month"] = (df["play_time_month"] * 12).round().astype("Int64")

    # ---- 2. Question1 映射 ----
    if "Question1" not in df.columns:
        raise SystemExit("列 'Question1' 不存在，请检查列名。")
    q1_map = {"是": 1, "否": 2, "存在，但不重要": 3}
    df["Question1"] = df["Question1"].map(q1_map).astype("Int64")

    # 如有未映射值，警告
    if df["Question1"].isna().any():
        unmapped = df.loc[df["Question1"].isna(), "Question1"].unique()
        print(f"[WARN] 以下 Question1 值未映射: {unmapped}")

    # 保存
    df.to_excel(CLEAN_XLS, index=False)
    df.to_csv(CLEAN_CSV, index=False, encoding="utf-8-sig")
    print(f"[OK] 清洗完成，已保存 {CLEAN_XLS} / {CLEAN_CSV}")

if __name__ == "__main__":
    main()