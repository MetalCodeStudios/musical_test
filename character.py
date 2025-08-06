import screenWindow
from screenWindow import playSound
#import threading
# Import essential things
import random
import json
# Import essential things
import random
import json
import os
import sys
import math
import copy
WHITE = (255, 255, 255)
effectList = []
opponentOriginalHp = {}
totalDamage = {}
opponentDamage = []
opponentFrame = {}
theAggresor = {}
effectText = []

effectStuff = {}
freeRange = False
inf = float('inf')
energyLoop = []
dialogueText = []
effectText = []

itemObj = {}
skillObj = {}
actObj = {}
fightObj = {}

playerObj = {}
opponentObj = {}
itemList = []
class Item:
    def __init__(self, name, type, num, info, usePercent=False, targetType='Single', repeatHowMany=1, targetAmount=1, stackDuration=False, stackAmplifier=False, applyEffect=None, removeEffect=None, numCap=30, color=WHITE):

        if applyEffect is None:
            applyEffect = {}
        if removeEffect is None:
            removeEffect = {}

        self.name = name
        self.type = type  # 'Weapon', 'Armour', 'Item', plus stat types like 'atk'
        self.num = num
        self.info = info

        self.usePercent = usePercent
        self.targetType = targetType
        self.useAnim = False
        self.animType = None
        self.repeatHowMany = repeatHowMany
        self.targetAmount = targetAmount
        self.stackDuration = stackDuration
        self.stackAmplifier = stackAmplifier
        self.applyEffect = applyEffect
        self.removeEffect = removeEffect
        self.numCap = numCap
        self.color = color
        if 'Weapon' in self.type or 'Armour' in self.type:
            self.targetAmount = 1
            self.targetType = 'Single' if self.targetType != 'Self' else 'Self'
            for i in applyEffect:
                applyEffect[i][0] = inf

        itemObj[self.name] = self
        itemList.append(self)

    def customUse(self, target, giver):
        pass

    def use(self, target, giver, doRemove=True, extra2=None):
        giver.activity = 'Item_done'
        if target != giver:
            target.activity = 'Item_on'

        if 'Weapon' in self.type:
            if target.weapon.name != 'None':
                target.inventory.append(target.weapon)
            for eff in target.weapon.applyEffect:
                eff.remove(target)
            target.weapon = self
            #if doRemove:
            giver.inventory.remove(self)
            for stat in target.addBase:
                for name in target.addBase[stat]:
                    if name != self.name:
                        continue
                    target.addBase[stat][name] = 0

            target.levelUp(0)


        elif 'Armour' in self.type:
            if target.weapon.name != 'None':
                target.inventory.append(target.armour)
            for eff in target.weapon.applyEffect:
                eff.remove(target)
            target.armour = self

            giver.inventory.remove(self)
            for stat in target.addBase:
                for name in target.addBase[stat]:
                    if name != self.name:
                        continue
                    target.addBase[stat][name] = 0
            #target.levelUp(0)
        else:
            giver.inventory.remove(self)

        self.customUse(target, giver)

        # === Effects ===
        if self.applyEffect:
            for eff in self.applyEffect:
                turn = self.applyEffect[eff][0]
                amp = self.applyEffect[eff][1]
                eff.apply(giver, target, turn, amp, self.stackDuration, self.stackAmplifier)

        if self.removeEffect:
            for eff in self.removeEffect:
                eff.remove(target)

        # === Stat Mods ===
        if 'opponent' in self.type:
            multiply = -1
        else:
            multiply = 1

        if 'missingHp' in self.type:
                number = 0
                if target.hp <= 0 and 'canRevive' not in self.type:
                    pass
                elif self.useAnim == True:
                    pass
                elif self.usePercent:
                    number = (target.maxhp - target.hp) * (self.baseNum / 100) * multiply * -1
                else:
                    number = self.num * multiply * -1

                if int(number) != 0:
                    fightyLoop.append([target, target, int(number)])

        elif 'hp' in self.type:
                number = 0
                if target.hp <= 0 and 'canRevive' not in self.type:
                    pass
                elif self.useAnim == True:
                    pass
                elif self.usePercent:
                    number = target.maxhp * (self.baseNum / 100) * multiply * -1
                else:
                    number = self.num * multiply * -1
                if int(number) != 0:
                    fightyLoop.append([target, target, int(number)])

        if 'maxhp' in self.type:
            if self.name in target.addBase['hp']:
                if self.usePercent:
                    target.addBase['hp'][self.name] += target.setNum[0] * self.num / 100 * multiply
                else:
                    target.addBase['hp'][self.name] += self.num * multiply

                if target.addBase['hp'][self.name] >= self.numCap:
                    target.addBase['hp'][self.name] = self.numCap * multiply
            else:
                if self.usePercent:
                    target.addBase['hp'][self.name] = target.setNum[0] * self.num / 100 * multiply
                else:
                    target.addBase['hp'][self.name] = self.num * multiply

                if target.addBase['hp'][self.name] >= self.numCap:
                    target.addBase['hp'][self.name] = self.numCap * multiply

        if 'atk' in self.type:
            if self.name in target.addBase['attack']:
                if self.usePercent:
                    target.addBase['attack'][self.name] += target.setNum[1] * self.num / 100 * multiply
                else:
                    target.addBase['attack'][self.name] += self.num * multiply

                if target.addBase['attack'][self.name] >= self.numCap:
                    target.addBase['attack'][self.name] = self.numCap * multiply
            else:
                if self.usePercent:
                    target.addBase['attack'][self.name] = target.setNum[1] * self.num / 100 * multiply
                else:
                    target.addBase['attack'][self.name] = self.num * multiply

                if target.addBase['attack'][self.name] >= self.numCap:
                    target.addBase['attack'][self.name] = self.numCap * multiply

        if 'def' in self.type:
            if self.name in target.addBase['defense']:
                if self.usePercent:
                    target.addBase['defense'][self.name] += target.setNum[2] * self.num / 100 * multiply
                else:
                    target.addBase['defense'][self.name] += self.num * multiply

                if target.addBase['defense'][self.name] >= self.numCap:
                    target.addBase['defense'][self.name] = self.numCap * multiply
            else:
                if self.usePercent:
                    target.addBase['defense'][self.name] = target.setNum[2] * self.num / 100 * multiply
                else:
                    target.addBase['defense'][self.name] = self.num * multiply

                if target.addBase['defense'][self.name] >= self.numCap:
                    target.addBase['defense'][self.name] = self.numCap * multiply

        if 'spd' in self.type:
            if self.name in target.addBase['speed']:
                if self.usePercent:
                    target.addBase['speed'][self.name] += target.setNum[3] * self.num / 100 * multiply
                else:
                    target.addBase['speed'][self.name] += self.num * multiply

                if target.addBase['speed'][self.name] >= self.numCap:
                    target.addBase['speed'][self.name] = self.numCap * multiply
            else:
                if self.usePercent:
                    target.addBase['speed'][self.name] = target.setNum[3] * self.num / 100 * multiply
                else:
                    target.addBase['speed'][self.name] = self.num * multiply

                if target.addBase['speed'][self.name] >= self.numCap:
                    target.addBase['speed'][self.name] = self.numCap * multiply

        if 'rge' in self.type:
            if self.name in target.addBase['range']:
                if self.usePercent:
                    target.addBase['range'][self.name] += target.setNum[4] * self.num / 100 * multiply
                else:
                    target.addBase['range'][self.name] += self.num * multiply

                if target.addBase['range'][self.name] >= self.numCap:
                    target.addBase['range'][self.name] = self.numCap * multiply
            else:
                if self.usePercent:
                    target.addBase['range'][self.name] = target.setNum[4] * self.num / 100 * multiply
                else:
                    target.addBase['range'][self.name] = self.num * multiply

                if target.addBase['range'][self.name] >= self.numCap:
                    target.addBase['range'][self.name] = self.numCap * multiply

        if 'prod' in self.type:
            if self.name in target.addBase['productivity']:
                if self.usePercent:
                    target.addBase['productivity'][self.name] += target.setNum[5] * self.num / 100 * multiply
                else:
                    target.addBase['productivity'][self.name] += self.num * multiply

                if target.addBase['productivity'][self.name] >= self.numCap:
                    target.addBase['productivity'][self.name] = self.numCap * multiply
            else:
                if self.usePercent:
                    target.addBase['productivity'][self.name] = target.setNum[5] * self.num / 100 * multiply
                else:
                    target.addBase['productivity'][self.name] = self.num * multiply

                if target.addBase['productivity'][self.name] >= self.numCap:
                    target.addBase['productivity'][self.name] = self.numCap * multiply

        target.levelUp(0)


itemHealing = []
fightyLoop = []
noWeapon = Item('None', 'slashWeapon', 0, '-')
noArmour = Item('None', 'Armour', 0, '-')
hpPot = Item('Health Potion', 'Item: ally, hp', 100, 'A green glowing potion. Sure to recover your health and energise you!', targetType='Self')
hpElixer = Item('Health Elixer', 'Item: ally, hp', 300, 'More glowing than ever! Triple the potency, triple the health recovered!', targetType='Self')
soulCube = Item('Life Cube', 'Item: ally, canRevive, hp', 1000, 'Revive a fallen teammate.', targetType='Dead')
placeHolder_inventory = [hpPot]

class Opponent:
    def __init__(self, name, classes, tempClass, base, setNum=None, newNum=None, addBase=None, hp=20, maxhp=20, attack=20, defense=20, speed=20, mana=0, maxMana=100,
                 damage=1, range=1, productivity=0, accuracy=100, spare=0, weapon=noWeapon, armour=noArmour, level=1, xp=0, fight=[], inventory=None, action=[], skills=[], canFly=False,
                 flyRange=20, flyType=0, scale=1, status='Neutral', info='Checked', buff=None, passiveBuff=None, barColor=(255, 255, 255), color=(255, 255, 255), skinList=['Default'], skin='Default',
                 offsetX=0, offsetY=0, beSelectOnce=True):

        if buff is None:
            buff = {}
        if passiveBuff is None:
            passiveBuff = {}
        if addBase is None:
            addBase = {'attack':{}, 'defense':{}, 'speed':{}, 'hp':{}, 'range':{}, 'maxhp':{}, 'productivity':{}, 'damage':{}, 'accuracy':{}}
        if setNum is None:
            setNum = []
        if newNum is None:
            newNum = copy.copy(setNum)
        if inventory is None:
            inventory = placeHolder_inventory
        self.setNum = setNum
        self.newNum = newNum
        self.defaultNum = copy.copy(setNum)
        self.tracker = {"Hurt":0, "Died":0, "Attacked":0, "currentDamage": 0}
        self.name = name
        self.dataName = name
        self.displayName = name
        self.classes = classes
        self.tempClass = tempClass
        self.base = base
        self.addBase = addBase
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range = range
        self.productivity = productivity
        self.mana = mana
        self.maxMana = maxMana
        self.damage = damage
        self.accuracy = accuracy
        self.spare = spare
        self.weapon = weapon
        self.armour = armour
        self.level = level
        self.xp = xp
        self.fight = fight
        self.inventory = inventory
        self.action = action
        self.skills = skills
        self.hp = hp
        self.maxhp = maxhp
        self.status = status
        self.barColor = barColor
        self.color = color
        self.info = info
        self.buff = buff
        self.passiveBuff = passiveBuff
        self.skin = skin
        self.skinList = skinList
        self.flyRange = flyRange
        self.canFly = canFly
        self.flyType = flyType
        self.sprite = None
        self.activity = 'Idle'
        self.usingWhat = None
        self.targets = []
        self.forceAction = False
        self.oriSkin = None
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.scale = scale
        self.beSelectOnce = beSelectOnce

        opponentObj[self.name] = self

    def doAction(self, type, useWhat, target):
        self.activity = type
        self.forceAction = True
        self.usingWhat = useWhat
        self.targets = target

    def updateTurn(self):
        if self.displayName == "Blueberry":
            effect = None
            for i in self.buff:
                if i.name == "Force":
                    effect = i
                    break
            if effect == None and "God Mode" in self.skin:
                self.skin = self.skin.replace(" God Mode", "")
                confusion.apply(self, self, 3, 2)
                self.canFly = False
                self.addBase["damage"]["GOD MODE"] = 1

    def attacked(self, damage):
        self.hp -= damage

    def levelUp(self, xpGain, add=True):
        requirement = 0
        #for level in range(1, self.level + 1):
            #requirement += level * (level + 19)
        requirement += self.level * (self.level + 19)
        deLevel = (abs(self.level) - 1) * ((abs(self.level) - 1) + 19)
        self.xp += xpGain
        while self.xp >= requirement:
            self.level += 1
            requirement = self.level * (self.level + 19)

        #while self.xp < deLevel:
         #   self.level -= 1
          #  deLevel = (abs(self.level) - 1) * ((abs(self.level) - 1) + 19)

        # Hey Look, stats change from level below this comment! Don't change it.
        # Hey Look, stats change from level below this comment! Don't change it.
        #self.weapon.use(self, self)
        #self.armour.use(self, self)
        self.attack = 25 + 5*self.base[1] + (2 + 1*self.base[1])*(self.level - 1) + self.weapon.num if self.base[1] != inf else inf

        self.defense = 15 + 10*self.base[2] + (2 + 1*self.base[2])*(self.level - 1) + self.armour.num if self.base[2] != inf else inf

        self.speed = 20 + 5*self.base[3] + (3 + 1*self.base[3])*(self.level - 1) if self.base[3] != inf else inf

        self.maxhp = 50 + 10*self.base[0] + (3 + 1*self.base[0])*(self.level - 1) if self.base[0] != inf else inf

        self.range = self.base[4]

        self.productivity = 0.4*self.base[5]

        self.damage = 1

        self.accuracy = 1

        if self.setNum != []:
            self.attack = self.setNum[1] + (2 + 1*self.base[1])*(self.level - 1) + self.weapon.num if self.base[1] != inf else inf

            self.defense = self.setNum[2] + (2 + 1*self.base[2])*(self.level - 1) + self.armour.num if self.base[2] != inf else inf

            self.speed = self.setNum[3] + (3 + 1*self.base[3])*(self.level - 1) if self.base[3] != inf else inf

            self.maxhp = self.setNum[0] + (3 + 1*self.base[0])*(self.level - 1) if self.base[0] != inf else inf

            self.range = self.setNum[4]

            self.productivity = self.setNum[5]

        if self.newNum != self.setNum:
            self.attack = self.newNum[1] + (2 + 1*self.base[1])*(self.level - 1) + self.weapon.num if self.base[1] != inf else inf

            self.defense = self.newNum[2] + (2 + 1*self.base[2])*(self.level - 1) + self.armour.num if self.base[2] != inf else inf

            self.speed = self.newNum[3] + (3 + 1*self.base[3])*(self.level - 1) if self.base[3] != inf else inf

            self.maxhp = self.newNum[0] + (3 + 1*self.base[0])*(self.level - 1) if self.base[0] != inf else inf

            self.range = self.newNum[4]

            self.productivity = self.newNum[5]


        if add:
            for i in self.addBase['attack'].values():
                self.attack += i

            for i in self.addBase['defense'].values():
                self.defense += i

            for i in self.addBase['speed'].values():
                self.speed += i

            for i in self.addBase['hp'].values():
                self.maxhp += i

            for i in self.addBase['range'].values():
                self.range += i

            for i in self.addBase['productivity'].values():
                self.productivity += i

            for i in self.addBase['damage'].values():
                self.damage *= i

            for i in self.addBase['accuracy'].values():
                self.accuracy += i

        self.attack = int(self.attack) if self.attack != inf else inf
        self.defense = int(self.defense) if self.defense != inf else inf
        self.speed = int(self.speed) if self.speed != inf else inf
        self.maxhp = int(self.maxhp) if self.maxhp != inf else inf
        self.range = int(self.range) if self.range != inf else inf
        self.productivity = int(self.productivity*100)/100 if self.productivity != inf else inf


        for i in self.skills:
            if 'magic' in self.weapon.name:
                i.num = i.baseNum + 2*((self.level - 1) + self.weapon.num * 2)
            else:
                i.num = abs(i.baseNum) + ((self.level - 1) + self.weapon.num) if i.baseNum != 0 else i.num
                if i.baseNum < 0:
                    i.num *= -1

    def hpSet(self):
        self.hp = self.maxhp

