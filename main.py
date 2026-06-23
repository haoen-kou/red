import pandas as pd
from config import *
from backtest import backtest_one_month
from report import (
    save_month_result,
    save_summary,
    save_all_results,
    save_type_analysis,
)


def main():

    all_results = []

    summary_rows = []

    rolling_cash = INIT_CASH

    trade_files = sorted(
        TRADE_DIR.glob("Table*.xls")
    )

    for trade_file in trade_files:

        result_df, limit_count = (
            backtest_one_month(
                trade_file
            )
        )

        if result_df.empty:
            continue

        month_name = trade_file.stem

        month_file = (
            RESULT_DIR
            / f"{month_name}.xlsx"
        )

        save_month_result(
            result_df,
            month_file,
        )

        total_profit = (
            result_df["盈利金额"]
            .sum()
        )

        rolling_cash += total_profit

        win_rate = (
            (
                result_df["收益率%"]
                > 0
            ).mean()
            * 100
        )

        summary_rows.append({

            "月份": month_name,

            "交易数": len(
                result_df
            ),

            "涨停过滤": limit_count,

            "胜率": round(
                win_rate,
                2,
            ),

            "平均收益率": round(
                result_df[
                    "收益率%"
                ].mean(),
                2,
            ),

            "平均持仓天数": round(
                result_df[
                    "持仓天数"
                ].mean(),
                2,
            ),

            "最大盈利": round(
                result_df[
                    "收益率%"
                ].max(),
                2,
            ),

            "最大亏损": round(
                result_df[
                    "收益率%"
                ].min(),
                2,
            ),

            "总盈利": round(
                total_profit,
                2,
            ),

            "期末资金": round(
                rolling_cash,
                2,
            ),
        })

        all_results.append(
            result_df
        )

    save_summary(
        summary_rows,
        RESULT_DIR,
    )

    save_all_results(
        all_results,
        RESULT_DIR,
    )

    if all_results:
        all_df = pd.concat(
            all_results,
            ignore_index=True,
        )

        save_type_analysis(
            all_df,
            RESULT_DIR,
        )

    print("\n====================")
    print("全部回测完成")
    print("====================")

    print(
        f"最终资金: "
        f"{rolling_cash:,.2f}"
    )

    print(
        f"结果目录: "
        f"{RESULT_DIR}"
    )


if __name__ == "__main__":
    main()