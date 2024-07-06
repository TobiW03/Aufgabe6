import streamlit as st
import streamlit_option_menu as som
import pandas as pd
import pickle, person, BMI, Home

with st.sidebar:
    selected_page = som.option_menu("Navigation", ["Home", "Benutzer auswählen", "Neuen Benutzer hinzufügen", "Neues EKG hinzufügen", "BMI-Rechner", "Trainingstagebuch"])

if selected_page == "Home":
    Home.home()
    
if selected_page == "Benutzer auswählen":
    st.title("Benutzer auswählen")
    st.write("This is the second page of my app.")

if selected_page == "Neuen Benutzer hinzufügen":
    st.title("Neuen Benutzer hinzufügen")
    st.write("This is the third page of my app.")

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

    