class Player:
    def __init__(self, name, classes, tempClass, base, setNum=None, newNum=None, addBase=None, hp=20, maxhp=20, attack=20, defense=20, speed=20, mana=0, maxMana=100,
                 damage=1, range=1, productivity=0, accuracy=100, spare=0, weapon=noWeapon, armour=noArmour, level=1, xp=0, fight=[], inventory=None, action=[], skills=[], canFly=False,
                 flyRange=20, flyType=0, scale=1, status='Neutral', info='Checked', buff=None, passiveBuff=None, barColor=(255, 255, 255), color=(255, 255, 255), skinList=['Default'], skin='Default',
                 offsetX=0, offsetY=0, beSelectOnce=True):

        if buff is None:
            buff = {}
        if passiveBuff is None:
            passiveBuff = {}
        if addBase is None:
            addBase = {'attack':{}, 'defense':{}, 'speed':{}, 'hp':{}, 'range':{}, 'maxhp':{}, 'productivity':{}, 'damage':{}, 'accuracy':{}}
        if setNum is None:
            setNum = []
        if newNum is None:
            newNum = copy.copy(setNum)
        if inventory is None:
            inventory = placeHolder_inventory
        self.setNum = setNum
        self.newNum = newNum
        self.defaultNum = copy.copy(setNum)
        self.tracker = {"Hurt":0, "Died":0, "Attacked":0, "currentDamage": 0}
        self.name = name
        self.dataName = name
        self.displayName = name
        self.classes = classes
        self.tempClass = tempClass
        self.base = base
        self.addBase = addBase
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range = range
        self.productivity = productivity
        self.mana = mana
        self.maxMana = maxMana
        self.damage = damage
        self.accuracy = accuracy
        self.spare = spare
        self.weapon = weapon
        self.armour = armour
        self.level = level
        self.xp = xp
        self.fight = fight
        self.inventory = inventory
        self.action = action
        self.skills = skills
        self.hp = hp
        self.maxhp = maxhp
        self.status = status
        self.barColor = barColor
        self.color = color
        self.info = info
        self.buff = buff
        self.passiveBuff = passiveBuff
        self.skin = skin
        self.skinList = skinList
        self.flyRange = flyRange
        self.canFly = canFly
        self.flyType = flyType
        self.sprite = None
        self.activity = 'Idle'
        self.usingWhat = None
        self.targets = []
        self.forceAction = False
        self.oriSkin = None
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.scale = scale
        self.beSelectOnce = beSelectOnce
        #self.damageTaken = 0

        playerObj[self.name] = self

    def doAction(self, type, useWhat, target):
        self.activity = type
        self.forceAction = True
        self.usingWhat = useWhat
        self.targets = target

    def attacked(self, damage):
        self.hp -= damage

    def updateTurn(self):
        if self.displayName == "Blueberry":
            effect = None
            for i in self.buff:
                if i.name == "Force":
                    effect = i
                    break
            if effect == None and "God Mode" in self.skin:
                self.skin = self.skin.replace(" God Mode", "")
                confusion.apply(self, self, 3, 3)
                self.canFly = False
                self.addBase["damage"]["GOD MODE"] = 1

    def levelUp(self, xpGain, add=True):
        requirement = 0
        #for level in range(1, self.level + 1):
            #requirement += level * (level + 19)
        requirement += self.level * (self.level + 19)
        deLevel = (abs(self.level) - 1) * ((abs(self.level) - 1) + 19)
        self.xp += xpGain
        while self.xp >= requirement:
            self.level += 1
            requirement = self.level * (self.level + 19)

        #while self.xp < deLevel:
         #   self.level -= 1
          #  deLevel = (abs(self.level) - 1) * ((abs(self.level) - 1) + 19)

        # Hey Look, stats change from level below this comment! Don't change it.
        # Hey Look, stats change from level below this comment! Don't change it.
        self.attack = 25 + 5*self.base[1] + (2 + 1*self.base[1])*(self.level - 1) + self.weapon.num if self.base[1] != inf else inf

        self.defense = 15 + 10*self.base[2] + (2 + 1*self.base[2])*(self.level - 1) + self.armour.num if self.base[2] != inf else inf

        self.speed = 20 + 5*self.base[3] + (3 + 1*self.base[3])*(self.level - 1) if self.base[3] != inf else inf

        self.maxhp = 50 + 10*self.base[0] + (3 + 1*self.base[0])*(self.level - 1) if self.base[0] != inf else inf

        self.range = self.base[4]

        self.productivity = 0.4*self.base[5]

        self.damage = 1

        self.accuracy = 1

        if self.setNum != []:
            self.attack = self.setNum[1] + (2 + 1*self.base[1])*(self.level - 1) + self.weapon.num if self.base[1] != inf else inf

            self.defense = self.setNum[2] + (2 + 1*self.base[2])*(self.level - 1) + self.armour.num if self.base[2] != inf else inf

            self.speed = self.setNum[3] + (3 + 1*self.base[3])*(self.level - 1) if self.base[3] != inf else inf

            self.maxhp = self.setNum[0] + (3 + 1*self.base[0])*(self.level - 1) if self.base[0] != inf else inf

            self.range = self.setNum[4]

            self.productivity = self.setNum[5]

        if self.newNum != self.setNum:
            self.attack = self.newNum[1] + (2 + 1*self.base[1])*(self.level - 1) + self.weapon.num if self.base[1] != inf else inf

            self.defense = self.newNum[2] + (2 + 1*self.base[2])*(self.level - 1) + self.armour.num if self.base[2] != inf else inf

            self.speed = self.newNum[3] + (3 + 1*self.base[3])*(self.level - 1) if self.base[3] != inf else inf

            self.maxhp = self.newNum[0] + (3 + 1*self.base[0])*(self.level - 1) if self.base[0] != inf else inf

            self.range = self.newNum[4]

            self.productivity = self.newNum[5]


        if add:
            for i in self.addBase['attack'].values():
                self.attack += i

            for i in self.addBase['defense'].values():
                self.defense += i

            for i in self.addBase['speed'].values():
                self.speed += i

            for i in self.addBase['hp'].values():
                self.maxhp += i

            for i in self.addBase['range'].values():
                self.range += i

            for i in self.addBase['productivity'].values():
                self.productivity += i

            for i in self.addBase['damage'].values():
                self.damage *= i

            for i in self.addBase['accuracy'].values():
                self.accuracy += i

        self.attack = int(self.attack) if self.attack != inf else inf
        self.defense = int(self.defense) if self.defense != inf else inf
        self.speed = int(self.speed) if self.speed != inf else inf
        self.maxhp = int(self.maxhp) if self.maxhp != inf else inf
        self.range = int(self.range) if self.range != inf else inf
        self.productivity = int(self.productivity*100)/100 if self.productivity != inf else inf


        for i in self.skills:
            if 'magic' in self.weapon.name:
                i.num = i.baseNum + 2*((self.level - 1) + self.weapon.num * 2)
            else:
                i.num = abs(i.baseNum) + ((self.level - 1) + self.weapon.num) if i.baseNum != 0 else i.num
                if i.baseNum < 0:
                    i.num *= -1

    def hpSet(self):
        self.hp = self.maxhp



        #return currentNum

class Skill:
    #def __init__(self, name, cost, type, info, baseNum, num, turn, multiNum, target, effects):
    def __init__(self, name, cost=10, info='Skill', type='ally:', baseNum=10, num=10, numCap=30, usePercent=False, cooldown='0T', targetType='Single',
                 repeatHowMany=1, targetAmount=1, useAnim=False, animType='Thrower', ignoreDefense=False, stackDuration=False, stackAmplifier=False,
                 applyEffect=None, removeEffect=None, maxAmplifier=None, maxDuration=None, changePhaseTo=None, useDialogue=None, color=WHITE, range=None, considerRange=False):
        if applyEffect == None:
            applyEffect = {}
        if removeEffect == None:
            removeEffect = {}
        self.name = name
        self.cost = cost
        self.info = info
        self.type = type
        self.baseNum = baseNum
        self.num = num
        self.numCap = numCap
        self.usePercent = usePercent
        self.cooldown = cooldown
        self.targetType = targetType #Self, Single, Multiple, All
        self.repeatHowMany = repeatHowMany
        self.targetAmount = targetAmount
        #Effects Below
        self.useAnim = useAnim
        self.animType = animType
        self.stackDuration = stackDuration
        self.stackAmplifier = stackAmplifier
        self.maxDuration = maxDuration
        self.maxAmplifier = maxAmplifier
        self.applyEffect = applyEffect
        self.removeEffect = removeEffect
        self.changePhaseTo = changePhaseTo
        self.useDialogue = useDialogue
        self.ignoreDefense = ignoreDefense
        self.color = color
        self.range = range
        self.considerRange = considerRange

        skillObj[self.name] = self

    def projectileStart(self, caster, target, damage, trueDamage, listThing, projSprite, bar):
        pass

    def projectileUse(self, caster, target, damage, trueDamage, listThing, projSprite, bar):
        target.tracker['currentDamage'] = trueDamage

    def customUse(self, caster, targeted):
        if caster.name == "Copycat":
            if self.name == 'Copy':
                if targeted.name != "Copycat":
                    caster.skills = copy.deepcopy(targeted.skills)
                    caster.skin = targeted.skin
                    caster.fight = copy.deepcopy(targeted.fight)
                    caster.classes = targeted.classes
                    caster.passiveBuff = copy.deepcopy(targeted.passiveBuff)
                    caster.dataName = targeted.name
                    caster.setNum = caster.newNum = copy.deepcopy(targeted.setNum)
                    caster.hp = round(targeted.maxhp * caster.hp/caster.maxhp)
                    caster.maxhp = targeted.maxhp
                    caster.skills.insert(0, copySkill)
                else:
                    caster.skills = [copySkill]
                    caster.skin = "Default"
                    caster.fight = [scratch]
                    caster.classes = "All rounder"
                    caster.passiveBuff = []#copy.deepcopy(targeted.passiveBuff)
                    caster.dataName = targeted.name
                    caster.setNum = caster.newNum = targeted.defaultNum
                    caster.hp = round(caster.defaultNum[0] * caster.hp/caster.maxhp)
                    caster.maxhp = 120#targeted.defaultNum[0]
                caster.levelUp(0)

        if caster.name == "Jam Jar":
            if self.name == "Lid On":
                caster.skills = [lid_off]#copy.deepcopy(targeted.skills)
                caster.fight = [doubleFistBash]
                caster.setNum = [148, 46, 31, 10, 1, 1]
                caster.base = [4, 4, 4, 1, 1, 1]
            elif self.name == "Lid Off":
                caster.skills = [lid_on]#copy.deepcopy(targeted.skills)
                caster.fight = [lidSlam]
                caster.setNum = [148, 34, 48, 2, 1, 1]
                caster.base = [4, 3, 5, 1, 1, 1]

        if caster.name == "Screamy":
            if self.name == "SCREAMER!":
                caster.skills.clear()

        if caster.name == "Blueberry":
            if self.name == "GOD MODE":
                #caster.skills.clear()
                screenWindow.hud.camera_color = (255, 0, 255)
                screenWindow.hud.camera_fade = 255
                caster.canFly=True
                caster.addBase['damage']['GOD MODE'] = 0



    def use(self, caster, targeted):
        self.customUse(caster, targeted)
        energyLoop.append([caster, caster, self.cost])
        caster.activity = 'Skill_done'# + self.name]
        if self.useDialogue != None:
            with open(f'data/dialogue/{caster.dataName}.txt', 'r') as file:
                code = file.read()
                diction = eval(code)
            if self.useDialogue in diction:
                text = random.choice(diction[self.useDialogue])
                dialogueText.append([text, caster, 0, False])

        if not isinstance(targeted, list):
            targeted = [targeted]
        for i in targeted:
            if isinstance(self.changePhaseTo, str):
                if i.oriSkin == None:
                    i.oriSkin = i.skin
                if self.changePhaseTo != 'Default':
                    i.skin = i.oriSkin + ' ' + self.changePhaseTo
                else:
                    i.skin = i.oriSkin
            if i != caster:
                i.activity = 'Skill_on'
        if self.applyEffect != None and not self.useAnim:
            for i in self.applyEffect:
                turn = self.applyEffect[i][0]
                amplifier = self.applyEffect[i][1]
                if len(self.applyEffect[i]) > 2:
                    otherTurn = self.applyEffect[i][2]
                else:
                    otherTurn = 0
                for target in targeted:
                    i.apply(caster, target, turn, amplifier, self.stackDuration, self.stackAmplifier, self.maxAmplifier, self.maxDuration, otherTurn)
        if self.removeEffect != None and not self.useAnim:
            for i in self.removeEffect:
                #turn = self.applyEffect[i][0]
                #amplifier = self.applyEffect[i][1]
                for target in targeted:
                    i.remove(target)

        if 'opponent' in self.type:
            multiply = -1
        else:
            multiply = 1

        if 'missingHp' in self.type:
             for target in targeted:
                if target.hp <= 0 and 'canRevive' not in self.type:
                    continue
                if self.useAnim == True:
                    continue
                global itemHealing
                if self.usePercent:
                    number = (target.maxhp - target.hp) * (self.baseNum / 100) * multiply * -1
                else:
                    number = self.num * multiply * -1
                #itemHealing.insert(0, [self, target, 0, int(number)])
                if int(number) != 0:
                    fightyLoop.append([target, caster, int(number)])

        elif 'hp' in self.type:
             for target in targeted:
                if target.hp <= 0 and 'canRevive' not in self.type:
                    continue
                if self.useAnim == True:
                    continue
                global itemHealing
                if self.usePercent:
                    number = target.maxhp * (self.baseNum / 100) * multiply * -1
                else:
                    number = self.num * multiply * -1
                #itemHealing.insert(0, [self, target, 0, int(number)])
                fightyLoop.append([target, caster, int(number)])

        for target in targeted:
            if 'maxhp' in self.type:
                if self.name in target.addBase['hp']:
                    #if self.target.addBase['attack'][self.name] < self.numCap
                    if self.usePercent:
                        target.addBase['hp'][self.name] += target.setNum[0] * self.num/100 * multiply
                    else:
                        target.addBase['hp'][self.name] += self.num * multiply

                    if target.addBase['hp'][self.name] >= self.numCap:
                        target.addBase['hp'][self.name] = self.numCap * multiply
                else:
                    if self.usePercent:
                        target.addBase['hp'][self.name] = target.setNum[0] * self.num/100 * multiply
                        #print(target.addBase['maxhp'][self.name])
                    else:
                        target.addBase['hp'][self.name] = self.num * multiply

                    if target.addBase['hp'][self.name] >= self.numCap:
                        target.addBase['hp'][self.name] = self.numCap * multiply

            if 'atk' in self.type:
                if self.name in target.addBase['attack']:
                    #if self.target.addBase['attack'][self.name] < self.numCap
                    if self.usePercent:
                        target.addBase['attack'][self.name] += target.setNum[1] * self.num/100 * multiply
                    else:
                        target.addBase['attack'][self.name] += self.num * multiply

                    if target.addBase['attack'][self.name] >= self.numCap:
                        target.addBase['attack'][self.name] = self.numCap * multiply
                else:
                    if self.usePercent:
                        target.addBase['attack'][self.name] = target.setNum[1] * self.num/100 * multiply
                    else:
                        target.addBase['attack'][self.name] = self.num * multiply

                    if target.addBase['attack'][self.name] >= self.numCap:
                        target.addBase['attack'][self.name] = self.numCap * multiply

            if 'def' in self.type:
                if self.name in target.addBase['defense']:
                    #if target.addBase['attack'][self.name] < self.numCap
                    if self.usePercent:
                        target.addBase['defense'][self.name] += target.setNum[2] * self.num/100 * multiply
                    else:
                        target.addBase['defense'][self.name] += self.num * multiply

                    if target.addBase['defense'][self.name] >= self.numCap:
                        target.addBase['defense'][self.name] = self.numCap * multiply
                else:
                    if self.usePercent:
                        target.addBase['defense'][self.name] = target.setNum[2] * self.num/100 * multiply
                    else:
                        target.addBase['defense'][self.name] = self.num * multiply

                    if target.addBase['defense'][self.name] >= self.numCap:
                        target.addBase['defense'][self.name] = self.numCap * multiply

            if 'spd' in self.type:
                if self.name in target.addBase['speed']:
                    #if target.addBase['attack'][self.name] < self.numCap
                    if self.usePercent:
                        target.addBase['speed'][self.name] += target.setNum[3] * self.num/100 * multiply
                    else:
                        target.addBase['speed'][self.name] += self.num * multiply

                    if target.addBase['speed'][self.name] >= self.numCap:
                        target.addBase['speed'][self.name] = self.numCap * multiply
                else:
                    if self.usePercent:
                        target.addBase['speed'][self.name] = target.setNum[3] * self.num/100 * multiply
                    else:
                        target.addBase['speed'][self.name] = self.num * multiply

                    if target.addBase['speed'][self.name] >= self.numCap:
                        target.addBase['speed'][self.name] = self.numCap * multiply

            if 'rge' in self.type:
                if self.name in target.addBase['range']:
                    #if target.addBase['attack'][self.name] < self.numCap
                    if self.usePercent:
                        target.addBase['range'][self.name] += target.setNum[4] * self.num/100 * multiply
                    else:
                        target.addBase['range'][self.name] += self.num * multiply

                    if target.addBase['range'][self.name] >= self.numCap:
                        target.addBase['range'][self.name] = self.numCap * multiply
                else:
                    if self.usePercent:
                        target.addBase['range'][self.name] = target.setNum[4] * self.num/100 * multiply
                    else:
                        target.addBase['range'][self.name] = self.num * multiply

                    if target.addBase['range'][self.name] >= self.numCap:
                        target.addBase['range'][self.name] = self.numCap * multiply

            if 'prod' in self.type:
                if self.name in target.addBase['productivity']:
                    #if target.addBase['attack'][self.name] < self.numCap
                    if self.usePercent:
                        target.addBase['productivity'][self.name] += target.setNum[5] * self.num/100 * multiply
                    else:
                        target.addBase['productivity'][self.name] += self.num * multiply

                    if target.addBase['productivity'][self.name] >= self.numCap:
                        target.addBase['productivity'][self.name] = self.numCap * multiply
                else:
                    if self.usePercent:
                        target.addBase['productivity'][self.name] = target.setNum[5] * self.num/100 * multiply
                    else:
                        target.addBase['productivity'][self.name] = self.num * multiply

                    if target.addBase['productivity'][self.name] >= self.numCap:
                        target.addBase['productivity'][self.name] = self.numCap * multiply

            target.levelUp(0)


        #self.target = targeted
        #self.currentTurn = self.turn

    def check(self):
        self.currentTurn -= 1
        if self.currentTurn > 0:
            if 'continuous' in self.type:
                if 'ally' in self.type:
                    if 'hp' in self.type:
                        self.target.hp += self.num
                    if 'atk' in self.type:
                        self.target.attack += self.num
                    if 'def' in self.type:
                        self.target.defense += self.num
                elif 'opponent' in self.type:
                    if 'hp' in self.type:
                        self.target.hp -= self.num
                    if 'atk' in self.type:
                        self.target.attack -= self.num
                    if 'def' in self.type:
                        self.target.defense -= self.num
        elif self.target != None:
            if 'permanent' not in self.type:
                if 'ally' in self.type:
                    if 'hp' in self.type:
                        self.target.hp -= self.num
                    if 'atk' in self.type:
                        self.target.attack -= self.num
                    if 'def' in self.type:
                        self.target.defense -= self.num
                elif 'opponent' in self.type:
                    if 'hp' in self.type:
                        self.target.hp += self.num
                    if 'atk' in self.type:
                        self.target.attack += self.num
                    if 'def' in self.type:
                        self.target.defense += self.num
            self.target = None


