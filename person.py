import json
from datetime import datetime
from tinydb import TinyDB, Query
import os
import csv


class Person:
    @staticmethod
    def load_person_data(file_path):
        """A Function that knows where the person Database is and returns a Dictionary with the Persons"""
        def check_keys(d):
            """A Function that checks if the Dictionary has the required keys"""
            required_keys = {"firstname", "lastname", "date_of_birth", "id", "ekg_tests", "picture_path"}
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
                    IDCheck = Query()
                    user_id = element["id"]
                    result = db.search(IDCheck.id == user_id)
                    if result:
                        print("Error: The ID already exists in the database")
                        continue
                    else:
                        db.insert(element)

        elif file_extension == ".csv":
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not check_keys(row):
                        print("Error: The CSV file does not have the required keys")
                        return
                    else:
                        IDCheck = Query()
                        user_id = row["id"]
                        result = db.search(IDCheck.id == user_id)
                        if result:
                            print("Error: The ID already exists in the database")
                            continue
                        else:
                            db.insert(row)
        else:
            print("Bis jetzt nur json und csv Dateien unterstützt")

    @staticmethod
    def add_user(firstname, lastname, date_of_birth, id, ekg_tests, picture_path):
        """A Function that adds a new user to the person database"""
        data = {"firstname": firstname, 
                "lastname": lastname, 
                "date_of_birth": date_of_birth,
                "id": id,
                "ekg_tests": ekg_tests,
                "picture_path": picture_path}
        db.insert(data)
    
    @staticmethod
    def del_user(id):
        """A Function that deletes a user from the person database"""
        db.remove(doc_ids=[id])

    @staticmethod
    def get_person_list(db):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = [] #Liste für alle Namen

        for eintrag in db:
            list_of_names.append(eintrag.get("firstname") + " " + eintrag.get("lastname"))
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""
        fullname = suchstring.split(", ")
        fn = fullname[1]
        ln = fullname[0]

        # Abfrageobjekt für TinyDB erstellen
        Person = Query()
        # Eintrag in der Datenbank suchen
        Erg = db.search(Person.firstname == fn and Person.lastname == ln)
        if Erg:
            return (Erg)
        else:
            return None
        
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
    Person.load_person_data("data/person_db.json")
    Person.load_person_data("data/personstest.csv")
    print(Person.get_person_list(db))
    print(Person.find_person_data_by_name("Wannenmacher, Tobias"))
    Person1 = Person(db.get(doc_id=1))
    print(Person1.maxHR)

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