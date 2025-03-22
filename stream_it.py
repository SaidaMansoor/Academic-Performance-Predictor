import streamlit as stream
import requests
import pickle
import sklearn
import joblib

stream.title("Student Performance Predictor")
stream.write('Enter the following details to predict performance:')


# Input fields
hours_studied = stream.number_input("Hours Studied", min_value=0, step=1)
previous_scores = stream.number_input("Previous Scores", min_value=0, max_value=100, step=1)
sleep_hours = stream.number_input("Sleep Hours", min_value=0, step=1)
sample_paper = stream.number_input("Sample Paper Attempted", min_value=0, step=1)
extra_activity = stream.radio("Did extra practice?", ["Yes", "No"])

# Button to make prediction
if stream.button("Predict Performance"):
    # Prepare data for API
    data = {
        "hours_studied": hours_studied,
        "previous_scores": previous_scores,
        "sleep_hours": sleep_hours,
        "sample_paper": sample_paper,
        "activity": "yes" if extra_activity == "Yes" else "no"
    }

    # Send request to FastAPI
    response = requests.post("https://0fed-106-222-217-190.ngrok-free.app/alone2", json=data)

    
    # Show response
    if response.status_code == 200:
        result = response.json()
        stream.success(f"Predicted Performance Index: {result['Performance Index']}")
    else:
        stream.error(f"Error: Could not get prediction. Status code: {response.status_code}")
        stream.error(f"Response: {response.text}")