from datetime import date
import psycopg2
import json
from Db_connection import Db_connection
from GlobalFunctions import GlobalFunctions


class Appointment:

    def __init__(self, dietitian_ID, date_start, date_finish, status, patient_ID, notes):
        self.dietitian_ID=dietitian_ID
        self.date_start=date_start
        self.date_finish=date_finish
        self.status=status
        self.patient_ID=patient_ID 
        self.notes=notes
    
    def appointment_json(self):
        self.date_start = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.date_start)
        self.date_finish = GlobalFunctions.convert_date_to_FE_mm_dd_yyyy(self.date_finish)
        return json.dumps(vars(self),default=str);

    @staticmethod
    def fetchDietitianMonthAppointment(dietitian_ID):
        cur = Db_connection.getConnection().cursor()
        cur.execute("SELECT patient_id, to_char(measurement_date, 'MM/DD/YYYY'), weight, height, waist_circumference, hip_circumference, abdominal_skinfold, chest_skinfold, front_thigh_skinfold, midaxillary_skinfold, subscapular_skinfold, suprailiac_skinfold, triceps_skinfold FROM anthropometry where patient_id = %s ORDER BY measurement_date desc",(p_ID,))
        patientAnths = cur.fetchall()
        cur.close
        return patientAnths