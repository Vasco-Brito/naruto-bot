import math
import json

class xpPlayer:

    def __init__(self, xp, nivel, ranking):
        self.xp = xp
        self.level = nivel
        self.ranking = ranking



    def setNivel(self, nivel):
        self.level = nivel
    def getNivel(self):
        return self.level

    def setXp(self, xp):
        self.xp = xp
    def getXp(self):
        return self.xp
    async def increaseXp(self, xp, user, roleMap, bot):
        #for x in user.roles:
        #    if x.name != '@everyone':
        #        roleId = int(x.id)
        #        if roleMap.__contains__(roleId):
        #            if json.loads(roleMap[roleId].getRegras())['ganho'] == 'False':
        #                return
        xpNextLevel = self.nextLevelXP(self.getNivel())
        xpNextLevel = xpNextLevel * 2
        if self.xp+xp >= xpNextLevel:
            self.level += 1
            self.xp = self.xp + xp - xpNextLevel
            for x in roleMap:
                if self.level == roleMap[x].nivel:
                    await user.add_roles(roleMap[x].role)
        else:
            self.xp += xp

    def setRanking(self, ranking):
        self.ranking = ranking
    def getRanking(self):
        return self.ranking

    def nextLevelXP(self, nivel):
        nextLevel = nivel+1
        formula = 1.6888 * (math.pow(nextLevel, 3)) + 20.9300 * (math.pow(nextLevel, 2)) + 99.3738 * nextLevel - 55.6714
        return formula