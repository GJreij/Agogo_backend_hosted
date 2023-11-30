import json
from GlobalFunctions import GlobalFunctions
from werkzeug.exceptions import BadRequest
from flask import Flask, jsonify, request
from BodyComp import BodyComp
from Db_connection import Db_connection
from Dietitian import Dietitian
from HealthHist import HealthHist
from LifeStyle import LifeStyle
from MealPrepItem import MealPrepItem
from MpCombination import MpCombination
from Patient import Patient
from Anthropometry import Anthropometry
from MealPrep import MealPrep
from Ingredient import Ingredient
from Diet import Diet
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from Recipee import Recipee

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'AJOUJOUUUUUUU IS ONLINEEE!'

@app.get('/admin/closeConn')
def Close_Con():
     Db_connection.closeConnection(Db_connection.getConnection())
     return "connection closed";

#DIETITIAN CLASS
@app.get('/dietitian/login')
def getDietitian():
    #data = request.get_json()
    #dietitian_email = data['dietitian_email']
    #dietitian_pwd = data['dietitian_pwd']
    #dietitian_email = request.args.get("dietitian_email")
    dietitian_ID = request.args.get("dietitian_ID")
    return Dietitian.fetchDietitian(dietitian_ID);
    
@app.get('/dietitian/getDietitians')
def getAllDietitians():
    return Dietitian.getDietitians();

@app.get('/dietitian/patients')
def fetDietitianPatients():
    #data = request.get_json()
    #dietitian_ID = data['dietitian_ID']
    dietitian_ID = request.args.get("dietitian_ID")
    return Dietitian.fetchDietitianPatients(dietitian_ID);
    

@app.post('/dietitian/createPatient')
def setPatient():
    data = request.get_json()
    return Dietitian.createPatient(json.dumps(data))

@app.post('/dietitian/deactivatePatient')
def deactivatePatient():
    data = request.get_json()
    return Dietitian.deactivatePatient(data['patient_ID']);

@app.post('/dietitian/activatePatient')
def activatePatient():
    data = request.get_json()
    return Dietitian.activatePatient(data['patient_ID']);

@app.post('/dietitian/addDietitian')
def addDietitian():
    data = request.get_json()
    return Dietitian.addDietitian(json.dumps(data));

@app.put('/dietitian/updateDietitian')
def updateDietitian():
    data = request.get_json()
    return Dietitian.updateDietitian(json.dumps(data));

@app.delete('/dietitian/deleteDietitian')
def deleteDietitian():
    data = json.loads(json.dumps(request.get_json()))
    return Dietitian.removeDietitian(data['dietitian_id']);

#END OF DIETITIAN CLASS.


#PATIENT CLASS
@app.get('/patient/login')
def getPatient():
    #data = request.get_json()
    #patient_email = data['patient_email']
    #patient_pwd = data['patient_pwd']
    patient_email = request.args.get("patient_email")
    patient_pwd = request.args.get("patient_pwd")
    return Patient.fetchPatient(patient_email,patient_pwd);
    
@app.get('/patient/staticInfo')
def getPatientStaticInfo():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return Patient.fetchPatientStaticInfo(patient_ID);


@app.get('/patient/calculations')
def getPatientCalculations():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return Patient.fetchPatientCalculations(patient_ID);


@app.get('/patient/patientLogs')
def getPatientLogs():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return Patient.fetchPatientLogs(patient_ID);    

@app.get('/patient/LastAnthropometry')
def getPatientLastAnthropometry():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return Anthropometry.fetchPatientLastAnth(patient_ID);
  

@app.get('/patient/AnthropometryHistory')
def getPatientAnthropometryHist():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return Anthropometry.fetchPatientAnthHist(patient_ID);

@app.post('/patient/addAnthropometry')
def addAnthropometry():
    data = request.get_json()
    return Anthropometry.addAnthropometry(json.dumps(data))

@app.get('/patient/LastBodyComp')
def getPatientLastBodyComp():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return BodyComp.fetchPatientLastBC(patient_ID);


@app.get('/patient/BodyCompHistory')
def getPatientBodyCompHist():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return BodyComp.fetchPatientBCHist(patient_ID);

