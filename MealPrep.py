# Model for MealPrep
from Db_connection import Db_connection
import json
import itertools
import heapq
from decimal import Decimal
from MpCombination import MpCombination
import psycopg2
from GlobalFunctions import GlobalFunctions

from Recipee import Recipee

def handle_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
    
    
class MealPrep:

    def __init__(self, diet_id, recipee_id, date,meal_id,patient_id,diet_start_date):
        self.diet_id = diet_id
        self.recipee_id = recipee_id  
        self.date = date  
        self.meal_id = meal_id  
        self.patient_id = patient_id
        self.diet_start_date = diet_start_date  

    def MealPrep_json(self):
        return json.dumps(vars(self), default=str)
    
        
    @staticmethod
    def generate_shopping_list(dietitian_ID, recipee_id):
        err_msg = None
        if dietitian_ID == '':
            err_msg = 'Dietitian ID is missing'
        if recipee_id == '' or recipee_id == 0 or recipee_id == '0':
            err_msg = 'Please select a recipee'

        if err_msg != None:
            response = {
                        "status": "error",
                        "message": err_msg
                    }            
            return json.dumps(response)
        
        try:
            cur = Db_connection.getConnection().cursor()        
            query = f"""SELECT ri.ingredient_id,i."name", ri.grammes, ri.litters, ri.cup, ri.tbsp, ri.tsp, ri.small, ri.medium, ri.large 
                        FROM recipeingredients ri,ingredient i WHERE ri.recipee_id = {recipee_id} and i.ingredient_id =ri.ingredient_id"""
            cur.execute(query)
            
            ingredients = cur.fetchall()
            # shopping_list = [ingredient[0] for ingredient in ingredients]  
            shopping_List = []
            for ingr in ingredients:
                shopping_List.append({"ingredient_id":ingr[0],
                                    "name":ingr[1],
                                    "grammes":ingr[2],
                                    "litters":ingr[3],
                                    "cup":ingr[4],
                                    "tbsp":ingr[5],
                                    "tsp":ingr[6],
                                    "small":ingr[7],
                                    "medium":ingr[8],
                                    "large":ingr[9] })

            cur.close()
            to_ret = json.dumps(shopping_List)
            return GlobalFunctions.cleanJSON(to_ret);
        except psycopg2.Error as e:
            response = {
                        "status": "error",
                        "message": "DB error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response)  
        except Exception as e:
            response = {
                        "status": "error",
                        "message": "Server error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response)         
    
    
    @staticmethod
    def generate_meal_plan_LSM(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days):
        err_msg = None
        if dietitian_ID == '':
            err_msg = 'Dietitian ID is missing'
        if protein_goal == '' or protein_goal == 0 or protein_goal == '0':
            err_msg = 'Protein goal should be a value bigger than 0'
        if carbs_goal == '' or carbs_goal == 0 or carbs_goal == '0':
            err_msg = 'Carbs goal should be a value bigger than 0'
        if fat_goal == '' or fat_goal == 0 or fat_goal == '0':
            err_msg = 'Fat goal should be a value bigger than 0'
        if nbr_days == '' or nbr_days == 0 or nbr_days == '0':
            err_msg = 'Number of days should be a value bigger than 0'
        
        if err_msg != None:
            response = {
                        "status": "error",
                        "message": err_msg
                    }            
            return json.dumps(response)
        try:
            cur = Db_connection.getConnection().cursor()
            # Fetch all meals
            cur.execute("SELECT recipee_id, protein, carbs, fat, meal_type, servings, name, description,calories FROM recipee")
            meals = cur.fetchall()
            breakfast_weight = 1
            lunch_weight = 1
            dinner_weight = 1
            breakfasts = [meal for meal in meals if meal[4] == 'Breakfast']
            lunches = [meal for meal in meals if meal[4] == 'Lunch']
            dinners = [meal for meal in meals if meal[4] == 'Dinner']
            # Use a heap to keep track of the top 7 combinations
            all_combinations = []
            
            # Generate all possible combinations of meals for breakfast, lunch, and dinner
            for breakfast in breakfasts:
                for lunch in lunches:
                    for dinner in dinners:
                        for breakfast_servings in range(1, int(breakfast[5]) + 1):  # Assuming servings is an integer
                            for lunch_servings in range(1, int(lunch[5]) + 1):
                                for dinner_servings in range(1, int(dinner[5]) + 1):
                                    protein_meals = (breakfast[1] * breakfast_servings * breakfast_weight + 
                                                    lunch[1] * lunch_servings * lunch_weight+ 
                                                    dinner[1] * dinner_servings * dinner_weight)
                                    carbs_meals = (breakfast[2] * breakfast_servings * breakfast_weight + 
                                                lunch[2] * lunch_servings * lunch_weight+ 
                                                dinner[2] * dinner_servings * dinner_weight)
                                    fat_meals = (breakfast[3] * breakfast_servings * breakfast_weight + 
                                                lunch[3] * lunch_servings * lunch_weight + 
                                                dinner[3] * dinner_servings * dinner_weight)
                                    
                                    # Calculate LSM score
                                    score = (4*(protein_goal - protein_meals)**2 + 
                                            (carbs_goal - carbs_meals)**2 + 
                                            (fat_goal - fat_meals)**2)
                                    MpCombination.add_combination_lst(all_combinations,breakfast,lunch,dinner,breakfast_servings,lunch_servings,dinner_servings,score)
                                    # combination = MpCombination.create_combination(breakfast,lunch,dinner,breakfast_servings,lunch_servings,dinner_servings,score)
                                    # combJson = combination.mpCombination_json()
                                    # print(combJson)
                                    # all_combinations = all_combinations.append(combJson);
    
            # Sort the combinations based on LSM score in ascending order
            all_combinations.sort(key=lambda x: x["score"])
            nbr_days = int(nbr_days)
            best_combinations = all_combinations[:nbr_days]
            cur.close()
            to_ret = json.dumps({"best_combinations": best_combinations}, default=lambda x: float(x) if isinstance(x, Decimal) else x)
            return GlobalFunctions.cleanJSON(to_ret);

        except psycopg2.Error as e:
            response = {
                        "status": "error",
                        "message": "DB error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response)  
        except Exception as e:
            response = {
                        "status": "error",
                        "message": "Server error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response) 


    
    def generate_meal_plan_with_fixed_lunch(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days, fixed_lunch_id):
        err_msg = None
        if dietitian_ID == '':
            err_msg = 'Dietitian ID is missing'
        if protein_goal == '' or protein_goal == 0 or protein_goal == '0':
            err_msg = 'Protein goal should be a value bigger than 0'
        if carbs_goal == '' or carbs_goal == 0 or carbs_goal == '0':
            err_msg = 'Carbs goal should be a value bigger than 0'
        if fat_goal == '' or fat_goal == 0 or fat_goal == '0':
            err_msg = 'Fat goal should be a value bigger than 0'
        if nbr_days == '' or nbr_days == 0 or nbr_days == '0':
            err_msg = 'Number of days should be a value bigger than 0'
        if fixed_lunch_id == '' or fixed_lunch_id == 0 or fixed_lunch_id == '0':
            err_msg = 'Fixed lunch should be delected'
        
        if err_msg != None:
            response = {
                        "status": "error",
                        "message": err_msg
                    }            
            return json.dumps(response)
        
        try:
            cur = Db_connection.getConnection().cursor()
            # Fetch all meals
            cur.execute("SELECT recipee_id, protein, carbs, fat, meal_type, servings, name, description,calories FROM recipee")
            meals = cur.fetchall()
            
            breakfasts = [meal for meal in meals if meal[4] == 'Breakfast']
            lunches = [meal for meal in meals if meal[4] == 'Lunch' and meal[0] == fixed_lunch_id]
            dinners = [meal for meal in meals if meal[4] == 'Dinner']
            
            # Use a list to keep track of the top combinations
            all_combinations = []
            
            # Fetch the fixed lunch
            fixed_lunch = lunches[0] if lunches else None

            if not fixed_lunch:
                response = {
                            "status": "error",
                            "message": 'Invalid fixed lunch ID'
                        }            
                return json.dumps(response)
            
            # Generate all possible combinations of meals for breakfast and dinner with the fixed lunch
            for breakfast in breakfasts:
                for dinner in dinners:
                    for breakfast_servings in range(1, int(breakfast[5]) + 1):
                        for dinner_servings in range(1, int(dinner[5]) + 1):
                            for lunch_servings in range(1, int(fixed_lunch[5]) + 1):
                                protein_meals = (breakfast[1] * breakfast_servings + 
                                                fixed_lunch[1] * lunch_servings + 
                                                dinner[1] * dinner_servings)
                                carbs_meals = (breakfast[2] * breakfast_servings + 
                                            fixed_lunch[2] * lunch_servings + 
                                            dinner[2] * dinner_servings)
                                fat_meals = (breakfast[3] * breakfast_servings + 
                                            fixed_lunch[3] * lunch_servings + 
                                            dinner[3] * dinner_servings)
                                
                                # Calculate LSM score
                                score = (4*(protein_goal - protein_meals)**2 + 
                                        (carbs_goal - carbs_meals)**2 + 
                                        (fat_goal - fat_meals)**2)
                                MpCombination.add_combination_lst(all_combinations,breakfast,fixed_lunch,dinner,breakfast_servings,lunch_servings,dinner_servings,score)
            
            # Sort the combinations based on LSM score in ascending order
            all_combinations.sort(key=lambda x: x["score"])
            best_combinations = all_combinations[:nbr_days]
            cur.close()
            
            to_ret = json.dumps({"best_combinations": best_combinations}, default=lambda x: float(x) if isinstance(x, Decimal) else x)
            return GlobalFunctions.cleanJSON(to_ret)
        except psycopg2.Error as e:
            response = {
                        "status": "error",
                        "message": "DB error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response)  
        except Exception as e:
            response = {
                        "status": "error",
                        "message": "Server error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response) 
       

