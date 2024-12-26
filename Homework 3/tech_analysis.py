import pandas as pd
import talib
from datetime import datetime, timedelta
import json


def fetch_historical_data(conn, issuer, start_date, end_date):
    query = """
        SELECT ISSUER, DATE, LAST_TRADE_PRICE, MAX_PRICE, MIN_PRICE, VOLUME
        FROM issuers_data
        WHERE ISSUER = ? AND DATE BETWEEN ? AND ?
        ORDER BY DATE ASC
    """
    data = pd.read_sql_query(query, conn,
                             params=(issuer, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

    data['DATE'] = pd.to_datetime(data['DATE'])
    data.set_index('DATE', inplace=True)
    data.sort_index(inplace=True)

    for column in ['LAST_TRADE_PRICE', 'MAX_PRICE', 'MIN_PRICE']:
        data[column] = data[column].apply(lambda x: float(x.replace('.', '').replace(',', '.')))

    return data


def calculate_indicators(data):
    prices = data['LAST_TRADE_PRICE']
    high = data['MAX_PRICE']
    low = data['MIN_PRICE']

    data['RSI'] = talib.RSI(prices, timeperiod=30)
    data['STOCH_K'], data['STOCH_D'] = talib.STOCH(high, low, prices, fastk_period=30, slowk_period=3, slowd_period=3)
    data['MACD'], data['MACD_SIGNAL'], _ = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    data['CCI'] = talib.CCI(high, low, prices, timeperiod=30)
    data['WILLR'] = talib.WILLR(high, low, prices, timeperiod=30)

    data['SMA'] = talib.SMA(prices, timeperiod=30)
    data['EMA'] = talib.EMA(prices, timeperiod=30)
    data['WMA'] = talib.WMA(prices, timeperiod=30)
    data['TRIMA'] = talib.TRIMA(prices, timeperiod=30)
    data['KAMA'] = talib.KAMA(prices, timeperiod=30)

    return data


def generate_signals(data):
    def oscillator_signal(value, overbought=70, oversold=30):
        if value > overbought:
            return 'SELL'
        elif value < oversold:
            return 'BUY'
        else:
            return 'HOLD'

    def ma_signal(price, ma_value):
        if price > ma_value:
            return 'BUY'
        elif price < ma_value:
            return 'SELL'
        else:
            return 'HOLD'

    data['RSI_SIGNAL'] = data['RSI'].apply(oscillator_signal)
    data['CCI_SIGNAL'] = data['CCI'].apply(oscillator_signal)
    data['WILLR_SIGNAL'] = data['WILLR'].apply(oscillator_signal)
    data['STOCH_SIGNAL'] = data['STOCH_K'].apply(oscillator_signal)
    data['MACD_SIGNAL'] = data['MACD'].apply(oscillator_signal)

    for ma in ['SMA', 'EMA', 'WMA', 'TRIMA', 'KAMA']:
        signal_col = f"{ma}_SIGNAL"
        data[signal_col] = data.apply(lambda row: ma_signal(row['LAST_TRADE_PRICE'], row[ma]), axis=1)

    return data


def perform_technical_analysis(conn, issuer, timeperiod):
    """
    Main function to perform technical analysis

    Args:
        conn (sqlite3.Connection): Database connection.
        issuer (str): Stock issuer.
        timeperiod (int): Analysis period in days.

    Returns:
        dict: Technical analysis summary.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)

    data = fetch_historical_data(conn, issuer, start_date, end_date)

    if data.empty:
        return {"error": "No data available for this issuer in the selected period."}

    data = calculate_indicators(data)
    data = generate_signals(data)

    selected_period = data.tail(timeperiod)

    oscillator_summary = {
        "Relative Strength Index (RSI)": {
            "value": round(selected_period['RSI'].mean(), 2),
            "signal": selected_period['RSI_SIGNAL'].mode()[0]
        },
        "Commodity Channel Index (CCI)": {
            "value": round(selected_period['CCI'].mean(), 2),
            "signal": selected_period['CCI_SIGNAL'].mode()[0]
        },
        "Williams %R (WILLR)": {
            "value": round(selected_period['WILLR'].mean(), 2),
            "signal": selected_period['WILLR_SIGNAL'].mode()[0]
        },
        "Stochastic Oscillator (STOCH)": {
            "value": round(selected_period['STOCH_K'].mean(), 2),
            "signal": selected_period['STOCH_SIGNAL'].mode()[0]
        },
        "Moving Average Convergence Divergence (MACD)": {
            "value": round(selected_period['MACD'].mean(), 2),
            "signal": selected_period['MACD_SIGNAL'].mode()[0]
        }
    }

    moving_average_summary = {
        "Simple Moving Average (SMA)": {
            "value": round(selected_period['SMA'].mean(), 2),
            "signal": selected_period['SMA_SIGNAL'].mode()[0]
        },
        "Exponential Moving Average (EMA)": {
            "value": round(selected_period['EMA'].mean(), 2),
            "signal": selected_period['EMA_SIGNAL'].mode()[0]
        },
        "Weighted Moving Average (WMA)": {
            "value": round(selected_period['WMA'].mean(), 2),
            "signal": selected_period['WMA_SIGNAL'].mode()[0]
        },
        "Triangular Moving Average (TRIMA)": {
            "value": round(selected_period['TRIMA'].mean(), 2),
            "signal": selected_period['TRIMA_SIGNAL'].mode()[0]
        },
        "Kaufman Adaptive Moving Average (KAMA)": {
            "value": round(selected_period['KAMA'].mean(), 2),
            "signal": selected_period['KAMA_SIGNAL'].mode()[0]
        }
    }

    signal_counts = {
        signal: sum([
            1 for osc in oscillator_summary.values() if osc['signal'] == signal
        ]) + sum([
            1 for ma in moving_average_summary.values() if ma['signal'] == signal
        ])
        for signal in ['BUY', 'SELL', 'HOLD']
    }

    result = {
        "oscillator_summary": oscillator_summary,
        "moving_average_summary": moving_average_summary,
        "signal_counts": signal_counts,
        "final_recommendation": max(signal_counts, key=signal_counts.get) if signal_counts['BUY'] != signal_counts[
            'SELL'] else 'HOLD'
    }

    return json.dumps(result, indent=4)
