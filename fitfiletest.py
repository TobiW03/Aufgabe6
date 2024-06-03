import fitparse

# Pfad zur FIT-Datei
fitfile_path = 'data/Fitfiles/FitFile.fit'

# FIT-Datei öffnen
fitfile = fitparse.FitFile(fitfile_path)

# Menge für die einzigartigen Nachrichtentypen
unique_message_types = set()

# Durchlaufe alle Nachrichten in der FIT-Datei
for record in fitfile.get_messages():
    # Füge den Nachrichtentyp zur Menge der einzigartigen Nachrichtentypen hinzu
    unique_message_types.add(record.name)

# Ausgabe der einzigartigen Nachrichtentypen
print("Einzigartige Nachrichtentypen:")
for message_type in unique_message_types:
    print(message_type)