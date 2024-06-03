import fitparse

# Pfad zur FIT-Datei
fitfile_path = 'data/Fitfiles/FitFile.fit'

# FIT-Datei öffnen
fitfile = fitparse.FitFile(fitfile_path)

# Durchlaufe alle Nachrichten in der FIT-Datei
for record in fitfile.get_messages():
    # Jede Nachricht besteht aus Feldern
    for field in record:
        print(field.name, field.value)