# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 21:18:00 2023

@author: gjreij-ext
"""

from flask import jsonify, request
import json
import psycopg2
from Db_connection import Db_connection  # Assuming Db_connection is your database connection file

class Ingredient:

    def __init__(self, ingredient_id, name, fat, carbs, protein, calories, grammes, liters, cup, tbsp, tsp, small, medium, large):
        self.ingredient_id = ingredient_id
        self.name = name
        self.fat = fat
        self.carbs = carbs
        self.protein = protein
        self.calories = calories
        self.grammes = grammes
        self.liters = liters
        self.cup = cup
        self.tbsp = tbsp
        self.tsp = tsp
        self.small = small
        self.medium = medium
        self.large = large

    def ingredient_json(self):
        json_ingredient = json.dumps(vars(self))
        return json_ingredient

    @staticmethod
    def fetchIngredientDetails(ingredient_id):
        cur = Db_connection.getConnection().cursor()
        if not ingredient_id:
            return('Please enter an Ingredient ID')

        cur.execute("SELECT ingredient_id,name, fat, carbs, protein, calories, grammes, liters, cup, tbsp, tsp, small, medium, large FROM public.ingredient WHERE ingredient_id = %s", (ingredient_id))
        ingredient = cur.fetchone()

        if cur.rowcount == 1:
            ingredient_id, name, fat, carbs, protein, calories, grammes, liters, cup, tbsp, tsp, small, medium, large = ingredient
        
            ingredient_obj = Ingredient(
                ingredient_id=ingredient_id,
                name=name,
                fat=fat,
                carbs=carbs,
                protein=protein,
                calories=calories,
                grammes=grammes,
                liters=liters,
                cup=cup,
                tbsp=tbsp,
                tsp=tsp,
                small=small,
                medium=medium,
                large=large
            )
            return jsonify(json.loads(ingredient_obj.ingredient_json()))

        else:
            return ('Ingredient Not Found')
        
    
    @staticmethod
    def addIngredient(ingredientJSON):
        ingredientData = json.loads(ingredientJSON)
        cur = Db_connection.getConnection().cursor()
        
        try:
            insert_query = """INSERT INTO public.ingredient (name, fat, carbs, protein, calories, grammes, liters, cup, tbsp, tsp, small, medium, large) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING ingredient_id;"""
            
            cur.execute(insert_query, (ingredientData["name"], ingredientData["fat"], ingredientData["carbs"], ingredientData["protein"], ingredientData["calories"], ingredientData["grammes"], ingredientData["liters"], ingredientData["cup"], 
                                       ingredientData["tbsp"], ingredientData["tsp"], ingredientData["small"], ingredientData["medium"], ingredientData["large"]))
            
            # Commit the transaction
            Db_connection.commit()
            
            # Fetch the automatically generated ingredient_id
            ingredient_id = cur.fetchone()[0]
            
            # Close the cursor
            cur.close()
            
            return f"Ingredient added successfully with ID: {ingredient_id}"
            
        except psycopg2.Error as e:
            return f"Database error: {e}"
    
    
    @staticmethod
    def updateIngredient(ingredient_id, updated_data):
        cur = Db_connection.getConnection().cursor()
        try:
            # Update the database record with the new values
            update_query = """UPDATE public.ingredient 
                              SET name=%s, fat=%s, carbs=%s, protein=%s, calories=%s, grammes=%s, liters=%s, 
                                  cup=%s, tbsp=%s, tsp=%s, small=%s, medium=%s, large=%s
                              WHERE ingredient_id=%s;"""
            
            cur.execute(update_query, (updated_data["name"], updated_data["fat"], updated_data["carbs"], 
                                       updated_data["protein"], updated_data["calories"], updated_data["grammes"], 
                                       updated_data["liters"], updated_data["cup"], updated_data["tbsp"], updated_data["tsp"], 
                                       updated_data["small"], updated_data["medium"], updated_data["large"], ingredient_id))
            
            # Commit the transaction and close the cursor
            Db_connection.commit()
            cur.close()
            
            if cur.rowcount:
                return f"Ingredient with ID: {ingredient_id} updated successfully."
            else:
                return f"No ingredient found with ID: {ingredient_id}"
    
        except psycopg2.Error as e:
            return f"Database error: {e}"
