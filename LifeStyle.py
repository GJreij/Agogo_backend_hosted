from werkzeug.exceptions import BadRequest
import json
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions


class LifeStyle:

    def __init__(self,patient_id, measurement_date, physical_activity, sleep_quality, smoker, 
                 alcohol_consumption, usual_wake_up_time, usual_bed_time, favorite_food, disliked_food, 
                 water_intake, eating_behaviour):
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

        
       
        
        
    def LifeStyle_json(self):
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientLifeStyleList(p_ID):
        cur = Db_connection.getConnection().cursor()
        if p_ID == '' :
            return('Please select a patient to display');
        cur.execute("SELECT patient_id, to_char(measurement_date, 'DD/MM/YYYY'), physical_activity, sleep_quality, smoker, alcohol_consumption, usual_wake_up_time, usual_bed_time, favorite_food, disliked_food, water_intake, eating_behaviour FROM public.life_style where patient_id = %s ORDER BY measurement_date desc",(p_ID))
        result = cur.fetchall()
        cur.close
        return result
        

    @staticmethod
    def fetchPatientLastLifeStyle(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        lifeStylehists = LifeStyle.fetchPatientLifeStyleList(p_ID);
        lastLifeStyle = LifeStyle(lifeStylehists[0][0],lifeStylehists[0][1],lifeStylehists[0][2],lifeStylehists[0][3],lifeStylehists[0][4],lifeStylehists[0][5],lifeStylehists[0][6],lifeStylehists[0][7],lifeStylehists[0][8],lifeStylehists[0][9],lifeStylehists[0][10],lifeStylehists[0][11])
        return lastLifeStyle.LifeStyle_json();
        

    @staticmethod
    def fetchPatientLifeStyleHist(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        lifeStylehists = LifeStyle.fetchPatientLifeStyleList(p_ID);
        jsonHist = [];
        for lifeStylehist in lifeStylehists:
            histObject = LifeStyle(lifeStylehist[0],lifeStylehist[1],lifeStylehist[2],lifeStylehist[3],lifeStylehist[4],lifeStylehist[5],lifeStylehist[6],lifeStylehist[7],lifeStylehist[8],lifeStylehist[9],lifeStylehist[10],lifeStylehist[11])
            jsonHist.append(histObject.LifeStyle_json())
        return jsonHist;


    @staticmethod
    def addLifeStyle(patientJSON):
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                return "patient_ID is missing"
        else:
            return "patient_ID is missing"   

        query = 'INSERT INTO life_style ' + GlobalFunctions.buildInsertQuery(patient_data) 
        print(query)
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        return "life_style log addedsuccessfully"
    