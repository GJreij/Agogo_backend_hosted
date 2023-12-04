from GlobalFunctions import GlobalFunctions
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
        err_msg = None
        if diet_id == '' or diet_id == None or not diet_id.isnumeric():
            err_msg = 'Please insert a valid Diet ID'
        if patient_id == '' or patient_id == None or not patient_id.isnumeric():
            err_msg = 'Please insert a valid patient ID'  
        if combination_id == '' or combination_id == None or not combination_id.isnumeric():
            err_msg = 'Please insert a valid combination ID'                      
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
        
        try:
            cur = Db_connection.getConnection().cursor()
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
            cur.close()
            return MpCombination(breakfast,lunch,dinner,0)
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    
    @staticmethod
    def insertCombinations(jsonCombs):
        try:
            for combination in jsonCombs:
                print(combination)
                if not 'diet_id' in combination or not 'breakfast' in combination or not 'breakfastservings' in combination or not 'lunch' in combination or not 'lunchservings' in combination or not 'dinner' in combination or not 'dinnerservings' in combination or not 'patient_id' in combination or combination['diet_id'] == None or combination['breakfast'] == None or combination['breakfastservings'] == None or combination['lunch'] == None or combination['lunchservings'] == None or combination['dinner'] == None or combination['dinnerservings'] == None or combination['patient_id'] == None or combination['diet_id'] == '' or combination['breakfast'] == '' or combination['breakfastservings'] == '' or combination['lunch'] == '' or combination['lunchservings'] == '' or combination['dinner'] == '' or combination['dinnerservings'] == '' or combination['patient_id'] == '':
                    return GlobalFunctions.return_error_msg("the combination has missing values: "+ json.dumps(combination) )
                MpCombination.insertCombination(combination)

            return GlobalFunctions.return_success_msg("Combinations added successfully")
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
        

    @staticmethod
    def insertCombination(combination):
        query = 'INSERT INTO combination ' + GlobalFunctions.buildInsertQuery(combination) 
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        cur.close()
        return "Combination added successfully"
    

    @staticmethod
    def getDayCombination(dietID,patientID):
        try:
            combinationsToRet = []
            cur = Db_connection.getConnection().cursor()
            query = '''select  combination_id, diet_id, patient_id,
                        breakfast, breakfastservings, 
                        lunch, lunchservings, 
                        dinner, dinnerservings
                        FROM combination
                        WHERE patient_id =%s
                        and diet_id = %s'''
            cur.execute(query, (patientID,dietID,))
            records = cur.fetchall()
    
            if records is None:
                return GlobalFunctions.return_error_msg("no combinations found")
            for record in records:
                breakfast = Recipee.getRecipee(record[3])
                breakfast = Recipee.transformJsonToRecipee(json.loads(breakfast))
                breakfast.setServings(record[4])
                lunch = Recipee.getRecipee(record[5])
                lunch = Recipee.transformJsonToRecipee(json.loads(lunch))
                lunch.setServings(record[6])
                dinner = Recipee.getRecipee(record[7])
                dinner = Recipee.transformJsonToRecipee(json.loads(dinner))
                dinner.setServings(record[8])
                combinationsToRet.append(MpCombination(breakfast,lunch,dinner,0).mpCombination_json())
               
            cur.close()

            return GlobalFunctions.cleanJSON(GlobalFunctions.return_success_msg(combinationsToRet))
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))