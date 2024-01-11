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


# Recruitment task

# Junior Python Dev

### Required Skills:

- Python 3 Knowledge: Proficiency and experience in Python programming, including scripting and process optimization, ability to implement Object-Oriented Programming (OOP).
- Linux Terminal Proficiency: Ability to work in a Linux environment, including terminal operation and performing system-level tasks.
- Database and SQL Knowledge: Understanding of PostgreSQL/MySQL databases, the ability to create and manage databases (working with the aggregation of different databases).
- API Usage: Proficiency in utilizing APIs for language translation or other services.
- Flexibility: Readiness to work on diverse tasks that may frequently change, openness to learning, and the ability to quickly acquire new skills and tools.
- Creativity and Problem-Solving: Ability to think creatively and find innovative solutions for various tasks and problems.

### Additional Advantages:

- Familiarity with containerization (Docker).
- Experience with Text-to-Image models, NLP (Natural Language Processing).

---

# To do:

### Fetching Currency Data:

- Utilizing the website https://api.nbp.pl/ and Python, retrieve exchange rates for EUR/PLN, USD/PLN, and CHF/PLN for the last 90 days.
- Save this data in separate columns. Additionally, create two more columns containing the EUR/USD and CHF/USD rates, calculated based on the retrieved data.

### Data Selection:

- Allow the user to input the name of the currency pairs they wish to access information for. Ideally, enable the user to specify multiple currency pairs.
- Filter the data to only include rows relevant to the chosen currency pairs.

### Saving Data:

- Save all the previously mentioned data (dates and rates for five pairs) into a CSV file named "all_currency_data.csv".
- Develop a function to permit the saving of only the user-selected currency pairs to a CSV file named "selected_currency_data.csv".
    - The CSV should retain the columns from the original file but only for the currencies selected by the user.
    - Store the filtered data in the CSV file.

### User Interaction:

- After saving the data, display a confirmation message such as "Data for [Currency] has been saved!"

### Error Handling:

- Create and implement appropriate error handling mechanisms for potential issues that might arise during the execution of the script. Ensure that the user is informed in a user-friendly manner about any errors that occur.

### Data Analysis:

- Develop a Python function that calculates and displays the average rate value, median, minimum, and maximum for the selected currency pair.

### Add:

- Implement functionality for the script to run daily at 12:00 PM and automatically save the data to the "all_currency_data.csv" file. Ensure that each script execution overwrites the file only with new entries.

### Reflection:

- Describe in text why you decided to perform the task in the chosen way. Provide insights into your decision-making process, the rationale behind your choices, and any considerations or trade-offs you made. This will help in understanding your approach and thought process.
