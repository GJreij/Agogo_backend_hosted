import psycopg2
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
        self.date_of_birth = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.date_of_birth)
        return json.dumps(vars(self));

    def printPatient(self):
        print('patient ID: ',self.patient_id, ' - patient full name: ', self.first_name, ' ', self.last_name)


# STATIC METHODS TO BE USED
    @staticmethod
    def fetchPatient(p_email,p_pwd):
        err_msg = None
        if p_email == '' or p_email == None:
            err_msg = 'Email is missing'
        if p_pwd == '' or p_pwd == None:
            err_msg = 'Password is missing'
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
        
        try:
            cur = Db_connection.getConnection().cursor()
            if p_email == '' or p_pwd == '':
                return GlobalFunctions.return_error_msg("Please enter an Email and Password")
                
            cur.execute("select p.patient_id ,p.first_name ,p.last_name ,p.gender ,to_char(p.date_of_birth, 'MM/DD/YYYY'),p.phone ,p.email ,p.address ,p.dietitian_id ,p.status  from patient_static_info p where p.email = %s and p.pwd = %s",(p_email,p_pwd))
            patient = cur.fetchall()
            if cur.rowcount == 1 :
                print(cur.rowcount)
                patientR = Patient(patient[0][0],patient[0][1],patient[0][2],patient[0][3],patient[0][4],patient[0][5],patient[0][6],patient[0][7],patient[0][8],patient[0][9])
                cur.close;
                return patientR.Patient_json();
            else :
                cur.close;
                return GlobalFunctions.return_error_msg("The email or password is incorrect")

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))


    @staticmethod
    def fetchPatientStaticInfo(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
           return GlobalFunctions.return_error_msg(err_msg)
        try:
            cur = Db_connection.getConnection().cursor()
            cur.execute("select p.patient_id ,p.first_name ,p.last_name ,p.gender ,to_char(p.date_of_birth, 'MM/DD/YYYY'),p.phone ,p.email ,p.address ,p.dietitian_id ,p.status  from patient_static_info p where p.patient_id = %s",(p_ID))
            patient = cur.fetchall()
            if cur.rowcount == 1 :
                patientR = Patient(patient[0][0],patient[0][1],patient[0][2],patient[0][3],patient[0][4],patient[0][5],patient[0][6],patient[0][7],patient[0][8],patient[0][9])
                cur.close;
                return patientR.Patient_json();
            else :
                cur.close;
                return GlobalFunctions.return_error_msg("The patient ID is incorrect")
                
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    @staticmethod
    def fetchPatientAllInfo(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'

        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
        try:
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
            to_ret = json.dumps(p_data)
            return GlobalFunctions.cleanJSON(to_ret)
                
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))


    @staticmethod
    def deleteAccount(patient_ID):
        err_msg = None
        if patient_ID == '' or patient_ID == None or not patient_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
                #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)

        try:
            cur = Db_connection.getConnection().cursor()
            cur.execute('delete from patient_static_info where patient_id = {0}'.format(patient_ID))
            Db_connection.commit();
            response = {
                        "status": "success",
                        "message": "Patient deleted successfully"
                    }            
            return json.dumps(response) 
        
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))

    @staticmethod
    def updatePatientStatInfo(patientJSON):
        err_msg = None
        patient_data = json.loads(patientJSON)
        if 'patient_ID' in patient_data:
            if patient_data['patient_ID'] == '':
                err_msg = "patient_ID is missing"
        else:
            err_msg = "patient_ID is missing"   
        #response if error
        if err_msg != None:
            return GlobalFunctions.return_error_msg(err_msg)
            
        try:
            query = 'UPDATE patient_static_info SET ' + GlobalFunctions.buildUpdateQuery(patient_data) 
            query = query + "WHERE patient_id = '" + str(patient_data['patient_ID']) + "'"
            cur = Db_connection.getConnection().cursor()
            cur.execute(query)
            Db_connection.commit();
            response = {
                        "status": "success",
                        "message": "Patient updated successfully"
                    }            
            return json.dumps(response)
            
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
    
