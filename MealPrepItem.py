# Model for MealPrep
import psycopg2
from Db_connection import Db_connection
import json

from GlobalFunctions import GlobalFunctions

    
class MealPrepItem:


    def __init__(self, diet_id, recipee_id, date, meal_type, servings, patient_id, diet_start_date, combinationnbr):
        self.diet_id=diet_id
        self.recipee_id=recipee_id
        self.date=date
        self.meal_type=meal_type
        self.servings=servings
        self.patient_id=patient_id
        self.diet_start_date=diet_start_date
        self.combinationnbr=combinationnbr


    def mpItem_json(self):
        json_mpItem = json.dumps(vars(self))
        return json_mpItem

    @staticmethod
    def mpItem_PK_check(mpItem):
         #PK Checks
        if 'diet_id' in mpItem:
            if mpItem['diet_id'] == '':
                return "diet_id is missing"
        if 'recipee_id' in mpItem:
            if mpItem['recipee_id'] == '':
                return "recipee_id is missing"
        if 'meal_type' in mpItem:
            if mpItem['meal_type'] == '':
                return "meal_type is missing"
        if 'patient_id' in mpItem:
            if mpItem['patient_id'] == '':
                return "patient_id is missing"
        if 'diet_start_date' in mpItem:
            if mpItem['diet_start_date'] == '':
                return "diet_start_date is missing"
        if 'combinationnbr' in mpItem:
            if mpItem['combinationnbr'] == '':
                return "combinationnbr is missing"
        return "ok"

    @staticmethod
    def addMealPrepItem(mpItemJSON):
        try:
            mpItem = json.loads(mpItemJSON)
            pk_check = MealPrepItem.mpItem_PK_check(mpItem)
            if pk_check != "ok":
                return GlobalFunctions.return_error_msg(pk_check)
        
            cur = Db_connection.getConnection().cursor()
        
        
            insert_query = """INSERT INTO public.meal_prep (diet_id, recipee_id, date, meal_type, servings, patient_id, diet_start_date, combinationnbr) 
            VALUES(%s, %s, TO_DATE(%s,'YYYY-MM-DD'), %s, %s, %s, TO_DATE(%s,'YYYY-MM-DD'), %s);"""
            
            cur.execute(insert_query, (mpItem["diet_id"], mpItem["recipee_id"], 
                                    GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(mpItem["date"]),
                                      mpItem["meal_type"], mpItem["servings"],mpItem["patient_id"], 
                                      GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(mpItem["diet_start_date"]),
                                          mpItem["combinationnbr"]))
                        
            # Commit the transaction
            Db_connection.commit()
            
            # Close the cursor
            cur.close()
            response = {
                        "status": "success",
                        "message": "Meal Prep Item inserted successfully"
                    }            
            return json.dumps(response)
            
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))   
        


    @staticmethod
    def addbulkMealPrepItems(mpItemsJson):
        try:
            insert_query = """INSERT INTO public.meal_prep (diet_id, recipee_id, date, meal_type, servings, patient_id, diet_start_date, combinationnbr) VALUES """
            comma = 'n'
            mpItemsJson = json.loads(mpItemsJson)
            
            for mpItem in mpItemsJson:
                mpItem = json.loads(json.dumps(mpItem))
                print(mpItem)
                pk_check = MealPrepItem.mpItem_PK_check(mpItem)
                if pk_check != "ok":
                    return GlobalFunctions.return_error_msg(pk_check)
                
                if comma == 'y':
                    insert_query = insert_query+','
                insert_query =insert_query+ "('"+mpItem["diet_id"]+"', '"+mpItem["recipee_id"]+"', TO_DATE('"+GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(mpItem["date"])+"','YYYY-MM-DD'),'"+ mpItem["meal_type"]+"', '"+mpItem["servings"]+"', '"+mpItem["patient_id"]+"', TO_DATE('"+GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(mpItem["diet_start_date"])+"','YYYY-MM-DD'),'" +mpItem["combinationnbr"]+"')"
                comma = 'y';
            print(insert_query)
            cur = Db_connection.getConnection().cursor()
        
            cur.execute(insert_query)
          # Commit the transaction
            Db_connection.commit()
            
            # Close the cursor
            cur.close()
            
            response = {
                        "status": "success",
                        "message": "meal prep items added successfully"
                    }            
            return json.dumps(response)
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))   
        
        