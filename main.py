import datetime
import random
import threading
import discord

from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
from utils.db.connection import connectToDatabase
from utils.db.xp import hasUserID, insertUser, getUserXP, updateDb
from utils.db.role import newRole, loadAllRoles
from xpSystem.constPlayer import xpPlayer
from xpSystem.roleSystem import roleSystem

bot = commands.Bot(command_prefix='$')
token = 'OTQxNzAwMTgyNjI4NzczOTU5.YgZwow.JGJTJgZ5apiLGKRZzp7qlLiPUJ8'
xpUsers = { }
roleMap = { }
f_stop = threading.Event()
timerRunning = True;

async def reloadData():
    global timerRunning
    timerRunning = False
    updateDb(xpUsers)
    xpUsers.clear()
    roleMap.clear()

    for g in bot.guilds:
        if g.id == 937034395209039872: ##Meu discord
            for x in await loadAllRoles():
                print(x)
                role = get(g.roles, id=x[0])
                roleMap[role.id] = roleSystem(id=role.id, roleName=role.name, nivel=x[2], role=role, regras=x[3])
        elif g.id == 941012595006124063: ##Discord de Naruto
            for x in await loadAllRoles():
                role = get(g.roles, id=x[0])
                roleMap[role.id] = roleSystem(id=role.id, roleName=role.name, nivel=x[2], role=role, regras=x[3])
    timerRunning = True

def xpSaveTimer(f_stop):
    if not f_stop.is_set():
        if timerRunning:
            print(f'{datetime.datetime.now()} - A atualizar um total de {xpUsers.__len__()} utilizadores')
            updateDb(xpUsers)
        threading.Timer(60, xpSaveTimer, [f_stop]).start()
    if timerRunning:
        xpUsers.clear()

@bot.event
async def on_ready():
    await connectToDatabase()
    xpSaveTimer(f_stop)
    for g in bot.guilds:
        if g.id == 937034395209039872: ##Meu discord
            for x in await loadAllRoles():
                role = get(g.roles, id=x[0])
                roleMap[role.id] = roleSystem(id=role.id, roleName=role.name, nivel=x[2], role=role, regras=x[3])
        elif g.id == 941012595006124063: ##Discord de Naruto
            for x in await loadAllRoles():
                role = get(g.roles, id=x[0])
                roleMap[role.id] = roleSystem(id=role.id, roleName=role.name, nivel=x[2], role=role, regras=x[3])
    print("O bot esta a correr...")


@bot.event
async def on_message(message):
    messageContent = message.content
    #if messageContent.startswith(bot.command_prefix):
    if message.author.bot:
        return
    authorId = message.author.id
    if not await hasUserID(authorId):
        await insertUser(authorId)
    elif xpUsers.__contains__(authorId):
        await xpUsers[authorId].increaseXp(random.randint(1, 10), message.author, roleMap, bot)
    else:
        xpUsers[authorId] = await getUserXP(authorId)
        await xpUsers[authorId].increaseXp(random.randint(1, 10), message.author, roleMap, bot)
    await bot.process_commands(message)


@bot.command(name="nivel")
async def nivel(ctx):
    id = ctx.author.id
    if xpUsers.__contains__(id):
        await ctx.send(f'{ctx.author.mention} está no nivel {xpUsers[id].getNivel()}')
    else:
        xpUsers[id] = await getUserXP(id)
        await ctx.send(f'{ctx.author.mention} está no nivel {xpUsers[id].getNivel()}')

@bot.command(name="setCargo")
@has_permissions(administrator=True)
async def setarNivelCargo(ctx, role: discord.Role, nivel):
    id = ctx.author.id
    if not xpUsers.__contains__(id):
        xpUsers[id] = await getUserXP(id)

    roleMap[nivel] = roleSystem(id=role.id, roleName=role.name, nivel=nivel, role=role)
    await newRole(role, nivel)
    await ctx.send(f'{ctx.author.mention} >> Role foi criada.')

@bot.command(name="reloadDb")
async def recarregarDB(ctx):
    if ctx.author.id == 199582033809244161:
        await reloadData()
        await ctx.send(f'{ctx.author.mention} a base de dados foi recarregada')
    else:
        print("Sem permissão")

bot.run(token)

