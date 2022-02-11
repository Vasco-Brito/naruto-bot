import mysql.connector
from mysql.connector import Error

dbConnect = ''

async def connectToDatabase():
    try:
        conn = mysql.connector.connect(host='database-1.cyk0yprojvvx.us-east-2.rds.amazonaws.com',
                                             database='narutodb',
                                             user='admin',
                                             password='12345678')

        setconn(conn)
    except Error as e:
       print("Error while connecting to MySQL ", e)


def setconn(connection):
    global dbConnect
    dbConnect = connection

def getconn():
    global dbConnect
    return dbConnect