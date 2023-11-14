import json
from werkzeug.exceptions import BadRequest
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'



@app.post('/MealPrep/generateMealPlan')
def generate_meal_plan_LSM():
    data = request.get_json()
    meal_plan = MealPrep.generate_meal_plan_LSM(data['dietitian_ID'], data['protein_goal'], data['carbs_goal'], data['fat_goal'], data['nbr_days'])
    return meal_plan




app.run()
