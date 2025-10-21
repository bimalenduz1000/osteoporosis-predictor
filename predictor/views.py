import os
import joblib
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'model.pkl')

# Load model once
model = joblib.load(model_path)

def home(request):
    result = None
    if request.method == 'POST':
        try:
            age = int(request.POST['age'])
            height = float(request.POST['height'])
            weight = float(request.POST['weight'])
            # ... other fields

            # Make prediction
            data = [[age, height, weight, ...]]  # match your model's input order
            pred = model.predict_proba(data)[0][1]  # probability of osteoporosis
            result = round(pred * 100, 2)
        except Exception as e:
            result = f"Error: {e}"

    return render(request, 'index.html', {'result': result})
