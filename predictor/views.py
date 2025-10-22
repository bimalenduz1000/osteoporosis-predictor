# predictor/views.py
from django.shortcuts import render
import joblib
import pandas as pd

# Load the pre-trained model
MODEL_PATH = "predictor/osp.joblib"  # Ensure this path is correct
model = joblib.load(MODEL_PATH)

# All columns used during training (numeric + one-hot)
ALL_COLUMNS = [
    "Age",
    "Gender_Asian", "Gender_Male",
    "Race_Asian", "Race_Other",
    "Hormone_Normal",
    "FHistory_No",
    "Weight_Normal",
    "Calcium_Adequate",
    "Activity_Active",
    "Smoking_No",
    "MedCondition_Rheumatoid Arthritis",
    "Medications_Corticosteroids",
    "Fractures_No"
]

# Helper function to map categorical input to one-hot
def map_categorical_input(form_data):
    mapping = {
        "Gender_Asian": 1 if form_data["gender"] == "Asian" else 0,
        "Gender_Male": 1 if form_data["gender"] == "Male" else 0,
        "Race_Asian": 1 if form_data["race"] == "Asian" else 0,
        "Race_Other": 1 if form_data["race"] not in ["Asian", "Caucasian", "African American"] else 0,
        "Hormone_Normal": 1 if form_data["hormone"] == "Normal" else 0,
        "FHistory_No": 1 if form_data["fhistory"] == "No" else 0,
        "Weight_Normal": 1 if form_data["weight"] == "Normal" else 0,
        "Calcium_Adequate": 1 if form_data["calcium"] == "Adequate" else 0,
        "Activity_Active": 1 if form_data["activity"] == "Active" else 0,
        "Smoking_No": 1 if form_data["smoking"] == "No" else 0,
        "MedCondition_Rheumatoid Arthritis": 1 if form_data["medcondition"] == "Rheumatoid Arthritis" else 0,
        "Medications_Corticosteroids": 1 if form_data["medications"] == "Corticosteroids" else 0,
        "Fractures_No": 1 if form_data["fractures"] == "No" else 0
    }
    return mapping

def home(request):
    context = {}
    if request.method == "POST":
        try:
            # Read form inputs
            form_data = {
                "age": int(request.POST.get("age", 0)),
                "gender": request.POST.get("gender", ""),
                "race": request.POST.get("race", ""),
                "hormone": request.POST.get("hormone", ""),
                "fhistory": request.POST.get("fhistory", ""),
                "weight": request.POST.get("weight", ""),
                "calcium": request.POST.get("calcium", ""),
                "activity": request.POST.get("activity", ""),
                "smoking": request.POST.get("smoking", ""),
                "medcondition": request.POST.get("medcondition", ""),
                "medications": request.POST.get("medications", ""),
                "fractures": request.POST.get("fractures", "")
            }

            # Create input DataFrame
            input_dict = {"Age": [form_data["age"]]}
            input_dict.update({col: [val] for col, val in map_categorical_input(form_data).items()})

            # Make sure columns match model
            X_input = pd.DataFrame(input_dict, columns=ALL_COLUMNS)

            # Predict
            prediction = model.predict(X_input)[0]
            context["prediction"] = "Yes, at risk" if prediction == 1 else "No, low risk"

        except Exception as e:
            context["error"] = f"Error during prediction: {e}"

    return render(request, "predictor/index.html", context)

