import os
from django.shortcuts import render
import joblib
import pandas as pd

# Get the base directory of the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the model and expected columns
model = joblib.load(os.path.join(BASE_DIR, "osp.joblib"))
expected_columns = joblib.load(os.path.join(BASE_DIR, "columns.pkl"))

def home(request):
    result = None
    form_data = {}

    if request.method == "POST":
        # Collect form data
        form_data = {
            "age": request.POST.get("age"),
            "gender": request.POST.get("gender"),
            "race": request.POST.get("race"),
            "hormone": request.POST.get("hormone"),
            "fhistory": request.POST.get("fhistory"),
            "weight": request.POST.get("weight"),
            "calcium": request.POST.get("calcium"),
            "activity": request.POST.get("activity"),
            "smoking": request.POST.get("smoking"),
            "medcondition": request.POST.get("medcondition"),
            "medications": request.POST.get("medications"),
            "fractures": request.POST.get("fractures"),
        }

        # Convert to DataFrame
        input_dict = {
            key: [int(value) if key == "age" else value]
            for key, value in form_data.items()
        }
        df = pd.DataFrame(input_dict)

        # One-hot encode and align columns
        df_encoded = pd.get_dummies(df)
        df_encoded = df_encoded.reindex(columns=expected_columns, fill_value=0)

        # Predict
        pred = model.predict(df_encoded)[0]
        result = "Positive" if pred == 1 else "Negative"

    return render(request, "predictor/index.html", {
        "result": result,
        "form_data": form_data
    })
