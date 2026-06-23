import pandas as pd
from pathlib import Path

# ==========================================
# 参数
# ==========================================

trade_file = r"C:\Users\lianghaoen\Desktop\强中强数据\Table202605.xls"

data_dir = Path(r"D:\qdata\stock-5m-close-price")

init_cash = 500000       # 初始资金
position_size = 100000   # 每次投入

# ==========================================
# 读取选股记录
# ==========================================

df_trade = pd.read_csv(
    trade_file,
    sep="\t",
    encoding="gb18030"
)

results = []

skip_limit_count = 0

# ==========================================
# 开始回测
# ==========================================

for _, row in df_trade.iterrows():

    code = str(row["代码"]).strip().upper()

    open_date = pd.to_datetime(
        row["buy"]
    ).strftime("%Y-%m-%d")

    csv_file = data_dir / f"{code.lower()}.csv"

    if not csv_file.exists():
        print(f"找不到文件: {csv_file.name}")
        continue

    try:

        df = pd.read_csv(
            csv_file,
            encoding="gb18030",
            skiprows=1
        )

    except Exception as e:

        print(code, e)
        continue

    # ==========================================
    # 清洗列名
    # ==========================================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if "交易日期" not in df.columns:
        print(f"{code} 缺少交易日期列")
        continue

    if "1430" not in df.columns:
        print(f"{code} 缺少1430列")
        continue

    if "1455" not in df.columns:
        print(f"{code} 缺少1455列")
        continue

    # ==========================================
    # 日期统一
    # ==========================================

    df["交易日期"] = pd.to_datetime(
        df["交易日期"]
    ).dt.strftime("%Y-%m-%d")

    trade_days = df["交易日期"].tolist()

    # ==========================================
    # 找买入日
    # ==========================================

    buy_row = df[
        df["交易日期"] == open_date
    ]

    if buy_row.empty:
        print(f"{code} 找不到开仓日期 {open_date}")
        continue

    try:

        buy_price = float(
            buy_row.iloc[0]["1430"]
        )

    except:
        print(f"{code} 买入价异常")
        continue

    try:

        buy_idx = trade_days.index(open_date)

    except:
        continue

    # ==========================================
    # 判断涨停买不进
    # ==========================================

    if buy_idx > 0:

        try:

            prev1455 = float(
                df.iloc[buy_idx - 1]["1455"]
            )

            open_change = (
                buy_price / prev1455 - 1
            ) * 100

            stock_num = code[2:]

            if stock_num.startswith(("30", "688")):
                limit_pct = 20

            elif stock_num.startswith(
                ("83", "87", "92")
            ):
                limit_pct = 30

            else:
                limit_pct = 10

            if open_change >= limit_pct * 0.995:

                skip_limit_count += 1

                print(
                    f"{code} "
                    f"涨停买不进 "
                    f"{open_change:.2f}%"
                )

                continue

        except:
            continue

    # ==========================================
    # 持有逻辑
    # ==========================================

    sell_price = None
    sell_date = None

    for i in range(buy_idx + 1, len(df)):

        try:

            prev1455 = float(
                df.iloc[i - 1]["1455"]
            )

            curr1430 = float(
                df.iloc[i]["1430"]
            )

        except:
            continue

        # 继续持有

        if curr1430 > prev1455:
            continue

        # 卖出

        sell_price = curr1430

        sell_date = df.iloc[i]["交易日期"]

        break

    # ==========================================
    # 最后一天仍未卖出
    # ==========================================

    if sell_price is None:

        try:

            sell_price = float(
                df.iloc[-1]["1430"]
            )

            sell_date = df.iloc[-1]["交易日期"]

        except:
            continue

    # ==========================================
    # 收益计算
    # ==========================================

    profit_pct = (
        sell_price / buy_price - 1
    ) * 100

    profit_money = (
        position_size
        * profit_pct
        / 100
    )

    hold_days = (
        pd.to_datetime(sell_date)
        - pd.to_datetime(open_date)
    ).days

    results.append({

        "股票代码": code,

        "开仓日期": open_date,

        "卖出日期": sell_date,

        "持仓天数": hold_days,

        "买入价": round(
            buy_price,
            3
        ),

        "卖出价": round(
            sell_price,
            3
        ),

        "收益率%": round(
            profit_pct,
            2
        ),

        "盈利金额": round(
            profit_money,
            2
        )

    })

# ==========================================
# 汇总结果
# ==========================================

result_df = pd.DataFrame(results)

if result_df.empty:

    print("没有产生交易结果")

else:

    final_cash = init_cash

    for _, row in result_df.iterrows():

        final_cash += row["盈利金额"]

    total_profit = (
        final_cash - init_cash
    )

    total_return = (
        total_profit
        / init_cash
        * 100
    )

    win_rate = (
        (result_df["收益率%"] > 0)
        .mean()
        * 100
    )

    print("\n========================")
    print("回测结果")
    print("========================")

    print(
        f"交易次数: {len(result_df)}"
    )

    print(
        f"涨停无法买入数量: {skip_limit_count}"
    )

    print(
        f"平均收益率: "
        f"{result_df['收益率%'].mean():.2f}%"
    )

    print(
        f"胜率: "
        f"{win_rate:.2f}%"
    )

    print(
        f"最大盈利: "
        f"{result_df['收益率%'].max():.2f}%"
    )

    print(
        f"最大亏损: "
        f"{result_df['收益率%'].min():.2f}%"
    )

    print()

    print(
        f"初始资金: "
        f"{init_cash:,.2f}"
    )

    print(
        f"最终资金: "
        f"{final_cash:,.2f}"
    )

    print(
        f"总盈利: "
        f"{total_profit:,.2f}"
    )

    print(
        f"总收益率: "
        f"{total_return:.2f}%"
    )

    output_file = "强中强1430策略回测.xlsx"

    result_df.to_excel(
        output_file,
        index=False
    )

    print()
    print(
        f"结果已保存: "
        f"{output_file}"
    )