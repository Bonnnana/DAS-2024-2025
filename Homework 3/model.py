import sqlite3
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Path to your SQLite database file
db_path = '../Homework 1/all_issuers_data.db'


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


def train_and_evaluate_stock_model(
        stock_symbol,
        train_ratio=0.8,
        rolling_window=5,
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1
):
    """
    Pulls data for 'stock_symbol' from issuers_data,
    fixes numeric formats, engineers features, trains an XGBoost model,
    evaluates performance, and predicts next-day movement.
    """

    # ----------------------------------------------------------------------
    # 1. Open database connection, query data for the given issuer, then close.
    # ----------------------------------------------------------------------
    connection = connect_db()
    if connection is None:
        print("Could not establish a database connection.")
        return None, None, None, None

    query = "SELECT * FROM issuers_data WHERE ISSUER = :issuer"
    df = pd.read_sql_query(query, connection, params={"issuer": stock_symbol})

    connection.close()  # Close the connection after loading data
    print("Database connection closed.")

    if df.empty:
        print(f"No data found for issuer '{stock_symbol}'.")
        return "ERROR the prediction can't be made"

    # ----------------------------------------------------------------------
    # 2. Sort by DATE and reset index
    # ----------------------------------------------------------------------
    df.sort_values(by='DATE', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # ----------------------------------------------------------------------
    # 3. Convert relevant columns to numeric
    #    Fix the European numeric format before converting to floats.
    # ----------------------------------------------------------------------
    numeric_cols = [
        "LAST_TRADE_PRICE",
        "MAX_PRICE",
        "MIN_PRICE",
        "AVG_PRICE",
        "PERCENT_CHANGE",
        "TURNOVER",
        "TOTAL_TURNOVER"
    ]

    for col in numeric_cols:
        # Step 1: Convert to string if not already
        df[col] = df[col].astype(str)
        # Step 2: Apply fix_numeric_format
        df[col] = df[col].apply(fix_numeric_format)
        # Step 3: Convert to numeric
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Now drop rows where these columns are NaN
    df.dropna(subset=numeric_cols, inplace=True)

    # Check VOLUME similarly, if it exists
    if 'VOLUME' in df.columns:
        df['VOLUME'] = df['VOLUME'].astype(str)
        df['VOLUME'] = df['VOLUME'].apply(fix_numeric_format)
        df['VOLUME'] = pd.to_numeric(df['VOLUME'], errors='coerce')
        df.dropna(subset=['VOLUME'], inplace=True)
    else:
        # If VOLUME doesn't exist, create a dummy column (optional)
        df['VOLUME'] = 0

    # ----------------------------------------------------------------------
    # 4. Define the target (next-day price up or down)
    # ----------------------------------------------------------------------
    df['TARGET'] = (
            df['LAST_TRADE_PRICE'].shift(-1) > df['LAST_TRADE_PRICE']
    ).astype(int)

    # ----------------------------------------------------------------------
    # 5. Feature Engineering (lag features, rolling window stats)
    # ----------------------------------------------------------------------
    df['PRICE_1DAY_AGO'] = df['LAST_TRADE_PRICE'].shift(1)
    df['PRICE_2DAYS_AGO'] = df['LAST_TRADE_PRICE'].shift(2)
    df['PRICE_3DAYS_AGO'] = df['LAST_TRADE_PRICE'].shift(3)

    df[f'ROLLING_AVG_{rolling_window}'] = (
        df['LAST_TRADE_PRICE'].rolling(rolling_window).mean()
    )
    df[f'ROLLING_STD_{rolling_window}'] = (
        df['LAST_TRADE_PRICE'].rolling(rolling_window).std()
    )

    feature_cols = [
        "LAST_TRADE_PRICE",
        "MAX_PRICE",
        "MIN_PRICE",
        "AVG_PRICE",
        "PERCENT_CHANGE",
        "VOLUME",
        "TURNOVER",
        "TOTAL_TURNOVER",
        "PRICE_1DAY_AGO",
        "PRICE_2DAYS_AGO",
        "PRICE_3DAYS_AGO",
        f'ROLLING_AVG_{rolling_window}',
        f'ROLLING_STD_{rolling_window}'
    ]

    # Drop rows where these feature columns or TARGET are NaN
    df.dropna(subset=feature_cols + ['TARGET'], inplace=True)

    # ----------------------------------------------------------------------
    # 6. Split the data into train & test sets chronologically
    # ----------------------------------------------------------------------
    train_size = int(train_ratio * len(df))
    if train_size == 0 or train_size >= len(df):
        print("Not enough data to split into train and test.")
        return "ERROR the prediction can't be made"

    train_data = df.iloc[:train_size].copy()
    test_data = df.iloc[train_size:].copy()

    if len(train_data) == 0 or len(test_data) == 0:
        print("Not enough data after splitting for training or testing.")
        return "ERROR the prediction can't be made"

    X_train = train_data[feature_cols]
    y_train = train_data['TARGET']
    X_test = test_data[feature_cols]
    y_test = test_data['TARGET']

    # ----------------------------------------------------------------------
    # 7. Train the XGBoost model
    # ----------------------------------------------------------------------
    model = XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)

    # ----------------------------------------------------------------------
    # 8. Evaluate performance on the test set
    # ----------------------------------------------------------------------
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)

    print(f"\nModel trained for stock: {stock_symbol}")
    print(f"Total rows after cleaning: {len(df)}")
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
    print(f"Test Accuracy: {accuracy:.3f}")
    print("Classification Report:")
    print(classification_rep)

    # ----------------------------------------------------------------------
    # 9. Predict "tomorrow" relative to the most recent date in df
    # ----------------------------------------------------------------------
    latest_row = df.iloc[-1].copy()  # has all features for the last date
    X_future = latest_row[feature_cols].values.reshape(1, -1)
    future_pred = model.predict(X_future)[0]

    if future_pred == 1:
        print("Model predicts: The price is likely to go UP on the next day.")
    else:
        print("Model predicts: The price is likely to go DOWN (or stay the same) on the next day.")

    return "UP" if future_pred == 1 else "DOWN"


# =============================================================================
# Main section to test the function
# =============================================================================
if __name__ == '__main__':
    test_symbol = "ALK"  # or any other issuer you want to test
    model, acc, report, future_prediction = train_and_evaluate_stock_model(
        stock_symbol=test_symbol,
        train_ratio=0.8,
        rolling_window=5,
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1
    )

    if model is not None:
        print("\nFinished training and prediction.")
        print(f"Future prediction code for {test_symbol}: "
              f"{future_prediction} (1=Up, 0=Down/StaySame)")
        print(f"\nAccuracy {acc}")
