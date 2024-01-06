from flask import Flask, jsonify, request
import sqlite3
import subprocess

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('currency_data.db')
    conn.row_factory = sqlite3.Row  # To umożliwi dostęp do danych przez indeksy i nazwy kolumn
    return conn

@app.route('/api/data', methods=['GET'])
def get_data():
    filter_query = request.args.get('filter', '')  # Pobierz parametr 'filter' z URL-a
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Zmodyfikowane zapytanie, aby pobrać tylko kolumny z parami walutowymi oraz datę
    query = "SELECT date, eur_pln, usd_pln, chf_pln, eur_usd, eur_chf FROM currency_rates"
    if filter_query:
        query += " WHERE eur_pln LIKE ? OR usd_pln LIKE ? OR chf_pln LIKE ?"
        rows = cursor.execute(query, ('%' + filter_query + '%', '%' + filter_query + '%', '%' + filter_query + '%')).fetchall()
    else:
        rows = cursor.execute(query).fetchall()
    
    conn.close()
    
    # Konwertuj dane do formatu JSON
    data = [dict(ix) for ix in rows]
    return jsonify(data)

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Uruchomienie skryptu w tle
        subprocess.Popen(['python', 'kursywalut.py'])
        return jsonify({'message': 'Skrypt kursywalut.py został uruchomiony.'}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

