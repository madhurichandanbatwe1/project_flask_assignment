from flask import Flask, render_template, request, jsonify
from recommendation_engine import get_user_recommendations
import pandas as pd
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def recommendations(user_id):
    ratings_df=pd.read_excel(r"C:\Users\madhu\pendrive\myfiles\Data science Pro\assignments\project_flask_assignment\ques4\data\data.xlsx")
    recommendations = get_user_recommendations(user_id, ratings_df)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
