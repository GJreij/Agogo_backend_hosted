from flask import jsonify
import flask
import psycopg2
from werkzeug.exceptions import BadRequest
import json
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions
from Patient import Patient


class Dietitian:

    # raise_amount = 1.04 -- this will appear in all classes 
    # in the self.raise_amount or Class.raise_amount but can be overridable

    def __init__(self,dietitian_id,first_name,family_name,date_of_birth,phone_number,email):
        self.dietitian_id=dietitian_id
        self.first_name=first_name
        self.family_name=family_name
        self.date_of_birth=date_of_birth
        self.phone_number=phone_number
        self.email=email
        # Dietitian.num_of_emps +=1 This will create a variable in all the instances

    def dietitian_json(self):
        print('json dietitian______')
        self.date_of_birth = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.date_of_birth)
        jsonDietitian = json.dumps(vars(self));
        jsonDietitian = jsonDietitian.replace(r'"{\\', '{').replace('\\', '').replace('}"','}')
        print(jsonDietitian)
        return jsonDietitian;



# STATIC METHODS TO BE USED
    @staticmethod
    def fetchDietitian(dietitian_ID):
        try:
            if dietitian_ID == '' or not dietitian_ID.isnumeric():
                return GlobalFunctions.return_error_msg("Please enter a valid dietitian_ID")

            cur = Db_connection.getConnection().cursor()
            cur.execute("select d.dietitian_id, d.first_name , d.family_name , to_char(d.date_of_birth, 'MM/DD/YYYY'), d.phone_number ,d.email from dietitian d where d.dietitian_id = %s",(dietitian_ID,))
            dietitian = cur.fetchall()
            if cur.rowcount == 1 :
                dietitianR = Dietitian(dietitian[0][0],dietitian[0][1],dietitian[0][2],dietitian[0][3],dietitian[0][4],dietitian[0][5])
                cur.close();
                return dietitianR.dietitian_json();
            else :
                cur.close();
                return GlobalFunctions.return_error_msg("The dietitian does not exist")

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))



    @staticmethod
    def fetchDietitianPatients(dietitian_ID):
        try:
            if dietitian_ID == '' or not dietitian_ID.isnumeric():
                return GlobalFunctions.return_error_msg("Please enter a valid dietitian_ID")
            
            cur = Db_connection.getConnection().cursor()
            cur.execute("select p.patient_id ,p.first_name ,p.last_name ,p.gender ,to_char(p.date_of_birth, 'MM/DD/YYYY'),p.phone ,p.email ,p.address ,p.dietitian_id ,p.status  from patient_static_info p where p.dietitian_id = %s",(dietitian_ID,))
            patients = cur.fetchall()
            jsonPatientsArray = [];
            for patient in patients:
                patientObject = Patient(patient[0],patient[1],patient[2],patient[3],patient[4],patient[5],patient[6],patient[7],patient[8],patient[9])
                jsonPatientsArray.append(patientObject.Patient_json())
            cur.close();
            return GlobalFunctions.cleanJSON(jsonPatientsArray);

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))


