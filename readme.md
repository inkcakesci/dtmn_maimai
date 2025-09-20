
# 起步年龄是否影响音乐游戏表现？——以《舞萌DX》为例

[❤点我前往ipynb的结论界面❤](https://inkcakesci.github.io/dtmn_maimai/)

> **TL;DR**  
> 基于 n=347 份有效样本，在控制总游玩次数与练习时长后，**更早的入坑年龄（start_age）与更高的 DX rating 仍显著相关**（非线性、边际递减）。练习量（play_count）是最大解释因子，但年龄相关变量（start_age、current_age）保留独立贡献。针对活跃玩家总体（≈5.16 万），95% 抽样误差约 **±5.23%**。

---

## 1. 项目概览

- **研究问题**：年龄是否对街机音乐游戏表现（DX rating）具有独立影响？  
- **数据来源**：线上问卷 + 机台公开榜单。共收集 397 份，随机抽取并清洗后得到 **347 份**有效样本。  
- **主要方法**：描述统计、分段/对数可视化、逐步 OLS（含交互）、随机森林与 XGBoost（置换重要度、TreeSHAP），5 折交叉验证报告 \(R^2\)。  
- **核心结论**：练习投入是首要因素；在其控制下，**入坑更早**（start_age 越小）与更高表现相关，**current_age** 亦存在次级但稳健的负向效应；“2 年左右达平台期”的指数饱和现象明显。

---

## 2. 仓库结构

```

dtmn\_maimai/
├─ document/                    # 已废弃：论文/报告（docx / pdf）
├─ plots/                       # 导出的图
├─ analysis.ipynb               # 主分析 Notebook
├─ analysis.html                # 导出的 HTML 报告
├─ anonymize_dataset.py         # 脱敏脚本
├─ dataset\_public.csv           # 脱敏后的公开数据（发布用）
├─ requirements.txt             # 环境依赖
└─ temp.py                      # 临时脚本/试验代码

````

> **数据隐私**：公开数据已脱敏（生日精度降至“年”，去除可识别字段；过滤极低活跃用户，保持口径一致）。

---

## 3. 关键结果（摘录）

* **可视化**

    * `fig2.png`：Rating vs 入坑年龄（LOESS 平滑）；
    * `fig3.png`：按游玩次数分级 + OLS；
    * `fig4.png`：Rating vs 游玩时间（指数饱和拟合）；
    * `fig5.png`：对数处理（log10）后的线性趋势；
* **回归**

    * 加入 `start_age`、`current_age` 后，模型解释力 $\Delta R^2$ 有显著提升；
    * `start_age × play_count` 交互显著为负，表明“越早入坑 + 高投入”的组合增益更明显；
* **特征重要度**

    * 置换重要度（RF/XGB）与 TreeSHAP 一致指向：`play_count` 贡献最大；`start_age`、`current_age` 保留稳定的次级影响。

> 详细表格与区间见论文正文与 `analysis.ipynb`。

---

## 4. 许可

* **代码**：MIT（建议保留作者署名）
* **数据**：CC BY-NC 4.0（署名-非商用）
* **如何跑代码？** 因为数据已经脱敏，我并不提供原始dataset，如果你有需要，请联系我trotyls@outlook.com

---

## 5. 致谢

感谢舞萌社群以及所有参与问卷的玩家与社群.
