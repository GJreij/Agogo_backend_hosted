import datetime
import json


class GlobalFunctions:

    @staticmethod
    def buildUpdateQuery(patient_data):
        query = ''
        comma = 'no'
        for i in patient_data:
            if patient_data[i] != '':
                if comma =='no':
                    query = query + i +"= '"+ str(patient_data[i]) + "' "
                    comma = 'yes'
                else:
                    query = query + ", "+i+"= '"+ str(patient_data[i]) + "' "
        return query
    
    @staticmethod
    def buildInsertQuery(patient_data):
        query1 = '('
        query2 = '('
        comma1 = 'no'
        comma2 = 'no'
        for i in patient_data:
            if patient_data[i] != '':
                if comma1 =='no':
                    query1 = query1 + i
                    comma1 = 'yes'
                else:
                    query1 = query1 + ", "+i
        query1 = query1 + ") "

        for i in patient_data:
            if patient_data[i] != '':
                if comma2 =='no':
                    query2 = query2 +"'"+ str(patient_data[i]) + "' "
                    comma2 = 'yes'
                else:
                    query2 = query2 +",'"+ str(patient_data[i]) + "' "
        query2 = query2 + ") "     
        
        query = query1 + " VALUES " + query2
        return query


    @staticmethod
    def cleanJSON(json_obj):
        json_obj = json.dumps(json_obj)
        json_obj = json_obj.replace(r'"{\\', '{').replace('\\', '').replace('}"','}').replace('"{', '{')
        return json_obj
    
    @staticmethod
    def convert_date_to_yyyy_mm_dd(date_str):
        # Define possible date formats
        date_formats = [
            "%d-%m-%Y",  # DD-MM-YYYY
            "%m/%d/%Y",  # MM/DD/YYYY
            "%Y/%m/%d",  # YYYY/MM/DD
            "%b %d, %Y", # Nov 18, 2023 (Month abbreviation, day, year)
            # ... add other formats as needed
        ]

        for format in date_formats:
            try:
                # Try to parse the date using the current format
                parsed_date = datetime.strptime(date_str, format)
                # If parsing is successful, return the date in YYYY-MM-DD format
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                # If parsing fails, try the next format
                continue
            
        # If none of the formats match, return an error message or handle as needed
        return "Invalid date format"