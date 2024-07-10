import streamlit as st

def calculate_calories(sex, age, weight, height, activity_level):
    """Funktion zur Berechnung des täglichen Kalorienbedarfs."""
    if sex == "Männlich":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    activity_multipliers = {
        "Kaum oder gar keine Bewegung": 1.2,
        "Leichte Bewegung (1-3 Tage/Woche)": 1.375,
        "Mäßig aktive Bewegung (3-5 Tage/Woche)": 1.55,
        "Starke aktive Bewegung (6-7 Tage/Woche)": 1.725,
        "Sehr starke aktive Bewegung (zweimal täglich)": 1.9
    }
    
    calories = bmr * activity_multipliers[activity_level]
    return calories

def nutrition_advice():
    """Funktion zur Ernährungsberatung."""

    st.header("Ernährungsberatung")
    
    goal = st.selectbox("Ziel auswählen", ["Definierter werden", "Form halten", "Mehr Masse aufbauen"])
   

    st.header("Kalorienrechner")
    
    sex = st.selectbox("Geschlecht", ["Männlich", "Weiblich"])
    age = st.number_input("Alter", min_value=5, max_value=120, value=5, step=1)
    weight = st.number_input("Gewicht (kg)", min_value=10, max_value=300, value=10, step=1)
    height = st.number_input("Größe (cm)", min_value=100, max_value=250, value=100, step=1)
    activity_level = st.selectbox("Aktivitätslevel", [
        "Kaum oder gar keine Bewegung",
        "Leichte Bewegung (1-3 Tage/Woche)",
        "Mäßig aktive Bewegung (3-5 Tage/Woche)",
        "Starke aktive Bewegung (6-7 Tage/Woche)",
        "Sehr starke aktive Bewegung (zweimal täglich)"
    ])
    
    if st.button("Kalorienbedarf berechnen"):
        calories = calculate_calories(sex, age, weight, height, activity_level)
        st.write(f"Ihr geschätzter täglicher Kalorienbedarf beträgt: {calories:.2f} kcal")
        
        if goal == "Definierter werden":
            st.header("Definierter werden")
            st.write("""
            Um definierter zu werden, sollte man auf eine ausgewogene Ernährung achten, die reich an Proteinen und Ballaststoffen ist. 
            Gleichzeitig sollte man den Konsum von Zucker und gesättigten Fetten reduzieren. Hier sind einige Tipps:
            - Erhöhe deinen Proteinverbrauch (z.B. durch mageres Fleisch, Fisch, Eier, Bohnen und Nüsse).
            - Iss mehr Gemüse und Früchte.
            - Reduziere den Konsum von verarbeiteten Lebensmitteln.
            - Trinke ausreichend Wasser.
            - Vermeide zuckerhaltige Getränke und Snacks.
            """)

        elif goal == "Form halten":
            st.header("Form halten")
            st.write("""
            Um deine aktuelle Form zu halten, ist es wichtig, eine ausgewogene und abwechslungsreiche Ernährung beizubehalten.
            Hier sind einige Tipps:
            - Achte auf eine ausgewogene Mischung aus Kohlenhydraten, Proteinen und Fetten.
            - Halte deine Portionsgrößen im Auge.
            - Integriere regelmäßig Bewegung und Sport in deinen Alltag.
            - Trinke ausreichend Wasser.
            - Gönne dir gelegentlich auch mal etwas, das dir besonders gut schmeckt, aber achte darauf, dass es nicht zur Gewohnheit wird.
            """)

        elif goal == "Mehr Masse aufbauen":
            st.header("Mehr Masse aufbauen")
            st.write("""
            Um mehr Masse aufzubauen, musst du sicherstellen, dass du mehr Kalorien zu dir nimmst, als du verbrauchst.
            Hier sind einige Tipps:
            - Erhöhe deine Kalorienaufnahme durch gesunde und nährstoffreiche Lebensmittel.
            - Konsumiere ausreichend Proteine (z.B. durch Fleisch, Fisch, Eier, Milchprodukte, Hülsenfrüchte).
            - Achte auf eine gute Mischung aus Kohlenhydraten und gesunden Fetten.
            - Integriere Krafttraining in dein Fitnessprogramm.
            - Trinke ausreichend Wasser.
            """)
