import requests
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import subprocess

def fetch_currency_data(currency_code, days=90):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"Dane dla {currency_code} pomyślnie pobrane z API.")
        return [(rate["effectiveDate"], rate["mid"]) for rate in data["rates"]]
    except Exception as e:
        print(f"Błąd podczas pobierania danych dla {currency_code} z API: {e}")
        return None

try:
    conn = sqlite3.connect('currency_data.db')
    cursor = conn.cursor()
    print("Pomyślnie połączono z bazą danych.")
except Exception as e:
    print(f"Błąd podczas łączenia z bazą danych: {e}")

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS currency_rates (
            date TEXT,
            eur_pln REAL,
            usd_pln REAL,
            chf_pln REAL,
            fetch_date TEXT
        )
    ''')
    conn.commit()
    print("Tabela w bazie danych została pomyślnie utworzona/zaktualizowana.")
except Exception as e:
    print(f"Błąd podczas tworzenia/aktualizacji tabeli: {e}")

eur_pln_data = fetch_currency_data("EUR")
usd_pln_data = fetch_currency_data("USD")
chf_pln_data = fetch_currency_data("CHF")

if eur_pln_data and usd_pln_data and chf_pln_data:
    data = {
        "date": [date for date, _ in eur_pln_data],
        "eur_pln": [rate for _, rate in eur_pln_data],
        "usd_pln": [rate for _, rate in usd_pln_data],
        "chf_pln": [rate for _, rate in chf_pln_data],
    }
    df = pd.DataFrame(data)
    fetch_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df["fetch_date"] = fetch_date

    existing_dates = pd.read_sql("SELECT date FROM currency_rates", conn)["date"].tolist()
    df_new = df[~df['date'].isin(existing_dates)]
    
    if not df_new.empty:
        try:
            df_new.to_sql('currency_rates', conn, if_exists='append', index=False)
            print("Nowe dane zostały pomyślnie zapisane w bazie danych.")
        except Exception as e:
            print(f"Błąd podczas zapisywania nowych danych do bazy: {e}")

        try:
            with open("all_currency_data.csv", 'a') as f:
                df_new.to_csv(f, header=f.tell()==0, index=False)
            print("Nowe dane zostały pomyślnie zapisane do pliku CSV.")
        except Exception as e:
            print(f"Błąd podczas zapisywania danych do pliku CSV: {e}")
    else:
        print("Brak nowych danych do zapisania.")
else:
    print("Nie udało się pobrać wszystkich danych z API.")

try:
    conn.close()
    print("Połączenie z bazą danych zostało zamknięte.")
except Exception as e:
    print(f"Błąd podczas zamykania połączenia z bazą danych: {e}")

try:
    print("Uruchamiam przelicznik.py...")
    subprocess.run(["python", "przelicznik.py"], check=True)
    print("Przelicznik.py został pomyślnie uruchomiony.")
except subprocess.CalledProcessError as e:
    print(f"Błąd podczas uruchamiania przelicznik.py: {e}")
