from flask import jsonify, request
import json
import psycopg2
from Db_connection import Db_connection
from Recipee import Recipee  # Assuming Db_connection is your database connection file

class MpCombination:

    def __init__(self, breakfast: Recipee, lunch: Recipee, dinner: Recipee, score):
        self.breakfast = breakfast
        self.lunch= lunch
        self.dinner = dinner
        self.score = score

    
    def mpCombination_json(self):
        combination = {
                        "breakfast": self.breakfast.recipee_json(),
                        "lunch": self.lunch.recipee_json(),
                        "dinner": self.dinner.recipee_json(),
                        "score": self.score
                                }
        return combination
    
    def get_breakfast(self):
        return self.breakfast
    
    def get_lunch(self):
        return self.lunch
    
    def get_dinner(self):
        return self.dinner
    
    def get_score(self):
        return self.score
    
    @staticmethod
    def create_combination(breakfast,lunch,dinner,breakfast_servings,lunch_servings,dinner_servings,score):
        #recipee_id, name, description, meal_type, calories, fat, protein, servings, carbs
        breakfast_obj = Recipee(breakfast[0],breakfast[6],breakfast[7],breakfast[4],breakfast[8],breakfast[3],breakfast[1],breakfast_servings,breakfast[2]);
        lunch_obj = Recipee(lunch[0],lunch[6],lunch[7],lunch[4],lunch[8],lunch[3],lunch[1],lunch_servings,lunch[2]);
        dinner_obj = Recipee(dinner[0],dinner[6],dinner[7],dinner[4],dinner[8],dinner[3],dinner[1],dinner_servings,dinner[2]);

        combinationToRet = MpCombination(breakfast_obj,lunch_obj,dinner_obj,score)

        return combinationToRet;

    @staticmethod
    def add_combination_lst(all_combinations,breakfast,lunch,dinner,breakfast_servings,lunch_servings,dinner_servings,score):
        comb1= MpCombination.create_combination(breakfast,lunch,dinner,breakfast_servings,lunch_servings,dinner_servings,score)
        all_combinations.append(comb1.mpCombination_json())
        return all_combinations;
 
    @staticmethod
    def transformJsonToMPcombination(jsonCombination):
        jsonBreakfast = jsonCombination['breakfast']
        jsonLunch = jsonCombination['lunch']
        jsonDinner = jsonCombination['dinner']
        score = jsonCombination['score']
        breakfast = Recipee.transformJsonToRecipee(jsonBreakfast)
        lunch = Recipee.transformJsonToRecipee(jsonLunch)
        dinner = Recipee.transformJsonToRecipee(jsonDinner)

        comb = MpCombination(breakfast,lunch, dinner,score)
        return comb.mpCombination_json()
    

    @staticmethod
    def getCombination(diet_id,patient_id,combination_id):
        cur = Db_connection.getConnection().cursor()
        try:
            query = '''select r.recipee_id, r.name, r.description, LOWER(r.meal_type), r.calories, r.fat, r.protein, r.servings, r.carbs
                        from meal_prep mp ,recipee r 
                        where mp.recipee_id = r.recipee_id 
                        and mp.patient_id =%s
                        and diet_id = %s
                        and combinationnbr =%s'''
            cur.execute(query, (patient_id,diet_id,combination_id))
            records = cur.fetchall()
    
            if records is None:
                return None
            for record in records:
                if record[3]=='breakfast':
                    breakfast = Recipee(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]);
                if record[3]=='lunch':
                    lunch = Recipee(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]);
                if record[3]=='dinner':
                    dinner = Recipee(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]); 
            
            return MpCombination(breakfast,lunch,dinner,0)
        except psycopg2.Error as e:
            return f"Database error: {e}"
        finally:
            if cur:
                cur.close()
    