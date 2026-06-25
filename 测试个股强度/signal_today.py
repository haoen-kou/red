import pandas as pd
from utils import *
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.expand_frame_repr", False)

from config import *
from backtest import load_stock_data


def get_stock_signal(
    code,
    stock_name,
    buy_price,
):

    df = load_stock_data(
        code.upper()
    )

    if df is None:

        return {

            "股票代码": code,

            "股票名称": stock_name,

            "状态": "无数据",

        }

    try:

        latest_date = (
            df.iloc[-1]["交易日期"]
        )

        latest_price = float(
            df.iloc[-1][COMPARE_TIME]
        )

    except:

        return {

            "股票代码": code,

            "股票名称": stock_name,

            "状态": "最新价格异常",

        }

    current_profit = (

        latest_price
        / buy_price
        - 1

    ) * 100

    breakout_pct = None

    stock_type = "强势"

    highest20 = None

    try:

        highest20 = max(

            df.iloc[-20:][
                COMPARE_TIME
            ].astype(float)

        )

        breakout_pct = (

            latest_price
            / highest20
            - 1

        ) * 100

        if (
            breakout_pct
            >= BREAKOUT_PCT
        ):

            stock_type = "趋势"

    except:

        pass

    target_price = None

    highest_price = None

    drawdown_price = None

    # ==========================
    # 强势股
    # ==========================

    if stock_type == "强势":

        target_price = round(

            buy_price
            * (
                1
                + STRONG_TAKE_PROFIT
            ),

            3,

        )

    # ==========================
    # 趋势股
    # ==========================

    else:

        try:

            highest_price = max(

                df.iloc[-60:][
                    COMPARE_TIME
                ].astype(float)

            )

            drawdown_price = round(

                highest_price
                * (
                    1
                    - DRAWDOWN_RATIO
                ),

                3,

            )

        except:

            pass

    return {

        "股票代码": code,

        "股票名称": stock_name,

        "买入价": round(
            buy_price,
            3,
        ),

        "最新日期": latest_date,

        "最新价": round(
            latest_price,
            3,
        ),

        "股票类型": stock_type,

        "当前收益%": round(
            current_profit,
            2,
        ),

        "突破幅度%": (
            round(
                breakout_pct,
                2,
            )
            if breakout_pct is not None
            else None
        ),

        "强势目标价": target_price,

        "趋势最高价": (
            round(
                highest_price,
                3,
            )
            if highest_price is not None
            else None
        ),

        "趋势回撤价": drawdown_price,

    }


def get_stock_signals(
    positions,
):

    results = []

    for (
        code,
        stock_name,
        buy_price,
    ) in positions:

        results.append(

            get_stock_signal(
                code,
                stock_name,
                buy_price,
            )

        )

    return pd.DataFrame(
        results
    )



if __name__ == "__main__":
    full_code, stock_name = (
        get_full_code_and_name(
            "688548"
        )
    )

    print(full_code)
    print(stock_name)
    positions = [

        (
            "SZ002068",
            "黑猫股份",
            12.65,
        ),

    ]

    result_df = get_stock_signals(
        positions
    )

    print()
    print(result_df)
    print()