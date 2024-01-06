import schedule
import subprocess
import time

def run_script():
    print("Uruchamianie skryptu kursywalut.py...")
    subprocess.run(["python", "kursywalut.py"])

# Planowanie zadania codziennie o 12:00
schedule.every().day.at("12:00").do(run_script)

print("Zaplanowano uruchamianie skryptu kursywalut.py codziennie o 12:00")

# Pętla nieskończona, aby utrzymać proces działający
while True:
    schedule.run_pending()
    time.sleep(1)
