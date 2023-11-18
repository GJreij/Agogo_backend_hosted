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

