import streamlit as st
import streamlit_option_menu as som

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
    weight = st.text_input("Gewicht in kg")
    height = st.text_input("Größe in cm")