buffList = []
debuffList = []
class Effect:
    def __init__(self, name, type, info, num=0, usePercent=False, multiplier=1, stackable=False, applyRepeated=False, delay='0T', doStun=False, useAtStart=True, useVisual=False, affectWhat=None, color=(255, 255, 255)):
        if affectWhat == None:
            affectWhat = {'hp': 30}
        self.name = name
        self.type = type
        self.num = num
        self.doStun = doStun
        self.info = info
        self.multiplier = multiplier
        self.stackable = stackable
        self.applyRepeated = applyRepeated
        self.delay = delay
        self.useVisual = useVisual
        self.color = color
        self.useAtStart = useAtStart
        effectList.append(self)
        if self.type == 'Buff':
            buffList.append(self)
        elif self.type == 'Debuff':
            debuffList.append(self)

#    def update(self, ):
    def remove(self, target):
        if self in target.buff:
            del target.buff[self]

    def apply(self, caster, target, num=1, amplifier=1, stackDur=False, stackAmp=False, maxAmp=None, maxDur=None, turn=0):
        target.levelUp(0, False)
        if self.type != 'Passive':
            oriDur = oriAmp = 0
            #if self not in target.buff or not stackDur:
            oriDur = 0
            oriTurn = 0
            if stackDur:
                if self in target.buff:
                    oriDur += target.buff[self][0]
                    oriTurn += target.buff[self][3]
            if stackAmp:
                if self in target.buff:
                    oriAmp = target.buff[self][2]
            oriDur += num
            oriAmp += amplifier
            oriTurn += turn
            if turn > 0:
                oriTurn += 1
            if maxAmp != None:
                oriAmp = min(oriAmp, maxAmp)
            if maxDur != None:
                oriDur = min(oriDur, maxDur)
            target.buff[self] = [oriDur, caster, oriAmp, oriTurn]
            effectStuff[(self, target)] = [oriDur, target, True, caster, oriAmp, oriTurn]
        else:
            effectStuff[(self, target)] = [target, True, 'Passive']
            if self not in target.passiveBuff:
                target.passiveBuff[self] = [False, False]
           # boolean = False
            #if self.name == 'Locked In':
             #   if target.hp < 90


def actCall(act, target, actor):
    return None

class Act:
    def __init__(self, name, desc, sparingPoints, energyPoints, superPoints, checkAttack, useOn, color=WHITE, canTargetDead=False, range=None, considerRange=False):#, usePattern, number):

      self.name = name

      self.desc = desc

      self.sparingPoints = sparingPoints

      self.energyPoints = energyPoints

      self.superPoints = superPoints

      self.checkAttack = checkAttack

      self.useOn = useOn

      self.color = color

      actObj[self.name] = self

      self.range = range

      self.considerRange = considerRange

      self.canTargetDead = canTargetDead

      #self.usePattern = usePattern

      #self.number = number

    def call(self, target, actor, actDialogueNum):
        spareGiven = self.sparingPoints
        checkingAttack = False
        actReturn = ''
        actor.activity = 'Act_done'# + self.name
        if target != actor:
            target.activity = 'Acted_on'# + self.name
        if self.checkAttack:
            if target.hp < target.maxHp:
                checkingAttack = True

        if self.name == 'Check':
            actReturn = [
                        f"* Name: {target.name}.\n* LVL {target.level}  {target.attack} ATK  {target.defense} DEF  {target.speed} SPD",
                        f"* {target.info}"
                        ]

        if self.name == 'Defend':
            actReturn = [f"* {actor.name} became wary and defended."]
            defendBuff.apply(actor, target, 1)

        if self.name == 'Swap':
            actReturn = [f"* {actor.name} swapped postion with {target.name}!"]

        if self.name == 'Heal':
            actReturn = [
                        f"* {actor.name} recovered small amount of their hp.",
                        f"* But was it worth it?"]
            fightyLoop.append([target, actor, int(-1 * target.maxhp/10)])
            if actor.hp > actor.maxhp:
                actor.hp = actor.maxhp

        if self.name == 'InstaSpare':
            actReturn = [f"* {actor.name} did something cool!"]

        if self.name == 'Talk':
            if target.name == 'Allerwave':
                actReturn = [f"* {actor.name} try to talk to {target.name}.", "* Allerwave seems pleased."]
            else:
                actReturn = [f"* {actor.name} try to talk some sense into {target.name}.", f"* But {target.name} refuse to listen."]
                target.spare -= self.sparingPoints

        if self.name == 'Spare':
            if target.spare >= 100:
                target.status = 'Spared'
                actReturn = [f"* {actor.name} spared {target.name}!"]
            else:
                actReturn = [f"* {actor.name} try to spare...", "* But the enemy isn't sparable yet..."]

        if self.name == 'Stunned':
            actReturn = [f"* {actor.name} cannot do any actions! Turn skipped!"]

        if self.name == 'Sparing':
            actReturn = [f"* {actor.name} doesn't want to fight anymore..."]

        if self.name == 'Level Up':
            if actor.level < 20:
                playSound('Level_sfx.ogg')
                effectText.append([self, target, 0, False])
                target.sprite.color = (255, 255, 0)
                target.sprite.tintColor = (255, 255, 0)
                target.sprite.targetColor = (255, 255, 0)
                actReturn = [f"* {actor.name} leveled up!"]
                actor.level += 1
                actor.levelUp(0)
            else:
                actReturn = [f"* {actor.name} try to level up...", f"* ...", "* Nothing happened.", "* The AP went to waste.", "* Yet you swore something in the corner of your eye..."]


        if self.name == 'Overcharge':
            playSound('Level_sfx.ogg')
            #effectText.append([self, target, 0, False])
            target.sprite.color = (0, 255, 255)
            target.sprite.tintColor = (0, 255, 255)
            target.sprite.targetColor = (0, 255, 255)
            actReturn = [f"* {actor.name} went into Overdrive!"]
            overdrive.apply(actor, target, 0, 5, turn=10)
            #actor.level += 1
           # actor.levelUp(0)
        actUsed = self
        anyThing = actCall(actUsed, target, actor)
        if isinstance(anyThing, list):
            actReturn = anyThing
        target.spare += self.sparingPoints
        if int(-1*self.energyPoints*target.productivity) < 0:
            actor.levelUp(0)
            energyLoop.append([actor, actor, int(-1*self.energyPoints*actor.productivity)])
        elif int(-1*self.energyPoints) > 0:
            actor.levelUp(0)
            energyLoop.append([actor, actor, int(-1*self.energyPoints)])

       # actor.mana += self.energyPoints
        actor.mana = min(actor.mana, actor.maxMana)
        if target.spare >= 100:
            target.spare = 100
        return actReturn

        #usingPattern = self.usePattern

