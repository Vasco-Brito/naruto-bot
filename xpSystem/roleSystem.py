import discord

class roleSystem:

    def __init__(self, id, roleName, nivel, role='', regras=''):
        self.id = id
        self.roleName = roleName
        self.nivel = nivel
        self.role = role
        self.regras = regras

    def setId(self, id):
        self.id = id
    def getId(self):
        return self.id

    def setRoleName(self, roleName):
        self.roleName = roleName
    def getRoleName(self):
        return self.roleName

    def setNivel(self, id):
        self.id = id
    def getNivel(self):
        return self.nivel

    def setRole(self, role: discord.Role):
        self.role = role
    def getRole(self):
        return self.role

    def getRegras(self):
        return self.regras