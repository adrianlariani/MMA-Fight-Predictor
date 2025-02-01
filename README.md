# MMA-Fight-Predictor
MMA Fight Predictor is a web application designed to predict the winner of MMA fights based on fighter statistics. Using historical data and a machine learning model, this app compares fighters' attributes to provide a prediction of who might win in a given matchup. The project has a Flask backend server with a Next.js frontend interface, with data stored in a PostgreSQL database.

Project Link: https://mma-fight-predictor-gamma.vercel.app/
## Features
 - Fight Prediction: Compare two fighters’ statistics to predict the outcome.
 - Interactive Interface: Select fighters from dropdowns and view prediction results.
 - Data Management: PostgreSQL database stores historical fight data, current fighter statistics, and images.
 - Machine Learning Model: Computes predictions based on a weighted comparison of fighter statistics trained on historical data of UFC fights.

## Technologies
- Backend: Flask, Next.js
- Frontend: Next.js
- Database: PostgreSQL
- Styling: Tailwind CSS
- Machine Learning: Pytorch
- etc.



## Project Structure
```bash
mma-fight-predictor/
├── client/                 # Next.js frontend application
├── data_setup/             # Setup scripts for setting up databases including fight history and fighter statistics
├── server/                 # Flask backend application
│   └── app.py              # Main Flask app with prediction route
├── requirements.txt        # Python dependencies
├── mma_predictor_model.pth # Machine Learning model trained on fight history
└── README.md               # Project documentation
```



