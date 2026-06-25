from config import (
    DRAWDOWN_RATIO_LOW,
    DRAWDOWN_RATIO_MID,
    DRAWDOWN_RATIO_HIGH,
)


def should_sell(
    df,
    buy_idx,
    current_idx,
    buy_price,
    buy_time,
    compare_time,
):

    # ==========================
    # 历史最高价
    # ==========================

    highest_price = buy_price

    for i in range(
        buy_idx,
        current_idx + 1,
    ):

        try:

            highest_price = max(
                highest_price,
                float(
                    df.iloc[i][buy_time]
                )
            )

        except:

            pass

    curr_price = float(
        df.iloc[current_idx][buy_time]
    )

    # ==========================
    # 最大盈利
    # ==========================

    max_profit = (

        highest_price
        / buy_price

        - 1

    )

    # ==========================
    # 动态回撤
    # ==========================

    if max_profit < 0.20:

        drawdown_ratio = (
            DRAWDOWN_RATIO_LOW
        )

    elif max_profit < 0.50:

        drawdown_ratio = (
            DRAWDOWN_RATIO_MID
        )

    else:

        drawdown_ratio = (
            DRAWDOWN_RATIO_HIGH
        )

    # ==========================
    # 当前回撤
    # ==========================

    drawdown = (

        highest_price
        - curr_price

    ) / highest_price

    return (
        drawdown
        >= drawdown_ratio
    )