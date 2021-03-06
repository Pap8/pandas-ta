# -*- coding: utf-8 -*-
from pandas_ta.overlap import ema, rma, sma, wma
from .true_range import true_range
from pandas_ta.utils import get_drift, get_offset, verify_series


def atr(high, low, close, length=None, mamode=None, drift=None, offset=None, **kwargs):
    """Indicator: Average True Range (ATR)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    mamode = mamode = mamode.lower() if mamode else "rma"
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    _mode = ""
    tr = true_range(high=high, low=low, close=close, drift=drift)
    if mamode == "ema":
        atr, _mode = ema(tr, length=length), "ema"
    elif mamode == "sma":
        atr, _mode = sma(tr, length=length), "sma"
    elif mamode == "wma":
        atr, _mode = wma(tr, length=length), "wma"
    else: # "rma"
        atr = rma(tr, length=length)

    percentage = kwargs.pop("percent", False)
    if percentage:
        atr *= 100 / close

    # Offset
    if offset != 0:
        atr = atr.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        atr.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        atr.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    # mamode_ = 
    atr.name = f"ATR{_mode}_{length}{'p' if percentage else ''}"
    atr.category = "volatility"

    return atr


atr.__doc__ = \
    """Average True Range (ATR)
    Averge True Range is used to measure volatility, especially
    volatility caused by gaps or limit moves.
    Sources:
        https://www.tradingview.com/wiki/Average_True_Range_(ATR)
    Calculation:
        Default Inputs:
            length=14, drift=1, percent=False
        SMA = Simple Moving Average
        EMA = Exponential Moving Average
        WMA = Weighted Moving Average 
        RMA = Running Moving Average
        TR = True Range
        tr = TR(high, low, close, drift)
        if 'ema':
            ATR = EMA(tr, length)
        elif 'sma':
            ATR = SMA(tr, length)
        elif 'wma':
            ATR = WMA(tr, length)
        else:
            ATR = RMA(tr, length)
            
        if percent:
            ATR *= 100 / close
    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        mamode (str): 'sma', 'ema', 'wma' or 'rma'. Default: 'rma'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0
    Kwargs:
        percent (bool, optional): Return as percentage. Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method
    Returns:
        pd.Series: New feature generated.
    """
