from config import DRAWDOWN_RATIO


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

    drawdown = (
        highest_price - curr_price
    ) / highest_price

    return drawdown >= DRAWDOWN_RATIO