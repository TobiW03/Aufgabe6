import streamlit as st
import streamlit_option_menu as som
import pandas as pd

with st.sidebar:
    selected_page = som.option_menu("Navigation", ["Home", "Page 2", "Page 3", "BMI-Rechner"])

if selected_page == "Home":
    st.title("Fitnessapp")
    st.write("Sie befinden sich auf der Startseite der Fitnessapp.")
    st.image("Running.jpg")
    
if selected_page == "Page 2":
    st.title("Page 2")
    st.write("This is the second page of my app.")

if selected_page == "Page 3":
    st.title("Page 3")
    st.write("This is the third page of my app.")

if selected_page == "BMI-Rechner": 
    st.title("BMI-Rechner")
    weight = st.text_input("Gewicht in kg", None)
    height = st.text_input("Größe in cm", None)
    if st.button("BMI berechnen"):
        bmi = float(weight) / ((float(height) / 100) ** 2)
    try:
        st.write("Ihr BMI beträgt:", round(bmi, 2))
        if bmi < 18.5:
            weight_class = "Untergewicht"
        elif bmi < 25:
            weight_class = "Normalgewicht"
        elif bmi < 30:
            weight_class = "Übergewicht"
        elif bmi < 35:
            weight_class = "Adipositas Grad I"
        elif bmi < 40:
            weight_class = "Adipositas Grad II"
        else:
            weight_class = "Adipositas Grad III"
        st.write("Sie haben", weight_class, ".")
    except:
        pass
    st.write("Der BMI wird nach folgender Formel berechnet: Gewicht in kg / (Größe in m)²")
    st.header("BMI-Klassifikation")
    df = pd.DataFrame({
        "BMI": ["< 18.5", "18.5 - 24.9", "25 - 29.9", "30 - 34.9", "35 - 39.9", "≥ 40"],
        "Gewichtsklasse": ["Untergewicht", "Normalgewicht", "Übergewicht", "Adipositas Grad I", "Adipositas Grad II", "Adipositas Grad III"]
    })
    df = df.set_index("BMI")
    st.write(df)

    

