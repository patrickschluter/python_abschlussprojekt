import csv
from pathlib import Path
from datetime import datetime
import subprocess

def neues_ticket():
    print()
    print("===== Neues Ticket erstellen =====")

    name = input("Name: ")
    abteilung = input("Abteilung: ")
    problem = input("Problem: ")
    prioritaet = input("Priorität: ")
    status = input("Status: ")

    with open("tickets/neue_tickets.txt", "a", encoding="utf-8") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Abteilung: {abteilung}\n")
        file.write(f"Problem: {problem}\n")
        file.write(f"Priorität: {prioritaet}\n")
        file.write(f"Status: {status}\n")
        file.write("------------------------------\n")

    print("Das Ticket wurde erfolgreich gespeichert.")

def tickets_anzeigen():
    print()
    print("===== Bestehende Tickets =====")

    try:
        with open("data/tickets.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for ticket in reader:
                print("------------------------------")
                print("Ticket-ID:", ticket["ticket_id"])
                print("Name:", ticket["name"])
                print("Abteilung:", ticket["abteilung"])
                print("Problem:", ticket["problem"])
                print("Priorität:", ticket["prioritaet"])
                print("Status:", ticket["status"])

    except FileNotFoundError:
        print("Die Datei tickets.csv wurde nicht gefunden.")

def benutzer_anzeigen():
    print()
    print("===== Benutzerliste =====")

    try:
        with open("data/benutzer.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for benutzer in reader:
                print("------------------------------")
                print("Username:", benutzer["username"])
                print("Name:", benutzer["name"])
                print("Abteilung:", benutzer["abteilung"])
                print("Rolle:", benutzer["rolle"])
                print("Status:", benutzer["status"])

                if benutzer["status"] != "aktiv":
                    print("ACHTUNG: Dieser Benutzer ist nicht aktiv!")

    except FileNotFoundError:
        print("Die Datei benutzer.csv wurde nicht gefunden.")

def inventar_anzeigen():
    print()
    print("===== Inventarliste =====")

    try:
        with open("data/inventar.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for geraet in reader:
                print("------------------------------")
                print("Geräte-ID:", geraet["geraete_id"])
                print("Gerät:", geraet["geraet"])
                print("Benutzer:", geraet["benutzer"])
                print("Abteilung:", geraet["abteilung"])
                print("Standort:", geraet["standort"])
                print("Status:", geraet["status"])

                if geraet["status"] == "defekt":
                    print("WARNUNG: Gerät ist defekt!")
                elif geraet["status"] == "wartung":
                    print("WARNUNG: Gerät befindet sich in Wartung!")
                elif geraet["status"] == "verloren":
                    print("WARNUNG: Gerät wurde als verloren gemeldet!")

    except FileNotFoundError:
        print("Die Datei inventar.csv wurde nicht gefunden.")

def logdatei_durchsuchen():
    print()
    print("===== Logdatei durchsuchen =====")

    suchwort = input("Suchwort eingeben: ")

    try:
        with open("logs/server.log", "r", encoding="utf-8") as file:
            gefunden = False

            for zeile in file:
                if suchwort.lower() in zeile.lower():
                    print(zeile.strip())
                    gefunden = True

            if not gefunden:
                print("Keine passenden Einträge gefunden.")

    except FileNotFoundError:
        print("Die Datei server.log wurde nicht gefunden.")

def ordner_analysieren():
    print()
    print("===== Ordner analysieren =====")

    pfad = Path(input("Ordnerpfad eingeben: "))

    if pfad.exists() and pfad.is_dir():
        dateien = 0
        ordner = 0

        for eintrag in pfad.iterdir():
            if eintrag.is_file():
                dateien += 1
            elif eintrag.is_dir():
                ordner += 1

        print("Dateien:", dateien)
        print("Unterordner:", ordner)

    else:
        print("Der Ordner wurde nicht gefunden.")

def systemreport_erstellen():
    print()
    print("===== Systemreport erstellen =====")

    try:
        arbeitsverzeichnis = Path.cwd()

        # Prüfen, ob die Logdatei vorhanden ist
        logdatei = Path("logs/server.log")

        if not logdatei.exists():
            print("Die Logdatei wurde nicht gefunden.")
            return

        # Prüfen, ob der Reports-Ordner vorhanden ist
        reports_ordner = Path("reports")
        reports_ordner.mkdir(exist_ok=True)

        # Dateien im Projektordner zählen
        dateien = 0

        for eintrag in arbeitsverzeichnis.rglob("*"):
            if eintrag.is_file():
                dateien += 1

        # Einfachen Systembefehl ausführen
        result = subprocess.run(
            ["whoami"],
            capture_output=True,
            text=True
        )

        benutzer = result.stdout.strip()

        # ERROR und WARN zählen
        error_count = 0
        warn_count = 0

        with open(logdatei, "r", encoding="utf-8") as file:
            for zeile in file:
                if "ERROR" in zeile.upper():
                    error_count += 1

                if "WARN" in zeile.upper():
                    warn_count += 1

        # Systemreport schreiben
        with open(
            "reports/system_report.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write("===== SYSTEMREPORT =====\n")
            file.write(f"Datum und Uhrzeit: {datetime.now()}\n")
            file.write(f"Arbeitsverzeichnis: {arbeitsverzeichnis}\n")
            file.write(f"Anzahl Dateien im Projektordner: {dateien}\n")
            file.write(f"Aktueller Benutzer: {benutzer}\n")
            file.write(f"ERROR-Einträge im Log: {error_count}\n")
            file.write(f"WARN-Einträge im Log: {warn_count}\n")

            if error_count > 0 or warn_count > 0:
                file.write(
                    "Zusammenfassung: Warnungen oder Fehler gefunden.\n"
                )
            else:
                file.write(
                    "Zusammenfassung: Keine Warnungen oder Fehler gefunden.\n"
                )

        print("Der Systemreport wurde erfolgreich erstellt.")

    except FileNotFoundError as fehler:
        print("Eine benötigte Datei wurde nicht gefunden:", fehler)

    except Exception as fehler:
        print("Beim Erstellen des Reports ist ein Fehler aufgetreten:", fehler)

def menue():
    while True:
        print()
        print("======================================")
        print(" IT-Support und Systemadmin Diagnose-Tool")
        print("======================================")
        print("1. Neues Ticket erstellen")
        print("2. Bestehende Tickets anzeigen")
        print("3. Benutzerliste anzeigen")
        print("4. Inventarliste anzeigen")
        print("5. Logdatei durchsuchen")
        print("6. Ordner analysieren")
        print("7. Systemreport erstellen")
        print("8. Programm beenden")
        print()

        auswahl = input("Auswahl eingeben: ")

        if auswahl == "1":
             neues_ticket()
        elif auswahl == "2":
            tickets_anzeigen()
        elif auswahl == "3":
             benutzer_anzeigen()
        elif auswahl == "4":
             inventar_anzeigen()
        elif auswahl == "5":
             logdatei_durchsuchen()
        elif auswahl == "6":
             ordner_analysieren()
        elif auswahl == "7":
             systemreport_erstellen()
        elif auswahl == "8":
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte eine Zahl von 1 bis 8 eingeben.")


menue()