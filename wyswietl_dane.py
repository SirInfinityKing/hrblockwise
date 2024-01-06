import sqlite3
import pandas as pd

# Tworzenie połączenia z bazą danych
conn = sqlite3.connect('currency_data.db')

# Wykonanie zapytania SQL i wyświetlenie wyników
query = "SELECT * FROM currency_rates"
df = pd.read_sql_query(query, conn)
print(df)

# Zamknięcie połączenia
conn.close()
