from database.DB_connect import DBConnect
from model.state import State


class DAO():

    @staticmethod
    def getAllYears():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor( dictionary=True )
        ris=[]

        query=""" select distinct year(s.`datetime`) as anno
                 from sighting s 
                 order by anno desc """

        cursor.execute(query)
        for row in cursor:
            ris.append(row["anno"])

        cursor.close()
        cnx.close()
        return ris

    # ------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllShapes():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """ select distinct s.shape
                    from sighting s  """

        cursor.execute(query)
        for row in cursor:
            ris.append(row["shape"])

        cursor.close()
        cnx.close()
        return ris

    # ------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllNodes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """ select *
                    from state s  """

        cursor.execute(query)
        for row in cursor:
            ris.append( State(**row))

        cursor.close()
        cnx.close()
        return ris

    # ------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdgesWeightMio(anno, shape):
        #SECONDO ME E' GIUSTO
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """ select n.state1 , n.state2 , count(*) as peso
                    from sighting s1, sighting s2, neighbor n 
                    where s1.state = n.state1
                    and s2.state = n.state2
                    and s1.state < s2.state
                    and s1.shape = %s
                    and s2.shape = %s
                    and year(s1.`datetime`) = %s
                    and year(s2.`datetime`) = %s
                    group by n.state1, n.state2  """

        cursor.execute(query, (shape, shape, anno, anno))
        for row in cursor:
            ris.append( (row["state1"],
                        row["state2"],
                        row["peso"] )   )

        cursor.close()
        cnx.close()
        return ris

    # ------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdgesWeightProf( anno, shape):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """ SELECT n.state1, n.state2 , count(*) as peso
                    FROM sighting s , neighbor n 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    and (s.state = n.state1 or s.state = n.state2 )
                    and n.state1 < n.state2
                    group by n.state1 , n.state2 """


        cursor.execute(query, ( anno, shape ))
        for row in cursor:
            ris.append( ( row["state1"],
                          row["state2"],
                          row["peso"] ))

        cursor.close()
        cnx.close()
        return ris

    # ------------------------------------------------------------------------------------------------------------------------------------------
