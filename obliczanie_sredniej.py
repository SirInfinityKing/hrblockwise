import sys
import sqlite3
import pandas as pd
import json

def calculate_currency_statistics(currency_pair, db_path='currency_data.db'):
    try:
        conn = sqlite3.connect(db_path)
        query = f"SELECT {currency_pair} FROM currency_rates"
        df = pd.read_sql_query(query, conn)
        mean = df[currency_pair].mean()
        median = df[currency_pair].median()
        min_value = df[currency_pair].min()
        max_value = df[currency_pair].max()
        conn.close()
        return {'mean': mean, 'median': median, 'min': min_value, 'max': max_value}
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        currency_pair = sys.argv[1]

    stats = calculate_currency_statistics(currency_pair)
    print(json.dumps(stats))  # Wypisanie wyniku w formacie JSON
