from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import pickle
import os

app = FastAPI()

# Initialize variables
model = None
data = None
MODEL_FILE = "model.pkl"

# Endpoint to upload dataset
@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    global data
    try:
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

        # Read CSV
        data = pd.read_csv(file.file)

        # Ensure the required target column exists
        if "Fail_tomorrow" not in data.columns:
            raise HTTPException(status_code=400, detail="Dataset must contain a 'Fail_tomorrow' column.")

        # Ensure target is binary
        if data["Fail_tomorrow"].nunique() != 2:
            raise HTTPException(status_code=400, detail="'Fail_tomorrow' column must be binary (two unique values).")

        return {"message": "Dataset uploaded successfully!", "columns": list(data.columns)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# Endpoint to train the model
@app.post("/train")
async def train_model():
    global model, data
    if data is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded. Please upload a dataset first.")

    try:
        # Split data into features and target
        X = data.loc[:, data.columns != "Fail_tomorrow"]
        y = data["Fail_tomorrow"]

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Save the trained model
        with open(MODEL_FILE, "wb") as f:
            pickle.dump(model, f)

        return {
            "message": "Model trained successfully!",
            "accuracy": round(accuracy, 2),
            "f1_score": round(f1, 2),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training model: {str(e)}")

# Endpoint to predict
class PredictRequest(BaseModel):
    Min_Temp: float
    Max_Temp: float
    Leakage: float
    Electricity: float

@app.post("/predict")
async def predict(request: PredictRequest):
    global model

    # Load the model if not already loaded
    if model is None:
        if os.path.exists(MODEL_FILE):
            with open(MODEL_FILE, "rb") as f:
                model = pickle.load(f)
        else:
            raise HTTPException(status_code=400, detail="No model available. Train a model first.")

    try:
        # Prepare input for prediction
        input_data = pd.DataFrame([request.dict()])

        prediction = model.predict(input_data)
        confidence = max(model.predict_proba(input_data)[0])

        return {
            "Downtime": "Yes" if prediction[0] == 1 else "No",
            "Confidence": round(confidence, 2),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
