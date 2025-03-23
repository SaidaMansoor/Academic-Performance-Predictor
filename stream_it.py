import streamlit as st
import numpy as np
import pickle
import joblib

st.title("Student Performance Predictor")
st.write('Enter the following details to predict performance:')
st.write(f"API URL: https://your-new-ngrok-url.ngrok-free.app/alone2")


# Input fields
hours_studied = st.number_input("Hours Studied", min_value=0, step=1)
previous_scores = st.number_input("Previous Scores", min_value=0, max_value=100, step=1)
sleep_hours = st.number_input("Sleep Hours", min_value=0, step=1)
sample_paper = st.number_input("Sample Paper Attempted", min_value=0, step=1)
extra_activity = st.radio("Did extra practice?", ["Yes", "No"])

# Make prediction
if st.button("Check Performance"):
    input_data = np.array([hr_std, pr_scr, hr_slp, sp_ppr, act_num_0, act_num_1])
    prediction = model.predict([input_data])
    
    st.success(f'Predicted Performance Index: {round(prediction[0], 2)}')