import pandas as pd


def save_type_analysis(
    all_df,
    result_dir,
):

    if all_df.empty:
        return

    analysis_df = (
        all_df
        .groupby("股票类型")
        .agg({

            "股票代码": "count",

            "收益率%": [
                "mean",
                "max",
                "min"
            ],

            "盈利金额": "sum",

            "持仓天数": "mean",

        })
    )

    hold_desc = (
        all_df
        .groupby("股票类型")
        ["持仓天数"]
        .describe()
    )

    hold_desc.to_excel(
        result_dir / "持仓天数分析.xlsx"
    )

    profit_desc = (
        all_df
        .groupby("股票类型")
        ["收益率%"]
        .describe()
    )

    profit_desc.to_excel(
        result_dir / "收益率分析.xlsx"
    )

    analysis_df.columns = [

        "交易数",

        "平均收益率",

        "最大收益",

        "最大亏损",

        "总盈利",

        "平均持仓天数",

    ]

    analysis_df["胜率"] = (

        all_df
        .groupby("股票类型")
        ["收益率%"]
        .apply(
            lambda x:
            (x > 0).mean() * 100
        )

    )

    analysis_df = analysis_df.round(2)

    analysis_df.to_excel(
        result_dir / "趋势_vs_强势.xlsx"
    )

    breakout_analysis = (
        all_df
        .dropna(subset=["突破幅度"])
    )

    breakout_analysis["突破区间"] = pd.cut(

        breakout_analysis["突破幅度"],

        bins=[
            -100,
            0,
            2,
            5,
            10,
            20,
            100
        ]
    )

    result = (

        breakout_analysis

        .groupby("突破区间")

        .agg({

            "收益率%": [
                "count",
                "mean",
                "median",
                "max",
                "min"
            ]

        })

    )

    result.to_excel(
        result_dir / "突破幅度分析.xlsx"
    )

    return analysis_df


def save_month_result(
    result_df,
    month_file,
):
    """
    保存单月明细
    """

    result_df.to_excel(
        month_file,
        index=False,
    )


def save_summary(
    summary_rows,
    result_dir,
):
    """
    保存月度汇总
    """

    if not summary_rows:
        return

    summary_df = pd.DataFrame(
        summary_rows
    )

    summary_df.to_excel(
        result_dir / "月度汇总.xlsx",
        index=False,
    )


def save_all_results(
    all_results,
    result_dir,
):
    """
    保存全部交易明细
    """

    if not all_results:
        return

    all_df = pd.concat(
        all_results,
        ignore_index=True,
    )

    all_df.to_excel(
        result_dir / "全部明细.xlsx",
        index=False,
    )