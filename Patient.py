import decimal
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
            cur.execute("select p.patient_id ,p.first_name ,p.last_name ,p.gender ,to_char(p.date_of_birth, 'MM/DD/YYYY'),p.phone ,p.email ,p.address ,p.dietitian_id ,p.status  from patient_static_info p where p.patient_id = %s",(p_ID,))
            patient = cur.fetchall()
            if cur.rowcount == 1 :
                print(patient)
                patientR = Patient(patient[0][0],patient[0][1],patient[0][2],patient[0][3],patient[0][4],patient[0][5],patient[0][6],patient[0][7],patient[0][8],patient[0][9])
                print("still nothing")
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
    

    @staticmethod
    def fetchPatientCalculations(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
           return GlobalFunctions.return_error_msg(err_msg)
        try:
            #Calculating BMR
            cur = Db_connection.getConnection().cursor()
            cur.execute("select p.patient_id ,p.gender ,to_char(p.date_of_birth, 'DD/MM/YYYY') as date_of_birth ,date_part('YEAR',age(current_date ,p.date_of_birth)) as AGE,a.weight , a.height , a.measurement_date from patient_static_info p , anthropometry a where p.patient_id = %s and a.patient_id = p.patient_id order by a.measurement_date desc",(p_ID,))
            patient = cur.fetchall()
            if cur.rowcount == 0 :
                cur.close();
                return GlobalFunctions.return_error_msg("The patient ID is incorrect")
            else :
                age = decimal.Decimal(patient[0][3])
                gender = str(patient[0][1])
                weight = decimal.Decimal(patient[0][4])
                heightcm = decimal.Decimal(patient[0][5])
                heightM = decimal.Decimal(heightcm/100)
                cur.close();

                #calculate BMI:
                BMI = weight / (heightM*heightM)

                if gender.upper() == "MALE":
                    #88.362 + (13.397 x weight in kg) + (4.799 x height in cm) – (5.677 x age in years)
                    BMR_WHO = decimal.Decimal(88.362)+(decimal.Decimal(13.397)*weight)+(decimal.Decimal(4.799)*heightcm)-(decimal.Decimal(5.677)*age)
                    print("BMR_WHO")
                    #66.473 + ( 13.7516 × weight in kg ) + ( 5.0033 × height in cm ) – ( 6.755 × age in years )
                    BMR_Harris_Benedict = decimal.Decimal(66.473) + (decimal.Decimal(13.7516)*weight) + (decimal.Decimal(5.0033)*heightcm)-(decimal.Decimal(6.755)*age)
                    print("BMR_Harris_Benedict")

                    #(10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
                    BMR_Mifflin_StJeor = (decimal.Decimal(10)*weight)+(decimal.Decimal(6.25)*heightcm)-(decimal.Decimal(5)*age)+decimal.Decimal(5)
                    print("BMR_Mifflin_StJeor")


                if gender.upper() == "FEMALE":
                    #447.593 + (9.247 x weight in kg) + (3.098 x height in cm) – (4.330 x age in years)
                    BMR_WHO = decimal.Decimal(447.593)+(decimal.Decimal(9.247)*weight)+(decimal.Decimal(3.098)*heightcm)-(decimal.Decimal(4.330)*age)
                    #655.0955 + ( 9.5634 × weight in kg ) + ( 1.8496 × height in cm ) – ( 4.6756 × age in years )
                    BMR_Harris_Benedict = decimal.Decimal(655.0955) + (decimal.Decimal(9.5634)*weight) + (decimal.Decimal(1.8496)*heightcm)-(decimal.Decimal(4.6756)*age)
                    #(10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) -161
                    BMR_Mifflin_StJeor = (10*weight)+(decimal.Decimal(6.25)*heightcm)-(decimal.Decimal(5)*age)-decimal.Decimal(161)
                print("___________________")

                #Calculating TDEE
            cur1 = Db_connection.getConnection().cursor()
            cur1.execute("select p.patient_id , l.physical_activity from patient_static_info p , life_style l where p.patient_id = l.patient_id and p.patient_id = %s order by l.measurement_date desc",(p_ID,))
            patient1 = cur1.fetchall()
            if cur1.rowcount == 0 :
                cur1.close();
                return GlobalFunctions.return_error_msg("The patient ID is incorrect")
            else :
                physical_activity = str(patient1[0][1])
                TDEE_factor = 0
                if physical_activity.upper() == "SEDENTARY": TDEE_factor = 1.2
                if physical_activity.upper() == "LIGHTLY ACTIVE": TDEE_factor = 1.375
                if physical_activity.upper() == "MODERATELY ACTIVE": TDEE_factor = 1.55
                if physical_activity.upper() == "VERY ACTIVE": TDEE_factor = 1.725
                if physical_activity.upper() == "SUPER ACTIVE": TDEE_factor = 1.9

                TDEE = decimal.Decimal(BMR_Mifflin_StJeor) * decimal.Decimal(TDEE_factor)

            #PREPARING THE RETURN
            to_ret = {
                "patient_ID" : str(p_ID),
                "BMI" : str(round(BMI,2)),
                "BMR_WHO" : str(round(BMR_WHO,2)),
                "BMR_Mifflin_StJeor" : str(round(BMR_Mifflin_StJeor,2)),
                "BMR_Harris_Benedict" : str(round(BMR_Harris_Benedict,2)),
                "TDEE" : str(round(TDEE,2))
            }
            return GlobalFunctions.return_success_msg(json.dumps(to_ret))
                
        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))
        

    @staticmethod
    def fetchPatientLogs(p_ID):
        err_msg = None
        if p_ID == '' or p_ID == None or not p_ID.isnumeric():
            err_msg = 'Please insert a valid patient ID'
        #response if error
        if err_msg != None:
           return GlobalFunctions.return_error_msg(err_msg)
        try:
            #Calculating BMR
            cur = Db_connection.getConnection().cursor()
            cur.execute("select coalesce(a.patient_id,bc.patient_id ) ,coalesce (a.measurement_date,bc.measurement_date) as  measurement_date, a.weight, a.waist_circumference  , bc.body_fat_percentage ,bc.fat_mass ,bc.muscle_mass ,bc.muscle_mass_percentage from anthropometry a full outer join body_composition bc on a.patient_id = bc.patient_id and a.measurement_date = bc.measurement_date where  a.patient_id =%s or bc.patient_id = %s ORDER BY measurement_date DESC",(p_ID,p_ID,))
            patientLogs = cur.fetchall()
            if cur.rowcount == 0 :
                cur.close();
                return GlobalFunctions.return_error_msg("The patient ID is incorrect")
            else :
                jsonLogs = [];
                for log in patientLogs:
                    to_ret_Log = {
                            "patient_ID" : str(log[0]),
                            "measurement_date" : str(log[1]),
                            "weight" : str(log[2]),
                            "waist_circumference" : str(log[3]),
                            "body_fat_percentage" : str(log[4]),
                            "fat_mass" : str(log[5]),
                            "muscle_mass" : str(log[6]),
                            "muscle_mass_percentage" : str(log[7]),
                        }
                    jsonLogs.append(json.dumps(to_ret_Log))

                return GlobalFunctions.cleanJSON(GlobalFunctions.return_success_msg(jsonLogs));

        except psycopg2.Error as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("DB error: " + str(e))
        except Exception as e:
            Db_connection.closeConnection(Db_connection.getConnection());
            return GlobalFunctions.return_error_msg("Server error: " + str(e))