from flask import jsonify, request
import json
import psycopg2
from Db_connection import Db_connection  # Assuming Db_connection is your database connection file

class Recipee:

    def __init__(self, recipee_id, name, description, meal_type, calories, fat, protein, servings, carbs):
       self.recipee_id=str(recipee_id)
       self.name=name
       self.description=description
       self.meal_type=meal_type
       self.calories=str(calories)
       self.fat=str(fat)
       self.protein=str(protein)
       self.servings=str(servings)
       self.carbs=str(carbs)

    def recipee_json(self):
        json_recipee = json.dumps(vars(self))
        return json_recipee
    
    @staticmethod
    def transformJsonToRecipee(jsonRecipee):
        recip = Recipee(jsonRecipee['recipee_id'],jsonRecipee['name'],jsonRecipee['description'],jsonRecipee['meal_type'] ,jsonRecipee['calories'] ,
                         jsonRecipee['fat'],jsonRecipee['protein'] ,jsonRecipee['servings'] ,jsonRecipee['carbs'] )

        return recip
                  
    @staticmethod
    def getRecipee(recipee_id):
        cur = Db_connection.getConnection().cursor()
        try:
            query = '''SELECT recipee_id, name, description, meal_type, calories, fat, protein, servings, carbs FROM recipee WHERE recipee_id=%s'''
            cur.execute(query, (recipee_id,))
            record = cur.fetchone()

            if record is None:
                return None
    
            recipee = Recipee(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8])
                
            
            return recipee.recipee_json()
        except psycopg2.Error as e:
            return f"Database error: {e}"
        finally:
            if cur:
                cur.close()
    
    