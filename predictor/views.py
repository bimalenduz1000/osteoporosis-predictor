import os
import pickle
import numpy as np
from django.shortcuts import render, redirect
from django.conf import settings

# Load model once
MODEL_PATH = os.path.join(settings.BASE_DIR, 'osp.pkl')
with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

def home(request):
    prediction = None

    if request.method == 'POST':
        # Get form values
        age = float(request.POST.get('age', 0))
        gender = request.POST.get('gender', 'Female')
        hormone = request.POST.get('hormone', 'Normal')
        fhistory = request.POST.get('fhistory', 'No')
        race = request.POST.get('race', 'Caucasian')
        weight = request.POST.get('weight', 'Normal')
        calcium = request.POST.get('calcium', 'Adequate')
        activity = request.POST.get('activity', 'Active')
        smoking = request.POST.get('smoking', 'No')
        medcondition = request.POST.get('medcondition', 'Hyperthyroidism')
        medications = request.POST.get('medications', 'Corticosteroids')
        fractures = request.POST.get('fractures', 'No')

        features = [
            age,
            1 if gender == 'Female' else 0,
            1 if gender == 'Male' else 0,
            1 if hormone == 'Normal' else 0,
            1 if hormone == 'Postmenopausal' else 0,
            1 if fhistory == 'No' else 0,
            1 if fhistory == 'Yes' else 0,
            1 if race == 'African American' else 0,
            1 if race == 'Asian' else 0,
            1 if race == 'Caucasian' else 0,
            1 if weight == 'Normal' else 0,
            1 if weight == 'Underweight' else 0,
            1 if calcium == 'Adequate' else 0,
            1 if calcium == 'Low' else 0,
            1 if activity == 'Active' else 0,
            1 if activity == 'Sedentary' else 0,
            1 if smoking == 'No' else 0,
            1 if smoking == 'Yes' else 0,
            1 if medcondition == 'Hyperthyroidism' else 0,
            1 if medcondition == 'Rheumatoid Arthritis' else 0,
            1 if medications == 'Corticosteroids' else 0,
            1 if fractures == 'No' else 0,
            1 if fractures == 'Yes' else 0,
        ]

        X_input = np.array([features])
        result = model.predict(X_input)[0]
        prediction = 'Osteoporosis' if int(result) == 1 else 'No Osteoporosis'

        # Save prediction in session to show once
        request.session['prediction'] = prediction
        return redirect('/')

    # Show prediction if exists in session
    if 'prediction' in request.session:
        prediction = request.session['prediction']
        del request.session['prediction']  # remove after showing once

    return render(request, 'predictor/index.html', {'prediction': prediction})