@app.get('/patient/LastHealthHistory')
def getPatientLastHealthHistory():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return HealthHist.fetchPatientLastHealthHist(patient_ID);


@app.get('/patient/allHealthHistory')
def getPatientAllHealthHistory():    
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return HealthHist.fetchPatientAllHealthHist(patient_ID);

@app.get('/patient/LastLifeStyle')
def getPatientLastLifeStyle():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return LifeStyle.fetchPatientLastLifeStyle(patient_ID);


@app.get('/patient/LifeStyleHistory')
def getPatientLifeStyleHistory():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return LifeStyle.fetchPatientLifeStyleHist(patient_ID);


@app.get('/patient/allInfo')
def getPatientAllInfo():
    #data = request.get_json()
    #patient_ID = data['patient_ID']
    patient_ID = request.args.get("patient_ID")
    return Patient.fetchPatientAllInfo(patient_ID);

@app.delete('/patient/deletePatient')
def deletePatient():
    data = request.get_json()
    return Patient.deleteAccount(data['patient_ID']);

@app.put('/patient/updateStaticInfo')
def updatePatientStatic():
    data = request.get_json()
    return Patient.updatePatientStatInfo(json.dumps(data))



@app.post('/patient/addBodyComp')
def addBodyComp():
    data = request.get_json()
    return BodyComp.addBodyComp(json.dumps(data))


@app.post('/patient/addHealthHistory')
def addHealthHistory():
    data = request.get_json()
    return HealthHist.addHealthHistory(json.dumps(data))

@app.post('/patient/addLifeStyle')
def addLifeStyle():
    data = request.get_json()
    return LifeStyle.addLifeStyle(json.dumps(data))

#END OF PATIENT CLASS





# @app.get('/recepies')
# def getPatients():
#     conn = Db_connection.getConnection()
#     cur = conn.cursor()
#     cur.execute('select r."Name" as recipee ,i."name" as ingredient, ri.grammes ,ri.litters, ri.cup ,ri.tbsp ,ri.small ,ri.medium ,ri."Large" from recipeingredients ri,recipee r, ingredient i where  r.recipee_id =ri.recipee_id and ri.ingredient_id = i.ingredient_id;')
#     recepies = cur.fetchall()
#     #print(recepies);
#     # recepies = json.dumps(recepies)
#     # print("_____________________________________________________");
#     # print("______________________________________________________");
#     # print(recepies);
#     recepies = jsonify(recepies)
#     # print("_____________________________________________________");
#     # print("______________________________________________________");
#     # print(recepies);
#     # recepies = json.dumps(recepies);
#     cur.close()
#     return recepies;




############################################################## JREIJ'S CODE


########################## Generate Meal Plan

# should it be get??
@app.post('/MealPrep/generateMealPlan')
def generate_meal_plan_LSM():
    data = request.get_json()
    meal_plan = MealPrep.generate_meal_plan_LSM(data['dietitian_ID'], data['protein_goal'], data['carbs_goal'], data['fat_goal'], data['nbr_days'])
    return meal_plan
# should it be get??
@app.post('/MealPrep/generateMealPlanFixedLunch')
def generate_meal_plan_fixed_lunch():
    data = request.get_json()
    meal_plan = MealPrep.generate_meal_plan_with_fixed_lunch(data['dietitian_ID'], data['protein_goal'], data['carbs_goal'], data['fat_goal'], data['nbr_days'], data['fixed_lunch_id'])
    return meal_plan

@app.get('/MealPrep/generateShoppingList')
def generate_shopping_list():
    #data = request.get_json()
    #dietitian_ID = data['dietitian_ID']
    #recipee_id = data['recipee_id']
    dietitian_ID = request.args.get("dietitian_ID")
    recipee_id = request.args.get("recipee_id")
    return MealPrep.generate_shopping_list(dietitian_ID, recipee_id)
    

@app.post('/MealPrep/insertMealPlanItem')
def insertMealPlan():
    data = request.get_json()
    return MealPrepItem.addMealPrepItem(json.dumps(data))

