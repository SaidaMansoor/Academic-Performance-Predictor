import streamlit as st
import numpy as np
import pickle
import joblib

st.title("Student's Performance Checker")

# Load model
@st.cache_resource  # This caches the model loading
def load_model():
    file = open('performance.pkl', 'rb')
    return joblib.load(file)

model = load_model()

# Create input fields
hr_std = st.number_input("Studied hour", min_value=0)
pr_scr = st.number_input("Previous score", min_value=0, max_value=100)
hr_slp = st.number_input("Hour sleep", min_value=0)
sp_ppr = st.number_input("No. of sample paper solved", min_value=0)
activi = st.radio('Activity',['Yes','No'])

# Convert radio button to numeric
act_num_1 = 1 if activi == "Yes" else 0
act_num_0 = 0 if activi == "No" else 1

# Make prediction
if st.button("Check Performance"):
    input_data = np.array([hr_std, pr_scr, hr_slp, sp_ppr, act_num_0, act_num_1])
    prediction = model.predict([input_data])
    
    st.success(f'Predicted Performance Index: {round(prediction[0], 2)}')