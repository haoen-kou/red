from pathlib import Path

TRADE_DIR = Path(
    r"D:\code\PycharmProjects\red\backtest"
)

DATA_DIR = Path(
    r"D:\qdata\stock-5m-close-price"
)

RESULT_DIR = Path(
    r"D:\code\PycharmProjects\red\result"
)

TRADING_DATA_DIR = Path(
    r"D:\qdata\stock-trading-data"
)

RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INIT_CASH = 500000

POSITION_SIZE = 100000

BUY_TIME = "1430"

COMPARE_TIME = "1455"

LIMIT_RATIO = 0.998

# 是否启用趋势股判断
# True:
#   趋势股 -> 原策略
#   强势股 -> 5%止盈
#
# False:
#   所有股票都按趋势策略
ENABLE_TREND_FILTER = True

# 是否参与强势股

ENABLE_STRONG_STOCK = True

# 趋势股判定
BREAKOUT_PCT = 7

# 回撤卖出比例
DRAWDOWN_RATIO = 0.05

# 趋势股动态回撤

# 盈利20%以内
DRAWDOWN_RATIO_LOW = 0.10

# 盈利20%-50%
DRAWDOWN_RATIO_MID = 0.08

# 盈利50%以上
DRAWDOWN_RATIO_HIGH = 0.05
# 强势股止盈比例
# 0.05 = 5%
# 0.08 = 8%
# 0.10 = 10%
STRONG_TAKE_PROFIT = 0.06

# 趋势股最大持仓天数
TREND_MAX_HOLD_DAYS = 0

# 强势股最大持仓天数
STRONG_MAX_HOLD_DAYS = 0