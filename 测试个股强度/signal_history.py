import pandas as pd
from utils import *
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.expand_frame_repr", False)

from backtest import (
    backtest_one_stock,
    load_stock_data,
)


def get_stock_signal(
    code,
    stock_name,
    buy_price,
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

    latest_price = float(
        df.iloc[-1]["1455"]
    )

    current_profit = (
        latest_price / buy_price - 1
    ) * 100

    return {

        "股票代码": code,

        "股票名称": stock_name,

        "开仓日期": open_date,

        "买入价": round(
            buy_price,
            3,
        ),

        "最新价": round(
            latest_price,
            3,
        ),

        "当前收益%": round(
            current_profit,
            2,
        ),

        # 直接使用回测结果
        "股票类型":
            result["股票类型"],

        "突破幅度":
            result.get(
                "突破幅度",
                None
            ),

        "预计卖出日期":
            result["卖出日期"],

        "预计卖出时间":
            result["卖出时间"],

        "预计卖出价":
            result["卖出价"],

    }


def get_stock_signals(
    positions,
):

    results = []

    for (
        code,
        stock_name,
        buy_price,
        open_date,
    ) in positions:

        results.append(

            get_stock_signal(
                code,
                stock_name,
                buy_price,
                open_date,
            )

        )

    return pd.DataFrame(
        results
    )


if __name__ == "__main__":

    full_code, stock_name = (
        get_full_code_and_name(
            "001359"
        )
    )
    positions = [

        (
            full_code,
            stock_name,
            125,
            "2026-06-23",
        ),

        (
            "SZ002068",
            "黑猫股份",
            12.65,
            "2026-06-23",
        ),

        (
            "SZ301150",
            "中一科技",
            48.50,
            "2026-06-18",
        ),

    ]

    result_df = get_stock_signals(
        positions
    )

    print()
    print(result_df)
    print()