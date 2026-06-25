from config import TRADING_DATA_DIR
import pandas as pd
stock_name_cache = {}


def get_stock_name(
    full_code,
):

    if full_code in stock_name_cache:
        return stock_name_cache[full_code]

    file_path = (
        TRADING_DATA_DIR
        / f"{full_code.lower()}.csv"
    )

    if not file_path.exists():
        return ""

    try:

        df = pd.read_csv(
            file_path,
            encoding="gb18030",
            skiprows=1,
            usecols=["股票名称"],
            nrows=10,
        )

        names = (
            df["股票名称"]
            .astype(str)
            .str.strip()
            .tolist()
        )

        for name in names:

            # 跳过新股名称

            if name.startswith(
                (
                    "N",
                    "C",
                    "XD",
                    "XR",
                    "DR",
                )
            ):
                continue

            stock_name_cache[
                full_code
            ] = name

            return name

        # 全部都是N开头

        name = names[-1]

        stock_name_cache[
            full_code
        ] = name

        return name

    except Exception as e:

        print(
            full_code,
            e,
        )

        return ""

def get_full_code_and_name(
    code,
):

    code = str(code).strip()

    if code.startswith(
        ("00", "30")
    ):
        full_code = f"SZ{code}"

    elif code.startswith(
        ("60", "68")
    ):
        full_code = f"SH{code}"

    elif code.startswith(
        ("83", "87", "92")
    ):
        full_code = f"BJ{code}"

    else:

        return (
            code,
            "",
        )

    stock_name = get_stock_name(
        full_code
    )

    return (
        full_code,
        stock_name,
    )