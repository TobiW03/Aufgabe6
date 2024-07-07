import json
from datetime import datetime
from tinydb import TinyDB, Query
import os
import csv
import pandas as pd
import ast

class Person:
    @staticmethod
    def load_person_data(database,file_path):
        """A Function that knows where the person Database is and returns a Dictionary with the Persons"""
        def check_keys(d):
            """A Function that checks if the Dictionary has the required keys"""
            required_keys = {"firstname", "lastname", "date_of_birth", "id", "picture_path"}
            return required_keys.issubset(d.keys())
        def detect_file_type(file_path):
            """A Function that detects the file type of a file"""
            _, file_extension = os.path.splitext(file_path)
            return file_extension.lower()
        file_extension = detect_file_type(file_path)

        if file_extension == ".json":
            file = open(file_path)
            person_data = json.load(file)
            for element in person_data:
                if not check_keys(element):
                    print("Error: The JSON file does not have the required keys")
                    return
                else:
                    #Trainingstagebuch einfügen
                    IDCheck = Query()
                    user_id = element["id"]
                    result = database.search(IDCheck.id == user_id)
                    if result:
                        print("Error: The ID already exists in the database")
                        continue
                    else:
                        if 'diary' not in element:
                            element['diary'] = pd.DataFrame({
                            "Wochentag": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                            "Sportart": [None, None, None, None, None, None, None],
                            "Ort": [None, None, None, None, None, None, None],
                            "Dauer": [None, None, None, None, None, None, None],
                            "Kalorienverbrauch": [None, None, None, None, None, None, None],
                            "Wetter": [None, None, None, None, None, None, None],
                            "PartnerIn": [None, None, None, None, None, None, None],
                            })
                            element['diary'] = element['diary'].set_index("Wochentag")
                            element['diary'] = element['diary'].to_dict()
                            database.insert(element)
                        else:
                            database.insert(element)

        elif file_extension == ".csv":
            with open(file_path, mode='r', newline='',encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(row)
                    if not check_keys(row):
                        print("Error: The CSV file does not have the required keys")
                        return
                    else:

                        row["ekg_tests"] = [{
                            'id': int(row["ecg_id"]), 
                            'date': row["date"], 
                            'result_link': row["result_link"]}]
                        row.pop("ecg_id", None)
                        row.pop("date", None)
                        row.pop("result_link", None)

                        "Trainingstagebuch einfügen"
                        IDCheck = Query()
                        user_id = row["id"]
                        result = database.search(IDCheck.id == user_id)
                        if result:
                            print("Error: The ID already exists in the database")
                            continue
                        else:
                            if type(row['id']) == str:
                                row['id'] = int(row['id'])
                            if 'diary' not in row or row['diary'] == "":
                                row['diary'] = pd.DataFrame({
                                "Wochentag": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                "Sportart": [None, None, None, None, None, None, None],
                                "Ort": [None, None, None, None, None, None, None],
                                "Dauer": [None, None, None, None, None, None, None],
                                "Kalorienverbrauch": [None, None, None, None, None, None, None],
                                "Wetter": [None, None, None, None, None, None, None],
                                "PartnerIn": [None, None, None, None, None, None, None],
                                })
                                row['diary'] = row['diary'].set_index("Wochentag")
                                row['diary'] = row['diary'].to_dict()
                                database.insert(row)
                            else:
                                database.insert(row)
        else:
            print("Bis jetzt nur json und csv Dateien unterstützt")

    @staticmethod
    def add_user(database,firstname, lastname, date_of_birth, id, ekg_tests, picture_path): #updaten
        """A Function that adds a new user to the person database"""
        data = {"firstname": firstname, 
                "lastname": lastname, 
                "id": id, 
                "date_of_birth": date_of_birth, 
                "picture_path": picture_path, 
                "ekg_tests": ekg_tests, 
                "diary": pd.DataFrame({
                                "Wochentag": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                "Sportart": [None, None, None, None, None, None, None],
                                "Ort": [None, None, None, None, None, None, None],
                                "Dauer": [None, None, None, None, None, None, None],
                                "Kalorienverbrauch": [None, None, None, None, None, None, None],
                                "Wetter": [None, None, None, None, None, None, None],
                                "PartnerIn": [None, None, None, None, None, None, None],
                                })}
        data['diary'] = data['diary'].set_index("Wochentag")
        data['diary'] = data['diary'].to_dict()
        database.insert(data)
    
    @staticmethod
    def del_user(database,id): #updaten
        """A Function that deletes a user from the person database"""
        database.remove(doc_ids=[id])

    @staticmethod
    def update_user(database,id, firstname, lastname, date_of_birth, ekg_tests, picture_path):
        """A Function that updates a user in the person database"""
        # Abfrageobjekt für TinyDB erstellen
        Person = Query()
        # Eintrag in der Datenbank suchen
        Erg = database.search(Person.id == id)
        if Erg:
            # Eintrag in der Datenbank aktualisieren
            database.update({"firstname": firstname, 
                        "lastname": lastname, 
                        "id": id, 
                        "date_of_birth": date_of_birth, 
                        "picture_path": picture_path, 
                        "ekg_tests": ekg_tests}, Person.id == id)
        else:
            print("Person nicht gefunden")

    @staticmethod
    def get_person_list(db):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = [] #Liste für alle Namen

        for eintrag in db:
            list_of_names.append(eintrag.get("firstname") + " " + eintrag.get("lastname"))
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(database,suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""
        fullname = suchstring.split(" ")
        fn = fullname[0]
        ln = fullname[1]

        # Abfrageobjekt für TinyDB erstellen
        Person = Query()
        # Eintrag in der Datenbank suchen
        Erg = database.search(Person.firstname == fn and Person.lastname == ln)
        if Erg:
            return (Erg)
        else:
            return None
        
    @staticmethod
    def find_person_data_by_id(database,id):
        """ Eine Funktion der die ID übergeben wird
        und die die Person als Dictionary zurück gibt"""
        # Abfrageobjekt für TinyDB erstellen
        Person = Query()
        # Eintrag in der Datenbank suchen
        Erg = database.search(Person.id == id)
        if Erg:
            return (Erg)
        else:
            return None

    ### Sporttagebuch
    def diary(self):
        """Funktion zum Erstellen des Standard-DataFrames d. Sporttagebuchs"""
        for eintrag in db:
            if eintrag["id"] == self.id:
                if eintrag["diary"] == []: #Wenn das Trainingstagebuch leer ist
                    self.dfdiary = pd.DataFrame({
                    "Wochentag": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                    "Sportart": [None, None, None, None, None, None, None],
                    "Ort": [None, None, None, None, None, None, None],
                    "Dauer": [None, None, None, None, None, None, None],
                    "Kalorienverbrauch": [None, None, None, None, None, None, None],
                    "Wetter": [None, None, None, None, None, None, None],
                    "PartnerIn": [None, None, None, None, None, None, None],
                    })
                    self.dfdiary = self.dfdiary.set_index("Wochentag")
                else:
                    self.dfdiary = pd.DataFrame(eintrag["diary"])
                    #self.dfdiary = self.dfdiary.set_index("Wochentag")
            else:
                print("Person nicht gefunden")
    
    #unklar, ob Funktion noch benötigt wird
    def load_dataframe(self,user_id):
        """Funktion zum Laden des DataFrames aus einer Datei"""
        filename = f"{user_id}_edited_df.pkl"
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                return pickle.load(file)
        else:
            return create_default_dataframe()
    #unklar, ob Funktion noch benötigt wird
    def save_dataframe(df, user_id):
        """Funktion zum Speichern des DataFrames in einer Datei"""
        filename = f"{user_id}_edited_df.pkl"
        with open(filename, "wb") as file:
            pickle.dump(df, file)
    
        
    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.age = self.calc_age()
        self.maxHR = self.calc_max_heart_rate()
        self.ecg_data = person_dict["ekg_tests"]
        self.ecg_result_link = person_dict["ekg_tests"][0]["result_link"]
        self.trainingsdiary = self.diary()

        #Speichern
        for eintrag in db:
            if eintrag.get('id') == self.id:
                # Neuen Wert hinzufügen oder vorhandenen Wert aktualisieren
                data_dict = self.dfdiary.to_dict()
                eintrag['diary'] = data_dict
                # Eintrag aktualisieren                    
                db.update(eintrag, doc_ids=[eintrag.doc_id])
                break
            else:
                print("Person nicht gefunden")
        return self.dfdiary

    def calc_age(self):
        date = datetime.now()
        currentyear = date.year
        age = currentyear - self.date_of_birth
        return age

    def calc_max_heart_rate(self):
        maxHR = 220-self.age
        return maxHR

    @staticmethod
    def load_by_id(id, personOBJ):
        id_found = False
        for person in personOBJ:
            if person.id == id:
                print({
                    "id": person.id,
                    "date_of_birth": person.date_of_birth,
                    "first_name": person.firstname,
                    "last_name": person.lastname,
                    "picture_path": person.picture_path,
                    "ekg_datei": person.ecg_result_link
                })
                id_found = True
                break
        if not id_found:
            print("ID not found")

if __name__ == "__main__":
    db = TinyDB("data/PersonsDatabase.json")
    db.truncate()
    Person.load_person_data(db,"data/person_db.json")
    Person.load_person_data(db,"data/personstest.csv")
    #print(Person.get_person_list(db))




    print(Person.find_person_data_by_name(db,"Julian Huber"))
    #print(Person.find_person_data_by_id(db,3))
    #Person1 = Person(db.get(doc_id=1))
    #print(Person1.maxHR)
    db.close()
    """
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    print(person_names)
    Person1 = Person(persons[0])
    Person2 = Person(persons[1])
    Person3 = Person(persons[2])
    #print(Person.find_person_data_by_name("Huber, Julian"))
    person_instances = [Person1, Person2, Person3]
    Person.load_by_id(3, person_instances)"""