#insert methods
    @staticmethod
    def createPatient(patientJSON):
        try:
            patientData = json.loads(patientJSON)
            dietitian_ID = patientData['dietitian_id']
            error_msg = None
            if patientData['dietitian_id'] == '' or not dietitian_ID.isnumeric():
                error_msg = "Please enter a valid dietitian_ID"
            if patientData['pwd'] =='' :
                error_msg = "Please set a temporary password for the client"
            #return if error
            if error_msg != None:
                return GlobalFunctions.return_error_msg(error_msg)

            cur = Db_connection.getConnection().cursor()
            cur.execute("INSERT INTO public.patient_static_info (first_name, last_name, gender, date_of_birth, phone, email, address, dietitian_id, pwd, status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING patient_id"
                        ,(patientData['first_name'], patientData['last_name'], patientData['gender'],
                        GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(patientData['date_of_birth']), 
                        patientData['phone'], patientData['email'], patientData['address'], patientData['dietitian_id']
                        , patientData['pwd'], 'ACTIVE'));
            patient_ID = cur.fetchone()[0]
            Db_connection.commit();
            cur.close();
            patientData['patient_id'] = str(patient_ID)
            patientR = Patient(str(patient_ID),patientData['first_name'],patientData['last_name'], patientData['gender'],patientData['date_of_birth'],
                            patientData['phone'], patientData['email'], patientData['address'], patientData['dietitian_id'],'ACTIVE')
            
            return patientR.Patient_json();

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    
    @staticmethod
    def deactivatePatient(patient_ID):
        try:
            if patient_ID == '' or not patient_ID.isnumeric():
                return GlobalFunctions.return_error_msg("Please enter a valid Patient ID")
               
            cur = Db_connection.getConnection().cursor()
            cur.execute("UPDATE patient_static_info SET status= %s WHERE patient_id= %s",("UNACTIVE",patient_ID));
            Db_connection.commit();
            cur.close();
            msg_succes= "Patient "+ patient_ID + " Deactivated successfully"
            response = {
                        "status": "success",
                        "message": msg_succes
                    }
            return response
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))        

    @staticmethod
    def activatePatient(patient_ID):
        try:
            if patient_ID == '' or not patient_ID.isnumeric():
                return GlobalFunctions.return_error_msg("Please enter a valid Patient ID")
            
            cur = Db_connection.getConnection().cursor()
            cur.execute("UPDATE patient_static_info SET status= %s WHERE patient_id= %s",("ACTIVE",patient_ID));
            Db_connection.commit();
            cur.close();
            msg_succes= "Patient "+ patient_ID + " Activated successfully"
            response = {
                        "status": "success",
                        "message": msg_succes
                    }
            return response    
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))


    
    @staticmethod
    def addDietitian(dietitianData):
        dietitianData = json.loads(dietitianData)
        try:
            if dietitianData['email'] == '':
                return GlobalFunctions.return_error_msg("Dietitian Email is a mandatory field")
            
            cur = Db_connection.getConnection().cursor()
            query = 'INSERT INTO dietitian ' + GlobalFunctions.buildInsertQuery(dietitianData) + ' RETURNING dietitian_id' 
            cur.execute(query)
            # Commit the transaction
            Db_connection.commit()
            # Fetch the automatically generated ingredient_id
            dietitian_id = cur.fetchone()[0]
            # Close the cursor
            cur.close();
            response = {
                        "status": "success",
                        "message": "Operation completed successfully.",
                        "dietitian_id" : dietitian_id
                    }

            return json.dumps(response)
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
    
    
    
    @staticmethod
    def updateDietitian(updated_data):
        updated_data = json.loads(updated_data)
        dietitian_id = updated_data['dietitian_id']
        error_msg = None
        try:
            if 'dietitian_id' in updated_data:
                if updated_data['dietitian_id'] == '' or not dietitian_id.isnumeric():
                    error_msg = "dietitian_id is missing"
            else:
                error_msg = "dietitian_id is missing"
            if error_msg != None:
                return GlobalFunctions.return_error_msg(error_msg)

            cur = Db_connection.getConnection().cursor()
            update_query = 'UPDATE dietitian SET ' + GlobalFunctions.buildUpdateQuery(updated_data) 
            update_query = update_query + "WHERE dietitian_id = '" + str(dietitian_id) + "'"
                
            cur.execute(update_query)
            
            # Commit the transaction and close the cursor
            Db_connection.commit()
            cur.close()
            
            response = {
                        "status": "success",
                        "message": "Operation completed successfully.",
                        "dietitian_id" : dietitian_id
                    }
            return json.dumps(response)
    
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

#HERE
    @staticmethod
    def getDietitians():
        try:                
            cur = Db_connection.getConnection().cursor()
            
            query = "SELECT dietitian_id,first_name,family_name,to_char(date_of_birth, 'MM/DD/YYYY'),phone_number,email FROM dietitian"
            print(query)
            cur.execute(query)
            # dietitianID,Fname,Lname,DOB,phone,email
            # Commit the transaction and close the cursor
            dietitians = cur.fetchall()
            #patientsArray = [];
            jsonDietitiansArray = [];
            for dietitian in dietitians:
                dietitianObject = Dietitian(dietitian[0],dietitian[1],dietitian[2],dietitian[3],dietitian[4],dietitian[5])
                jsonDietitiansArray.append(dietitianObject.dietitian_json())            
            cur.close()

            jsonDietitiansArray = GlobalFunctions.cleanJSON(jsonDietitiansArray)
            # jsonDietitiansArray = json.dumps(jsonDietitiansArray)
            # jsonDietitiansArray = jsonDietitiansArray.replace(r'"{\\', '{').replace('\\', '').replace('}"','}').replace('"{', '{')
            return jsonDietitiansArray;
    
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    @staticmethod
    def removeDietitian(dietitian_id):
        try:
            if dietitian_id  == '':
                return GlobalFunctions.return_error_msg("dietitian_id is missing")
                
            cur = Db_connection.getConnection().cursor()
            query = "DELETE FROM dietitian WHERE dietitian_id = %s"
                
            cur.execute(query,(dietitian_id,))
            
            # Commit the transaction and close the cursor
            Db_connection.commit()
            cur.close()
            
            if cur.rowcount:
                response = {
                        "status": "success",
                        "message": "Dietitian removed successfully",
                        "dietitian_id" : dietitian_id
                    }
                return json.dumps(response) 
            else:
                error_msg = "Dietitian " +dietitian_id+ " not found"
                return GlobalFunctions.return_error_msg(error_msg)
    
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e)) 