class Fight:
    def __init__(self, name, infoClass, classType, info, extraInfo='', range='Default', baseAttack='Default', attack='Default', bars=None,
                 useHitChance=False, hitChanceEquation='95-Range*10', stackDuration=False, stackAmplifier=False, applyEffect=None, removeEffect=None,
                 maxAmplifier=None, maxDuration=None, fightAnim='attack', barFightAnim=None, allAtOnce=True, color=WHITE):
        if applyEffect == None:
            applyEffect = {}
        if removeEffect == None:
            removeEffect = {}
        if bars == None:
            bars = ['A1']
        if barFightAnim == None:
            barFightAnim = {}
            for i in bars:
                barFightAnim[i] = 'attack'
        #classType = 'Back' if classType in ['Melee', 'Tank'] else 'Support'
        self.name = name
        self.infoClass = infoClass
        self.classType = classType
        self.info = info
        self.extraInfo = extraInfo
        self.bars = bars
        self.range = range
        self.useHitChance = useHitChance
        self.stackDuration = stackDuration
        self.hitChanceEquation = hitChanceEquation
        self.stackAmplifier = stackAmplifier
        self.applyEffect = applyEffect
        self.removeEffect = removeEffect
        self.baseAttack = baseAttack
        self.attack = attack
        self.maxDuration = maxDuration
        self.maxAmplifier = maxAmplifier
        self.fightAnim = fightAnim
        self.barFightAnim = barFightAnim
        self.currentBar = 'A1'
        self.nextBar = 'A1'
        self.allAtOnce = allAtOnce
        self.color = color

        fightObj[self.name] = self

    #def use(self, caster, target):
        #pass

    def projectileStart(self, caster, target, damage, trueDamage, listThing, projSprite, bar):
        if self.name == "Annoying Hacks" and ("Default" in caster.skin or "Job Application" in caster.skin):
            extra = ''
            extraList = ['', '_Tri', '_Squ', '_Hex']
            extra = random.choice(extraList)
            projSprite.image = f'attackAnimate/projectile/{self.name}_{caster.skin}{extra}.png'

    def projectileUse(self, caster, target, damage, trueDamage, listThing, projSprite, bar):
        doStun = False
        for i in caster.buff:
            if i.name == 'Shocker':
                number = random.randint(1, 100)
                if number <= 20:
                    doStun = True
        if doStun:
            stun.apply(caster, target, 0, 1, turn=1)
        target.tracker['currentDamage'] = trueDamage
        for i in self.bars:
            if i not in self.barFightAnim:
                #print(True)
                self.barFightAnim[i] = self.fightAnim
        if self.name == 'SCREAM':
            if isinstance(target, Player):
                whichOne = party
            else:
                whichOne = opponent
            whichOne.index(target)
            targetting = []
            if whichOne.index(target) != 0:
                targetNum = whichOne.index(target) - 1
                while whichOne[targetNum].hp <= 0 and targetNum != 0:
                    targetNum -= 1
                if whichOne[targetNum].hp > 0:
                    targetting.append(whichOne[targetNum])

            if whichOne.index(target) + 1 < len(whichOne):
                targetNum = whichOne.index(target) + 1
                while whichOne[targetNum].hp <= 0 and targetNum < len(whichOne) - 1:
                    targetNum += 1
                if whichOne[targetNum].hp > 0:
                    targetting.append(whichOne[targetNum])
            targetting.append(target)

            for i in targetting:
                if "Screamer" in caster.skin:
                    chance = 45
                else:
                    chance = 35
                num = random.randint(1, 100)
                if num <= chance:
                    fightyLoop.append([i, caster, trueDamage//2])
                    stun.apply(caster, i, 0, 1, turn=2)
        elif self.name == 'Purple Power':
            if isinstance(target, Player):
                whichOne = party
                factor = -1
                limit = 0
                newList = []
                for i in whichOne:
                    if i.hp > 0:
                        newList.append(i)
                whichOne = newList
            else:
                whichOne = opponent
                factor = 1
                newList = []
                for i in whichOne:
                    if i.hp > 0:
                        newList.append(i)
                limit = len(newList) - 1
                whichOne = newList
            if whichOne.index(target) != limit and isinstance(damage, int) and projSprite.image != 'attackAnimate/projectile/Purple Power_Strong.png':
                listThing[0].append(whichOne[whichOne.index(target) + factor])
                listThing[7].append(False)
                projSprite.image = 'attackAnimate/projectile/Purple Power_Strong.png'
                caster.newNum[1] = 31
                caster.levelUp(0)
                speedNum = random.randint(1, 100)
                if speedNum <= target.speed/2:
                    #print(target.speed/2, speedNum)
                    listThing[4] = 1
                listThing[3] = max(int( listThing[6][4] * (caster.attack * (100 - target.defense)/100) ), 1)#trueDamage * (31/18)

        elif self.name == 'Knockback':
            if isinstance(target, Player):
                whichOne = party
                factor = -1
                limit = 0
                allAlive = []
                for i in whichOne:
                    if i.hp > 0:
                        allAlive.append(i)
            else:
                whichOne = opponent
                factor = 1
                limit = len(opponent) - 1
                allAlive = []
                for i in whichOne:
                    if i.hp > 0:
                        allAlive.append(i)
                limit = len(allAlive) - 1
            if target not in allAlive:
                return False
            if allAlive.index(target) != limit and isinstance(damage, int):
                if listThing[6][4] == 1 and random.randint(1, 100) <= 50:
                    playerA = target
                    playerB = allAlive[allAlive.index(target) + factor]
                    indexA = whichOne.index(playerA)
                    indexB = whichOne.index(playerB)
                    whichOne[indexB] = playerA
                    whichOne[indexA] = playerB
                    speedReset()
        elif self.name == "Annoying Hacks":
            doBuff = random.randint(0,1)
            if doBuff == 1 and isinstance(damage, int):
                effectList = [confusion, distracted, tired, slow, blindness, stun, burning, poison]
                amplifier = [1, 1, 2, 1, 1, 1, 1, 1]
                effectNum = random.randint(0, 7)
                effectList[effectNum].apply(caster, target, 1, amplifier[effectNum])
        elif self.name == "Adventure Sword":
            doBuff = random.randint(0,1)
           # print(doBuff)
            if doBuff == 1 and isinstance(damage, int) and listThing[6][4] == 1 :
                effectList = [stun]
                #amplifier = [1, 1, 2, 1, 1, 1, 1, 1]
                #effectNum = random.randint(0, 7)
                stun.apply(caster, target, 1, 1)


        #pass

debug = []
speedReset = ''
class Debug:
    def __init__(self, name, info):
        self.name = name
        self.info = info
        debug.append(self)

    def use(self, target):
        if self.name == 'Level Up':
            target.level += 1
            target.levelUp(0)

        if self.name == 'Level Down':
            target.level -= 1
            target.levelUp(0)

        if self.name == 'Increase AP':
            energyLoop.append([target, target, -10])

        if self.name == 'Decrease AP':
            energyLoop.append([target, target, 10])

        if self.name == 'Increase HP':
            fightyLoop.append([target, target, -50])

        if self.name == 'Decrease HP':
            fightyLoop.append([target, target, 50])

        if self.name == 'Instakill':
            fightyLoop.append([target, target, target.maxhp])

        if self.name == 'Revive':
            fightyLoop.append([target, target, -int(target.maxhp - target.hp)])

        if self.name == 'Buff':
            buffChoice = random.randint(0, len(buffList)-1)
            buffList[buffChoice].apply(target, target, 1, 1, True, True)

        if self.name == 'Debuff':
            buffChoice = random.randint(0, len(debuffList)-1)
            debuffList[buffChoice].apply(target, target, 1, 1, True, True)

        if self.name == 'Clear Buff':
            for i in target.buff:
                target.buff[i][0] = 0
                i.apply(target, target, 0, 0, True, True)
            #target.buff.clear()
        if self.name == 'Add Item':
            itemChoice = random.randint(0, len(itemList)-1)
            target.inventory.append(itemList[itemChoice])
            #debuffList[buffChoice].apply(target, target, 1, 1, True, True)

        if self.name == 'Add Fight Bars V1':
            #fightyLoop.append([target, target, target.maxhp])
            for i in target.fight:
                lastBar = i.bars[len(i.bars)-1]
                i.bars.append(chr(ord(lastBar[0]) + 1))
                for j in i.bars:
                    if j not in i.barFightAnim:
                        i.barFightAnim[j] = i.fightAnim



        if self.name == 'Add Fight Bars V2':
            #fightyLoop.append([target, target, target.maxhp])
            for i in target.fight:
                lastBar = i.bars[len(i.bars)-1]
                i.bars.append(lastBar[0] + str(int(lastBar[1:]) + 1))
                for j in i.bars:
                    if j not in i.barFightAnim:
                        i.barFightAnim[j] = i.fightAnim

        if self.name == 'Summon Ally':
            if isinstance(target, Player):
                if len(party) != len(validAlly):
                    randomNum = random.randint(0, len(validAlly) - 1)
                    while validAlly[randomNum] in party:
                        randomNum = random.randint(0, len(validAlly) - 1)
                    party.append(validAlly[randomNum])
            else:
                randomNum = random.randint(0, len(validEnemy) - 1)
                while validEnemy[randomNum] in opponent:
                    randomNum = random.randint(0, len(validEnemy) - 1)
                opponent.append(validEnemy[randomNum])

        if self.name == 'Unlimited Range':
            global freeRange
            freeRange = not freeRange

levelUp = Debug('Level Up', 'Target will be leveled up.')
levelDown = Debug('Level Down', 'Target will be leveled down.')
apUp = Debug('Increase AP', 'Target will gain 10AP.')
apDown = Debug('Decrease AP', 'Target will lose 10AP.')
hpUp = Debug('Increase HP', 'Target will gain 50HP.')
hpDown = Debug('Decrease HP', 'Target will lose 50HP.')
instaKill = Debug('Instakill', 'Target will die.')
revive = Debug('Revive', 'Target will be revived.')
buff = Debug('Buff', 'Target will gain a random buff.')
debuff = Debug('Debuff', 'Target will gain a random debuff.')
clearBuff = Debug('Clear Buff', 'Target will lose all status effects.')
barAdd = Debug('Add Fight Bars V1', 'Target normal Attacks will gain a Undertale Yellow styled bar.')
barAdd = Debug('Add Fight Bars V2', 'Target normal Attacks will gain a Undertale styled bar.')
addItem = Debug('Add Item', "Add a random item to the Target inventory.")
summonAlly = Debug('Summon Ally', 'Summon Ally')
rangeFree = Debug('Unlimited Range', 'Remove Range stat as a factor.')
freeRange = False

#hpDown = Debug('Decrease HP', 'Target will lose 50HP.')

# Effect( Name, Type, Info, Percentage, Multiplier)
#bleed = Effect('Bleeding', 'Debuff', 'Loses Hp Every Turn', 20, 5, True, (180, 0, 0))
defendBuff = Effect('Defended', 'Buff', 'Boost defense by 2x', 0, 3, False, color=(200, 200, 200))
itch = Effect('Itched', 'Debuff', 'Lowers Attack and Speed', 30, 2, False, color=(213, 211, 178))
encouragement = Effect('Encouraged', 'Buff', 'Increase defense by 1.35x', 30, 2, True, color=(213, 211, 178))
trapped = Effect('Trapped', 'Debuff', 'Disable your Turn', 20, 3, True, doStun=True, useVisual=True, color=(200, 200, 200))
stun = Effect('Stun', 'Debuff', 'Disable your Turn', 20, 3, True, doStun=True, useVisual=False, color=(255, 255, 0))
block = Effect('Blocking', 'Buff', 'Blocks all incoming attacks.', 20, 3, True, doStun=False, useVisual=False, color=(100, 100, 100))
blindness = Effect('Blindness', 'Debuff', 'Lowers hit accuracy.', 20, 3, True, doStun=False, useVisual=False, color=(100, 100, 100))
shocker = Effect('Shocker', 'Buff', 'Gives chance to stun.', 20, 3, True, doStun=False, useVisual=False, color=(255, 255, 100))

# Main Buffs
healing = Effect('Healing', 'Buff', 'Gain HP every turn', applyRepeated=True, num=5, color=(0, 255, 0))
vitality = Effect('Vitality', 'Buff', 'Boost Max Health', num=20, color=(0, 255, 255))
force = Effect('Force', 'Buff', 'Boost Attack', num=20, color=(255, 0, 0))
guard = Effect('Guard', 'Buff', 'Boost Defense', num=20, color=(0, 0, 255))
momentum = Effect('Momentum', 'Buff', 'Boost Speed', num=20, color=(255, 255, 0))
efficiency = Effect('Efficiency', 'Buff', 'Boost Productivity', num=20, color=(255, 0, 255))
reach = Effect('Reach', 'Buff', 'Boost Range', num=20, color=(255, 150, 0))
overdrive = Effect('Overdrive', 'Buff', 'Boost All', num=20, color=(0, 150, 255))

#Damage dealer
bleeding = Effect('Bleeding', 'Debuff', 'Lose HP every turn', applyRepeated=True, num=5, color=(180, 0, 0), useAtStart=False)
burning = Effect('Burning', 'Debuff', 'Lose HP every turn', applyRepeated=True, num=6, color=(255, 100, 0), useAtStart=False)
poison = Effect('Poison', 'Debuff', 'Lose HP every turn', applyRepeated=True, num=4, color=(0, 150, 0), useAtStart=False)

#Corrupted counterpart
vulnerable = Effect('Vulnerable', 'Debuff', 'Lose Max Health', num=20, color=(75, 129, 149))
confusion = Effect('Confusion', 'Debuff', 'Lose Attack', num=20, color=(130, 73, 73))
distracted = Effect('Distracted', 'Debuff', 'Lose Defense', num=20, color=(73, 73, 130))
slow = Effect('Slow', 'Debuff', 'Lose Speed', num=20, color=(130, 130, 73))
tired = Effect('Tired', 'Debuff', 'Lose Productivity', num=20, color=(130, 73, 130))
restricted = Effect('Restricted', 'Debuff', 'Lose Range', num=20, color=(130, 90, 73))

#Passive
doubleStrike = Effect('Double Strike', 'Passive', 'When FInley falls below 20% Health, they attack their next target twice. This only happens once every time they fall below 20% Health. However it can happen again if Finley heals and falls below 20% Health again.', color=(211, 211, 211))
booster = Effect('Boosters', 'Passive', "Rayson's speed increases by 1.50x after his health drops below 50%.", color=(150, 255, 150))
glitched = Effect('Glitched', 'Passive', "Rayson's attack has a 20% chance of multiplying its damage by 1.25x.", color=(150, 255, 150))
lockedIn = Effect('Locked In', 'Passive', "Lock's damage increases by 30% while his health is below 30%.", color=(255, 255, 0))
iteker = Effect('Iteker', 'Passive', 'After 15 turns, Rekety turns into Iteker and now casts a higher stage of Bleeding every 10 turns, starting at Bleeding II when Iteker is triggered. (Max Stage: Bleeding V)', num=5, color=(150, 0, 0))
regenTurn = Effect('Regeneration', 'Passive', 'Rany heals 5 Health every turn.', color=(255, 0, 0))
sadism = Effect('Sadism', 'Passive', "Dandee enjoys watching others suffer and die. When someone dies, whether it's his enemies or teammates, Dandee gains Force I buff for 5 turns and it adds to the amount of turns if it is still active.", color=(100, 255, 100))
disperse = Effect('Disperse', 'Passive', 'When Dandee is defeated, he releases 3 blowballs each in 8 different directions, damaging anyone who is near him.', color=(255, 255, 255))
readyToStrike = Effect('Ready To Strike', 'Passive', 'If Red Dude get damaged by an enemy in 3 different turns, his attack increases by 1.25x for the rest of the battle.', color=(210, 50, 50))
productivityZero = Effect('Productivity Zero', 'Passive', 'After being damaged, Thin becomes weak and his Productivity drops to 0.00x', color=(100, 100, 100))
caneHealing = Effect('Cane Healing', 'Passive', "When Caen takes damage, all allies within a radius of 1 are healed for 60% of the damage he receives and gain Momentum I for 2 turns. If Momentum has more than 2 turns remaining, its duration won't extend. It only resets to 2 turns if it's at 2 or fewer.", color=(255, 100, 100))
healingTunes = Effect('Healing Tunes', 'Passive', 'T Music plays on his special keyboard, healing allies within a radius of 1 by 10 HP each cycle.', color=(255, 100, 100))
weAreRumbley = Effect('We Are Rumbley', 'Passive', 'You may select multiple Rumbleys in a battle. At the end, XP gained is averaged based on their performance, then slightly multiplied depending on how many Rumbleys participated. The more united their effort, the more they grow together.', color=(255, 100, 255))

#bleedSword.applyEffect = {bleeding:[inf, 1]}
#heavySword.applyEffect = {slow:[inf, 1]}

fluffball = Fight('Fluffball', 'Ranged', 'Support', 'Taphygrafy releases extra fluff that has dust and dirt trapped in it. Dealing low damage by making its target uncomfortable and itchy.')

cutStuff = Fight('Just Cut', 'Melee', 'Melee', 'Finley cuts their chosen target with their knife.', range=1, baseAttack=4, attack=42, barFightAnim={'A1':'attack', 'B1':'attack'})
knifeShot = Fight('Knife Shot', 'Ranged', 'Range', 'Finley makes a precise shot with their knife.', range=4, baseAttack=3, attack=38, fightAnim='attack_range', barFightAnim={'A1':'attack_range', 'B1':'attack_range'})

tasteThePaper = Fight('Taste the Paper!', 'Thrower', 'Thrower', 'Calvy throws one of his many thick notebooks that are filled with doodles, damaging the target it lands on')

powerBullet = Fight('Power Bullet', 'Ranged', 'Range', 'Rayson fires a green bullet made out of energy and sharp metallic parts, damaging enemies from a far distance.')

spike = Fight('Spike', 'Under Attack', 'Under', 'Blue Guy creates a spike with his powers, damaging his target by making it impale them from the ground.')

strike = Fight('Strike', 'Melee', 'Melee', 'Li Wei use the Sickle to strike a targetted enemy. It have been used before.')

punch = Fight('Punch', 'Melee', 'Tank', 'Lock punches a targeted enemy with his fist.')

pencilJab = Fight('Pencil Jab', 'Melee', 'Melee', 'Rany jabs his foes with a strong sharp pencil.')

webBomb = Fight('Web Bomb', 'Thrower', 'Thrower', 'Ocho spins rapidly to create a web bomb and then hurl it at his enemy, casting a Slow I for 3 turns which adds more if he targets players which have the Slow debuff active.', stackDuration=True, applyEffect={slow: [0, 1, 3]})

watchYouBleed = Fight('Watch you bleed', 'Melee', 'Melee', 'Rekety aims for certain part of his opponent, causing them to bleed, casting Bleeding I debuff which last for 1 cycle and will keep upgrading the longer the battle lasts.', applyEffect={bleeding: [1, 1]})

blowballs = Fight('Blowballs', 'Ranged', 'Range', 'Dandee ejects 5 blowballs that upon contact with the target, deals small amounts of damage each. The further the blowballs travel, the more likely it will miss the target.', extraInfo=" \n Range 1: 85% \n Range 2: 75% \n Range 3: 65% \n Range 4: 55% \n Range 5: 45%", attack=13, useHitChance=True, bars=['A1', 'B1', 'C1', 'D1', 'E1'])

blastRay = Fight('Blast Ray', 'Ranged', 'Range', 'A powerful beam, magnified by the Crown power!', bars=['A1', 'A2', 'B1'])

scratch = Fight('Scratch', 'Melee', 'Melee', 'Copycat scratches its target, damaging them.')

crimsonFang = Fight('Crimson Fang', 'Melee', 'Melee', 'Red Dude strikes his target, damaging them and casting a Confused I debuff on them for 3 turns. Debuff does not stack, resets back to 3 turns if enemy is struck again.', applyEffect={confusion: [0, 1, 3]})
#Under, Slam, Back
winterWhack = Fight('Winter Whack', 'Melee', 'Slam', 'Candace whacks her target with her candy cane, damaging them.')

weakPoke = Fight('Weak Poke', 'Melee', 'Melee', 'Thin tries to attack the enemy, damaging both the enemy and himself.')

hotTea = Fight('Hot Tea', 'Thrower', 'Thrower', "Mr Grafy's hat throws a hot cup of tea at his target, dealing damage and applying Burning I for 3 turns. If hit again while Burning I is active, it resets back to 2. Don't question how the tea stays in the cup in mid-air.", applyEffect={burning: [0, 1, 2]})

doubleFistBash = Fight('Double Fist Bash', 'Melee', 'Melee', 'Jam Jar bashes his target with both his fists.', bars=['A1', 'B1'], attack=23, barFightAnim={'A1':'attack', 'B1':'attack_2'}, allAtOnce=False)

lidSlam = Fight('Lid Slam', 'Ram', 'Slam', 'Jam Jar rushes towards his target and slams into them with his lid.')

scream = Fight('SCREAM', 'Spam', 'Tank', 'Screamy floats toward his target and unleashes a bone-chilling scream. The main target takes full damage, and all enemies within a radius of 1 have a 35% chance to be Stunned for 1 turn. Stunned enemies in the radius also take 0.5x the damage dealt to the main target. If a target is already stunned, no additional stun is applied.')

sharpCane = Fight('Sharp Cane', 'Range', 'Range', 'Caen fires a sharpened candy cane, damaging the target when hit ')

purplePower = Fight('Purple Power', 'Thrower', 'Thrower', 'Purple Kid hurls a purple energy ball that bounces off the target, dealing light damage, before hitting the rumbler behind for heavier damage.', attack=18)

sliceTime = Fight('Slice Time', 'Melee', 'Melee', 'Locon slices his target with a pizza cutter.')

melodyBurst = Fight('Melody Burst', 'Range', 'Range', 'T Music plays on his special keyboard, sending out damaging musical notes that strike a targeted enemy.')

knockback = Fight('Knockback', 'Melee', 'Melee', 'Blue-Black deal a powerful punch on his target. Upon a critical hit, has a 50% chance of pushing the target back by 1 space, swapping spaces with the enemy behind the target.')

threeShot = Fight('Three Shot', 'Ranged', 'Range', 'Orange Girl fires 3 energy shots at her target, damaging them.', attack=14, bars=['A1', 'B1', 'C1'])

_4ero4rm = Fight('4ero 4rm', 'Ranged', 'Range', '4minti fires his arm at his target, damaging them from a distance.')

solarDart = Fight('Solar Dart', 'Ranged', 'Hold', 'Yellow Spark charges up a bright energy shot and fires it at her target, inflicting 1 turn of Blindness I.', applyEffect={blindness:[0, 1, 1]})

hornLaunch = Fight('Horn Launch', 'Thrower', 'Thrower', 'Gregley launches both his horns, each dealing damage to his target.', attack=21, bars=['A1', 'B1'])

zeefight = Fight('[CORRUPTED]', 'Melee', 'Melee', '[REDACTED]', bars=['A1', 'B2', 'C3', 'D4', 'E5', 'F6'])

swordSlash = Fight('Sword Slash', 'Melee', 'Back', 'Uses the Sickle to strike a targetted enemy. It have been used before.', bars=['A1', 'B1'], barFightAnim={'A1':'attack', 'B1':'attack_2'}, allAtOnce=False)

knuckleDash = Fight('Knuckle Dash', 'Melee', 'Melee', 'Rumbley quickly dashes toward their target and delivers a solid punch, dealing damage on impact.')

annoyingHacks = Fight('Annoying Hacks', 'Key Pattern (Range)', 'Controller', 'Blueberry shoots one of his annoying attacks, dealing damage and having a 50% chance to apply one of the following debuffs randomly for 1 cycle: Confused I, Distracted I, Slow I, Tired II, Blindness I, Stun, Burning I or Poison I.')

adventureSword = Fight('Adventure Sword', 'Melee', 'Melee', "Adv-Grafy strikes his target with his trusty wooden adventure sword. On a critical hit, there's a 50% chance to stun the target for 1 cycle.")

newFrame = 0
battleFrame = 0

#healThread = threading.Thread(target=healWhileloop)
#healThread.start()
healthPill = Item('Bandage', 'Item: ally, hp', 100, "Recover the User's health by wrapping around the injury site. Some say that these bandages are magic.", targetType='Self')
glowingHealthPill = Item('Medkit', 'Item: ally, hp', 200, 'A kit containing everything you can use to treat many injuries. This allow the User to recover more Health.', targetType='Self')
attackPill = Item('Attack Pill', 'Item: ally, atk', 10, "Increase and strengthen the User's muscle instantly, raising the User's Attack.", targetType='Self')
defensePill = Item('Defense Pill', 'Item: ally, def', 10, "Immediately densify the User's body and making it durable, raising the User's Defense.", targetType='Self')
speedPill = Item('Speed Pill', 'Item: ally, spd', 10, "Instantly boost the User's energy and increase User's stamina, raising the User's Speed.", targetType='Self')
coffee = Item('Coffee', 'Item: ally, prod', 0.05, "Replaced the now banned Productivity Pill. When drunk, it increase the User's Productivity slightly.", targetType='Self')
extender = Item('Arm Extenders', 'Item: ally, rge', 1, "When used, it allows the User to reach further. This increase the User's Range.", targetType='Self')
vitalPill = Item('Vitality Pill', 'Item: ally, maxhp', 25, "An experimental pill that force the User's cells to become stronger, increasing their maximum Health.", targetType='Self')
cyanide = Item('Cyanide Vial', 'Item: opponent', 10, "Throw it at the target, they will get Cyanide Poisoning. Inflicts them with Poison II that last 5 turns.", targetType='Single')
dynamite = Item('Dynamite', 'Item: opponent, hp', 1000, "Throw it at the target, they will explode and die. No chance of recovery.", targetType='Single')
elixer = Item('Elixer', 'Item: ally', 0, "A glowing pulsating elixer that can cure the User of many Debuffs.", removeEffect=[bleeding, poison, vulnerable, confusion, distracted, slow, tired])
divinePotion = Item('Divine Potion', 'Item: ally, hp, atk, def, spd, prod, rge, canRevive', 50, "Cures many Debuffs, and give the User incredible strength in every area. Also can be used to revive people!", removeEffect=[bleeding, poison, vulnerable, confusion, distracted, slow, tired])
redHalos = Item('Swirling Halos', 'Weapon: ally, atk, spd, rge', 200, 'These crimson halos pulsate with immense power, rumours suggest they belong to a powerful entity. If worn, User may become corrupted by the godlike power they give.')
redCloak = Item('Eternal Cloak', 'Armour: ally, def, prod, maxhp', 200, 'This cloak flows like red stardust, rumours suggest they belong to a powerful entity. If worn, User may become corrupted by the godlike power they give.')
bleedSword = Item('Bleeding Sword', 'Weapon: ally', 70, 'A sword that harm you in exchange for power.', applyEffect={copy.deepcopy(bleeding):[inf, 1]})
heavySword = Item('Heavy Sword', 'Weapon: ally', 50, 'A sword that while powerful, slows you down.', applyEffect={copy.deepcopy(slow):[inf, 2]})
ironSword = Item('Iron Sword', 'Weapon: ally', 30, 'A simple albeit weak sword. Useful for beginners, useless for advanced people.')
boneSword = Item('Iron Sword', 'Weapon: ally', 90, 'An enchanted sword made of bone, it have tasted blood before.')
darkArmour = Item('Dark Armour', 'Armour: ally', 40, "A powerful armour that increase the Wearer's Maximum Health and Defense in exchange for the Wearer's Productivity.", applyEffect={copy.deepcopy(tired):[inf, 4], copy.deepcopy(block):[inf, 5]})
steelChestplate = Item('Steel Chestplate', 'Armour: ally', 20, 'A durable armour with reasonable protection. The heaviness of the armour could make the Wearer slower.', applyEffect={copy.deepcopy(slow):[inf, 1]})
leatherChestplate = Item('Leather Chestplate', 'Armour: ally', 5, 'A weak chestplate for a weak protection. It have been used many times over.')

canRevive = True # True means it needs reviving spells, False means heal spells can work
playerHp = {}

check = Act('Check', 'Check an enemy to try to find some useful info about them.', 0, 6, 6, False, 'opponent', canTargetDead=True)
defend = Act('Defend', 'Increase defense for one cycle.', 0, 20, 20, False, 'self')
swap = Act('Swap', 'Swap position with another party member.', 0, 0, 0, False, 'ally')
heal = Act('Heal', 'Recover a small amount of hp. Useful sometimes.', 0, 2, 2, False, 'self')
level_up = Act('Level Up', 'The character will level up!', 0, -100, 0, False, 'self')
overcharge = Act('Overcharge', 'The character will be in Overdrive V for 10 turns!', 0, 0, -1000, False, 'self')
talk = Act('Talk', 'Try to reason with the opponent. Hopefully it may work.', 34, 10, 10, False, 'opponent')
instaSpare = Act('InstaSpare', 'Increase the opponent spare to max!TESTING ONLY', 100, 0, 0, False, 'opponent')
spare = Act('Spare', 'Try to attempt to spare an opponent.', 0, 0, 0, False, 'opponent')
stunned = Act('Stunned', 'Stun', 0, 0, 0, False, 'opponent')
sparing = Act('Sparing', 'Sparing', 0, 0, 0, False, 'opponent')
#Act(

actions = [check, defend, swap, heal, level_up, overcharge, talk, spare]

sword = Item('Iron Sword', 'slashWeapon', 50, 'A simple yet elegant and sharp Iron blade. [BETA ITEM]')
bat = Item('Baseball Bat', 'bashWeapon', 15, 'A really hard wooden Bat, it can cause concussion. [BETA ITEM]')
pencil = Item('Long Pencil', 'bashWeapon', 15, 'A really long and sharp wooden pencil.  [BETA ITEM]')
staff = Item('Orb Staff', 'magicWeapon', 30, 'A beginner magic Staff, the orb swirl a lot. [BETA ITEM]')
phone = Item('Brick Phone', 'rangeWeapon', 20, 'Who in the right mind made these hard phones? [BETA ITEM]')
helmet = Item('Iron Helmet', 'Armour', 10, 'A sturdy protective Helmet! [BETA ITEM]')
milk = Item('Milk', 'Item', 100, 'A very very refreshing Milky Milk! [BETA ITEM]')
___ = Item('3uahw8dka9wjsus8', 'slashWeapon', 23981929, 'eddew7d7edghwde908wjz9-0a. [BETA ITEM]')

# Tags are atk, def, hp, maxhp, continuous, permanent, multi_num, all, self, revive
# Stackable means whether to

#tYPE CAN HAVE ally: hp, maxhp, rge, prod, atk, def, spd, canRevive

statUp = Skill('Powered Boosting', cost=0, type='everyone: hp, atk, maxhp, def, spd, rge, prod, canRevive', info='Boost every single thing holy Shit',
               baseNum=100, usePercent=False, targetType='Multiple', targetAmount=3, stackDuration=True, stackAmplifier=True, applyEffect={force:[10, 1], reach:[10, 1], momentum:[10, 1], healing:[10, 1],
                                                                                                 vitality:[10, 1], guard:[10, 1], efficiency:[10, 1]})
statDown = Skill('Powered Weaken', cost=0, type='everyone: hp, atk, maxhp, def, spd, rge, prod, canRevive', info='Destroy every single thing holy Shit',
               baseNum=-100, usePercent=True, targetType='Single', targetAmount=3, stackDuration=True, stackAmplifier=True, applyEffect={confusion:[10, 1], restricted:[10, 1], slow:[10, 1], poison:[10, 1],
                                                                                                 vulnerable:[10, 1], distracted:[10, 1], tired:[10, 1]})
applyEffect = {}
for i in effectList:
    if i.type != 'Passive':
        applyEffect[i] = [10, 1]

allBuff = Skill('All Buff', cost=0, type='everyone: hp, atk, maxhp, def, spd, rge, prod, canRevive', info='All thing holy Shit',
               baseNum=0, usePercent=True, targetType='Single', targetAmount=3, stackDuration=True, stackAmplifier=True, applyEffect=applyEffect)
hitAll = Skill('Hit All', cost=0, type='everyone: hp',
                   info='Attacks Everyone with a melee attack',
                   baseNum=200, num=200, useAnim=True, animType='Melee', targetType='All')

#Test
power_slash = Skill('Power Slash', cost=10, type='opponent: hp',
                   info='Attacks a target with a powerful strike.',
                   baseNum=250, num=250, useAnim=True, animType='Melee', targetType='Single')



fun_doodles = Skill('Fun Doodles', cost=30, type='ally: missingHp', info='Calvy doodles on one of his notebooks, keeping himself more calm and healing himself by 70% of his missing HP.',
                    baseNum=70, num=70, usePercent=True,
                    targetType='Self')

blue_slash = Skill('Blue Slash', cost=85, type='opponent: hp',
                   info='Blue Guy attacks with a fast flying blue slash that pierces through enemies and inflict Confusion I for one cycle, however, walls are able to block this attack.',
                   baseNum=30, num=30, useAnim=True, animType='Range', targetType='All', applyEffect={confusion:[1, 1]})

fuzzy_encouragement = Skill('Fuzzy Encouragement', cost=50, type='ally: def', info="Taphygrafy gives all his teammates some encouragement, giving them Guard I buff for 6 turns. Doing it again while Guard is still active resets the duration and increases the buff's stage (Max: Guard II).",
                            baseNum=0, num=0, targetType='All', applyEffect={guard:[0, 1, 6]}, stackAmplifier=True, maxAmplifier=2)

healing_orb = Skill('Healing Orb', cost=80, type='ally: hp', info='Rany lobs a healing orb at an ally or himself, granting Healng II buff for one cycle.',
                    baseNum=-10, num=-10, useAnim=True, applyEffect={healing:[1, 2]})

web_wrap = Skill('Web Wrap', cost=75, type='opponent: hp',
                 info='Ocho shoots a web that wraps around his target, trapping them for 2 cycles. If the trapped target is targetted again, 2 more cycles will be added.',
                  animType='Range', stackDuration=True, useAnim=True, applyEffect={trapped:[2, 1]})

copySkill = Skill('Copy', cost=70, type='everyone:', info='Copycat targets someone to copy, taking up their appearance, attacks and abilities.', num=0, baseNum=0)


cane_boost = Skill('Cane Boost', cost=45, type='ally: hp', baseNum=15, num=15, usePercent=False,
                 info='Candace consumes a Candy Cane, instantly healing 15 HP and granting 5 turns of Momentum II buff to herself. Buff turns can stack in duration.',
                  stackDuration=True, applyEffect={momentum:[0, 2, 5]}, targetType='Self')

coffee_charge = Skill('Coffee Charge', cost=55, type='ally: hp', baseNum=-10, num=-10, usePercent=False,
                 info="Mr Grafy gives a cup of coffee to an ally, granting Efficiency II for 10 turns and healing 10 HP. Drinking again while still active resets the duration and increases the buff's stage (Max: Efficiency III).",
                  useAnim=True, stackAmplifier=True, maxAmplifier=3, applyEffect={efficiency:[0, 2, 10]}, targetType='Single')

lid_off = Skill('Lid Off', cost=20, type='ally', baseNum=0, num=0, usePercent=False,
                 info='Jam Jar takes off his Lid and uses it as a shield, going into Defense mode.',
                  targetType='Self', changePhaseTo='Defense', useDialogue='defense')

lid_on = Skill('Lid On', cost=20, type='ally', baseNum=0, num=0, usePercent=False,
                 info='Jam Jar puts on his Lid, going into Offense mode.',
                  targetType='Self', changePhaseTo='Default', useDialogue='offense')

screamer = Skill('SCREAMER!', cost=90, type='ally: atk', baseNum=1.25, num=1.25, usePercent=False,
                 info='Once activated, Screamy enters his second phase. In this form, his attack is now increased by 1.25x and now has a 45% chance to stun enemies. This ability can only be used once per battle.',
                  targetType='Self', changePhaseTo='Screamer')

hot_and_ready = Skill('Hot and Ready', cost=45, type='ally: hp', baseNum=-40, num=-40, usePercent=False,
                 info="Locon tosses a fresh slice of pizza to a chosen ally, restoring 30 HP and granting Momentum I buff for 1 turn.",
                 useAnim=True, animType='Thrower', stackAmplifier=True, maxAmplifier=3, applyEffect={momentum:[0, 1, 2]}, useDialogue='skill')

orange_blast = Skill('Orange Blast', cost=82, type='opponent: hp',
                   info='Orange Girl fires a large orange energy blast, dealing damage and applying 2 turns of Distracted I debuff on the hit target.',
                   baseNum=32, num=32, useAnim=True, animType='Range', targetType='Single', applyEffect={distracted:[0, 1, 2]})

he4dshot = Skill('He4dshot', cost=62, type='opponent: hp',
                   info='4minti shoots his head straight towards his target, dealing heavy damage and stunning them for 1 turn.',
                   baseNum=50, num=50, useAnim=True, animType='Range', targetType='Single', applyEffect={stun:[0, 1, 1]}, useDialogue="skill")

spark_charge = Skill('Spark Charge', cost=78, type='ally: def',
                   info='Yellow Spark charges a selected ally, granting them Force II and Shocker I buffs for 5 turns. Buffs do not stack; if applied again while active, their durations are refreshed. For multi-hit rumblers, Shocker I only applies to the first projectile fired per turn.',
                   baseNum=0, num=0, useAnim=True, animType='Thrower', targetType='Single', applyEffect={force:[0, 2, 5], shocker:[0, 1, 5]}, useDialogue="skill")

god_mode = Skill('GOD MODE', cost=100, type='ally', usePercent=False,
                 info='Blueberry activates GOD MODE for 6 turns, making him invincible to damage and granting Force V. However, after GOD MODE ends, Blueberry suffers from Confused II debuff for 3 turns.',
                  targetType='Self', changePhaseTo='God Mode', applyEffect={force:[0, 4, 5]}, useDialogue='skill')
#Zephyr Fight Only
life_bless = Skill('Life Bless', cost=60, type='ally: hp', info='Heal every ally on the battlefield with a potent blessing.',
                    baseNum=100, num=100, targetType='All')
focus = Skill('Focus', cost=50, type='ally: atk', info='Increase focus on the enemy, raising attack by 25 per use. Total attack boost is capped at 40.',
              baseNum=0, num=25, numCap=40, targetType='Self')
guardUp = Skill('Guard Up', cost=60, type='ally: def', info='Give Everyone Guard I for 10 turns.',
                            baseNum=0, num=0, targetType='All', applyEffect={guard:[0, 1, 10]})
slash_rage = Skill('Slash Rage', cost=70, ignoreDefense=True, type='opponent: hp', info='Lunge multiple slashes at the enemy! Dealing a good chunk of damage!', baseNum=150, repeatHowMany=3, useAnim=True, animType='Melee')

debuff_pierce = Skill('Debuff Pierce', cost=90, ignoreDefense=True, type='opponent: hp', info='Unleash a ray that pierces through all enemy! And debuff them with Confusion I for 2 cycles.', baseNum=80, useAnim=True, animType='Range', targetType='All', applyEffect={confusion:[2, 1]})

#bob = Opponent('Bob', 700, 700, 30, 10, 60, 0, 100, 100, 'A Simple Man Lol', {})
#sarah = Opponent('Sarah', 700, 700, 30, 10, 20, 0, 100, 100, 'A Simple Woman Lol', {})
#david = Opponent('David', 700, 700, 30, 10, 20, 0, 100, 100, 'A Simple Man Lol', {})
#hope = Opponent('Hope', 700, 700, 30, 10, 20, 0, 100, 100, 'A Simple Woman Lol', {})
opStat = [5, 5, 5, 5, 5]
lockEn = Opponent('Lock', 'Tank', '', [5, 3, 4, 1, 1, 1], setNum=[165, 30, 33, 8, 1, 1], fight=[punch], action=actions, info='Lock is never wrong. Well, at least that is what he thinks. His failure is not his fault, it is yours.', passiveBuff={lockedIn:[False, False]}, color=(255, 255, 0), skinList=['Default', 'Dark', 'Key Battler', 'Royal Blue', 'Rayson Swap'])
li_weiEn = Opponent('Li Wei', 'Melee', '', [4, 4, 2, 4, 1, 1], setNum=[125, 43, 13, 33, 1, 1], fight=[strike], action=actions, info='After losing his job, he instead decides to take part in a violent fighting game than actually finding a new one.', color=(255, 100, 0), skinList=['Default', 'Azure'])
blue_guyEn = Opponent('Blue Guy', 'Controller', '', [2, 5, 2, 5, 4, 4], setNum=[85, 47, 10, 38, 4, 1.25], fight=[spike], action=actions, skills=[blue_slash], info='Blue Guy is a competitive person. Mess with him and you may regret what you did.', color=(0, 0, 255))
raysonEn = Opponent('Rayson', 'Range', '', [1, 4, 2, 2, 5, 4], setNum=[70, 44, 18, 20, 5, 1.75], fight=[powerBullet], action=actions, info='Rayson is tired of how robots are being treated and one day plans to take over the world and treat humans the way robots were treated, workers that serve a purpose for the benefits of their creator.', passiveBuff={booster:[False, False], glitched:[False, False]}, color=(30, 250, 30), skinList=['Default', 'Really Red'])
calvyEn = Opponent('Calvy', 'Thrower', '', [1, 4, 3, 3, 3, 2], setNum=[56, 45, 29, 28, 2, 1.25], fight=[tasteThePaper], action=actions, skills=[fun_doodles], info='This young boy enjoys drawing a lot. You would expect kids his age to be playing and watching their tablets all day, but Calvy spents hours of his days doodling on the thousands of notebooks in his room.', color=(255, 112, 255), skinList=['Default', 'Inverted'])
finleyEn = Opponent('Finley', 'All rounder', '', [3, 4, 3, 3, 1, 2], setNum=[115, 42, 12, 30, 1, 1.25], fight=[cutStuff, knifeShot], action=actions, info='Being bullied and laughed at by everyone, Finley is certain that this world is just filled with horrible people. He plans to take down all his enemies one day, one by one, brutally.', passiveBuff={doubleStrike:[False, False]}, color=(255, 112, 210))
taphygrafyEn = Opponent('Taphygrafy', 'Support', '', [2, 1, 3, 4, 3, 4], setNum=[82, 10, 30, 32, 3, 1.75], fight=[fluffball], action=actions, skills=[fuzzy_encouragement], info='Taphygrafy is a fluffball of joy! With this fluffball, your day would definetly be much better!', color=(180, 180, 180))
ranyEn = Opponent('Rany', 'Support', '', [1, 2, 3, 2, 2, 5], setNum=[70, 28, 21, 18, 2, 2], fight=[pencilJab], level=1, action=actions, skills=[healing_orb], info='Is he a human or not? Why in the hell does he have a circular head and a weird blue hairstyle? Also, where did he even get that pencil', passiveBuff={regenTurn:[False, False]}, color=(255, 0, 0))
ochoEn = Opponent('Ocho', 'Controller', '', [0, 1, 0, 1, 1, 1], setNum=[53, 27, 12, 37, 3, 1.75], fight=[webBomb], action=actions, skills=[web_wrap], info='Trapping and slowing are no strangers to the amazing Ocho! He found out that he could make webs very quickly and he makes use of his new-found talent in battle.', color=(255, 0, 0))
rekety = Opponent('Rekety', 'Melee', '', [2, 4, 2, 4, 1, 1], setNum=[88, 48, 11, 32, 1, 1], fight=[watchYouBleed], action=actions,
info='Despite the things Rekety has achieved, he is never satisifed. Maybe one day, he will eventually find something that satisfy him.',
passiveBuff={iteker:[False, False]}, skinList=['Default', 'Rekverty', 'Red', 'Rektmas', 'Candy Cane', 'Rany Swap'], barColor=(101, 103, 255), color=(0, 0, 238))
dandeeEn = Opponent('Dandee', 'Range', '', [1, 5, 2, 2, 5, 4], setNum=[68, 65, 16, 20, 5, 1.75], fight=[blowballs], action=actions, info="Dandee may seem like a harmless dandelion but he is someone you wouldn't want to mess with. This sadistic dandelion is usually harmless, but when in the mood to kill, his blowballs become dangerous.", passiveBuff={sadism:[False, False], disperse:[False, False]}, color=(95, 255, 95))
copycatEn = Opponent('Copycat', 'All rounder', '', [3, 2, 2, 3, 2, 4], setNum=[120, 25, 14, 26, 2, 1.75], fight=[scratch], action=actions, skills=[copySkill], info='A fast learner and a master at shapeshifting, many suspect that Copycat is a creature from a planet far far away. Much is unknown about Copycat', color=(200, 50, 255))
red_dudeEn = Opponent('Red Dude', 'Melee', '', [2, 4, 2, 4, 1, 1], setNum=[92, 44, 16, 35, 1, 1], fight=[crimsonFang], action=actions, info="Unlike his brother, Blue Guy, Red Dude isn't as competitive. However, he a mischievous person.", passiveBuff={readyToStrike:[False, False]}, color=(220, 50, 50))
candaceEn = Opponent('Candace', 'Melee', '', [2, 4, 2, 4, 2, 2], setNum=[95, 41, 18, 31, 2, 1.25], fight=[winterWhack], skills=[cane_boost], action=actions,
info='Candace always feels jolly. To her everyday feels like Christmas. No one is changing her mind.',
skinList=["Default", "Cooling Winter"], color=(229, 39, 36))
Zephyr = Opponent('Zephyr', 'Range', '', [0, 0, 0, 0, 0, 0], setNum=[2500, 120, 40, 130, 2, 5], level=25, fight=[blastRay], action=actions, skills=[debuff_pierce], info='An entity corrupted by the Crown. Strangely, Rany shivers at this. What could both of them be hiding?', passiveBuff={}, color=(255, 0, 0))

skeleton = Opponent('Skeleton', 'Melee', '', [0, 0, 0, 0, 0, 0], setNum=[500, 70, 20, 252, 3, 2.3], fight=[swordSlash], action=actions,
info='A warrior who had lost his light.', scale=1.2, offsetY=20, weapon=boneSword, armour=darkArmour, inventory=[boneSword, darkArmour],
passiveBuff={}, skinList=['Default'], barColor=(101, 103, 255), color=(238, 238, 238))
darkArmour.use(skeleton, skeleton)
boneSword.use(skeleton, skeleton)
skeleton.inventory.clear()

lockEn = Opponent('Lock', 'Tank', '', [5, 3, 4, 1, 1, 1], setNum=[165, 30, 33, 8, 1, 1], fight=[punch], action=actions, info='Lock is never wrong. Well, at least that is what he thinks. His failure is not his fault, it is yours.', passiveBuff={lockedIn:[False, False]}, barColor=(255, 249, 133), color=(250, 197, 7), skinList=['Default', 'Dark', 'Key Battler', 'Royal Blue', 'Rayson Swap'])
li_weiEn = Opponent('Li Wei', 'Melee', '', [4, 4, 2, 4, 1, 1], setNum=[125, 43, 13, 33, 1, 1], fight=[strike], action=actions, info='After losing his job, he decides to take part in a violent fighting game instead of actually finding a new one.', barColor=(255, 207, 132), color=(255, 115, 0), skinList=['Default', 'Azure', 'Snowman'])
zee = Player('Zee', 'Melee', '', [-3, -2, -2, -3, 0, 0], setNum=[999, 999, 999, 999, 999, 999], maxMana=999, level=99, fight=[zeefight], action=actions, info='DHaiwn8372na0o!28dna82#%^&*(!jhs82728&*@*9d286*(*&^#":Hdjshsjdcx][}{POIhsjwu|[]13==', color=(100, 0, 0), skinList=['Default'])
blue_guyEn = Opponent('Blue Guy', 'Controller', '', [2, 4, 2, 4, 4, 2], setNum=[85, 47, 10, 38, 4, 1.25], fight=[spike], action=actions, canFly=True, skills=[blue_slash], info='Blue Guy is a competitive person who is the brother of Red Dude and cousin of Purple Kid. He was the leader of the Colourful 6, a team that has since disbanded, leaving only the three of them together.', barColor=(133, 134, 255), skinList=['Default', 'Egg Guy'], color=(1, 42, 254))
raysonEn = Opponent('Rayson', 'Range', '', [1, 4, 2, 2, 5, 4], setNum=[70, 44, 18, 20, 5, 1.75], fight=[powerBullet], action=actions, info='Rayson is tired of how robots are being treated and one day plans to take over the world and treat humans the way robots were treated, workers that serve a purpose for the benefits of their creator.', passiveBuff={booster:[False, False], glitched:[False, False]}, barColor=(138, 254, 133), color=(55, 254, 1), skinList=['Default', 'Static', 'Water Gun', 'Summer Blaster', 'Lock Swap'])
calvyEn = Opponent('Calvy', 'Thrower', '', [1, 4, 3, 3, 3, 2], setNum=[56, 45, 29, 28, 3, 1.25], fight=[tasteThePaper], action=actions,
skills=[fun_doodles], info="""This young boy enjoys drawing a lot. You would expect kids his age to be playing and watching their tablets all day, but Calvy spents hours of his days doodling on the thousands of notebooks in his room.""",
barColor=(255, 133, 238), color=(255, 1, 254), skinList=['Default', 'Inverted', 'Sandcastle', 'Sunny Builder'])
finleyEn = Opponent('Finley', 'All rounder', '', [3, 4, 3, 3, 1, 2], setNum=[115, 42, 12, 30, 1, 1.25], fight=[cutStuff, knifeShot], action=actions,
info='Being bullied and laughed at by everyone, Finley is certain that this world is just filled with horrible people. They plan to take down all their enemies one day, one by one, brutally.',
passiveBuff={doubleStrike:[False, False]}, barColor=(254, 132, 173), color=(255, 0, 118), skinList=["Default", "Option Two", "Red Vanity", "Blue Vanity"])
taphygrafyEn = Opponent('Taphygrafy', 'Support', '', [2, 1, 3, 4, 3, 4], setNum=[82, 10, 30, 32, 3, 1.75], fight=[fluffball], action=actions, skills=[fuzzy_encouragement], info='Taphygrafy is a fluffball of joy! With this fluffball, your day would definetly be much better!', barColor=(194, 194, 194), color=(128, 127, 128), skinList=['Default', 'Crazy April'])
ranyEn = Opponent('Rany', 'Support', '', [1, 2, 3, 2, 2, 5], setNum=[70, 28, 21, 18, 2, 2], fight=[pencilJab], level=1, action=actions, skills=[healing_orb], info='Is he a human or not? Why in the hell does he have a circular head and a weird blue hairstyle? Also, where did he even get that pencil', passiveBuff={regenTurn:[False, False]}, barColor=(219, 133, 133), color=(219, 0, 37), skinList=['Default', 'Inversed', 'Rekety Swap', 'Version B'])
ochoEn = Opponent('Ocho', 'Controller', '', [1, 2, 2, 4, 3, 4], setNum=[53, 27, 12, 37, 3, 1.75], fight=[webBomb], action=actions, skills=[web_wrap], info='Trapping and slowing are no strangers to the amazing Ocho! He found out that he could make webs very quickly and he makes use of his new-found talent in battle.', barColor=(130, 129, 129), color=(94, 93, 93), skinList=['Default', 'Brown', 'White', 'JPG'])
reketyEn = Opponent('Rekety', 'Melee', '', [2, 4, 2, 4, 1, 1], setNum=[88, 48, 11, 32, 1, 1], fight=[watchYouBleed], action=actions,
info='Despite the things Rekety has achieved, he is never satisifed. Maybe one day, he will eventually find something that satisfy him.',
passiveBuff={iteker:[False, False]}, skinList=['Default', 'Rekverty', 'Red', 'Rektmas', 'Candy Cane', 'Rany Swap'], barColor=(101, 103, 255), color=(0, 0, 238))
dandeeEn = Opponent('Dandee', 'Range', '', [1, 5, 2, 2, 5, 4], setNum=[68, 65, 16, 20, 5, 1.75], fight=[blowballs], action=actions, info="Dandee may seem like a harmless dandelion but he is someone you wouldn't want to mess with. This sadistic dandelion is usually harmless, but when in the mood to kill, his blowballs become dangerous.", passiveBuff={sadism:[False, False], disperse:[False, False]}, barColor=(112, 216, 113), color=(36, 216, 1), skinList=['Default', 'Bald'])
copycatEn = Opponent('Copycat', 'All rounder', '', [3, 2, 2, 3, 2, 4], setNum=[120, 25, 14, 26, 2, 1.75], fight=[scratch], action=actions, skills=[copySkill],
info='A fast learner and a master at shapeshifting, many suspect that Copycat is a creature from a planet far far away. Much is unknown about Copycat',
barColor=(214, 133, 255), color=(128, 0, 254), skinList=["Default", "Black"])
red_dudeEn = Opponent('Red Dude', 'Melee', '', [2, 4, 2, 4, 1, 1], setNum=[92, 44, 16, 35, 1, 1], fight=[crimsonFang], action=actions, info="Unlike his brother, Blue Guy, Red Dude isn't as competitive. However, he a mischievous person.", passiveBuff={readyToStrike:[False, False]}, barColor=(254, 133, 131), color=(254, 1, 38))

candaceEn = Opponent('Candace', 'Melee', '', [2, 4, 2, 4, 2, 2], setNum=[95, 41, 18, 31, 2, 1.25], fight=[winterWhack], skills=[cane_boost], action=actions,
info='Candace always feels jolly. To her everyday feels like Christmas. No one is changing her mind.',
skinList=["Default", "Cooling Winter"], barColor=(255, 152, 151), color=(229, 39, 36))

thinEn = Opponent('Thin', 'Challenge', '', [1, 1, 1, 1, 1, 1], setNum=[50, 10, 0, 1, 1, 1], fight=[weakPoke], action=actions,
info='Thin? Why are you here and who signed you up to play? Only play this rumbler if you want a challenge.', passiveBuff={productivityZero:[False, False]},
skinList=["Default", "Light Mode", "Thinbrella", "Thinner", "Post-it", "Thick"], barColor=(82, 82, 82), color=(36, 36, 36))

mr_grafyEn = Opponent('Mr Grafy', 'All rounder', '', [2, 2, 3, 2, 3, 4], setNum=[87, 27, 30, 12, 3, 1.75], fight=[hotTea], skills=[coffee_charge], action=actions,
info='A warm cup of tea or coffee is enough to fuel Mr Grafy through his day',
skinList=["Default"], barColor=(82, 82, 82), color=(194, 114, 31))

jam_jarEn = Opponent('Jam Jar', 'Tank', '', [4, 4, 4, 1, 1, 1], setNum=[148, 46, 31, 10, 1, 1], fight=[doubleFistBash], skills=[lid_off], action=actions,
info="Jam Jar knows when's the time to lid off.",
skinList=["Default", "Peanut Butter"], barColor=(190, 27, 52), color=(190, 27, 52))

screamyEn = Opponent('Screamy', 'Controller', '', [3, 2, 2, 4, 3, 2], setNum=[113, 29, 11, 17, 3, 1.25], fight=[scream], skills=[screamer], action=actions,
info="He screams. He floats. He's everything your ears fear.", canFly = True, flyRange=5,
skinList=["Default", "Unpixel", "Depressed"], barColor=(190, 27, 52), color=(255, 0, 0))

caenEn = Opponent('Caen', 'Support', '', [2, 2, 2, 4, 3, 4], setNum=[99, 28, 15, 32, 3, 1.75], fight=[sharpCane], action=actions, canFly=True,
info='Caen was brought to life by Candace using the combined powers of the Christmas spirit and a Life Cube.', passiveBuff={caneHealing:[False, False]},
skinList=["Default", "Chill Days", "Festive Feeling"], barColor=(190, 27, 52), color=(229, 39, 36))

purple_kidEn = Opponent('Purple Kid', 'Thrower', '', [2, 4, 2, 4, 4, 2], setNum=[89, 49, 16, 32, 4, 1.75], fight=[purplePower], action=actions,
info='Purple Kid, the cousin of Blue Guy and Red Dude, is the most logical of the trio. However, in battle, she becomes relentless in her pursuit of victory, sometimes even forgetting about logic altogether.',
skinList=["Default"], barColor=(190, 27, 52), color=(128, 0, 254))

loconEn = Opponent('Locon', 'Support', '', [2, 2, 2, 4, 2, 4], setNum=[95, 25, 20, 32, 2, 1.75], fight=[sliceTime], skills=[hot_and_ready], action=actions,
info='Locon loves making and sharing pizza, using his skills to support allies while slicing through enemies with his trusty pizza cutter.',
skinList=["Default", "Dimensional", "Bacon Hair", "Bacon Shift"], barColor=(190, 27, 52), color=(229, 0, 35))

t_musicEn = Opponent('T Music', 'Support', '', [2, 2, 2, 4, 2, 4], setNum=[95, 25, 20, 32, 2, 1.75], fight=[melodyBurst], action=actions,
info='T Music, short for Taphygrafy Music (not to be confused with Taphygrafy), is a fluffball who loves playing the piano and sharing his tunes with everyone.',
passiveBuff={healingTunes:[False, False]}, skinList=["Default"], barColor=(190, 27, 52), color=(58, 230, 0), offsetX=35)

blue_blackEn = Opponent('Blue-Black', 'Tank', '', [4, 4, 4, 1, 1, 1], setNum=[148, 47, 31, 5, 1, 1], fight=[knockback], action=actions,
info="Formerly known as Green Boy, Blue-Black left the Colourful 6 to use his powers for his own gain, even lying to make his escape. Now the arch-rival of Blue Guy, he's fast, but his habit of admiring himself often slows him down drastically.",
skinList=["Default", "Too Cool"], barColor=(190, 27, 52), color=(56, 242, 0))

orange_girlEn = Opponent('Orange Girl', 'Range', '', [2, 4, 1, 3, 4, 4], setNum=[87, 42, 9, 29, 4, 1.75], fight=[threeShot], skills=[orange_blast], action=actions,
info='Orange Girl was a former member of the Colourful 6 but left due to personal reasons. Despite her departure, she parted on good terms with the rest of the team, leaving behind no hard feelings.',
skinList=["Default"], barColor=(190, 27, 52), color=(254, 90, 0))

fourmintiEn = Opponent('4minti', 'Range', '', [2, 4, 2, 2, 4, 4], setNum=[92, 40, 19, 15, 4, 1.75], fight=[_4ero4rm], skills=[he4dshot], action=actions,
info="Wh4t is 4minti? Wh4t's up with the number four?",
skinList=["Default", "Inverted"], barColor=(190, 27, 52), color=(1, 241, 197))

yellow_sparkEn = Opponent('Yellow Spark', 'Support', '', [2, 2, 2, 4, 4, 4], setNum=[82, 28, 13, 34, 4, 1.75], fight=[solarDart], skills=[spark_charge], action=actions,
info='A former Colourful 6 member who left to chase bigger dreams. Rumours say she dated Blue-Black, the current status of their relationship remains a mystery.',
skinList=["Default"], barColor=(190, 27, 52), color=(254, 254, 0))

gregleyEn = Opponent('Gregley', 'Thrower', '', [1, 4, 5, 3, 3, 1], setNum=[59, 42, 48, 27, 3, 1], fight=[hornLaunch], skills=[], action=actions,
info="Gregley appears to come from a strange and weird world. Though he is Gracie's father, she always seems to avoid him, no one really knows why.",
skinList=["Default", "Purple"], barColor=(190, 27, 52), color=(0, 254, 0), canFly=True, flyType=1, flyRange=10)

rumbleyEn = Opponent('Rumbley', 'All rounder', '', [3, 3, 3, 3, 3, 2], setNum=[112, 35, 25, 26, 3, 1.25], fight=[knuckleDash], action=actions,
info="Rumbley wasn't invited to the games, they were made for them. As the mascot of Intense Rumble, Rumbley isn't afraid to interact with the other rumblers. Originally just a mascot, they ended up becoming a rumbler, proving they're more than that.",
skinList=["Default"], barColor=(190, 27, 52), color=(158, 0, 254), beSelectOnce=False, passiveBuff={weAreRumbley:[False, False]})

blueberryEn = Opponent('Blueberry', 'Controller', '', [2, 3, 1, 5, 4, 2], setNum=[89, 34, 2, 42, 4, 1.25], fight=[annoyingHacks], skills=[god_mode], action=actions,
info="Blueberry used to be unstoppable, until the anti-cheat kicked in. Now he's just a cheater with nerfed hacks.",
skinList=["Default", "Job Application", "Noob", "Inverted Noob"], barColor=(190, 27, 52), color=(1, 122, 242))

adv_grafyEn = Player('Adv-Grafy', 'Melee', '', [2, 4, 2, 4, 1, 2], setNum=[88, 42, 18, 38, 1, 1.25], fight=[adventureSword], action=actions,
info='Adv-Grafy, short for Adventure-Grafy, is a curious fluffball who is constantly seeking fun, thrills, and a brand new adventure.',
barColor=(255, 207, 132), color=(255, 0, 0), skinList=['Default'])

validEnemy = [lockEn, li_weiEn, blue_guyEn, raysonEn, calvyEn, finleyEn, taphygrafyEn, ranyEn, ochoEn, reketyEn, dandeeEn, copycatEn, red_dudeEn, candaceEn, thinEn,
              mr_grafyEn, jam_jarEn, screamyEn, caenEn, purple_kidEn, loconEn, t_musicEn, blue_blackEn, orange_girlEn, fourmintiEn, yellow_sparkEn, gregleyEn,
              rumbleyEn, blueberryEn, adv_grafyEn]


lock = Player('Lock', 'Tank', '', [5, 3, 4, 1, 1, 1], setNum=[165, 30, 33, 8, 1, 1], fight=[punch], action=actions, info='Lock is never wrong. Well, at least that is what he thinks. His failure is not his fault, it is yours.', passiveBuff={lockedIn:[False, False]}, barColor=(255, 249, 133), color=(250, 197, 7), skinList=['Default', 'Dark', 'Key Battler', 'Royal Blue', 'Rayson Swap'])
li_wei = Player('Li Wei', 'Melee', '', [4, 4, 2, 4, 1, 1], setNum=[125, 43, 13, 33, 1, 1], fight=[strike], action=actions, info='After losing his job, he decides to take part in a violent fighting game instead of actually finding a new one.', barColor=(255, 207, 132), color=(255, 115, 0), skinList=['Default', 'Azure', 'Snowman'])
zee = Player('Zee', 'Melee', '', [-3, -2, -2, -3, 0, 0], setNum=[999, 999, 999, 999, 999, 999], maxMana=999, level=99, fight=[zeefight], action=actions, info='DHaiwn8372na0o!28dna82#%^&*(!jhs82728&*@*9d286*(*&^#":Hdjshsjdcx][}{POIhsjwu|[]13==', color=(100, 0, 0), skinList=['Default'])
blue_guy = Player('Blue Guy', 'Controller', '', [2, 4, 2, 4, 4, 2], setNum=[85, 47, 10, 38, 4, 1.25], fight=[spike], action=actions, canFly=True, skills=[blue_slash], info='Blue Guy is a competitive person who is the brother of Red Dude and cousin of Purple Kid. He was the leader of the Colourful 6, a team that has since disbanded, leaving only the three of them together.', barColor=(133, 134, 255), skinList=['Default', 'Egg Guy'], color=(1, 42, 254))
rayson = Player('Rayson', 'Range', '', [1, 4, 2, 2, 5, 4], setNum=[70, 44, 18, 20, 5, 1.75], fight=[powerBullet], action=actions, info='Rayson is tired of how robots are being treated and one day plans to take over the world and treat humans the way robots were treated, workers that serve a purpose for the benefits of their creator.', passiveBuff={booster:[False, False], glitched:[False, False]}, barColor=(138, 254, 133), color=(55, 254, 1), skinList=['Default', 'Static', 'Water Gun', 'Summer Blaster', 'Lock Swap'])
calvy = Player('Calvy', 'Thrower', '', [1, 4, 3, 3, 3, 2], setNum=[56, 45, 29, 28, 3, 1.25], fight=[tasteThePaper], action=actions,
skills=[fun_doodles], info="""This young boy enjoys drawing a lot. You would expect kids his age to be playing and watching their tablets all day, but Calvy spents hours of his days doodling on the thousands of notebooks in his room.""",
barColor=(255, 133, 238), color=(255, 1, 254), skinList=['Default', 'Inverted', 'Sandcastle', 'Sunny Builder'])
finley = Player('Finley', 'All rounder', '', [3, 4, 3, 3, 1, 2], setNum=[115, 42, 12, 30, 1, 1.25], fight=[cutStuff, knifeShot], action=actions,
info='Being bullied and laughed at by everyone, Finley is certain that this world is just filled with horrible people. They plan to take down all their enemies one day, one by one, brutally.',
passiveBuff={doubleStrike:[False, False]}, barColor=(254, 132, 173), color=(255, 0, 118), skinList=["Default", "Option Two", "Red Vanity", "Blue Vanity"])
taphygrafy = Player('Taphygrafy', 'Support', '', [2, 1, 3, 4, 3, 4], setNum=[82, 10, 30, 32, 3, 1.75], fight=[fluffball], action=actions, skills=[fuzzy_encouragement], info='Taphygrafy is a fluffball of joy! With this fluffball, your day would definetly be much better!', barColor=(194, 194, 194), color=(128, 127, 128), skinList=['Default', 'Crazy April'])
rany = Player('Rany', 'Support', '', [1, 2, 3, 2, 2, 5], setNum=[70, 28, 21, 18, 2, 2], fight=[pencilJab], level=1, action=actions, skills=[healing_orb], info='Is he a human or not? Why in the hell does he have a circular head and a weird blue hairstyle? Also, where did he even get that pencil', passiveBuff={regenTurn:[False, False]}, barColor=(219, 133, 133), color=(219, 0, 37), skinList=['Default', 'Inversed', 'Rekety Swap', 'Version B'])
ocho = Player('Ocho', 'Controller', '', [1, 2, 2, 4, 3, 4], setNum=[53, 27, 12, 37, 3, 1.75], fight=[webBomb], action=actions, skills=[web_wrap], info='Trapping and slowing are no strangers to the amazing Ocho! He found out that he could make webs very quickly and he makes use of his new-found talent in battle.', barColor=(130, 129, 129), color=(94, 93, 93), skinList=['Default', 'Brown', 'White', 'JPG'])
rekety = Player('Rekety', 'Melee', '', [2, 4, 2, 4, 1, 1], setNum=[88, 48, 11, 32, 1, 1], fight=[watchYouBleed], action=actions,
info='Despite the things Rekety has achieved, he is never satisifed. Maybe one day, he will eventually find something that satisfy him.',
passiveBuff={iteker:[False, False]}, skinList=['Default', 'Rekverty', 'Red', 'Rektmas', 'Candy Cane', 'Rany Swap'], barColor=(101, 103, 255), color=(0, 0, 238))
dandee = Player('Dandee', 'Range', '', [1, 5, 2, 2, 5, 4], setNum=[68, 65, 16, 20, 5, 1.75], fight=[blowballs], action=actions, info="Dandee may seem like a harmless dandelion but he is someone you wouldn't want to mess with. This sadistic dandelion is usually harmless, but when in the mood to kill, his blowballs become dangerous.", passiveBuff={sadism:[False, False], disperse:[False, False]}, barColor=(112, 216, 113), color=(36, 216, 1), skinList=['Default', 'Bald'])
copycat = Player('Copycat', 'All rounder', '', [3, 2, 2, 3, 2, 4], setNum=[120, 25, 14, 26, 2, 1.75], fight=[scratch], action=actions, skills=[copySkill],
info='A fast learner and a master at shapeshifting, many suspect that Copycat is a creature from a planet far far away. Much is unknown about Copycat',
barColor=(214, 133, 255), color=(128, 0, 254), skinList=["Default", "Black"])
red_dude = Player('Red Dude', 'Melee', '', [2, 4, 2, 4, 1, 1], setNum=[92, 44, 16, 35, 1, 1], fight=[crimsonFang], action=actions, info="Unlike his brother, Blue Guy, Red Dude isn't as competitive. However, he a mischievous person.", passiveBuff={readyToStrike:[False, False]}, barColor=(254, 133, 131), color=(254, 1, 38))

candace = Player('Candace', 'Melee', '', [2, 4, 2, 4, 2, 2], setNum=[95, 41, 18, 31, 2, 1.25], fight=[winterWhack], skills=[cane_boost], action=actions,
info='Candace always feels jolly. To her everyday feels like Christmas. No one is changing her mind.',
skinList=["Default", "Cooling Winter"], barColor=(255, 152, 151), color=(229, 39, 36))

thin = Player('Thin', 'Challenge', '', [1, 1, 1, 1, 1, 1], setNum=[50, 10, 0, 1, 1, 1], fight=[weakPoke], action=actions,
info='Thin? Why are you here and who signed you up to play? Only play this rumbler if you want a challenge.', passiveBuff={productivityZero:[False, False]},
skinList=["Default", "Light Mode", "Thinbrella", "Thinner", "Post-it", "Thick"], barColor=(82, 82, 82), color=(36, 36, 36))

mr_grafy = Player('Mr Grafy', 'All rounder', '', [2, 2, 3, 2, 3, 4], setNum=[87, 27, 30, 12, 3, 1.75], fight=[hotTea], skills=[coffee_charge], action=actions,
info='A warm cup of tea or coffee is enough to fuel Mr Grafy through his day',
skinList=["Default"], barColor=(82, 82, 82), color=(194, 114, 31))

jam_jar = Player('Jam Jar', 'Tank', '', [4, 4, 4, 1, 1, 1], setNum=[148, 46, 31, 10, 1, 1], fight=[doubleFistBash], skills=[lid_off], action=actions,
info="Jam Jar knows when's the time to lid off.",
skinList=["Default", "Peanut Butter"], barColor=(190, 27, 52), color=(190, 27, 52))

screamy = Player('Screamy', 'Controller', '', [3, 2, 2, 4, 3, 2], setNum=[113, 29, 11, 17, 3, 1.25], fight=[scream], skills=[screamer], action=actions,
info="He screams. He floats. He's everything your ears fear.", canFly = True, flyRange=5,
skinList=["Default", "Unpixel", "Depressed"], barColor=(190, 27, 52), color=(255, 0, 0))

caen = Player('Caen', 'Support', '', [2, 2, 2, 4, 3, 4], setNum=[99, 28, 15, 32, 3, 1.75], fight=[sharpCane], action=actions, canFly=True,
info='Caen was brought to life by Candace using the combined powers of the Christmas spirit and a Life Cube.', passiveBuff={caneHealing:[False, False]},
skinList=["Default", "Chill Days", "Festive Feeling"], barColor=(190, 27, 52), color=(229, 39, 36))

purple_kid = Player('Purple Kid', 'Thrower', '', [2, 4, 2, 4, 4, 2], setNum=[89, 49, 16, 32, 4, 1.75], fight=[purplePower], action=actions,
info='Purple Kid, the cousin of Blue Guy and Red Dude, is the most logical of the trio. However, in battle, she becomes relentless in her pursuit of victory, sometimes even forgetting about logic altogether.',
skinList=["Default"], barColor=(190, 27, 52), color=(128, 0, 254))

locon = Player('Locon', 'Support', '', [2, 2, 2, 4, 2, 4], setNum=[95, 25, 20, 32, 2, 1.75], fight=[sliceTime], skills=[hot_and_ready], action=actions,
info='Locon loves making and sharing pizza, using his skills to support allies while slicing through enemies with his trusty pizza cutter.',
skinList=["Default", "Dimensional", "Bacon Hair", "Bacon Shift"], barColor=(190, 27, 52), color=(229, 0, 35))

t_music = Player('T Music', 'Support', '', [2, 2, 2, 4, 2, 4], setNum=[95, 25, 20, 32, 2, 1.75], fight=[melodyBurst], action=actions,
info='T Music, short for Taphygrafy Music (not to be confused with Taphygrafy), is a fluffball who loves playing the piano and sharing his tunes with everyone.',
passiveBuff={healingTunes:[False, False]}, skinList=["Default"], barColor=(190, 27, 52), color=(58, 230, 0), offsetX=35)

blue_black = Player('Blue-Black', 'Tank', '', [4, 4, 4, 1, 1, 1], setNum=[148, 47, 31, 5, 1, 1], fight=[knockback], action=actions,
info="Formerly known as Green Boy, Blue-Black left the Colourful 6 to use his powers for his own gain, even lying to make his escape. Now the arch-rival of Blue Guy, he's fast, but his habit of admiring himself often slows him down drastically.",
skinList=["Default", "Too Cool"], barColor=(190, 27, 52), color=(56, 242, 0))

orange_girl = Player('Orange Girl', 'Range', '', [2, 4, 1, 3, 4, 4], setNum=[87, 42, 9, 29, 4, 1.75], fight=[threeShot], skills=[orange_blast], action=actions,
info='Orange Girl was a former member of the Colourful 6 but left due to personal reasons. Despite her departure, she parted on good terms with the rest of the team, leaving behind no hard feelings.',
skinList=["Default"], barColor=(190, 27, 52), color=(254, 90, 0))

fourminti = Player('4minti', 'Range', '', [2, 4, 2, 2, 4, 4], setNum=[92, 40, 19, 15, 4, 1.75], fight=[_4ero4rm], skills=[he4dshot], action=actions,
info="Wh4t is 4minti? Wh4t's up with the number four?",
skinList=["Default", "Inverted"], barColor=(190, 27, 52), color=(1, 241, 197))

yellow_spark = Player('Yellow Spark', 'Support', '', [2, 2, 2, 4, 4, 4], setNum=[82, 28, 13, 34, 4, 1.75], fight=[solarDart], skills=[spark_charge], action=actions,
info='A former Colourful 6 member who left to chase bigger dreams. Rumours say she dated Blue-Black, the current status of their relationship remains a mystery.',
skinList=["Default"], barColor=(190, 27, 52), color=(254, 254, 0))

gregley = Player('Gregley', 'Thrower', '', [1, 4, 5, 3, 3, 1], setNum=[59, 42, 48, 27, 3, 1], fight=[hornLaunch], skills=[], action=actions,
info="Gregley appears to come from a strange and weird world. Though he is Gracie's father, she always seems to avoid him, no one really knows why.",
skinList=["Default", "Purple"], barColor=(190, 27, 52), color=(0, 254, 0), canFly=True, flyType=1, flyRange=10)

rumbley = Player('Rumbley', 'All rounder', '', [3, 3, 3, 3, 3, 2], setNum=[112, 35, 25, 26, 3, 1.25], fight=[knuckleDash], action=actions,
info="Rumbley wasn't invited to the games, they were made for them. As the mascot of Intense Rumble, Rumbley isn't afraid to interact with the other rumblers. Originally just a mascot, they ended up becoming a rumbler, proving they're more than that.",
skinList=["Default"], barColor=(190, 27, 52), color=(158, 0, 254), beSelectOnce=False, passiveBuff={weAreRumbley:[False, False]})

blueberry = Player('Blueberry', 'Controller', '', [2, 3, 1, 5, 4, 2], setNum=[89, 34, 2, 42, 4, 1.25], fight=[annoyingHacks], skills=[god_mode], action=actions,
info="Blueberry used to be unstoppable, until the anti-cheat kicked in. Now he's just a cheater with nerfed hacks.",
skinList=["Default", "Job Application", "Noob", "Inverted Noob"], barColor=(190, 27, 52), color=(1, 122, 242))

adv_grafy = Player('Adv-Grafy', 'Melee', '', [2, 4, 2, 4, 1, 2], setNum=[88, 42, 18, 38, 1, 1.25], fight=[adventureSword], action=actions,
info='Adv-Grafy, short for Adventure-Grafy, is a curious fluffball who is constantly seeking fun, thrills, and a brand new adventure.',
barColor=(255, 207, 132), color=(255, 0, 0), skinList=['Default'])



validAlly = [lock, li_wei, blue_guy, rayson, calvy, finley, taphygrafy, rany, ocho, rekety, dandee, copycat, red_dude, candace, thin, mr_grafy, jam_jar,
             screamy, caen, purple_kid, locon, t_music, blue_black, orange_girl, fourminti, yellow_spark, gregley, rumbley, blueberry, adv_grafy]
inventory = [hpPot, hpPot, hpPot, attackPill, defensePill, hpElixer, soulCube]
for i in validAlly:
    i.inventory = inventory
einventory = [hpPot, hpPot, hpPot]
for i in validEnemy:
    i.inventory = einventory

# HP, ATTACK, DEFENSE, SPEED, PROD
#zr = Player('Zr', 'Thrower', '', [2, 4, 1, 4, 0], 20, 20, 10, 0, 21, 1, 0, phone, helmet, 1, 0, [], [redHalos, sword, helmet], actions, [blast, strikeDown, concussion], 'Neutral', 'He is a gamer and stuff.', {}, (255, 255, 255))
#squarey = Player('Squarey', 'Melee', '', [20, 4, 1, 4, 9, 0],  20, 20, 10, 0, 18, 1, 0, bat, helmet, 1, 0, [], [milk, milk, milk, ___], actions, [regen, dualHeal, constantRegen], 'Neutral', 'Loves food apparently.', {}, (0, 182, 255))
#rany = Player('Rany', 'Melee', '', [1, 1, 1, 1, 1],  20, 20, 10, 0, 15, 1, 0, bat, helmet, 1, 0, [], [milk, milk, milk, milk, bat, phone, helmet, sword, staff, redHalos, redCloak], actions, [regen, dualHeal, constantRegen], 'Neutral', 'The weakest human', {}, (255, 40, 40))
#rekety = Player('Rekety', 'Melee', '', [3, 5, 2, 3, 1], 20, 20, 10, 0, 21, 1, 0, sword, helmet, 1, 0, [], [milk, milk, milk], actions, [bleedStrike, rage, shieldUp], 'Neutral', 'Why is he wielding a sickle?', {}, (26, 46, 247))
#mei = Player('Mei', 'Magic', '', [2, 5, 2, 5, 4], 20, 20, 10, 0, 22, 1, 0, staff, helmet, 1, 0, [], [milk, milk, milk], actions, [blast, attackDown, revive], 'Neutral', 'A powerful stickfigure who was formerly influential.', {}, (183, 183, 183))
allerwaveEn = Opponent('Allerwave', 'Melee', '', [200, 200, 0, 300, 3, 30], setNum=[200, 200, 200, 0, 200, 200], fight=[pencilJab], weapon=redHalos,
                   armour=redCloak, action=actions, skills=[statUp, statDown, allBuff],
                   info='One of the creator of this world, the one who program everything. Normally chill but will be livid if he enconters a bug.',
                   color=(255, 50, 50))
allerwave = Player('Allerwave', 'Melee', '', [200, 200, 0, 0, 3, 30], setNum=[200, 30, 0, 10, 10, 2], fight=[pencilJab], weapon=redHalos,
                   armour=noArmour, action=actions, skills=[statUp, statDown, allBuff, hitAll],
                   info='One of the creator of this world, the one who program everything. Normally chill but will be livid if he enconters a bug.', barColor=(185, 43, 43),
                   color=(153, 38, 30), canFly=False, flyRange=25)

the_creator = Player('The Creator', 'Melee', '', [200, 200, 0, 0, 3, 30], setNum=[200, 200, 0, 10, 10, 2], fight=[watchYouBleed], weapon=noWeapon,
                   armour=noArmour, action=actions, skills=[statUp, statDown, allBuff, hitAll],
                   info='One of the creator of this world, the one who direct it all. The illustrator and writer behind this world.', barColor=(0, 0, 0),
                   color=(255, 255, 255))

the_creatorEn = Opponent('The Creator', 'Melee', '', [200, 200, 0, 0, 3, 30], setNum=[200, 2763, 200, 200, 200, 200], fight=[watchYouBleed], weapon=redHalos,
                   armour=redCloak, action=actions, skills=[statUp, statDown, allBuff, hitAll],
                   info='One of the creator of this world, the one who direct it all. The illustrator and writer behind this world.',
                   color=(0, 0, 0))

#validAlly += [allerwave, the_creator]

#party = [zr, rany, mei, squarey, rekety]
#party = [zr, squarey, rekety, mei]
#party = [lock, blue_guy, li_wei]
#party = [allerwave]#, blue_guy, rayson]
#party = [zr, zr, zr]
#party = [zr, rany, squarey]
#opponent = [bob, sarah, david]
#party = [allerwave, lock, li_wei, squarey]
#opponent = [calvyEn, raysonEn, li_weiEn]
#validEnemy.append(squareyEn)
opponent = [Zephyr]#, allerwave]
party = [rany, rekety]

items = []
skillAnim = []
slash = []
bash = []
proj = []
magic = []
for i in range(1,11):
    if i < 7:
        skillAnim.append(f'attackAnimate/skill/skill{i}.png')
    if i < 9:
        slash.append(f'attackAnimate/slice/slice{i}.png')
    if i < 10:
        bash.append(f'attackAnimate/bash/bash{i}.png')
    magic.append(f'attackAnimate/magic/magic{i}.png')
    proj.append(f'attackAnimate/range/range{i}.png')


items = []
skills = []
def what():
    global items
    for varName, varValue in globals().items():
        if isinstance(varValue, Item):
            items.append(globals()[varName])

        elif isinstance(varValue, Skill):
            skills.append(globals()[varName])

what()

for i in party:
    i.levelUp(0)
