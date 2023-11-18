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
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientAnthropometryList(p_ID):
        cur = Db_connection.getConnection().cursor()
        if p_ID == '' :
            return('Please select a patient to display');
        cur.execute("SELECT patient_id, to_char(measurement_date, 'DD/MM/YYYY'), weight, height, waist_circumference, hip_circumference, abdominal_skinfold, chest_skinfold, front_thigh_skinfold, midaxillary_skinfold, subscapular_skinfold, suprailiac_skinfold, triceps_skinfold FROM anthropometry where patient_id = %s ORDER BY measurement_date desc",(p_ID))
        patientAnths = cur.fetchall()
        cur.close
        return patientAnths
        

    @staticmethod
    def fetchPatientLastAnth(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        anths = Anthropometry.fetchPatientAnthropometryList(p_ID);
        lastAnth = Anthropometry(anths[0][0],anths[0][1],anths[0][2],anths[0][3],anths[0][4],anths[0][5],anths[0][6],anths[0][7],anths[0][8],anths[0][9],anths[0][10],anths[0][11],anths[0][12])
        return lastAnth.Anthropometry_json();
        

    @staticmethod
    def fetchPatientAnthHist(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        anths = Anthropometry.fetchPatientAnthropometryList(p_ID);
       # lastAnth = Anthropometry(anths[0][0],anths[0][1],anths[0][2],anths[0][3],anths[0][4],anths[0][5],anths[0][6],anths[0][7],anths[0][8],anths[0][9],anths[0][10],anths[0][11],anths[0][12])
       
        jsonAnthHist = [];
        for anth in anths:
            anthObject = Anthropometry(anth[0],anth[1],anth[2],anth[3],anth[4],anth[5],anth[6],anth[7],anth[8],anth[9],anth[10],anth[11],anth[12])
            #patientsArray.append(patientObject)
            jsonAnthHist.append(anthObject.Anthropometry_json())
        return jsonAnthHist;

    @staticmethod
    def addAnthropometry(patientJSON):
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                return "patient_ID is missing"
            
        else:
            return "patient_ID is missng"   

        query = 'INSERT INTO anthropometry ' + GlobalFunctions.buildInsertQuery(patient_data) 
        print(query)
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        return "Anthropometry log addedsuccessfully"
    
    
