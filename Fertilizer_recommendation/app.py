from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os

app = Flask(__name__)

# Absolute paths to saved model artifacts
model_path = r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Fertilizer_recommendation\model_output\svm_fertilizer_model.pkl"
scaler_path = r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Fertilizer_recommendation\model_output\scaler.pkl"
label_encoders_path = r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Fertilizer_recommendation\model_output\label_encoders.pkl"

# Load saved model, scaler, and label encoders
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(label_encoders_path)

# Feature columns expected
feature_columns = ['Temparature', 'Humidity ', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous']

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        # Render the input form for user
        return render_template('index.html')

    # Handle POST JSON request for prediction
    data = request.json
    
    if not data:
        return jsonify({'error': 'No JSON payload received'}), 400

    # Extract input features
    features = []
    for col in feature_columns:
        if col not in data:
            return jsonify({'error': f'Missing feature: {col}'}), 400
        features.append(data[col])

    # Encode categorical features using saved label encoders
    for cat_col in ['Soil Type', 'Crop Type']:
        le = label_encoders[cat_col]
        if features[feature_columns.index(cat_col)] in le.classes_:
            features[feature_columns.index(cat_col)] = np.where(le.classes_ == features[feature_columns.index(cat_col)])[0][0]
        else:
            return jsonify({'error': f'Unknown category in {cat_col}: {features[feature_columns.index(cat_col)]}'}), 400

    # Prepare features for model
    features_array = np.array(features, dtype=float).reshape(1, -1)
    scaled_features = scaler.transform(features_array)

    # Predict fertilizer class
    pred_encoded = model.predict(scaled_features)[0]
    pred_label = label_encoders['Fertilizer Name'].inverse_transform([pred_encoded])[0]

    # Return JSON response
    return jsonify({'predicted_fertilizer': pred_label})

if __name__ == '__main__':
    app.run(debug=True,port=5505)
