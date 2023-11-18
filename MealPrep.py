# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 21:52:42 2023

@author: gjreij-ext
"""

# Model for MealPrep
from Db_connection import Db_connection
import json
import itertools
import heapq
from decimal import Decimal
from MpCombination import MpCombination

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
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
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
        return json.dumps(shopping_List)
    
    
    
    @staticmethod
    def generate_meal_plan_LSM(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
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
        return json.dumps({"best_combinations": best_combinations}, default=lambda x: float(x) if isinstance(x, Decimal) else x)



    
    def generate_meal_plan_with_fixed_lunch(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days, fixed_lunch_id):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
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
            return 'Invalid fixed lunch ID'
        
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
                            
                            # # Add the combination and its score to the list
                            # combination = {
                            #     "breakfast": breakfast[0:4],
                            #     "lunch": fixed_lunch[0:4],
                            #     "dinner": dinner[0:4],
                            #     "breakfast_servings": breakfast_servings,
                            #     "lunch_servings": lunch_servings,
                            #     "dinner_servings": dinner_servings,
                            #     "score": score,
                            # }
                            
                            # all_combinations.append(combination)
                            # all_combinations = MpCombination.create_combination(all_combinations,breakfast,fixed_lunch,dinner,breakfast_servings,lunch_servings,dinner_servings,score);
                            
        
        # Sort the combinations based on LSM score in ascending order
        all_combinations.sort(key=lambda x: x["score"])
        best_combinations = all_combinations[:nbr_days]
        cur.close()
        
        return json.dumps({"best_combinations": best_combinations}, default=lambda x: float(x) if isinstance(x, Decimal) else x)

    

