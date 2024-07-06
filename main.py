import streamlit as st
import streamlit_option_menu as som
import pandas as pd
import pickle, person, BMI, Home
from tinydb import TinyDB, Query
import person
import os
from datetime import datetime

@st.cache(allow_output_mutation=True)
def load_data():
    db = TinyDB("data/PersonsDatabase.json")
    db.truncate()
    person.Person.load_person_data(db,"data/person_db.json")
    person.Person.load_person_data(db,"data/personstest.csv")
    return db

db = load_data()
#print(person.Person.find_person_data_by_id(db,5))
#print(person.Person.find_person_data_by_id(db,4))


with st.sidebar:
    selected_page = som.option_menu("Navigation", ["Home", "Benutzer auswählen", "Benutzer bearbeiten", "Neues EKG hinzufügen", "BMI-Rechner", "Trainingstagebuch"])

if selected_page == "Home":
    Home.home()
    
if selected_page == "Benutzer auswählen":
    st.title("Benutzer auswählen")
    st.write("This is the second page of my app.")

if selected_page == "Benutzer bearbeiten":
    AddDelUp = st.selectbox('Wähle eine Option aus:', ['Benutzer hinzufügen', 'Benutzer löschen', 'Benutzer bearbeiten'])
    
    if AddDelUp == 'Benutzer hinzufügen':
        st.title("Benutzer hinzufügen")

        col1,col2,col3 = st.columns(3)
        with col1:
            NewUserID = 1
            for entry in db:
                if NewUserID == entry['id']:
                    NewUserID += 1
            st.markdown(("ID: ",NewUserID))
            LabelYear = st.text_input("Geburtsjahr: ")
        with col2:
            LabelFirstname = st.text_input("Vorname: ")
            EKGUpload = st.file_uploader("EKG Datei hochladen: ",type=['csv'])
        with col3:
            LabelLastname = st.text_input("Nachname: ")
            PictureUpload = st.file_uploader("Bild Datei hochladen: ",type=['jpg','png','jpeg'])

        if st.button("Benutzer hinzufügen"):
            if LabelYear.strip() and LabelFirstname.strip() and LabelLastname.strip() and EKGUpload and PictureUpload and LabelYear.isnumeric():
                EKGUploadpath = os.path.join("data/ekg_data",EKGUpload.name)
                PictureUploadpath = os.path.join("data/pictures",PictureUpload.name)

                NewECGID = 1
                for user in db:
                    print(user['ekg_tests'])
                    for ecgtest in user['ekg_tests']:
                        if NewECGID == ecgtest['id']:
                            print(ecgtest['id'])
                            NewECGID += 1
                
                heute = datetime.today()
                datum_format = heute.strftime("%d-%m-%Y")

                EKGInfo = [{
                    "id":NewECGID,
                    "date":datum_format,
                    "result_link":EKGUploadpath}]

                with open(EKGUploadpath, 'wb') as f:
                    f.write(EKGUpload.getbuffer())
                with open(PictureUploadpath, 'wb') as f:
                    f.write(PictureUpload.getbuffer())
                person.Person.add_user(db,LabelFirstname,LabelLastname,LabelYear,NewUserID,EKGInfo,PictureUploadpath)
                st.write("Benutzer wurde hinzugefügt")
            else:
                st.write("Bitte alle Felder ausfüllen und Eingaben überprüfen")  
        




    if AddDelUp == 'Benutzer löschen':
        FeldID = st.text_input("ID")
        if type(FeldID) == str and FeldID.isnumeric():
            Daten = person.Person.find_person_data_by_id(db,int(FeldID))
            try:
                st.image(Daten[0]['picture_path'], caption='Ausgewählter User', use_column_width=True)
            except:
                st.image('data/pictures/none.jpg', caption='Kein Bild vorhanden', use_column_width=True)
            if st.button("Benutzer entfernen"):
                person.Person.del_user(db,int(FeldID))
                st.write("Benutzer wurde gelöscht")
                os.remove(Daten[0]['picture_path'])
                for ekg in Daten[0]['ekg_tests']:
                    os.remove(ekg["result_link"])
            if Daten == None:
                st.write("ID nicht gefunden")







    if AddDelUp == 'Benutzer bearbeiten':
        st.title("Benutzer bearbeiten")



    
    



    
    
    
    """
    col1,col2,col3 = st.columns(3)
    with col1:
        image_path = 'data/pictures/none.jpg'
        st.image(image_path, caption='User', use_column_width=True)
    with col2:
        FeldID = st.text_input("ID")
    with col3:
        def button1_action():
            st.write("Button 1 wurde gedrückt!")
        def button2_action():
            st.write("Button 2 wurde gedrückt!")
        def button3_action():
            st.write("Button 3 wurde gedrückt!")

        if st.button("Benutzer hinzufügen"):
            button1_action()
        if st.button("Benutzer löschen"):
            button2_action()
        if st.button("Benutzer bearbeiten"):
            button3_action()"""

if selected_page == "Neues EKG hinzufügen":
    st.title("Neues EKG hinzufügen")
    st.write("This is the fourth page of my app.")

if selected_page == "BMI-Rechner": 
   BMI.bmi_calc()

if selected_page == "Trainingstagebuch":
    st.title("Trainingstagebuch")

    # Funktion zum Erstellen des Standard-DataFrames
    def create_default_dataframe():
        return pd.DataFrame({
            "Wochentag": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
            "Sportart": [None, None, None, None, None, None, None],
            "Ort": [None, None, None, None, None, None, None],
            "Dauer": [None, None, None, None, None, None, None],
            "Kalorienverbrauch": [None, None, None, None, None, None, None],
            "Wetter": [None, None, None, None, None, None, None],
            "PartnerIn": [None, None, None, None, None, None, None],
        }).set_index("Wochentag")

    # Funktion zum Laden des DataFrames aus der Datei
    def load_dataframe(user_id):
        filename = f"{user_id}_edited_df.pkl"
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                return pickle.load(file)
        else:
            return create_default_dataframe()

    # Funktion zum Speichern des DataFrames in eine Datei
    def save_dataframe(df, user_id):
        filename = f"{user_id}_edited_df.pkl"
        with open(filename, "wb") as file:
            pickle.dump(df, file)

    # Beispiel-Benutzerliste
    user_list = person.Person.get_person_list(db)

    # Benutzer-ID auswählen
    user_id = st.selectbox("Benutzer auswählen", user_list)

    if user_id:
        # Laden des DataFrames für den spezifischen Benutzer
        df = load_dataframe(user_id)

        # Anzeige und Bearbeitung des DataFrames
        edited_df = st.data_editor(df)

        # Speicherung des bearbeiteten DataFrames in Session State
        st.session_state['edited_df'] = edited_df

        # Button zum Speichern des DataFrames in eine Datei
        if st.button("Daten speichern"):
            save_dataframe(st.session_state['edited_df'], user_id)
            st.success("Daten erfolgreich gespeichert!")

        # Button zum Zurücksetzen des DataFrames
        if st.button("Daten zurücksetzen"):
            reset_df = create_default_dataframe()
            save_dataframe(reset_df, user_id)
            st.session_state['edited_df'] = reset_df
            st.success("Daten erfolgreich zurückgesetzt!")

        st.write("Bearbeiten Sie den DataFrame und klicken Sie auf 'Daten speichern', um Änderungen zu speichern.")
        st.write("Klicken Sie auf 'Daten zurücksetzen', um den DataFrame auf die Standardwerte zurückzusetzen.")

    

