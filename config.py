from pathlib import Path

# ==========================
# 自动识别盘符
# ==========================

if Path(
    r"D:\code\PycharmProjects\red"
).exists():

    ROOT_DIR = Path(
        r"D:\code\PycharmProjects\red"
    )

    DATA_ROOT = Path(
        r"D:\qdata"
    )

else:

    ROOT_DIR = Path(
        r"C:\code\red"
    )

    DATA_ROOT = Path(
        r"C:\code\data"
    )

# ==========================
# 目录
# ==========================

TRADE_DIR = (
    ROOT_DIR
    / "backtest"
)

RESULT_DIR = (
    ROOT_DIR
    / "result"
)

DATA_DIR = (
    DATA_ROOT
    / "stock-5m-close-price"
)

TRADING_DATA_DIR = (
    DATA_ROOT
    / "stock-trading-data"
)

RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================
# 回测参数
# ==========================

INIT_CASH = 500000

POSITION_SIZE = 100000

BUY_TIME = "1430"

COMPARE_TIME = "1455"

LIMIT_RATIO = 0.998

# ==========================
# 趋势/强势开关
# ==========================

ENABLE_TREND_FILTER = True

ENABLE_STRONG_STOCK = True

# ==========================
# 趋势股判定
# ==========================

BREAKOUT_PCT = 7

# ==========================
# 固定回撤
# ==========================

DRAWDOWN_RATIO = 0.05

# ==========================
# 动态回撤
# ==========================

# 盈利20%以内
DRAWDOWN_RATIO_LOW = 0.10

# 盈利20%-50%
DRAWDOWN_RATIO_MID = 0.08

# 盈利50%以上
DRAWDOWN_RATIO_HIGH = 0.05

# ==========================
# 强势股止盈
# ==========================

STRONG_TAKE_PROFIT = 0.06

# ==========================
# 最大持仓天数
# ==========================

TREND_MAX_HOLD_DAYS = 0

STRONG_MAX_HOLD_DAYS = 0