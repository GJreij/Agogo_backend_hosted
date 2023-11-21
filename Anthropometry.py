import psycopg2
from werkzeug.exceptions import BadRequest
import json
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions


class Anthropometry:

    def __init__(self,patient_id, measurement_date, weight, height, waist_circumference, hip_circumference, abdominal_skinfold, 
                 chest_skinfold, front_thigh_skinfold, midaxillary_skinfold, subscapular_skinfold, 
                 suprailiac_skinfold, triceps_skinfold):
        self.patient_id=patient_id
        self.measurement_date=measurement_date
        self.weight=weight
        self.height=height
        self.waist_circumference=waist_circumference
        self.hip_circumference=hip_circumference
        self.abdominal_skinfold=abdominal_skinfold
        self.chest_skinfold=chest_skinfold
        self.front_thigh_skinfold=front_thigh_skinfold
        self.midaxillary_skinfold=midaxillary_skinfold
        self.subscapular_skinfold=subscapular_skinfold
        self.suprailiac_skinfold=suprailiac_skinfold
        self.triceps_skinfold=triceps_skinfold
#ZZEsd
    def Anthropometry_json(self):
        self.measurement_date = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.measurement_date)
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientAnthropometryList(p_ID):
        cur = Db_connection.getConnection().cursor()
        cur.execute("SELECT patient_id, to_char(measurement_date, 'MM/DD/YYYY'), weight, height, waist_circumference, hip_circumference, abdominal_skinfold, chest_skinfold, front_thigh_skinfold, midaxillary_skinfold, subscapular_skinfold, suprailiac_skinfold, triceps_skinfold FROM anthropometry where patient_id = %s ORDER BY measurement_date desc",(p_ID))
        patientAnths = cur.fetchall()
        cur.close
        return patientAnths
        

    @staticmethod
    def fetchPatientLastAnth(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None:
            err_msg = 'Patient ID is missing'
        #response if error
        if err_msg != None:
            response = {
                        "status": "error",
                        "message": err_msg
                    }            
            return json.dumps(response)
            
        try:
            anths = Anthropometry.fetchPatientAnthropometryList(p_ID);
            if len(anths) == 0 :
                response = {
                        "status": "error",
                        "message": "Patient hs no Anthropometry info"
                    }            
                return json.dumps(response)
            lastAnth = Anthropometry(anths[0][0],anths[0][1],anths[0][2],anths[0][3],anths[0][4],anths[0][5],anths[0][6],anths[0][7],anths[0][8],anths[0][9],anths[0][10],anths[0][11],anths[0][12])
            to_ret = json.dumps(lastAnth.Anthropometry_json());
            return GlobalFunctions.cleanJSON(to_ret)
        except psycopg2.Error as e:
            response = {
                        "status": "error",
                        "message": "DB error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response)  
        except Exception as e:
            response = {
                        "status": "error",
                        "message": "Server error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response) 


    @staticmethod
    def fetchPatientAnthHist(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None:
            err_msg = 'Patient ID is missing'
        #response if error
        if err_msg != None:
            response = {
                        "status": "error",
                        "message": err_msg
                    }            
            return json.dumps(response)
            
        try:
            anths = Anthropometry.fetchPatientAnthropometryList(p_ID);        
            jsonAnthHist = [];
            for anth in anths:
                anthObject = Anthropometry(anth[0],anth[1],anth[2],anth[3],anth[4],anth[5],anth[6],anth[7],anth[8],anth[9],anth[10],anth[11],anth[12])
                jsonAnthHist.append(anthObject.Anthropometry_json())
            return GlobalFunctions.cleanJSON(jsonAnthHist)
        except psycopg2.Error as e:
            response = {
                        "status": "error",
                        "message": "DB error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response)  
        except Exception as e:
            response = {
                        "status": "error",
                        "message": "Server error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response) 
    
    
    @staticmethod
    def addAnthropometry(patientJSON):
        err_msg = None
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                err_msg = "patient_ID is missing"
        else:
            err_msg = "patient_ID is missng"   
        #response if error
        if err_msg != None:
            response = {
                        "status": "error",
                        "message": err_msg
                    }            
            return json.dumps(response)
        try:
            query = 'INSERT INTO anthropometry ' + GlobalFunctions.buildInsertQuery(patient_data) 
            cur = Db_connection.getConnection().cursor()
            cur.execute(query)
            Db_connection.commit();
            cur.close();
            response = {
                        "status": "success",
                        "message": "Anthropometry log added successfully"
                    }            
            return json.dumps(response)
        
        except psycopg2.Error as e:
            response = {
                        "status": "error",
                        "message": "DB error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response)  
        except Exception as e:
            response = {
                        "status": "error",
                        "message": "Server error: " + str(e)
                    }
            Db_connection.closeConnection(Db_connection.getConnection());              
            return json.dumps(response) 
