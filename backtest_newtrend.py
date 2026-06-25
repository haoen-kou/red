import pandas as pd

from config import *
from 策略.strategy import should_sell
from pattern.强势和趋势测试 import get_pattern_signal
from config import ENABLE_TREND_FILTER
from utils import load_stock_data


# ==========================================
# 涨停判断
# ==========================================

def get_limit_pct(code):

    stock_num = code[2:]

    if stock_num.startswith(("30", "688")):
        return 20

    if stock_num.startswith(("83", "87", "92")):
        return 30

    return 10


def is_limit_up(
    code,
    buy_price,
    prev_price,
):

    change_pct = (
        buy_price / prev_price - 1
    ) * 100

    limit_pct = get_limit_pct(code)

    return (
        change_pct
        >= limit_pct * LIMIT_RATIO
    )


# ==========================================
# 单只股票回测
# ==========================================

def backtest_one_stock(
    code,
    stock_name,
    open_date,
):

    df = load_stock_data(code)

    if df is None:
        return None

    buy_row = df[
        df["交易日期"] == open_date
    ]

    if buy_row.empty:
        return None

    trade_days = df["交易日期"].tolist()

    try:

        buy_idx = trade_days.index(
            open_date
        )

    except:

        return None

    try:

        buy_price = float(
            buy_row.iloc[0][BUY_TIME]
        )

    except:

        return None

    # ==========================
    # 涨停过滤
    # ==========================

    if buy_idx > 0:

        try:

            prev_price = float(
                df.iloc[
                    buy_idx - 1
                ][COMPARE_TIME]
            )

            if is_limit_up(
                code,
                buy_price,
                prev_price,
            ):
                return "LIMIT_UP"

        except:

            return None

    # ==========================
    # 判断趋势股
    # ==========================

    breakout_pct = None
    pattern_score = None

    if not ENABLE_TREND_FILTER:

        is_trend = True

    else:

        try:

            pattern = get_pattern_signal(
                code[2:],  # 去掉SZ/SH/BJ
                open_date,
            )

            pattern_score = pattern["评分"]

            # 只有真正趋势股走趋势策略
            is_trend = (
                    pattern["模式"] == "趋势股"
            )

        except:

            is_trend = True

    # 不做强势股

    if (
            not ENABLE_STRONG_STOCK
            and not is_trend
    ):
        return "SKIP_STRONG"

    # ==========================
    # 卖出逻辑
    # ==========================

    sell_price = None
    sell_date = None
    sell_time = None

    # =====================================
    # 趋势股
    # =====================================

    if is_trend:

        for i in range(
                buy_idx + 1,
                len(df),
        ):

            try:

                if should_sell(
                        df,
                        buy_idx,
                        i,
                        buy_price,
                        BUY_TIME,
                        COMPARE_TIME,
                ):
                    sell_price = float(
                        df.iloc[i][BUY_TIME]
                    )

                    sell_date = (
                        df.iloc[i]["交易日期"]
                    )

                    break

            except:

                continue

    # =====================================
    # 强势股
    # =====================================

    else:

        take_profit_price = (
                buy_price
                * (
                        1 + STRONG_TAKE_PROFIT
                )
        )

        time_cols = [
            c for c in df.columns
            if c.isdigit()
        ]

        for i in range(
                buy_idx + 1,
                len(df),
        ):
            if (
                    STRONG_MAX_HOLD_DAYS > 0
                    and i - buy_idx >= STRONG_MAX_HOLD_DAYS
            ):
                sell_price = float(
                    df.iloc[i][BUY_TIME]
                )

                sell_date = (
                    df.iloc[i]["交易日期"]
                )

                break

            sold = False

            day_row = df.iloc[i]

            for t in time_cols:

                try:

                    price = float(
                        day_row[t]
                    )

                except:

                    continue

                if price >= take_profit_price:
                    sell_price = price

                    sell_date = (
                        day_row["交易日期"]
                    )
                    sell_time = t
                    sold = True

                    break

            if sold:
                break

    # ==========================
    # 最后一天还没卖
    # ==========================

    if sell_price is None:

        try:

            sell_price = float(
                df.iloc[-1][BUY_TIME]
            )

            sell_date = (
                df.iloc[-1]["交易日期"]
            )
            sell_time = BUY_TIME
        except:

            return None

    profit_pct = (
        sell_price / buy_price - 1
    ) * 100

    profit_money = (
        POSITION_SIZE
        * profit_pct
        / 100
    )

    hold_days = (
        pd.to_datetime(sell_date)
        - pd.to_datetime(open_date)
    ).days

    return {

        "股票代码": code,

        "股票名称": stock_name,

        "股票类型": (
            "趋势"
            if is_trend
            else "强势"
        ),

        "评分": pattern_score,

        "开仓日期": open_date,

        "卖出日期": sell_date,
        "卖出时间": sell_time,
        "持仓天数": hold_days,

        "买入价": round(
            buy_price,
            3,
        ),

        "卖出价": round(
            sell_price,
            3,
        ),

        "收益率%": round(
            profit_pct,
            2,
        ),

        "盈利金额": round(
            profit_money,
            2,
        ),
    }


# ==========================================
# 单月回测
# ==========================================

def backtest_one_month(
    trade_file,
):

    print(
        f"\n开始回测 {trade_file.name}"
    )

    df_trade = pd.read_csv(
        trade_file,
        sep="\t",
        encoding="gb18030",
    )

    results = []

    limit_count = 0

    for _, row in df_trade.iterrows():

        code = str(
            row["代码"]
        ).strip().upper()

        stock_name = str(
            row["    名称"]
        ).strip()

        open_date = pd.to_datetime(
            row["buy"]
        ).strftime("%Y-%m-%d")

        result = backtest_one_stock(
            code,
            stock_name,
            open_date,
        )

        if result == "LIMIT_UP":

            limit_count += 1

            continue

        if result == "SKIP_STRONG":
            continue

        if result:

            results.append(
                result
            )

    result_df = pd.DataFrame(
        results
    )

    return result_df, limit_count