import streamlit as st
import numpy as np
import pandas as pd
import pickle

rfr = pickle.load(open("rfr.pkl", "rb"))

gender_map = {'Male': 0, 'Female': 1}

def pred(Gender, Age, Height, Weight, Duration, Heart_rate, Body_temp,
         Activity, Steps, Time_of_day, Fitness_level):
    """
    Prediction function: only uses the features the model was trained on
    """
    df = pd.DataFrame([[
        gender_map[Gender],
        Age,
        Height,
        Weight,
        Duration,
        Heart_rate,
        Body_temp
    ]], columns=[
        'Gender','Age','Height','Weight','Duration',
        'Heart_Rate','Body_Temp'
    ])

    prediction = rfr.predict(df)
    return prediction[0]

st.title("💪 Calories Burned Prediction App")

st.markdown("This app estimates the number of calories burned based on your workout and body details.")

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
