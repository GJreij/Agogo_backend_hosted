from datetime import date
import psycopg2
from werkzeug.exceptions import BadRequest
import json
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions


class HealthHist:

    def __init__(self,patient_id, measurement_date, medical_diseases, medication, family_history, 
                 personal_history, bowel_movement, allergies_intolerences, diastolic_bp, systolic_bp, 
                 hdl_cholesterol, ldl_cholesterol, total_cholesterol, triglycerides):
        self.patient_id=patient_id
        self.measurement_date=measurement_date
        self.medical_diseases=medical_diseases
        self.medication=medication
        self.family_history=family_history
        self.personal_history=personal_history
        self.bowel_movement=bowel_movement
        self.allergies_intolerences=allergies_intolerences
        self.diastolic_bp=diastolic_bp
        self.systolic_bp=systolic_bp
        self.hdl_cholesterol=hdl_cholesterol
        self.ldl_cholesterol=ldl_cholesterol
        self.total_cholesterol=total_cholesterol
        self.triglycerides=triglycerides
       
        
        
    def HealthHist_json(self):
        self.measurement_date = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.measurement_date)
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientHealthHistList(p_ID):
        cur = Db_connection.getConnection().cursor()
        cur.execute("SELECT patient_id, to_char(measurement_date, 'MM/DD/YYYY'), medical_diseases, medication, family_history, personal_history, bowel_movement, allergies_intolerences, diastolic_bp, systolic_bp, hdl_cholesterol, ldl_cholesterol, total_cholesterol, triglycerides FROM public.health_history where patient_id = %s ORDER BY measurement_date desc",(p_ID,))
        result = cur.fetchall()
        cur.close
        return result
        

    @staticmethod
    def fetchPatientLastHealthHist(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
            
        try:
            healthhists = HealthHist.fetchPatientHealthHistList(p_ID);
            if len(healthhists) == 0 :
                return GlobalFunctions.return_error_msg("Patient has no Health History info")
              
            lastHealthH = HealthHist(healthhists[0][0],healthhists[0][1],healthhists[0][2],healthhists[0][3],healthhists[0][4],healthhists[0][5],healthhists[0][6],healthhists[0][7],healthhists[0][8],healthhists[0][9],healthhists[0][10],healthhists[0][11],healthhists[0][12],healthhists[0][13])
         
            return GlobalFunctions.return_success_msg(lastHealthH.HealthHist_json());
             

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
        

    @staticmethod
    def fetchPatientAllHealthHist(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
        try:
            healthhists = HealthHist.fetchPatientHealthHistList(p_ID);
            healthhists.reverse();
            jsonHist = [];
            for healthhist in healthhists:
                histObject = HealthHist(healthhist[0],healthhist[1],healthhist[2],healthhist[3],healthhist[4],healthhist[5],healthhist[6],healthhist[7],healthhist[8],healthhist[9],healthhist[10],healthhist[11],healthhist[12],healthhist[13])
                jsonHist.append(histObject.HealthHist_json())
            return GlobalFunctions.cleanJSON(jsonHist);

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    @staticmethod
    def insertHealthHist(patient_data):
        query = 'INSERT INTO health_history ' + GlobalFunctions.buildInsertQuery(patient_data) 
        print(query)
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        cur.close()
        response = {
                        "status": "success",
                        "message": "Health history log added successfully"
                    }            
        return json.dumps(response)

    @staticmethod
    def checkUpdate(patient_ID,measurement_date):
        cur = Db_connection.getConnection().cursor()
        cur.execute("SELECT count(*) FROM public.health_history where patient_id = %s AND measurement_date = to_date(%s, 'YYYY-MM-DD')",
                    (patient_ID,measurement_date,))
        count = cur.fetchone()
        cur.close
        
        if count[0] == 0:
            return False
        else:
            return True

    @staticmethod
    def updateHealthHist(patient_data):
        query = 'UPDATE health_history SET ' + GlobalFunctions.buildUpdateQuery(patient_data) 
        query = query + "WHERE patient_id = '" + str(patient_data['patient_ID']) + "' AND measurement_date = to_date('"+patient_data['measurement_date']+"', 'YYYY-MM-DD')"
        print(query)
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        response = {
                        "status": "success",
                        "message": "Health History log Updated successfully"
                    }
        return json.dumps(response)          

    @staticmethod
    def addHealthHistory(patientJSON):
        try:
            err_msg = None
            patient_data = json.loads(patientJSON)
            if 'patient_ID' in patient_data:
                if patient_data['patient_ID'] == '' or not patient_data['patient_ID'].isnumeric():
                    err_msg= "patient_ID is missing"
            else:
                err_msg= "patient_ID is missing"   
            #response if error
            if err_msg != None:
                return GlobalFunctions.return_error_msg(err_msg)
            

            #if front don't send measurment date, it will be set to sysdate
            if 'measurement_date' in patient_data:
                if patient_data['measurement_date'] == '':
                    patient_data['measurement_date'] = date.today().strftime("%m/%d/%Y")
            else:
                patient_data['measurement_date'] = date.today().strftime("%m/%d/%Y")
            
            patient_data['measurement_date'] = GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(patient_data['measurement_date'])

      
            #Checking if line already exists:
            if HealthHist.checkUpdate(patient_data['patient_ID'],GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(patient_data['measurement_date'])):
                return HealthHist.updateHealthHist(patient_data)
            else:
                return HealthHist.insertHealthHist(patient_data)

        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))