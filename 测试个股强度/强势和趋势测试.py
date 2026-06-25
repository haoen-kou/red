import numpy as np
import pandas as pd

from backtest import load_stock_data
from utils import get_full_code_and_name


def judge_with_5min(
    df_5min,
):

    df = df_5min.copy()

    df["MA5"] = (
        df["close"]
        .rolling(5)
        .mean()
    )

    df["MA60"] = (
        df["close"]
        .rolling(60)
        .mean()
    )

    if len(df) < 60:

        return {
            "pattern": "数据不足",
            "score": 0,
        }

    df_valid = df.iloc[60:].copy()

    latest_close = (
        df_valid["close"]
        .iloc[-1]
    )

    latest_ma60 = (
        df_valid["MA60"]
        .iloc[-1]
    )

    deviation = (
        latest_close
        - latest_ma60
    ) / latest_ma60

    df_valid["tr"] = np.maximum(
        df_valid["high"]
        - df_valid["low"],
        np.maximum(
            abs(
                df_valid["high"]
                - df_valid["close"].shift(1)
            ),
            abs(
                df_valid["low"]
                - df_valid["close"].shift(1)
            ),
        ),
    )

    atr_ratio = (
        df_valid["tr"].mean()
        / latest_close
    )

    price_cv = (
        df_valid["close"].std()
        / df_valid["close"].mean()
    )

    recent_return = (
        df_valid["close"].iloc[-1]
        - df_valid["close"].iloc[-20]
    ) / df_valid["close"].iloc[-20]

    score = 0

    # 偏离度

    if deviation > 0.08:
        score += 30

    elif deviation > 0.05:
        score += 20

    elif deviation > 0.02:
        score += 10

    # ATR

    if atr_ratio > 0.025:
        score += 30

    elif atr_ratio > 0.015:
        score += 20

    else:
        score += 5

    # 变异系数

    if price_cv > 0.03:
        score += 20

    elif price_cv > 0.015:
        score += 10

    else:
        score += 5

    # 最近20根涨幅

    if recent_return > 0.05:
        score += 20

    elif recent_return > 0.02:
        score += 10

    elif recent_return > 0:
        score += 5

    if score >= 70:

        pattern = "强势股"

    elif score >= 50:

        pattern = "强势震荡"

    else:

        pattern = "趋势股"

    return {

        "pattern": pattern,

        "score": score,

        "deviation": round(
            deviation * 100,
            2,
        ),

        "atr": round(
            atr_ratio * 100,
            2,
        ),

        "price_cv": round(
            price_cv * 100,
            2,
        ),

        "recent_return": round(
            recent_return * 100,
            2,
        ),
    }


def get_pattern_signal(
    code,
    trade_date=None,
):

    full_code, stock_name = (
        get_full_code_and_name(
            code
        )
    )

    df = load_stock_data(
        full_code
    )

    if df is None:

        return {

            "股票代码": full_code,

            "股票名称": stock_name,

            "状态": "无数据",

        }

    # ======================
    # 指定日期
    # ======================

    if trade_date:

        trade_date = pd.to_datetime(
            trade_date
        ).strftime(
            "%Y-%m-%d"
        )

        df = df[
            df["交易日期"]
            <= trade_date
        ]

        if df.empty:

            return {

                "股票代码": full_code,

                "股票名称": stock_name,

                "状态": "日期无数据",

            }

    # ======================
    # 最近20个交易日
    # ======================

    df = df.tail(20)

    time_cols = sorted(
        [
            c
            for c in df.columns
            if c.isdigit()
        ]
    )

    rows = []

    for _, row in df.iterrows():

        for t in time_cols:

            try:

                price = float(
                    row[t]
                )

            except:

                continue

            rows.append({

                "close": price,

                "high": price,

                "low": price,

            })

    df_5min = pd.DataFrame(
        rows
    )

    result = judge_with_5min(
        df_5min
    )

    return {

        "股票代码": full_code,

        "股票名称": stock_name,

        "截止日期":
            (
                df.iloc[-1]["交易日期"]
                if len(df)
                else None
            ),

        "模式":
            result["pattern"],

        "评分":
            result["score"],

        "偏离度%":
            result["deviation"],

        "ATR%":
            result["atr"],

        "价格变异系数%":
            result["price_cv"],

        "20根涨幅%":
            result["recent_return"],
    }

def get_pattern_signals(
    positions,
):

    results = []

    for item in positions:

        # 可以只传代码
        if len(item) == 1:

            code = item[0]

            trade_date = None

        # 传代码+日期
        else:

            code = item[0]

            trade_date = item[1]

        result = get_pattern_signal(
            code,
            trade_date,
        )

        results.append(
            result
        )

    return pd.DataFrame(
        results
    )


if __name__ == "__main__":

    positions = [

        # (
        #     "002498",
        #     "2026-01-22",
        # ),

        (
            "001359",
            "2026-06-24",
        ),

        (
            "603260",
        ),      # 不写日期，默认最新

        (
            "002631",
        ),

    ]

    result_df = get_pattern_signals(
        positions
    )

    print()

    print(result_df)

    print()