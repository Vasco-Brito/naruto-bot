import discord
from mysql.connector import Error
from utils.db.connection import getconn, connectToDatabase
from xpSystem.constPlayer import xpPlayer

async def loadAllRoles():
    if not getconn().is_connected():
        connectToDatabase()
    try:
        cursor = getconn().cursor()

        cursor.execute(f'Select * from levelRanks')
        return cursor.fetchall()


    except Error as e:
        print("Error while connecting to MySQL ", e)

async def newRole(role: discord.Role, level):
    if not getconn().is_connected():
        connectToDatabase()
    try:
        cursor = getconn().cursor()

        cursor.execute(f'Insert into levelRanks (id, rankName, nivel) Values ({role.id}, "{role.name}", {level})')
        getconn().commit()
    except Error as e:
        print("Error while connecting to MySQL ", e)