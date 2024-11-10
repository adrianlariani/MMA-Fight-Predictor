from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn

app = Flask(__name__)
CORS(app)


class LogisticRegression(nn.Module):
    def __init__(self, n_input_features):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(n_input_features, 1)

    def forward(self, x):
        y_predicted = torch.sigmoid(self.linear(x))
        return y_predicted

model = LogisticRegression(n_input_features=13)
model.load_state_dict(torch.load('../mma_predictor_model.pth'))
model.eval()


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = data['features']
    float_features = list(map(float, features))
    features_tensor = torch.tensor(float_features, dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        prediction = model(features_tensor)
        prediction_probability = prediction.item()

    return jsonify({'prediction': str(round(prediction_probability))})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
