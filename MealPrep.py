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
        if dietitian_ID == '' or not dietitian_ID.isnumeric():
            err_msg = 'Please enter a valid Dietitian ID'
        if recipee_id == '' or recipee_id == 0 or recipee_id == '0' or not recipee_id.isnumeric():
            err_msg = 'Please select a recipee'

        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
        
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
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))     
    
    
    @staticmethod
    def generate_meal_plan_LSM(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days):
        try:
            err_msg = None
            if dietitian_ID == '' or not str(dietitian_ID).isnumeric():
                err_msg = 'Please insert a valid Dietitian ID'
            if protein_goal == '' or protein_goal == 0 or protein_goal == '0' or not str(protein_goal).isnumeric():
                err_msg = 'Please insert a valid Protein goal'
            if carbs_goal == '' or carbs_goal == 0 or carbs_goal == '0' or not str(carbs_goal).isnumeric():
                err_msg = 'Please insert a valid Carbs goal'
            if fat_goal == '' or fat_goal == 0 or fat_goal == '0' or not str(fat_goal).isnumeric():
                err_msg = 'Please insert a valid Fat goal'
            if nbr_days == '' or nbr_days == 0 or nbr_days == '0' or not str(nbr_days).isnumeric():
                err_msg = 'Please insert a valid Number of days'
            
            if err_msg != None:
                return GlobalFunctions.return_error_msg(err_msg)
            dietitian_ID = int(dietitian_ID)
            protein_goal = int(protein_goal)
            carbs_goal = int(carbs_goal)
            fat_goal = int(fat_goal)
            nbr_days = int(nbr_days)
        
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
            unique_combinations = set()
            # Generate all possible combinations of meals for breakfast, lunch, and dinner
            for breakfast in breakfasts:
                for lunch in lunches:
                    for dinner in dinners:      
                        if dinner[6] != breakfast[6] and dinner[6]!=lunch[6] and breakfast[6] !=lunch[6]:
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
                                        
                                        # Calculate LSM scor
                                        score = (4*(protein_goal - protein_meals)**2 + 
                                                (carbs_goal - carbs_meals)**2 + 
                                                (fat_goal - fat_meals)**2)
                                        current_combination1 = tuple([breakfast[6], lunch[6], dinner[6], breakfast_servings, lunch_servings, dinner_servings])
                                        current_combination2 = tuple([breakfast[6], dinner[6], lunch[6], breakfast_servings, dinner_servings, lunch_servings])
                                        current_combination3 = tuple([dinner[6], breakfast[6], lunch[6], dinner_servings, breakfast_servings, lunch_servings])
                                        current_combination4 = tuple([dinner[6], lunch[6], breakfast[6], dinner_servings, lunch_servings, breakfast_servings])
                                        current_combination5 = tuple([lunch[6], breakfast[6],  dinner[6], lunch_servings, breakfast_servings,  dinner_servings])
                                        current_combination6 = tuple([lunch[6],  dinner[6], breakfast[6], lunch_servings,  dinner_servings, breakfast_servings])

                                        # Check if the combination is unique
                                        if current_combination1 not in unique_combinations and current_combination2 not in unique_combinations and current_combination3 not in unique_combinations and current_combination4 not in unique_combinations and current_combination5 not in unique_combinations and current_combination6 not in unique_combinations :
                                            # Add the combination to the set of unique combinations
                                            unique_combinations.add(current_combination1)

                                            # Add the combination to the list or perform further processing
                                            MpCombination.add_combination_lst(all_combinations, breakfast, lunch, dinner, breakfast_servings, lunch_servings, dinner_servings, score)
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
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    
    def generate_meal_plan_with_fixed_lunch(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days, fixed_lunch_id):
        err_msg = None
        if dietitian_ID == '' or not dietitian_ID.isnumeric():
            err_msg = 'Please insert a valid Dietitian ID'
        if protein_goal == '' or protein_goal == 0 or protein_goal == '0' or not protein_goal.isnumeric():
            err_msg = 'Please insert a valid Protein goal'
        if carbs_goal == '' or carbs_goal == 0 or carbs_goal == '0' or not carbs_goal.isnumeric():
            err_msg = 'Please insert a valid Carbs goal'
        if fat_goal == '' or fat_goal == 0 or fat_goal == '0' or not fat_goal.isnumeric():
            err_msg = 'Please insert a valid Fat goal'
        if nbr_days == '' or nbr_days == 0 or nbr_days == '0' or not nbr_days.isnumeric():
            err_msg = 'Please insert a valid Number of days'
        if fixed_lunch_id == '' or fixed_lunch_id == 0 or fixed_lunch_id == '0' or not fixed_lunch_id.isnumeric():
            err_msg = 'Please insert a valid Fixed lunch'            
        
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
        
        dietitian_ID = int(dietitian_ID)
        protein_goal = int(protein_goal)
        carbs_goal = int(carbs_goal)
        fat_goal = int(fat_goal)
        nbr_days = int(nbr_days)
        fixed_lunch_id = int(fixed_lunch_id)

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
                return GlobalFunctions.return_error_msg('Please insert a valid Fixed lunch')
            
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
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))    

