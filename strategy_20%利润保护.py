from config import (
    DRAWDOWN_RATIO,
)

MIN_PROFIT_TO_TRAIL = 0.20


def should_sell(
    df,
    buy_idx,
    current_idx,
    buy_price,
    buy_time,
    compare_time,
):

    highest_price = buy_price

    for i in range(
        buy_idx,
        current_idx + 1,
    ):

        highest_price = max(
            highest_price,
            float(
                df.iloc[i][buy_time]
            )
        )

    curr_price = float(
        df.iloc[current_idx][buy_time]
    )

    # 当前最大盈利

    max_profit = (
        highest_price / buy_price
        - 1
    )

    # 20%以内不给卖

    if (
        max_profit
        < MIN_PROFIT_TO_TRAIL
    ):
        return False

    drawdown = (
        highest_price
        - curr_price
    ) / highest_price

    return (
        drawdown
        >= DRAWDOWN_RATIO
    )