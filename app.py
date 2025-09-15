import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Load model
rfr = pickle.load(open("rfr.pkl", "rb"))

# Gender mapping
gender_map = {'Male': 0, 'Female': 1}

# Prediction function
def pred(Gender, Age, Height, Weight, Duration, Heart_rate, Body_temp,
         Activity, Steps, Time_of_day, Fitness_level):
    df = pd.DataFrame([[gender_map[Gender],
                        Age, Height, Weight, Duration,
                        Heart_rate, Body_temp]],
                      columns=['Gender', 'Age', 'Height', 'Weight',
                               'Duration', 'Heart_Rate', 'Body_Temp'])
    prediction = rfr.predict(df)
    return prediction[0]

# ----------------- CSS Styling -----------------
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------- Login System -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔑 Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":  # Dummy credentials
            st.session_state.logged_in = True
            st.success("✅ Login Successful!")
        else:
            st.error("❌ Invalid Username or Password")
else:
    # ----------------- Main App -----------------
    st.title("💪 Calories Burned Prediction App")
    st.markdown("This app estimates calories burned and suggests diet plans.")

    # User Inputs
    Gender = st.selectbox('Gender', list(gender_map.keys()))
    Age = st.slider('Age', 10, 80, 25)
    Height = st.slider('Height (cm)', 100, 220, 170)
    Weight = st.slider('Weight (kg)', 30, 150, 70)
    Duration = st.slider('Workout Duration (minutes)', 5, 180, 30)
    Heart_rate = st.slider('Heart Rate (bpm)', 60, 200, 120)
    Body_temp = st.slider('Body Temperature (°C)', 35.0, 42.0, 37.0)

    Activity = st.selectbox('Activity Type', ['Running', 'Walking', 'Cycling', 'Yoga', 'Swimming'])
    Steps = st.number_input('Steps Taken During Workout', min_value=0, value=1000)
    Time_of_day = st.selectbox('Time of Day', ['Morning', 'Afternoon', 'Evening', 'Night'])
    Fitness_level = st.selectbox('Fitness Level', ['Beginner', 'Intermediate', 'Advanced'])

    if st.button('Predict Calories Burned'):
        result = pred(Gender, Age, Height, Weight, Duration, Heart_rate, Body_temp,
                      Activity, Steps, Time_of_day, Fitness_level)
        st.success(f"🔥 Estimated Calories Burned: **{result:.2f} kcal**")

        # ----------------- Diet Plan -----------------
        st.subheader("🥗 Suggested Diet Plan")

        if result < 200:
            diet = {
                "Oats with milk": 150,
                "1 Banana": 100,
                "Green Tea": 30
            }
        elif result < 400:
            diet = {
                "2 Boiled Eggs": 150,
                "Grilled Chicken Salad": 250,
                "Apple": 80
            }
        else:
            diet = {
                "Brown Rice + Veg Curry": 350,
                "Paneer/Chicken Curry": 250,
                "Protein Shake": 200,
                "Fruit Bowl": 150
            }

        df_diet = pd.DataFrame(list(diet.items()), columns=["Food Item", "Calories (kcal)"])
        st.table(df_diet)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.success("🔒 Logged out successfully!")
