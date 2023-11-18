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
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientHealthHistList(p_ID):
        cur = Db_connection.getConnection().cursor()
        if p_ID == '' :
            return('Please select a patient to display');
        cur.execute("SELECT patient_id, to_char(measurement_date, 'DD/MM/YYYY'), medical_diseases, medication, family_history, personal_history, bowel_movement, allergies_intolerences, diastolic_bp, systolic_bp, hdl_cholesterol, ldl_cholesterol, total_cholesterol, triglycerides FROM public.health_history where patient_id = %s ORDER BY measurement_date desc",(p_ID))
        result = cur.fetchall()
        cur.close
        return result
        

    @staticmethod
    def fetchPatientLastHealthHist(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        healthhists = HealthHist.fetchPatientHealthHistList(p_ID);
        lastHealthH = HealthHist(healthhists[0][0],healthhists[0][1],healthhists[0][2],healthhists[0][3],healthhists[0][4],healthhists[0][5],healthhists[0][6],healthhists[0][7],healthhists[0][8],healthhists[0][9],healthhists[0][10],healthhists[0][11],healthhists[0][12],healthhists[0][13])
        return lastHealthH.HealthHist_json();
        

    @staticmethod
    def fetchPatientAllHealthHist(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        healthhists = HealthHist.fetchPatientHealthHistList(p_ID);
        jsonHist = [];
        for healthhist in healthhists:
            histObject = HealthHist(healthhist[0],healthhist[1],healthhist[2],healthhist[3],healthhist[4],healthhist[5],healthhist[6],healthhist[7],healthhist[8],healthhist[9],healthhist[10],healthhist[11],healthhist[12],healthhist[13])
            jsonHist.append(histObject.HealthHist_json())
        return jsonHist;


    @staticmethod
    def addHealthHistory(patientJSON):
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                return "patient_ID is missing"
        else:
            return "patient_ID is missing"   

        query = 'INSERT INTO health_history ' + GlobalFunctions.buildInsertQuery(patient_data) 
        print(query)
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        return "health_history log addedsuccessfully"
    
    