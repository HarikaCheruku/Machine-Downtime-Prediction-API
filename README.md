<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Machine Downtime Prediction API</title>
</head>
<body>
    <h1>Machine Downtime Prediction API</h1>
    <p>This project provides a FastAPI-based service for predicting machine downtime based on various parameters such as temperature, leakage, and electricity usage. The API allows users to upload datasets, train machine learning models, and make predictions.</p>

    <h2>Installation Instructions</h2>

    <ol>
        <li><strong>Clone the repository:</strong>
            <pre>git clone https://github.com/your-repo-url.git</pre>
        </li>
        <li><strong>Navigate to the project directory:</strong>
            <pre>cd machine_downtime_api</pre>
        </li>
        <li><strong>Create a virtual environment (optional but recommended):</strong>
            <ul>
                <li>On Windows:
                    <pre>python -m venv venv</pre>
                </li>
                <li>On macOS/Linux:
                    <pre>python3 -m venv venv</pre>
                </li>
            </ul>
        </li>
        <li><strong>Activate the virtual environment:</strong>
            <ul>
                <li>On Windows:
                    <pre>venv\Scripts\activate</pre>
                </li>
                <li>On macOS/Linux:
                    <pre>source venv/bin/activate</pre>
                </li>
            </ul>
        </li>
        <li><strong>Install dependencies:</strong>
            <pre>pip install -r requirements.txt</pre>
        </li>
        <li><strong>Run the FastAPI server:</strong>
            <pre>uvicorn main:app --reload</pre>
            <p>This will start the FastAPI server in development mode. You can access the API at <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a>.</p>
        </li>
    </ol>

    <h2>API Endpoints</h2>

    <h3>1. Upload Dataset</h3>
    <p><strong>URL:</strong> /upload</p>
    <p><strong>Method:</strong> POST</p>
    <p><strong>Description:</strong> Upload a CSV file containing the machine data.</p>
    <pre>curl -X POST -F "file=@your_dataset.csv" http://127.0.0.1:8000/upload</pre>

    <h3>2. Train the Model</h3>
    <p><strong>URL:</strong> /train</p>
    <p><strong>Method:</strong> POST</p>
    <p><strong>Description:</strong> Train the model with the uploaded dataset.</p>
    <pre>curl -X POST http://127.0.0.1:8000/train</pre>

    <h3>3. Make a Prediction</h3>
    <p><strong>URL:</strong> /predict</p>
    <p><strong>Method:</strong> POST</p>
    <p><strong>Description:</strong> Send a JSON object with features to predict machine downtime.</p>
    <pre>curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d "{\"Min_Temp\": 12.5, \"Max_Temp\": 32.1, \"Leakage\": 1.5, \"Electricity\": 8.5}"</pre>

    <h2>Example Responses</h2>

    <h3>For /predict endpoint:</h3>
    <p>If the prediction is "No" downtime with 100% confidence, you will receive the following response:</p>
    <pre>
    {
      "Downtime": "No",
      "Confidence": 1.0
    }
    </pre>

    <p>If the prediction is "Yes" downtime with a different confidence score:</p>
    <pre>
    {
      "Downtime": "Yes",
      "Confidence": 0.87
    }
    </pre>

    <h2>Troubleshooting</h2>

    <h3>Error: "JSON decode error"</h3>
    <p>Ensure the request body is valid JSON format. For example:</p>
    <pre>
    {
      "Min_Temp": 12.5,
      "Max_Temp": 32.1,
      "Leakage": 1.5,
      "Electricity": 8.5
    }
    </pre>

    <h3>Error: "Model not trained"</h3>
    <p>Ensure that you have uploaded the dataset and trained the model before making predictions.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>
