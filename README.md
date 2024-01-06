# hrblockwise

Stworzyłem osobne pliki dla każdego skryptu, oraz REST dla możliwości skalowania / wyboru dowolnego UI/UX.
Dzięki temu w każdym momencie można zmienić funkcje jednego, co nie wpłynie na pracę innych aplikacji.

app.py - UI oparte o streamlit - streamlit run app.py - z poziomu UI można zarządzać wszystkimi aplikacjiami.  

api.py - uruchamia się automatycznie przy starcie streamlit API dla odczytu bazy danych, czy uruchamiania wybranych aplikacji.

kursywalut.py - pobiera dane z API wybranych kursów walut + uruchamia przelicznik.py

W przypadku zadania nie trzeba było jej tworzyć, lecz zachowując logikę skalowalności, można ją rozbudować o kolejne funkcje
przelicznik.py - autonomiczna aplikacja obserwująca zmiany w bazie danych co 60 sekund. Jeśli nastąpią zmiany <pobranie nowych danych> przelicza dodatkowe pary i dodaje je do bazy.

wyswietl_dane.py - prosty skrypt do sprawdzenia co się znajduje w bazie danych w konsoli - uruchamiany tylko w konsoli

cyklicznie.py - odpowiada za reagularne pobieranie danych

musiałem zrobić kilka rzeczy na subproccess ze względu na zależności od gotowych rozwiązań streamlit. Wywalało mi je API, a zapewne musiałbym zapisać wyniki do sesji usera - np. bazy lub cashe i dopiero wtedy mógłbym uruchomić całą resztę po API
