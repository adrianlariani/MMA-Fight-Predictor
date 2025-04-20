import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
import os

from update_fighter_data import event_update_fighters

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
    ids = [fighter['value'] for fighter in data["fighters"]]
    features = get_fighter_data_by_id(ids[0], ids[1])

    float_features = list(map(float, features))
    features_tensor = torch.tensor(float_features, dtype=torch.float32).unsqueeze(0)
    print(features_tensor)
    with torch.no_grad():
        prediction = model(features_tensor)
        prediction_probability = prediction.item()

    return jsonify({'prediction': str(round(prediction_probability))})

@app.route('/keep_online', methods=['GET'])
def ping():
    return ('', 204)


@app.route('/update_fighter_data', methods=['PUT'])
def update_fighter_data():
    event_update_fighters()
    return '', 204

def get_fighter_data_by_id(id1, id2):
      query = """SELECT
                f1.weight - f2.weight AS weight_diff,
                f1.height - f2.height AS height_diff,
                f1.reach - f2.reach AS reach_diff,
                CASE f1.stance
                  WHEN 'Orthodox' THEN 0
                  WHEN 'Southpaw' THEN 1
                  WHEN 'Switch' THEN 2
                  WHEN 'Open Stance' THEN 3
                  ELSE 0
                END AS r_stance,
                CASE f2.stance
                    WHEN 'Orthodox' THEN 0
                    WHEN 'Southpaw' THEN 1
                    WHEN 'Switch' THEN 2
                    WHEN 'Open Stance' THEN 3
                    ELSE 0
                END AS b_stance,
                f1.slpm - f2.slpm AS SLpM_total_diff,
                f1.str_acc - f2.str_acc AS sig_str_acc_total_diff,
                f1.sapm - f2.sapm AS SApM_total_diff,
                f1.str_def - f2.str_def AS str_def_total_diff,
                f1.td_avg - f2.td_avg AS td_avg_diff,
                f1.td_acc - f2.td_acc AS td_acc_total_diff,
                f1.td_def - f2.td_def AS td_def_total_diff,
                f1.sub_avg - f2.sub_avg AS sub_avg_diff
                FROM fighter_statistics f1
                JOIN fighter_statistics f2
                ON f1.id = %s AND f2.id = %s;"""
      conn = psycopg2.connect(database=os.environ["DATABASE_NAME"],
                          host=os.environ["DATABASE_HOST"],
                          user=os.environ["DATABASE_USERNAME"],
                          password=os.environ["DATABASE_PASSWORD"]
                          )
      cursor = conn.cursor()
      cursor.execute(query, (id1, id2))
      data = cursor.fetchone()
      cursor.close()
      return data



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
