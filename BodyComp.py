import psycopg2
from werkzeug.exceptions import BadRequest
import json
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions


class BodyComp:

    def __init__(self,patient_id, measurement_date, body_fat_percentage, fat_mass, muscle_mass, muscle_mass_percentage, body_type):
        self.patient_id=patient_id
        self.measurement_date=measurement_date
        self.body_fat_percentage=body_fat_percentage
        self.fat_mass=fat_mass
        self.muscle_mass=muscle_mass
        self.muscle_mass_percentage=muscle_mass_percentage
        self.body_type=body_type
        
        
    def BodyComp_json(self):
        self.measurement_date = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.measurement_date)
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientBodyCompList(p_ID):
        cur = Db_connection.getConnection().cursor()
        cur.execute("SELECT patient_id, to_char(measurement_date, 'MM/DD/YYYY'), body_fat_percentage, fat_mass, muscle_mass, muscle_mass_percentage, body_type FROM public.body_composition where patient_id = %s ORDER BY measurement_date desc",(p_ID))
        patientBC = cur.fetchall()
        cur.close
        return patientBC
        

    @staticmethod
    def fetchPatientLastBC(p_ID):
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
            boCos = BodyComp.fetchPatientBodyCompList(p_ID);
            if len(boCos) == 0 :
                response = {
                        "status": "error",
                        "message": "Patient hs no Body Composition info"
                    }            
                return json.dumps(response)
            lastBC = BodyComp(boCos[0][0],boCos[0][1],boCos[0][2],boCos[0][3],boCos[0][4],boCos[0][5],boCos[0][6])
            return lastBC.BodyComp_json();
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
    def fetchPatientBCHist(p_ID):
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
            boCos = BodyComp.fetchPatientBodyCompList(p_ID);       
            jsonHist = [];
            for boCo in boCos:
                histObject = BodyComp(boCo[0],boCo[1],boCo[2],boCo[3],boCo[4],boCo[5],boCo[6])
                jsonHist.append(histObject.BodyComp_json())
            return GlobalFunctions.cleanJSON(jsonHist);
    
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
    def addBodyComp(patientJSON):
        err_msg = None
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                err_msg = "patient_ID is missing"
        else:
            err_msg = "patient_ID is missing"   
        #response if error
        if err_msg != None:
            response = {
                        "status": "error",
                        "message": err_msg
                    }            
            return json.dumps(response)
        try:
            query = 'INSERT INTO body_composition ' + GlobalFunctions.buildInsertQuery(patient_data) 
            print(query)
            cur = Db_connection.getConnection().cursor()
            cur.execute(query)
            Db_connection.commit();
            response = {
                        "status": "success",
                        "message": "Body composition log added successfully"
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