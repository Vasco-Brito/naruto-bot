from mysql.connector import Error
from utils.db.connection import getconn, connectToDatabase
from xpSystem.constPlayer import xpPlayer


async def loadAll():
    if not getconn().is_connected():
        connectToDatabase()
    try:
        cursor = getconn().cursor()
        cursor.execute('Select * from discordUsers')
        return cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL ", e)

async def hasUserID(userID):
    if not getconn().is_connected():
        connectToDatabase()
    try:
        cursor = getconn().cursor()

        cursor.execute(f'SELECT * from discordUsers WHERE DiscordID = {userID}')
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False
    except Error as e:
        print("Error while connecting to MySQL ", e)

async def insertUser(userID):
    if not getconn().is_connected():
        connectToDatabase()
    try:
        cursor = getconn().cursor()

        cursor.execute(f'Insert into discordUsers(DiscordID, xp, nivel) Values({userID},0,1)')
        getconn().commit()
    except Error as e:
        print("Error while connecting to MySQL ", e)

async def getUserXP(userID):
    if not getconn().is_connected():
        connectToDatabase()
    try:
        cursor = getconn().cursor()

        cursor.execute(f'SELECT xp, nivel, ranking FROM discordUsers WHERE DiscordID = {userID}')
        result = cursor.fetchall()[0]

        obj = xpPlayer(xp=result[0], nivel=result[1], ranking=result[2])
        return obj
    except Error as e:
        print("Error while connecting to MySQL ", e)

def updateDb(lista):
    if not getconn().is_connected():
        connectToDatabase()
    try:
        cursor = getconn().cursor()

        for id in lista:
            xp = lista[id].getXp()
            ranking = lista[id].getRanking()
            nivel = lista[id].getNivel()
            cursor.execute(
                f'UPDATE discordUsers SET xp = {xp}, nivel = {nivel}, ranking = {ranking} WHERE DiscordID = {id} AND manualModify = FALSE')

        cursor.execute(f'UPDATE discordUsers SET manualModify = FALSE WHERE manualModify = TRUE')
        getconn().commit()
    except Error as e:
        print("Error while connecting to MySQL ", e)

