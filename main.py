import streamlit as st
import streamlit_option_menu as som
import pandas as pd
import BMI, Home
from tinydb import TinyDB, Query
import person
import os
from datetime import datetime
import ekgdata
import Ernährungsberatung

@st.cache(allow_output_mutation=True)
def load_data():
    """Cache für das Laden der Datenbanken und der EKG-Datenbank."""
    db = TinyDB("data/PersonsDatabase.json")
    db.truncate()
    person.Person.load_person_data(db,"data/person_db.json")
    person.Person.load_person_data(db,"data/personstest.csv")
    dbecg = TinyDB("data/EKGDatabase.json")
    dbecg.truncate()
    ekgdata.EKGdata.load_ekg_data(dbecg,"data/person_db.json")
    return db,dbecg

db,dbecg = load_data()

with st.sidebar:
    selected_page = som.option_menu("Navigation", ["Home", "Kalorienrechner", "Benutzer bearbeiten", "EKGs", "BMI-Rechner", "Trainingstagebuch"])

if selected_page == "Home": #Homepage
    Home.home()

if selected_page == "Benutzer bearbeiten": #Benutzer hinzufügen, löschen, bearbeiten
    AddDelUp = st.selectbox('Wähle eine Option aus:', ['Benutzer hinzufügen', 'Benutzer löschen', 'Benutzer bearbeiten'])
    
    if AddDelUp == 'Benutzer hinzufügen':
        st.title("Benutzer hinzufügen")
        col1,col2,col3 = st.columns(3)
        with col1:
            NewUserID = 1
            for entry in db: #jeder User mit neuer ID, welche noch nicht vergeben ist und die niedrigst freiest mögliche nimmt.
                if NewUserID == entry['id']:
                    NewUserID += 1
            st.markdown(("ID: ",NewUserID))
            LabelYear = st.text_input("Geburtsjahr: ")
        with col2:
            LabelFirstname = st.text_input("Vorname: ")
            EKGUpload = st.file_uploader("EKG Datei hochladen: ",type=['csv','txt'])
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
            Bild = True
            try:
                st.image(Daten[0]['picture_path'], caption='Ausgewählter User', use_column_width=True)
            except:
                st.image('data/pictures/none.jpg', caption='Kein Bild vorhanden', use_column_width=True)
                Bild = False
            if st.button("Benutzer entfernen"):
                person.Person.del_user(db,int(FeldID))
                st.write("Benutzer wurde gelöscht")
                if Bild == True:
                    os.remove(Daten[0]['picture_path'])
                    for ekg in Daten[0]['ekg_tests']:
                        os.remove(ekg["result_link"])
            if Daten == None:
                st.write("ID nicht gefunden")

    if AddDelUp == 'Benutzer bearbeiten':
        st.title("Benutzer bearbeiten")
        user_list = person.Person.get_person_list(db)
        # Benutzer-ID auswählen
        user_id = st.selectbox("Benutzer auswählen", user_list)
        Daten = person.Person.find_person_data_by_name(db,user_id)
        col1,col2,col3 = st.columns(3)
        with col1:
            LabelFirstname = st.text_input("Vorname",value=(Daten[0]['firstname']))
            LabelPic = st.text_input("Dateipfad zum Bild",value=(Daten[0]['picture_path']))
        with col2:
            LabelLastname = st.text_input('Nachname',value=(Daten[0]['lastname']))
        with col3:
            LabelBirth = st.text_input('Geburtsjahr',value=(Daten[0]['date_of_birth']))
            try:
                st.image(Daten[0]['picture_path'], caption='User', use_column_width=True)
            except:
                st.image('data/pictures/none.jpg', caption='Kein Bild vorhanden', use_column_width=True)
        if st.button("Benutzerdaten ändern"):
            if LabelFirstname.strip() and LabelLastname.strip() and LabelBirth.strip() and LabelBirth.isnumeric():
                person.Person.update_user(db,Daten[0]['id'],LabelFirstname,LabelLastname,LabelBirth,Daten[0]['ekg_tests'],LabelPic)
                st.write("Benutzerdaten wurden geändert")
            else:
                st.write("Bitte alle Felder ausfüllen und Eingaben überprüfen")

    
    

if selected_page == "EKGs":
    st.title("Neues EKG hinzufügen")
    user_list = person.Person.get_person_list(db)
    # Benutzer-ID auswählen
    user_id = st.selectbox("Benutzer auswählen", user_list)
    Datenecg = person.Person.find_person_data_by_name(db,user_id)
    if len(Datenecg[0]['ekg_tests']) > 1:
        slider_value = st.slider('Wähle einen Wert:', min_value=0, max_value=(len(Datenecg[0]['ekg_tests'])-1), value=0, step=1)
        EKGs = ekgdata.EKGdata(Datenecg[0]['ekg_tests'][slider_value])
        st.plotly_chart(EKGs.fig)
        st.write("EKG-ID: ",EKGs.id)
        st.write("EKG-Datum",EKGs.date)
        st.write("EKG-estimated HR",round(EKGs.estimated_hr,2))
        if EKGs.estimated_hr > 100:
            st.write("Rhytmisch, Tachykard")
        elif EKGs.estimated_hr > 60:
            st.write("Rhytmisch, normofrequent")
        else:
            st.write("Rhythmisch, bradykard")
    else:
        try:
            EKG = ekgdata.EKGdata(Datenecg[0]['ekg_tests'][0])
            st.plotly_chart(EKG.fig)
            st.write("EKG-ID: ",EKG.id)
            st.write("EKG-Datum",EKG.date)
            st.write("EKG-estimated HR",round(EKG.estimated_hr,2))
            if EKG.estimated_hr > 100:
                st.write("Rhytmisch, Tachykard")
            elif EKG.estimated_hr > 60:
                st.write("Rhytmisch, normofrequent")
            else:
                st.write("Rhythmisch, bradykard")
        except:
            st.write("Keine EKG-Daten gefunden.")

if selected_page == "BMI-Rechner": 
   BMI.bmi_calc()

if selected_page == "Kalorienrechner":
    st.title("Ernährungsberatung & Kalorienrechner")
    Ernährungsberatung.nutrition_advice()

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
        datas = person.Person.find_person_data_by_name(db,user_id)
        df = pd.DataFrame(datas[0]['diary'])
        return df

    # Funktion zum Speichern des DataFrames in eine Datei
    def save_dataframe(df, user_id):
        Daten = person.Person.find_person_data_by_name(db,user_id)
        df_dict = df.to_dict(orient="records")
        person.Person.update_diary(db,Daten[0]['id'],df_dict)

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