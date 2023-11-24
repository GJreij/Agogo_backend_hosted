import psycopg2
from werkzeug.exceptions import BadRequest
import json
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions


class LifeStyle:

    def __init__(self,patient_id, measurement_date, physical_activity, sleep_quality, smoker, 
                 alcohol_consumption, usual_wake_up_time, usual_bed_time, favorite_food, disliked_food, 
                 water_intake, eating_behaviour):
        print("LS Creating")
        self.patient_id=patient_id
        self.measurement_date=measurement_date
        self.physical_activity=physical_activity
        self.sleep_quality=sleep_quality
        self.smoker=smoker
        self.alcohol_consumption=alcohol_consumption
        self.usual_wake_up_time=usual_wake_up_time
        self.usual_bed_time=usual_bed_time
        self.favorite_food=favorite_food
        self.disliked_food=disliked_food
        self.water_intake=water_intake
        self.eating_behaviour=eating_behaviour
        print("LS Created")
        print(self.LifeStyle_json())

        
       
        
        
    def LifeStyle_json(self):
        self.measurement_date = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.measurement_date)
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientLifeStyleList(p_ID):
        cur = Db_connection.getConnection().cursor()
        cur.execute("SELECT patient_id, to_char(measurement_date, 'MM/DD/YYYY'), physical_activity, sleep_quality, smoker, alcohol_consumption, usual_wake_up_time, usual_bed_time, favorite_food, disliked_food, water_intake, eating_behaviour FROM public.life_style where patient_id = %s ORDER BY measurement_date desc",(p_ID,))
        result = cur.fetchall()
        cur.close
        return result
        

    @staticmethod
    def fetchPatientLastLifeStyle(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
            
        try:
            lifeStylehists = LifeStyle.fetchPatientLifeStyleList(p_ID);

            if len(lifeStylehists) == 0 :
                return GlobalFunctions.return_error_msg("Patient hs no Life Style info")
                
            lastLifeStyle = LifeStyle(lifeStylehists[0][0],lifeStylehists[0][1],lifeStylehists[0][2],lifeStylehists[0][3],lifeStylehists[0][4],lifeStylehists[0][5],lifeStylehists[0][6],lifeStylehists[0][7],lifeStylehists[0][8],lifeStylehists[0][9],lifeStylehists[0][10],lifeStylehists[0][11])
            return GlobalFunctions.return_success_msg(lastLifeStyle.LifeStyle_json());
       
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
        

    @staticmethod
    def fetchPatientLifeStyleHist(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
     
        try:
            lifeStylehists = LifeStyle.fetchPatientLifeStyleList(p_ID);
            jsonHist = [];
            for lifeStylehist in lifeStylehists:
                histObject = LifeStyle(lifeStylehist[0],lifeStylehist[1],lifeStylehist[2],lifeStylehist[3],lifeStylehist[4],lifeStylehist[5],lifeStylehist[6],lifeStylehist[7],lifeStylehist[8],lifeStylehist[9],lifeStylehist[10],lifeStylehist[11])
                jsonHist.append(histObject.LifeStyle_json())
            return GlobalFunctions.cleanJSON(jsonHist);
    
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    @staticmethod
    def addLifeStyle(patientJSON):
        err_msg = None
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '' or not patient_data['patient_ID'].isnumeric():
                err_msg = "Please insert a valid patient ID"
        else:
            err_msg = "patient_ID is missing"   
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
        
        try:
            query = 'INSERT INTO life_style ' + GlobalFunctions.buildInsertQuery(patient_data) 
            cur = Db_connection.getConnection().cursor()
            cur.execute(query)
            Db_connection.commit();
            cur.close()
            response = {
                        "status": "success",
                        "message": "Life Style log added successfully"
                    }            
            return json.dumps(response)
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
