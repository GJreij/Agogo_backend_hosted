from datetime import date
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
        cur.execute("SELECT patient_id, to_char(measurement_date, 'MM/DD/YYYY'), body_fat_percentage, fat_mass, muscle_mass, muscle_mass_percentage, body_type FROM public.body_composition where patient_id = %s ORDER BY measurement_date desc",(p_ID,))
        patientBC = cur.fetchall()
        cur.close
        return patientBC
        

    @staticmethod
    def fetchPatientLastBC(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
            
        try:
            boCos = BodyComp.fetchPatientBodyCompList(p_ID);
            if len(boCos) == 0 :
                return GlobalFunctions.return_error_msg("Patient hs no Body Composition info")
            
            lastBC = BodyComp(boCos[0][0],boCos[0][1],boCos[0][2],boCos[0][3],boCos[0][4],boCos[0][5],boCos[0][6])
          
            return GlobalFunctions.return_success_msg(lastBC.BodyComp_json());
    
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
        

    @staticmethod
    def fetchPatientBCHist(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
            
        try:
            boCos = BodyComp.fetchPatientBodyCompList(p_ID);       
            jsonHist = [];
            for boCo in boCos:
                histObject = BodyComp(boCo[0],boCo[1],boCo[2],boCo[3],boCo[4],boCo[5],boCo[6])
                jsonHist.append(histObject.BodyComp_json())
            return GlobalFunctions.cleanJSON(jsonHist);
    
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    @staticmethod
    def insertBodyComp(patient_data):
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

       
    @staticmethod
    def updateBodyComp(patient_data):
            query = 'UPDATE body_composition SET ' + GlobalFunctions.buildUpdateQuery(patient_data) 
            query = query + "WHERE patient_id = '" + str(patient_data['patient_ID']) + "' AND measurement_date = to_date('"+patient_data['measurement_date']+"', 'YYYY-MM-DD')"
            print(query)
            cur = Db_connection.getConnection().cursor()
            cur.execute(query)
            Db_connection.commit();
            response = {
                        "status": "success",
                        "message": "Body composition log Updated successfully"
                    }
            return json.dumps(response)  

        
    @staticmethod
    def checkUpdate(patient_ID,measurement_date):
        cur = Db_connection.getConnection().cursor()
        cur.execute("SELECT count(*) FROM public.body_composition where patient_id = %s AND measurement_date = to_date(%s, 'YYYY-MM-DD')",
                    (patient_ID,measurement_date,))
        count = cur.fetchone()
        cur.close
        
        if count[0] == 0:
            return False
        else:
            return True

    @staticmethod
    def addBodyComp(patientJSON):
        try:
            err_msg = None
            patient_data = json.loads(patientJSON)
            if 'patient_ID' in patient_data:
                if patient_data['patient_ID'] == ''  or not patient_data['patient_ID'].isnumeric():
                    err_msg = 'Please insert a valid patient ID'
            else:
                err_msg = "patient_ID is missing"   
            #response if error
            if err_msg != None:
                GlobalFunctions.return_error_msg(err_msg)

            #if front don't send measurment date, it will be set to sysdate
            if 'measurement_date' in patient_data:
                if patient_data['measurement_date'] == '':
                    patient_data['measurement_date'] = date.today().strftime("%m/%d/%Y")
            else:
                patient_data['measurement_date'] = date.today().strftime("%m/%d/%Y")
            
            patient_data['measurement_date'] = GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(patient_data['measurement_date'])
          
            #Checking if line already exists:
            if BodyComp.checkUpdate(patient_data['patient_ID'],GlobalFunctions.convert_date_to_DB_yyyy_mm_dd(patient_data['measurement_date'])):
                return BodyComp.updateBodyComp(patient_data)
            else:
                return BodyComp.insertBodyComp(patient_data)
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
        


        