import pandas as pd
from pathlib import Path
import sys

INPUT_CSV = Path("dataset_clean.csv")

def main():
    # 1. 读入
    try:
        df = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        sys.exit(f"[ERROR] 找不到文件：{INPUT_CSV.resolve()}")

    # 2. 过滤
    total_before = len(df)
    df_filtered = df[df["player_rating"] >= 11000].copy()
    total_after = len(df_filtered)
    removed = total_before - total_after

    print(f"[INFO] 原始记录：{total_before} 条")
    print(f"[INFO] 删除低于 11000 分的玩家：{removed} 条")
    print(f"[INFO] 保留记录：{total_after} 条")

    # 3. 覆盖写回
    df_filtered.to_csv(INPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"[OK] 已覆盖保存至 {INPUT_CSV}")

if __name__ == "__main__":
    main()