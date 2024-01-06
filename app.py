import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import subprocess
from io import BytesIO
import psutil

# Uruchom api.py jako proces w tle
subprocess.Popen(["python", "api.py"])

st.title('Moja Aplikacja Streamlit')

# Adresy URL API
API_URL = "http://localhost:5000/api/data"
RUN_SCRIPT_URL = "http://localhost:5000/run-script"


@st.cache_data(ttl=3600)
def load_data_from_api():
    response = requests.get(API_URL)
    if response.ok:
        df = pd.DataFrame(response.json())
        df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        st.error('Nie udało się pobrać danych z API.')
        return pd.DataFrame()

def run_kursywalut_script():
    response = requests.post(RUN_SCRIPT_URL)
    if response.ok:
        st.success('Pobrano najnowsze dane!')
    else:
        st.error('Nie udało się, próbuj później.')

def is_script_running(script_name):
    "Sprawdza, czy skrypt jest uruchomiony."
    for process in psutil.process_iter(['name']):
        if script_name in process.info['name']:
            return True
    return False

st.title('Dashboard kursów walutowych')

with st.sidebar:
    st.title('Panel zarządzania')
    if st.button('Zaktualizuj o najnowsze dane'):
        run_kursywalut_script()

    # Sprawdzanie, czy skrypt cyklicznie.py jest uruchomiony
    script_status = is_script_running("cyklicznie.py")
    if st.checkbox('Uruchom pobieranie codziennie o 12:00', value=script_status):
        if not script_status:
            # Jeśli skrypt nie jest uruchomiony, uruchom go
            subprocess.Popen(["python", "cyklicznie.py"])
            st.success('Uruchomiono czyklicne pobieranie danych!')
        else:
            st.warning('Pobieranie danych już jest aktywne')
    else:
        if script_status:
            st.warning('Pobieranie danych aktywne')
        else:
            st.error('Nie aktywowałeś cyklicznego pobierania danych')

    # Lista dostępnych par walutowych
    available_currency_pairs = ["EUR/PLN", "USD/PLN", "CHF/PLN", "EUR/USD", "EUR/CHF"]
    selected_pairs = st.multiselect('Wybierz pary walutowe', available_currency_pairs)
    
    # Wybór zakresu dat
    date_range = st.slider("Wybierz zakres dni do wyświetlenia", 1, 90, 30)
    start_date = datetime.now() - timedelta(days=date_range)



df = load_data_from_api()

if not df.empty and selected_pairs:
    df = df[df['date'] >= start_date]

    friendly_column_names = {
        'date': 'Data',
        'eur_pln': 'EUR/PLN',
        'usd_pln': 'USD/PLN',
        'chf_pln': 'CHF/PLN',
        'eur_usd': 'EUR/USD',
        'eur_chf': 'EUR/CHF'
    }
    df.rename(columns=friendly_column_names, inplace=True)
    df_display = df[['Data'] + selected_pairs]
    st.dataframe(df_display)

    # Funkcja konwertująca DataFrame do CSV
    def to_csv(df):
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8')
        return output.getvalue()

    # Przycisk pobierania wybranych par walutowych jako CSV
    csv = to_csv(df_display)
    st.download_button(
        label="Pobierz wybrane pary walutowe jako CSV",
        data=csv,
        file_name='selected_currency_pairs.csv',
        mime='text/csv',
        on_click=lambda: st.session_state.setdefault('download_clicked', True)  # Ustawienie flagi w stan sesji
    )

    # Sprawdzanie, czy przycisk został naciśnięty i wyświetlanie komunikatu
    if st.session_state.get('download_clicked'):
        st.success('Plik z wybranymi parami został pobrany.')
        st.session_state['download_clicked'] = False  # Resetowanie flagi


# Uruchamianie skryptu obliczanie_sredniej.py dla każdej wybranej pary walutowej
if st.button('Przelicz statystyki dla wybranych par'):
    for pair in selected_pairs:
        currency_pair_key = pair.replace('/', '_').lower()
        
        # Uruchomienie skryptu obliczanie_sredniej.py
        process = subprocess.Popen(
            ['python', 'obliczanie_sredniej.py', currency_pair_key], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            # Prezentacja wyników
            result = stdout.decode().strip()
            st.write(f"Statystyki dla {pair}: {result}")
        else:
            st.error(f"Błąd podczas obliczania statystyk dla {pair}: {stderr.decode()}")
