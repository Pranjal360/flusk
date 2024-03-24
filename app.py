from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
# Load the pickled model
model = joblib.load('train_model.sav')


@app.route('/predict', methods=['POST'])
def predict():
    # Get input features from request
    features = request.json['features']

    input_data_as_numpy_array = np.asarray(features)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = model.predict(input_data_reshaped)

    # Return prediction as JSON response
    return jsonify({'prediction': prediction.tolist()})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)