@app.post('/MealPrep/insertBulkMPItems')
def insertBulkMPItems():
    data = request.get_json()
    return MealPrepItem.addbulkMealPrepItems(json.dumps(data))

@app.get('/MealPrep/getCombination')
def getCombination():
    #data = request.get_json()
    #diet_id = data['diet_id']
    #patient_id = data['patient_id']
    #combination_id = data['combination_id']
    diet_id = request.args.get("diet_id")
    patient_id = request.args.get("patient_id")
    combination_id = request.args.get("combination_id")
    mpComb = MpCombination.getCombination(diet_id,patient_id,combination_id)
    return mpComb.mpCombination_json();


#HERE
########################## Ingredient Class
@app.get('/Ingredient/details')
def getIngredientDetails():
    #data = request.get_json()
    #ingredient_id = data['ingredient_id']
    ingredient_id = request.args.get("ingredient_id")
    return Ingredient.fetchIngredientDetails(ingredient_id)

@app.post('/Ingredient/addIngredient')
def addIngredient():
    data = request.get_json()
    return Ingredient.addIngredient(json.dumps(data))    
           
@app.put('/Ingredient/updateIngredient')
def updateIngredient():
    try:
        data = request.get_json()
        ingredient_id = data.get('ingredient_id')

        if not ingredient_id:
            return jsonify({'status': 'error', 'message': 'Ingredient ID is required'}), 400

        result = Ingredient.updateIngredient(ingredient_id, data)
        return jsonify({'status': 'success', 'message': result}), 200

    except ValueError as ve:
        return jsonify({'status': 'error', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'error', 'message': 'Something went wrong'}), 500    


########################## Diet Class

@app.post('/Diet/createDiet')
def createDiet():
    data = request.get_json()
    return Diet.createDiet(json.dumps(data))
  

@app.put('/Diet/udpateDiet')
def updateDiet():
    data = request.get_json()
    diet_id = data.get('diet_id')

    if not diet_id:
        return GlobalFunctions.return_error_msg('Diet ID is required')
    return Diet.updateDiet(diet_id, data)

   
@app.delete('/Diet/deleteDiet')
def deleteDiet():
    try:
        data = request.get_json()
        diet_id = data.get('diet_id')

        if not diet_id:
            return jsonify({'status': 'error', 'message': 'Diet ID is required'}), 400

        result = Diet.deleteDiet(diet_id)
        return jsonify({'status': 'success', 'message': result}), 200

    except ValueError as ve:
        return jsonify({'status': 'error', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'error', 'message': 'Something went wrong'}), 500  

@app.get('/Diet/getDietHistory')
def getDietHistory():
        #data = request.get_json()
        #patient_id = data.get('patient_id')
    patient_id = request.args.get("patient_id")
    return Diet.getDietHistory(patient_id)
   

@app.get('/Diet/getLastDiet')
def getLastDiet():
    patient_id = request.args.get("patient_id")
    return Diet.getLastDiet(patient_id)

@app.get('/diet/getDietCombinations')
def getDietCombinations():
    #data = request.get_json()
    #patient_id = data.get('patient_id')
    #diet_id = data['diet_id']
    patient_id = request.args.get("patient_id")
    diet_id = request.args.get("diet_id")
    mpCombs = Diet.getDietCombinations(diet_id, patient_id)
    return mpCombs;

############################ Recipee Class

@app.get('/Recipee/getRecipee')
def getRecipeeByID():
    try:
        #data = request.get_json()
        #recipee_id = data.get('recipee_id')
        recipee_id = request.args.get("recipee_id")

        if not recipee_id:
            return jsonify({'status': 'error', 'message': 'recipee_id is required'}), 400

        recipee = Recipee.getRecipee(recipee_id)
        
        if recipee is None:
            return jsonify({'status': 'success', 'message': 'No recipees found for the given recipee ID'}), 200

        return recipee, 200

    except ValueError as ve:
        return jsonify({'status': 'error', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'error', 'message': 'Something went wrong'}), 500






# ########################## Swagger Documentation

# Config Swagger UI
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # Our API url

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "AGOGO"
    }
)

# Register blueprint at URL
CORS(app)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
if __name__ == "__main__":
         app.run(host='0.0.0.0')

