import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)

# 显示所有行
pd.set_option('display.max_rows', None)

# 不限制显示宽度
pd.set_option('display.width', None)

# 每列最大显示长度
pd.set_option('display.max_colwidth', None)

# 不自动换行
pd.set_option('display.expand_frame_repr', False)
from config import *
from backtest import (
    backtest_one_stock,
    load_stock_data,
)


def get_live_signal(
    code,
    stock_name,
    open_date,
):

    result = backtest_one_stock(
        code=code,
        stock_name=stock_name,
        open_date=open_date,
    )

    if result is None:

        return {
            "股票代码": code,
            "股票名称": stock_name,
            "状态": "失败",
        }

    if result == "LIMIT_UP":

        return {
            "股票代码": code,
            "股票名称": stock_name,
            "状态": "涨停买不进",
        }

    if result == "SKIP_STRONG":

        return {
            "股票代码": code,
            "股票名称": stock_name,
            "状态": "强势股过滤",
        }

    df = load_stock_data(code)

    if df is None:

        return {
            "股票代码": code,
            "股票名称": stock_name,
            "状态": "无数据",
        }

    open_date = pd.to_datetime(
        open_date
    ).strftime("%Y-%m-%d")

    trade_days = df["交易日期"].tolist()

    try:

        buy_idx = trade_days.index(
            open_date
        )

    except:

        return {
            "股票代码": code,
            "股票名称": stock_name,
            "状态": "找不到开仓日期",
        }

    buy_price = result["买入价"]

    stock_type = result["股票类型"]

    today_row = df.iloc[-1]

    current_price = float(
        today_row[BUY_TIME]
    )

    current_date = (
        today_row["交易日期"]
    )

    current_profit = (
        current_price / buy_price - 1
    ) * 100

    trade_hold_days = (
        len(df) - 1 - buy_idx
    )

    target_price = None

    drawdown_price = None

    highest_price = None

    # ======================
    # 强势股
    # ======================

    if stock_type == "强势":

        target_price = round(
            buy_price
            * (1 + STRONG_TAKE_PROFIT),
            3,
        )

    # ======================
    # 趋势股
    # ======================

    else:

        highest_price = max(

            df.iloc[
                buy_idx:
            ][BUY_TIME].astype(float)

        )

        drawdown_price = round(

            highest_price
            * (
                1
                - DRAWDOWN_RATIO
            ),

            3,
        )

    return {

        "股票代码": code,

        "股票名称": stock_name,

        "股票类型": stock_type,

        "开仓日期": open_date,

        "预计卖出日期":
            result["卖出日期"],

        "预计卖出时间":
            result["卖出时间"],

        "预计卖出价":
            result["卖出价"],

        "当前日期": current_date,

        "持仓交易日": trade_hold_days,

        "买入价": round(
            buy_price,
            3,
        ),

        "当前价": round(
            current_price,
            3,
        ),

        "当前收益%": round(
            current_profit,
            2,
        ),

        "目标价": target_price,

        "历史最高价": highest_price,

        "趋势回撤价": drawdown_price,

        "状态": (
            "已卖出"
            if result["卖出日期"]
            <= current_date
            else "持有中"
        ),
    }


def get_live_signals(
    positions,
):

    results = []

    for (
        code,
        stock_name,
        open_date,
    ) in positions:

        results.append(

            get_live_signal(
                code,
                stock_name,
                open_date,
            )

        )

    return pd.DataFrame(
        results
    )


if __name__ == "__main__":

    positions = [

        (
            "SZ300067",
            "安诺其",
            "2026-05-06",
        ),

        (
            "SZ001359",
            "平安电工",
            "2026-06-22",
        ),

        (
            "SZ002068",
            "黑猫股份",
            "2026-06-22",
        ),

    ]

    df = get_live_signals(
        positions
    )

    print()

    print(df)

    print()