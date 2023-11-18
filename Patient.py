from werkzeug.exceptions import BadRequest
import json
from Anthropometry import Anthropometry
from BodyComp import BodyComp
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions
from HealthHist import HealthHist
from LifeStyle import LifeStyle


class Patient:

    def __init__(self,patient_id,first_name,last_name,gender,date_of_birth,phone,email,address,dietitian_id,status ):
        self.patient_id=patient_id
        self.first_name=first_name
        self.last_name=last_name
        self.gender=gender
        self.gender=gender
        self.date_of_birth=date_of_birth
        self.phone=phone
        self.email=email
        self.address=address
        self.dietitian_id=dietitian_id
        self.status=status;


    def Patient_json(self):
        return json.dumps(vars(self));

    def printPatient(self):
        print('patient ID: ',self.patient_id, ' - patient full name: ', self.first_name, ' ', self.last_name)


# STATIC METHODS TO BE USED
    @staticmethod
    def fetchPatient(p_email,p_pwd):
        cur = Db_connection.getConnection().cursor()
        if p_email == '' or p_pwd == '':
            return('Please enter an Email and Password');
        cur.execute("select p.patient_id ,p.first_name ,p.last_name ,p.gender ,to_char(p.date_of_birth, 'DD/MM/YYYY'),p.phone ,p.email ,p.address ,p.dietitian_id ,p.status  from patient_static_info p where p.email = %s and p.pwd = %s",(p_email,p_pwd))
        patient = cur.fetchall()
        if cur.rowcount == 1 :
            print(cur.rowcount)
            patientR = Patient(patient[0][0],patient[0][1],patient[0][2],patient[0][3],patient[0][4],patient[0][5],patient[0][6],patient[0][7],patient[0][8],patient[0][9])
            cur.close;
            return patientR.Patient_json();
        else :
            cur.close;
            return('The email or password is incorrect');

    @staticmethod
    def fetchPatientStaticInfo(p_ID):
        cur = Db_connection.getConnection().cursor()
        if p_ID == '' :
            return('Please select a patient to display');
        cur.execute("select p.patient_id ,p.first_name ,p.last_name ,p.gender ,to_char(p.date_of_birth, 'DD/MM/YYYY'),p.phone ,p.email ,p.address ,p.dietitian_id ,p.status  from patient_static_info p where p.patient_id = %s",(p_ID))
        patient = cur.fetchall()
        if cur.rowcount == 1 :
            patientR = Patient(patient[0][0],patient[0][1],patient[0][2],patient[0][3],patient[0][4],patient[0][5],patient[0][6],patient[0][7],patient[0][8],patient[0][9])
            cur.close;
            return patientR.Patient_json();
        else :
            cur.close;
            return('The patient ID is incorrect');

    @staticmethod
    def fetchPatientAllInfo(p_ID):
        p_stat_info = Patient.fetchPatientStaticInfo(p_ID);
        p_Anthropometry = Anthropometry.fetchPatientLastAnth(p_ID);
        p_BodyComp = BodyComp.fetchPatientLastBC(p_ID)
        p_HealthHist = HealthHist.fetchPatientLastHealthHist(p_ID)
        p_LifeStyle = LifeStyle.fetchPatientLastLifeStyle(p_ID)
        p_data = {}
        p_data['p_stat_info'] = p_stat_info
        p_data['p_Anthropometry'] = p_Anthropometry
        p_data['p_BodyComp'] = p_BodyComp
        p_data['p_HealthHist'] = p_HealthHist
        p_data['p_LifeStyle'] = p_LifeStyle
        return json.dumps(p_data)

    @staticmethod
    def deleteAccount(patient_ID):
        if patient_ID == '' :
            return 'Patient ID is missing'
        cur = Db_connection.getConnection().cursor()
        cur.execute('delete from patient_static_info where patient_id = {0}'.format(patient_ID))
        Db_connection.commit();
        return "good bye"

    @staticmethod
    def updatePatientStatInfo(patientJSON):
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                return "patient_ID is missing"
        else:
            return "patient_ID is missing"   

        query = 'UPDATE patient_static_info SET ' + GlobalFunctions.buildUpdateQuery(patient_data) 
        query = query + "WHERE patient_id = '" + str(patient_data['patient_ID']) + "'"
        cur = Db_connection.getConnection().cursor()
        cur.execute(query)
        Db_connection.commit();
        return "Updated successfully"
    
