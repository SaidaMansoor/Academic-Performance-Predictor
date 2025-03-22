from fastapi import FastAPI, Request 

import pickle
import sklearn
import joblib

app = FastAPI()
file = open("performance.pkl", 'rb')
model = joblib.load(file)

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}


# @app.post('/alone1')
# async def post_data(request:Request):
#     if request.method == 'POST':
#         data = await request.json()
#         print("received data:", data)
#         return {'message':data}

@app.post('/alone2')
async def student_performance(request:Request):
    if request.method == "POST":
        data = await request.json()
        hours_studied = int(data['hours_studied'])
        previous_scores = int(data['previous_scores'])
        hours_sleep = int(data['sleep_hours'])
        sample_paper = int(data['sample_paper'])
        activity = data['activity']  # Expect 'yes' or 'no' directly

        # Convert activity to binary features
        if activity == 'yes':
            yes = 1
            no = 0
        else:
            yes = 0
            no = 1

        x = model.predict([[
            hours_studied,
            previous_scores,
            hours_sleep,
            sample_paper,
            no,
            yes
        ]])
        
        return{'Performance Index': int(x[0])}  # Return first value