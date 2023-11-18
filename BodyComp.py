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
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchPatientBodyCompList(p_ID):
        cur = Db_connection.getConnection().cursor()
        if p_ID == '' :
            return('Please select a patient to display');
        cur.execute("SELECT patient_id, to_char(measurement_date, 'DD/MM/YYYY'), body_fat_percentage, fat_mass, muscle_mass, muscle_mass_percentage, body_type FROM public.body_composition where patient_id = %s ORDER BY measurement_date desc",(p_ID))
        patientBC = cur.fetchall()
        cur.close
        return patientBC
        

    @staticmethod
    def fetchPatientLastBC(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        boCos = BodyComp.fetchPatientBodyCompList(p_ID);
        lastBC = BodyComp(boCos[0][0],boCos[0][1],boCos[0][2],boCos[0][3],boCos[0][4],boCos[0][5],boCos[0][6])
        return lastBC.BodyComp_json();
        

    @staticmethod
    def fetchPatientBCHist(p_ID):
        if p_ID == '' :
            return('Please select a patient to display');
        boCos = BodyComp.fetchPatientBodyCompList(p_ID);       
        jsonHist = [];
        for boCo in boCos:
            histObject = BodyComp(boCo[0],boCo[1],boCo[2],boCo[3],boCo[4],boCo[5],boCo[6])
            jsonHist.append(histObject.BodyComp_json())
        return jsonHist;


    @staticmethod
    def addBodyComp(patientJSON):
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                return "patient_ID is missing"
        else:
            return "patient_ID is missing"   

        query = 'INSERT INTO body_composition ' + GlobalFunctions.buildInsertQuery(patient_data) 
        print(query)
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        return "body_composition log addedsuccessfully"
    
    