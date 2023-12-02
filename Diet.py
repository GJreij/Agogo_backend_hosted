# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 23:38:47 2023

@author: gjreij-ext
"""

import json
from Db_connection import Db_connection
import psycopg2
from GlobalFunctions import GlobalFunctions

from MpCombination import MpCombination

class Diet:
    def __init__(self, diet_id, patient_id, start_date, end_date, calories_intake, fat_intake, carbs_intake, protein_intake, meals_nbr):
        self.diet_id = diet_id
        self.patient_id = patient_id
        self.start_date = start_date
        self.end_date = end_date
        self.calories_intake = calories_intake
        self.fat_intake = fat_intake
        self.carbs_intake = carbs_intake
        self.protein_intake = protein_intake
        self.meals_nbr = meals_nbr

    def diet_json(self):
        return json.dumps(vars(self))

    @staticmethod
    def createDiet(dietJSON):
        dietData = json.loads(dietJSON)
        cur = Db_connection.getConnection().cursor()
        
        try:
            query = '''INSERT INTO public.diet (patient_id, start_date, end_date, calories_intake, fat_intake, carbs_intake, protein_intake, meals_nbr, notes) 
                       VALUES (%s, TO_DATE(%s,'YYYY-MM-DD'), TO_DATE(%s,'YYYY-MM-DD'), %s, %s, %s, %s, %s,%s) RETURNING diet_id'''
            print(query)
            cur.execute(query, (dietData["patient_id"], 
                                GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(dietData["start_date"]), 
                                GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(dietData["end_date"]), 
                                dietData["calories_intake"], 
                                dietData["fat_intake"], dietData["carbs_intake"], dietData["protein_intake"], dietData["meals_nbr"],dietData["notes"]))
            diet_id = cur.fetchone()[0]
            cur.connection.commit()
            cur.close()
            return GlobalFunctions.return_success_msg(diet_id)
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    @staticmethod
    def updateDiet(diet_id, updated_data):
        
        cur = Db_connection.getConnection().cursor()
        
        try:
            query = '''UPDATE public.diet SET patient_id=%s, start_date=%s, end_date=%s, calories_intake=%s, 
                       fat_intake=%s, carbs_intake=%s, protein_intake=%s, meals_nbr=%s, notes=%s WHERE diet_id=%s'''
            cur.execute(query, (updated_data["patient_id"], 
                                GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(updated_data["start_date"]), 
                                GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(updated_data["end_date"]), 
                                updated_data["calories_intake"], updated_data["fat_intake"], updated_data["carbs_intake"], 
                                updated_data["protein_intake"], updated_data["meals_nbr"], updated_data["notes"], diet_id))
            cur.connection.commit()

            # Check if the update was successful
            if cur.rowcount:
                cur.close()
                return GlobalFunctions.return_success_msg(f"Diet updated successfully with ID: {diet_id}.")
            else:
                cur.close()
                return GlobalFunctions.return_error_msg("No record found with the given ID")

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
        
    @staticmethod
    def deleteDiet(diet_id):
        
        cur = Db_connection.getConnection().cursor()
        
        try:
            query = '''DELETE FROM public.diet WHERE diet_id=%s'''
            cur.execute(query, (diet_id,))
            cur.connection.commit()
            
            # Check if the delete was successful
            if cur.rowcount:
                cur.close()
                return GlobalFunctions.return_success_msg(f"Diet deleted successfully with ID: {diet_id}.")
            else:
                cur.close()
                return GlobalFunctions.return_error_msg("No record found with the given ID")
                
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))                
        
    @staticmethod
    def getDietHistory(patient_id):
        cur = Db_connection.getConnection().cursor()
        diets = []
        try:
            query = '''SELECT diet_id, patient_id, start_date, end_date, calories_intake, fat_intake, carbs_intake, protein_intake, meals_nbr, notes FROM public.diet WHERE patient_id=%s'''
            cur.execute(query, (patient_id,))
            records = cur.fetchall()
            for record in records:
                diet = {
                    'diet_id': str(record[0]),
                'patient_id': str(record[1]),
                'start_date': str(record[2]),
                'end_date': str(record[3]),
                'calories_intake': str(record[4]),
                'fat_intake': str(record[5]),
                'carbs_intake': str(record[6]),
                'protein_intake': str(record[7]),
                'meals_nbr': str(record[8]),
                'notes' : str(record[9])
                }
                diets.append(diet)
            return GlobalFunctions.cleanJSON(GlobalFunctions.return_success_msg(diets))
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))   
                
    @staticmethod
    def getLastDiet(patient_id):
        try:
            cur = Db_connection.getConnection().cursor()
            query = '''SELECT 
             diet_id, patient_id, start_date, end_date, calories_intake, fat_intake, carbs_intake, protein_intake, meals_nbr, notes
               FROM public.diet WHERE patient_id=%s ORDER BY start_date DESC LIMIT 1'''
            cur.execute(query, (patient_id,))
            record = cur.fetchone()
    
            if record is None:
                return GlobalFunctions.return_error_msg("No previous diet")
                
            diet = {
                'diet_id': str(record[0]),
                'patient_id': str(record[1]),
                'start_date': str(record[2]),
                'end_date': str(record[3]),
                'calories_intake': str(record[4]),
                'fat_intake': str(record[5]),
                'carbs_intake': str(record[6]),
                'protein_intake': str(record[7]),
                'meals_nbr': str(record[8]),
                'notes' : str(record[9])
            }
            return GlobalFunctions.return_success_msg(diet)
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))


    @staticmethod
    def getDietCombinations(diet_id,patient_id):
        # cur = Db_connection.getConnection().cursor()
        try:
            cur2 = Db_connection.getConnection().cursor()
            # query = '''select r.recipee_id, r.name, r.description, r.meal_type, r.calories, r.fat, r.protein, r.servings, r.carbs,mp.combinationnbr
            #             from meal_prep mp ,recipee r 
            #             where mp.recipee_id = r.recipee_id 
            #             and mp.patient_id =%s
            #             and diet_id = %s
            #             order by combinationnbr '''
            # cur.execute(query, (patient_id,diet_id))
            # records = cur.fetchall()
            maxQ = '''select DISTINCT(mp.combinationnbr)
                        from meal_prep mp ,recipee r 
                        where mp.recipee_id = r.recipee_id 
                        and mp.patient_id =%s
                        and diet_id = %s'''
            cur2.execute(maxQ,(patient_id,diet_id))
            nbr_comb = cur2.fetchall()
            combinations = []
            for i in nbr_comb:
                combination = MpCombination.getCombination(diet_id,patient_id,i[0])
                combinations.append(combination.mpCombination_json())

            return combinations
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))