"""
strategy.py

所有卖出策略都放这里
"""


def should_sell(
    df,
    buy_idx,
    current_idx,
    buy_price,
    buy_time,
    compare_time,
):
    """
    当前策略：

    今天1430 <= 昨天1455
    卖出

    今天1430 > 昨天1455
    继续持有
    """

    prev_close = float(
        df.iloc[current_idx - 1][compare_time]
    )

    curr_price = float(
        df.iloc[current_idx][buy_time]
    )

    return curr_price <= prev_close