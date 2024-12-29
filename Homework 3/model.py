import sqlite3

import matplotlib
import pandas as pd
import base64
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import io

# Path to your SQLite database file
db_path = '../../proekt/Homework 1/all_issuers_data.db'

def connect_db():
    """
    Opens a connection to the SQLite database and returns the connection object.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enables column name-based access
        print("Database connection established successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def fix_numeric_format(value):
    """
    This function takes a numeric string in a European format, e.g. '6.928.265,00',
    and returns a standard float-compatible string, e.g. '6928265.00'.
    """
    if not isinstance(value, str):
        # If it's already a float or int (or NaN), just return it as-is
        return value
    # Remove all '.' (thousand separators)
    no_thousand_sep = value.replace('.', '')
    # Replace ',' with '.' for decimals
    standard_decimal = no_thousand_sep.replace(',', '.')
    return standard_decimal

def train_and_evaluate_stock_model_with_image(
        stock_symbol,
        train_ratio=0.7,
        rolling_window=5,
        n_units=50,
        dropout_rate=0.2,
        epochs=20,
        batch_size=32
):
    """
    Pulls data for 'stock_symbol' from issuers_data, fixes numeric formats,
    engineers features, trains an LSTM model, evaluates performance,
    and generates a line plot of stock prices over time.
    """
    # 1. Open database connection, query data, then close
    connection = connect_db()
    if connection is None:
        return "ERROR the prediction can't be made", None

    query = "SELECT * FROM issuers_data WHERE ISSUER = :issuer"
    df = pd.read_sql_query(query, connection, params={"issuer": stock_symbol})
    connection.close()

    if df.empty:
        return "ERROR the prediction can't be made", None

    # 2. Data preparation
    df.sort_values(by='DATE', inplace=True)
    df.reset_index(drop=True, inplace=True)

    numeric_cols = [
        "LAST_TRADE_PRICE", "MAX_PRICE", "MIN_PRICE", "AVG_PRICE",
        "PERCENT_CHANGE", "TURNOVER", "TOTAL_TURNOVER"
    ]

    for col in numeric_cols:
        df[col] = df[col].astype(str).apply(fix_numeric_format)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=numeric_cols, inplace=True)

    if 'VOLUME' in df.columns:
        df['VOLUME'] = df['VOLUME'].astype(str).apply(fix_numeric_format)
        df['VOLUME'] = pd.to_numeric(df['VOLUME'], errors='coerce')
        df.dropna(subset=['VOLUME'], inplace=True)
    else:
        df['VOLUME'] = 0

    df['TARGET'] = (df['LAST_TRADE_PRICE'].shift(-1) > df['LAST_TRADE_PRICE']).astype(int)

    # 3. Feature Engineering
    df['PRICE_1DAY_AGO'] = df['LAST_TRADE_PRICE'].shift(1)
    df['PRICE_2DAYS_AGO'] = df['LAST_TRADE_PRICE'].shift(2)
    df['PRICE_3DAYS_AGO'] = df['LAST_TRADE_PRICE'].shift(3)
    df[f'ROLLING_AVG_{rolling_window}'] = df['LAST_TRADE_PRICE'].rolling(rolling_window).mean()
    df[f'ROLLING_STD_{rolling_window}'] = df['LAST_TRADE_PRICE'].rolling(rolling_window).std()

    feature_cols = [
        "LAST_TRADE_PRICE", "MAX_PRICE", "MIN_PRICE", "AVG_PRICE",
        "PERCENT_CHANGE", "VOLUME", "TURNOVER", "TOTAL_TURNOVER",
        "PRICE_1DAY_AGO", "PRICE_2DAYS_AGO", "PRICE_3DAYS_AGO",
        f'ROLLING_AVG_{rolling_window}', f'ROLLING_STD_{rolling_window}'
    ]

    df.dropna(subset=feature_cols + ['TARGET'], inplace=True)

    # 4. Split data
    train_size = int(train_ratio * len(df))
    if train_size == 0 or train_size >= len(df):
        return "ERROR the prediction can't be made", None

    train_data = df.iloc[:train_size]
    validation_data = df.iloc[train_size:]

    X_train = train_data[feature_cols].values
    y_train = train_data['TARGET'].values
    X_validation = validation_data[feature_cols].values
    y_validation = validation_data['TARGET'].values

    # Reshape data for LSTM (samples, timesteps, features)
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_validation = X_validation.reshape((X_validation.shape[0], 1, X_validation.shape[1]))

    # 5. Build and train the model
    model = Sequential([
        LSTM(n_units, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=False),
        Dropout(dropout_rate),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)

    # 6. Predict and evaluate
    y_pred = (model.predict(X_validation) > 0.5).astype(int).flatten()

    latest_row = df.iloc[-1]
    X_future = latest_row[feature_cols].values.reshape(1, 1, -1)
    future_pred = (model.predict(X_future) > 0.5).astype(int)[0][0]
    prediction = "UP" if future_pred == 1 else "DOWN"

    # 7. Generate line plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['DATE'], df['LAST_TRADE_PRICE'], label='Last Trade Price', color='green', linewidth=2)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.tick_params(axis='x', which='both', labelbottom=False)
    ax.legend(loc='upper left', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    plt.close()

    # Convert image to Base64
    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')

    return prediction, img_base64

# =============================================================================
# Main section to test the function
# =============================================================================
if __name__ == '__main__':
    test_symbol = "ALK"  # or any other issuer you want to test
    # model, acc, report, future_prediction = train_and_evaluate_stock_model_with_image(
    #     stock_symbol=test_symbol,
    #     train_ratio=0.7,
    #     rolling_window=5,
    #     n_units=50,
    #     dropout_rate=0.2,
    #     epochs=20,
    #     batch_size=32
    # )
    #
    # if model is not None:
    #     print("\nFinished training and prediction.")
    #     print(f"Future prediction code for {test_symbol}: "
    #           f"{future_prediction} (1=Up, 0=Down/StaySame)")
    #     print(f"\nAccuracy {acc}")
