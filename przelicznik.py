import sqlite3
import pandas as pd
import time

# Połączenie z bazą danych
conn = sqlite3.connect('currency_data.db', check_same_thread=False)
cursor = conn.cursor()
print("Połączenie z bazą danych nawiązane.")

def update_rates_in_db(df, cursor):
    try:
        # Aktualizacja bazy danych z nowymi kursami
        df.to_sql('currency_rates', conn, if_exists='replace', index=False)
        print("Zaktualizowano kursy w bazie danych.")
    except Exception as e:
        print(f"Błąd podczas aktualizacji bazy danych: {e}")

def update_csv_file(df):
    try:
        # Zapisanie do pliku CSV
        df.to_csv("all_currency_data.csv", index=False)
        print("Zaktualizowano plik CSV z kursami walut.")
    except Exception as e:
        print(f"Błąd podczas aktualizacji pliku CSV: {e}")

def calculate_and_update_rates():
    try:
        df = pd.read_sql_query("SELECT * FROM currency_rates", conn)
        df['eur_usd'] = df['eur_pln'] / df['usd_pln']
        df['eur_chf'] = df['eur_pln'] / df['chf_pln']
        print("Przeliczono kursy EUR/USD i EUR/CHF.")
        update_rates_in_db(df, cursor)
        update_csv_file(df)
    except Exception as e:
        print(f"Błąd podczas przeliczania kursów: {e}")

# Przelicz kursy od razu po uruchomieniu
calculate_and_update_rates()

try:
    last_count = pd.read_sql_query("SELECT COUNT(*) FROM currency_rates", conn).iloc[0,0]
except Exception as e:
    print(f"Błąd podczas wczytywania danych z bazy: {e}")
    last_count = 0

# Nieskończona pętla do monitorowania bazy danych
while True:
    try:
        current_count = pd.read_sql_query("SELECT COUNT(*) FROM currency_rates", conn).iloc[0,0]
        if current_count > last_count:
            print("Wykryto nowe dane, przeliczam kursy...")
            calculate_and_update_rates()
            last_count = current_count
        else:
            print("Brak nowych danych. Ponowne sprawdzenie za 60 sekund.")
        time.sleep(60)  # Sprawdza bazę danych co 60 sekund
    except Exception as e:
        print(f"Błąd podczas sprawdzania bazy danych: {e}")
        time.sleep(60)

# Zasoby: połączenie powinno być zarządzane przy użyciu kontekstu lub zamykane po użyciu
