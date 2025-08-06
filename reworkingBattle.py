import json
import random
import json
import os
import sys
import pygame
#import pygame.gfxdraw
import math
from screenWindow import useWeb, achievementObj, scaleFactor, DynamicMusicPlayer, sprites, loadSprite, draw, updateTween, loadAnimatedSprite, animatedSprites, updateAnimation, playAnimation, useTexture, loadImg
import screenWindow
import character
from character import fightObj, skillObj, actObj, itemObj, playerObj, opponentObj
import string
import io
import os
import time as Time
import copy
import colorsys
import asyncio
#from pyo import *
#from pygame._sdl2 import Texture



#import numpy as np


# Starts up the "game" window
pygame.init()
# Starts up the audio system
pygame.mixer.init()
pygame.mixer.set_num_channels(64)

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 0)



inf = float('inf')

width = screenWindow.width
height = screenWindow.height

widthy = screenWindow.widthy#640
heighty = screenWindow.heighty#448

screen = screenWindow.screen
window = screenWindow.window
hud = screenWindow.hud
ringThing = pygame.Surface((width,height), pygame.SRCALPHA)
backGroundScreen = screenWindow.backGroundScreen
final = pygame.Surface((width,height), pygame.SRCALPHA)

soundVolume = screenWindow.soundVolume # Dictates Sound Volume
musicVolume = screenWindow.musicVolume # Dictates Music Volume


baseImg = screenWindow.baseImg
images = screenWindow.images
textures = screenWindow.textures
renderTexture = screenWindow.renderTexture
texts = screenWindow.texts
shapes = screenWindow.shapes


party = character.party
opponent = character.opponent

for i in party:
    if i.name == 'Dandee':
        i.skin = 'Alt'

for i in opponent:
    if i.name == 'Dandee':
        i.skin = 'Alt'

clock = screenWindow.clock #Starts up the FPS

useDefensePercent = True

def getVar(varName):
    return globals()[varName]
def setVar(varName, value):
    globals()[varName] = value

def debug_test(surface):
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface
    #print("fnction-scope #print is alive!")

drawRect, drawRing, drawCircle = screenWindow.drawRect, screenWindow.drawRing, screenWindow.drawCircle
scaleObj = screenWindow.scaleObj
loadImg = screenWindow.loadImg
render_text = screenWindow.render_text
rotateObj = screenWindow.rotateObj
blitObj = screenWindow.blitObj
soundCache = {}

    
# Function to play sound
def playSound(name, volume=1, doLoop=False):
    if name not in soundCache:
        soundCache[name] = pygame.mixer.Sound(f'sounds/{name}') # Loads in the sound from the sounds folder
    sound = soundCache[name]
    sound.set_volume(screenWindow.soundVolume*volume) # Sets the sound volume based off user current sound volume
    if doLoop:
        sound.play(loops=-1)
    else:
        sound.play() # Plays the sound

def screenBlit(finalscreen):  # clear window
    global width, height, renderTexture
    width, height = screenWindow.width, screenWindow.height
    #deltaTime = clock.get_time() / 1000

    screen.update(theDelta)
    hud.update(theDelta)
    backGroundScreen.update(theDelta)

    backGroundScreen.render_to(window)
    screen.render_to(window)
    hud.render_to(window)
    hud.clear((100, 0, 0, 0))
    screen.clear((100, 0, 0, 0))
    if screenWindow.useWeb == False:
        screenWindow.renderer.present()
        #pygame.display.flip()
        screenWindow.renderer.draw_color= ((255, 255, 255, 0))
        #screenWindow.renderer.clear()
    else:
        pygame.display.flip()


# Function to set the camera
def camSet(zoom, color, fade, shake):

    # Essentitals camera related variables to make global
    global camZoom
    global camColor
    global camFade
    global camShake

    # Set the camera variables
    camZoom = zoom # Set the camera zoom to the given zoom
    camColor = color # Set the camera color to the given color
    camFade = fade # Set the camera fade to the given fade
    camShake = shake # Set the camera shake to the given shake
import re
def other_render_text(text, color, size, border=False, border_color=(0, 0, 0), border_thickness=1, angle=0, frame=0):
    global texts
    key = f"{text}|{color}|{size}|{border}|{border_color}|{border_thickness}|{angle}|{frame}"

    if key in texts:
        return texts[key]

    font = pygame.font.Font("gameFont.otf", int(size * scaleFactor * 0.9))
    border_thickness = round(border_thickness * scaleFactor)

    if text.strip() == "":
        text = " "

    # Tag parsing setup
    color_stack = [color]
    effect_stack = []
    x_offset = 0
    char_surfaces = []

    tokens = re.findall(r'\[\#?[a-zA-Z0-9]+\]|\[\/\#?[a-zA-Z0-9]+\]|.', text)

    for i, token in enumerate(tokens):
        if token.startswith('[#') and token.endswith(']'):
            hex_color = token[2:-1]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            color_stack.append(rgb)
            continue
        elif token.startswith('[/#') and token.endswith(']'):
            if len(color_stack) > 1:
                color_stack.pop()
            continue
        elif token == '[shake]':
            effect_stack.append('shake')
            continue
        elif token == '[/shake]':
            if 'shake' in effect_stack:
                effect_stack.remove('shake')
            continue
        elif token == '[snake]':
            effect_stack.append('snake')
            continue
        elif token == '[/snake]':
            if 'snake' in effect_stack:
                effect_stack.remove('snake')
            continue
        elif token.startswith('[') and token.endswith(']'):
            continue  # ignore unknown tags

        current_color = color_stack[-1]
        char_surface = font.render(token, True, current_color).convert_alpha()

        if border:
            bordered = pygame.Surface(
                (char_surface.get_width() + 2 * border_thickness,
                 char_surface.get_height() + 2 * border_thickness),
                pygame.SRCALPHA)

            for dx in range(-border_thickness, border_thickness + 1):
                for dy in range(-border_thickness, border_thickness + 1):
                    if dx != 0 or dy != 0:
                        shadow = font.render(token, True, border_color).convert_alpha()
                        bordered.blit(shadow, (dx + border_thickness, dy + border_thickness))

            bordered.blit(char_surface, (border_thickness, border_thickness))
            char_surface = bordered

        # Animation (shake/snake) applied here
        offset_x, offset_y = 0, 0
        if 'shake' in effect_stack:
            offset_x += random.randint(-1, 1)*scaleFactor
            offset_y += random.randint(0, 3)*scaleFactor
        if 'snake' in effect_stack:
            offset_y += int(math.sin(((frame + i*3)/15) * 2 * math.pi ) * 4)

        char_surfaces.append((char_surface, x_offset + offset_x, offset_y))
        x_offset += char_surface.get_width()

    # Determine final surface size
    width = max([x + surf.get_width() for surf, x, y in char_surfaces]) if char_surfaces else 1
    height = max([surf.get_height() + y for surf, x, y in char_surfaces]) if char_surfaces else 1
    final_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for surf, x, y in char_surfaces:
        final_surface.blit(surf, (x, y))

    if angle != 0:
        final_surface = pygame.transform.rotate(final_surface, angle)

    texts[key] = final_surface
    return final_surface

def battleText(usePotrait=False, name=None, forceDo=False, emotion=None):
    global splashy
    global text_index
    global textBox

    font_size = 40
    font = pygame.font.Font("gameFont.otf", int(font_size * 0.9))
    maximum = hudRect[2] - 2 * hudRect[6] - 40

    if name is None:
        usePotrait = False
    if usePotrait:
        maximum -= 140

    # ===== Step 1: Tokenize input text (BBCode-like tags)
    def tokenize_rich_text(text):
        tag_pattern = re.compile(r'\[/?\#?[a-zA-Z0-9]+\]')
        tokens = []
        pos = 0
        for match in tag_pattern.finditer(text):
            if match.start() > pos:
                tokens.extend(list(text[pos:match.start()]))
            tokens.append(match.group())
            pos = match.end()
        if pos < len(text):
            tokens.extend(list(text[pos:]))
        return tokens

    def reconstruct_text_upto(tokens, visible_count):
        result = []
        open_tags = []
        vis_chars = 0

        for token in tokens:
            if re.fullmatch(r'\[/?\#?[a-zA-Z0-9]+\]', token):
                if token.startswith("[/"):
                    if open_tags and open_tags[-1] == token[2:-1]:
                        open_tags.pop()
                    result.append(token)
                else:
                    open_tags.append(token[1:-1])
                    result.append(token)
            else:
                if vis_chars >= visible_count:
                    break
                result.append(token)
                vis_chars += 1

        # Close open tags
        for tag in reversed(open_tags):
            result.append(f"[/{tag}]")
        return ''.join(result)

    # ========== Step 2: Typewriter Character Counting ==========
    tokens = tokenize_rich_text(splashy)
    if frame % int(1/theDelta) == 0:
        vis_chars = sum(1 for t in tokens[:text_index] if not re.fullmatch(r'\[/?\#?[a-zA-Z0-9]+\]', t))
        total_chars = sum(1 for t in tokens if not re.fullmatch(r'\[/?\#?[a-zA-Z0-9]+\]', t))
        if vis_chars < total_chars:
            text_index += 1
            playSound('Dialogue_sfx.ogg', 0.30)

        elif vis_chars >= total_chars:
            text_index = len(splashy)#total_chars + 2

    visible_text = reconstruct_text_upto(tokens, text_index)

    # ========== Step 3: Line wrapping with formatting ==========
    def wrap_rich_text(text, max_width, font):
        words = []
        current_word = ""
        tag_stack = []
        i = 0

        # Tokenize again, but word-based
        while i < len(text):
            if text[i] == '[':
                j = text.find(']', i)
                if j != -1:
                    tag = text[i:j+1]
                    if not tag.startswith("[/"):
                        tag_stack.append(tag)
                    else:
                        if tag_stack and tag_stack[-1][1:] == tag[2:]:
                            tag_stack.pop()
                    current_word += tag
                    i = j + 1
                    continue
            elif text[i] in (' ', '\n'):
                if current_word:
                    words.append(current_word)
                    current_word = ""
                #if text[i] != '\n':
                words.append(text[i])
                i += 1
            else:
                current_word += text[i]
                i += 1

        if current_word:
            words.append(current_word)

        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word
            test_surface = render_text(test_line, (255,255,255), font_size)
            if ((test_surface.get_width() > max_width*scaleFactor and current_line) and word != ' ') or word == '\n':
                lines.append(current_line.strip())
                if word != '\n' and word != ' ':
                    current_line = word
                else:
                    current_line = ''
            else:
                current_line = test_line
        if current_line.strip():
            lines.append(current_line.strip())

        return lines

    lines = wrap_rich_text(visible_text, maximum, font)

    # ========== Step 4: Portrait Drawing ==========
    if usePotrait:
        if emotion is None:
            icon = loadImg((f'selectionIcon/{name}.png', 0.55))
        else:
            icon = loadImg((f'selectionIcon/emotion/{name}/{emotion}.png', 0.55 * (220 / 300)))
        iconRect = icon.get_rect(center=(hudRect[4] + 80, hudRect[5] + 75))
        blitObj(hud, icon, iconRect.centerx, iconRect.centery, pivot_type="center")

    # ========== Step 5: Per-line Rendering & Blitting ==========
    xOffset = 140 if usePotrait else 0
    textBox = 18 * 2
    for num, line in enumerate(lines):
        if '[shake]' not in line and '[snake]' not in line:
            lineText = screenWindow.render_text(line, (255,255,255), font_size, frame=frame%30)
        else:
            lineText = other_render_text(line, (255,255,255), font_size, frame=frame%30)
        theXOffset = xOffset
        if num > 0 and line[0] != '*':
            theXOffset += 23
        y = hudRect[5] + num * font_size + 18
        
        blitObj(hud, lineText, hudRect[4] + 20 + theXOffset, y, pivot_type="topleft")

    textBox = 18 * 2 + len(lines) * font_size



def romanInt(num):
    # Define the Roman numeral symbols and their corresponding values
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num

def battleEnemy():
    if enemyAction[selectedEnemy] == 'chooseSkillEnemy':
        if 'multi_' in opponent[selectedEnemy].skills[whichAction[selectedEnemy]].type and 'opponent' in opponent[selectedEnemy].skills[whichAction[selectedEnemy]].type:
            for num in enemySelection[selectedEnemy]:
                numx = (width/2) /len(opponent) + (num * width/len(opponent))
                numy = (height -  75) - enemyTween[i] + battleStart
                numhpBG_X = numx - 200 / 2
                numhpBG_Y = numy - 50 / 2
                drawRect(screen, colorOfEnemy[selectedEnemy], (numhpBG_X, numhpBG_Y - 5, 220, 60))

    for i, enemy in enumerate(opponent):
            levelFont = font = pygame.font.Font(None, int(36*0.9))
            shakingX = 0
            shakingY = 0
            if enemy.hp/enemy.maxhp < 0.25:
                shakingX, shakingY = random.randint(-1, 1), random.randint(-2, 2)
            x = (width/2) /len(opponent) + (i * width/len(opponent)) + shakingX# + 100
            y = (height -  75) - enemyTween[i] + shakingY + battleStart
            iconX = (width/2) /len(opponent) - 100 + (i * width/len(opponent)) + 20 + shakingX
            iconY = y - 10
            hpX = x - 200 / 2 + 10
            hpY = y - 40 / 2
            hpBG_X = x - 210 / 2 + 10
            hpBG_Y = y - 50 / 2

            if selectedEnemy == i and enemyTurn:
                #drawRect(screen, (colorOfEnemy[i][0], colorOfEnemy[i][1], colorOfEnemy[i][2], 127), (hpBG_X, hpBG_Y + 55, 230, 10))
                drawRect(screen, colorOfEnemy[selectedEnemy], (hpBG_X, hpBG_Y - 5, 220, 60), 5)

            if enemySelection[selectedEnemy] == i and enemyAction[selectedEnemy] == 'chooseItemEnemy':
                drawRect(screen, colorOfEnemy[selectedEnemy], (hpBG_X, hpBG_Y - 5, 215, 60))


            name = enemy.name.upper()

            hpColor = enemy.color
            maxHpColor = (hpColor[0] * (180/255), hpColor[1] * (180/255), hpColor[2] * (180/255))
            HpBG = (hpColor[0] * (112/255), hpColor[1] * (112/255), hpColor[2] * (112/255))
            dhp = (hpColor[0] * (200/255), hpColor[1] * (200/255), hpColor[2] * (200/255))

            hp_ratio = 157 * (enemy.hp/enemy.maxhp)

            #image = loadImg(enemy.name + '.png')
            #image = scaleObj(image, 0.


            for numBuff, (buff, effects) in enumerate(enemy.buff.items()):
                buffX = hpX+ numBuff*40 + 43
                buffY = hpY + 45
                coloing = buff.color

                drawRect(screen, (coloing), (buffX, buffY, 35, 35))# The HP one
                drawRect(screen, (coloing[0] * 0.7, coloing[1] * 0.7, coloing[2] * 0.7), (buffX + 3, buffY + 3, 29, 29))# The HP one

                stuff = render_text(str(effects[0]), WHITE, 40, True, BLACK, 2)
                stuffRect = stuff.get_rect(center=(buffX + 35/2, buffY + 35/2))
                screen.blit(stuff, stuffRect)

            hpTextColor = BLACK
            if enemy.hp/enemy.maxhp <= 0.2:
                hpTextColor = YELLOW
            if enemy.hp/enemy.maxhp <= 0.05:
                hpTextColor = RED
            if enemy.hp/enemy.maxhp <= 0:
                hpTextColor = GRAY

            if enemy.hp == inf:
                text = '∞/∞'
            else:
                text = f'{int(enemy.hp)}/{enemy.maxhp}'

            hpText = render_text(text, hpTextColor, 48)
            #realText = textRender(text, hpTextColor, 48)
            hpWidth = hpText.get_size()[0] + 20
            if hpWidth < 157:
                hpWidth = 157
            #hpWidth = 150
            widthHp = hpWidth + (200 - 157)
            hpText_rect = hpText.get_rect(midright=(hpX + widthHp - 5, y))

            hp_ratio = hpWidth * (enemy.hp/enemy.maxhp) if enemy.hp != inf else hpWidth

            drawRect(screen, HpBG, (hpBG_X, hpBG_Y, widthHp + 10, 50)) # The HPBG one
            drawRect(screen, maxHpColor, (hpX, hpY, widthHp, 40)) # The MAX HP one
            drawRect(screen, hpColor, (hpX + 43, hpY, hp_ratio, 40))# The HP one
            drawRect(screen, dhp, (hpX + 43, hpY + 30, hp_ratio, 10)) #Still Hp

            partyIcon = loadImg(('battleIcon/' + enemy.name + '.png', 0.37, (255, 255, 255, 255)))
            classIcon = loadImg(('classes/' + enemy.classes + '.png', 0.37, (255, 255, 255, 255)))
            image_rect = partyIcon.get_rect(center=(iconX, iconY))
            class_rect = classIcon.get_rect(center=(iconX - 40, iconY + 30))
            screen.blit(partyIcon, image_rect)
            screen.blit(classIcon, class_rect)

            nameX = image_rect.right + 5 + shakingX
            nameY = y - 55

            hud.blit(hpText, hpText_rect)
            #blitText(screen, hpText_rect, realText, 10)

            nameText = render_text(name, BLACK, 42, True, WHITE, 2)
            nameText_rect = nameText.get_rect(topleft=(nameX - 5, nameY - 10))
            screen.blit(nameText, nameText_rect)

            levelWidth = levelFont.size(str(enemy.level))[0] + 6
            levelHeight = levelFont.size(str(enemy.level))[1] + 6

            levelText = render_text(f'{enemy.level}', colorOfEnemy[i], 40, True, BLACK, 1)
            levelRect = levelText.get_rect(center=(nameX - 93, nameY - 17))

            #drawRect(screen, hpColor, (levelRect[0] - 7, levelRect[1] - 7, levelWidth + 8, levelHeight + 8)) # The HPBG one
            #drawRect(screen, BLACK, (levelRect[0] - 3, levelRect[1] - 3, levelWidth, levelHeight)) # The MAX HP one

            #pygame.gfxdraw.aacircle(screen, levelRect[0], levelRect[1] , 22, hpColor)
            #pygame.gfxdraw.aacircle(screen, levelRect[0], levelRect[1] , 18, BLACK)
            #pygame.gfxdraw.filled_circle(screen, levelRect[0], levelRect[1] , 18, BLACK)
            drawCircle(screen, colorOfEnemy[i], (nameX - 93, nameY - 17) , 24)
            drawCircle(screen, BLACK, (nameX - 93, nameY - 17) , 20)

            screen.blit(levelText, (levelRect[0], levelRect[1]))

surfaceCache = {}
def loadSurface(width, height):
    key = (width, height)
    if key not in surfaceCache:
        print(1)
        surfaceCache[key] = pygame.Surface((max(width*scaleFactor, 1), max(height*scaleFactor, 1)), pygame.SRCALPHA)
    surfaceCache[key].fill((0, 0, 0, 0))
    return surfaceCache[key]
def battleAlly():
    global energy, intenseX, intenseNum
    deadCount = 0
    if allyAction[selectedAlly] == "chooseSkillAlly":
        if (
            "Multiple"
            in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType
            and "ally" in party[selectedAlly].skills[whichAction[selectedAlly]].type
        ):
            for num in allySelection[selectedAlly]:
                numx = (width / 2) / len(party) + (num * width / len(party))
                numy = (height - 75) - allyTween[num] + battleStart
                numhpBG_X = numx - 200 / 2
                numhpBG_Y = numy - 50 / 2
                if selectedAlly >= len(colorOfAlly):
                    colorOfAlly.append(party[selectedAlly].color)
                drawRect(
                    hud, colorOfAlly[selectedAlly], (numhpBG_X, numhpBG_Y - 5, 220, 60)
                )
    for i, ally in enumerate(party):
        if i >= len(colorOfAlly):
            colorOfAlly.append(party[i].color)
        if len(party) > 5 and ally != party[selectedAlly]:
            continue
        surface = loadSurface(290, 165)
        #levelFont = font = pygame.font.Font(None, int(36 * 0.9))
        shakingX = 0
        shakingY = 0
        if ally.hp / ally.maxhp < 0.25:
            shakingX, shakingY = random.randint(-1, 1), random.randint(-2, 2)
        #ally.levelUp(0)
        x = 160
        y = 100
        iconX = x - 80
        iconY = y - 10
        hpX = x - 200 / 2 + 5
        hpY = y - 90 / 2
        hpBG_X = x - 210 / 2 + 5
        hpBG_Y = y - 100 / 2

        if allySelection[selectedAlly] == i and allyAction[selectedAlly] in [
            "chooseItemAlly",
            "chooseSkillAlly",
            "chooseActAlly",
        ]:
            drawRect(
                surface, colorOfAlly[selectedAlly], (hpBG_X, hpBG_Y - 5, 215, 60)
            )

        name = ally.displayName.upper()
        hpColor = ally.color
        maxHpColor = (
            hpColor[0] * (170 / 255),
            hpColor[1] * (170 / 255),
            hpColor[2] * (170 / 255),
        )
        darkHpColor = (
            hpColor[0] * (180 / 255),
            hpColor[1] * (180 / 255),
            hpColor[2] * (180 / 255),
        )
        lightHpColor = (
            min(hpColor[0] + 40, 255),
            min(hpColor[1] + 40, 255),
            min(hpColor[2] + 40, 255),
        )
        HpBG = (
            hpColor[0] * (112 / 255),
            hpColor[1] * (112 / 255),
            hpColor[2] * (112 / 255),
        )
        dhp = (
            hpColor[0] * (210 / 255),
            hpColor[1] * (210 / 255),
            hpColor[2] * (210 / 255),
        )

        hpTextColor = BLACK if hpColor != (0, 0, 0) else WHITE
        if ally.hp / ally.maxhp <= 0.2:
            hpTextColor = YELLOW
        if ally.hp / ally.maxhp <= 0.05:
            hpTextColor = RED
        if ally.hp / ally.maxhp <= 0:
            hpTextColor = GRAY

        #print(ally.hp)
        if ally.maxhp == float('inf'):
            text = "\u221E/\u221E"
        else:
            text = f"{round(ally.hp)}/{ally.maxhp}"
            
        #print('\u221E')

        hpText = render_text(text, hpTextColor, 44)
        if ally.maxMana == 100:
            apText = render_text(str(round(ally.mana / ally.maxMana * 100)) + '%', hpTextColor, 32)
        else:
            apText = render_text(f'{str(round(ally.mana))}/{str(ally.maxMana)}', hpTextColor, 32)
        hpWidth = hpText.get_size()[0] + 20
        if hpWidth < 157:
            hpWidth = 157
        if len(party) == 5 and not (intenseMode and ally.hp > 0):
            if ally.maxhp == float('inf'):
                text = "\u221E"
            else:
                text = f"{round(ally.hp)}"
            hpWidth = 90
            hpText = render_text(text, hpTextColor, 44)
            apText = render_text(f'{str(round(ally.mana))}', hpTextColor, 32)
        widthHp = hpWidth + (200 - 157)
        widthAp = widthHp
        apWidth = hpWidth
        hp_ratio = hpWidth * (ally.hp / ally.maxhp) if ally.hp != inf else hpWidth
        ap_ratio = apWidth * (ally.mana / ally.maxMana)
        hpLight = (min(hpColor[0] + 70, 255), min(hpColor[1] + 70, 255), min(hpColor[2] + 70, 255))

        drawRect(surface, (0, 120, 120), (hpBG_X, hpBG_Y + 40, widthAp + 10, 35))
        drawRect(surface, (0, 170, 170), (hpX, hpY + 40, widthAp, 25))
        drawRect(surface, (0, 210, 210), (hpX + 43, hpY + 40, ap_ratio, 25))
        drawRect(surface, (0, 190, 190), (hpX + 43, hpY + 60, ap_ratio, 5))
        drawRect(surface, CYAN, (hpX + 43, hpY + 40, ap_ratio, 5))

        HpBG = ally.color
        #dhp = hpColor = darkHpColor = ally.barColor
        #dhp

        drawRect(surface, HpBG, (hpBG_X, hpBG_Y - 5, widthHp + 10, 50))
        drawRect(surface, maxHpColor, (hpX, hpY - 5, widthHp, 40))
        drawRect(surface, dhp, (hpX + 43, hpY - 5, hp_ratio, 40))
        drawRect(surface, lightHpColor, (hpX + 43, hpY - 5, hp_ratio, 5))
        drawRect(surface, darkHpColor, (hpX + 43, hpY + 30, hp_ratio, 5))

        partyIcon = loadImg(("battleIcon/" + ally.displayName + ".png", 0.40, (255, 255, 255, 255)))
        classIcon = loadImg(("classes/" + ally.classes + ".png", 0.37, (255, 255, 255, 255)))

        # REPLACED: get_rect + blit
        blitObj(surface, partyIcon, iconX, iconY, pivot_type="center")
        blitObj(surface, classIcon, iconX - 40, iconY + 30, pivot_type="center")

        nameX = iconX + (partyIcon.get_width()/scaleFactor) // 2 + 5 + shakingX
        nameY = y - 55

        blitObj(surface, hpText, hpX + widthHp - 5, y - 27, 'midright')
        blitObj(surface, apText, hpX + widthAp - 5, y + 7, 'midright')
        nameText = render_text(name, BLACK, 42, True, WHITE, 2)
        if (nameText.get_width()*(1/scaleFactor)) > 290 - (nameX - 30):
            nameText = scaleObj(nameText, ((290 - (nameX - 30)) / (nameText.get_width()*(1/scaleFactor)), 1), False)
        nameText_rect = nameText.get_rect(topleft=(nameX - 30, nameY - 40))
        blitObj(surface, nameText, nameX - 30, nameY - 40, pivot_type='topleft')

        levelText = render_text(f"{ally.level}", colorOfAlly[i], 40, True, BLACK, 1)

        drawCircle(surface, colorOfAlly[i], (nameX - 90, nameY - 17), 24)
        drawCircle(surface, BLACK, (nameX - 93, nameY - 17), 20)
        blitObj(surface, levelText, nameX - 93, nameY - 17)

        for numBuff, (buff, effects) in enumerate(ally.buff.items()):
            buffX = hpX + numBuff * 40 + 45 if len(ally.buff.items()) <= 4 else hpX + 45 + numBuff * (hpWidth - 40 + 5) / (len(ally.buff.items()) - 1)
            buffY = hpY + 20 + 48
            coloing = buff.color
            dark = (coloing[0] * 0.7, coloing[1] * 0.7, coloing[2] * 0.7)
            outline = (180, 70, 70) if "Debuff" in buff.type else (70, 255, 70)

            drawRect(surface, outline, (buffX - 3, buffY - 3, 41, 41))
            drawRect(surface, dark, (buffX, buffY, 35, 35))
            drawRect(surface, coloing, (buffX + 3, buffY + 3, 29, 29))

            if effects[0] == float('inf'):
                stuff = render_text('\u221E', WHITE, 28, True, BLACK, 2)
            else:
                if effects[0] > 0:
                    stuff = render_text(str(effects[0]) + 'C', WHITE, 28, True, BLACK, 2)
                else:
                    stuff = render_text(str(effects[3]) + 'T', WHITE, 28, True, BLACK, 2)
            blitObj(surface, stuff, buffX + 35 / 2, buffY + 28)

            stage = render_text(romanInt(effects[2]), WHITE, 20, True, BLACK, 2)
            blitObj(surface, stage, buffX + 35 / 2, buffY)

        #for num, players in enumerate(party):

        x = (width / 2) / len(party) + (i * width / len(party)) + shakingX + allyHudX
        y = (height - 80) - allyTween[i] + shakingY + battleStart
        if len(party) == 5:
            x += 45
        if len(party) > 5 and ally == party[selectedAlly]:
            x = 500

        #surface = rotateObj(surface, playerShakeX[i] / 8)
        if intenseMode and ally.hp <= 0:
            allyTween[i] += 10 * theDelta
            y += ((allyTween[i]/10)-8 + 4)**2
            x += 5*(allyTween[i]/10)
            surface = rotateObj(surface, -allyTween[i]/10)
            if i == intenseNum[0]:
                x += intenseX[0]
        elif intenseMode and ally.hp > 0:
            if allyTween[i] > 50:
                allyTween[i] = 50
            oriX = x
            x += intenseX[0]
            if opponentBot:
                xNum = 500
            else:
                xNum = 300
            intenseNum[0] = i
            if abs(x - xNum) > 1:
                intenseX[0] += (xNum - x)/15 * (theDelta)
            else:
                intenseX[0] = xNum - oriX
        blitObj(hud, surface, x-15/2, y, 'center', (0.5, 0.5))

intenseX = [0, 0]
intenseNum = [0, 0]
allyHudX = 0
enemyHudY = 0
def battleEnemy():
    global energy, intenseX, intenseNum
    deadCount = 0
    if enemyAction[selectedEnemy] == "chooseSkillAlly":
        if (
            "Multiple"
            in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType
            and "ally" in opponent[selectedEnemy].skills[whichAction[selectedEnemy]].type
        ):
            for num in enemySelection[selectedEnemy]:
                numx = (width / 2) / len(party) + (num * width / len(party))
                numy = (height - 75) - enemyTween[num] + battleStart
                numhpBG_X = numx - 200 / 2
                numhpBG_Y = numy - 50 / 2
                if selectedAlly >= len(colorOfEnemy):
                    colorOfEnemy.append(opponent[selectedEnemy].color)
                drawRect(
                    hud, colorOfEnemy[selectedEnemy], (numhpBG_X, numhpBG_Y - 5, 220, 60)
                )
    for i, ally in enumerate(opponent):
        if i >= len(colorOfEnemy):
            colorOfEnemy.append(opponent[i].color)
        surface = loadSurface(290, 165)
        levelFont = font = pygame.font.Font(None, int(36 * 0.9))
        shakingX = 0
        shakingY = 0
        if ally.hp / ally.maxhp < 0.25:
            shakingX, shakingY = random.randint(-1, 1), random.randint(-2, 2)
        ally.levelUp(0)
        x = 160
        y = 100
        iconX = x - 80
        iconY = y - 10
        hpX = x - 200 / 2 + 5
        hpY = y - 90 / 2
        hpBG_X = x - 210 / 2 + 5
        hpBG_Y = y - 100 / 2

        if enemySelection[selectedEnemy] == i and enemyAction[selectedEnemy] in [
            "chooseItemAlly",
            "chooseSkillAlly",
            "chooseActAlly",
        ]:
            drawRect(
                surface, colorOfEnemy[selectedEnemy], (hpBG_X, hpBG_Y - 5, 215, 60)
            )

        name = ally.displayName.upper()
        hpColor = ally.color
        maxHpColor = (
            hpColor[0] * (170 / 255),
            hpColor[1] * (170 / 255),
            hpColor[2] * (170 / 255),
        )
        darkHpColor = (
            hpColor[0] * (180 / 255),
            hpColor[1] * (180 / 255),
            hpColor[2] * (180 / 255),
        )
        lightHpColor = (
            min(hpColor[0] + 40, 255),
            min(hpColor[1] + 40, 255),
            min(hpColor[2] + 40, 255),
        )
        HpBG = (
            hpColor[0] * (112 / 255),
            hpColor[1] * (112 / 255),
            hpColor[2] * (112 / 255),
        )
        dhp = (
            hpColor[0] * (210 / 255),
            hpColor[1] * (210 / 255),
            hpColor[2] * (210 / 255),
        )

        hpTextColor = BLACK if hpColor != (0, 0, 0) else WHITE
        if ally.hp / ally.maxhp <= 0.2:
            hpTextColor = YELLOW
        if ally.hp / ally.maxhp <= 0.05:
            hpTextColor = RED
        if ally.hp / ally.maxhp <= 0:
            hpTextColor = GRAY


        if ally.hp == inf:
            text = "∞/∞"
        else:
            text = f"{round(ally.hp)}/{ally.maxhp}"

        hpText = render_text(text, hpTextColor, 44)
        if ally.maxMana == 100:
            apText = render_text(str(round(ally.mana / ally.maxMana * 100)) + '%', hpTextColor, 32)
        else:
            apText = render_text(f'{str(round(ally.mana))}/{str(ally.maxMana)}', hpTextColor, 32)
        hpWidth = hpText.get_size()[0] + 20
        if hpWidth < 157:
            hpWidth = 157
        widthHp = hpWidth + (200 - 157)
        widthAp = widthHp
        apWidth = hpWidth
        hp_ratio = hpWidth * (ally.hp / ally.maxhp) if ally.hp != inf else hpWidth
        ap_ratio = apWidth * (ally.mana / ally.maxMana)
        hpLight = (min(hpColor[0] + 70, 255), min(hpColor[1] + 70, 255), min(hpColor[2] + 70, 255))

        drawRect(surface, (0, 120, 120), (hpBG_X, hpBG_Y + 40, widthAp + 10, 35))
        drawRect(surface, (0, 170, 170), (hpX, hpY + 40, widthAp, 25))
        drawRect(surface, (0, 210, 210), (hpX + 43, hpY + 40, ap_ratio, 25))
        drawRect(surface, (0, 190, 190), (hpX + 43, hpY + 60, ap_ratio, 5))
        drawRect(surface, CYAN, (hpX + 43, hpY + 40, ap_ratio, 5))

        HpBG = ally.color
        #dhp = hpColor = darkHpColor = ally.barColor
        #dhp

        drawRect(surface, HpBG, (hpBG_X, hpBG_Y - 5, widthHp + 10, 50))
        drawRect(surface, maxHpColor, (hpX, hpY - 5, widthHp, 40))
        drawRect(surface, dhp, (hpX + 43, hpY - 5, hp_ratio, 40))
        drawRect(surface, lightHpColor, (hpX + 43, hpY - 5, hp_ratio, 5))
        drawRect(surface, darkHpColor, (hpX + 43, hpY + 30, hp_ratio, 5))

        partyIcon = loadImg(("battleIcon/" + ally.displayName + ".png", 0.40, (255, 255, 255, 255)))
        classIcon = loadImg(("classes/" + ally.classes + ".png", 0.37, (255, 255, 255, 255)))

        # REPLACED: get_rect + blit
        blitObj(surface, partyIcon, iconX, iconY, pivot_type="center")
        blitObj(surface, classIcon, iconX - 40, iconY + 30, pivot_type="center")

        nameX = iconX + (partyIcon.get_width()/scaleFactor) // 2 + 5 + shakingX
        nameY = y - 55

        blitObj(surface, hpText, hpX + widthHp - 5, y - 27, 'midright')
        blitObj(surface, apText, hpX + widthAp - 5, y + 7, 'midright')
        nameText = render_text(name, BLACK, 42, True, WHITE, 2)
        nameText_rect = nameText.get_rect(topleft=(nameX - 30, nameY - 40))
        blitObj(surface, nameText, nameX - 30, nameY - 40, pivot_type='topleft')

        levelText = render_text(f"{ally.level}", colorOfEnemy[i], 40, True, BLACK, 1)

        drawCircle(surface, colorOfEnemy[i], (nameX - 90, nameY - 17), 24)
        drawCircle(surface, BLACK, (nameX - 93, nameY - 17), 20)
        blitObj(surface, levelText, nameX - 93, nameY - 17)

        for numBuff, (buff, effects) in enumerate(ally.buff.items()):
            buffX = hpX + numBuff * 40 + 45 if len(ally.buff.items()) <= 4 else hpX + 45 + numBuff * (hpWidth - 40 + 5) / (len(ally.buff.items()) - 1)
            buffY = hpY + 20 + 48
            coloing = buff.color
            dark = (coloing[0] * 0.7, coloing[1] * 0.7, coloing[2] * 0.7)
            outline = (180, 70, 70) if "Debuff" in buff.type else (70, 255, 70)

            drawRect(surface, outline, (buffX - 3, buffY - 3, 41, 41))
            drawRect(surface, dark, (buffX, buffY, 35, 35))
            drawRect(surface, coloing, (buffX + 3, buffY + 3, 29, 29))

            if effects[0] == float('inf'):
                stuff = render_text(str('∞'), WHITE, 28, True, BLACK, 2)
            else:
                stuff = render_text(str(effects[0]), WHITE, 28, True, BLACK, 2)
            blitObj(surface, stuff, buffX + 35 / 2, buffY + 28)

            stage = render_text(romanInt(effects[2]), WHITE, 20, True, BLACK, 2)
            blitObj(surface, stage, buffX + 35 / 2, buffY)

        #for num, players in enumerate(party):

        x = (width / 2) / len(opponent) + (i * width / len(opponent)) + shakingX + enemyHudX
        y = (height - 90) - enemyTween[i] + shakingY + battleStart

        #surface = rotateObj(surface, playerShakeX[i] / 8)
        if intenseMode and ally.hp <= 0:
            enemyTween[i] += 10
            y += ((enemyTween[i]/10)-8 + 4)**2
            x += 2*(enemyTween[i]/10)
            surface = rotateObj(surface, -enemyTween[i]/10)
            if i == intenseNum[1]:
                x += intenseX[1]
        elif intenseMode and ally.hp > 0:
            if enemyTween[i] > 50:
                enemyTween[i] = 50
            if opponentBot:
                xNum = 500
            else:
                xNum = 700
            oriX = x
            x += intenseX[1]
            intenseNum[1] = i
            if abs(x - xNum) > 1:
                intenseX[1] += (xNum - x)/15 / (30*theDelta)
            else:
                intenseX[1] = xNum - oriX
        blitObj(hud, surface, x-15/2, y, 'center', (0.5, 0.5))


def splashText(text, bool, num):
    global splashy
    global text_index
    global battleSplash
    text_index = num
    #if text != None:
    splashy = str(text)
    if bool == True:
        battleSplash = True
    else:
        battleSplash = False

actionList = [False, [0, 0], (width/2, height/2), "Fight", 0]
def destroyAction(name="Fight"):
    actionList[0] = True
    actionList[3] = name
    actionList[2] = actionList[1]
    actionList[4] = 0
    hud.camera_shake = 10
    hud.start_shake(90, 10)
    screen.camera_shake = 10
    screen.start_shake(90, 10)
    backGroundScreen.camera_shake = 10
    backGroundScreen.start_shake(90, 10)
    playSound("Hurt_sfx.ogg", 2)

def loadMenu(borderColor=(100, 100, 100), inColor=(150, 150, 150)):
    global hudScroll, selectedAction

    if turnDialogue[min(turn-1, len(turnDialogue)-1)][2] == True:
        if (allyTurn or enemyTurn) and hudScroll > 0 and hudRect[3] >= 150 and hudRect[2] >= (len(actions) * 70 + 20):
            hudScroll -= 20/3

        elif (allyTurn or enemyTurn) and hudScroll <= 0:
            hudScroll = 0

        elif not (allyTurn or enemyTurn) and hudScroll < 150:
            hudScroll += 20/3

        elif not (allyTurn or enemyTurn) and hudScroll >= 150:
            hudScroll = 150

        hudScroll = 0 if not (turnAlly or turnEnemy) else hudScroll

    if actionList[0] != True and hudScroll != 80 and hudRect[3] >= 150 and hudRect[2] >= (len(actions) * 70 + 20) and (not (turnEnemy and opponentBot)) and turnDialogue[min(turn-1, len(turnDialogue)-1)][2] == True:
        actionCenterY = 310 + hudScroll
        actionLength = len(actions) * 70 + 20
        actionHeight = 90
        actionX = hudRect[4]
        actionY = actionCenterY - (actionHeight / 2) - (345 - hudRect[5])
        thickness = 6
        drawRect(hud, borderColor, (actionX, actionY, actionLength, actionHeight)) # The HPBG one
        drawRect(hud, inColor, (actionX + thickness, actionY + thickness, actionLength - (2*thickness), actionHeight - (2*thickness))) # The MAX HP one
        actionList[1] = [actionX + actionLength/2, actionCenterY + actionHeight/2]
        for i, stuff in enumerate(actions):
                whichOne = selectedAlly if not turnEnemy else selectedEnemy
                whichOne = min(whichOne, len(theAlly) - 1)
                color = colorOfAlly if not turnEnemy else colorOfEnemy
                x = actionX + 45 + 70 * i
                y = hudScroll + 310 - (345 - hudRect[5])
                if i == selectedAction:
                    colour = (255, 255, 255)
                    scale = 0.6
                else:
                    colour = color[whichOne]
                    scale = 0.6

                image = loadImg((stuff + '.png', scale, colour))
                #img = image.copy()
                img_rect = image.get_rect(center=(x, y))

                blitObj(hud, image, x, y)
                #img = None
        cursor = loadImg(('scroll.png', 0.25, color[whichOne]), angle=-90)
        blitObj(hud, cursor, actionX + 45 + 70*selectedAction, y - 40)
        text = render_text(actions[selectedAction].upper(), YELLOW, 36, True, BLACK, 2)
        blitObj(hud, text, actionX + 45 + 70*selectedAction, y - 60)

    if actionList[0] == True:
        actionWhich[selectedWhich] = None
        whichAction[selectedWhich] = 0
        whichSelection[selectedWhich] = 0
        actionList[2][0] += (width/2 - actionList[2][0])/4
        actionList[2][1] += (height/2 - 100 - actionList[2][1])/4
        if abs(actionList[2][0] - width/2) < 0.1:
            actionList[2][0] = width/2
            actionList[2][1] = height/2 - 100
            if actionList[4] == 0 or actionList[4] == 26:
                if actionList[4] == 0:
                    playSound("Attack_sfx.ogg")
                hud.camera_shake = 10
                hud.start_shake(90, 10)
                screen.camera_shake = 10
                screen.start_shake(90, 10)
                backGroundScreen.camera_shake = 10
                backGroundScreen.start_shake(90, 10)

            actionList[4] += 1
            if actionList[4] == 39:
                actionList[0] = False
                actions.remove(actionList[3])
                hudScroll = 150
                selectedAction = 0
            
        actionCenterY = actionList[2][1] + min(max(40*(actionList[4]-26), 0), 250)
        actionLength = len(actions) * 70 + 20 - min(max(5*(actionList[4]-8), 0), 70)
        actionHeight = 90
        actionX = actionList[2][0] - actionLength / 2 #+ 2*min(max(2*(actionList[4]-8), 0), 70)
        actionY = actionList[2][1] - (actionHeight / 2) + min(max(40*(actionList[4]-26), 0), 250)
        thickness = 6
        drawRect(hud, borderColor, (actionX, actionY, actionLength, actionHeight)) # The HPBG one
        drawRect(hud, inColor, (actionX + thickness, actionY + thickness, actionLength - (2*thickness), actionHeight - (2*thickness))) # The MAX HP one
        #actionList[1] = (actionX, actionY)
        for i, stuff in enumerate(actions):
                whichOne = selectedAlly if not turnEnemy else selectedEnemy
                whichOne = min(whichOne, len(theAlly) - 1)
                color = colorOfAlly if not turnEnemy else colorOfEnemy
                x = actionX + 45 + 70 * i 
                if actionList[0] == True:
                    if i > actions.index(actionList[3]):
                        x = actionX + 45 + 70 * i - min(max(5*(actionList[4]-8), 0), 70)
                    #else:
                        #x = actionX + 45 + 70 * i + min(max(5*(actionList[4]-8), 0), 70)
                oriX = x
                y = actionCenterY
                oriY = y
                if i == selectedAction:
                    colour = (255, 255, 255)
                    scale = 0.6
                else:
                    colour = color[whichOne]
                    scale = 0.6

                if actionList[4] > 0 and stuff == actionList[3]:
                    colour = (20, 20, 20)

                image = loadImg((stuff + '.png', scale, colour))
                #img = image.copy()
                if actionList[4] >= 8 and stuff == actionList[3]:
                    frame = actionList[4] - 8
                    image = loadImg((stuff + '.png', scale, colour), angle=-4*frame)
                    y += (frame - 5)**2
                    x += 10*frame 
                img_rect = image.get_rect(center=(x, y))

                blitObj(hud, image, x, y)

                if actionList[4] > 0 and stuff == actionList[3]:
                    if actions[selectedAction] == stuff:
                        selectedAction += 1
                    if selectedAction >= len(actions):
                        selectedAction = 0
                    drawRect(hud, RED, oriX - 70 + actionList[4]*3.5, 0, 140 - actionList[4]*7, height)
                #img = None
        if actionList[0]:
            cursor = loadImg(('scroll.png', 0.25, color[whichOne]), angle=-90)
            if selectedAction > actions.index(actionList[3]):
                blitObj(hud, cursor, actionX + 45 + 70*selectedAction - min(max(5*(actionList[4]-8), 0), 70), oriY - 40)
            else:
                blitObj(hud, cursor, actionX + 45 + 70*selectedAction, oriY - 40)
            text = render_text(actions[selectedAction].upper(), YELLOW, 36, True, BLACK, 2)
            if selectedAction > actions.index(actionList[3]):
                blitObj(hud, text, actionX + 45 + 70*selectedAction - min(max(5*(actionList[4]-8), 0), 70), oriY - 60)
            else:
                blitObj(hud, text, actionX + 45 + 70*selectedAction, oriY - 60)

    centerX = hudRect[0]
    centerY = hudRect[1]
    hudLength = hudRect[2]
    hudHeight = hudRect[3]
    hudX = hudRect[4]
    hudY = hudRect[5]
    thickness = hudRect[6]
    drawRect(hud, borderColor, (hudX, hudY, hudLength, hudHeight)) # The HPBG one
    drawRect(hud, inColor, (hudX + thickness, hudY + thickness, hudLength - (2*thickness), hudHeight - (2*thickness))) # The MAX HP one

    energyLength = 220
    if hudRect[2] <= 230:
        energyLength = hudRect[2] - 10

    energy_ratio = energy / 1000 * energyLength
    enerTrans_ratio = energyTrans / 1000 * energyLength

    hpBG_X = hudX + hudLength - (energyLength + 10)
    hpBG_Y = hudRect[5] - 50
    hpX = hpBG_X + 5
    hpY = hpBG_Y + 5

    drawRect(hud, (150, 0, 0), (hpBG_X, hpBG_Y, energyLength + 10, 35)) # The HPBG one
    drawRect(hud, (200, 0, 0), (hpX, hpY, energyLength, 25)) # The MAX HP one
    drawRect(hud, WHITE, (hpX, hpY, enerTrans_ratio, 25)) # The FADE one
    drawRect(hud, RED, (hpX, hpY, energy_ratio, 25)) # The HP one

    energyText = render_text(f'SP {int(energy)}%', BLACK, 50, True, WHITE, 2)
    blitObj(hud, energyText, hudX + hudLength, hpBG_Y - 40, pivot_type="topright")

def barBlitUp():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    #attackMeterX = hudRect[2]/2
    fightFrame += 1
    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            fightFrame -= 10
            if 'Under' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Under' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1

    startSpot = hudRect[1] + 270/2#hudRect[3] + hudRect[5]#hudRect[5]
    attackMeterX = 270

    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.6
        multiply = -1.7 if hardMode else -1.3
        baseNum = (6 / 3) * theDelta if not easyMode else theDelta
    else:
        theBase = 1
        multiply = 0.8
        baseNum = (4 / 3) * theDelta

    for i, bar in enumerate(fightBar[:inBar]):

            if 'NoBar' in bar or not 'Under' in bar:
                continue
            else:
                barColor = fightingBar[bar][6].color
                allyNum = theAlly.index(fightingBar[bar][6])
                identifier = ''
                for strI in fightingBar[bar][10]:
                    if not strI.isdigit():
                        identifier += strI
                    else:
                        break
                theAttack = fightingBar[bar][7]
                if ((theAttack.nextBar == fightingBar[bar][10])
                    or theAttack.bars.index(fightingBar[bar][10]) == 0):
                    fightingBar[bar][11] = True
                if fightingBar[bar][11] == False:
                    continue

                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = abs(theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[0]
                if 'done' in fightingBar[bar][2]:
                    fightSuccess = True
                    x = fightBarX2[i]
                else:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x




                if (x < hudRect[5]) and (not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            x = fightBarX2[i]
                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0

                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True
                    barAlpha[i] = max(0, barAlpha[i] - 40)

                if fightSuccess and barAlpha[i] - 40 > 0:
                    #barColor = YELLOW
                    fightScale[i] += 0.1
                    barAlpha[i] -= 40
                elif barAlpha[i] - 40 <= 0 or fightBarX2[i] < -10:
                    barNoMore = True

                if abs((hudRect[1] - 270/2) - fightBarX2[i] + 15) <= 10 and fightSuccess:
                    fightBarX2[i] = (hudRect[1] - 270/2) + 15
                    x = (hudRect[1] - 270/2) + 15
                    critHit = True
                    barColor = (255, 255, 0)


                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i])




                if not barNoMore:
                    meter = loadImg(('meterDown.png', fightScale[i], FinalBarColor))
                    blitObj(hud, meter, y, x, pivot_type="center")


                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in fightingBar[bar][2]:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not ((critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot)):
                    critHitBool = False
                if strike:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = abs(attackMeterX - fightBarX2[i])
                        attackMeterWidth = attack_rect.width
                        maxDistance = attackMeterWidth /2
                        damagePercent = (theBase - (min(distance / maxDistance, 1))*multiply)
                        if (critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            if fightFail and turnEnemy and opponentBot:
                                distance = abs(attackMeterX - (hudRect[3] + hudRect[5]) )
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = abs((hudRect[1] - 270/2) + 15 - fightBarX2[barNum])
                                attackMeterWidth = attack_rect.width
                                maxDistance = attackMeterX - 15
                                damagePercent = (theBase - (min(distance / maxDistance, 1))*multiply)
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                if abs(fightingBar[barBar][8] - 100*damagePercent) < 5 and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done':
                                    fightingBar[barBar][2] = 'done'
                                    fightingBar[barBar][7].currentBar = fightingBar[barBar][10]
                                    theBar = fightingBar[barBar][7].bars
                                    fightingBar[barBar][7].nextBar = theBar[ min(theBar.index(fightingBar[barBar][10]) + 1, len(theBar) - 1 )]
                                    #playSound('Attack_sfx.ogg')
                                if (critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                                    if fightFail and turnEnemy and opponentBot:
                                        distance = abs(attackMeterX - (hudRect[3] + hudRect[5]) )
                                trueDamage = damage * damagePercent
                                if fightBarX2[barNum] <= 35:
                                    trueDamage = 0
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount


def barBlitDown():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    #attackMeterX = hudRect[2]/2
    fightFrame += 1
    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            fightFrame -= 10
            if 'Support' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Support' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1

    startSpot = hudRect[1] - 270/2
    attackMeterX = 270

    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.6
        multiply = -1.7 if hardMode else -1.3
        baseNum = (6 / 3) * theDelta if not easyMode else theDelta
    else:
        theBase = 1
        multiply = 0.8
        baseNum = (4 / 3) * theDelta

    for i, bar in enumerate(fightBar[:inBar]):

            if 'NoBar' in bar or not 'Support' in bar:
                continue
            else:
                barColor = fightingBar[bar][6].color
                allyNum = theAlly.index(fightingBar[bar][6])
                identifier = ''
                for strI in fightingBar[bar][10]:
                    if not strI.isdigit():
                        identifier += strI
                    else:
                        break
                theAttack = fightingBar[bar][7]
                if ((theAttack.nextBar == fightingBar[bar][10])
                    or theAttack.bars.index(fightingBar[bar][10]) == 0):
                    fightingBar[bar][11] = True
                if fightingBar[bar][11] == False:
                    continue

                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = abs(theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[0]
                if 'done' in fightingBar[bar][2]:
                    fightSuccess = True
                    x = fightBarX2[i]
                else:
                    x = startSpot + 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x



                if (x > hudRect[1] + 270/2) and (not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            x = fightBarX2[i]
                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0

                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True
                    barAlpha[i] = max(0, barAlpha[i] - 40)

                if fightSuccess and barAlpha[i] - 40 > 0:
                    #barColor = YELLOW
                    fightScale[i] += 0.1
                    barAlpha[i] -= 40
                elif barAlpha[i] - 40 <= 0 or fightBarX2[i] < -10:
                    barNoMore = True

                if abs((hudRect[1] + 270/2) - fightBarX2[i] - 15) <= 10 and fightSuccess:
                    fightBarX2[i] = (hudRect[1] + 270/2) - 15
                    x = (hudRect[1] + 270/2) - 15
                    critHit = True
                    barColor = (255, 255, 0)

                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i])




                if not barNoMore:
                    meter = loadImg(('meterDown.png', fightScale[i], FinalBarColor))
                    blitObj(hud, meter, y, x, pivot_type="center")


                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in fightingBar[bar][2]:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not ((critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot)):
                    critHitBool = False
                if strike:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = ((hudRect[1] + 270/2) - 15 - fightBarX2[barNum])
                        attackMeterWidth = attack_rect.width
                        maxDistance = attackMeterX - 15
                        damagePercent = (theBase - (min(distance / maxDistance, 1))*multiply)
                        if (abs(distance) < 10 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            if fightFail and turnEnemy and opponentBot:
                                distance = abs(attackMeterX - hudRect[5])
                            damagePercent = (theBase - (1)*multiply)
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = (((hudRect[1] + 270/2) - 15) - fightBarX2[barNum])
                                attackMeterWidth = attack_rect.width
                                maxDistance = attackMeterX - 15 #attackMeterWidth /2
                                damagePercent = (theBase - (min(distance / maxDistance, 1))*multiply)
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                if abs(fightingBar[barBar][8] - 100*damagePercent) < 5 and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done':
                                    fightingBar[barBar][2] = 'done'
                                    fightingBar[barBar][7].currentBar = fightingBar[barBar][10]
                                    theBar = fightingBar[barBar][7].bars
                                    fightingBar[barBar][7].nextBar = theBar[ min(theBar.index(fightingBar[barBar][10]) + 1, len(theBar) - 1 )]
                                    #playSound('Attack_sfx.ogg')
                                #if (abs(distance) < 10 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                                   # if fightFail and turnEnemy and opponentBot:
                                        #distance = abs(attackMeterX - hudRect[5])
                                    #damagePercent = (theBase - (1)*multiply)
                                trueDamage = damage * damagePercent
                                if fightBarX2[barNum] <= 35:
                                    trueDamage = 0
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount

def spiralBlit():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    #attackMeterX = hudRect[2]/2
    fightFrame += 1
    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            fightFrame -= 10
            if 'Thrower' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Thrower' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1

    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.6
        multiply = -1.7 if hardMode else -1.3
        baseNum = (math.pi/1.5) * theDelta if not easyMode else (math.pi/2) * theDelta
    else:
        theBase = 1
        multiply = 1
        baseNum = (math.pi/2) * theDelta

    try:
        ringThing
    except NameError:
        ringThing = pygame.Surface((scaleFactor*hudRect[2]*1.5,scaleFactor*hudRect[3]*1.5), pygame.SRCALPHA)

    startSpot = math.pi * 5
    if ringThing.get_width() != scaleFactor*hudRect[2]*1.5 and ringThing.get_height() != scaleFactor*hudRect[3]*1.5:
        ringThing = pygame.Surface((scaleFactor*hudRect[2]*1.5,scaleFactor*hudRect[3]*1.5), pygame.SRCALPHA)

    for i, bar in enumerate(fightBar[:inBar]):

            if 'NoBar' in bar or not 'Thrower' in bar:
                continue
            else:
                barColor = fightingBar[bar][6].color
                allyNum = theAlly.index(fightingBar[bar][6])
                identifier = ''
                for strI in fightingBar[bar][10]:
                    if not strI.isdigit():
                        identifier += strI
                    else:
                        break
                theAttack = fightingBar[bar][7]
                if ((theAttack.nextBar == fightingBar[bar][10])
                    or theAttack.bars.index(fightingBar[bar][10]) == 0):
                    fightingBar[bar][11] = True
                if fightingBar[bar][11] == False:
                    continue

                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = abs(theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[1]
                if 'done' in fightingBar[bar][2]:
                    fightSuccess = True
                    x = fightBarX2[i]
                else:
                    x = startSpot - x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x

                if (x <= 0) and (not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            x = fightBarX2[i]
                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0

                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True
                    barAlpha[i] = max(0, barAlpha[i] - 40)

                if fightSuccess and barAlpha[i] - 40 > 0:
                    #barColor = YELLOW
                    fightScale[i] += 0.2
                    barAlpha[i] -= 40
                elif barAlpha[i] - 40 <= 0 or fightBarX2[i] < -10:
                    barNoMore = True

                if abs(2.5 * math.pi - fightBarX2[i]) <= 0.3 and fightSuccess:
                    fightBarX2[i] = 2.5 * math.pi
                    #fightBarX = 0.2
                    x = 2.5 * math.pi
                    critHit = True
                    barColor = (255, 255, 0)

                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i])
                darkColor = (0.6*barColor[0], 0.6*barColor[1], 0.6*barColor[2], barAlpha[i])
                black = (0, 0, 0, barAlpha[i])




                if not barNoMore:
                    stupidX = math.cos(x) * (71 * x * 0.25) / math.pi + hudRect[2]*1.5/2
                    stupidY = math.sin(x) * (-71 * x * 0.25) / math.pi + hudRect[3]*1.5/2
                    drawCircle(ringThing, darkColor, (stupidX, stupidY), 16*fightScale[i])
                    drawCircle(ringThing, FinalBarColor, (stupidX, stupidY), 16*fightScale[i] - 3)
                    blitObj(hud, ringThing, hudRect[0], hudRect[1])
                    ringThing.fill((0, 0, 0, 0))

                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in fightingBar[bar][2]:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not ((critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot)):
                    critHitBool = False
                if strike:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = abs(2.5 * math.pi - fightBarX2[i])
                        attackMeterWidth = math.pi * 5
                        maxDistance = attackMeterWidth / 2
                        damagePercent = (theBase - (distance / maxDistance)*multiply)
                        if (abs(distance) < 0.3 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            damagePercent = 1*abs(multiply)
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = abs(2.5 * math.pi - fightBarX2[barNum])
                                attackMeterWidth = math.pi * 5
                                maxDistance = attackMeterWidth /2
                                damagePercent = (theBase - (distance / maxDistance)*multiply)
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                if abs(fightingBar[barBar][8] - 100*damagePercent) < 5 and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done':
                                    fightingBar[barBar][2] = 'done'
                                    fightingBar[barBar][7].currentBar = fightingBar[barBar][10]
                                    theBar = fightingBar[barBar][7].bars
                                    fightingBar[barBar][7].nextBar = theBar[ min(theBar.index(fightingBar[barBar][10]) + 1, len(theBar) - 1 )]
                                    #playSound('Attack_sfx.ogg')
                                if (abs(distance) < 0.3 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                                    damagePercent = 1*abs(multiply)
                                trueDamage = damage * damagePercent
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount

def backBarBlit():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    global botplay
    fightFrame += 1
    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            fightFrame -= 10
            if 'Back' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Back' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1

    startSpot = hudRect[0] + 527/2
    attackMeterX = hudRect[4] + 90
    #botplay = False

    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.6
        multiply = -1.7 if hardMode else -1.3
        baseNum = -3.2 * theDelta if not easyMode else 2.6*theDelta
    else:
        theBase = 1
        multiply = 1
        baseNum = -2.1 * theDelta

    for i, bar in enumerate(fightBar[:inBar]):

            if 'NoBar' in bar or not 'Back' in bar:
                continue
            else:
                barColor = fightingBar[bar][6].color
                allyNum = theAlly.index(fightingBar[bar][6])
                identifier = ''
                for strI in fightingBar[bar][10]:
                    if not strI.isdigit():
                        identifier += strI
                    else:
                        break
                theAttack = fightingBar[bar][7]
                if ((theAttack.nextBar == fightingBar[bar][10])
                    or theAttack.bars.index(fightingBar[bar][10]) == 0):
                    fightingBar[bar][11] = True
                if fightingBar[bar][11] == False:
                    continue


                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = abs(theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[1]
                if 'done' in fightingBar[bar][2]:
                    fightSuccess = True
                    x = fightBarX2[i]
                else:
                    x = startSpot + 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x

                if (x <= hudRect[4]) and (not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            x = fightBarX2[i]
                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0
                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True
                    barAlpha[i] = max(0, barAlpha[i] - 40)


                if fightSuccess and barAlpha[i] - 40 > 0:
                    #barColor = YELLOW
                    fightScale[i] += 0.1
                    barAlpha[i] -= 40
                elif barAlpha[i] - 40 <= 0 or fightBarX2[i] < -10:
                    barNoMore = True

                if abs(attackMeterX - fightBarX2[i]) <= 10 and fightSuccess:
                    fightBarX2[i] = attackMeterX
                    x = attackMeterX
                    critHit = True
                    barColor = (255, 255, 0)

                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i])




                if not barNoMore:
                    meter = loadImg(('meter.png', fightScale[i], FinalBarColor))
                    blitObj(hud, meter, x, y)

                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in fightingBar[bar][2]:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not ((critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot)):
                    critHitBool = False
                if strike:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = abs(attackMeterX - fightBarX2[i])
                        attackMeterWidth = attack_rect.width
                        maxDistance = hudRect[2] - 90 + hudRect[4] if fightBarX2[i] <= attackMeterX else 90
                        distance = distance if fightBarX2[i] <= attackMeterX else (fightBarX2[i] - hudRect[4] - (hudRect[2] - 90))
                        damagePercent = (theBase - (distance / maxDistance)*multiply)
                        if (abs(distance) < 10 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            damagePercent = 1*abs(multiply)
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = abs(attackMeterX - fightBarX2[barNum])
                                attackMeterWidth = attack_rect.width
                                maxDistance = hudRect[2] - 90 + hudRect[4] if fightBarX2[barNum] >= attackMeterX else 90
                                distance = distance if fightBarX2[barNum] >= attackMeterX else 90 - (fightBarX2[barNum] - hudRect[4])
                                damagePercent = (theBase - (distance / maxDistance)*multiply)
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                if abs(fightingBar[barBar][8] - 100*damagePercent) < 5 and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done':
                                    fightingBar[barBar][2] = 'done'
                                    fightingBar[barBar][7].currentBar = fightingBar[barBar][10]
                                    theBar = fightingBar[barBar][7].bars
                                    fightingBar[barBar][7].nextBar = theBar[ min(theBar.index(fightingBar[barBar][10]) + 1, len(theBar) - 1 )]
                                    #playSound('Attack_sfx.ogg')
                                if (abs(distance) < 10 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                                    damagePercent = 1*abs(multiply)
                                trueDamage = damage * damagePercent
                                if fightBarX2[barNum] <= 35:
                                    trueDamage = 0
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount

def slamBarBlit():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    global botplay
    fightFrame += 1
    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            fightFrame -= 10
            if 'Slam' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Slam' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1

    attackMeterX = hudRect[4] + hudRect[2] - 90
    startSpot = hudRect[0] - 527/2    #botplay = False

    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.6
        multiply = -1.7 if hardMode else -1.3
        baseNum = 3.2 * theDelta if not easyMode else 2.6*theDelta
    else:
        theBase = 1
        multiply = 1
        baseNum = 2.1 * theDelta

    for i, bar in enumerate(fightBar[:inBar]):

            if 'NoBar' in bar or not 'Slam' in bar:
                continue
            else:

                barColor = fightingBar[bar][6].color
                allyNum = theAlly.index(fightingBar[bar][6])
                identifier = ''
                for strI in fightingBar[bar][10]:
                    if not strI.isdigit():
                        identifier += strI
                    else:
                        break
                theAttack = fightingBar[bar][7]
                if ((theAttack.nextBar == fightingBar[bar][10])
                    or theAttack.bars.index(fightingBar[bar][10]) == 0):
                    fightingBar[bar][11] = True
                if fightingBar[bar][11] == False:
                    continue


                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = abs(theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[1]
                if 'done' in fightingBar[bar][2]:
                    fightSuccess = True
                    x = fightBarX2[i]
                else:
                    x = startSpot + 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x

                if (x >= (hudRect[2] + hudRect[4]) and not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            x = fightBarX2[i]
                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0
                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True
                    barAlpha[i] = max(0, barAlpha[i] - 40)



                if (fightSuccess or fightFail) and barAlpha[i] - 40 > 0:
                    fightScale[i] += 0.1 if fightSuccess else 0
                    barAlpha[i] -= 40
                elif barAlpha[i] - 40 <= 0:
                    barNoMore = True

                if abs(attackMeterX - fightBarX2[i]) <= 10 and fightSuccess:
                    fightBarX2[i] = attackMeterX
                    x = attackMeterX
                    critHit = True
                    barColor = (255, 255, 0)

                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i])




                if not barNoMore:

                    meter = loadImg(('meter.png', fightScale[i], FinalBarColor))
                    meter_rect = meter.get_rect(center=(x, y))
                    blitObj(hud, meter, x, y)

                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in fightingBar[bar][2]:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not ((critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot)):
                    critHitBool = False
                if strike:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = abs(attackMeterX - fightBarX2[i])
                        attackMeterWidth = attack_rect.width
                        maxDistance = hudRect[2] - 90 + hudRect[4] if fightBarX2[i] <= attackMeterX else 90
                        distance = distance if fightBarX2[i] <= attackMeterX else (fightBarX2[i] - hudRect[4] - (hudRect[2] - 90))
                        damagePercent = (theBase - (distance / maxDistance)*multiply)
                        if (distance <= 10 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            damagePercent = 1*abs(multiply)
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = abs(attackMeterX - fightBarX2[barNum])
                                attackMeterWidth = attack_rect.width
                                maxDistance = hudRect[2] - 90 + hudRect[4] if fightBarX2[barNum] <= attackMeterX else 90
                                distance = distance if fightBarX2[barNum] <= attackMeterX else (fightBarX2[barNum] - hudRect[4] - (hudRect[2] - 90))
                                damagePercent = (theBase - (distance / maxDistance)*multiply)
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                if abs(fightingBar[barBar][8] - 100*damagePercent) < 5 and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done':
                                    fightingBar[barBar][2] = 'done'
                                    fightingBar[barBar][7].currentBar = fightingBar[barBar][10]
                                    theBar = fightingBar[barBar][7].bars
                                    fightingBar[barBar][7].nextBar = theBar[ min(theBar.index(fightingBar[barBar][10]) + 1, len(theBar) - 1 )]
                                    #playSound('Attack_sfx.ogg')
                                if (distance <= 10 and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                                    damagePercent = 1*abs(multiply)
                                trueDamage = damage * damagePercent
                                if fightBarX2[barNum] <= 35:
                                    trueDamage = 0
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount

holdTimer = 3
def holdBlit():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    global holdTimer
    #attackMeterX = hudRect[2]/2
    fightFrame += 1
    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            fightFrame -= 10
            if 'Hold' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Hold' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1
    global hardMode
    hardMode = False
    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.2
        multiply = -1.7 if hardMode else -1
        baseNum = 4.3 * theDelta if not easyMode else 3.1 * theDelta
    else:
        theBase = 1
        multiply = 1
        baseNum = 4.2 * theDelta

    try:
        ringThing
    except NameError:
        ringThing = pygame.Surface((hudRect[2]*1.5,hudRect[3]*1.5), pygame.SRCALPHA)

    startSpot = 630
    if ringThing.get_width() != hudRect[2]*1.5 and ringThing.get_height() != hudRect[3]*1.5:
        ringThing = pygame.Surface((hudRect[2]*1.5,hudRect[3]*1.5), pygame.SRCALPHA)

    for i, bar in enumerate(fightBar[:inBar]):

            if 'NoBar' in bar or not 'Hold' in bar:
                continue
            else:

                dashPassed = 0
                name = ''
                classes = ''
                identifier = ''
                for letter in bar:
                    if dashPassed == 1:
                        if letter == '_':
                            dashPassed = 2
                        else:
                            classes += letter
                    elif dashPassed == 2:
                        if letter.isdigit():
                            dashPassed = 3
                        else:
                            identifier += letter
                    elif letter == '_':
                        dashPassed = 1
                    elif dashPassed == 0:
                        name += letter
                #print(in

                for num, ally in enumerate(theAlly):
                    if ally.name == name:
                        barColor = color[num]
                        allyNum = num

                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = (theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                drawRect(hud, (0, 200, 200), hudRect[4], hudRect[5], 20)

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[1]

                confirmTouched = False
                if useMobile:
                    confirmButton = loadSprite('confirm', f'controls/confirm.png', (820, 380), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
                    if mouseTouch(confirmButton, False, True):
                        confirmTouch = True
                #print(fightBarX2[i])
                if botplay and fightBarX2[i] >= 220:
                    confirmTouched = True
                
                keys = pygame.key.get_pressed()
                if (keys[screenWindow.keyBind['Confirm']] or confirmTouched or (turnEnemy and enemyAutoAttack and opponentBot)) and holdTimer < 2.9:
                    #print(holdTimer)
                    #print(2)
                    if fightingBar[bar][2] != 'done' and fightingBar[bar][2] != 'failHit':
                        #print(2)
                        fightingBar[bar][2] = 'start'
                elif not confirmTouched and not keys[screenWindow.keyBind['Confirm']] and not (turnEnemy and enemyAutoAttack and opponentBot):
                    #print(True)
                    if fightingBar[bar][2] == 'start':
                        #print(1, frame)
                        fightingBar[bar][2] = 'done'

                timeLength = 210 * (holdTimer) / 3
                holdTimer -= abs(theDelta)/15
                if holdTimer <= 0:
                    fightingBar[bar][2] = 'failHit'

                hpBG_X = hudRect[5] + hudRect[3] - 220 #- 220/2
                hpBG_Y = hudRect[4] - 60 #- 30
                hpX = hpBG_X + 5
                hpY = hpBG_Y + 5

                drawRect(hud, (0, 150, 150, barAlpha[i]), (hpBG_Y, hpBG_X, 35, 220)) # The HPBG one
                drawRect(hud, (0, 200, 200, barAlpha[i]), (hpY, hpX, 25, 210)) # The MAX HP one
                drawRect(hud, (0, 255, 255, barAlpha[i]), (hpY, hpX+210-timeLength, 25, timeLength)) # The HP one

                #txt = render_text(f'{round(fightBarX2[i], 2)}', WHITE, 60, True, BLACK, 3)
                #blitObj(hud, txt, hudRect[0], hudRect[5] + 30)

                if 'bash' in bar:
                    x = startSpot - 45 * (x**2 - 3*x + 3)
                    fightBarX[i] += baseNum/7 * speedModifier
                    fightBarX2[i] = x
                elif 'range' in bar:
                    x = startSpot - 60*x
                    fightBarX[i] += baseNum/4 * speedModifier
                    fightBarX2[i] = x
                elif 'magic' in bar:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/5 * speedModifier
                    fightBarX2[i] = x
                elif 'slash' in bar:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x
                elif 'done' == fightingBar[bar][2]:
                    fightSuccess = True
                    x = fightBarX2[i]
                elif 'start' == fightingBar[bar][2]:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x
                else:
                    x = fightBarX2[i]



                if (x <= 0 and not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            #print(True)
                            x = fightBarX2[i]

                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])

                            #barColor = (255, 0, 0)
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0
                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True

                if (fightSuccess or fightFail) and barAlpha[i] - 20 > 0:
                    fightScale[i] += 0.02
                    barAlpha[i] -= 20
                elif barAlpha[i] - 20 <= 0:
                    barNoMore = True
                    barAlpha[i] = 0

                if 162 <= fightBarX2[i] <= 253 and fightSuccess:
                    critHit = True
                    barColor = (255, 255, 0)

                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i]*0.7)
                darkColor = (0.6*barColor[0], 0.6*barColor[1], 0.6*barColor[2], barAlpha[i])
                black = (0, 0, 0, barAlpha[i])




                if not barNoMore:
                    #img = loadImg(('attackHoldMeter.png', 0.25, FinalBarColor), blendMode='ADD')
                    #img.set_alpha(125)
                    #print((fightBarX2[i]/startSpot)*(img.get_width()/2)/scaleFactor )
                    drawCircle(ringThing, darkColor, ((ringThing.get_width()/2)/scaleFactor, (ringThing.get_height()/2)/scaleFactor), 112 * (1 - (fightBarX2[i] / startSpot)))
                    drawCircle(ringThing, FinalBarColor, ((ringThing.get_width()/2)/scaleFactor, (ringThing.get_height()/2)/scaleFactor), 105 * (1 - (fightBarX2[i] / startSpot)))
                    blitObj(hud, ringThing, hudRect[0], hudRect[1])
                    #drawRing(hud, FinalBarColor, (hudRect[0], hudRect[1]), 160 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1),
                      #       15*(fightBarX2[i] / startSpot), 5*(fightBarX2[i] / startSpot), darkColor)
                    #drawCircle(ringThing, darkColor, ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 165 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1), int(5))
                    #drawCircle(ringThing, FinalBarColor, ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 160 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1), int(15 * (fightBarX2[i] / startSpot)))
                    #drawCircle(ringThing, darkColor, ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 145 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1), int(5 * (fightBarX2[i] / startSpot)))
                    #drawCircle(ringThing, (0, 0, 0, 0), ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 140 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1))
                    #blitObj(hud, ringThing, hudRect[0], hudRect[1])

                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in bar:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not (critHit and not (turnEnemy and opponentBot)) or not (fightFail and turnEnemy and opponentBot):
                    critHitBool = False
                if strike:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = fightBarX2[i]
                        attackMeterWidth = attack_rect.width
                        maxDistance = startSpot
                        damagePercent = (theBase - (distance / maxDistance)*multiply)
                        if (critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            damagePercent = 1*abs(multiply)
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = fightBarX2[barNum]
                                attackMeterWidth = attack_rect.width
                                maxDistance = startSpot
                                if 162 <= distance <= 253:
                                    critBoost += 0.2
                                    #distance = 0
                                else:
                                    critHitBool = False
                                if distance < 162:
                                    damagePercent = min(1, (theBase - ((162 - distance) / 162)*multiply))
                                    #print(damagePercent, distance, ((162 - distance) / 162), theBase)
                                else:
                                    damagePercent = min(1, (theBase - ((distance-253)) / (maxDistance - 253))*multiply)
                                #print(damagePercent, distance)
                                #damagePercent = min(1, (theBase - (distance / maxDistance)*multiply))
                                if 162 <= distance <= 253:
                                    #print(True)
                                    damagePercent = 1
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                if abs(fightingBar[barBar][8] - 100*damagePercent) < 10 and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done':
                                    fightingBar[barBar][2] = 'done'
                                    #playSound('slice.wav')

                                trueDamage = damage * damagePercent# * critBoost
                                if fightBarX2[barNum] <= 35:
                                    trueDamage = 0
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount

def discBlit():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    #attackMeterX = hudRect[2]/2
    fightFrame += 1
    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            fightFrame -= 10
            if 'Range' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Range' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1
    global hardMode
    hardMode = False
    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.2
        multiply = -1.7 if hardMode else -1
        baseNum = 4.3 * theDelta if not easyMode else 3.1 * theDelta
    else:
        theBase = 1
        multiply = 1
        baseNum = 4.2 * theDelta

    try:
        ringThing
    except NameError:
        ringThing = pygame.Surface((hudRect[2]*1.5,hudRect[3]*1.5), pygame.SRCALPHA)

    startSpot = 630
    if ringThing.get_width() != hudRect[2]*1.5 and ringThing.get_height() != hudRect[3]*1.5:
        ringThing = pygame.Surface((hudRect[2]*1.5,hudRect[3]*1.5), pygame.SRCALPHA)

    for i, bar in enumerate(fightBar[:inBar]):

            if 'NoBar' in bar or not 'Range' in bar:
                continue
            else:


                barColor = fightingBar[bar][6].color
                allyNum = theAlly.index(fightingBar[bar][6])
                identifier = ''
                for strI in fightingBar[bar][10]:
                    if not strI.isdigit():
                        identifier += strI
                    else:
                        break
                theAttack = fightingBar[bar][7]
                if ((theAttack.nextBar == fightingBar[bar][10])
                    or theAttack.bars.index(fightingBar[bar][10]) == 0):
                    fightingBar[bar][11] = True
                if fightingBar[bar][11] == False:
                    continue


                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = (theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[1]
                if 'bash' in bar:
                    x = startSpot - 45 * (x**2 - 3*x + 3)
                    fightBarX[i] += baseNum/7 * speedModifier
                    fightBarX2[i] = x
                elif 'magic' in bar:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/5 * speedModifier
                    fightBarX2[i] = x
                elif 'slash' in bar:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x
                elif 'done' in fightingBar[bar][2]:
                    #print(True)
                    fightSuccess = True
                    x = fightBarX2[i]
                else:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x
                #print(fightingBar[bar][2])

                if (x <= 0 and not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            x = fightBarX2[i]
                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])

                            barColor = (255, 0, 0)
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0
                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True

                if fightSuccess and barAlpha[i] - 40 > 0:
                    fightScale[i] += 0.02
                    barAlpha[i] -= 40
                elif barAlpha[i] - 40 <= 0 or fightBarX2[i] < -10:
                    barNoMore = True

                if 90 <= fightBarX2[i] <= 167 and fightSuccess:
                    critHit = True
                    barColor = (255, 255, 0)

                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i])
                darkColor = (0.6*barColor[0], 0.6*barColor[1], 0.6*barColor[2], barAlpha[i])
                black = (0, 0, 0, barAlpha[i])




                if not barNoMore:
                    drawRing(hud, FinalBarColor, (hudRect[0], hudRect[1]), 160 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1),
                             15*(fightBarX2[i] / startSpot), 5*(fightBarX2[i] / startSpot), darkColor)
                    #drawCircle(ringThing, darkColor, ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 165 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1), int(5))
                    #drawCircle(ringThing, FinalBarColor, ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 160 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1), int(15 * (fightBarX2[i] / startSpot)))
                    #drawCircle(ringThing, darkColor, ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 145 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1), int(5 * (fightBarX2[i] / startSpot)))
                    #drawCircle(ringThing, (0, 0, 0, 0), ((hudRect[2]*1.5)/2, (hudRect[3]*1.5)/2), 140 * (fightBarX2[i] / startSpot) + 70*(fightScale[i] - 1))
                    #blitObj(hud, ringThing, hudRect[0], hudRect[1])

                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in bar:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not (critHit and not (turnEnemy and opponentBot)) or not (fightFail and turnEnemy and opponentBot):
                    critHitBool = False
                if strike:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = fightBarX2[i]
                        attackMeterWidth = attack_rect.width
                        maxDistance = startSpot
                        damagePercent = (theBase - (distance / maxDistance)*multiply)
                        if (critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            damagePercent = 1*abs(multiply)
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = fightBarX2[barNum]
                                attackMeterWidth = attack_rect.width
                                maxDistance = startSpot
                                if 90 <= distance <= 167:
                                    critBoost += 0.2
                                    distance = 0
                                else:
                                    critHitBool = False
                                damagePercent = min(1, (theBase - (distance / maxDistance)*multiply))
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                if abs(fightingBar[barBar][8] - 100*damagePercent) < 10 and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done':
                                    fightingBar[barBar][2] = 'done'
                                    fightingBar[barBar][7].currentBar = fightingBar[barBar][10]
                                    theBar = fightingBar[barBar][7].bars
                                    fightingBar[barBar][7].nextBar = theBar[ min(theBar.index(fightingBar[barBar][10]) + 1, len(theBar) - 1 )]
                                    #playSound('Attack_sfx.ogg')

                                trueDamage = damage * damagePercent# * critBoost
                                if fightBarX2[barNum] <= 35:
                                    trueDamage = 0
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount


def barBlit():
    global fightFrame
    global fightBarX
    global fightBarX2
    global fightBar
    global inBar
    global barAlpha
    global barScale
    global allyDamage
    global botplay
    currentIdentifier = ''
    dashPassed = 0
    fightFrame += 1

    if fightFrame >= 10 and inBar < len(fightBar):
        if random.randint(1, 10) > 4:
            forceChange = True
            fightFrame = 0
            if 'Melee' in fightBar[inBar]:
                inBar += 1
            else:
                while 'Melee' not in fightBar[max(inBar-1,0)] or inBar == -1:
                    inBar += 1
                #forceChange = False

    startSpot = hudRect[0] + 527/2#hudRect[4] + hudRect[2]
    attackMeterX = hudRect[0]

    if opponentBot and turnEnemy and not enemyAutoAttack:
        theBase = 0.9 if hardMode else 0.6
        multiply = -1.7 if hardMode else -1.3
        baseNum = 3.2 * theDelta if not easyMode else 2.6*theDelta
    else:
        theBase = 1
        multiply = 1
        baseNum = 2.1 * theDelta

    for i, bar in enumerate(fightBar[:inBar]):
            #continue
            if 'NoBar' in bar or not 'Melee' in bar or barAlpha[i] == 0:
                continue
            else:

                barColor = fightingBar[bar][6].color
                allyNum = theAlly.index(fightingBar[bar][6])
                identifier = ''
                for strI in fightingBar[bar][10]:
                    if not strI.isdigit():
                        identifier += strI
                    else:
                        break
                theAttack = fightingBar[bar][7]
                if ((theAttack.nextBar == fightingBar[bar][10])
                    or theAttack.bars.index(fightingBar[bar][10]) == 0):
                    fightingBar[bar][11] = True
                if fightingBar[bar][11] == False:
                    continue


                if opponentBot and turnEnemy:
                    speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                else:
                    speedDifference = abs(theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                    speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)

                if speedModifier < 0.7:
                    speedModifier = 0.7
                if speedModifier > 2.5:
                    speedModifier = 2.5

                fightSuccess = False
                barNoMore = False
                fightFail = False
                critHit = False
                critBoost = 1
                x = fightBarX[i]
                y = hudRect[1]
                if 'bash' in bar:
                    x = startSpot - 45 * (x**2 - 3*x + 3)
                    fightBarX[i] += baseNum/7 * speedModifier
                    fightBarX2[i] = x
                elif 'range' in bar:
                    x = startSpot - 60*x
                    fightBarX[i] += baseNum/4 * speedModifier
                    fightBarX2[i] = x
                elif 'magic' in bar:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/5 * speedModifier
                    fightBarX2[i] = x
                elif 'slash' in bar:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x
                elif 'done' in fightingBar[bar][2]:
                    fightSuccess = True
                    x = fightBarX2[i]
                else:
                    x = startSpot - 55*x
                    fightBarX[i] += baseNum/6 * speedModifier
                    fightBarX2[i] = x




                if (x <= hudRect[4] and not 'failHit' in fightingBar[bar][2]) and fightingBar[bar][2] != 'done':
                    if opponentBot and turnEnemy and not enemyAutoAttack:
                        fightingBar[bar][2] = 'done'
                        fightSuccess = True
                        x = fightBarX2[i]
                        print(True)
                    else:
                        if not easyMode:
                            fightFail = True
                            fightingBar[bar][2] = f'failHit'
                            x = fightBarX2[i]
                            barAlpha[i] -= 40
                            barAlpha[i] = max(0, barAlpha[i])

                            barColor = (255, 0, 0)
                        else:
                            fightBarX2[i] = startSpot
                            fightBarX[i] = 0
                if 'failHit' in fightingBar[bar][2]:
                    fightFail = True

                if (fightSuccess or fightFail) and barAlpha[i] - 40 > 0:
                    fightScale[i] += 0.1 if fightSuccess else 0
                    barAlpha[i] -= 40
                elif barAlpha[i] - 40 <= 0:
                    barNoMore = True
                    barAlpha[i] = 0

                if abs(attackMeterX - fightBarX2[i]) <= 10 and fightSuccess:
                    fightBarX2[i] = attackMeterX
                    x = attackMeterX
                    critHit = True
                    barColor = (255, 255, 0)

                FinalBarColor = (barColor[0], barColor[1], barColor[2], barAlpha[i])




                if not barNoMore:

                    meter = loadImg(('meter.png', fightScale[i], FinalBarColor))
                    meter_rect = meter.get_rect(center=(x, y))
                    blitObj(hud, meter, x, y)

                #if 'done' in fightBar[i]:
                strike = True
                for bar in fightBar:
                    if 'done' not in fightingBar[bar][2] and 'failHit' not in fightingBar[bar][2]:
                        if theAlly[allyNum].name in fightingBar[bar][2]:
                            strike = False
                    elif 'failHit' in fightingBar[bar][2]:
                        strike = True

                weapon = theAlly[allyNum].weapon.type
                critHitBool = True
                if not ((critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot)):
                    critHitBool = False
                if strike:# and 1==0:
                    if fightingBar[bar][0] == False:
                        if useDefensePercent:
                            damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                        else:
                            damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                        distance = abs(attackMeterX - fightBarX2[i])
                        attackMeterWidth = attack_rect.width
                        maxDistance = attackMeterWidth /2
                        damagePercent = (theBase - (distance / maxDistance)*multiply)
                        if (critHit and not (turnEnemy and opponentBot)) or (fightFail and turnEnemy and opponentBot):
                            damagePercent = 1*abs(multiply)
                        trueDamage = damage * damagePercent
                        fightingBar[bar][5] = trueDamage
                        critBoost += 0.3
                    else:
                        damageList = 0
                        damageCount = 0
                        damagelist = []
                        barUsed = [bar]
                        for barNum, barBar in enumerate(fightBar):
                            #if 'done' not in fightingBar[barBar][2]:
                                #continue
                            secondIdentifier = ''
                            dashPassed = 0
                            for letter in barBar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    secondIdentifier += letter if not letter.isdigit() else ''
                            if identifier in secondIdentifier and theAlly[allyNum] == fightingBar[barBar][6]:
                                barUsed.append(barBar)
                                damageCount += 1
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                distance = abs(527/2 - (fightBarX2[barNum] - (  hudRect[0]-527/2  ) ))
                                attackMeterWidth = 527
                                maxDistance = attackMeterWidth /2
                                damagePercent = (theBase - (distance / maxDistance)*multiply)
                                fightingBar[barBar][4] = round(damagePercent, 2)
                                #print(round(damagePrcent, 2))
                                #print(True)
                                if (fightingBar[barBar][8] <= 100*damagePercent) and (turnEnemy and opponentBot and enemyAutoAttack) and fightingBar[barBar][2] != 'done' and fightingBar[barBar][2] != 'failHit':
                                    fightingBar[barBar][2] = 'done'
                                    fightingBar[barBar][7].currentBar = fightingBar[barBar][10]
                                    theBar = fightingBar[barBar][7].bars
                                    fightingBar[barBar][7].nextBar = theBar[ min(theBar.index(fightingBar[barBar][10]) + 1, len(theBar) - 1 )]
                                    #print(fightingBar[barBar][10])
                                    #playSound('Attack_sfx.ogg')
                                if distance <= 10:
                                    critBoost += 0.2
                                else:
                                    critHitBool = False
                                trueDamage = damage * damagePercent * critBoost
                                if fightBarX2[barNum] <= 35:
                                    trueDamage = 0
                                damageList += trueDamage
                                damagelist.append(trueDamage)
                        critBoost = 1.3
                        if damageCount > 0:
                            for i in barUsed:
                                fightingBar[i][5] = damageList/damageCount


                            trueDamage = damageList/damageCount

def colorTween(colorA, colorB, time):
    r = colorA[0] + (colorB[0] - colorA[0]) * time
    g = colorA[1] + (colorB[1] - colorA[1]) * time
    b = colorA[2] + (colorB[2] - colorA[2]) * time
    return int(r), int(g), int(b)

def resetAllyTurn():
    global speedNum, speedNumOrder, turnAlly, turnEnemy, turn, cycle, allyCycle, enemyCycle, progressTurn
    selectedEnemy = 0
    enemyAction = []
    enemySelection = []

    selectedAlly = 0
    selectedEnemy = 0
    allyAction = []
    battleSplash = True
    allySelection = []
    allyTurn = True
    opponentTurn = False
    tempAlly = len(party) + 1
    inAct = False
    actionDia = []
    actionNum = 0
    actUsed = []
    actParty = 0
    inItem = False
    itemParty = 0
    itemHeal = []
    itemUsed = []
    attackFrame = []
    fightBar = []
    barIsAttacking = []
    fightBarX = []
    fightBarX2 = []
    fightScale = []
    barAlpha = []
    allyStrike = []
    allyAttack = []
    allyDamage = []
    opponentSmoothDamage = []
    inBar = 0
    fightFrame = 0
    inFight = False
    barSelect = 0
    damageX = []
    damageY = []
    damageY2 = []
    attackFade = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    skillUsed = []
    skillParty = 0
    itemNum = []
    keyHit = []
    keyUsed = []
    keyDone = []
    keyUsedBool = []
    fightUsed = []
    whichAction = []

    splashText(None, False, 0)

    meleeDone = throwerDone = rangeDone = controllerDone = supportDone = tankDone = underDone = slamDone = backDone = holdDone = False

    for i in (party + opponent):
        allyAttack.append(False)
        allyDamage.append(0)
        whichAction.append(0)
        i.tempClass = ''
        i.updateTurn()
        for j in i.fight:
            j.currentBar = j.nextBar = j.bars[0]

    for i in opponent:
        enemyShakeX.append(0)
        enemyShakeBool.append(False)
        enemySelection.append(0)
        enemyAction.append(None)
        i.newNum = copy.copy(i.setNum)
        i.levelUp(0)
        itemHeal.append(0)

    for i in party:
        playerShakeX.append(0)
        playerShakeBool.append(False)
        allyTween.append(0)
        allySelection.append(0)
        itemHeal.append(0)
        allyAction.append(None)
        whichAction.append(0)
        allyStrike.append(False)
        skillUsed.append(0)
        itemNum.append(0)
        i.newNum = copy.copy(i.setNum)
        i.levelUp(0)



    if progressTurn:
        speedNumOrder += 1

    if speedBasedTurn:
        if speedNumOrder >= len(speedOrder):
            speedNumOrder = 0
            cycle += 1

        if speedOrder[speedNumOrder][2] == 'Player':
            selectedAlly = speedOrder[speedNumOrder][1]
            speedNum = selectedAlly
            enemyTurn = False
            allyTurn = True
            turnAlly = True
            turnEnemy = False
            theAlly = party
            selectWho = selectedAlly
            dacycle = newCycle

        elif speedOrder[speedNumOrder][2] == 'Enemy':
            selectedEnemy = speedOrder[speedNumOrder][1]
            speedNum = selectedEnemy
            enemyTurn = True
            allyTurn = False
            turnEnemy = True
            turnAlly = False
            theAlly = opponent
            selectWho = selectedEnemy
            dacycle = newCycle

        if progressTurn:
            dacycle[theAlly[selectWho]] += 1

        if theAlly[selectWho].hp > 0:
            turn += 1
            print(True)
            for ally in party:
                if ally.hp <= 0:
                    continue
                for i in ally.buff:
                    character.effectStuff[(i, ally)] = [ally.buff[i][0], ally, False, ally.buff[i][1], ally.buff[i][2], ally.buff[i][3]]

                for i in ally.passiveBuff:
                    character.effectStuff[(i, ally)] = [ally, ally.passiveBuff[i][1], 'Passive']

            for enemy in opponent:
                if enemy.hp <= 0:
                    continue
                for i in enemy.buff:
                    character.effectStuff[(i, enemy)] = [enemy.buff[i][0], enemy, False, enemy.buff[i][1], enemy.buff[i][2], enemy.buff[i][3]]

                for i in enemy.passiveBuff:
                    character.effectStuff[(i, enemy)] = [enemy, enemy.passiveBuff[i][1], 'Passive']

    else:
        if turnAlly == True:
            turnEnemy = True
            turnAlly = False
            enemyTurn = True
        elif turnEnemy == True:
            turnEnemy = False
            turnAlly = True
            allyTurn = True
        turn += 1

    for players in party + opponent:
        if 'Death' not in players.status:
            players.status = "Neutral"
            #triggerEvent(players, "Hurt")

    progressTurn = True

    locals_dict = locals() # Loads in all local variables in this functions
    for var_name, var_value in locals_dict.items(): # Go through all local variables
        if var_name != 'my_function':  # Exclude all the function itself
            globals()[var_name] = var_value # Set those Variables as local


def addBattleText(text, size, start):
    global textBox
    displayed_lines = []
    current_line = ''
    current_width = 0
    font = pygame.font.Font("gameFont.otf", int(40*0.9))
    maximum = hudRect[2] - 2*hudRect[6] - 40

    # Process each character in the text up to the current text_index
    for char in text:
              # Exclude spaces from width calculation
            #current_width += font.size(char)[0]/3
            # Check for punctuation marks and handle line breaks if width exceeds max_width
            if char in [";"]:
                if current_width > maximum:
                    displayed_lines.append(current_line)
                    current_line = ""

                    current_width = 0
                current_line += char
                displayed_lines.append(current_line)
                current_line = ""
                current_width = 0
            elif char == "\n":  # Handle explicit line breaks
                displayed_lines.append(current_line)
                current_line = ""
                current_width = 0
            elif current_width > maximum:  # Start a new line if width exceeds max_width
                ##print(current_width, hudRect[2], hudRect[4])
                if char == " ":
                    displayed_lines.append(current_line)
                    current_line = ""
                    current_width = 0
                else:
                    # Find the last space in the current line
                    last_space_index = current_line.rfind(" ")
                    if last_space_index != -1:  # If space found, break the line at the last space
                        displayed_lines.append(current_line[:last_space_index])
                        current_line = current_line[last_space_index + 1:] + char
                        current_width = font.size(current_line)[0]
                    else:  # If no space found, break the line at the current character
                        displayed_lines.append(current_line)
                        current_line = char
                        current_width = font.size(char)[0]
            else:
                current_line += char
                current_width += font.size(char)[0]

    # Append any remaining text in current_line
    if current_line:
        displayed_lines.append(current_line)

    for num, line in enumerate(displayed_lines):
        lineText = render_text(line, (100, 100, 100), 40)
        text_offset =  hudRect[5] + 18 + (num + 1)*40
        blitObj(hud, lineText, hudRect[4] + 20, text_offset, 'topleft')
    textBox = 18*2 + (2 + len(displayed_lines))*40

    displayed_lines = []
    current_line = ''
    return text_offset

def addInBar():
    holdTimer = 3
    attackFrame = []
    fightBar = []
    fightingBar = {}
    fightBarX = []
    fightBarX2 = []
    fightScale = []
    barAlpha = []
    allyStrike = []
    allyDamage = []
    opponentSmoothDamage = []
    inBar = 1
    fightFrame = 0
    fightBarExtra = []
    keyIsUsed = [False, False, False, False]
    for num, ally in enumerate(theAlly):
        if actionWhich[num] == 'Fight':
            if 'bash' in ally.weapon.type:
                fightBar.append(f'bash_{theAlly[num].name}_{ally.tempClass}')
            elif 'slash' in ally.weapon.type or 1==1:
                #for i in range(65,67):
                for bar in ally.fight[whichAction[num]].bars:


                    fightBar.append(f'{theAlly[num].name}_{ally.tempClass}_{bar}')
                    fightingBar[f'{theAlly[num].name}_{ally.tempClass}_{bar}'] = [True, True, '', 1, 0, 0, ally, ally.fight[whichAction[num]], random.randint(80, 95), ally.tempClass, bar, ally.fight[whichAction[num]].allAtOnce, 0]
                    #2=Bar State, 3=Bar Speed, 4=Damage, 6=Ally, 7=FightUsed, 8=damagePercent, 9=class, 10=barUsed, 11=ShouldProceed, #12 Miss Bool
                    #fightBar.append(f'{theAlly[num].name}_{ally.tempClass}_{chr(i)}1')
                    #fightingBar[f'{theAlly[num].name}_{ally.tempClass}_{chr(i)}1'] = [True, True, '', 1, 0, 0, ally]
            elif 'range' in ally.weapon.type:
                for i in range(0, 3):
                    fightBar.append(f'range_{theAlly[num].name}_{ally.tempClass}')
            elif 'magic' in ally.weapon.type:
                fightBar.append(f'magic_{theAlly[num].name}_{ally.tempClass}')
            else:
                fightBar.append(f'slash_{theAlly[num].name}_{ally.tempClass}')
        else:
            fightBarExtra.append(f'NoBar_{theAlly[num].name}_{ally.tempClass}')
            fightingBar[f'NoBar_{theAlly[num].name}_{ally.tempClass}'] = [True, True, 'NoBar', 1, 0, 0, ally]
        if ally.tempClass in ['Tank', 'Controller']:
            keys = []
            arrowKeys = ['RIGHT', 'UP', 'LEFT', 'DOWN']
            keyHit.append(0)
            keyDone.append(False)
            #keyUsed
            if ally.tempClass == 'Tank':
                for i in range(0, random.randint(1, 4)):
                    remove = random.randint(0, len(arrowKeys) - 1)
                    if ally.tempClass == 'Tank':
                        keys.append(arrowKeys[remove])
                        keyUsedBool.append(False)
                    arrowKeys.pop(remove)
                keyUsed.append(keys)

            keys = []

            if ally.tempClass == 'Controller':
                for i in range(0, random.randint(4, 6)):
                    if ally.tempClass == 'Controller':
                        keys.append(random.choice(['RIGHT', 'UP', 'LEFT', 'DOWN']))#['z', 'x', 'c']))
                        keyUsedBool.append(False)
                keyUsed.append(keys)

        else:
            keyHit.append(0)
            keyDone.append(True)
            keyUsed.append([])

    for i in range(0, len(fightBar) + len(theAlly) + len(theOpponent)):
        attackFrame.append(0)
        allyStrike.append(False)
        allyAttack.append(False)
        fightBarX.append(0)
        fightBarX2.append(hudRect[4] + hudRect[2] - 7)
        fightScale.append(1)
        barAlpha.append(255)
        damageX.append(200 if i%2==1 else 40)
        damageY.append((150 + 40*(i//4)) if (i//2)%2 == 0 else (70 - 40*(i//4)))
        damageY2.append(float(0))
        allyDamage.append(0)

    barClass = ['Melee', 'Range', 'Thrower', 'Tank', 'Controller', 'Support', 'Under', 'Slam', 'Back']
    bars = {}
    for i in barClass:
        bars[i] = []
    for bar in fightBar:
        if fightingBar[bar][9] not in bars:
            bars[fightingBar[bar][9]] = []
        bars[fightingBar[bar][9]].append(bar)

    fightBar.clear()
    for bar in bars.values():
        fightBar += bar
    meleeChecked = False
    throwerChecked = False
    rangeChecked = False
    tankChecked = False
    controllerChecked = False
    supportChecked = False
    underChecked = False
    slamChecked = False
    backChecked = False
    holdChecked = False

    for i in theAlly:
        if i.tempClass == 'Melee':
            for bar in fightBar:
                if i.name in bar:
                    meleeChecked = True
                    break

        if i.tempClass == 'Thrower':
            for bar in fightBar:
                if i.name in bar:
                    throwerChecked = True
                    break

        if i.tempClass == 'Range':
            for bar in fightBar:
                if i.name in bar:
                    rangeChecked = True
                    break

        if i.tempClass == 'Tank':
            for bar in fightBar:
                if i.name in bar:
                    tankChecked = True
                    break

        if i.tempClass == 'Controller':
            for bar in fightBar:
                if i.name in bar:
                    controllerChecked = True
                    break

        if i.tempClass == 'Support':
            for bar in fightBar:
                if i.name in bar:
                    supportChecked = True
                    break

        if i.tempClass == 'Under':
            for bar in fightBar:
                if i.name in bar:
                    underChecked = True
                    break

        if i.tempClass == 'Slam':
            for bar in fightBar:
                if i.name in bar:
                    slamChecked = True
                    break

        if i.tempClass == 'Back':
            for bar in fightBar:
                if i.name in bar:
                    backChecked = True
                    break

        if i.tempClass == 'Hold':
            for bar in fightBar:
                if i.name in bar:
                    holdChecked = True
                    break


    if not meleeChecked:
        meleeDone = True

    if not throwerChecked:
        throwerDone = True

    if not rangeChecked:
        rangeDone = True

    if not tankChecked:
        tankDone = True

    if not controllerChecked:
        controllerDone = True

    if not supportChecked:
        supportDone = True

    if not slamChecked:
        slamDone = True

    if not backChecked:
        backDone = True

    if not underChecked:
        underDone = True

    if not holdChecked:
        holdDone = True


    for i in fightBarExtra:
        fightBar.append(i)
    locals_dict = locals() # Loads in all local variables in this functions
    for var_name, var_value in locals_dict.items(): # Go through all local variables
        if var_name != 'my_function':  # Exclude all the function itself
            globals()[var_name] = var_value # Set those Variables as local

def botPlay():
    global confirm
    global rightPressed
    global leftPressed
    global cancel
    global lastBeat
    attackMeterX = hudRect[2] / 2 + hudRect[4]
    lastBeat += theDelta
    trigger = False
    if frame%30 == 0:
        trigger = True
    if lastBeat >= 1000 / (songBpm):
        trigger = True
        lastBeat = 0

    totalHit = 0
    checkEnergy = energyTrans + energyGain
    if not (allyTurn or enemyTurn):
        if not inFight:
            confirm = True
        else:
            confirm = False
            dashPassed = False
            distance = []
            allBarHit = True

            if meleeUsed:
                maxDistance = hudRect[0]
                limit = 15

            elif throwerUsed:
                maxDistance = math.pi * 2.5
                limit = 0.3

            elif rangeUsed:
                maxDistance = 0
                limit = 150

            elif supportUsed:
                maxDistance = hudRect[3] + hudRect[5]
                limit = 15

            elif underUsed:
                maxDistance = hudRect[3]# + hudRect[5]
                limit = 15

            elif slamUsed:
                maxDistance = (hudRect[4] + hudRect[2]) - 90
                limit = 10

            elif backUsed:
                maxDistance = hudRect[4] + 90
                limit = 5

            else:
                maxDistance = hudRect[4] + hudRect[2]/2
                limit = 19

            shouldProceed = True
            if int(hudRect[2]) == 527 or int(hudRect[2]) == 250 or int(hudRect[2]) == 190:
                shouldProceed = True
            elif shouldProceed == None:
                shouldProceed = True

            if shouldProceed:
                #keys = pygame.key.get_pressed()
                #keys = list(keys)
                for num, bar in enumerate(fightBar[:inBar]):
                    if 'done' not in bar and 'fail' not in bar and 'NoBar' not in bar:
                        #if 'Tank' not in bar and 'Controller' not in bar:
                        if abs(maxDistance - fightBarX2[num]) < limit and not turnEnemy and fightingBar[bar][2] != 'done':
                                fightingBar[bar][2] = 'done'
                                fightingBar[bar][2] = 'done'
                                fightingBar[bar][7].currentBar = fightingBar[fightBar[barSelect]][10]
                                theBar = fightingBar[bar][7].bars
                                fightingBar[bar][7].nextBar = theBar[ min(theBar.index(fightingBar[bar][10]) + 1, len(theBar) - 1 )]
                                            #playSound('Attack_sfx.ogg')
##                            if abs(maxDistance - fightBarX2[num]) <= limit or (turnEnemy and opponentBot):
##                                name = ''
##                                for letter in fightBar[barSelect]:
##                                    if dashPassed:
##                                        name += letter
##                                    elif letter == '_':
##                                        dashPassed = True
##                                fightBar[barSelect] = f'done_{name}'
##                                playSound('Attack_sfx.ogg')
                    if tankUsed or controllerUsed:
                            for allyNum, ally in enumerate(theAlly):
                                if ally.name in bar:
                                    break
                            for nummy, i in enumerate(keyUsed[allyNum]):
                                keyUsedBool[nummy] = True
    elif trigger:
        useSkill = False
        for i in party[selectedAlly].skills:
            if party[selectedAlly].mana >= i.cost:
                useSkill = True
                break
        if turn <= len(turnDialogue):
            if turnDialogue[turn-1][2] == False:
                confirm = True
        if useSkill:
            if actions[selectedAction] != 'Skills':
                leftPressed = True
            elif not allyAction[selectedAlly] == 'inSkill':
                confirm = True
            elif allyAction[selectedAlly] == 'inSkill':
                leftPressed = True
                confirm = True
            else:
                confirm = True
        elif actions[selectedAction] != 'Fight' and effectiveRange > 0:
            leftPressed = True
        elif effectiveRange <= 0:
            if str(actions[selectedAction]) == 'Act' or 'Act' in str(allyAction[selectedAlly]):
                if str(allyAction[selectedAlly]) == 'inAct':
                    if theAlly[selectedWhich].action[whichAction[selectedWhich]].name == 'Defend':
                        confirm = True
                    else:
                        rightPressed = True
                else:
                    confirm = True
                ##print(True)
            elif str(allyAction[selectedAlly]) != 'None':
                cancel = True
            else:
                leftPressed = True

        else:
            confirm = True
            ##print(1, inFight)

projectilePattern = []
def projectileUpdate():
    converter = (math.pi/180)
    for num, item in enumerate(projectilePattern):
        projectileSprite = loadSprite(f"projectile_{item['Name']}_{str(num)}", f"attackAnimate/projectile/{item['Name']}.png", scale=0.35)
        if item["Bool"] == True:
            if item["Delay"] > 0:
                item["Delay"] -= 1*item["Speed"]
            else:
                item["Frame"] += 1*item["Speed"]
            x = item["StartPos"][0] + item["Frame"]*math.cos(item["Angle"]*converter)
            y = item["StartPos"][1] + item["Frame"]*math.sin(item["Angle"]*converter)
            projectileSprite.pos = (x, y)
            for targetNum, target in enumerate(item["Targets"]):
                if isinstance(target, character.Opponent):
                    if target not in opponent:
                        targetSprite = enemySprite[0]
                    else:
                        targetSprite = enemySprite[opponent.index(target)]
                elif isinstance(target, character.Player):
                    targetSprite = playerSprite[party.index(target)]
                if targetSprite.checkCollision(projectileSprite) and target.hp > 0 and item["TargetTracker"][targetNum] == False:
                    item["TargetTracker"][targetNum] = True
                    fightyLoop.append([target, item["Attacker"], int(item["Damage"]*target.damage*(100-target.defense)/100)])
                    item["PierceCounter"] += 1
                    if item["PierceCounter"] > item["PierceHowMany"]:
                        item["Bool"] = False
            projectileSprite.draw()
            if x < 0 or x > width or y < 0 or y > height:
                item["Bool"] = False
        else:
            del screenWindow.sprites[f"projectile_{item['Name']}_{str(num)}"]



def addProjectile(name, attacker, target, damage, startPos, speed, angle, pierce, pierceHowMany, delay, patternType):
    targeted = []
    targetBool = []
    if target == "All":
        for i in party + opponent:
            targeted.append(i)
            targetBool.append(False)
    if target == "Opponent":
        for i in opponent:
            targeted.append(i)
            targetBool.append(False)
    if target == "Ally":
        for i in party:
            targeted.append(i)
            targetBool.append(False)
    elif isinstance(target, list):
        targeted = target
    projectilePattern.append({
        "Name": name,
        "Attacker": attacker,
        "Targets": targeted,
        "Damage": damage,
        "StartPos": startPos,
        "Speed": speed,
        "Angle": angle,
        "UsePierce": pierce,
        "PierceHowMany": pierceHowMany,
        "Delay": delay,
        "PatternType": patternType,
        "Frame": 0,
        "PierceCounter": 0,
        "TargetTracker": targetBool,
        "Bool": True
                              })
def getCharacter(charList, element, Range):

    if Range < 1:
        raise ValueError("Range must be at least 1.")

    newList = []
    for i in charList:
        if i.hp > 0:
            newList.append(i)

    try:
        # Find the index of the first occurrence of the element
        index = newList.index(element)
    except ValueError:
        # If the element is not in the list, return an empty list or raise an error
        return []  # or raise ValueError("Element not found in the list.")

    # Calculate the starting and ending indices for slicing
    start = max(0, index - Range)
    end = min(len(newList), index + Range + 1)  # +1 because slicing is exclusive on the end

    # Get the sublist but exclude the element itself
    neighbors = newList[start:index] + newList[index + 1:end]

    return neighbors



def triggerEvent(player, eventName):
    ##print(eventName)
    if eventName == "Death":
        if "Dandee" in player.dataName:
            character.disperse.apply(player, player, num=5, stackDur=True)
            for i in range(0, 8):
                for num in range(0, 3):
                    if isinstance(player, character.Player):
                        addProjectile("Blowballs_Default", player, "Opponent", 13, playerSprite[party.index(player)].pos, 5*(3-num), i*45, False, 0, 50*num, None)
                    elif isinstance(player, character.Opponent):
                        addProjectile("Blowballs_Default", player, "Ally", 13, enemySprite[opponent.index(player)].pos, 5*(3-num), i*45, False, 0, 50*num, None)
        if player.dataName:
            #if character.dandee in party or character.dandeeEn in opponent:
            #if character.dandeeEn in opponent and character.dandeeEn.hp > 0:]
            for char in opponent+party:
                if char.dataName == "Dandee" and char.hp > 0:
                    if isinstance(char, character.Player):
                        sprite = playerSprite[party.index(char)]
                    else:
                        sprite = enemySprite[opponent.index(char)]
                    #sprite = playerSprite[party.index(character.dandee)]
                    playAnimation(sprite, "laugh", duration=1, resetDuration=True)
                    character.force.apply(char, char, num=0, turn=5, stackDur=True)
                    character.sadism.apply(char, char, num=0, turn=5, stackDur=True)

    elif eventName == "Hurt":
        if player.name == "Red Dude":
            if player.tracker["Hurt"] == 3:
                character.readyToStrike.apply(player, player, num=5, stackDur=True)
        elif player.name == "Thin":
            if player.tracker["Hurt"] == 1:
                character.productivityZero.apply(player, player, num=5, stackDur=True)
        elif player.name == "Caen":
            #if player.tracker["Hurt"] == 1:
            character.caneHealing.apply(player, player, num=5, stackDur=True)
            if isinstance(player, character.Player):
                whichOne = party
            else:
                whichOne = opponent
            charList = getCharacter(whichOne, player, 1)
            for i in charList:
                fightyLoop.append([i, player, -1 * int(player.tracker['currentDamage']*0.6)])
                character.momentum.apply(player, i, num=0, turn=2)



    elif eventName == "Attacked":
        if player.name == "Thin":
            fightyLoop.append([player, player, player.attack])






def loadPlayer():
    for num, players in enumerate(party):
        hadAttacked = False
        for attacks in attacking:
            if players == attacks[1]:
                hadAttacked = True
                break
        if ('Done' in str(allyAction[num])) and (not speedBasedTurn):
            hadAttacked = False
        x = playerCoords[num][0]
        y = playerCoords[num][1]# + 350/2
        if isinstance(playerSprite[num], screenWindow.Sprite):
            playerSprite[num].opacity=0
        #if players.sprite == None:
       # party[0].dataName = 'Li Wei'
        players.sprite = loadAnimatedSprite("Player" + players.dataName + players.name, players.dataName, (-200, y), scale=0.3)
        players.sprite.baseScale = players.scale
        playerSprite[num] = players.sprite#loadAnimatedSprite(str(num) + "Player" + players.dataName + players.name, players.dataName, (-200, y), scale=0.3)
        currPlayer = playerSprite[num]
        if useAnim and ('None' in str(allyAction[num]) or turnEnemy) and not playerShakeBool[num]:
            currPlayer.pivotType = 'midbottom'
            currPlayer.scaleY = 1 + round(0.02*math.sin((frame)/7+num), 2)
            currPlayer.scaleX = 1 - round(0.03*math.sin((frame)/7+num), 2)
        elif useAnim:
            currPlayer.scaleY = 1
            currPlayer.scaleX = 1
            currPlayer.pivotType = 'midbottom'
        #currPlayer.skin = players.skin
##        if frame%2:
##            party[0].name = 'Copycat'
##            character.copySkill.use(players, random.choice(character.validAlly))
##            party[0].name = "Li Wei"
##            party[0].displayName = random.choice(character.validAlly).name
##            party[0].dataName = random.choice(character.validAlly).name
##            currPlayer.character = random.choice(character.validAlly).name
##            party[0].color = random.choice(character.validAlly).color
##            if party[0].hp >= party[0].maxhp:
##                party[0].hp = party[0].maxhp

        #print(currPlayer.image)
        infPresent = False

        phaseTwo = False
        for i in players.passiveBuff:
            if i.name == 'Locked In' or i.name == 'Iteker':
                if players.passiveBuff[i][0] == True:
                    phaseTwo = True

        if phaseTwo:
            currPlayer.skin = players.skin + ' Phase2'
        else:
            currPlayer.skin = players.skin

        if isinstance(allyDamage[num], float):
            if allyDamage[num] == inf:
                infPresent = True
        if playerShakeBool[num] == True:
            if playerShakeX[num] == 90:
                if players.status != "Death":
                    #print(True)
                    players.tracker["Hurt"] += 1
                    players.status = "Hurt"
                    triggerEvent(players, "Hurt")
                currPlayer.color = RED
                currPlayer.tintColor = RED
                currPlayer.targetColor = RED
            currPlayer.tweenColor(WHITE, 'easeOut', 0.3)
            currPlayer.timerAnim = None
            if frame % int(1 / theDelta) == 0:
                playerShakeX[num] = -(playerShakeX[num] - playerShakeX[num]//4)
                allyTween[num] += playerShakeX[num]/5
            xShake = playerShakePos[num][0]
            yShake = playerShakePos[num][1]
            xShake += playerShakeX[num]
            if abs(playerShakeX[num]) < 0.01:
                playerShakeBool[num] = False
                allyTween[num] -= playerShakeX[num]/5
                playerShakePos[num] = ()
            currPlayer.pos = (xShake, yShake)
            currPlayer.tweenClear('pos')
            if players.hp > 0:
                playAnimation(currPlayer, 'hurt', False)
        elif players.hp > 0:
            if hadAttacked and not inSkill and isinstance(players.usingWhat, character.Fight):
                playAnimation(currPlayer, players.usingWhat.barFightAnim[players.usingWhat.currentBar], False)
                if 1==0:
                    if players.tempClass != players.classes:
                        animationSuccess = playAnimation(currPlayer, f'attack_{players.tempClass}'.lower(), False)
                        if animationSuccess == False:
                            playAnimation(currPlayer, 'idle', False)
                    else:
                        playAnimation(currPlayer, 'attack', False)

            elif 'None' in str(allyAction[num]):
                if players.name in ['Blue Guy', 'Allerwave']:
                    playerFloat[num] += math.pi/15 * theDelta
                playAnimation(currPlayer, 'idle', True)
            elif 'Fight' in str(allyAction[num]) or ('Skill' in str(allyAction[num]) and not 'in' in str(allyAction[num]) and allyTurn):
                playAnimation(currPlayer, 'attackPrep', False)
            elif inSkill and turnAlly and 'Skills' in allyAction[num]:
                playAnimation(currPlayer, 'skill', False)


        if playerShakeBool[num] == False:
            currPlayer.tweenPos((x, y), 'easeOut', 1, False)
            if currPlayer.color != WHITE:
                currPlayer.tweenColor(WHITE, 'easeOut', 0.3, False)

        #if players.hp/players.maxhp < 0.2:
            #currPlayer.pos =(x + random.randint(-2,2), y + random.randint(-1,1))

        if players.hp <= 0:
            playAnimation(currPlayer, 'death', False)
            ##print(num, playerAlpha, playerAlpha[num])
            playerAlpha[num] += int( -11 * theDelta)
            ##print(num, playerAlpha, playerAlpha[num])
            if playerAlpha[num] <= 0.5:
                playerAlpha[num] = 0
                currPlayer.opacity = 0
            elif frame%int(2/theDelta) == 0:
                currPlayer.opacity = 50*playerAlpha[num]/255
            else:
                currPlayer.opacity = 255*playerAlpha[num]/255
            if 'Death' not in players.status:
                players.status = "Death"
                triggerEvent(players, "Death")

        if players.hp > 0:
            playerAlpha[num] += 30 * theDelta
            if playerAlpha[num] >= 255:
                playerAlpha[num] = 255
            currPlayer.opacity = playerAlpha[num]
            if 'Death' in players.status:
                players.status = "Neutral"
                triggerEvent(players, "Revived")
        if not firstPerson:
            #print(currPlayer.name)
            x, y = players.offsetX, players.offsetY
            if useAnim:
                y += 350/2
            if players.canFly:
                if players.flyType == 0:
                    y += players.flyRange*math.sin(frame/15 + num)
                else:
                    y += players.flyRange*math.sin(frame/15 + num)
                    x = 2*players.flyRange*math.sin(frame/30 + num)
            #print(ally.name, ally.canFly, frame, round(y, 2))
            if not (len(party) > 5 and players != party[selectedAlly]):
                currPlayer.draw(x, y)
            elif len(party) > 5 and players == party[selectedAlly]:
                currPlayer.draw(0, y)
        currPlayer.pivotType = 'Center'
        #currPlayer.pos[1] -= 350/2

def loadEnemy():
    for num, players in enumerate(opponent):
        hadAttacked = False
        for attacks in attacking:
            if players == attacks[1]:
                hadAttacked = True
                break
        if ('Done' in str(enemyAction[num])) and (not speedBasedTurn):
            hadAttacked = False
        x = opponentCoords[num][0]
        y = opponentCoords[num][1]
        if isinstance(enemySprite[num], screenWindow.Sprite):
            enemySprite[num].opacity=0
        #if players.sprite == None:
       # party[0].dataName = 'Li Wei'
        players.sprite = loadAnimatedSprite("Opponent" + players.dataName + players.name, players.dataName, (width + 200, y), scale=0.3, flipX=True)
        players.sprite.baseScale = players.scale
        enemySprite[num] = players.sprite#loadAnimatedSprite(str(num) + "Player" + players.dataName + players.name, players.dataName, (-200, y), scale=0.3)
        currPlayer = enemySprite[num]
        infPresent = False
        if useAnim and ('None' in str(enemyAction[num]) or turnAlly) and not enemyShakeBool[num]:
            currPlayer.pivotType = 'midbottom'
            currPlayer.scaleY = 1 + round(0.02*math.sin((frame + 0.5)/7+num), 2)
        elif useAnim:
            currPlayer.pivotType = 'midbottom'
            currPlayer.scaleY = 1

        phaseTwo = False
        for i in players.passiveBuff:
            if i.name == 'Locked In' or i.name == 'Iteker':
                if players.passiveBuff[i][0] == True:
                    phaseTwo = True

        if phaseTwo:
            currPlayer.skin = players.skin + ' Phase2'
        else:
            currPlayer.skin = players.skin

        if isinstance(allyDamage[num], float):
            if allyDamage[num] == inf:
                infPresent = True
        if enemyShakeBool[num] == True:
            if enemyShakeX[num] == 90:
                if players.status != "Death":
                    #print(True)
                    players.tracker["Hurt"] += 1
                    players.status = "Hurt"
                    triggerEvent(players, "Hurt")
                currPlayer.color = RED
                currPlayer.tintColor = RED
                currPlayer.targetColor = RED
            currPlayer.timerAnim = None
            
            currPlayer.tweenColor(WHITE, 'easeOut', 0.3)
            if frame % int(1 / theDelta) == 0:
                enemyShakeX[num] = -(enemyShakeX[num] - enemyShakeX[num]//4)
                enemyTween[num] += enemyShakeX[num]/5
            xShake = enemyShakePos[num][0]
            yShake = enemyShakePos[num][1]
            xShake += enemyShakeX[num]
            if abs(enemyShakeX[num]) < 0.01:
                enemyShakeBool[num] = False
                enemyTween[num] -= enemyShakeX[num]/5
                enemyShakePos[num] = ()
            currPlayer.pos = (xShake, yShake)
            currPlayer.tweenClear('pos')
            if players.hp > 0:
                playAnimation(currPlayer, 'hurt', False)
        elif players.hp > 0:
            if hadAttacked and not inSkill and isinstance(players.usingWhat, character.Fight):
                playAnimation(currPlayer, players.usingWhat.barFightAnim[players.usingWhat.currentBar], False)
                if 1==0:
                    if players.tempClass != players.classes:
                        animationSuccess = playAnimation(currPlayer, f'attack_{players.tempClass}'.lower(), False)
                        if animationSuccess == False:
                            playAnimation(currPlayer, 'idle', False)
                    else:
                        playAnimation(currPlayer, 'attack', False)

            elif 'None' in str(enemyAction[num]):
                if players.name in ['Blue Guy', 'Allerwave']:
                    enemyFloat[num] += math.pi/15 * theDelta
                playAnimation(currPlayer, 'idle', True)
            elif 'Fight' in str(enemyAction[num]) or ('Skill' in str(enemyAction[num]) and not 'in' in str(enemyAction[num]) and enemyTurn):
                playAnimation(currPlayer, 'attackPrep', False)
            elif inSkill and turnEnemy and 'Skills' in enemyAction[num]:
                playAnimation(currPlayer, 'skill', False)


        if enemyShakeBool[num] == False:
            #print(currPlayer.name, x)
            currPlayer.tweenPos((x, y), 'easeOut', 1, False)
            if currPlayer.color != WHITE:
                currPlayer.tweenColor(WHITE, 'easeOut', 0.3, False)

        #if players.hp/players.maxhp < 0.2:
            #currPlayer.pos =(x + random.randint(-2,2), y + random.randint(-1,1))

        if players.hp <= 0:
            playAnimation(currPlayer, 'death', False)
            ##print(num, playerAlpha, playerAlpha[num])
            opponentAlpha[num] += int( -11 * theDelta)
            ##print(num, playerAlpha, playerAlpha[num])
            if opponentAlpha[num] <= 0.5:
                opponentAlpha[num] = 0
                currPlayer.opacity = 0
            elif frame%int(2/theDelta) == 0:
                currPlayer.opacity = 50*opponentAlpha[num]/255
            else:
                currPlayer.opacity = 255*opponentAlpha[num]/255
            if 'Death' not in players.status:
                players.status = "Death"
                triggerEvent(players, "Death")

        if players.hp > 0:
            opponentAlpha[num] += 30 * theDelta
            if opponentAlpha[num] >= 255:
                opponentAlpha[num] = 255
            currPlayer.opacity = opponentAlpha[num]
            if 'Death' in players.status:
                players.status = "Neutral"
                triggerEvent(players, "Revived")
        #if turnAlly:
            #if "Target" in actionWhich[selectedWhich]:
             #   if effective
        if True:
            #print(currPlayer.name)
            x, y = -players.offsetX, -players.offsetY
            if useAnim:
                y += 350/2
            if players.canFly:
                if players.flyType == 0:
                    y += players.flyRange*math.sin(frame/15 + num)
                else:
                    y += players.flyRange*math.sin(frame/15 + num)
                    x += 2*players.flyRange*math.sin(frame/30 + num)
            #print(ally.name, ally.canFly, frame, round(y, 2))
            currPlayer.draw(x, y)
        currPlayer.pivotType = "Center"

def loa4444dEnemy():
    multiDetected = True
    for num, i in enumerate(opponent):
        if not i.name.endswith(chr(65 + num)):
            multiDetected = False

    for num, players in enumerate(opponent):
        hadAttacked = False
        for attacks in attacking:
            if players == attacks[1]:
                hadAttacked = True
                break
        if ('Done' in str(enemyAction[num])) and (not speedBasedTurn):
            hadAttacked = False
        x = opponentCoords[num][0]
        y = opponentCoords[num][1]
        shakingX = 0
        if isinstance(enemySprite[num], screenWindow.Sprite):
            enemySprite[num].opacity=0
        theScale = 1 if not firstPerson else 1.2
        enemySprite[num] = loadAnimatedSprite("Enemy" + players.dataName + players.name, players.dataName, pos=(width + 200, y), baseScale=theScale, scale=0.3)
        currPlayer = enemySprite[num]
        currPlayer.flipX = True

        #currPlayer.pos = (currPlayer.pos[0] + shakingX, currPlayer.pos[1])

        infPresent = False

        phaseTwo = False
        for i in players.passiveBuff:
            if i.name == 'Locked In' or i.name == 'Iteker':
                if players.passiveBuff[i][0] == True:
                    phaseTwo = True

        if phaseTwo:
            currPlayer.skin = players.skin + ' Phase2'
        else:
            currPlayer.skin = players.skin

        if isinstance(allyDamage[num], float):
            if allyDamage[num] == inf:
                infPresent = True
        if enemyShakeBool[num] == True:
            if enemyShakeX[num] == 90:
                currPlayer.color = RED
                currPlayer.tintColor = RED
                currPlayer.targetColor = RED
                if 'Death' not in players.status and "Hurt" not in players.status:
                    players.tracker["Hurt"] += 1
                    players.status = "Hurt"
                    triggerEvent(players, "Hurt")
            currPlayer.tweenColor(WHITE, 'easeOut', 0.3, True)
            if frame % int(1 / theDelta) == 0:
                enemyShakeX[num] = -(enemyShakeX[num] - enemyShakeX[num]//4)
            xShake = enemyShakePos[num][0]
            yShake = enemyShakePos[num][1]
            xShake += enemyShakeX[num]
            enemyTween[num] += enemyShakeX[num]/10
            if abs(enemyShakeX[num]) < 0.01:
                enemyShakeBool[num] = False
                enemyTween[num] -= enemyShakeX[num]/10
                enemyShakePos[num] = ()

            currPlayer.pos = (xShake, yShake)
            currPlayer.tweenClear('pos')
            if players.hp > 0:
                playAnimation(currPlayer, 'hurt', False)
        elif players.hp > 0:
            if hadAttacked and not inSkill:
                if players.tempClass != players.classes:
                    animationSuccess = playAnimation(currPlayer, f'attack_{players.tempClass}'.lower(), False)
                    if animationSuccess == False:
                        playAnimation(currPlayer, 'idle', False)
                else:
                    playAnimation(currPlayer, 'attack', False)

            elif 'None' in str(enemyAction[num]):
                if players.name in ['Blue Guy', 'Allerwave']:
                    enemyFloat[num] += math.pi/15 * theDelta
                playAnimation(currPlayer, 'idle', True)
            elif 'Fight' in str(enemyAction[num]) or ('Skill' in str(enemyAction[num]) and not 'in' in str(enemyAction[num]) and enemyTurn):
                playAnimation(currPlayer, 'attackPrep', False)
            elif inSkill and turnEnemy and not enemyAction[num] == 'Done':
                playAnimation(currPlayer, 'skill', False)
                ##print(True)

        if enemyShakeBool[num] == False and players.status != 'Spared':
            currPlayer.tweenPos((x, y), 'easeOut', 1, False)
            if currPlayer.color != WHITE:
                currPlayer.tweenColor(WHITE, 'easeOut', 0.3, False)

        if players.hp <= 0:
            playAnimation(currPlayer, 'death', False)
            opponentAlpha[num] += (0 - opponentAlpha[num])/5 * theDelta
            if opponentAlpha[num] <= 0.5:
                opponentAlpha[num] = 0
                currPlayer.opacity = 0
            elif frame%int(2/theDelta) == 0:
                currPlayer.opacity = 50*opponentAlpha[num]/255
            else:
                currPlayer.opacity = 255*opponentAlpha[num]/255
            if 'Death' not in players.status:
                players.status = "Death"
                triggerEvent(players, "Death")

        if players.hp > 0:
            opponentAlpha[num] += 30 * theDelta
            if opponentAlpha[num] >= 255:
                opponentAlpha[num] = 255
            currPlayer.opacity = opponentAlpha[num]
            if 'Death' in players.status:
                players.status = "Neutral"
                triggerEvent(players, "Revived")

        if players.status == 'Spared':
            #currPlayer.targetOpacity = 150
            currPlayer.tweenColor(YELLOW, 'easeOut', 0.3, False)
            currPlayer.tweenOpacity(0, 'easeOut', 0.6, False)
            #i#f currPlayer.color[2] <= 0:
                #currPlayer.color = (currPlayer.color[0], currPlayer.color[1], 0)

        for buff in os.listdir("sprites/visualEffects"):
            buffName = os.path.splitext(buff)[0]
            buffSprite = loadSprite(f'{buffName}_{players.name}', f'visualEffects/{buffName}_{players.skin}.png', pos=(currPlayer.pos), scale=0.3)
            del screenWindow.sprites[f'{buffName}_{players.name}']

        for buff in players.buff:
            caster = players.buff[buff][1]
            if buff.useVisual == True:
                buffSprite = loadSprite(f'{buff.name}_{caster.skin}_{players.name}', f'visualEffects/{buff.name}_{caster.skin}.png', pos=(currPlayer.pos), scale=0.3)
                buffSprite.pos = currPlayer.pos
                buffSprite.opacity = currPlayer.opacity * min(1, players.buff[buff][0] / 3)

        if bossFight:
            currPlayer.pos = (currPlayer.pos[0], opponentCoords[num][1] + 30*math.sin(frame*2*math.pi/80))
        currPlayer.draw()






def HudTransition(hudList, hudToChange, num):
    hudDict = {'centerX':0, 'centerY':1 , 'hudLength':2 , 'hudHeight':3 , 'hudX':4 , 'hudY':5 , 'thickness':6}
    for nummy, i in enumerate(hudToChange):
        hudNum = hudDict[i]
        number = 20
        hudList[hudNum] += (num[nummy] - hudList[hudNum])/4 * theDelta
        if abs(hudList[hudNum] - num[nummy]) < 0.1:
            hudList[hudNum] = num[nummy]

        hudList[4] = hudList[0] - (hudList[2] / 2)
        hudList[5] = hudList[1] - (hudList[3] / 2)

def healWhileloop():
        itemHeal = character.itemHealing
        if itemHeal != []:
            backItem = itemHeal
            for num, i in enumerate(itemHeal):
                whichOne = party if isinstance(i[1], character.Player) else opponent
                whichColor = colorOfAlly if isinstance(i[1], character.Player) else colorOfEnemy
                if isinstance(i[0], int) or isinstance(i[0], float):
                    theNum = i[0]
                else:
                    theNum = i[0].num
                for allyNum, ally in enumerate(whichOne):
                    if ally == i[1]:
                        break
                i[1].color = GREEN
                i[1].hp += 0.2 * theNum/10 * theDelta
                i[2] += 0.2 * theNum/10 * theDelta
                if i[2] >= theNum:
                    backItem.pop(num)
                    i[1].hp = i[3] + theNum
                    i[1].color = whichColor[allyNum]
                elif i[1].hp >= i[1].maxhp:
                    i[1].hp = i[1].maxhp
                    backItem.pop(num)
                    i[1].color = whichColor[allyNum]

            itemHeal = backItem

def stupidEnergyLoop():
    global energyLoop
    # [target, attacker, damage, originalHp, finalHp, progress, the stupid Damage Y, damageOrder, [targetX, targetY]]
    for num, i in enumerate(energyLoop):
        try:
            i[3]
        except:

            if isinstance(i[2], int) or isinstance(i[2], float):
                if i[2] < 0:
                    #playSound('Healing_sfx.ogg')
                    pass
                else:
                    #playSound('Hurt_sfx.ogg')
                    pass
            #else:
                #color = (150, 150, 150)

            infPresent = False
            if isinstance(i[2], float):
                if i[2] == inf:
                    infPresent = True

            for stuff in range(0, 9):
                i.append(0)

            num2 = len(energyLoop)
            checked = False
            for stuff in energyLoop[::-1]:
                num2 -= 1
                if i[0] == stuff[0] and num2 < num:
                    i[3] = stuff[4]
                    ##print(True, stuff[4])
                    checked = True

            if checked == False:
                i[3] = i[0].mana
                ##print(i[3], i[0].mana)

            i[4] = i[3] - i[2] if isinstance(i[2], int) else i[3]
            if infPresent:
                i[4] = -999
            i[5] = i[3]
            i[6] = 0
            i[7] = num

            usingEffect = False

            if isinstance (i[1], character.Effect):
                i[0].color = i[1].color
                i[11] = i[1].color
                usingEffect = True

            damageString = False
            if isinstance(i[2], str):
                damageString = True

            if not usingEffect and not damageString:
                if i[2] > 0:
                    if i[1].tempClass == 'Tank' or i[1].tempClass == 'Melee':
                        camSet(1, RED, 0, 7)

            if isinstance(i[1], character.Player):
                for allyNum, ally in enumerate(party):
                    if ally == i[1]:
                        break
                i[11] = colorOfAlly[allyNum]

            if isinstance(i[1], character.Opponent):
                for opponentNum, enemies in enumerate(opponent):
                    if enemies == i[1]:
                        break
                i[11] = colorOfEnemy[opponentNum]

            if isinstance(i[0], character.Player):
                for allyNum, ally in enumerate(party):
                    if ally == i[0]:
                        break
                i[8] = playerCoords[allyNum]
                i[10] = colorOfAlly[allyNum] if isinstance (i[1], character.Effect) else None
                #if isinstance(i[2], int) or infPresent:
                 #   if i[2] >= 0:
                  #      #playerShakeBool[allyNum] = True
                    #    playerShakeX[allyNum] = 90
                   #     if playerShakePos[allyNum] == ():
                     #       playerShakePos[allyNum] = playerSprite[allyNum].pos
                    #else:
                        #playerSprite[allyNum].color = GREEN
                        #playerSprite[allyNum].targetColor = GREEN

            if isinstance(i[0], character.Opponent):
                for opponentNum, enemies in enumerate(opponent):
                    if enemies == i[0]:
                        break
                i[8] = opponentCoords[opponentNum]
                i[10] = colorOfEnemy[opponentNum] if isinstance (i[1], character.Effect) else None
                #if isinstance(i[2], int) or infPresent:
                    #if i[2] >= 0:
                        #enemyShakeBool[opponentNum] = True
                        #enemyShakeX[opponentNum] = 90
                        #if enemyShakePos[opponentNum] == ():
                        #    enemyShakePos[opponentNum] = enemySprite[opponentNum].pos
                    #else:
                        #enemySprite[opponentNum].color = GREEN
                        #enemySprite[opponentNum].targetColor = GREEN

            #i[9] = False

        if isinstance(i[0], character.Player):
            playerNum = party.index(i[0])
            i[8] = playerSprite[playerNum].pos
        else:
            playerNum = opponent.index(i[0])
            i[8] = enemySprite[playerNum].pos

    opponentList = []
    playerList = []
    for i in opponent:
        opponentList.append(0)
    for i in party:
        playerList.append(0)

    for i in energyLoop:
        if isinstance(i[0], character.Player):
                for allyNum, ally in enumerate(party):
                    if ally == i[0]:
                        break

                i[7] = playerList[allyNum]
                playerList[allyNum] += 1

        if isinstance(i[0], character.Opponent):
                for opponentNum, enemies in enumerate(opponent):
                    if enemies == i[0]:
                        break

                i[7] = opponentList[opponentNum]
                opponentList[opponentNum] += 1

    fightBackUp = energyLoop
    targets = []
    for num, i in enumerate(energyLoop):



        i[0].mana -= (i[5] - i[4])/4 * theDelta if i[3] != inf else 0
        i[5] -= (i[5] - i[4])/4 * theDelta if i[3] != inf else 0
        if (abs(i[5] - i[4]) < 0.1 or i[3] == inf) and i[9] == False and i[6] <= -2*math.pi:
            i[9] = True
            if i[10] != None:
                i[0].color = i[10]

        if isinstance(i[2], float) or isinstance(i[2], int):
            if i[2] < 0 and i[0].mana >= i[0].maxMana:
                i[0].mana = i[0].maxMana
                if i[9] == False and i[6] <= -2*math.pi:
                    i[9] = True
                    if i[10] != None:
                        i[0].color = i[10]

        width = 120
        height = 15
        i[6] -= math.pi/12 * theDelta if i[6] > -2*(math.pi) else 0
        damageY = 45*math.sin(i[6]) if i[6] > -(math.pi) else 25*math.sin(-i[6])
        damageY += (120 + 30*(i[7]//4) ) if (i[7]//2)%2 == 0 else (40 - 30*(i[7]//4))
        damageX = i[8][0] - 40 if i[7]%2 == 0 else i[8][0] + 40

        if i[0] not in targets:
            targets.append(i[0])
            y = 70
            x = i[8][0] - 110/2
            ehealth_ratio = i[0].mana / i[0].maxMana if i[0].mana != inf else 1
            hpPercent = i[0].mana/i[0].maxMana * 100 if i[0].mana != inf else 100
            coloring = GREEN
            darkColor = (0, 150, 0)
            if 0 <= hpPercent <= 100:
                percentDecrease = (hpPercent - 75)/25
                coloring = CYAN#colorTween(GREEN, CYAN, percentDecrease)
                darkColor = (0, 150, 150)#colorTween((0, 150, 0), (0, 150, 150), percentDecrease)

            elif 50 <= hpPercent <= 75:
                percentDecrease = (hpPercent - 50)/25
                coloring = colorTween(YELLOW, GREEN, percentDecrease)
                darkColor = colorTween((150, 150, 0), (0, 150, 0), percentDecrease)

            elif 25 <= hpPercent <= 50:
                percentDecrease = (hpPercent - 25)/25
                coloring = colorTween(ORANGE, YELLOW, percentDecrease)
                darkColor = colorTween((150, 58, 0), (150, 150, 0), percentDecrease)

            elif 0 <= hpPercent <= 25:
                percentDecrease = abs((hpPercent)/25)
                coloring = colorTween(RED, ORANGE, percentDecrease)
                darkColor = colorTween((150, 0, 0), (150, 58, 0), percentDecrease)

            else:
                coloring = BLACK
                darkColor = BLACK
                #opponentname = render_text(i.name, YELLOW if i.spare == 100 else WHITE, 40)
            ehealthbar2 = drawRect(screen, (70, 70, 70) ,(x - 5, y - 5, 120, 27))
            ehealthbar1 = drawRect(screen, darkColor ,(x - 5, y - 5, 120 * ehealth_ratio, 27))
            ehealthbar = drawRect(screen, (100,100,100) ,(x, y, 110, 17))
            ehealthbg = drawRect(screen, coloring, (x, y, 110 * ehealth_ratio, 17))

        extraStr = ''
        if isinstance(i[2], int) or isinstance(i[2], float):
            if i[2] < 0:
                color = (0, 255, 255)
                extraStr = '+'
            else:
                color = (0, 200, 200)#i[11]
                extraStr = ''
        else:
            color = i[11] #(150, 150, 150)
            extrStr = ''


        if str(i[2]) == 'inf':
            damageText = render_text('∞', BLACK, 50, True, color, 3)
        else:
            damageText = render_text(extraStr + str(abs(i[2])), BLACK, 40, True, color, 3)
        blitObj(screen, damageText, damageX, damageY)
    checked = False
    for i in energyLoop:
        if i[9] == False:
            checked = True
    if checked == False:
        characters = {}
        for i in energyLoop:
            if i[0] not in characters:
                characters[i[0]] = [0, []]
                characters[i[0]][0] = i[3]
            if isinstance(i[2], int):
                characters[i[0]][1].append(i[2])
        for i in characters:
            i.mana = characters[i][0]
            #i.mana -= characters[i][1]
            for damage in characters[i][1]:
                i.mana -= damage
                i.mana = max(0, min(i.maxMana, i.mana))
            characters[i][0] = i.mana

        energyLoop = character.energyLoop = []

damageShowType = 1
def stupidFightLoop():
    global fightyLoop
    # [target, attacker, damage, originalHp, finalHp, progress, the stupid Damage Y, damageOrder, [targetX, targetY]]
    for num, i in enumerate(fightyLoop):
        try:
            i[3]
        except:
            #if turnEnemy:
            #camSet(1, RED, 0, 7)

            if isinstance(i[2], int) or isinstance(i[2], float):
                if i[2] < 0:
                    playSound('Healing_sfx.ogg')
                else:
                    playSound('Hurt_sfx.ogg')
                    screen.camera_shake = 10
                    screen.start_shake(90, 10)
                    backGroundScreen.camera_shake = 10
                    backGroundScreen.start_shake(90, 10)
            #else:
                #color = (150, 150, 150)

            infPresent = False
            if isinstance(i[2], float):
                if i[2] == inf:
                    infPresent = True

            for stuff in range(0, 12):
                i.append(0)

            num2 = len(fightyLoop)
            checked = False
            for stuff in fightyLoop[::-1]:
                num2 -= 1
                if i[0] == stuff[0] and num2 < num:
                    i[3] = stuff[4]
                    checked = True

            if checked == False:
                i[3] = i[0].hp

            i[4] = i[3] - i[2] if isinstance(i[2], int) else i[3]
            if infPresent:
                i[4] = -999
            i[5] = i[3]
            i[6] = 0
            i[7] = num

            i[0].tracker["currentDamage"] = i[2]

            usingEffect = False

            if isinstance (i[1], character.Effect):
                #i[0].color = i[1].color
                i[11] = i[1].color
                usingEffect = True

            damageString = False
            if isinstance(i[2], str):
                damageString = True

            if not usingEffect and not damageString:
                if i[2] > 0:
                    if i[1].tempClass == 'Tank' or i[1].tempClass == 'Melee':
                        camSet(1, RED, 0, 7)

            if isinstance(i[1], character.Player):
                for allyNum, ally in enumerate(party):
                    if ally == i[1]:
                        break
                i[11] = colorOfAlly[allyNum]

            if isinstance(i[1], character.Opponent):
                for opponentNum, enemies in enumerate(opponent):
                    if enemies == i[1]:
                        break
                i[11] = colorOfEnemy[opponentNum]

            if isinstance(i[0], character.Player):
                for allyNum, ally in enumerate(party):
                    if ally == i[0]:
                        break
                i[8] = playerCoords[allyNum]
                i[10] = colorOfAlly[allyNum] if isinstance (i[1], character.Effect) else None
                if isinstance(i[2], int) or infPresent:
                    if i[2] >= 0:
                        playerShakeBool[allyNum] = True
                        playerShakeX[allyNum] = 90
                        if playerShakePos[allyNum] == ():
                            playerShakePos[allyNum] = playerSprite[allyNum].pos
                    else:
                        playerSprite[allyNum].color = GREEN
                        playerSprite[allyNum].tintColor = GREEN
                        playerSprite[allyNum].targetColor = GREEN

            if isinstance(i[0], character.Opponent):
                for opponentNum, enemies in enumerate(opponent):
                    if enemies == i[0]:
                        break
                i[8] = opponentCoords[opponentNum]
                i[10] = colorOfEnemy[opponentNum] if isinstance (i[1], character.Effect) else None
                if isinstance(i[2], int) or infPresent:
                    if i[2] >= 0:
                        enemyShakeBool[opponentNum] = True
                        enemyShakeX[opponentNum] = 90
                        if enemyShakePos[opponentNum] == ():
                            enemyShakePos[opponentNum] = enemySprite[opponentNum].pos
                    else:
                        enemySprite[opponentNum].color = GREEN
                        enemySprite[opponentNum].tintColor = GREEN
                        enemySprite[opponentNum].targetColor = GREEN

            i[9] = False
            i[12] = int(16 / theDelta)
            i[13] = i[2] if isinstance(i[2], int) else 0
            i[14] = 0


    opponentList = []
    playerList = []
    for i in opponent:
        opponentList.append(0)
    for i in party:
        playerList.append(0)

    for i in fightyLoop:
        if isinstance(i[0], character.Player):
                for allyNum, ally in enumerate(party):
                    if ally == i[0]:
                        break

                i[7] = playerList[allyNum]
                playerList[allyNum] += 1

        if isinstance(i[0], character.Opponent):
                for opponentNum, enemies in enumerate(opponent):
                    if enemies == i[0]:
                        break

                i[7] = opponentList[opponentNum]
                opponentList[opponentNum] += 1

    fightBackUp = fightyLoop
    targets = []
    for num, i in enumerate(fightyLoop):

        if i[9] == False and i[12] > i[14]:
            i[14] += 1
            #i[12] = min(i[12], i[13]) if i[2] > 0 else max(i[12], i[13])
            #if i[12] != i[13]:
            i[0].hp -= (i[13])/i[12] if i[0].maxhp != inf else 0
            #i[5] -= (i[13])/16 * theDelta if i[0].maxhp != inf else 0
        if (i[12] == i[14] or i[3] == inf) and i[9] == False and i[6] <= -2*math.pi:
            i[9] = True
            if i[10] != None:
                i[0].color = i[10]

        if isinstance(i[2], float) or isinstance(i[2], int):
            if i[2] < 0 and i[0].hp >= i[0].maxhp:
                i[0].hp = i[0].maxhp
                if i[9] == False:# and i[6] <= -2*math.pi:
                    i[9] = 1
                    if i[10] != None:
                        i[0].color = i[10]

        #for i in shit:
        if isinstance(i[0], character.Player):
            playerNum = party.index(i[0])
            i[8] = playerSprite[playerNum].pos
        else:
            playerNum = opponent.index(i[0])
            i[8] = enemySprite[playerNum].pos
        width = 120
        height = 15
        i[6] -= math.pi/24 * theDelta if i[6] > -2*(math.pi) else 0
        if damageShowType == 0:
            damageY = 45*math.sin(i[6]) if i[6] > -(math.pi) else 25*math.sin(-i[6])
            damageY += (150 + 30*(i[7]//4) ) if (i[7]//2)%2 == 0 else (70 - 30*(i[7]//4))
            damageX = i[8][0] - 40 if i[7]%2 == 0 else i[8][0] + 40
        elif damageShowType == 1:
            factorX = abs(i[6])/(math.pi/18)
            damageY = (factorX-10)**2
            damageY += i[8][1] - 50
            damageX = i[8][0] + (5*factorX if isinstance(i[0], character.Player) else -5*factorX)

        if i[0] not in targets and not isinstance(i[2], str):
            targets.append(i[0])
            if True:
                y = 100
                x = i[8][0] - 110/2
                ehealth_ratio = i[0].hp / i[0].maxhp if i[0].hp != inf else 1
                hpPercent = i[0].hp/i[0].maxhp * 100 if i[0].hp != inf else 100
                coloring = GREEN
                darkColor = (0, 150, 0)
                if 75 <= hpPercent <= 100:
                    percentDecrease = (hpPercent - 75)/25
                    coloring = colorTween(GREEN, GREEN, percentDecrease)
                    darkColor = colorTween((0, 150, 0), (0, 150, 0), percentDecrease)

                elif 50 <= hpPercent <= 75:
                    percentDecrease = (hpPercent - 50)/25
                    coloring = colorTween(YELLOW, GREEN, percentDecrease)
                    darkColor = colorTween((150, 150, 0), (0, 150, 0), percentDecrease)

                elif 25 <= hpPercent <= 50:
                    percentDecrease = (hpPercent - 25)/25
                    coloring = colorTween(ORANGE, YELLOW, percentDecrease)
                    darkColor = colorTween((150, 58, 0), (150, 150, 0), percentDecrease)

                elif 0 <= hpPercent <= 25:
                    percentDecrease = abs((hpPercent)/25)
                    coloring = colorTween(RED, ORANGE, percentDecrease)
                    darkColor = colorTween((150, 0, 0), (150, 58, 0), percentDecrease)

                else:
                    coloring = BLACK
                    darkColor = BLACK
                    #opponentname = render_text(i.name, YELLOW if i.spare == 100 else WHITE, 40)
                ehealthbar2 = drawRect(screen, (70, 70, 70) ,(x - 5, y - 5, 120, 27))
                ehealthbar1 = drawRect(screen, darkColor ,(x - 5, y - 5, 120 * ehealth_ratio, 27))
                ehealthbar = drawRect(screen, (100,100,100) ,(x, y, 110, 17))
                ehealthbg = drawRect(screen, coloring, (x, y, 110 * ehealth_ratio, 17))

        extraStr = ''
        if isinstance(i[2], int) or isinstance(i[2], float):
            if i[2] < 0:
                color = (50, 255, 50)
                damage = abs(i[2])
                extraStr = '+'
            else:
                color = i[11]
                extraStr = ''
                damage = i[2]
        else:
            color = i[11] #(150, 150, 150)
            damage = i[2]
            extraStr = ''

        if renderDamageText:
            fontSize = 40 if damageShowType == 0 else 45
            if str(i[2]) == 'inf':
                damageText = render_text('∞', BLACK, fontSize, True, color, 3)
            else:
                if color == (0, 0, 0):
                    color = (255, 255, 255, 255)
                damageText = render_text(extraStr + str(damage), BLACK, fontSize, True, color, 3)
            #if damageShowType == 1:
                #if abs(i[6]) > math.pi/(18/10):
                   # damageText.set_alpha(max(255-255*(abs(i[6])-math.pi/(18/10))/(1.5*math.pi), 0))
            blitObj(screen, damageText, damageX, damageY)

    checked = False
    for i in fightyLoop:
        if i[9] == False or i[6] > -2*math.pi:
            checked = True
    if checked == False:
        characters = {}
        for i in fightyLoop:
            if i[0] not in characters:
                characters[i[0]] = [0, []]
                characters[i[0]][0] = i[3]
            if isinstance(i[2], int):
                characters[i[0]][1].append(i[2])
        for i in characters:
            i.hp = characters[i][0]
            for damage in characters[i][1]:
                i.hp -= damage
                i.hp = min(i.maxhp, i.hp)
            characters[i][0] = i.hp
        fightyLoop = character.fightyLoop = []

    #fightyLoop = fightBackUp

def swapPos(A, B):
    global backUpCoords
    if len(backUpCoords) < 2: #and A != B:
        for allyNum, ally in enumerate(party):
            if ally == A:
                allyA = allyNum
            if ally == B:
                allyB = allyNum

        for i in range(0,3):
            backUpCoords.append(0)

        backUpCoords[0] = [allyA, playerCoords[allyA].copy()]
        backUpCoords[1] = [allyB, playerCoords[allyB].copy()]
        backUpCoords[2] = speedOrder[speedNumOrder]

def swapPosUpdate():
    global backUpCoords, hudTween, swap, swapFinally, speedOrder, speedNumOrder, original, selectedAlly, speedNum, allyAction
    if backUpCoords != []:
        allyA, allyB, oriA, oriB, original = backUpCoords[0][0], backUpCoords[1][0], backUpCoords[0][1], backUpCoords[1][1], backUpCoords[2]
        if not swapFinally:
            playerCoords[allyA][0] += (oriB[0] - playerCoords[allyA][0])/5 * theDelta
            playerCoords[allyB][0] += (oriA[0] - playerCoords[allyB][0])/5 * theDelta

            playerSprite[allyA].tweenPos(oriB, 'easeOut', 1, True)
            playerSprite[allyB].tweenPos(oriA, 'easeOut', 1, True)

        if hudTween <= math.pi:
            hudTween += math.pi/20 * theDelta

        if abs(oriA[0] - playerCoords[allyB][0]) < 0.5 or swapFinally:
            swapFinally = True
            if not swap:
                playerCoords[allyA][0], playerCoords[allyB][0],playerAlpha[allyB] , playerAlpha[allyA] = oriA[0], oriB[0], playerAlpha[allyA] , playerAlpha[allyB]
                party[allyA], party[allyB], colorOfAlly[allyA], colorOfAlly[allyB] = party[allyB], party[allyA], colorOfAlly[allyB], colorOfAlly[allyA]
                swap = True
                speedOrder = []
                for num, i in enumerate(party):
                    speedOrder.append([i.speed, num, 'Player', i.name])

                for num, i in enumerate(opponent):
                    speedOrder.append([i.speed, num, 'Enemy', i.name])

                organise = False
                while not organise:
                    organise = True
                    for num, i in enumerate(speedOrder):
                        if num + 1 < len(speedOrder):
                            if i[0] > speedOrder[(num + 1)][0]:
                                speedOrder[num], speedOrder[num + 1] = speedOrder[num + 1], speedOrder[num]
                                organise = False
                speedOrder.reverse()

                for num, stuff in enumerate(speedOrder):
                    if stuff[3] == original[3]:
                        speedNumOrder = num
                        selectedAlly = speedOrder[num][1]
                        speedNum = selectedAlly


            if hudTween <= 2*math.pi:
                hudTween += math.pi/20 * theDelta
            else:
                backUpCoords = []
                swap = False
                swapFinally = False
                hudTween = 0
            ##print('Done')

        for num in range(0, len(allyTween)):
            allyTween[num] = -370*math.sin(hudTween/2) * theDelta
   # if len(backUpCoords) > 2

#Shooter, Thrower, Under, Ram, Shaking
#def addAttack(targets, attacker, damage, dodgeBoolean, whatWasUsed, boolean=False, forceNoDone=False, pierceAnimationType='Ram', pierceThrough=False, pierceHowMany=1, pierceDamageReduction='+0', missAndHit=False, animationType='Ram', animationSpeed=0.7, rotate=True, rotateSpeed=5):

 #   attacking.append([targets, attacker, damage, dodgeBoolean, whatWasUsed, boolean, forceNoDone, pierceAnimationType='Ram', pierceThrough, pierceHowMany, pierceDamageReduction, missAndHit, animationType, animationSpeed, rotate, rotateSpeed])
def attackProUpdate():
    # [targets, attacker, class, damage, dodgedBool, whatWasUsed, Truebool]
    global attacking, actionWhich
    theNumber = -1
    for theNum, i in enumerate(attacking):
        try:
            i[8]
        except:
            attacking[theNum].append([])
            attacking[theNum].append([])
            attacking[theNum].append(False)
            for stuff in i[0]:
                i[8].append(False) # Has Hurt Bool
                i[7].append(False)

    attackers = {}
    hurt = {}
    for theNum, i in enumerate(attacking):
        if i[2] in ['Melee', 'Tank', 'Slam'] and not firstPerson:
            for num, proj in enumerate(i[0]):
                if False not in i[7]:
                    if i[4] == 0:
                        attackers[i[1]] = i[1]
                        hurt[i[1]] = i[1]
                doStartProj = False
                if False in i[7]:
                    damageListThing = [i[3], "DODGE", "WHIFF", "BLOCK"]
                    if '{i[5].name}_{i[1].skin}_{theNum}' not in screenWindow.sprites:
                        doStartProj = True
                    projSprite = loadSprite(f'{i[5].name}_{i[1].skin}_{theNum}', pos=(-100, -100))
                    #print(proj.name, type(proj))
                    theSprite = enemySprite[ opponent.index(proj) ] if isinstance(proj, character.Opponent) else playerSprite[ party.index(proj) ]
                    ##print(opponent.index(i[1]) if isinstance(i[1], character.Opponent) else party.index(i[1]))
                    attacker = enemySprite[ opponent.index(i[1]) ] if isinstance(i[1], character.Opponent) else playerSprite[ party.index(i[1]) ]
                    coord = opponentCoords[ opponent.index(proj) ] if isinstance(proj, character.Opponent) else playerCoords[ party.index(proj) ]
                    #coord2 =
                    daNum = 0.25 if isinstance(i[1], character.Player) else 0.35
                    index = opponent.index(i[1]) if isinstance(i[1], character.Opponent) else party.index(i[1])
                    if i[4] == 1:
                        multi = 1
                        attacker.tweenPos((coord[0] + daNum, attacker.pos[1]), 'circIn', 0.1, True)

                        theSprite.tweenScale(daNum, 'easeOut', 0.2)
                        #theSprite.tweenPos((coord[0] - 2.5*daNum, coord[1]), 'easeOut', 0.5, True)
                    else:
                        multi = 1
                        attacker.tweenPos((coord[0] + daNum, attacker.pos[1]), 'circIn', 0.1, True)
                    if doStartProj:
                        i[5].projectileStart(i[1], proj, damageListThing[i[4]], i[3], i, attacker, i[6])
                    if (abs(attacker.pos[0] - (coord[0] + multi*daNum)) <= 1 and i[4] == 1) or attacker.checkCollision(theSprite):#attacker.checkCollision(theSprite):
                        if i[7][num] != True:
                            theSprite.tweenScale(0.3, 'easeOut', 0.2, True)
                            if not attacker.checkCollision(theSprite) or i[4] == 1:
                                damage = 'DODGE'
                                playAnimation(theSprite, "dodge", duration=1, resetDuration=True)
                                with open(f'data/dialogue/{proj.dataName}.txt', 'r') as file:
                                        code = file.read()
                                diction = eval(code)
                                if 'dodge' in diction:
                                    text = random.choice(diction['dodge'])
                                    dialogueText.append([text, proj, 0, False])
                                i[5].projectileUse(i[1], proj, damage, i[3], i, attacker, i[6])
                            elif i[4] == 2:
                                damage = 'WHIFF'
                                i[5].projectileUse(i[1], proj, damage, i[3], i, attacker, i[6])
                            elif i[4] == 3:
                                playSound("Block_sfx.ogg", 2)
                                damage = 'BLOCK'
                                i[5].projectileUse(i[1], proj, damage, i[3], i, attacker, i[6])
                                playAnimation(theSprite, "block", duration=0.5, resetDuration=True)
                                #print(True)
                            else:
                                triggerEvent(i[1], 'Attacked')
                                damage = i[3]
                                i[5].projectileUse(i[1], proj, damage, i[3], i, attacker, i[6])
                                targetName = proj.dataName

                                attackerName = i[1].dataName
                                checked = True
                                if not i[9]:
                                    #print(i[1].name, frame)
                                    if i[1] not in attackers:
                                        checked = False
                                    i[9] = True
                                    attackers[i[1]] = i[1]

                                attackers[i[1]] = i[1]
                                hurtChecked = True
                                if i[1] not in hurt:
                                    hurtChecked = False
                                hurt[i[1]] = i[1]
                                with open(f'data/dialogue/{targetName}.txt', 'r') as file:
                                        code = file.read()
                                diction = eval(code)
                                if not hurtChecked:
                                    text = random.choice(diction['hurt'])
                                    dialogueText.append([text, proj, 0, False])
                                with open(f'data/dialogue/{attackerName}.txt', 'r') as file:
                                        code = file.read()
                                diction = eval(code)
                                text = random.choice(diction['attack'])
                                #checked = False
                                skillCheck = False
                                if isinstance(i[5], character.Skill):
                                    if i[5].useDialogue != None:
                                        skillCheck = True
                                if not checked:
                                    dialogueText.append([text, i[1], 0, False])
                                    theNumber = theNum


                            if i[4] == 0 and damage > 0:
                                if i[5].applyEffect != None:
                                    for effect in i[5].applyEffect:
                                        ##print(i[5].applyEffect)
                                        turn = i[5].applyEffect[effect][0]
                                        amplifier = i[5].applyEffect[effect][1]
                                        for target in i[0]:
                                            effect.apply(i[1], target, turn, amplifier, i[5].stackDuration, i[5].stackAmplifier)
                                if i[5].removeEffect != None:
                                    for effect in i[5].removeEffect:
                                        #turn = self.applyEffect[i][0]
                                        #amplifier = self.applyEffect[i][1]
                                        for target in i[0]:
                                            effect.remove(target)

                            if proj.hp > 0:
                                if isinstance(i[5], character.Skill) and damage > 0:
                                    if i[5].ignoreDefense == False:
                                        damage = int(damage * (100 - proj.defense)/100)
                                    #print(1)
                                fightyLoop.append([proj, i[1], damage])
                                #print(fightyLoop)
                            i[7][num] = True
                            if not isinstance(i[5], character.Skill) and False not in i[7]:
                                notDone = False
                                for bar in fightBar:
                                    if i[1].name in bar:
                                        if fightingBar[bar][2].lower() not in ['done', 'failhit']:
                                            notDone = True
                                            break
                                for thing in attacking:
                                    if thing[1] == i[1]:
                                        ##print(thing)
                                        if False in thing[7]:
                                            notDone = True
                                if not notDone:
                                    actionWhich[index] = 'Done'

                            else:
                                #actionWhich[index] = 'doneSkills'
                                targeted = proj
                                if not isinstance(targeted, list):
                                    targeted = [targeted]
                            #allyAttack[index] = None

        else:
            for num, proj in enumerate(i[0]):
                #print(f'Frame: {frame}')
                if False not in i[7]:
                    if i[4] == 0:
                        attackers[i[1]] = i[1]
                        hurt[i[1]] = i[1]
                if False in i[7]:
                    if not firstPerson:
                        #print(f'Frame: {frame}')
                        #attackers[i[1]] = i[1]
                        theSprite = enemySprite[ opponent.index(proj) ] if isinstance(proj, character.Opponent) else playerSprite[ party.index(proj) ]
                        isOpponent = True if isinstance(proj, character.Opponent) else False
                        attacker = enemySprite[ opponent.index(i[1]) ] if isinstance(i[1], character.Opponent) else playerSprite[ party.index(i[1]) ]
                        coord = opponentCoords[ opponent.index(proj) ] if isinstance(proj, character.Opponent) else playerCoords[ party.index(proj) ]
                        if isinstance(i[2], character.Skill):
                            theName = i[2].name
                        else:
                            theName = i[1].name
                        if attacker.pos[0] <= theSprite.pos[0]:
                            t = width + 100
                            doFlip = False
                        else:
                            t = 0 - 100
                            doFlip = True
                        if i[7][num] == True:
                            #print(frame)
                            #attackers[i[1]] = i[1]
                            #hurt[i[1]] = i[1]
                            projSprite = loadSprite(f'{i[5].name}_{i[1].skin}_{theNum}', f'attackAnimate/projectile/{i[5].name}_{i[1].skin}.png', pos=(attacker.pos), scale=0.25, angle = 0)

                        if i[4] == 1:
                            theSprite.tweenScale(0.25, 'easeOut', 0.2)
                        else:
                            theSprite.tweenScale(0.3, 'easeOut', 0.2)
                        doStartProj = False
                        if not i[7][num]:
                            damageListThing = [i[3], "DODGE", "WHIFF", "BLOCK"]
                            if f'{i[5].name}_{i[1].skin}_{theNum}' not in screenWindow.sprites:
                                doStartProj = True
                                #print(3)
                                
                            if i[2] == 'Thrower':
                                projSprite = loadSprite(f'{i[5].name}_{i[1].skin}_{theNum}', f'attackAnimate/projectile/{i[5].name}_{i[1].skin}.png', pos=(attacker.pos), scale=0.25, angle = 0)
                                if ((projSprite.pos[0] < (coord[0]) and isOpponent) or (projSprite.pos[0] > (coord[0]) and not isOpponent)) and not isinstance(i[5], character.Skill):
                                    projSprite.tweenThrow((coord[0], attacker.pos[1]), duration=0.8, peakHeight=250)
                                if projSprite.pos[0] == coord[0] and not isinstance(i[5], character.Skill):
                                    theNum = 500 if isOpponent else -500
                                    projSprite.tweenPos((coord[0] + theNum, height + 200), 'linear', 0.8, True)
                                elif isinstance(i[5], character.Skill):
                                    projSprite.tweenThrow((coord[0], attacker.pos[1]), duration=0.8, peakHeight=250)
                                if not projSprite.tweenActivePos:
                                    theNum = 500 if isOpponent else -500
                                    projSprite.tweenPos((coord[0] + theNum, height + 200), 'linear', 0.8, True)
                                #projSprite.flipX = theSprite.flipX
                                projSprite.angle -= 15 * theDelta
                                #projSprite.flipX = attacker.flipX
                            elif i[2] == 'Support':
                                projSprite = loadSprite(f'{i[5].name}_{i[1].skin}_{theNum}', f'attackAnimate/projectile/{i[5].name}_{i[1].skin}.png', pos=(attacker.pos), scale=0.35)
                                projSprite.pos = (projSprite.pos[0] + random.randint(-10, 10), projSprite.pos[1] + random.randint(-20, 10))
                                projSprite.tweenPos((t, attacker.pos[1]), 'linear', 2)
                                #projSprite.flipX = attacker.flipX
                            elif i[2] == 'Under':
                                projSprite = loadSprite(f'{i[5].name}_{i[1].skin}_{theNum}', f'attackAnimate/projectile/{i[5].name}_{i[1].skin}.png', pos=(theSprite.pos[0], attacker.pos[1] + 150), scale=0.25, opacity=0)
                                projSprite.opacity += 25.5
                                if projSprite.opacity >= 255:
                                    projSprite.opacity = 255
                                    projSprite.tweenPos((theSprite.pos[0], -200), 'linear', 0.4)
                                #projSprite.flipX = attacker.flipX
                            else:
                                projSprite = loadSprite(f'{i[5].name}_{i[1].skin}_{theNum}', f'attackAnimate/projectile/{i[5].name}_{i[1].skin}.png', pos=(attacker.pos), scale=0.25)
                                projSprite.tweenPos((t, attacker.pos[1]), 'linear', 0.6)
                            projSprite.flipX = doFlip#attacker.flipX
                            if doStartProj:
                                i[5].projectileStart(i[1], proj, damageListThing[i[4]], i[3], i, projSprite, i[6])

                        if (theSprite.checkCollision(projSprite) and i[4] == 0) or abs(projSprite.pos[0] - t) <= 50 or abs(projSprite.pos[1] - -200) <= 50 or abs(projSprite.pos[1] - (200 + height)) <= 50 or i[7][num] == True:
                            if i[7][num] != True and projSprite.opacity == 255 and not (i[2] == 'Thrower' and abs(projSprite.angle) < 70):
                                theSprite.tweenScale(0.3, 'easeOut', 0.2, True)
                                if (abs(projSprite.pos[0] - t) <= 50 or i[4]==1 or abs(projSprite.pos[1] - -200) <= 50 or abs(projSprite.pos[1] - (200 + height)) <= 50) and i[4] != 2:
                                    damage = 'DODGE'
                                    playAnimation(theSprite, "dodge", duration=1, resetDuration=True)
                                    with open(f'data/dialogue/{proj.dataName}.txt', 'r') as file:
                                            code = file.read()
                                    diction = eval(code)
                                    if 'dodge' in diction:
                                        text = random.choice(diction['dodge'])
                                        dialogueText.append([text, proj, 0, False])
                                    i[5].projectileUse(i[1], proj, damage, i[3], i, projSprite, i[6])
                                elif i[4] == 2:
                                    damage = 'WHIFF'
                                    i[5].projectileUse(i[1], proj, damage, i[3], i, projSprite, i[6])
                                elif i[4] == 3:
                                    damage = 'BLOCK'
                                    i[5].projectileUse(i[1], proj, damage, i[3], i, projSprite, i[6])
                                    playAnimation(theSprite, "block", duration=1, resetDuration=True)
                                else:
                                
                                    triggerEvent(i[1], 'Attacked')
                                    damage = i[3]
                                    i[5].projectileUse(i[1], proj, damage, i[3], i, projSprite, i[6])
                                    if damage > 0:
                                        #print(True)
                                        checked = True
                                        if not i[9]:
                                            #print(i[1].name, frame)
                                            if i[1] not in attackers:
                                                checked = False
                                            i[9] = True
                                            attackers[i[1]] = i[1]

                                        attackers[i[1]] = i[1]
                                        hurtChecked = True
                                        if i[1] not in hurt:
                                            hurtChecked = False
                                        hurt[i[1]] = i[1]
                                        #if isinstance(i[5], character.Fight):
                                            #if i[6][10] != 'A1':
                                                #checked = True#
                                        with open(f'data/dialogue/{proj.dataName}.txt', 'r') as file:
                                                code = file.read()
                                        diction = eval(code)
                                        if not hurtChecked:
                                            text = random.choice(diction['hurt'])
                                            dialogueText.append([text, proj, 0, False])
                                        with open(f'data/dialogue/{i[1].dataName}.txt', 'r') as file:
                                                code = file.read()
                                        diction = eval(code)
                                        text = random.choice(diction['attack'])

                                        skillCheck = True
                                       # if isinstance(i[5], character.Skill):
                                       #     if i[5].useDialogue != None:
                                        #        skillCheck = True

                                        if (not checked):
                                            dialogueText.append([text, i[1], 0, False])
                                            theNumber = theNum
                                        #elif not skillCheck and isinstance(i[5], character.Skill):
                                        #    if True not in i[7]:
                                        #        dialogueText.append([text, i[1], 0, False])
                                        #        theNumber = theNum


                                #print(i[1].damage, i[1].name)
                                if proj.hp > 0 and not (damage == 0 and proj.damage != 0):
                                    if isinstance(i[5], character.Skill) and damage > 0:
                                        if i[5].ignoreDefense == False:
                                            damage = int(damage * (100 - proj.defense)/100)
                                    
                                    fightyLoop.append([proj, i[1], damage])
                                i[7][num] = True
                                index = opponent.index(i[1]) if isinstance(i[1], character.Opponent) else party.index(i[1])
                                if not isinstance(i[5], character.Skill):# and False not in i[7]:
                                    #print(True)
                                    notDone = False
                                    for bar in fightBar:
                                        if i[1].name in bar:
                                            if fightingBar[bar][2].lower() not in ['done', 'failhit']:
                                                notDone = True
                                                break
                                    for thing in attacking:
                                        if thing[1] == i[1]:
                                            ##print(thing)
                                            if False in thing[7]:
                                                notDone = True
                                    if not notDone:# and False not in i[7]:
                                        #print(True)
                                        actionWhich[index] = 'Done'
                                else:
                                    #actionWhich[index] = 'doneSkills'
                                    targeted = proj
                                    if not isinstance(targeted, list):
                                        targeted = [targeted]

                                if i[4] == 0:
                                    proceed = True
                                    if isinstance(i[5], character.Skill):
                                        proceed = True
                                    else:
                                        if damage <= 0:
                                            proceed = False
                                    if proceed:      
                                        if i[5].applyEffect != None:
                                            for effect in i[5].applyEffect:
                                                ##print(i[5].applyEffect)
                                                turn = i[5].applyEffect[effect][0]
                                                amplifier = i[5].applyEffect[effect][1]
                                                turnDur = 0
                                                if len(i[5].applyEffect[effect]) == 3:
                                                    turnDur = i[5].applyEffect[effect][2]
                                                #for target in i[0]:
                                                effect.apply(i[1], proj, turn, amplifier, i[5].stackDuration, i[5].stackAmplifier, i[5].maxAmplifier, i[5].maxDuration, turnDur)
                                        if i[5].removeEffect != None:
                                            for effect in i[5].removeEffect:
                                                #turn = self.applyEffect[i][0]
                                                #amplifier = self.applyEffect[i][1]
                                                effect.apply(i[1], proj, turn, amplifier, i[5].stackDuration, i[5].stackAmplifier)
                    else:
                        theSprite = enemySprite[ opponent.index(proj) ] if isinstance(proj, character.Opponent) else playerSprite[ party.index(proj) ]
                        attacker = enemySprite[ opponent.index(i[1]) ] if isinstance(i[1], character.Opponent) else playerSprite[ party.index(i[1]) ]
                        if i[2] in ['Melee', 'Tank']:
                            animation = 'Slice'
                        elif i[2] in ['Slam', 'Support']:
                            animation = 'Bash'
                        elif i[2] in ['Controller', 'Under']:
                            animation = 'Magic'
                        elif i[2] in ['Range', 'Thrower']:
                            animation = 'Range'
                        projSprite = loadAnimatedSprite(f'{i[5].name}_{i[1].skin}_{theNum}', animation, color=attacker.color, baseScale=0.7)
                        #if f'{i[5].name}_{i[1].skin}_{theNum}' not in screenWindow.sprites:
                            #projSprite.currentFrameIndex = 0
                        projSprite.pos = theSprite.pos
                        #print(attacker.color)
                        projSprite.color = i[1].color
                        if isinstance(proj, character.Player):
                            x = (width / 2) / len(party) + (party.index(proj) * width / len(party))
                            y = height - 90 + allyTween[party.index(proj)]
                            projSprite.pos = (x, y)
                            projSprite.scale = 0.75
                            projSprite.layer = hud
                        #projSprite.targetColor = attacker.color
                        if len(projSprite.frames)-1 == projSprite.currentFrameIndex:
                            #theSprite.tweenScale(0.3, 'easeOut', 0.2, True)
                            if i[4] == 1:
                                damage = 'DODGE'
                                playAnimation(theSprite, "dodge", duration=1, resetDuration=True)
                                with open(f'data/dialogue/{proj.dataName}.txt', 'r') as file:
                                        code = file.read()
                                diction = eval(code)
                                if 'dodge' in diction:
                                    text = random.choice(diction['dodge'])
                                    dialogueText.append([text, proj, 0, False])
                            elif i[4] == 2:
                                damage = 'WHIFF'
                            elif i[4] == 3:
                                damage = 'BLOCK'
                            else:
                                triggerEvent(i[1], 'Attacked')
                                damage = i[3]
                                with open(f'data/dialogue/{proj.dataName}.txt', 'r') as file:
                                        code = file.read()
                                diction = eval(code)
                                text = random.choice(diction['hurt'])
                                dialogueText.append([text, proj, 0, False])
                                with open(f'data/dialogue/{i[1].dataName}.txt', 'r') as file:
                                        code = file.read()
                                diction = eval(code)
                                text = random.choice(diction['attack'])
                                checked = False
                                for stuff in dialogueText:
                                    if stuff[1] == i[1]:
                                        checked = True
                                        theNumber = theNum
                                        break
                                if not checked:
                                    dialogueText.append([text, i[1], 0, False])
                                    theNumber = theNum
                                else:
                                    if True not in i[7]:
                                        dialogueText.append([text, i[1], 0, False])
                                        theNumber = theNum

                            if proj.hp > 0:
                                fightyLoop.append([proj, i[1], damage])
                            i[7][num] = True
                            index = opponent.index(i[1]) if isinstance(i[1], character.Opponent) else party.index(i[1])
                            if not isinstance(i[5], character.Skill) and False not in i[7]:
                                notDone = False
                                for bar in fightBar:
                                    if i[1].name in bar:
                                        if fightingBar[bar][2].lower() not in ['done', 'failhit']:
                                            notDone = True
                                            break
                                for thing in attacking:
                                    if thing[1] == i[1]:
                                        ##print(thing)
                                        if False in thing[7]:
                                            notDone = True
                                if not notDone:
                                    actionWhich[index] = 'Done'
                            else:
                                #actionWhich[index] = 'doneSkills'
                                targeted = proj
                                if not isinstance(targeted, list):
                                    targeted = [targeted]

                            if i[4] == 0:
                                if i[5].applyEffect != None:
                                    for effect in i[5].applyEffect:
                                        ##print(i[5].applyEffect)
                                        turn = i[5].applyEffect[effect][0]
                                        amplifier = i[5].applyEffect[effect][1]
                                        #for target in i[0]:
                                        effect.apply(i[1], proj, turn, amplifier, i[5].stackDuration, i[5].stackAmplifier)
                                if i[5].removeEffect != None:
                                    for effect in i[5].removeEffect:
                                        #turn = self.applyEffect[i][0]
                                        #amplifier = self.applyEffect[i][1]
                                        effect.apply(i[1], proj, turn, amplifier, i[5].stackDuration, i[5].stackAmplifier)


                    if False not in i[7]:
                        ##print(f'{i[5].name}_{i[1].skin}_{theNum}', screenWindow.sprites.keys())
                        if f'{i[5].name}_{i[1].skin}_{theNum}' in screenWindow.sprites:
                            del screenWindow.sprites[f'{i[5].name}_{i[1].skin}_{theNum}']
                        if f'{i[5].name}_{i[1].skin}_{theNum}' in screenWindow.animatedSprites:
                            del screenWindow.animatedSprites[f'{i[5].name}_{i[1].skin}_{theNum}']
                    projSprite.draw()
                        #    #print(True)

    if allyTurn or enemyTurn:
        stuff = []
        for i in attacking:
            if False in i[7]:
                stuff.append(i)
        attacking = stuff


def damageControl(classes):
    global attackFrame, whichSelection, allyAttack, energyGain, fightyLoop, keyDone, actionWhich
    for num, ally in enumerate(theAlly):
        hitOnce = False
        strike = True
        animate = True
        notHit = False
        failed = False
        failedFully = False
        barIsConsidered = []

        if ally.tempClass in ['Tank', 'Controller']:

            if ally.tempClass != classes or keyDone[num] != True:
                continue
        elif ally.tempClass != classes:
            continue

        if 'slash' in ally.weapon.type:
            weaponUsed = slash
        elif 'bash' in ally.weapon.type:
            weaponUsed = bash
        elif 'range' in ally.weapon.type:
            weaponUsed = proj
        else:
            weaponUsed = magic
        weaponUsed = [0, 0]

        #prevNum = attackFrame[num]
        strike = True
        animate = True
        if ally.tempClass not in ['a', 'e']:
        #attackFrame[num] = prevNum
            for barNum, bar in enumerate(fightBar):
                if 'NoBar' in bar:
                    continue
                strike = True
                barUsed = fightingBar[bar]
                user = fightingBar[bar][6]
                if user.name != ally.name:
                    continue
                if user.tempClass not in ['']:
                    if ('done' in barUsed[2] or 'failHit' in barUsed[2]) and (not (turnEnemy and opponentBot and not enemyAutoAttack)):# and bar not in barIsConsidered:
                        if bar in barIsConsidered:
                            fightingBar[bar][4] = 1
                            strike = False
                        if 'failHit' in barUsed[2] and not (turnEnemy and opponentBot and not enemyAutoAttack):
                            failed = True
                            failedFully = True
                            theBaring = barUsed[7].bars
                            barUsed[7].nextBar = theBaring[ min(theBaring.index(barUsed[10]) + 1, len(theBaring) - 1 )]
                            for barNum2, moreBar in enumerate(fightBar):
                                if fightingBar[moreBar][6] == user and barNum2 > barNum:

                                    if fightingBar[moreBar][2].lower() in ['done']:
                                        failed = False
                                    if fightingBar[moreBar][2].lower() not in ['failhit', 'done']:
                                        ##print(fightingBar[moreBar][2].lower())
                                        failedFully = False
                                        break
                        if ally.name in bar:
                            identifier = ''
                            dashPassed = 0
                            for letter in bar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    identifier += letter if not letter.isdigit() else ''
        
                            for secondBar in fightBar:
                                secondIdentifier = ''
                                dashPassed = 0
                                for letter in secondBar:
                                    if letter == '_' and dashPassed < 2:
                                        dashPassed += 1
                                    elif dashPassed == 2:
                                        secondIdentifier += letter if not letter.isdigit() else ''
                                if secondIdentifier == identifier and not bar == secondBar and ally == fightingBar[secondBar][6]:
                                    ##print(identifier, secondIdentifier)
                                    barIsConsidered.append(secondBar)
                                    if fightingBar[secondBar][2] == '':
                                        strike = False

                    elif ('done' in barUsed[2] or 'failHit' in barUsed[2]) and (turnEnemy and opponentBot) and bar not in barIsConsidered:
                         if ally.name in bar:
                            if bar in barIsConsidered:
                                fightingBar[bar][4] = 1
                                strike = False
                            #print(True)
                            identifier = ''
                            dashPassed = 0
                            for letter in bar:
                                if letter == '_' and dashPassed < 2:
                                    dashPassed += 1
                                elif dashPassed == 2:
                                    identifier += letter if not letter.isdigit() else ''
                            #print(identifier)
                            identifier = fightingBar[bar][10][0]
                            for secondBar in fightBar:
                                secondIdentifier = fightingBar[secondBar][10][0]
                                
                                if secondIdentifier == identifier and not bar == secondBar and ally == fightingBar[secondBar][6]:
                                    ##print(identifier, secondIdentifier)
                                    barIsConsidered.append(secondBar)
                                    if fightingBar[secondBar][2] == '':
                                        strike = False
                    else:
                         strike = False


                if strike:
                    #if fightingBar[bar][10][1:] != '0':
                        #continue
                    whatFight = fightingBar[bar][7]
                    theAlly[num].activity = 'Attack_hit'
                    if failed:
                        damage = 'MISS'
                        theAlly[num].activity = 'Attack_miss'
                    elif fightingBar[bar][5] <= 0:
                        allyDamage[num] = damage = 1
                    else:
                        damage = math.ceil(fightingBar[bar][5]) if fightingBar[bar][5] != inf else inf
                        allyDamage[num] = math.ceil(allyDamage[num]) if allyDamage[num] != inf else inf

                    supposedDamage = theAlly[num].attack * ((100 - theOpponent[whichSelection[num]].defense)/100) if useDefensePercent else theAlly[num].attack - theOpponent[whichSelection[num]].defense
                    #if fightingBar[bar][5] >= supposedDamage and not failed:
                        #theAlly[num].activity = 'Attack_crit'
                        #print(True)
                    checked = False
                    for i in attacking:
                        if bar in barIsAttacking:
                            checked = True
                            break
                    checked = True if failed else checked
                    if fightingBar[bar][12] == 1:
                        failed = False
                        checked = True
                    if failed:
                        fightingBar[bar][12] = 1
                    doubleAttack = False
                    for i in theAlly[num].passiveBuff:
                        if i.name == 'Double Strike':
                            if theAlly[num].passiveBuff[i][0] == True and theAlly[num].passiveBuff[i][1] == False:
                                doubleAttack = True
                                theAlly[num].passiveBuff[i][1] = True

                    if useDodgeEquation:
                        stupidMiss = (theOpponent[whichSelection[num]].speed/(2*(theOpponent[whichSelection[num]].speed + theAlly[num].speed)))*100
                    else:
                        stupidMiss = int(theOpponent[whichSelection[num]].speed/2)
                    didMiss = 1 if random.randint(1, 100) <= stupidMiss else 0

                    for i in theOpponent[whichSelection[num]].buff:
                        #print(i.name)
                        if i.name == "Blocking":
                            didMiss = 3
                            #print(True)

                        if i.doStun == True:
                            didMiss = 0
                    accuracyChance = 100 - theAlly[num].accuracy*100
                    #print(accuracyChance, theAlly[num].accuracy)
                    didMiss = 2 if random.randint(1, 100) <= accuracyChance else didMiss
                    if whatFight.useHitChance == True:
                        Range = 0
                        if isinstance(theAlly[num], character.Player):
                            attacker = theAlly[num]
                            target = theOpponent[whichSelection[num]]
                            attackIs = 'Player'
                        else:
                            attacker = theAlly[num]
                            target = theOpponent[whichSelection[num]]
                            attackIs = 'Opponent'
                        if attackIs == 'Player':
                            Range = len(theAlly) - 1 - theAlly.index(attacker)
                            Range += 1 + theOpponent.index(target)
                            missChance = 100 - eval(whatFight.hitChanceEquation)
                            chance = random.randint(1, 100)
                            didMiss = 2 if chance <= missChance else didMiss
                        elif attackIs == 'Opponent':
                            Range = theAlly.index(attacker)
                            Range += len(theAlly) - theAlly.index(attacker)
                            missChance = 100 - eval(whatFight.hitChanceEquation)
                            didMiss = 2 if random.randint(1, 100) <= missChance else didMiss

                    if didMiss == 1:
                        theAlly[num].activity = 'Attack_dodged'
                    elif didMiss == 2:
                        theAlly[num].activity = 'Attack_missed'
                    elif didMiss == 3:
                        theAlly[num].activity = 'Attack_blocked'


                    infPresent = False
                    if isinstance(damage, float):
                        if damage == inf:
                            infPresent = True

                    if not checked and (isinstance(damage, int) or infPresent):
                        damagePercent = theOpponent[whichSelection[num]].damage
                        if abs(fightingBar[bar][4] - 1) < 0.01:
                            playSound('Crit_sfx.ogg')
                            if damagePercent != 0:
                                damagePercent += 0.15
                        else:
                            playSound('Attack_sfx.ogg')
                        #if didMiss == 3:
                            #playSound('Block_sfx.ogg')
                        #print(fightingBar[bar][2])
                        barIsAttacking.append(bar)
                        ally.levelUp(0)
                        energyGain += 15 * (ally.productivity)
                        energyLoop.append([theAlly[num], theAlly[num], int(-10 * (ally.productivity) / len(fightUsed[num].bars))])
                        #print(theOpponent[whichSelection[num]].damage)
                        #print(fightingBar[bar])
                        attacking.append([ [theOpponent[whichSelection[num]]] , theAlly[num], theAlly[num].tempClass, round(damage*damagePercent), didMiss, fightUsed[num], fightingBar[bar]])
                        #if doubleAttack:
                            #attacking.append([ [theOpponent[whichSelection[num]]] , theAlly[num], theAlly[num].tempClass, round(damage*damagePercent), didMiss, fightUsed[num]])
                    elif failed or not checked:
                        fightyLoop.append([theOpponent[whichSelection[num]], theAlly[num], damage])
                    if failedFully:
                        actionWhich[num] = 'Done'
                    #actionWhich[num] = 'Done'


def dialogueUpdate():
    global dialogueText
    allyDialogue = {}
    enemyDialogue = {}
    if dialogueText != []:
        font = pygame.font.Font("gameFont.otf", int(40*0.9))
        for num, text in enumerate(dialogueText):
            theText = text[0]
            target = text[1]
            try:
                text[4]
            except:
                text.append(255)
                text.append(False)

            displayed_lines = []
            current_line = ''
            current_width = 0
            maximum = 250
            text[2] += 1
            if text[2] >= 100:
                text[4] -= 40
                text[4] = max(text[4], 0)
                if text[4] == 0:
                    text[3] = True

            # Process each character in the text up to the current text_index
            for char in theText:
                    if char in [";"]:
                        if current_width > maximum:
                            displayed_lines.append(current_line)
                            current_line = ""

                            current_width = 0
                        current_line += char
                        displayed_lines.append(current_line)
                        current_line = ""
                        current_width = 0
                    elif char == "\n":  # Handle explicit line breaks
                        displayed_lines.append(current_line)
                        current_line = ""
                        current_width = 0
                    elif current_width > maximum:  # Start a new line if width exceeds max_width
                        ##print(current_width, hudRect[2], hudRect[4])
                        if char == " ":
                            displayed_lines.append(current_line)
                            current_line = ""
                            current_width = 0
                        else:
                            # Find the last space in the current line
                            last_space_index = current_line.rfind(" ")
                            if last_space_index != -1:  # If space found, break the line at the last space
                                displayed_lines.append(current_line[:last_space_index])
                                current_line = current_line[last_space_index + 1:] + char
                                current_width = font.size(current_line)[0]
                            else:  # If no space found, break the line at the current character
                                displayed_lines.append(current_line)
                                current_line = char
                                current_width = font.size(char)[0]
                    else:
                        current_line += char
                        current_width += font.size(char)[0]

            # Append any remaining text in current_line
            if current_line:
                displayed_lines.append(current_line)

            if isinstance(target, character.Player):
                allyDialogue[target.name + str(num)] = [target, displayed_lines, text[4]]
            else:
                enemyDialogue[target.name + str(num)] = [target, displayed_lines, text[4]]

        x = 0
        for value in allyDialogue.values():
            x += len(value[1])
        maxi = min(5, x)
        mini = max(0, x - 5)
        x = 0
        what = 0
        totalNum = 0
        for num, (key, value) in enumerate(allyDialogue.items()):
            icon = loadImg((f'selectionIcon/{value[0].displayName}.png', 0.20))
            if totalNum >= mini:
                icon.set_alpha(value[2])
                blitObj(hud, icon, 50, 103 + num*50 + what + x*50 - mini*50, 'topleft')
            what += x*50
            for x, text in enumerate(value[1]):
                totalNum += 1
                if totalNum <= mini:
                    continue
                textBar = render_text(text, value[0].color, 38, True, BLACK if value[0].color != (0, 0, 0) else WHITE, 2)
                textBar.set_alpha(value[2])
                blitObj(hud, textBar, 100, 100 + x*50 + num*50 + what - mini*50, 'topleft')

        x = 0
        for value in enemyDialogue.values():
            x += len(value[1])
        maxi = min(5, x)
        mini = max(0, x - 5)
        x = 0
        what = 0
        totalNum = 0
        for num, (key, value) in enumerate(enemyDialogue.items()):
            icon = loadImg((f'selectionIcon/{value[0].displayName}.png', 0.20), flipX=True)
            if totalNum >= mini:
                icon.set_alpha(value[2])
                blitObj(hud, icon, width - 50, 103 + num*50 + what + x*50 - mini*50, 'topright')
            what += x*50
            for x, text in enumerate(value[1]):
                totalNum += 1
                if totalNum <= mini:
                    continue
                textBar = render_text(text, value[0].color, 38, True, BLACK if value[0].color != (0, 0, 0) else WHITE, 2)
                textBar.set_alpha(value[2])
                blitObj(hud, textBar, width - 100, 100 + x*50 + num*50 + what - mini*50, 'topright')


        dialogueList = dialogueText.copy()
        dialogueText.clear()
        for i in dialogueList:
            if i[3] == False:
                dialogueText.append(i)
        #dialogueText = dialogueList


def effectTextUpdate():
    global effectText
    if effectText != []:
        effectNum = {}
        for num, text in enumerate(effectText):
            try:
                text[4]
            except:
                text.append(0)
            effect = text[0]
            target = text[1]
            if target not in effectNum:
                effectNum[target] = 0
            effectText[num][4] = effectNum[target]
            effectNum[target] += 1

        for num, text in enumerate(effectText):
            try:
                text[4]
            except:
                text.append(0)
            effect = text[0]
            target = text[1]

            if text[2] < math.pi:
                text[2] += math.pi/30 * theDelta
            else:
                text[2] = math.pi
                text[3] = True
            theTween = text[2]
            num = effectText[num][4]

            if isinstance(target, character.Player):
                for allyNum, ally in enumerate(party):
                    if ally == target:
                        break
                sprite = playerSprite[allyNum]

            if isinstance(target, character.Opponent):
                for opponentNum, enemies in enumerate(opponent):
                    if enemies == target:
                        break
                sprite = enemySprite[opponentNum]

            coordsUsed = sprite.pos
            x = coordsUsed[0]
            y = coordsUsed[1] - 80*math.sin(theTween/2) + 30*num

            alpha = 255*(1 - theTween / math.pi)
            #print(effect)

            textEffect = render_text(effect.name, effect.color, 38, True, BLACK, 2)
            textEffect.set_alpha(alpha)
            blitObj(screen, textEffect, x, y)

        stuff = True
        for i in effectText:
            if i[3] == False:
                stuff = False
        if stuff == True:
            effectText.clear()

def screenStuff():
    global screenText
    if screenText != []:
        for num, text in enumerate(screenText):
            theText = text[0]
            color = text[1]
            try:
                text[4]
            except:
                fontSize = 46
            else:
                fontSize = text[4]
            try:
                text[5]
            except:
                y_offset = 0
            else:
                y_offset = text[5]

            if text[2] < math.pi:
                text[2] += math.pi/30 * theDelta
            else:
                text[2] = math.pi
                text[3] = True
            theTween = text[2]

            x = width/2
            y = 300 - 80*math.sin(theTween/2)

            alpha = 255*(1 - theTween / math.pi)

            textEffect = render_text(theText, color, fontSize, True, BLACK, 2)
            textEffect.set_alpha(alpha)
            blitObj(hud, textEffect, x, y+y_offset)

        stuff = True
        for i in screenText:
            if i[3] == False:
                stuff = False
        if stuff == True:
            screenText = []


def effectUpdate():
    global oldCycle
    # Effect, Target, firstTimeBool
    effectStuff = character.effectStuff
    effected = effectStuff.copy()
    stuff = effected
    reset = False
    mustChange = {}
    if effected != {}:
        for key in effected:
            if effected[key][2] != 'Passive':
                target = effected[key][1]
                caster = effected[key][3]
                effect = key[0]
                mustChange[caster] = False
                firstTime = effected[key][2]
                if caster not in oldCycle:
                    #print(True)
                    continue

                if not firstTime and target.buff[effect][3] > 0 and target.buff[effect][0] == 0:
                    target.buff[effect][3] -= 1
                    effected[key][5] -= 1

                if oldCycle[caster] != newCycle[caster]:
                    mustChange[caster] = True
                    if not firstTime and target.buff[effect][0] > 0:
                        target.buff[effect][0] -= 1
                        effected[key][0] -= 1

                amplifier = effected[key][4]
                if effected[key][0] == 0 and effected[key][5] == 0:
                    pass
                else:
                    finalNum = (target.level * effect.multiplier)/10 + effect.num
                    target.levelUp(0, False)
                    applyBuffAgain = False
                    if firstTime:
                        applyBuffAgain = True
                        effected[key][2] = False
                        if reset == None:
                            target.levelUp(0, False)
                            reset = True
                    if effect.applyRepeated:
                        applyBuffAgain = True
                        effectNum = 0
                        target.levelUp(0, False)

                        for theStuff in target.addBase:
                            effectNum = 0
                            present = False
                            extraDict = target.addBase[theStuff].copy()
                            for umm in extraDict:
                                if effect.name in umm:
                                    effectNum += 1
                                    present = True
                            if present:
                                target.addBase[theStuff][effect.name +  str(effectNum)] = target.addBase[theStuff][effect.name]


                    if applyBuffAgain:
                        effectText.append([effect, target, 0, False])
                    if applyBuffAgain and not (effect.useAtStart == False and firstTime == True):
                        target.levelUp(0, False)
                        if effect.name == 'Bleeding':
                            damage = 5 * amplifier
                            fightyLoop.append([target, effect, int(damage)])

                        elif effect.name == 'Burning':
                            damage = 6 * amplifier
                            fightyLoop.append([target, effect, int(damage)])

                        elif effect.name == 'Weakness':
                            target.addBase['attack'][effect.name] = target.attack / 100 * finalNum

                        elif effect.name == 'Angry':
                            target.addBase['attack'][effect.name] = target.attack / 100 * finalNum

                        elif effect.name == 'Insane':
                            target.addBase['attack'][effect.name] = target.attack / 100 * finalNum
                            target.addBase['defense'][effect.name] = target.defense / 100 * finalNum

                        elif effect.name == 'Shielded':
                            target.addBase['defense'][effect.name] = target.defense / 100 * finalNum

                        elif effect.name == 'Defended':
                            target.addBase['damage'][effect.name] = 0.5

                        elif effect.name == 'Regeneration':
                            fightyLoop.append([target, effect, -1 * int(target.maxhp / 100 * finalNum)])
                        elif effect.name == 'Frozen' and not firstTime:
                            resetAllyTurn()
                            continue
                        elif effect.name == 'Encouraged':
                            target.addBase['defense'][effect.name] = target.defense * 0.2

                        elif effect.name == 'Healing':
                            fightyLoop.append([target, effect, -1 * int(effect.num) * amplifier])

                        elif effect.name == 'Vitality':
                            target.addBase['hp'][effect.name] = target.maxhp / 100 * effect.num * amplifier

                        elif effect.name == 'Force':
                            target.addBase['attack'][effect.name] = target.attack / 100 * effect.num * amplifier

                        elif effect.name == 'Momentum':
                            target.addBase['speed'][effect.name] = target.speed / 100 * effect.num * amplifier

                        elif effect.name == 'Guard':
                            target.addBase['defense'][effect.name] = target.defense / 100 * effect.num * amplifier

                        elif effect.name == 'Reach':
                            target.addBase['range'][effect.name] = target.range / 100 * effect.num * amplifier

                        elif effect.name == 'Efficiency':
                            target.addBase['productivity'][effect.name] = target.productivity / 100 * effect.num * amplifier

                        elif effect.name == 'Overdrive':
                            target.addBase['attack'][effect.name] = target.attack / 100 * effect.num * amplifier
                            target.addBase['speed'][effect.name] = target.speed / 100 * effect.num * amplifier
                            target.addBase['defense'][effect.name] = target.speed / 100 * effect.num * amplifier
                            target.addBase['productivity'][effect.name] = target.productivity / 100 * effect.num * amplifier

                        elif effect.name == 'Poison':
                            fightyLoop.append([target, effect, int(effect.num) * amplifier])

                        elif effect.name == 'Vulnerable':
                            target.addBase['hp'][effect.name] = -target.maxhp / 100 * effect.num * amplifier

                        elif effect.name == 'Confusion':
                            target.addBase['attack'][effect.name] = -target.attack / 100 * effect.num * amplifier

                        elif effect.name == 'Slow':
                            target.addBase['speed'][effect.name] = -target.speed / 100 * effect.num * amplifier

                        elif effect.name == 'Distracted':
                            target.addBase['defense'][effect.name] = -target.defense / 100 * effect.num * amplifier

                        elif effect.name == 'Restricted':
                            target.addBase['range'][effect.name] = -target.range / 100 * effect.num * amplifier

                        elif effect.name == 'Blindness':
                            target.addBase['accuracy'][effect.name] = -target.range / 100 * effect.num * amplifier

                        elif effect.name == 'Tired':
                            target.addBase['productivity'][effect.name] = -target.productivity / 100 * effect.num * amplifier
                        target.levelUp(0, True)
            else:
                passiveEffect = key[0]
                target = effected[key][0]
                usedIt = effected[key][1]
                #print(passiveEffect.name, target.name)

                boolean = False
                if passiveEffect.stackable:
                        applyBuffAgain = True
                        effectNum = 0
                        target.levelUp(0, False)

                        for theStuff in target.addBase:
                            effectNum = 0
                            present = False
                            extraDict = target.addBase[theStuff].copy()
                            for umm in extraDict:
                                if key.name in umm:
                                    effectNum += 1
                                    present = True
                            if present:
                                target.addBase[theStuff][key.name +  str(effectNum)] = target.addBase[theStuff][key.name]

                if passiveEffect.name == 'Locked In':
                    if target.hp/target.maxhp <= 0.3:
                        boolean = True
                        if not usedIt:
                            target.addBase['attack'][passiveEffect.name] = target.attack * 0.3
                    else:
                        boolean = False
                        #target.passiveBuff[passiveEffect][0] = False


                if passiveEffect.name == 'Iteker':
                    if turn >= 15:
                        boolean = True
                        usedIt = True
                        if (turn - 15)%10 == 0:
                            usedIt = False
                            for keyStuff in target.fight[0].applyEffect:
                                target.fight[0].applyEffect[keyStuff][1] += 1
                                target.fight[0].applyEffect[keyStuff][1] = min(target.fight[0].applyEffect[keyStuff][1], 5)

                if passiveEffect.name == 'Boosters':
                    if target.hp/target.maxhp <= 0.5:
                        boolean = True
                        if not usedIt and passiveEffect.name not in target.addBase['speed']:
                            target.addBase['speed'][passiveEffect.name] = target.speed * 0.50
                        else:
                            usedIt = True

                if passiveEffect.name == 'Glitched':
                    boolean = random.choice([True, False, False, False, False])
                    if boolean:
                        target.addBase['attack'][passiveEffect.name] = target.attack * 0.25

                if passiveEffect.name == 'Double Strike':
                    if target.hp/target.maxhp <= 0.2:
                        if usedIt:
                            for fightObj in target.fight:
                                fightObj.bars = ['A1']
                        else:
                            for fightObj in target.fight:
                                fightObj.bars = ['A1', 'B1']
                        boolean = True
                    else:
                        for fightObj in target.fight:
                            fightObj.bars = ['A1']

                if (passiveEffect.name == 'Sadism' or passiveEffect.name == 'Disperse') and usedIt:
                    boolean = True
                    effected[key][1] = usedIt = False

                if passiveEffect.name == 'Ready To Strike':
                    boolean = True
                    if usedIt:
                        target.addBase['attack'][passiveEffect.name] = target.attack * 0.25
                        usedIt = False
                    else:
                        usedIt = True

                if passiveEffect.name == 'Productivity Zero':
                    boolean = True
                    if usedIt:
                        target.addBase['productivity'][passiveEffect.name] = -1
                        usedIt = False
                    else:
                        usedIt = True

                if passiveEffect.name == 'Regeneration':
                    boolean = True
                    fightyLoop.append([target, passiveEffect, -5])

                if passiveEffect.name == 'Cane Healing' and usedIt:
                    boolean = True
                    effected[key][1] = usedIt = False

                if passiveEffect.name == 'Healing Tunes':
                    if oldCycle[target] != newCycle[target]:
                        mustChange[target] = True
                        if isinstance(target, character.Player):
                            whichOne = party
                            sprite = playerSprite[ whichOne.index(target) ]
                        else:
                            whichOne = opponent
                            sprite = enemySprite[ whichOne.index(target) ]
                        playAnimation(sprite, 'skill', duration=1, resetDuration=True)
                        #print(sprite.currentAnim, sprite.timerAnim)
                        boolean = True
                        usedIt = False
                        listThing = getCharacter(whichOne, target, 1)
                        for i in listThing:
                            fightyLoop.append([i, target, -15])
                    else:
                        boolean = False
                        usedIt = True

                if boolean == True and not usedIt:
                    effectText.append([passiveEffect, target, 0, False])

                target.passiveBuff[passiveEffect][0] = boolean


        for key in mustChange:
            if mustChange[key] == True:
                oldCycle[key] = newCycle[key]
        daeffected = effected.copy()
        for key in daeffected:
            target = effected[key][1]
            effect = key[0]
            passivity = True if effected[key][2]  == 'Passive' else False

            if effected[key][0] == 0 and effected[key][5] == 0 and effected[key][2] != 'Passive':
                del target.buff[effect]
                del effected[key]
                effectNum = 1
                for theStuff in target.addBase:
                    effectNum = 0
                    for umm in target.addBase[theStuff]:
                        if effect.name in umm:
                            effectNum += 1
                    for number in range(1, effectNum):
                        if effect.applyRepeated:
                            del target.addBase[theStuff][effect.name +  str(number)]
                        else:
                            del target.addBase[theStuff][effect.name]

                for every in target.addBase.values():
                    ori = every.copy()
                    for keys in ori:
                        every[effect.name] = None
                        del every[effect.name]

            if not passivity:
                target.levelUp(0, True)

            if passivity:
                target = effected[key][0]
                if target.passiveBuff[effect][0] == False:
                    target.passiveBuff[effect][1] = False

                    for theStuff in target.addBase:
                        effectNum = 0
                        for umm in target.addBase[theStuff]:
                            if effect.name in umm:
                                effectNum += 1
                        for number in range(1, effectNum):
                            del target.addBase[theStuff][effect.name +  str(number)]

                    for every in target.addBase.values():
                        ori = every.copy()
                        for keys in ori:
                            every[effect.name] = None
                            del every[effect.name]
                target.levelUp(0, True)

        effected = {}
        daeffected = {}
        effectStuff = {}
        character.effectStuff = {}


def theSelectHud(useAlly=False, useEnemy=False, useBoth=False):
    whatCoords = coords
    switchCheroo = False
    if not opponentBot and turnEnemy:
        switchCheroo = True
        #oriAlly = useAlly
        #useAlly = useEnemy
        #useEnemy = oriAlly

    #if switchCheroo:
    #    if isinstance(whichSelection[selectedWhich], list):
    #        selectionThing = len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect]
    #    else:
    #        selectionThing = len(theOpponent) - 1 - whichSelection[selectedWhich]
    #else:
    if isinstance(whichSelection[selectedWhich], list):
        selectionThing = whichSelection[selectedWhich][multiSelect]
    else:
        selectionThing = whichSelection[selectedWhich]

    if (useEnemy) and not useAlly:
        whatCoords = playerCoords if coords != playerCoords else opponentCoords
    elif not useBoth:
        whatCoords = coords
    if useBoth:
        whatCoords = playerCoords + opponentCoords

    if (useAlly) and not useEnemy:
        showingEnemy = theAlly[selectionThing]
        whatCoords = playerCoords if coords != playerCoords else opponentCoords
        whatSprite = sprite
    elif not useBoth:
        showingEnemy = theOpponent[selectionThing]
        whatCoords = coords
        whatSprite = (playerSprite if sprite != playerSprite else enemySprite)
    if useBoth:
        if turnEnemy:
            bothParty = opponent + party
            showingEnemy = bothParty[selectionThing]
            whatCoords = opponentCoords + playerCoords
            whatSprite = enemySprite + playerSprite
        elif turnAlly:
            bothParty = party + opponent
            showingEnemy = bothParty[selectionThing]
            whatCoords = playerCoords + opponentCoords
            whatSprite = playerSprite + enemySprite

    showBool = False
    if isinstance(showingEnemy, character.Opponent):
        showBool = True

    x = whatSprite[selectionThing].pos[0]
    y = whatSprite[selectionThing].pos[1]
    #x =
    x -= 100 if x > width/2 else -100#((turnAlly or useEnemy) and not useAlly and not useBoth) or (useBoth and showBool) else -100
    y = 150 + 5*math.sin(2*math.pi*(frame%30)/(30*(1/theDelta)))

    ehealth_ratio = showingEnemy.hp / showingEnemy.maxhp
    espare_ratio = showingEnemy.mana / showingEnemy.maxMana

    theOpponentname = render_text(showingEnemy.name, YELLOW if showingEnemy.spare == 100 else WHITE, 40)
    theOpponentname_rect = theOpponentname.get_rect(center=(x, y))
    name_bg_padding = 10  # Padding around the text
    # Add a black background layer with a border behind the name
    name_bg_padding = 10  # Padding around the text
    border_thickness = 6  # Thickness of the border
    name_bg_color = (0, 0, 0)  # Black background color
    border_color = showingEnemy.color  # White border color

    # Define the background rectangle
    name_bg_rect = pygame.Rect(
        theOpponentname_rect.left - name_bg_padding,
        theOpponentname_rect.top - name_bg_padding,
        theOpponentname_rect.width + 2 * name_bg_padding,
        theOpponentname_rect.height + 2 * name_bg_padding
    )

    border_bg_rect = pygame.Rect(
        theOpponentname_rect.left - name_bg_padding - border_thickness,
        theOpponentname_rect.top - name_bg_padding - border_thickness,
        theOpponentname_rect.width + 2 * name_bg_padding + border_thickness * 2,
        theOpponentname_rect.height + 2 * name_bg_padding + border_thickness * 2
    )

    # Draw the border
    drawRect(screen, border_color, border_bg_rect)  # Border slightly larger than the background

    # Draw the black background
    drawRect(screen, name_bg_color, name_bg_rect)

    blitObj(screen, theOpponentname, x, y)

    # Positioning calculations
    top = theOpponentname_rect.top
    left = theOpponentname_rect.left
    right = theOpponentname_rect.right
    down = theOpponentname_rect.bottom

    if isinstance(showingEnemy, character.Opponent):#((turnAlly or useEnemy) and not useAlly and not useBoth) or (useBoth and showBool):
        scrolly = loadImg(("scroll.png", 0.3, color[selectedWhich]), flipX=False)
        # Health bar is positioned to the left of the name
        hp_width = 160  # Width of the health bar
        hp_height = 30  # Height of the health bar
        hp_margin = 20  # Margin between the health bar and the text
        hpX = left - hp_width - hp_margin  # Left of health bar
        hpY = y - hp_height / 2  # Vertically centered with respect to the text
    elif isinstance(showingEnemy, character.Player):
        scrolly = loadImg(("scroll.png", 0.3, color[selectedWhich]), flipX=True)
        # Health bar is positioned to the right of the name
        hp_width = 160  # Width of the health bar
        hp_height = 30  # Height of the health bar
        hp_margin = 20  # Margin between the text and the health bar
        hpX = right + hp_margin  # Start from the right of the text with some margin
        hpY = y - hp_height / 2  # Vertically centered with respect to the text


    # Drawing the health bars
    ehealthbar_bg = drawRect(screen, BLACK, (hpX - 5, hpY - 5, hp_width + 10, hp_height + 10))  # Outer border
    ehealthbar_bg = drawRect(screen, (70, 70, 70), (hpX - 5, hpY - 5, hp_width + 10, hp_height + 10))  # Outer border
    ehealthbar = drawRect(screen, (100, 100, 100), (hpX, hpY, hp_width, hp_height))  # Background bar
    ehealthbar_bg = drawRect(screen, (0, 180, 0), (hpX - 5, hpY - 5, ehealth_ratio * (hp_width + 10), hp_height + 10))  # Outer border
    ehealthfg = drawRect(screen, (0, 255, 0), (hpX, hpY, hp_width * ehealth_ratio, hp_height))  # Health fill

    # Add percentage text inside the health bar
    health_percentage_text = render_text(f"{round(showingEnemy.hp)}/{showingEnemy.maxhp}", BLACK, 35)  # Smaller text size
    blitObj(screen, health_percentage_text, hpX + hp_width/2, y)


    # Spare bar is positioned below the health bar

    spare_width = 100
    spare_height = 10  # Height of the spare bar
    spare_margin = 15  # Margin between health bar and spare bar
    spareY = hpY - spare_height - spare_margin
    spareX = hpX if turnAlly else hpX + hp_width - spare_width

    esparebar_bg = drawRect(screen, (70, 70, 70), (spareX - 5, spareY - 5, spare_width + 10, spare_height + 10))  # Outer border
    esparebar_bg = drawRect(screen, (0, 170, 170), (spareX - 5, spareY - 5, (spare_width + 10)* espare_ratio, spare_height + 10))  # Outer border
    esparebar = drawRect(screen, (100, 100, 100), (spareX, spareY, spare_width, spare_height))  # Background bar
    esparefg = drawRect(screen, (0, 255, 255), (spareX, spareY, spare_width * espare_ratio, spare_height))  # Spare fill

    # Draw scroll indicators around the text
    if isinstance(showingEnemy, character.Opponent):
        blitObj(screen, scrolly, right + 5*math.sin(2*math.pi*(frame%60)/60), y - 20, 'topleft')
    else:
        rectStuff = scrolly.get_rect(topright=(left + 5*math.sin(2*math.pi*(frame%60)/60), y - 20))
        blitObj(screen, scrolly, left + 5*math.sin(2*math.pi*(frame%60)/60), y - 20, 'topright')

def mouseHover():
    for i in screenWindow.sprites.values():
        if i.mouseCollide == False:
            continue

        goHighlight = False
        if i.checkMouse(True):
            if i.targetScale != 1.3:
                i.tweenScale(1.3, 'circOut', 0.1, True)
            goHighlight = True
        elif i.mouseCollide == True:
            if i.targetScale != 1:
                i.tweenScale(1, 'circOut', 0.3, True)

        if goHighlight:
            rect = i.getRect()
            size = i.getSize()
            thickness = 5
            pygame.draw.rect(screen.surface, YELLOW, (rect.x - thickness, rect.y - thickness, size[0] + 2*thickness, size[1] + 2*thickness))

def mouseTouch(sprite, useClick=True, useHold=False, timeTaken=15, delay=5):
    global mouseTimer
    if sprite.checkMouse(True):
        if useClick:
            if mouseDown:
                if sprite.targetScale != 0.9:
                    sprite.tweenScale(0.9, 'circOut', 0.03, True)

                return True
        if useHold:
            if mouseHold:

                if sprite.targetScale != 0.9:
                    sprite.tweenScale(0.9, 'circOut', 0.03, True)

                mouseTimer += 1
                if mouseTimer == timeTaken:
                    mouseTimer = timeTaken - 1
                    if frame%delay == 0:
                        return True
            else:
                mouseTimer = 0
    return False

def addTurnDialogue(potrait=None, dialogue='', turn=0, emotion=None, doClear=False, doSpam=False):
    global turnDialogue
    canProceed = False
    if potrait == 'Clear' or doClear:
        clear = True
    else:
        clear = False
    while turn > len(turnDialogue):
        turnDialogue.append([[], [], True, 0, [], set([])])
    if not doSpam:
        if str(potrait) + str(dialogue) + str(emotion) not in turnDialogue[turn-1][5]:
            canProceed = True
    else:
        canProceed = True
    if not clear and canProceed:
        turnDialogue[turn-1][0].append(potrait)
        turnDialogue[turn-1][1].append(dialogue)
        turnDialogue[turn-1][2] = False
        turnDialogue[turn-1][4].append(emotion)
        turnDialogue[turn-1][5].add(str(potrait) + str(dialogue) + str(emotion))
    if clear:
        turnDialogue[turn-1][0] = []
        turnDialogue[turn-1][1] = []
        turnDialogue[turn-1][2] = False
        turnDialogue[turn-1][3] = 0
        turnDialogue[turn-1][4] = []
        turnDialogue[turn-1][5] = set([])

def setTurnText(text, potrait=None, emotion=None):
    global inTurnText
    inTurnText[1] = text
    inTurnText[0] = potrait
    inTurnText[2] = emotion

def isInDialogue(turn, dialogueIndex):
    if len(turnDialogue) < turn:
        return False
    if isinstance(dialogueIndex, int):
        if turnDialogue[turn-1][3] == dialogueIndex:
            return True
    return False

turn = 0
cycle = 0
newCycle = {}
oldCycle = {}
for i in opponent:
    newCycle[i] = 0
    oldCycle[i] = 0
for i in party:
    newCycle[i] = 0
    oldCycle[i] = 0
enemyShakePos = []
playerShakePos = []

dialogueText = character.dialogueText
effectText = character.effectText

actionWhich = 0
whichSelection = 0
selectedWhich = 0
theAlly = 0
theOpponent = 0
coords = 0
whichTurn = 0


oriCoords = []

attacking = []


backUpCoords = []
hudTween = 0
swap = False
swapFinally = False
original = ''

#soundVolume = 1
#musicVolume = 1

centerX = 500
centerY = 435
hudLength = 0
hudHeight = 180
hudX = centerX - (hudLength / 2)
hudY = centerY - (hudHeight / 2)
thickness = 6

hudRect = [centerX, centerY, hudLength, hudHeight, hudX, hudY, thickness]
transition = 0
currentChange = []

playerAnim = {'idle': 0, 'attackPrep': 0, 'attack': 0, 'hurt': 0}
playerAnimList = []
playerAlpha = []
enemyAlpha = []
playerSprite = []
enemySprite = []
playerFloat = []
enemyFloat = []
enemyTween = []
for i in party:
    playerAnimList.append(playerAnim.copy())
    playerSprite.append(0)
    playerFloat.append(0)
    playerShakePos.append(())
opponentHp = []
opponentAlpha = []
opponentCoords = []
playerCoords = []
for i in opponent:
    enemyTween.append(0)
    opponentCoords.append([])
    i.levelUp(0)
    i.hpSet()
    enemySprite.append(0)
    enemyFloat.append(0)
    enemyAlpha.append(0)
    enemyShakePos.append(())

for i in party:
    playerCoords.append([])
    playerAlpha.append(255)
for num, enemies in enumerate(opponent):
    opponentHp.append(enemies.hp)
    opponentAlpha.append(255)
    x = 600*((width/2)/500) + 200*((width/2)/500)/len(opponent) + 400*(width/1000)/len(opponent) * num
    y = 200
    opponentCoords[num] = [x, y]

for num, players in enumerate(party):
    x = 200*((width/2)/500)/len(party) + 400*(width/1000)/len(party) * num
    y = 200
    playerCoords[num] = [x, y]


slash = character.slash
bash = character.bash
proj = character.proj
magic = character.magic

color = []
colorOfAlly = []
colorOfEnemy = []
for i in party:
    i.levelUp(0)
    colorOfAlly.append(i.color)
    i.hpSet()

for i in opponent:
    colorOfEnemy.append(i.color)

floaty = 0

selectedAlly = 0
selectedAction = 0
multiSelect = 0
allyAction = []
battleSplash = True
allySelection = []
whichAction = []
allyTurn = True
enemyTurn = False
tempAlly = len(party) + 1

selectedEnemy = 0
selectedAction = 0
multiSelect = 0
enemyAction = []
battleSplash = True
enemySelection = []
whichAction = []
enemyTurn = False
tempEnemy = len(opponent) + 1


playerShakeX = []
playerShakeBool = []

speedBasedTurn = True
speedNum = 0
speedOrder = []
speedNumOrder = -1
for num, i in enumerate(party):
    speedOrder.append([i.speed, num, 'Player', i.name])

for num, i in enumerate(opponent):
    speedOrder.append([i.speed, num, 'Enemy', i.name])

organise = False
while not organise:
    organise = True
    for num, i in enumerate(speedOrder):
        if num + 1 < len(speedOrder):
            if i[0] > speedOrder[(num + 1)][0]:
                speedOrder[num], speedOrder[num + 1] = speedOrder[num + 1], speedOrder[num]
                organise = False
speedOrder.reverse()


opponentEnergy = 0
originalEnergy = 50
energy = 0
energyGain = 0
energyUsed = 0
energyTrans = 0
inSkill = False
skillParty = 0
skillUsed = []

inItem = False
itemParty = 0
itemHeal = []
itemUsed = []
itemNum = []

inAct = False
actionDia = []
actionNum = 0
actUsed = []
actParty = 0

fightyLoop = character.fightyLoop
energyLoop = character.energyLoop

attackFrame = []
fightBar = []
barIsAttacking = []
fightingBar = {}
fightBarX = []
fightBarX2 = []
fightScale = []
barAlpha = []
allyStrike = []
allyDamage = []
allyAttack = []
opponentSmoothDamage = []
enemyShakeX = []
enemyShakeBool = []
inBar = 0
fightFrame = 0
attackFade = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
inFight = False
barSelect = 0
damageX = []
damageY = []
damageY2 = []
fightUsed = []

enemyStrike = []
enemyDamage = []
enemyAttack = []
enemySmoothDamage = []
enemyShakeX = []
enemyShakeBool = []
inBar = 0
fightFrame = 0
attackFade = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
inFight = False
barSelect = 0
damageX = []
damageY = []
damageY2 = []

meleeDone = False
throwerDone = False
rangeDone = False
tankDone = False
controllerDone = False
supportDone = False
underDone = False
slamDone = False
backDone = False
holdDone = False

meleeUsed = False
throwerUsed = False
rangeUsed = False
tankUsed = False
controllerUsed = False
supportUsed = False
underUsed = False
slamUsed = False
backUsed = False
holdUsed = False

splashy = ''
text_index = 0

allyTween = []
enemyTween = []
opponentBot = False
for i in party:
    allyTween.append(0)
    allySelection.append(0)
    itemHeal.append(0)
    allyAction.append(None)
    whichAction.append(0)
    allyStrike.append(False)
    skillUsed.append(0)
    itemNum.append(0)
    playerShakeX.append(0)
    playerShakeBool.append(False)
    #print(i.name, i.xp)

for i in opponent:
    enemyTween.append(0)
    enemySelection.append(0)
    itemHeal.append(0)
    enemyAction.append(None)
    whichAction.append(0)
    enemyStrike.append(False)
    skillUsed.append(0)
    itemNum.append(0)
    enemyShakeX.append(0)
    enemyShakeBool.append(False)
    i.levelUp(0)

frame = screenWindow.frame
time = 0.0
cycle = 0
hudScroll = 0
movingHud = 0
ripple = []
cycling = 0
debug = False
debugList = ['', 'windowSize', 'wavey', 'characters', 'modify']
whichPage = {'botPlay': False, 'windowSize': False, 'wavey': False, 'characters': False, 'modify': False}
debugSelect = 0
enemyAutoAttack = True
botplay = screenWindow.trigger['Botplay'].boolean#screenWindow.controlVar[0][1]
hardMode = screenWindow.trigger['Hard Mode'].boolean
easyMode = screenWindow.trigger['Easy Mode'].boolean
canGainXp = screenWindow.controlVar[1][1]
wavey = False
instantAttack = True

keyUsed = []
keyHit = []
keyDone = []
keyUsedBool = []



turnAlly = False
turnEnemy = True
cycle = 1


globalList = []
globalLibrary = {}


effectiveRange = 0

dafps = 60

playBack = 1 * 30 * 1/max(25, min(60, (dafps/2)))
songBpm = 175 * playBack
beat = 0
lastBeat = pygame.time.get_ticks()

stuff = random.randint(0, 10)

baseTextBoxHeight = 180
textBox = baseTextBoxHeight
start_time = Time.perf_counter()
music = {}

# Initial audio stream with normal speed
songPos = 0

#pygame.mixer.music.load(audio_stream) # Loads the background music
#pygame.mixer.music.load(f'sounds/music/{stuff}.mp3')
#pygame.mixer.music.play(loops=-1)
#debug_test(screen)
#music = DynamicMusicPlayer(f"sounds/bgm.ogg", loop=True)
#music.fade_in()
debug_test(screen)
fullscreen = screenWindow.fullscreen
useExtraDialogue = True
useDodgeEquation = False
useCustomDialogue = True
backgroundNum = random.randint(0,15)
turnDialogue = [[[None, None, None], ['Get ready to rumble.'], False, 0, [None]]]
bossFight = False
tutorial = False
inTurnText = [None, 'Text', None]
#pygame.mixer.music.load(f'data/sounds/music/BattleMusic.mp3')
#backgroundNum = 17
#pygame.mixer.music.play(loops=-1)
stress = 0
inBattle = True
animate = False
strike = False
camSet(1.5, BLACK, 255, 0)

battleStart = 30
screenText = []
theDelta = 0
beatMultiply = 1

hud.cameraY = height + 200
hud.move_to(0, 0, 1)

screen.start_fade(BLACK, 255, 1)
hud.start_fade(BLACK, 255, 1)
backGroundScreen.start_fade(BLACK, 255, 1)
desktopX, desktopY = pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]
attackMeterX = 0
deadCount = 0
mouseHold = mouseDown = False
MUSICSTART = False
commandMode = False
commandText = ''
buffMenu = False
buff_tweenY = 1000
music = None

renderDamageText = True

def onUpdate():
    pass
def onStart():
    pass
def onEnd():
    pass

def speedReset():
    global speedNum, speedOrder, speedNumOrder, selectedWhich, selectedAlly, selectedEnemy
    oriInstance = speedOrder[speedNumOrder][2]
    oriName = speedOrder[speedNumOrder][3]
    speedNum = 0
    speedOrder = []
    speedNumOrder = -1
    for num, i in enumerate(party):
        i.levelUp(0)
        speedOrder.append([i.speed, num, 'Player', i.name])

    for num, i in enumerate(opponent):
        i.levelUp(0)
        speedOrder.append([i.speed, num, 'Enemy', i.name])

    organise = False
    while not organise:
        organise = True
        for num, i in enumerate(speedOrder):
            if num + 1 < len(speedOrder):
                if i[0] > speedOrder[(num + 1)][0]:
                    speedOrder[num], speedOrder[num + 1] = speedOrder[num + 1], speedOrder[num]

                    organise = False
    speedOrder.reverse()
    for num, i in enumerate(speedOrder):
        if i[3] == oriName:
            if i[2] == oriInstance:
                speedNumOrder = num
                break
    for num, i in enumerate(theAlly):
        if i.name == speedOrder[speedNumOrder][3]:
            selectedWhich = num
            if isinstance(i, character.Player):
                selectedAlly = num
            else:
                selectedEnemy = num
            speedNum = num
character.speedReset = speedReset

selectedBuff = 0
buffScroll = 0
actCall = character.actCall
useAnim = False
audio = None
if sys.platform == "emscripten":
    from js import document
    audio = document.getElementById("bgmusic")
def main(Players, Enemies, useSpeedTurn=True, usingDebug=False, battleData=None):
    global music, oldCycle, newCycle
    global party, opponent, speedBasedTurn, speedNum, speedOrder, speedNumOrder, bossFight, useExtraDialogue, useDodgeEquation, useHitChance, useCustomDialogue, useDefensePercent, dacycle, oldCycle, newCycle
    global inBattle, frame, time, cycling, fullscreen, dafps, battleStart, turnAlly, turnEnemy, allyTurn, enemyTurn, botplay, color, battleSplash, bossFight, backgroundNum, useExtraDialogue
    global selectedAlly, selectedEnemy, allySelection, enemySelection, allyAction, enemyAction, floaty, energy, energyGain, energyTrans, allyTween, enemyTween
    global movingHud, tempAlly, actions, text_index, splashy, inFight, inSkill, inAct, inItem, speedNum, actionWhich, theAlly, theOpponent, whichSelection, selectedWhich
    global meleeDone, rangeDone, throwerDone, tankDone, controllerDone, supportDone, underDone, slamDone, backDone, holdDone
    global meleeFound, rangeFound, throwerFound, tankFound, controllerFound, supportFound, underFound, slamFound, backFound, holdFound
    global meleeUsed, rangeUsed, throwerUsed, tankUsed, controllerUsed, supportUsed, underUsed, slamUsed, backUsed, holdUsed, commandText
    global meleeParticipants, rangeParticipants, throwerParticipants, tankParticipants, controllerParticipants, supportParticipants, underUsed, slamParticipants, backParticipants, holdParticipants
    global attack_rect, inBar, effectiveRange, attackMeterX, hud, screen, baseTextBoxHeight, textBox, hudRect, theDelta, deadCount, mouseHold, mouseDown, MUSICSTART, commandMode
    global party, scaleFactor, buffMenu, buff_tweenY, deltaTime, text_index, allyHudX, enemyHudX, opponentBot, energy, energyTrans, energyGain
    global playerAlpha, enemyAlpha, playerSprite, enemySprite, playerFloat, enemyFloat, enemyTween, opponentCoords, enemyShakeX, enemyShakeBool
    global opponentCoords, opponentAlpha, tutorial, turnDialogue, botplay, hardMode, easyMode, enemyAutoAttack, useExtraDialogue, instantAttack, intenseMode, intenseX

    global turn, cycle, newCycle, oldCycle, theAlly, theOpponent, coords, whichTurn, oriCoords, attacking, backUpCoords, hudTween, swap, swapFinally, original
    global centerX, centerY, hudLength, hudHeight, hudX, hudY, thickness, opponentCoords, playerCoords
    global transition, playerAlpha, colorOfAlly, colorOfEnemy, selectedAction, multiSelect, speedBasedTurn, speedOrder, speedNumOrder
    global originalEnergy, skillParty, skillUsed, itemParty, itemUsed, itemNum, actParty, actUsed, actionDia, actionNum, attackFade, barSelect, fightUsed, hudScroll
    global fightFrame, stupidFightloop, sprite, allyTween, enemyTween, fightyLoop, battleSplash, backGroundNum, stuff, useDebug, useCustomBattle, selectedBuff, buffScroll

    global onStart, onUpdate, actCall, frame, onEnd, useMobile, allowGameOver, allowWin, useAnim
    def onUpdate():
        pass
    def onStart():
        pass
    def onEnd():
        pass
    frame = 0
    actions = [character.check, character.defend, character.swap, character.heal, character.level_up, character.overcharge, character.talk, character.spare]
    if usingDebug:
        for i in Players+Enemies:
            i.action = actions
    else:
        actions = [character.check, character.defend, character.swap, character.heal, character.level_up, character.talk, character.spare]
        for i in Players+Enemies:
            i.action = actions
    attacking.clear()
    energy = energyTrans = energyGain = 0
    intenseX = [0, 0]
    intenseMode = False
    projectilePattern.clear()
    character.effectStuff.clear()
    playerShakePos.clear()
    enemyShakePos.clear()
    allowGameOver = True
    allowWin = True
    opponentBot = not screenWindow.trigger['Multiplayer'].boolean
    #allyHudX = -1000
    enemyHudX = width
    oldCycle.clear()
    newCycle.clear()
    useDebug = usingDebug
    effectStuff = character.effectStuff
    botplay = screenWindow.trigger['Botplay'].boolean#screenWindow.controlVar[0][1]
    hardMode = screenWindow.trigger['Hard Mode'].boolean
    useMobile = screenWindow.trigger['Use Mobile'].boolean
    easyMode = screenWindow.trigger['Easy Mode'].boolean
    useExtraDialogue = screenWindow.trigger['Extra Dialogue'].boolean
    enemyAutoAttack = screenWindow.trigger['RNG Attacks'].boolean
    instantAttack = screenWindow.trigger['Fast Fight Load'].boolean
    useAnim = screenWindow.trigger['Use Animation'].boolean
    if hardMode:
        inventory = copy.copy(character.inventory)
        for i in Enemies:
            i.level += 1
            i.levelUp(0)
            i.inventory = inventory


    dafps = 30
    stuff = random.randint(0, 10)
    stuff = 5
    backGroundNum = 14#random.randint(0, 15)
    character.party = party = Players
    useHitChance = True
    character.opponent = opponent = Enemies
    fightyLoop.clear()
    energyLoop.clear()
    newCycle.clear()
    oldCycle.clear()
    tutorial = False
    inBattle = True
    allyTween = []
    enemyTween = []
    attackFrame = []
    fightBar = []
    barIsAttacking = []
    fightingBar = {}
    fightBarX = []
    fightBarX2 = []
    fightScale = []
    barAlpha = []
    allyStrike = []
    allyDamage = []
    allyAttack = []
    opponentSmoothDamage = []
    enemyShakeX = []
    enemyShakeBool = []
    inBar = 0
    fightFrame = 0
    attackFade = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    inFight = False
    barSelect = 0
    damageX = []
    damageY = []
    damageY2 = []
    fightUsed = []

    enemyStrike = []
    enemyDamage = []
    enemyAttack = []
    enemySmoothDamage = []
    enemyShakeX = []
    enemyShakeBool = []
    inBar = 0
    fightFrame = 0
    attackFade = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    inFight = False
    barSelect = 0
    damageX = []
    damageY = []
    damageY2 = []

    meleeDone = False
    throwerDone = False
    rangeDone = False
    tankDone = False
    controllerDone = False
    supportDone = False
    underDone = False
    slamDone = False
    backDone = False
    holdDone = False

    meleeUsed = False
    throwerUsed = False
    rangeUsed = False
    tankUsed = False
    controllerUsed = False
    supportUsed = False
    underUsed = False
    slamUsed = False
    backUsed = False
    holdUsed = False

    useCustomDialogue = False
    turnDialogue.clear()
    turnDialogue = [[[None, None, None], ['Get ready to rumble.'], False, 0, [None], set([])]]
    turn = 1
    cycle = 1

    splashy = ''
    text_index = 0
    stuff = 5
    speedBasedTurn = useSpeedTurn
    if battleData != None:
        useCustomBattle = True
        with open(f'data/battle/{battleData}.py', 'r') as f:
            exec(f.read(), globals(), globals())
        onStart()
        character.actCall = actCall

    for i in opponent:
        newCycle[i] = 0
        oldCycle[i] = 0
    for i in party:
        newCycle[i] = 0
        oldCycle[i] = 0
    speedNum = 0
    speedOrder = []
    speedNumOrder = -1
    for num, i in enumerate(party):
        i.levelUp(0)
        speedOrder.append([i.speed, num, 'Player', i.name])

    for num, i in enumerate(opponent):
        i.levelUp(0)
        speedOrder.append([i.speed, num, 'Enemy', i.name])

    organise = False
    while not organise:
        organise = True
        for num, i in enumerate(speedOrder):
            if num + 1 < len(speedOrder):
                if i[0] > speedOrder[(num + 1)][0]:
                    speedOrder[num], speedOrder[num + 1] = speedOrder[num + 1], speedOrder[num]

                    organise = False
    speedOrder.reverse()
    if speedBasedTurn:
        turn = 1
    #for i in speedOrder:
        #print(i[0], i[3])
    #for i in party + opponent:
        #i.hp = i.maxhp

        #addTurnDialogue(None, "Rekety and Rany gained the Talk action!", 8)

    playerShakeX.clear()
    playerShakeBool.clear()
    enemyShakeX.clear()
    enemyShakeBool.clear()
    dialogueText.clear()

    for i in party:
        allyTween.append(0)
        allySelection.append(0)
        itemHeal.append(0)
        allyAction.append(None)
        whichAction.append(0)
        allyStrike.append(False)
        skillUsed.append(0)
        itemNum.append(0)
        playerShakeX.append(0)
        playerShakeBool.append(False)
        #print(i.name, i.xp)

    for i in opponent:
        enemyTween.append(0)
        enemySelection.append(0)
        itemHeal.append(0)
        enemyAction.append(None)
        whichAction.append(0)
        enemyStrike.append(False)
        skillUsed.append(0)
        itemNum.append(0)
        enemyShakeX.append(0)
        enemyShakeBool.append(False)
        i.levelUp(0)

    #stuff = 3
    if not screenWindow.useWeb:
        music = DynamicMusicPlayer(f"sounds/music/{stuff}.ogg", loop=True)
    else:
        #pygame.mixer.music.load(f'sounds/music/{stuff}.ogg')
        #pygame.mixer.music.play(loops=-1)
        if sys.platform == "emscripten":
            audio.src = 'music/{stuff}.mp3'
        else:
            playSound(f'music/{stuff}.ogg', 1, True)
    playerAlpha = []
    enemyAlpha = []
    playerSprite.clear()
    enemySprite.clear()
    playerFloat = []
    enemyFloat = []
    enemyTween = []
    for i in party:
        playerAnimList.append(playerAnim.copy())
        playerSprite.append(0)
        playerFloat.append(0)
        playerShakePos.append(())
    opponentHp = []
    opponentAlpha = []
    opponentCoords.clear()
    playerCoords.clear()
    for i in opponent:
        enemyTween.append(0)
        opponentCoords.append([])
        i.levelUp(0)
        i.hpSet()
        enemySprite.append(0)
        enemyFloat.append(0)
        enemyAlpha.append(0)
        enemyShakePos.append(())

    for i in party:
        playerCoords.append([])
        playerAlpha.append(255)
    for num, enemies in enumerate(opponent):
        opponentHp.append(enemies.hp)
        opponentAlpha.append(255)
        if firstPerson:
            x = 1000*((width/2)/500) + 500*((width/2)/500)/len(opponent)# + 400*(width/1000)/len(opponent) * num
        else:
            x = 600*((width/2)/500) + 200*((width/2)/500)/len(opponent) + 400*(width/1000)/len(opponent) * num
        y = 200 + 3*num - 3*len(opponent)
        opponentCoords[num] = [x, y]

    for num, players in enumerate(party):
        if firstPerson:
            x = -200
        else:
            x = 200*((width/2)/500)/len(party) + 400*(width/1000)/len(party) * num
        y = 200 + 3*num - 3*len(party)
        playerCoords[num] = [x, y]

    colorOfAlly = []
    colorOfEnemy = []
    for i in party:
        i.levelUp(0)
        colorOfAlly.append(i.color)
        i.hpSet()

    for i in opponent:
        colorOfEnemy.append(i.color)
    resetAllyTurn()
    turn = 1
    #for i in Enemies:
        #print(id(i), i.name)
        #onUpdate()
    #for i in opponent:
        ##print(i.name, i.name)


    #asyncio.run(battleRun())

confirm = False
cancel = False
rightPressed = False
leftPressed = False
upPressed = False
downPressed = False
special = False
useDebug = False
useCustomBattle = False
skipDialogue = False
mouseTouch, mouseHover = screenWindow.mouseTouch, screenWindow.mouseHover
actions = []
progressTurn = True
firstPerson = False
win = gameOver = False
selectedBuff = 0
buffScroll = 0

intenseMode = False
useMobile = False
freeRange = character.freeRange
allowGameOver = True
allowWin = True
async def battleRun():
    global inBattle, frame, time, cycling, fullscreen, dafps, battleStart, turnAlly, turnEnemy, allyTurn, enemyTurn, botplay, color, battleSplash, bossFight, backgroundNum, useExtraDialogue
    global selectedAlly, selectedEnemy, allySelection, enemySelection, allyAction, enemyAction, floaty, energy, energyGain, energyTrans, allyTween, enemyTween
    global movingHud, tempAlly, actions, text_index, splashy, inFight, inSkill, inAct, inItem, speedNum, actionWhich, theAlly, theOpponent, whichSelection, selectedWhich
    global meleeDone, rangeDone, throwerDone, tankDone, controllerDone, supportDone, underDone, slamDone, backDone, holdDone
    global meleeFound, rangeFound, throwerFound, tankFound, controllerFound, supportFound, underFound, slamFound, backFound, holdFound
    global meleeUsed, rangeUsed, throwerUsed, tankUsed, controllerUsed, supportUsed, underUsed, slamUsed, backUsed, holdUsed, commandText
    global meleeParticipants, rangeParticipants, throwerParticipants, tankParticipants, controllerParticipants, supportParticipants, underUsed, slamParticipants, backParticipants, holdParticipants
    global attack_rect, inBar, effectiveRange, attackMeterX, hud, screen, baseTextBoxHeight, textBox, hudRect, theDelta, deadCount, mouseHold, mouseDown, MUSICSTART, commandMode
    global party, scaleFactor, buffMenu, buff_tweenY, deltaTime, text_index, inBar, beat, enemyHudX, allyHudX

    global turn, cycle, newCycle, oldCycle, theAlly, theOpponent, coords, whichTurn, oriCoords, attacking, backUpCoords, hudTween, swap, swapFinally, original
    global centerX, centerY, hudLength, hudHeight, hudX, hudY, thickness
    global transition, playerAlpha, colorOfAlly, colorOfEnemy, selectedAction, multiSelect, speedBasedTurn, speedOrder, speedNumOrder
    global originalEnergy, skillParty, skillUsed, itemParty, itemUsed, itemNum, actParty, actUsed, actionDia, actionNum, attackFade, barSelect, fightUsed, hudScroll
    global fightFrame, stupidFightloop, sprite, allyTween, enemyTween, fightyLoop, battleSplash
    global confirm, leftPressed, rightPressed, cancel, useDebug, progressTurn, skipDialogue, win, gameOver, selectedBuff, buffScroll, intenseMode, music

    winX = winY = 0
    selectedAction = 0
    if useDebug:
        actions = ['Fight', 'Skills', 'Act', 'Items', 'Debug']
    else:
        actions = ['Fight', 'Skills', 'Act', 'Items']
    #dafps = 60
    while inBattle:
        #inBar = len(fightBar)
        await asyncio.sleep(0)
        if firstPerson:
            for i in party:
                i.setNum[4] = 99
                i.newNum[4] = 99
        playBack = 30 * 1/max(25, min(60, (dafps)))
        clock.tick(30)
        #dafps = 60
        screenWindow.deltaTime = 2/dafps
        theDelta = 30 * 1/dafps
        frame += 1
        time += 0.02
        cycling += 1
        confirm = False
        cancel = False
        rightPressed = False
        leftPressed = False
        upPressed = False
        downPressed = False
        special = False
        #if frame%3:
            #party[0].dataName = random.choice(character.validAlly).name
        #party[0].name = random.choice(character.validAlly).name
        if turn == 8:
            if character.talk not in party[0].action:
                party[0].action.append(character.talk)

        for event in pygame.event.get(): # For every event
            if event.type == pygame.QUIT: # If the event is quit, basically pressing the X at the top right of the window
                inBattle = False # Quit the game without SAVING!
            elif event.type == pygame.KEYDOWN: # If the event involved a key on the keyboard being pressed once
                if not commandMode:
                    if event.key == pygame.K_F4:
                        fullscreen = not fullscreen
                        fullscreen = fullscreen
                        if fullscreen:
                            #screen = pygame.transform.rotate(screen, allyTween[2]/6)
                            screenWindow.changeSize(0, 0, fullscreen)

                        else:
                            screenWindow.changeSize(1000, 700, fullscreen)


                    if event.key == screenWindow.keyBind['Confirm']:
                        confirm = True
                    elif event.key == screenWindow.keyBind['Cancel']:
                        cancel = True
                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        special = True
                    elif event.key == pygame.K_1:
                        #for num, i in enumerate(opponentHp):
                        dafps += 10
                    #scaleFactor += 0.1
                    elif event.key == pygame.K_2:
                        for num, i in enumerate(party):
                            fightyLoop.append([party[num], party[0], 100])
                        playSound('fail.wav')
                        camSet(1, RED, 255, 7)
                    elif event.key == pygame.K_3:
                        for i in opponent:
                            fightyLoop.append([i, party[0], -10])
                    elif event.key == pygame.K_4:
                        actionWhich[selectedWhich] = 'Done'
                        resetAllyTurn()
                    elif event.key == pygame.K_5:
                        for num, i in enumerate(party):
                            fightyLoop.append([party[num], party[num], -100])
                    elif event.key == pygame.K_6:
                        energyGain += 999
                        for num, i in enumerate(party):
                            energyLoop.append([party[num], party[0], -100])
                    elif event.key == pygame.K_7:
                        for i in party:
                            i.level += 1
                            i.levelUp(0)
                    elif event.key == pygame.K_8:
                        for i in party:
                            i.level -= 1
                            i.levelUp(0)
                    elif event.key == pygame.K_9:
                         for i in opponent:
                            fightyLoop.append([i, party[0], 100])
                    elif event.key == pygame.K_0:
                        commandMode = True
                    elif event.key == pygame.K_RIGHT:
                        rightPressed = True
                    elif event.key == pygame.K_LEFT:
                        leftPressed = True
                    elif event.key == pygame.K_UP:
                        upPressed = True
                    elif event.key == pygame.K_DOWN:
                        downPressed = True
                elif commandMode:
                    if event.key == pygame.K_BACKSPACE: # If the key pressed is backspace
                        commandText = commandText[:-1] # Remove the last character from the user's input
                    elif event.key == pygame.K_RETURN:
                        confirm = True
                    elif event.key == pygame.K_BACKSPACE:
                        cancel = True
                    else: # If the key pressed is not backspace
                        commandText += event.unicode

        #if frame == 90:
            #destroyAction()

        battleStart -= battleStart/7 * theDelta
        if battleStart < 0.001:
            battleStart = 0

        if pygame.key.get_pressed()[pygame.K_SPACE] == True and frame%3 == 0:
            skipDialogue = True
        else:
            skipDialogue = False
        charList = [character.blue_guy, character.purple_kid, character.red_dude]
        #if frame%0 == 0:
            #party[0] = charList[(frame//10)%3]

        pygame.mixer.music.set_volume(screenWindow.musicVolume) # Set the music volume
        if party[0].name == 'Zee':
            actions = ['Fight', 'Items', 'Fight']
        #hud.camera_rotation = 0.5*math.sin(frame/30)
        #backGroundScreen.camera_rotation = 1*math.sin(-frame/15)
        #screen.camera_rotation = 1*math.sin(-frame/15)

        screenStuff()
        fps = clock.get_fps()
        fps_text = render_text(f"FPS: {int(fps)}/30", WHITE, 30, True, BLACK, 2)
        blitObj(screen, fps_text, 10, 10, pivot_type='topleft')
        #blitObj(screen, fps_text, 10, 10, pivot_type='topleft')
        if frame<=1:
            continue

        #winY -= winY/7 * theDelta
        #winX -= winX/7 * theDelta

        #window.window.position = (desktopX/2-1000*scaleFactor/2+winX, desktopY/2-700*scaleFactor/2+winY)

        #music.update()
        if not screenWindow.useWeb:
            if music.cur_beat != beat and 1==0:
                #screen.start_rotation(10 if beat%2 == 0 else -10, 1)
                #screen.camera_rotation = 10 if beat%2 == 0 else -10#1*math.sin(-frame/15)
                beat = music.cur_beat
                if beat%2 == 0:
                    winY = 10
                    winX = -10 if beat%4 == 0 else 10
                #window.window.position = #(10 if beat%2 == 0 else -10, 90)

        #for num, i in enumerate(allyAction):
         #   text = render_text(str(i), WHITE, 40, True, BLACK, 4)
          #  blitObj(hud, text, width/2, 400+num*40)
        MUSICSTART = True

        if MUSICSTART and not commandMode:
            battleAlly()
            if not opponentBot:
                battleEnemy()
        mouseHover()
        if useMobile:
            leftArrow = loadSprite('left', f'controls/left.png', (100, 500), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
            rightArrow = loadSprite('right', f'controls/right.png', (260, 500), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
            downArrow = loadSprite('down', f'controls/down.png', (180, 580), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
            upArrow = loadSprite('up', f'controls/up.png', (180, 420), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
            confirmButton = loadSprite('confirm', f'controls/confirm.png', (820, 380), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
            cancelButton = loadSprite('cancel', f'controls/cancel.png', (820, 480), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
            specialButton = loadSprite('special', f'controls/special.png', (820, 580), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
            resetMusic = loadSprite('setting', f'controls/special.png', (920, 480), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud, color=PURPLE)
            if mouseTouch(resetMusic, True, True):
                pygame.mixer.music.play(loops=-1)


            if mouseTouch(leftArrow, True, True):
                leftPressed = True
            if mouseTouch(rightArrow, True, True):
                rightPressed = True
            if mouseTouch(upArrow, True, True):
                upPressed = True
            if mouseTouch(downArrow, True, True):
                downPressed = True
            if mouseTouch(confirmButton, True, True):
                confirm = True
            if mouseTouch(specialButton, True, True):
                special = True
            if mouseTouch(cancelButton, True, True):
                cancel = True

        buff_tweenY -= (buff_tweenY/5 if buffMenu else - buff_tweenY/5)*theDelta
        buff_tweenY = max(10, min(buff_tweenY, 700))
        if buff_tweenY < 700:
            #drawRect(hud, (150, 150, 150), 45, 45 , width - 90, height - 90)
            #drawRect(hud, (200, 200, 200), 50, 50, width - 100, height - 100)
            statList = ['health', 'level', 'mana', 'attack', 'defense', 'speed', 'productivity', 'range']
            colorList = [GREEN, GRAY, CYAN, RED, BLUE, YELLOW, PURPLE, ORANGE]
            shortStat = {'level':'LVL', 'health':'HP', 'attack':'ATK', 'defense':'DEF', 'speed':'SPD', 'productivity':'PRD', 'range':'RGE', 'mana':'MP'}
            allyThing = party if opponentBot else theAlly
            #for num, ally in enumerate(party[:1]):
            if leftPressed:
                selectedBuff -= 1
                if selectedBuff < 0:
                    selectedBuff = len(allyThing) - 1
                playSound('Select_sfx.ogg', 0.9)
                buffScroll = 0
            if rightPressed:
                selectedBuff += 1
                if selectedBuff >= len(allyThing):
                    selectedBuff = 0
                playSound('Select_sfx.ogg', 0.9)
                buffScroll = 0

            if upPressed:
                buffScroll -= 120
                if buffScroll <= 0:
                    buffScroll = 0
                playSound('Select_sfx.ogg', 0.9)

            if downPressed:
                buffScroll += 120
                playSound('Select_sfx.ogg', 0.9)
            #print(buffScroll, 120*((len(players.buff) + len(players.passiveBuff) )//2))
            #print("current:" + str(buffScroll))
            
            num = 0
            ally = allyThing[selectedBuff]
            buffScroll = min(buffScroll, 120*((len(ally.buff) + len(ally.passiveBuff) - 1)//2) )
            playerStat = {'level':ally.level, 'health':ally.maxhp, 'attack':ally.attack, 'defense':ally.defense, 'speed':ally.speed, 'productivity':ally.productivity, 'range':ally.range, 'mana':round(ally.mana)}
            x = 55
            y = 100 + 205*num + buff_tweenY
            statWidth = width-45*2#+10
            statHeight = 210
            drawRect(hud, ally.color, x-10, y+statHeight-40, statWidth, height-(y+statHeight)-(y-50+5)+40)
            drawRect(hud, (0, 0, 0), x, y+statHeight-10, statWidth-20, height-(y+statHeight)-(y-50+5))
            surface = loadSurface(statWidth-20, height-(y+statHeight)-(y-50+5))
            numBuff = -1
            for numBuff, (buff, effects) in enumerate(ally.passiveBuff.items()):
                buffX = 20 + (numBuff%2)*statWidth/2#hpX + numBuff * 40 + 45 if len(ally.buff.items()) <= 4 else hpX + 45 + numBuff * (hpWidth - 40 + 5) / (len(ally.buff.items()) - 1)
                buffY = 20+ 120*(numBuff//2) - buffScroll
                coloing = buff.color
                dark = (coloing[0] * 0.7, coloing[1] * 0.7, coloing[2] * 0.7)
                outline = (180, 70, 70) if "Debuff" in buff.type else (70, 255, 70)

                drawRect(surface, outline, (buffX - 4, buffY - 4, 90, 90))
                drawRect(surface, dark, (buffX, buffY, 82, 82))
                drawRect(surface, coloing, (buffX + 7, buffY + 7, 68, 68))

                stuff = render_text(f"{buff.name}", WHITE, 50, True, BLACK, 2)
                blitObj(surface, stuff, buffX + 100, buffY - 4, pivot_type='topleft')

                if effects[0] == True and effects[1] == False:
                    stuff = render_text(f"Active", GREEN, 50, True, BLACK, 2)
                else:
                    stuff = render_text(f"Not Active", RED, 50, True, BLACK, 2)
                blitObj(surface, stuff, buffX + 100, buffY + 97, pivot_type='bottomleft')

                stage = render_text("P", WHITE, 50, True, BLACK, 3)
                blitObj(surface, stage, buffX - 4 , buffY + 97, pivot_type='bottomleft')

            addedNum = numBuff + 1


            for numBuff, (buff, effects) in enumerate(ally.buff.items()):
                numBuff += addedNum
                buffX = 20 + (numBuff%2)*statWidth/2#hpX + numBuff * 40 + 45 if len(ally.buff.items()) <= 4 else hpX + 45 + numBuff * (hpWidth - 40 + 5) / (len(ally.buff.items()) - 1)
                buffY = 20+ 120*(numBuff//2) - buffScroll
                coloing = buff.color
                dark = (coloing[0] * 0.7, coloing[1] * 0.7, coloing[2] * 0.7)
                outline = (180, 70, 70) if "Debuff" in buff.type else (70, 255, 70)

                drawRect(surface, outline, (buffX - 4, buffY - 4, 90, 90))
                drawRect(surface, dark, (buffX, buffY, 82, 82))
                drawRect(surface, coloing, (buffX + 7, buffY + 7, 68, 68))

                stuff = render_text(f"{buff.name}", WHITE, 50, True, BLACK, 2)
                blitObj(surface, stuff, buffX + 100, buffY - 4, pivot_type='topleft')

                if effects[0] == float('inf'):
                    text = "∞"
                else:
                    text = effects[0]

                stuff = render_text(f"Cycles: {text} | Turns: {effects[3]}", WHITE, 50, True, BLACK, 2)
                blitObj(surface, stuff, buffX + 100, buffY + 97, pivot_type='bottomleft')

                stage = render_text(romanInt(effects[2]), WHITE, 50, True, BLACK, 3)
                blitObj(surface, stage, buffX - 4 , buffY + 97, pivot_type='bottomleft')
            blitObj(hud, surface, x, y+statHeight-10, pivot_type='topleft')

            drawRect(hud, ally.color, width/2-200, y-50 , 400, 100)
            drawRect(hud, (0.73*ally.color[0], 0.73*ally.color[1], 0.73*ally.color[2]), width/2-170+5, y-50+5 , 340-10, 100-10)
            nameText = render_text(f"<< {ally.name} >>", WHITE, 40, True, BLACK, 2)

            blitObj(hud, nameText, width/2, y-25)
            drawRect(hud, ally.color, x-10, y-10 , statWidth, statHeight)
            drawRect(hud, (0.73*ally.color[0], 0.73*ally.color[1], 0.73*ally.color[2]), x-5, y-5, statWidth-10, statHeight-10)
            iconImg = loadImg((f'selectionIcon/{ally.displayName}.png', 0.75))
            blitObj(hud, iconImg, x, y, pivot_type='topleft')
            for statNum, stat in enumerate(statList):
                statX = x + 200 + 170*(statNum//2)
                statY = y + 15 + (statNum%2)*85
                drawRect(hud, (0.68*colorList[statNum][0], 0.68*colorList[statNum][1], 0.68*colorList[statNum][2]), statX, statY, 160, 40)
                drawRect(hud, colorList[statNum], statX+3, statY+3, 160-6, 40-6)
                statImg = loadImg((f'stats/{stat}.png', 0.75))
                blitObj(hud, statImg, statX, statY, pivot_type='topleft')
                statText = render_text(str(playerStat[stat]), WHITE, 40, True, BLACK, 2)
                blitObj(hud, statText, statX+160/2+75/2, statY+40/2)
                shortText = render_text(str(shortStat[stat]), WHITE, 36, True, BLACK, 2)
                blitObj(hud, shortText, statX+75/2, statY)


        for i in achievementObj.values():
            i.update()
        draw(hud)
        screenBlit(screen)

        hud.fill((0, 0, 0, 0))
        #screen.fill(GRAY)
       # backGroundScreen.fill((120, 120, 180, 180))
        if 1==1:
            if turnAlly:
                backGroundScreen.fill((120, 120, 180, 255)) # Fill the screen with WHITE
                drawRect(backGroundScreen, (100, 100, 160), (0, 400, width, 30))
                drawRect(backGroundScreen, (100, 100, 160), 0, 400, (width/2 - 1000/2), height-400)
                drawRect(backGroundScreen, (100, 100, 160), (width/2 + 1000/2), 400, (width/2 - 1000/2), height-400)
            else:
                backGroundScreen.fill((180, 120, 120, 255))
                drawRect(backGroundScreen, (160, 100, 100), (0, 400, width, 30))
                drawRect(backGroundScreen, (160, 100, 100), 0, 400, (width/2 - 1000/2), height-400)
                drawRect(backGroundScreen, (160, 100, 100), (width/2 + 1000/2), 400, (width/2 - 1000/2), height-400)
        #background = loadImg(('backgrounds/' + str(backgroundNum) + '.png'))
        background = loadImg(('backgrounds/14.png'))
        backgroundRect = background.get_rect(center=(width/2, -300))
        for i in range(0, 6):
            x = i*(width/2 - 1000/2)/5
            theWidth = (width/2 - 1000/2)/5
            theHeight = 400
            drawRect(backGroundScreen, (255-i*20, 255-i*20, 255-i*20), x, 0, theWidth, theHeight)
        for i in range(0, 6):
            x = width - (i+1)*(width/2 - 1000/2)/5
            theWidth = (width/2 - 1000/2)/5
            theHeight = 400
            drawRect(backGroundScreen, (255-i*20, 255-i*20, 255-i*20), x, 0, theWidth, theHeight)

        blitObj(backGroundScreen, background, width/2, 50, 'center')
        if opponent[0].name == 'The Creator' and 1==0:
            backGroundScreen.fill((0, 0, 0, 255))
            backGroundScreen.camera_rotation = 3*math.sin(frame/20)
            backGroundScreen.camera_zoom = (abs(math.cos(frame/10))+1.5)
            for i in range(0, 11):
                drawRect(backGroundScreen.surface, (min(i*10, 255), min(i*10, 255), min(i*10, 255)) ,(0, 0+i*40+20*math.sin(frame/20+i), width, height-i*80+10*math.cos(frame/20+i)))
            #for i in range(0, 11):
                #drawRect(hud.surface, (0, 0, min(i*10, 255), 150) ,(0, 0+i*40+20*math.cos(frame/20+i), width, height-i*80+10*math.sin(frame/20+i)))
        screen.fill((0, 0, 0, 0))
        #blitObj(screen, backGroundScreen, 0, 0, 'center')
        #pygame.draw.rect(
        mouse_pos = pygame.mouse.get_pos() # Get the mouse position
        mouse_buttons = pygame.mouse.get_pressed() # Get the mouse buttons
        # Super funni thing to make mouse input work properly :]
        if any(mouse_buttons): # If any of the mouse buttons are pressed
            if mouseHold: # If the mouse button are held down
                mouseDown = False # Automatically stop the input of 'mouse being clicked once' to the game
            else: # If the mouse button are not held down, though his means that in the first frame after bthe mouse was clicked
                mouseDown, mouseHold = True, True # Sends to the game an input of the mouse having been clicked once and also sends an input that the mouse is also currently being held down for later frames
        else: # If no mouse buttons are pressed
            mouseHold, mouseDown = False, False
        if battleStart != 0 and 1==0:
            drawRect(hud, RED, 0, 0, 250, 700)
            drawRect(hud, YELLOW, 250, 0, 250, 700)
            drawRect(hud, GREEN, 500, 0, 250, 700)
            drawRect(hud, BLUE, 750, 0, 250, 700)
            drawRect(hud, CYAN, 0, 500, 1000, 200)
            leftClick = render_text('LEFT CLICK', WHITE, 50, True, BLACK, 3)
            canceled = render_text('CANCEL', WHITE, 50, True, BLACK, 3)
            confirmed = render_text('CONFIRM', WHITE, 50, True, BLACK, 3)
            rightClick = render_text('RIGHT CLICK', WHITE, 50, True, BLACK, 3)
            specialClick = render_text('SPECIAL', WHITE, 50, True, BLACK, 3)
            blitObj(hud, leftClick, 125, 250)
            blitObj(hud, canceled, 375, 250)
            blitObj(hud, confirmed, 625, 250)
            blitObj(hud, rightClick, 875, 250)
            blitObj(hud, specialClick, 500, 550)
        if 1==0 and MUSICSTART:
            drawRect(screen, RED, 0, 0, 250, 500, border=5)
            drawRect(screen, YELLOW, 250, 0, 250, 500, border=5)
            drawRect(screen, GREEN, 500, 0, 250, 500, border=5)
            drawRect(screen, BLUE, 750, 0, 250, 500, border=5)
            drawRect(screen, CYAN, 0, 500, 1000, 200, border=5)
        if mouseDown and 1==0:
            battleStart = 0
            if not MUSICSTART:
                MUSICSTART = True
        if battleStart == 0 and 1==0:
            MUSICSTART = True
        if MUSICSTART != True:
            continue
        resetSpeed = False
        for num, ally in enumerate(party):
            if ally not in oldCycle:
                newCycle[ally] = 0
                oldCycle[ally] = 0
            colorOfAlly[num] = ally.color
            if num >= len(allyAction):
                #print(allyAction)
                resetSpeed = True
                allyTween.append(0)
                allySelection.append(0)
                allyDamage.append(0)
                itemHeal.append(0)
                allyAction.append(None)
                whichAction.append(0)
                allyStrike.append(False)
                skillUsed.append(0)
                itemNum.append(0)
                playerShakeX.append(0)
                playerShakeBool.append(False)
                playerCoords.append([-400, 200])
                playerAlpha.append(255)
                playerSprite.append(0)
                playerFloat.append(0)
                playerShakePos.append(())

        for num, enemy in enumerate(opponent):
            if enemy not in oldCycle:
                newCycle[enemy] = 0
                oldCycle[enemy] = 0
            if num >= len(enemyAction):
                resetSpeed = True
                colorOfEnemy.append(enemy.color)
                enemyTween.append(0)
                enemySelection.append(0)
                enemyDamage.append(0)
                allyDamage.append(0)
                itemHeal.append(0)
                enemyAction.append(None)
                whichAction.append(0)
                enemyStrike.append(False)
                skillUsed.append(0)
                itemNum.append(0)
                enemyShakeX.append(0)
                enemyShakeBool.append(False)
                opponentCoords.append([width+400, 200])
                opponentAlpha.append(255)
                enemySprite.append(0)
                enemyFloat.append(0)
                enemyShakePos.append(())
            colorOfEnemy[num] = enemy.color
        if resetSpeed:
            speedReset()

        # Super funni thing to make mouse input work properly :]
        if any(mouse_buttons): # If any of the mouse buttons are pressed
            if screenWindow.mouseHold: # If the mouse button are held down
                screenWindow.mouseDown = False # Automatically stop the input of 'mouse being clicked once' to the game
            else: # If the mouse button are not held down, though his means that in the first frame after bthe mouse was clicked
                screenWindow.mouseDown, screenWindow.mouseHold = True, True # Sends to the game an input of the mouse having been clicked once and also sends an input that the mouse is also currently being held down for later frames
        else: # If no mouse buttons are pressed
            screenWindow.mouseHold, screenWindow.mouseDown = False, False # Automatically stop the input of 'mouse being clicked once' and 'mouse held down continuously' to the game

        if mouse_pos[1] <= 500*scaleFactor and 1==0:
            if 0 <= mouse_pos[0] <= 250*scaleFactor:
                if mouseDown:
                    leftPressed = True
                if mouseHold:
                    drawRect(screen, (255, 200, 200), 0, 0, 250, 500, border=5)
            if 250*scaleFactor <= mouse_pos[0] <= 500*scaleFactor:
                if mouseDown:
                    cancel = True
                if mouseHold:
                    drawRect(screen, (255, 255, 200), 250, 0, 250, 500, border=5)
            if 500*scaleFactor <= mouse_pos[0] <= 750*scaleFactor:
                if mouseDown:
                    confirm = True
                if mouseHold:
                    drawRect(screen, (200, 255, 200), 500, 0, 250, 500, border=5)
            if 750*scaleFactor <= mouse_pos[0] <= 1000*scaleFactor:
                if mouseDown:
                    rightPressed = True
                if mouseHold:
                    drawRect(screen, (200, 200, 255), 750, 0, 250, 500, border=5)
        elif 1==0:
            if mouseDown:
                special = True
            if mouseHold:
                drawRect(screen, (200, 255, 255), 0, 500, 1000, 200, border=5)

        if commandMode:
            drawRect(hud, WHITE, 45, height - 255 , width - 90, 60)
            drawRect(hud, BLACK, 50, height - 250, width - 100, 50)
            terminalText = render_text("Command Terminal...", BLACK, 50, True, WHITE, 2)
            blitObj(hud, terminalText, 45, height - 300, pivot_type='topleft')
            commandRender = render_text(commandText, WHITE, 50)
            blitObj(hud, commandRender, 52, height - 248, pivot_type='topleft')
            if cancel:
                commandMode = False
                commandText = ''
            if confirm:
                commandMode = False
                exec(commandText)
                commandText = ''
            continue

        if special:
            buffMenu = not buffMenu
            buffScroll = 0
        if debug:
            huddy = loadImg(('hud.png', (1.3, 1.7)))
            hud_rect = huddy.get_rect(center=(500, 300))
            screen.blit(huddy, hud_rect)
            inPage = whichPage[debugList[debugSelect]]
            if confirm:
                if debugSelect == 0:
                    botplay = not botplay#not botplay

                elif debugSelect == 2:
                    wavey = not wavey
                else:
                    whichPage[debugList[debugSelect]] = True

            if cancel:
                whichPage[debugList[debugSelect]] = False

            if upPressed:
                if not inPage:
                    debugSelect -= 1
                    if debugSelect < 0:
                        debugSelect = len(debugList) - 1
                elif inPage:
                    if debugSelect == 1:
                        heighty -= 1

            if downPressed:
                if not inPage:
                    debugSelect += 1
                    if debugSelect > len(debugList) - 1:
                        debugSelect = 0
                elif inPage:
                    if debugSelect == 1:
                        heighty += 1

            if leftPressed:
                if debugSelect == 1 and inPage:
                    widthy -= 1

            if rightPressed:
                if debugSelect == 1 and inPage:
                    widthy += 1



            for num, i in enumerate(debugList):
                x = 500
                y = 200 + 50*num
                if num == 0:
                    addInfo = ': ' + str(botplay)
                elif num == 1:
                    addInfo = ': ' + str(window.get_size())
                elif num == 2:
                    addInfo = ': ' + str(wavey)
                else:
                    addInfo = ''
                debugText = render_text(i + addInfo, YELLOW if debugSelect == num else WHITE, 40)
                debugRect = debugText.get_rect(center=(x, y))
                screen.blit(debugText, debugRect)
            continue
        turnPlayText = render_text(f'TURN {str(turn)}', WHITE, 50, True, BLACK, 3)
        blitObj(hud, turnPlayText, width/2, 150)
        cyclePlayText = render_text(f'CYCLE {str(cycle)}', WHITE, 50, True, BLACK, 3)
        blitObj(hud, cyclePlayText, width/2, 100)

        if botplay:
            botPlay()
            botPlayText = render_text('BOTPLAY', WHITE, 50, True, BLACK, 3)
            blitObj(hud, botPlayText, width/2, 200)

        if inBattle:
            for num, ally in enumerate(party):
                if intenseMode and ally.hp <= 0:
                    continue
                if (turnAlly or intenseMode) or opponentBot:
                    allyHudX += (0 - allyHudX)/10
                if num == selectedAlly and allyTurn:
                    allyTween[num] += 4 if allyTween[num] < 20 else 0
                    if allyTween[num] < -20:
                        allyTween[num] += 50

                elif not turnEnemy:
                    if -4 <= allyTween[num] <= 4:
                        allyTween[num] = 0
                    elif allyTween[num] < -20:
                        allyTween[num] += 50
                    elif allyTween[num] < 0:
                        allyTween[num] += 4
                    elif allyTween[num] > 0:
                        allyTween[num] -= 4
                    else:
                        pass
                elif turnEnemy and not opponentBot and not intenseMode:
                        allyHudX += (-1100 - allyHudX)/10

            if not opponentBot:
                for num, ally in enumerate(opponent):
                    if turnEnemy or intenseMode:
                        enemyHudX += (0 - enemyHudX)/10
                    if num == selectedEnemy and enemyTurn:
                        enemyTween[num] += 4 if enemyTween[num] < 20 else 0
                        if enemyTween[num] < -20:
                            enemyTween[num] += 50

                    elif not turnAlly:
                        if -4 <= enemyTween[num] <= 4:
                            enemyTween[num] = 0
                        elif enemyTween[num] < -20:
                            enemyTween[num] += 50
                        elif enemyTween[num] < 0:
                            enemyTween[num] += 4
                        elif enemyTween[num] > 0:
                            enemyTween[num] -= 4
                        else:
                            pass


                    elif turnAlly and not opponentBot and not intenseMode:
                        enemyHudX += (1100 - enemyHudX)/10
                        #enemyTween[num] -= 50 if enemyTween[num] > -500 else 0


        #floaty += math.pi/15

        if energyGain > 0 and energyTrans < 1000:
            energyTrans += 11
            energyGain -= 11
            if energyGain < 0:
                while energyGain < 0:
                    energyTrans -= 7
                    energyGain += 7
            if energyGain < 11:
                energyTrans += energyGain
                energyGain = 0
            if energyTrans > 1000:
                energyTrans = 1000
        elif energyTrans > 1000:
            energyTrans = 1000
            energyGain = 0
        elif energyTrans == 1000 and energyGain > 0:
            energyGain = 0



        if energyGain < 0 and energyTrans > 0:
            energyTrans -= 7
            energyGain += 7
            if energyGain > -7:
                energyTrans += energyGain
                energyGain = 0
        elif energyTrans <= 0:
            energyTrans, energyGain = 0, 0




        if energyTrans > energy:
            energy += 7
        else:
            energy = energyTrans


        if movingHud < 0:
            movingHud += 7
            movingHud = math.ceil(movingHud)

        elif movingHud > 0:
            movingHud -= 7
            movingHud = round(movingHud)

        if tempAlly != selectedAlly:
            hudScroll = 100

        tempAlly = selectedAlly

        deadCount = 0

        checked = False

        for i in fightyLoop:
            for players in opponent:
                if players == i[0]:
                    checked = True
                    break
        oriOpponentCoords = opponentCoords.copy()
        if not (checked or backUpCoords != []):
            opponentCoords.clear()
        for num, enemies in enumerate(opponent):
            if checked or backUpCoords != []:
                continue
            opponentCoords.append([0])
            alive = 0
            for i in opponent:
                if i.hp > 0:
                    alive += 1
            if enemies.hp <= 0:
                deadCount += 1

            if alive == 0:
                alive = 1

            theWidth = 1000

            if firstPerson:
                #x = 500*((theWidth/2)/500) + 1000*(theWidth/1000)/alive * num + (width/2 - theWidth/2)
                x = 500*((theWidth/2)/500)/alive + 1000*(theWidth/1000)/alive * (num - deadCount)
            else:
                x = 600*((theWidth/2)/500) + 200*((theWidth/2)/500)/alive + 400*(theWidth/1000)/alive * (num - deadCount) + (width/2 - theWidth/2)
            y = 200 + 3*num - 3*len(opponent)

            if enemies.hp <= 0:
                opponentCoords[num] = oriOpponentCoords[num]
            else:
                opponentCoords[num] = [x, y]

        deadCount = 0
        checked = False
        for i in fightyLoop:
            for players in party:
                if players == i[0]:
                    checked = True
                    break
        oriPlayerCoords = playerCoords.copy()
        if not (checked or backUpCoords != []):
            playerCoords.clear()
        for num, players in enumerate(party):
            if checked or backUpCoords != []:
                continue
            playerCoords.append([0])
            alive = 0
            for i in party:
                if i.hp > 0:
                    alive += 1
            if players.hp <= 0:
                deadCount += 1

            if alive == 0:
                alive = 1

            theWidth = 1000
            if firstPerson:
                x = -200
            else:
                x = 200*((theWidth/2)/500)/alive + 400*(theWidth/1000)/alive * (num - deadCount) + (width/2 - theWidth/2)
            y = 200 + 3*num - 3*len(party)

            if players.hp <= 0:
                #pass
                playerCoords[num] = oriPlayerCoords[num]
            else:
                playerCoords[num] = [x, y]

        loadEnemy()
        loadPlayer()
        projectileUpdate()

        updateTween()
        updateAnimation()

        #draw()
        swapPosUpdate()


        effectUpdate()
        effectTextUpdate()
        healWhileloop()
        attackProUpdate()
        stupidFightLoop()
        stupidEnergyLoop()

        if useExtraDialogue:
            dialogueUpdate()


        for i in party:
            if i.name in ['Allerwave', 'The Creator']:
                i.hp += 2
                if i.hp <= 0:
                    i.hp = 1
                if i.hp >= i.maxhp:
                    i.hp = i.maxhp

        if turnAlly:
            actionWhich = allyAction
            whichSelection = allySelection #Targets, whichAction=index of the thing
            selectedWhich = selectedAlly
            theAlly = party
            theOpponent = opponent
            coords = opponentCoords
            other = playerCoords
            whichTurn = allyTurn
            color = colorOfAlly
            sprite = playerSprite
            usingEnergy = theAlly[selectedWhich].mana

        if turnEnemy:
            actionWhich = enemyAction
            whichSelection = enemySelection
            selectedWhich = selectedEnemy
            theAlly = opponent
            theOpponent = party
            coords = playerCoords
            other = opponentCoords
            whichTurn = enemyTurn
            color = colorOfEnemy
            sprite = enemySprite
            usingEnergy = theAlly[selectedWhich].mana

        #actionDict = {'inFight':'Choosing_attack', 'inFight':'Choosing_attack'}
        for num, ally in enumerate(theAlly):
            #if not (allyTurn or enemyTurn):
                #continue
            if str(actionWhich[num]) in ['Item_done', 'Item_on', 'usedItems', 'usedAct', 'usedSkills', 'doneSkills', 'Done']:
                #print(1)
                continue
            #print(ally.activity)
            ally.activity = str(actionWhich[num])
            #print(ally.activity)
            whatList = [0]*(whichAction[num] + 1)*2
            if 'Skill' in ally.activity:
                whatList = ally.skills
            if 'Fight' in ally.activity:
                whatList = ally.fight
            if 'Act' in ally.activity:
                whatList = ally.action
            if 'Item' in ally.activity:# and not ally.activity in ['Item_done', 'Item_on']:
                whatList = ally.inventory
            if 'Debug' in ally.activity:
                whatList = character.debug
            if 'None' not in ally.activity and 'Done' not in ally.activity:
                #print(ally.activity, whichAction[num], whatList)
                ally.usingWhat = whatList[whichAction[num]]

           # if 'Act' in ally.activity:
            ally.targets.clear()
            if 'Skill' in ally.activity:
                if 'everyone' in ally.usingWhat.type:
                    whichOne = party + opponent
                elif 'ally' in ally.usingWhat.type:
                    whichOne = theAlly
                elif 'opponent' in ally.usingWhat.type:
                    whichOne = theOpponent

                if isinstance(whichSelection[num], list):
                    for i in whichSelection[num]:
                        ally.targets.append(whichOne[i])
                else:
                    ally.targets.append(whichOne[whichSelection[num]])
            elif 'Act' in ally.activity:
                if 'ally' in ally.usingWhat.useOn or 'self' in ally.usingWhat.useOn:
                    whichOne = theAlly
                elif 'opponent' in ally.usingWhat.useOn:
                    whichOne = theOpponent

                if isinstance(whichSelection[num], list):
                    for i in whichSelection[num]:
                        ally.targets.append(whichOne[i])
                else:
                    ally.targets.append(whichOne[whichSelection[num]])

            elif 'Item' in ally.activity:
                whichOne = theAlly
                if 'ally' in ally.usingWhat.type:
                    whichOne = theAlly
                elif 'opponent' in ally.usingWhat.type:
                    whichOne = theOpponent

                if isinstance(whichSelection[num], list):
                    for i in whichSelection[num]:
                        ally.targets.append(whichOne[i])
                else:
                    ally.targets.append(whichOne[whichSelection[num]])

            elif 'Fight' in ally.activity:
                whichOne = theOpponent
                if 'ally' in ally.usingWhat.classType:
                    whichOne = theAlly
                elif 'opponent' in ally.usingWhat.classType:
                    whichOne = theOpponent

                if isinstance(whichSelection[num], list):
                    for i in whichSelection[num]:
                        ally.targets.append(whichOne[i])
                else:
                    ally.targets.append(whichOne[whichSelection[num]])


        if firstPerson:
            hudWidth = 600+200*width/1000
            baseTextBoxHeight = 150
            yOffset = 50
        else:
            hudWidth = 500+200*width/1000
            baseTextBoxHeight = 160
            yOffset = 50
        if (allyTurn or enemyTurn or gameOver or win):
            yPos = (height/2 + baseTextBoxHeight) - max(baseTextBoxHeight, textBox)
            yCenter = yPos + (max(baseTextBoxHeight, textBox) / 2) + yOffset
            HudTransition(hudRect, ['centerY', 'centerX', 'hudLength', 'hudHeight'], [yCenter, width/2, hudWidth, max(baseTextBoxHeight, textBox)])
        else:
            yCenter = yPos + (max(baseTextBoxHeight, textBox) / 2) + yOffset
            if inFight:
                if meleeUsed:
                    if meleeFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [527, 190])
                    else:
                        HudTransition(hudRect, ['hudLength'], [527 * attackFade[0]/300])
                elif rangeUsed:
                    if rangeFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [250, 250])
                    else:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [250 * attackFade[2]/300, 250])
                elif throwerUsed:
                    if throwerFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [250, 250])
                    else:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [250 * attackFade[1]/300, 250])
                elif tankUsed:
                    if tankFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [527, 190])
                    else:
                        HudTransition(hudRect, ['hudLength'], [527 * attackFade[3]/300])
                elif controllerUsed:
                    if controllerFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [527, 190])
                    else:
                        HudTransition(hudRect, ['hudLength'], [527 * attackFade[4]/300])
                elif supportUsed:
                    if supportFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight', 'centerY'], [190, 270, 395])
                    else:
                        HudTransition(hudRect, ['hudHeight', 'centerY'], [190 * attackFade[5]/300, 435])
                elif underUsed:
                    if underFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight', 'centerY'], [190, 270, 395])
                    else:
                        HudTransition(hudRect, ['hudHeight', 'centerY'], [190 * attackFade[6]/300, 435])
                elif slamUsed:
                    if slamFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [527, 190])
                    else:
                        HudTransition(hudRect, ['hudHeight'], [190 * attackFade[7]/300])
                elif backUsed:
                    if backFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [527, 190])
                    else:
                        HudTransition(hudRect, ['hudHeight'], [190 * attackFade[8]/300])
                elif holdUsed:
                    if holdFound:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [250, 250])
                    else:
                        HudTransition(hudRect, ['hudLength', 'hudHeight'], [250 * attackFade[9]/300, 250])

            else:
                yPos = (height/2 + baseTextBoxHeight) - max(baseTextBoxHeight, textBox)
                yCenter = yPos + (max(baseTextBoxHeight, textBox) / 2) + yOffset
                HudTransition(hudRect, ['centerY', 'centerX', 'hudLength', 'hudHeight'], [yCenter, width/2, hudWidth, max(baseTextBoxHeight, textBox)])
        loadMenu()

        for num, i in enumerate(party[::-1]):
            if backUpCoords == [] and i.hp <= 0 and num != len(party) - 1 and playerAlpha[::-1][num] == 0:
                if party[::-1][num + 1].hp > 0:
                    pass

        gameOver = True
        for num, i in enumerate(party):
            if i.hp > 0 or inFight or inSkill:
                gameOver = False
                break

        win = True
        for num, i in enumerate(opponent):
            if (i.hp > 0 and i.status != 'Spared') or inFight or inSkill or inAct or inItem:
                win = False
                break

        deadCount = 0
        for i in party:
            if i.hp <= 0:
                deadCount += 1

        if battleSplash == True and turnDialogue[min(turn, len(turnDialogue))-1][2] == True and tutorial:
            if turn==1 and not bossFight:
                inTurnText[1] = 'Let us start with fighting. Use [LEFT] and [RIGHT] keys to move your menu selection. Use [CONFIRM] on the Fight button.'
                inTurnText[0] = 'Mascot'
                inTurnText[2] = 'Neutral'
                if confirm and actions[selectedAction] != 'Fight':
                    addTurnDialogue('Clear')
                    text_index = 0
                    addTurnDialogue('Mascot', "Let's not focus on that now shall we?", 0, 'Confused')
                    addTurnDialogue('Mascot', "Use the Fight button!", 0, 'Confused')
                    actionWhich[selectedWhich] = None
                elif actionWhich[selectedWhich] == 'chooseFightTarget':
                    inTurnText[1] = 'Use [LEFT] and [RIGHT] to move selection if there is more than one enemy. Use [CONFIRM] on the enemy you wish to target.'
            else:
                if deadCount == 0:
                    inTurnText[1] = 'The realm is swaying.'
                elif deadCount == 1:
                    inTurnText[1] = f'{theAlly[selectedWhich].name} is feeling stressed out.'
                if actionWhich[selectedWhich] == 'chooseFightTarget':
                    inTurnText[1] = f'{theAlly[selectedWhich].name} hands grip tightly.'

        if useCustomBattle:
            onUpdate()

        if battleStart <= 0:
            #if deadCount > 0:
                #hud.camera_fade = 120
            #else:
                #hud.camera_fade = 0
            #hud.camera_shake = deadCount
            #screen.camera_shake = deadCount
            #hud.camera_color = BLACK
            #hud.camera_fade = deadCount*100/len(party)
            #hud.camera_color = RED
            aliveAlly = []
            for i in party:
                if i.hp > 0:
                    aliveAlly.append(i)
            aliveEnemy = []
            for i in opponent:
                if i.hp > 0:
                    aliveEnemy.append(i)
            doIt = False
            if len(party) > 2 and len(opponent) > 2:
                doIt = True
            if len(aliveAlly) == 1 and len(aliveEnemy) == 1 and doIt:
                if not intenseMode:
                    intenseMode = True
                    screenText.append(['[b]1    O N    1[/b]', RED, 0, False, 50])
                    screenText.append([f'{aliveAlly[0].name} vs {aliveEnemy[0].name}', RED, 0, False, 40, 50])
                    #party.clear()
                    #opponent.clear()
                    #for i in aliveAlly:
                     #   party.append(i)
                    #for i in aliveEnemy:
                    #    opponent.append(i)
                    #party = aliveAlly
                    #opponent = aliveEnemy
                    #speedReset()
                    if useDebug:
                        destroyAction("Debug")
                    if screenWindow.useWeb:
                        pygame.mixer.stop()
                        if aliveAlly[0].level >= 10:
                            playSound('music/Megalovania.ogg', -1)
                        else:
                            if sys.platform == "emscripten":
                                audio.src = 'music/3.mp3'
                            else:
                                playSound(f'music/3.ogg', 1, True)
                        #pygame.mixer.music.load("sounds/music/3.ogg")
                        #pygame.mixer.music.play(fade_ms=3000)
                    else:
                        music.stop()
                        if aliveAlly[0].level >= 10:
                            music = DynamicMusicPlayer(f"sounds/music/Megalovania.ogg", loop=True)
                        else:
                            #playSound('music/3.ogg', -1)
                            music = DynamicMusicPlayer(f"sounds/music/3.ogg", loop=True)
                        #music.fade_in()
            if doIt and intenseMode:
                    backGroundScreen.camera_color = (255, 0, 0)
                    backGroundScreen.camera_fade = 150
                    hud.cameraY = 2*math.sin(frame/7)
                    hud.cameraX = 4*math.cos(frame/14)
                    #backGroundScreen.cameraX = 5*math.cos(frame/14)
                    #backGroundScreen.cameraY = 2.5*math.sin(frame/7)
                    #screen.camera_rotation = math.sin(frame/7)
                    #backGroundScreen.camera_rotation = math.sin(frame/7)
                    #screen.cameraX = 5*math.cos(frame/14)
                    #screen.cameraY = 2.5*math.sin(frame/7)
                    

        if not screenWindow.useWeb and party[0].name != 'Zee':
            music.set_speed((playBack-0.15*deadCount/len(party)))
            if sys.platform == "emscripten":
                #audio.src = 'music/3.mp3'
                audio.preservesPitch = False
                audio.playbackRate = max(0.5, random.randint(1,3)/3)
        elif party[0].name == 'Zee' and frame%10 == 0:
            music.set_speed(max(0.5, random.randint(1,3)/3) )
            hud.camera_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            hud.camera_fade = 100

        #dafps = 60 + 10*deadCount
        if buffMenu:
            whichTurn = False

        if actionList[0] == True:
            whichTurn = False
        if turn <= len(turnDialogue) and not gameOver and not win:
            if turnDialogue[turn-1][2] == False:
                whichTurn = False
                splashText(f'* {turnDialogue[turn-1][1][turnDialogue[turn-1][3]]}', True, text_index)
                battleText(True, name=turnDialogue[turn-1][0][turnDialogue[turn-1][3]], forceDo=True, emotion=turnDialogue[turn-1][4][turnDialogue[turn-1][3]])
                if cancel or skipDialogue:
                    text_index = len(splashy)

                if confirm or skipDialogue:
                    if text_index >= len(splashy) and len(turnDialogue[turn-1][1]) - 1 == turnDialogue[turn-1][3]:# and backUpCoords == []:
                        battleSplash = True
                        turnDialogue[turn-1][2] = True
                        text_index = 0

                    elif text_index >= len(splashy):
                        text_index = 0
                        turnDialogue[turn-1][3] += 1

        if gameOver and allowGameOver:
            if (not turnAlly) or allyTurn or enemyTurn or turnEnemy:
                playSound('Lose_sfx.ogg')
            turnAlly = True
            allyTurn = enemyTurn = turnEnemy = False
            splashText('* Everyone is down. You have lost the battle...', True, text_index)
            battleText()
            if confirm:
                onEnd()
                inBattle = False
                if not screenWindow.useWeb:
                    music.stop()
                for i in character.party:
                    for buff in i.passiveBuff:
                        i.passiveBuff[buff] = [False, False]
                    i.buff = {}

            continue
            pass

        if win and allowWin:
            if (not turnAlly) or allyTurn or enemyTurn or turnEnemy:
                playSound('Win_sfx.ogg')
            turnAlly = True
            allyTurn = enemyTurn = turnEnemy = False
            text = f'* All the opponents are down! You won!'
            if canGainXp:
                text += '\n*Everyone gained 20Xp!!'
            if not useDebug:
                if len(party) == 1 and party[0].name == "Thin":
                    achievementObj["Thin Win!"].trigger()
                if len(party) == 5:
                    achievementObj["Victorious!"].trigger()
            splashText(text, True, text_index)
            battleText()
            if confirm:
                onEnd()
                inBattle = False
                if not screenWindow.useWeb:
                    music.stop()
                for i in character.party:
                    for buff in i.passiveBuff:
                        i.passiveBuff[buff] = [False, False]
                    i.buff = {}

                if canGainXp or True:
                    totalXp = 20*len(opponent)
                    for i in party:
                        i.levelUp(totalXp/len(opponent))
            continue


        if selectedAlly >= len(party):
            allyTurn = False



        if theAlly[selectedWhich].hp <= 0:
            if speedBasedTurn:
                resetAllyTurn()
                #pass
                continue
            else:
                if turnAlly:
                    selectedAlly += 1
                    selectedWhich = selectedAlly
                elif turnEnemy:
                    selectedEnemy += 1
                    selectedWhich = selectedEnemy

        if speedBasedTurn:
            arrow = loadImg(('ArrowPointer.png', 0.5))
            blitObj(screen, arrow, sprite[selectedWhich].pos[0], sprite[selectedWhich].pos[1] - 160)

        if not whichTurn:
            if 'Skills' in actionWhich or 'usedSkills' in actionWhich or 'doneSkills' in actionWhich:
                inSkill = True
                inAct = False
                inItem = False
                inFight = False
            elif 'usedAct' in actionWhich or 'Act' in actionWhich:
                inSkill = False
                inAct = True
                inItem = False
                inFight = False
            elif 'Items' in actionWhich:
                inSkill = False
                inAct = False
                inItem = True
                inFight = False
            elif 'usedItems' in actionWhich:
                inSkill = False
                inAct = False
                inItem = True
                inFight = False
            elif 'Fight' in actionWhich:
                inSkill = False
                inAct = False
                inFight = True
                inItem = False
            elif meleeDone and throwerDone and rangeDone and tankDone and controllerDone and supportDone and slamDone and underDone and backDone and holdDone:
                continueTurn = False
                for i in actionWhich:
                    if i != 'Done':
                        continueTurn = False
                        break
                if not continueTurn:
                    resetAllyTurn()
                continue
        else:
            inSkill = inAct = inFight = inItem = False
            if 'Done' in actionWhich:
                resetAllyTurn()
                continue

        if cancel or skipDialogue:
            if not (allyTurn or enemyTurn):
                text_index = len(splashy)

        if (confirm or skipDialogue) and not (allyTurn or enemyTurn):
            if inSkill:
                if text_index >= len(splashy) and actionWhich[skillParty] == 'usedSkills':
                    actionWhich[skillParty] = 'Done'
                    text_index = 0
                    if skillParty < len(party) - 1:
                        while 'Skills' not in str(actionWhich[skillParty]) and skillParty < len(theAlly) - 1:
                            skillParty += 1
                    if skillParty >= len(theAlly) - 1:
                        addInBar()

            elif inAct:
                if text_index >= len(splashy) and actionNum == len(actionDia) - 1 and backUpCoords == []:
                    actionWhich[actParty] = 'Done'
                    text_index = 0
                    actParty += 1
                    if actParty > len(theAlly) - 1:
                        actParty = len(theAlly)
                    addInBar()
                    if actParty < len(theAlly) - 1:
                        #print(actionWhich, actParty)
                        while 'Act' not in str(actionWhich[actParty]) and actParty < len(theAlly) - 1:
                            actParty += 1

                elif text_index >= len(splashy) and actionNum < len(actionDia) - 1:
                    actionNum += 1
                    text_index = 0

            elif inItem:
                if text_index >= len(splashy):
                    if text_index >= len(splashy) and actionWhich[itemParty] == 'usedItems':
                        actionWhich[itemParty] = 'Done'
                        text_index = 0
                        itemParty += 1
                        addInBar()
                        if itemParty < len(theAlly) - 1:
                            while 'Items' not in str(actionWhich[itemParty]) and itemParty < len(theAlly) - 1:
                                itemParty += 1

        if confirm and not (allyTurn or enemyTurn):
            if inFight and not botplay:
                rangeThing = 6
                if meleeUsed:
                    maxDistance = (hudRect[4] + hudRect[2])/2

                elif throwerUsed:
                    maxDistance = 0
                    rangeThing = 0.1

                elif rangeUsed:
                    maxDistance = math.pi * 5

                elif supportUsed:
                    maxDistance = hudRect[3] + hudRect[5]
                    rangeThing = 0.1

                elif underUsed:
                    maxDistance = hudRect[5]
                    rangeThing = 0.1

                elif slamUsed:
                    maxDistance = (hudRect[4] + hudRect[2]) + 90

                elif backUsed:
                    maxDistance = hudRect[4] + 90

                else:
                    maxDistance = hudRect[4] + hudRect[2]/2


                if ((int(hudRect[2]) == 527 or int(hudRect[2]) == 250 or int(hudRect[2]) == 190) or instantAttack) and not holdUsed and inBar >= 1 and not (enemyAutoAttack and opponentBot and turnEnemy):

                    dashPassed = False
                    distance = []
                    allBarHit = True

                    for num, bar in enumerate(fightBar[:inBar]):
                        theBar = fightingBar[bar][2]
                        if ('done' not in theBar) and ('fail' not in theBar) and ('NoBar' not in theBar):
                            distance.append(abs(maxDistance - fightBarX2[num]))
                            allBarHit = False

                        else:
                            distance.append(9999)


                    barSelect = distance.index(min(distance))


                    if not allBarHit:
                        pass

                    name = ''
                    for letter in fightBar[barSelect]:
                        if dashPassed:
                            name += letter
                        elif letter == '_':
                            dashPassed = True

                    fightingBar[fightBar[barSelect]][2] = 'done'
                    fightingBar[fightBar[barSelect]][7].currentBar = fightingBar[fightBar[barSelect]][10]
                    theBar = fightingBar[fightBar[barSelect]][7].bars
                    fightingBar[fightBar[barSelect]][7].nextBar = theBar[ min(theBar.index(fightingBar[fightBar[barSelect]][10]) + 1, len(theBar) - 1 )]
                    for distNum, dist in enumerate(distance):
                        dashPassed = False
                        name = ''
                        for letter in fightBar[distNum]:
                            if dashPassed:
                                name += letter
                            elif letter == '_':
                                dashPassed = True
                        if abs(float(distance[barSelect]) - float(dist)) <= rangeThing and dist != 9999:
                            fightingBar[fightBar[distNum]][2] = f'done'

        if not whichTurn:

            if ('Skills' in actionWhich or 'usedSkills' in actionWhich or 'doneSkills' in actionWhich):
                skills = skillUsed[skillParty]
                allyGiver = theAlly[skillParty]
                if 'opponent' in skills.type:
                    whichOne = theOpponent
                elif 'ally' in skills.type:
                    whichOne = theAlly
                else:
                    whichOne = theAlly + theOpponent
                if isinstance(whichSelection[skillParty], list):
                    allyReceiver= []
                    for i in whichSelection[skillParty]:
                        allyReceiver.append(whichOne[i])
                else:
                    allyReceiver = whichOne[whichSelection[skillParty]]
                addInfo = ''
                if 'opponent' in skills.type:
                    itemText = f'* {allyGiver.name} Used {skills.name.upper()}!'
                    if skills.applyEffect != {}:
                        addInfo = '* Inflicted'
                        for i in skills.applyEffect:
                            addInfo += f' {i.name},'
                        addInfo = addInfo[:-1]
                        addInfo += '!'
                else:
                    itemText = f'* {allyGiver.name} Used {skills.name.upper()}!'
                    if skills.applyEffect != {}:
                        addInfo = '* Buff with'
                        for i in skills.applyEffect:
                            addInfo += f' {i.name},'
                        addInfo = addInfo[:-1]
                        addInfo += '!'


                if actionWhich[skillParty] == 'Skills':
                    skills.use(allyGiver, allyReceiver)
                    playSound('Skill_sfx.ogg')
                    camSet(1.3, YELLOW, 170, 1)
                    if skills.useAnim == False:
                        actionWhich[skillParty] = 'usedSkills'


                splashText(itemText + '\n' + addInfo, True, text_index)
                battleText()

                for num, ally in enumerate(theAlly[:(skillParty + 1)]):
                    if actionWhich[num] == 'Fight' or skillUsed[num] == None or skillUsed[num].useAnim == False:
                        continue
                    else:

                        strike = True
                        animate = True
                        weaponUsed = character.skillAnim
                        skillUsedNow = skillUsed[num]
                        if 'hp' in skillUsedNow.type or 'opponent' in skills.type:
                            allyDamage[num] = skillUsedNow.num

                        if allyDamage[num] == None or skillUsedNow == None:
                            strike = False
                            animate = False


                        if attackFrame[num] == 0 and animate:
                            if actionWhich[skillParty] == 'Skills':
                                actionWhich[skillParty] = 'usedSkills'
                                if 'ally' in skills.type:
                                    whichOne = theAlly
                                elif 'opponent' in skills.type:
                                    whichOne = theOpponent
                                else:
                                    whichOne = theAlly + theOpponent
                                if isinstance(whichSelection[num], list):
                                    allOpponents = []
                                    for allyNum, allies in enumerate(whichSelection[num]):
                                        if whichOne[allies].hp > 0:
                                            allOpponents.append(whichOne[allies])
                                    attacking.append([ allOpponents , theAlly[num], skills.animType, skills.num*theAlly[num].damage, False, skills, None])
                                else:
                                    for repeatation in range(0, skills.repeatHowMany):
                                        if 'opponent' in skills.type:
                                            #print(7)
                                            attacking.append([ [theOpponent[whichSelection[num]]] , theAlly[num], skills.animType, skills.num*theOpponent[whichSelection[num]].damage, False, skills, None])
                                        else:
                                            attacking.append([ [theAlly[whichSelection[num]]] , theAlly[num], skills.animType, skills.num, False, skills, None])


            elif ('Act' in actionWhich or 'usedAct' in actionWhich):
                act = actUsed[actParty]
                allyGiver = theAlly[actParty]
                if 'opponent' in act.useOn:
                    allyReceiver = theOpponent[whichSelection[actParty]]
                else:
                    allyReceiver = theAlly[whichSelection[actParty]]

                if actionWhich[actParty] == 'Act':
                    actionDia = act.call(allyReceiver, allyGiver, 0)
                    playSound('snd_item.ogg')
                    actionWhich[actParty] = 'usedAct'
                    camSet(1.3, CYAN, 170, 1)
                    if 'Swap' in act.name:
                        swapPos(allyGiver, allyReceiver)

                if isinstance(actionDia[actionNum], str):
                    splashText(actionDia[actionNum], True, text_index)
                    battleText()
                elif isinstance(actionDia[actionNum], list):
                    splashText(actionDia[actionNum][0], True, text_index)
                    if actionDia[actionNum][1] != None:
                        battleText(True, actionDia[actionNum][1])
                    else:
                        battleText()
            elif ('Items' in actionWhich or 'usedItems' in actionWhich):
                items = itemUsed[itemParty]
                if 'ally' in items.type:
                    whichOne = theAlly
                elif 'opponent' in items.type:
                    whichOne = theOpponent
                else:
                    whichOne = theAlly + theOpponent
                allyGiver = theAlly[itemParty]
                allyReceiver = whichOne[whichSelection[itemParty]]
                if 'Weapon' in items.type or 'Armour' in items.type:
                    if allyGiver.name == allyReceiver.name:
                        itemText = f'* {allyGiver.name} equipped the {items.name}!'
                        addInfo = ''
                    else:
                        itemText = f'* {allyGiver.name} gave the {items.name} to {allyReceiver.name}!'
                        addInfo = f'* {allyReceiver.name} equipped the {items.name}!'
                elif 'usedItems' not in actionWhich:
                    if allyGiver.name == allyReceiver.name:
                        itemText = f'* {allyGiver.name} used the {items.name}!'
                        addInfo = f''
                    elif allyGiver in theAlly and allyReceiver in theOpponent:
                        itemText = f'* {allyGiver.name} threw the {items.name} to {allyReceiver.name}!'
                        addInfo = f'* {allyReceiver.name} was affected by the {items.name}!'
                    elif allyGiver in theAlly and allyReceiver in theAlly:
                        itemText = f'* {allyGiver.name} gave the {items.name} to {allyReceiver.name}!'
                        addInfo = f'* {allyReceiver.name} used the {items.name}!'

                    #if (allyReceiver.hp + items.num) < allyReceiver.maxhp:
                     #   addInfo = f'* {allyReceiver.name} Recovered {items.num}HP!'
                    #else:
                     #   addInfo = f"* {allyReceiver.name}'s HP is fully Restored!"

                    if allyReceiver.hp <= 0 and items.name != 'Life Cube':
                        addInfo = f'* But, it did not work.'

                if actionWhich[itemParty] == 'Items':
                    itemHeal[itemParty] = items.use(allyReceiver, allyGiver, itemParty)
                    playSound('snd_item.ogg' if 'Weapon' in items.type or 'Armour' in items.type else 'Healing_sfx.ogg')
                    actionWhich[itemParty] = 'usedItems'
                    camSet(1.3, GREEN, 170, 1)


                splashText(itemText + ' \n' + addInfo, True, text_index)
                battleText()

            elif inFight == True:

                meleeUsed = False
                throwerUsed = False
                rangeUsed = False
                tankUsed = False
                controllerUsed = False
                supportUsed = False
                underUsed = False
                slamUsed = False
                backUsed = False
                holdUsed = False

                meleeFound = False
                throwerFound = False
                rangeFound = False
                tankFound = False
                controllerFound = False
                supportFound = False
                underFound = False
                slamFound = False
                backFound = False
                holdFound = False

                meleeParticipants = []
                throwerParticipants = []
                rangeParticipants = []
                tankParticipants = []
                controllerParticipants = []
                supportParticipants = []
                underParticipants = []
                slamParticipants = []
                backParticipants = []
                holdParticipants = []


                for i in fightBar:
                    if 'Melee' in i:
                        meleeUsed = True

                if meleeUsed:
                    for num, i in enumerate(actionWhich):
                        if 'Melee' in theAlly[num].tempClass:
                            meleeParticipants.append(i)
                            if 'Fight' in str(i) or str(i) in 'doneMiss':
                                meleeFound = True

                    if meleeDone:
                        meleeUsed = False




                if meleeUsed == False:
                    for i in fightBar:
                        if 'Thrower' in i:
                            throwerUsed = True
                    if throwerUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Thrower' in theAlly[num].tempClass:
                                throwerParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    throwerFound = True

                        if throwerDone:
                            throwerUsed = False




                if throwerUsed == False:
                    for i in fightBar:
                        if 'Range' in i:
                            rangeUsed = True
                    if rangeUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Range' in theAlly[num].tempClass:
                                rangeParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    rangeFound = True

                        if rangeDone:
                            rangeUsed = False




                if rangeUsed == False:
                    for i in fightBar:
                        if 'Tank' in i:
                            tankUsed = True
                    if tankUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Tank' in theAlly[num].tempClass:
                                tankParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    tankFound = True

                        if tankDone:
                            tankUsed = False




                if tankUsed == False:
                    for i in fightBar:
                        if 'Controller' in i:
                            controllerUsed = True
                    if controllerUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Controller' in theAlly[num].tempClass:
                                controllerParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    controllerFound = True

                        if controllerDone:
                            controllerUsed = False

                       # #print(controllerDone)


                if controllerUsed == False:
                    for i in fightBar:
                        if 'Support' in i:
                            supportUsed = True

                    if supportUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Support' in theAlly[num].tempClass:
                                supportParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    supportFound = True

                        if supportDone:
                            supportUsed = False

                if supportUsed == False:
                    for i in fightBar:
                        if 'Under' in i:
                            underUsed = True

                    if underUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Under' in theAlly[num].tempClass:
                                underParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    underFound = True

                        if underDone:
                            underUsed = False

                if underUsed == False:
                    for i in fightBar:
                        if 'Slam' in i:
                            slamUsed = True

                    if slamUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Slam' in theAlly[num].tempClass:
                                slamParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    slamFound = True

                        if slamDone:
                            slamUsed = False

                if slamUsed == False:
                    for i in fightBar:
                        if 'Back' in i:
                            backUsed = True

                    if backUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Back' in theAlly[num].tempClass:
                                backParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                    backFound = True

                        if backDone:
                            backUsed = False

                if backUsed == False:
                    for i in fightBar:
                        if 'Hold' in i:
                            holdUsed = True

                    if holdUsed:
                        for num, i in enumerate(actionWhich):
                            if 'Hold' in theAlly[num].tempClass:
                                holdParticipants.append(i)
                                if 'Fight' in str(i) or str(i) in 'doneMiss':
                                   holdFound = True

                        if holdDone:
                            holdUsed = False


                if meleeUsed and not meleeDone:
                    if int(hudRect[2]) == 527 and meleeFound:

                        attackMeter = loadImg(('attackMeter.png', 0.5))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[2]/2 + hudRect[4]


                        barBlit() # Animate the bar moving across the meter

                        damageControl('Melee')
                        attackFade[0] = 255


                    elif not meleeFound:
                        #inBar = 0
                        #fightFrame = 0
                        if attackFade[0] > 0:
                            attackFade[0] -= 20 * theDelta
                            attackFade[0] = max(attackFade[0], 0)

                            #barBlit()

                            attackMeter = loadImg(('attackMeter.png'))
                            attackMeter.set_alpha(attackFade[0])
                            attackMeter = scaleObj(attackMeter, (0.5 * attackFade[0]/255, 0.5))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            barBlit()
                        else:
                            meleeDone = True
                            inBar = 0
                            fightFrame = 0

                    elif int(hudRect[2]) != 527 and meleeFound:
                        attackFade[0] = max(0, attackFade[0] - 20 * theDelta)
                        attackMeter = loadImg(('attackMeter.png', (0.5 * (1 - attackFade[0]/255), 0.5)))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[0])
                        if instantAttack:
                            attackMeter = loadImg(('attackMeter.png', 0.5))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            barBlit()
                            damageControl('Melee')
                            attackFade[0] = 255
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                elif throwerUsed and not throwerDone:
                    if int(hudRect[2]) == 250 and throwerFound:
                        attackFade[2] = 255
                        attackMeter = loadImg(('attackSpiralMeter.png', 0.25))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[2]/2 + hudRect[4]


                        spiralBlit() # Animate the bar moving across the meter

                        damageControl('Thrower')


                    elif not throwerFound:
                        if attackFade[2] - 20 > 0:
                            attackFade[2] -= 20 * theDelta

                            attackMeter = loadImg('attackSpiralMeter.png')
                            attackMeter.set_alpha(attackFade[2])
                            attackMeter = scaleObj(attackMeter, (0.25 * attackFade[2]/255))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            spiralBlit()
                        else:
                            throwerDone = True
                            inBar = 0
                            fightFrame = 0

                    elif int(hudRect[2]) != 250 and throwerFound:
                        attackFade[2] = max(0, attackFade[2] - 20 * theDelta)
                        attackMeter = loadImg(('attackSpiralMeter.png', 0.25 * (1 - attackFade[2]/255)))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[2])
                        if instantAttack:
                            attackFade[2] = 255
                            attackMeter = loadImg(('attackSpiralMeter.png', 0.25))
                            attackMeter.set_alpha(255)
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            spiralBlit()
                            damageControl('Thrower')
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                elif rangeUsed and not rangeDone:
                    if int(hudRect[2]) == 250 and rangeFound:
                        attackMeter = loadImg(('attackDiscMeter.png', 0.25))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[2]/2 + hudRect[4]


                        discBlit() # Animate the bar moving across the meter

                        damageControl('Range')
                        attackFade[1] = 255


                    elif not rangeFound:
                        if attackFade[1] - 20 > 0:
                            attackFade[1] -= 20 * theDelta

                            attackMeter = loadImg('attackDiscMeter.png')
                            attackMeter.set_alpha(attackFade[1])
                            attackMeter = scaleObj(attackMeter, (0.25 * attackFade[1]/255))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            discBlit()
                        else:
                            rangeDone = True
                            inBar = 0
                            fightFrame = 0

                    elif int(hudRect[2]) != 250 and rangeFound:
                        attackFade[1] = max(0, attackFade[1] - 20 * theDelta)
                        attackMeter = loadImg(('attackDiscMeter.png', 0.25 * (1 - attackFade[1]/255)))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[1])
                        if instantAttack:
                            attackMeter = loadImg(('attackDiscMeter.png', 0.25))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            discBlit()
                            damageControl('Range')
                            attackFade[1] = 255
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])


                elif tankUsed and not tankDone:
                    if tankFound:
                        inBar = 0
                        fightFrame = 0
                        attackMeter = loadImg('attackMeter.png')
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))

                        attackMeterX = hudRect[2]/2 + hudRect[4]

                        keys = pygame.key.get_pressed()
                        keys_2 = {'K_LEFT': leftPressed,'K_DOWN': downPressed, 'K_UP': upPressed, 'K_RIGHT': rightPressed}

                        numPassed =  False

                        for number, bar in enumerate(fightingBar):
                            if not 'Tank' in bar:
                                continue


                            dashPassed = 0
                            name = ''
                            classes = ''
                            identifier = ''
                            for letter in bar:
                                if dashPassed == 1:
                                    if letter == '_':
                                        dashPassed = 2
                                    else:
                                        classes += letter
                                elif dashPassed == 2:
                                    if letter.isdigit():
                                        dashPassed = 3
                                    else:
                                        identifier += letter
                                elif letter == '_':
                                    dashPassed = 1
                                elif dashPassed == 0:
                                    name += letter

                            for num, ally in enumerate(theAlly):
                                if ally.name == name:
                                    barColor = color[num]
                                    allyNum = num

                            if opponentBot and turnEnemy and not enemyAutoAttack:
                                speedDifference = abs(party[enemySelection[allyNum]].speed - opponent[allyNum].speed) / 100
                                speedModifier = 1 + speedDifference if party[enemySelection[allyNum]].speed < opponent[allyNum].speed else 1 - abs(speedDifference)
                                addMulti = 1 if hardMode else 0.2
                                baseNum = 2*theDelta if not easyMode else 1.5*theDelta
                            else:
                                speedDifference = abs(theOpponent[whichSelection[allyNum]].speed - theAlly[allyNum].speed) / 100
                                speedModifier = 1 + speedDifference if theOpponent[whichSelection[allyNum]].speed > theAlly[allyNum].speed else 1 - abs(speedDifference)
                                addMulti = 0
                                baseNum = 1*theDelta

                            if speedModifier < 0.7:
                                speedModifier = 0.7
                            if speedModifier > 2.5:
                                speedModifier = 2.5

                            doKeyHit = False
                            if botplay and turnAlly:
                                if frame%2 == 0:
                                    doKeyHit = True
                            if ((opponentBot and turnEnemy and not enemyAutoAttack)) and fightBarX[number] < 100:
                                keyHit[allyNum] += 0.8
                            elif enemyAutoAttack and turnEnemy and opponentBot:
                                if frame%4 == 0:
                                    doKeyHit = True
                                #keyHit[allyNum] += 0.5
                            if keyHit[allyNum] < 0:
                                keyHit[allyNum] = 0

                            fightBarX[number] += speedModifier*baseNum
                            if fightBarX[number] >= 100 or (turnEnemy and opponentBot and keyHit[allyNum] == 0 and not enemyAutoAttack) or keyHit[allyNum] > 15*len(keyUsed[allyNum]):
                                keyDone[allyNum] = True
                                multiplier = keyHit[allyNum]/(15*len(keyUsed[allyNum]))
                                multiplier += addMulti
                                multiplier = min(multiplier, 1.4)
                                if useDefensePercent:
                                    damage = theAlly[allyNum].attack * ((100 - theOpponent[whichSelection[allyNum]].defense)/100)
                                else:
                                    damage = theAlly[allyNum].attack - theOpponent[whichSelection[allyNum]].defense
                                fightingBar[bar][2] = 'done'
                                fightingBar[bar][5] = damage * multiplier
                                fightingBar[bar][4] = multiplier

                            timeLength = 210 * (100 - fightBarX[number]) / 100

                            hpBG_X = hudRect[4] + 30
                            hpBG_Y = hudRect[5] - 30 + hudRect[3] - 35
                            hpX = hpBG_X + 5
                            hpY = hpBG_Y + 5

                            drawRect(hud, (0, 150, 150), (hpBG_X, hpBG_Y, 220, 35)) # The HPBG one
                            drawRect(hud, (0, 200, 200), (hpX, hpY, 210, 25)) # The MAX HP one
                            drawRect(hud, CYAN, (hpX, hpY, timeLength, 25)) # The HP one

                            hit = render_text(f'Hits: {int(keyHit[allyNum])}/{15*len(keyUsed[allyNum])}', WHITE, 40)

                            blitObj(hud, hit, hpBG_X + 240, hpBG_Y, 'topleft')

                            for num, i in enumerate(keyUsed[allyNum]):
                                x = hudRect[4] + 100*num + 60
                                y = hudRect[5] + 60
                                key_pressed = keys[getattr(pygame, f"K_{i}")] or keys_2[f"K_{i}"]
                                if (key_pressed or keyUsedBool[num] == True) and not keyDone[allyNum] and not (turnEnemy and opponentBot and enemyAutoAttack):
                                    if not keyIsUsed[num]:
                                        buttonColor = YELLOW
                                        scale = 0.6
                                        keyHit[allyNum] += 1 if not (opponentBot and turnEnemy) else -1
                                    keyIsUsed[num] = True
                                elif doKeyHit:
                                    buttonColor = YELLOW
                                    scale = 0.6
                                    keyHit[allyNum] += 1 
                                else:
                                    buttonColor = WHITE
                                    scale = 0.7
                                    keyIsUsed[num] = False
                                arrow = loadImg( (f'{i}.png', scale, buttonColor) )
                                blitObj(hud, arrow, x, y)


                        damageControl('Tank')



                    elif int(hudRect[2]) <= 527 and not tankFound:
                        if attackFade[3] - 20 > 0:
                            attackFade[3] -= 20 * theDelta
                        else:
                            tankDone = True

                elif controllerUsed and not controllerDone:
                    inBar = 0
                    fightFrame = 0
                    if int(hudRect[2]) == 527 and controllerFound:

                        attackMeter = loadImg('attackMeter.png')
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))

                        attackMeterX = hudRect[2]/2 + hudRect[4]

                        for number, bar in enumerate(fightingBar):
                            if not 'Controller' in bar:
                                continue

                            i = fightingBar[bar][6]

                            if opponentBot and turnEnemy and not enemyAutoAttack:
                                speedDifference = abs(party[enemySelection[number]].speed - opponent[number].speed) / 100
                                speedModifier = 1 + speedDifference if party[enemySelection[number]].speed < opponent[number].speed else 1 - abs(speedDifference)
                                base = 1.5 if hardMode else 1
                                further = 0.8 if hardMode else 0.3
                                baseNum = 4*theDelta if not easyMode else 1.5*theDelta
                            else:
                                #print(number, len(theAlly))
                                theNum = theAlly.index(i)
                                speedDifference = abs(theOpponent[whichSelection[theNum]].speed - theAlly[theNum].speed) / 100
                                speedModifier = 1 + speedDifference if theOpponent[whichSelection[theNum]].speed > theAlly[theNum].speed else 1 - abs(speedDifference)
                                base = 0
                                further = 0
                                baseNum = 2*theDelta

                            if opponentBot and turnEnemy and enemyAutoAttack:
                                if frame%3 == 0 and not keyDone[theNum]:
                                    keyHit[theNum] += 1
                                    if random.randint(1, 100) <= 7*keyHit[theNum]:
                                        keyDone[theNum] = True
                            if turnAlly and botplay:
                                if frame%2 == 0 and not keyDone[theNum]:
                                    keyHit[theNum] += 1

                            if speedModifier < 0.2:
                                speedModifier = 0.2
                            if speedModifier > 2.5:
                                speedModifier = 2.5

                            if keyDone[theNum] == False:
                                fightBarX[number] += baseNum*speedModifier*4/len(keyUsed[theNum])
                            if fightBarX[number] >= 80 or keyHit[theNum] == len(keyUsed[theNum]) or keyDone[theNum]:
                                keyDone[theNum] = True
                                multiplier = abs(keyHit[theNum]/len(keyUsed[theNum]) - base) + further
                                added = 0 if multiplier < 1 else 0.3
                                multiplier += added
                                if useDefensePercent:
                                    damage = i.attack * ((100 - theOpponent[whichSelection[theNum]].defense)/100)
                                else:
                                    damage = i.attack - theOpponent[whichSelection[theNum]].defense
                                allyDamage[number] = damage * multiplier
                                fightingBar[bar][2] = 'done'
                                fightingBar[bar][5] = damage * multiplier
                                fightingBar[bar][4] = multiplier

                            timeLength = 210 * (70 - fightBarX[number]) / 70

                            hpBG_X = hudRect[4] + 30
                            hpBG_Y = hudRect[5] - 30 + hudRect[3] - 35
                            hpX = hpBG_X + 5
                            hpY = hpBG_Y + 5

                            drawRect(hud, (0, 150, 150), (hpBG_X, hpBG_Y, 220, 35)) # The HPBG one
                            drawRect(hud, (0, 200, 200), (hpX, hpY, 210, 25)) # The MAX HP one
                            drawRect(hud, CYAN, (hpX, hpY, timeLength, 25)) # The HP one

                            hit = render_text(f'Hits: {keyHit[theNum]}/{len(keyUsed[theNum])}', WHITE, 40)
                            blitObj(hud, hit, hpBG_X + 240, hpBG_Y, 'topleft')
                            numUsed = 0

                            breakTurn = False
                            for num, i in enumerate(keyUsed[theNum]):
                                variable = {letter: None for letter in string.ascii_lowercase}
                                color = {"LEFT":(155, 0, 255), "DOWN":(0, 255, 255), "UP":(0, 255, 0), "RIGHT":(255, 0, 0)}
                                angle = {"LEFT":90, "DOWN":180, "UP":0, "RIGHT":270}
                                poop = {"LEFT":leftPressed, "RIGHT":rightPressed, "UP":upPressed, "DOWN":downPressed}
                                index = {"LEFT":0, "RIGHT":1, "UP":2, "DOWN":3}
                                indexNum = index[i]
                                x = hudRect[4] + 80*num + 30
                                y = hudRect[5] + 30
                                key_pressed = poop[i]#pygame.key.get_pressed()[getattr(pygame, f"K_{i}")]

                                if (key_pressed or keyUsedBool[num] == True) and num == keyHit[theNum] and numUsed == 0 and keyDone[theNum] == False and breakTurn == False:
                                    numUsed = 1
                                    keyHit[theNum] += 1
                                    breakTurn = True
                                if key_pressed == True:
                                    if i != keyUsed[number][min(keyHit[theNum], len(keyUsed[theNum])-1)] and breakTurn==False:
                                        keyDone[theNum] = True

                                if num < keyHit[theNum]:
                                    buttonColor = YELLOW
                                    scale = 70
                                elif num == keyHit[theNum] and keyDone[theNum]:
                                    buttonColor = GRAY
                                    scale = 70
                                else:
                                    buttonColor = color[i]
                                    scale = 70
                                drawRect(hud, (buttonColor[0] * 180/255, buttonColor[1] * 180/255, buttonColor[2] * 180/255), (x, y, scale, scale)) # The HPBG one
                                drawRect(hud, (buttonColor), (x + 5, y + 5, scale - 10, scale - 10)) # The MAX HP one
                                #letter= render_text(f'{i.upper()[0]}', BLACK, 60*scale/70)
                                textArrow = loadImg(("textArrow.png", 1, WHITE), angle=angle[i])
                                blitObj(hud, textArrow, x + 35, y + 35)






                        damageControl('Controller')


                    elif int(hudRect[2]) <= 527 and not controllerFound:
                        if attackFade[4] - 20 > 0:
                            attackFade[4] -= 20 * theDelta

                        else:
                            controllerDone = True

                elif supportUsed and not supportDone:
                    if int(hudRect[2]) == 190 and supportFound:

                        attackFade[5] = 255
                        attackMeter = loadImg(('attackDownMeter.png', 0.5))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[3] + hudRect[5]


                        barBlitDown() # Animate the bar moving across the meter

                        damageControl('Support')



                    elif not supportFound:
                        if attackFade[5] - 20 > 0:
                            attackFade[5] -= 20 * theDelta

                            attackMeter = loadImg('attackDownMeter.png')
                            attackMeter.set_alpha(attackFade[5])
                            attackMeter = scaleObj(attackMeter, (0.5, 0.5 * attackFade[5]/255))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            barBlitDown()
                        else:
                            supportDone = True
                            inBar = 0
                            fightFrame = 0

                    elif int(hudRect[2]) != 190 and supportFound:
                        attackFade[5] = max(0, attackFade[5] - 20 * theDelta)
                        attackMeter = loadImg(('attackDownMeter.png', (0.5, 0.5 * (1 - attackFade[5]/255))))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[5])
                        if instantAttack:
                            attackMeter = loadImg(('attackDownMeter.png', 0.5))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            barBlitDown()
                            damageControl('Support')
                            attackFade[5] = 255
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                elif underUsed and not underDone:
                    if int(hudRect[2]) == 190 and underFound:

                        attackFade[6] = 255
                        attackMeter = loadImg(('attackUpMeter.png', 0.5))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[3] + hudRect[5]


                        barBlitUp() # Animate the bar moving across the meter

                        damageControl('Under')



                    elif not underFound:
                        if attackFade[6] - 20 > 0:
                            attackFade[6] -= 20 * theDelta

                            attackMeter = loadImg('attackUpMeter.png')
                            attackMeter.set_alpha(attackFade[6])
                            attackMeter = scaleObj(attackMeter, (0.5, 0.5 * attackFade[6]/255))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            barBlitUp()
                        else:
                            underDone = True
                            inBar = 0
                            fightFrame = 0

                    elif int(hudRect[2]) != 190 and underFound:
                        attackFade[6] = max(0, attackFade[6] - 20 * theDelta)
                        attackMeter = loadImg(('attackUpMeter.png', (0.5, 0.5 * (1 - attackFade[6]/255))))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[6])
                        if instantAttack:
                            attackMeter = loadImg(('attackUpMeter.png', 0.5))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            barBlitUp()
                            damageControl('Under')
                            attackFade[6] = 255
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                elif slamUsed and not slamDone:
                    if int(hudRect[2]) == 527 and slamFound:

                        attackFade[7] = 255
                        attackMeter = loadImg(('attackRightMeter.png', 0.5))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[3] + hudRect[5]


                        slamBarBlit() # Animate the bar moving across the meter

                        damageControl('Slam')



                    elif not slamFound:
                        if attackFade[7] - 20 > 0:
                            attackFade[7] -= 20 * theDelta

                            attackMeter = loadImg('attackRightMeter.png')
                            attackMeter.set_alpha(attackFade[7])
                            attackMeter = scaleObj(attackMeter, (0.5, 0.5 * attackFade[7]/255))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            slamBarBlit()
                        else:
                            slamDone = True
                            inBar = 0
                            fightFrame = 0

                    elif int(hudRect[2]) != 527 and slamFound:
                        attackFade[7] = max(0, attackFade[7] - 20 * theDelta)
                        attackMeter = loadImg(('attackRightMeter.png', (0.5, 0.5 * (1 - attackFade[7]/255))))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[7])
                        if instantAttack:
                            attackMeter = loadImg(('attackRightMeter.png', 0.5))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            slamBarBlit()
                            damageControl('Slam')
                            attackFade[7] = 255
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                elif backUsed and not backDone:
                    if int(hudRect[2]) == 527 and backFound:

                        attackFade[8] = 255
                        attackMeter = loadImg(('attackLeftMeter.png', 0.5))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[3] + hudRect[5]


                        backBarBlit() # Animate the bar moving across the meter

                        damageControl('Back')


                    elif not backFound:
                        if attackFade[8] - 20 > 0:
                            attackFade[8] -= 20 * theDelta

                            attackMeter = loadImg('attackLeftMeter.png')
                            attackMeter.set_alpha(attackFade[8])
                            attackMeter = scaleObj(attackMeter, (0.5, 0.5 * attackFade[8]/255))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            backBarBlit()
                        else:
                            backDone = True
                            inBar = 0
                            fightFrame = 0

                    elif backFound:
                        attackFade[8] = max(0, attackFade[8] - 20 * theDelta)
                        attackMeter = loadImg(('attackLeftMeter.png', (0.5, 0.5 * (1 - attackFade[8]/255))))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[8])
                        if instantAttack:
                            attackMeter = loadImg(('attackLeftMeter.png', 0.5))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            backBarBlit()
                            damageControl('Back')
                            attackFade[8] = 255
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                elif holdUsed and not holdDone:
                    if int(hudRect[2]) == 250 and holdFound:
                        attackMeter = loadImg(('attackHoldMeter.png', 0.25))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255)
                        blitObj(hud, attackMeter, hudRect[0], hudRect[1])

                        attackMeterX = hudRect[2]/2 + hudRect[4]


                        holdBlit() # Animate the bar moving across the meter

                        damageControl('Hold')
                        attackFade[9] = 255


                    elif not holdFound:
                        if attackFade[9] - 20 > 0:
                            attackFade[9] -= 20 * theDelta

                            attackMeter = loadImg('attackHoldMeter.png')
                            attackMeter.set_alpha(attackFade[9])
                            attackMeter = scaleObj(attackMeter, (0.25 * attackFade[9]/255))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            holdBlit()
                        else:
                            holdDone = True
                            inBar = 0
                            fightFrame = 0

                    elif int(hudRect[2]) != 250 and holdFound:
                        attackFade[9] = max(0, attackFade[9] - 20 * theDelta)
                        attackMeter = loadImg(('attackHoldMeter.png', 0.25 * (1 - attackFade[9]/255)))
                        attack_rect = attackMeter.get_rect(center=(hudRect[0], hudRect[1]))
                        attackMeter.set_alpha(255 - attackFade[9])
                        if instantAttack:
                            attackMeter = loadImg(('attackHoldMeter.png', 0.25))
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])
                            holdBlit()
                            damageControl('Hold')
                            attackFade[9] = 255
                        else:
                            blitObj(hud, attackMeter, hudRect[0], hudRect[1])

        if whichTurn: #and abs(hudWidth - hudRect[2]) <= 5:
            stunDone = False
            spareWant = False
            for i in theAlly[selectedWhich].buff:
                if i.doStun == True:
                    actionWhich[selectedWhich] = 'Act'
                    stunDone = True
            if theAlly[selectedWhich].spare >= 100:
                spareWant = True
                actionWhich[selectedWhich] = 'Act'


            if stunDone or spareWant:
                allyTurn = enemyTurn = False
                for num, ally in enumerate(theAlly):
                    if actionWhich[num] == 'Items':
                        itemUsed.append(ally.inventory[whichAction[num]])
                    else:
                        itemUsed.append(None)

                    if actionWhich[num] == 'Act':
                        if stunDone:
                            actUsed.append(character.stunned)
                        elif spareWant:
                            actUsed.append(character.sparing)
                            ##print(True)
                    else:
                        actUsed.append(None)

                    while actionWhich[itemParty] != 'Items' and itemParty < len(theAlly) - 1:
                        itemParty += 1

                    while actionWhich[actParty] != 'Act' and actParty < len(theAlly) - 1:
                        actParty += 1

                    for num, ally in enumerate(theAlly):
                        if actionWhich[num] == 'Skills':
                            skillUsed.append(ally.skills[whichAction[num]])
                        else:
                            skillUsed.append(None)

                        if actionWhich[num] == 'Fight':
                            fightUsed.append(ally.fight[whichAction[num]])
                        else:
                            fightUsed.append(None)

                    while actionWhich[skillParty] != 'Skills' and skillParty < len(theAlly) - 1:
                        skillParty += 1
                continue




            if actionWhich[selectedWhich] == 'inFight':
                fighting = theAlly[selectedWhich].fight[whichAction[selectedWhich]]
                if fighting.range != 'Default':
                    theAlly[selectedWhich].newNum[4] = fighting.range
                if fighting.attack != 'Default':
                    theAlly[selectedWhich].newNum[1] = fighting.attack
                theAlly[selectedWhich].levelUp(0)
            elif theAlly[selectedWhich] == None:
                theAlly[selectedWhich].newNum = copy.copy(theAlly[selectedWhich].setNum)
                theAlly[selectedWhich].levelUp(0)



            if turnAlly:
                currentAlly = theAlly[selectedWhich]  # Selected ally
                allyRange = currentAlly.range  # Assuming each ally has a 'range' attribute

                # Calculate living allies behind the current ally
                livingAlliesBehind = sum(1 for ally in theAlly[selectedWhich + 1:] if ally.hp > 0)

                # Effective range: Ally's range reduced by living allies behind
                effectiveRange = max(0, allyRange - livingAlliesBehind)

                number = 0

                while True:
                    # Calculate dead enemies in front of the current ally that will add to the range
                    deadEnemiesInFront = sum(1 for enemy in theOpponent[:effectiveRange] if enemy.hp <= 0 or enemy.status == 'Spared')

                    effectiveRange = max(0, allyRange - livingAlliesBehind + deadEnemiesInFront)
                    if number == effectiveRange:
                        break
                    number = effectiveRange

                # Wrap back to the furthest valid enemy if out of range or dead
                noValidEnemies = True
            else:
                # Get the current ally and their range
                currentAlly = theAlly[selectedWhich]  # Selected ally
                allyRange = currentAlly.range  # Assuming each ally has a 'range' attribute

                # Calculate living allies behind the current ally
                livingAlliesBehind = 0
                for num, ally in enumerate(theAlly):
                    if num >= selectedWhich:
                        break
                    if ally.hp > 0 and ally.status != 'Spared':
                        livingAlliesBehind += 1
                #print(livingAlliesBehind)
                #livingAlliesBehind = sum(1 for ally in theAlly[::-1][len(theAlly) - selectedWhich:] if ally.hp > 0)

                # Effective range: Ally's range reduced by living allies behind
                effectiveRange = max(0, allyRange - livingAlliesBehind)

                number = 0

                for num, ally in enumerate(theOpponent[::-1][:effectiveRange]):
                    if ally.hp <= 0 or ally.status == 'Spared':
                        #break
                        number += 1
                effectiveRange += number
                        #livingAlliesBehind += 1

                # Wrap back to the furthest valid enemy if out of range or dead
                noValidEnemies = True

            if freeRange:
                effectiveRange = 9999

            if opponentBot and turnEnemy:
                if speedBasedTurn:
                    useItem = False
                    if theAlly[selectedWhich].hp < 0.2*theAlly[selectedWhich].maxhp:
                        itemChance = random.randint(0, 100)
                        if itemChance < 70 and theAlly[selectedWhich].inventory != []:
                            useItem = True
                    useSkill = False
                    if theAlly[selectedWhich].skills != []:
                        for skillNum, i in enumerate(theAlly[selectedWhich].skills):
                            if i.cost <= theAlly[selectedWhich].mana and i.cost != 0:
                                whatSkillUsed = i
                                useSkill = True
                                whichAction[selectedWhich] = skillNum
                                break

                    useAct = False
                    if effectiveRange <= 0:
                        useAct = True
                    #print(f"{theAlly[selectedWhich].name} range is {effectiveRange}")

                    if theAlly[selectedWhich].mana >= 100:
                        useAct = True

                    if not useSkill and not useItem and not useAct:
                        actionWhich[selectedWhich] = 'Fight'
                        if theAlly[selectedWhich].fight != []:
                            whichAction[selectedWhich] = random.randint( 0, len(theAlly[selectedWhich].fight) - 1 )
                            theAlly[selectedWhich].tempClass = theAlly[selectedEnemy].fight[whichAction[selectedWhich]].classType
                            fighting = theAlly[selectedWhich].fight[whichAction[selectedWhich]]
                            if fighting.range != 'Default':
                                theAlly[selectedWhich].newNum[4] = fighting.range
                            if fighting.attack != 'Default':
                                theAlly[selectedWhich].newNum[1] = fighting.attack
                            theAlly[selectedWhich].levelUp(0)

                        else:
                            theAlly[selectedWhich].tempClass = theAlly[selectedWhich].classes

                        #whichSelection[selectedWhich] = random.randint(0, len(party) - 1)
                        #while theOpponent[whichSelection[selectedWhich]].hp <= 0:
                                #whichSelection[selectedWhich] = random.randint(0, len(party) - 1)
                        whichSelection[selectedWhich] = len(theOpponent) - 1
                        while whichSelection[selectedWhich] > 0 and theOpponent[whichSelection[selectedWhich]].hp <= 0:
                            whichSelection[selectedWhich] -= 1
                    elif useItem:
                        actionWhich[selectedWhich] = 'Items'
                        whichAction[selectedWhich] = random.randint(0, len(theAlly[selectedWhich].inventory)-1)
                        whichSelection[selectedWhich] = theAlly.index(theAlly[selectedWhich])
                    elif useAct:
                        actionWhich[selectedWhich] = 'Act'
                        if theAlly[selectedWhich].mana >= 100:
                            whichAction[selectedWhich] = 4
                        else:
                            whichAction[selectedWhich] = 1
                        whichSelection[selectedWhich] = theAlly.index(theAlly[selectedWhich])
                    elif useSkill:
                        if 'everyone' in whatSkillUsed.type:
                            targetting = theAlly + theOpponent
                        elif 'ally' in whatSkillUsed.type:
                            targetting = theAlly
                        else:
                            targetting = theOpponent
                        actionWhich[selectedWhich] = 'Skills'
                        if whatSkillUsed.targetType == 'All':
                            whichSelection[selectedWhich] = []
                            for number in range(0, len(targetting)):
                                 whichSelection[selectedWhich].append(number)
                        elif whatSkillUsed.targetType == 'Multiple':
                            whichSelection[selectedWhich] = []
                            for number in range(0, min(len(targetting), whatSkillUsed.targetAmount)):
                                 if targetting[number].hp > 0:
                                     whichSelection[selectedWhich].append(number)
                        elif whatSkillUsed.targetType == 'Self':
                            actionWhich[selectedWhich] = 'Skills'
                            #whichAction[selectedWhich] = 1
                            whichSelection[selectedWhich] = theAlly.index(theAlly[selectedWhich])
                        else:
                            if 'everyone' in whatSkillUsed.type:
                                targetting = theAlly + theOpponent
                            elif 'ally' in whatSkillUsed.type:
                                targetting = theAlly
                            else:
                                targetting = theOpponent
                            newTarget = []
                            for i in targetting:
                                if i.hp > 0:
                                    newTarget.append(i)
                            highestAttack = newTarget[0]
                            for i in newTarget:
                                if highestAttack.attack < i.attack:
                                    highestAttack = i
                            whichSelection[selectedWhich] = targetting.index(highestAttack)
                            #while theOpponent[whichSelection[selectedWhich]].hp <= 0:
                                #whichSelection[selectedWhich] = random.randint(0, len(party) - 1)
                    selectedWhich += 1

                    if speedNum != selectedWhich and speedBasedTurn:
                        speedNum = selectedWhich
                        allyTurn = enemyTurn = False
                        battleSplash = False
                        for num, i in enumerate(actionWhich):
                            if i == None:
                                actionWhich[num] = 'Done'

                else:
                    for num, i in enumerate(actionWhich):
                        #if i == None:
                        actionWhich[num] = 'Fight'
                        if theAlly[num].fight != []:
                            whichAction[num] = random.randint( 0, len(theAlly[num].fight) - 1 )
                            theAlly[num].tempClass = theAlly[num].fight[whichAction[num]].classType
                            ##print(theAlly[num].fight[whichAction[num]].name)
                        else:
                            theAlly[num].tempClass = theAlly[num].classes

                    selectedEnemy = len(theAlly) - 1
                       #whichSelection[num] = random.randint(0, len(theOpponent) - 1)

                    #whichSelection = speedNum = len(theAlly) - 1
                    allyTurn = enemyTurn = False
                    battleSplash = False
                    #selectedEnemy = speedNum


                addInBar()
                itemUsed = []
                skillUsed = []
                fightUsed = []
                actUsed = []
                actParty = 0
                itemParty = 0
                skillParty = 0
                #for num in range( 0, len(whichAction) ):
                    #whichAction[num] = 0


                for num, ally in enumerate(theAlly):
                    if actionWhich[num] == 'Items':
                        itemUsed.append(ally.inventory[whichAction[num]])
                    else:
                        itemUsed.append(None)

                    if actionWhich[num] == 'Act':
                        actUsed.append(ally.action[whichAction[num]])
                    else:
                        actUsed.append(None)

                while actionWhich[itemParty] != 'Items' and itemParty < len(theAlly) - 1:
                    itemParty += 1

                while actionWhich[actParty] != 'Act' and actParty < len(theAlly) - 1:
                    actParty += 1

                for num, ally in enumerate(theAlly):
                    if actionWhich[num] == 'Skills':
                        skillUsed.append(ally.skills[whichAction[num]])
                    else:
                        skillUsed.append(None)

                    if actionWhich[num] == 'Fight':
                        fightUsed.append(ally.fight[whichAction[num]])
                    else:
                        fightUsed.append(None)

                while actionWhich[skillParty] != 'Skills' and skillParty < len(theAlly) - 1:
                    skillParty += 1
            #elif theAlly[selectedWhich].hp <= 0:
                #resetAllyTurn()

            else:
                if leftPressed:
                    #if isinstance(whichSelection[selectedWhich], list):
                    #    whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect]
                    #else:
                    #    whichSelection[selectedWhich] = len(theOpponent) - 1 - whichSelection[selectedWhich]
                    if actionWhich[selectedWhich] == 'chooseFightTarget':  # Check if the current action is aiming in a fight
                        # Move selection to the left (previous enemy)
                        whichSelection[selectedWhich] -= 1
                        if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                            whichSelection[selectedWhich] = len(theOpponent) - 1

                        if turnAlly:
                            while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                whichSelection[selectedWhich] -= 1
                                if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                                    whichSelection[selectedWhich] = len(theOpponent) - 1
                        else:
                            #if whichSelection[selectedWhich] >= len(theOpponent) - 1:
                                #whichSelection[selectedWhich] = 0
                            while theOpponent[whichSelection[selectedWhich]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                whichSelection[selectedWhich] += 1
                                if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the first enemy
                                    whichSelection[selectedWhich] = 0

                        # Check if a valid enemy was found
                        if theOpponent[whichSelection[selectedWhich]].hp > 0 and whichSelection[selectedWhich] < effectiveRange:
                            noValidEnemies = False

                        #if noValidEnemies:
                            #print("No valid enemies to target")

                    elif actionWhich[selectedWhich] == 'inFight':
                        whichAction[selectedWhich] -= 1
                        if whichAction[selectedWhich] < 0:
                            whichAction[selectedWhich] = len(theAlly[selectedWhich].fight) - 1
                        hudRect[0] = width/2 - 50


                    elif actionWhich[selectedWhich] == 'inItem':
                        whichAction[selectedWhich] -= 1
                        if whichAction[selectedWhich] < 0:
                            whichAction[selectedWhich] = len(theAlly[selectedWhich].inventory) - 1
                        hudRect[0] = width/2 - 50

                    elif actionWhich[selectedWhich] == 'inDebug':
                        whichAction[selectedWhich] -= 1
                        if whichAction[selectedWhich] < 0:
                            whichAction[selectedWhich] = len(character.debug) - 1
                        hudRect[0] = width/2 - 50

                    elif actionWhich[selectedWhich] == 'inSkill':
                        whichAction[selectedWhich] -= 1
                        if whichAction[selectedWhich] < 0:
                            whichAction[selectedWhich] = len(theAlly[selectedWhich].skills) - 1
                        hudRect[0] = width/2 - 50

                    elif actionWhich[selectedWhich] == 'inAct':
                        whichAction[selectedWhich] -= 1
                        if whichAction[selectedWhich] < 0:
                            whichAction[selectedWhich] = len(theAlly[selectedWhich].action) - 1
                        hudRect[0] = width/2 - 50

                    elif actionWhich[selectedWhich] == 'chooseItemTarget':
                        if 'ally' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].type:
                            whichOne = theAlly
                        elif 'opponent' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].type:
                            whichOne = theOpponent
                        else:
                            whichOne = theAlly + theOpponent

                        if 'Multiple' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                            whichSelection[selectedWhich][multiSelect] -= 1
                            if whichSelection[selectedWhich][multiSelect] < 0:
                                whichSelection[selectedWhich][multiSelect] = len(whichOne) - 1
                            for i in whichSelection[selectedWhich][:multiSelect]:
                                while whichSelection[selectedWhich][multiSelect] == i:
                                    whichSelection[selectedWhich][multiSelect] -= 1
                                    if whichSelection[selectedWhich][multiSelect] < 0:
                                        whichSelection[selectedWhich][multiSelect] = len(whichOne) - 1

                            if whichOne == theOpponent:

                                if turnAlly:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                                else:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theOpponent):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0
                            elif whichOne == theAlly and not 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:

                                if turnAlly:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= 99:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                                else:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theAlly) - 1 - whichSelection[selectedWhich][multiSelect] >= 99:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theAlly):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0

                        else:
                            whichSelection[selectedWhich] -= 1
                            if whichSelection[selectedWhich] < 0:
                                whichSelection[selectedWhich] = len(whichOne) - 1

                            while whichOne[whichSelection[selectedWhich]].hp > 0 and 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                    whichSelection[selectedWhich] -= 1
                                    if whichSelection[selectedWhich] < 0:
                                        whichSelection[selectedWhich] = len(whichOne) - 1

                            if whichOne == theOpponent:
                                if turnAlly:
                                    while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = len(theOpponent) - 1
                                else:
                                    while theOpponent[whichSelection[selectedWhich]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = 0
                            elif whichOne == theAlly and not 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                if turnAlly:
                                    while theAlly[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = len(theAlly) - 1
                                else:
                                    while theAlly[whichSelection[selectedWhich]].hp <= 0 or len(theAlly) - 1 - whichSelection[selectedWhich] >= 99:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theAlly):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = 0


                    elif actionWhich[selectedWhich] == 'chooseDebugTarget':
                        whichSelection[selectedWhich] -= 1
                        if whichSelection[selectedWhich] < 0:
                            whichSelection[selectedWhich] = len(party + opponent) - 1

                    elif actionWhich[selectedWhich] == 'chooseActTarget':
                        items = theAlly[selectedWhich].action[whichAction[selectedWhich]]
                        whichOne = theOpponent if 'opponent' in items.useOn else theAlly
                        whichSelection[selectedWhich] -= 1
                        if whichSelection[selectedWhich] < 0:
                            whichSelection[selectedWhich] = len(whichOne) - 1

                        canTargetDead = items.canTargetDead
                        if items.considerRange == True:
                            if items.range != None:
                                effectiveRange = items.range
                        else:
                            effectiveRange = 999

                        if turnAlly:
                            while (not canTargetDead and whichOne[whichSelection[selectedWhich]].hp <= 0) or whichSelection[selectedWhich] >= effectiveRange:
                                whichSelection[selectedWhich] -= 1
                                if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                                    whichSelection[selectedWhich] = len(whichOne) - 1
                        else:
                            while (not canTargetDead and whichOne[whichSelection[selectedWhich]].hp <= 0) or len(whichOne) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                whichSelection[selectedWhich] += 1
                                if whichSelection[selectedWhich] >= len(whichOne):  # Wrap around to the first enemy
                                    whichSelection[selectedWhich] = 0

                    elif actionWhich[selectedWhich] == 'chooseSkillTarget':
                        if 'ally' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                            whichOne = theAlly
                        elif 'opponent' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                            whichOne = theOpponent
                        else:
                            whichOne = theAlly + theOpponent

                        if 'Multiple' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType:
                            whichSelection[selectedWhich][multiSelect] -= 1
                            if whichSelection[selectedWhich][multiSelect] < 0:
                                whichSelection[selectedWhich][multiSelect] = len(whichOne) - 1
                            for i in whichSelection[selectedWhich][:multiSelect]:
                                while whichSelection[selectedWhich][multiSelect] == i:
                                    whichSelection[selectedWhich][multiSelect] -= 1
                                    if whichSelection[selectedWhich][multiSelect] < 0:
                                        whichSelection[selectedWhich][multiSelect] = len(whichOne) - 1

                            if whichOne == theOpponent:
                                if turnAlly:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                                else:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theOpponent):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0
                            elif whichOne == theAlly:
                                if turnAlly:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theAlly) - 1
                                else:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theAlly) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theAlly):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0

                        else:
                            whichSelection[selectedWhich] -= 1
                            if whichSelection[selectedWhich] < 0:
                                whichSelection[selectedWhich] = len(whichOne) - 1

                            if whichOne == theOpponent:
                                if turnAlly:
                                    #print(whichSelection[selectedWhich])
                                    while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = 0
                                else:
                                    #whichSelection[selectedWhich] = len(theOpponent) - 1
                                    while theOpponent[whichSelection[selectedWhich]].hp < 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = len(theOpponent) - 1
                            elif whichOne == theAlly:
                                if turnAlly:
                                    #print(whichSelection[selectedWhich])
                                    while theAlly[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] < 0:  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = len(theAlly) - 1
                                else:
                                    #whichSelection[selectedWhich] = len(theAlly) - 1
                                    while theAlly[whichSelection[selectedWhich]].hp < 0 or len(theAlly) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theAlly):  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = 0

                    else:
                        selectedAction -= 1
                        if selectedAction < 0:
                            selectedAction = len(actions) - 1

                    playSound('Select_sfx.ogg', 0.9)

                if rightPressed:
                    if actionWhich[selectedWhich] == 'chooseFightTarget':  # Check if the current action is aiming in a fight
                        # Move selection to the right (next enemy)
                        whichSelection[selectedWhich] += 1
                        if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the first enemy
                            whichSelection[selectedWhich] = 0

                        if turnAlly:
                            while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                whichSelection[selectedWhich] += 1
                                if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the first enemy
                                    whichSelection[selectedWhich] = 0
                        else:
                            while theOpponent[whichSelection[selectedWhich]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                whichSelection[selectedWhich] -= 1
                                if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                                    whichSelection[selectedWhich] = len(theOpponent) - 1

                        # Check if a valid enemy was found
                        if theOpponent[whichSelection[selectedWhich]].hp > 0 and whichSelection[selectedWhich] < effectiveRange:
                            noValidEnemies = False

                        #if noValidEnemies:
                            #print("No valid enemies to target")

                    elif actionWhich[selectedWhich] == 'inFight':
                        whichAction[selectedWhich] += 1
                        if whichAction[selectedWhich] > len(theAlly[selectedWhich].fight) - 1:
                            whichAction[selectedWhich] = 0
                        hudRect[0] = width/2 + 50


                    elif actionWhich[selectedWhich] == 'inItem':
                        whichAction[selectedWhich] += 1
                        if whichAction[selectedWhich] > len(theAlly[selectedWhich].inventory) - 1:
                            whichAction[selectedWhich] = 0
                        hudRect[0] = width/2 + 50

                    elif actionWhich[selectedWhich] == 'inDebug':
                        whichAction[selectedWhich] += 1
                        if whichAction[selectedWhich] > len(character.debug) - 1:
                            whichAction[selectedWhich] = 0
                        hudRect[0] = width/2 + 50


                    elif actionWhich[selectedWhich] == 'inSkill':
                        whichAction[selectedWhich] += 1
                        if whichAction[selectedWhich] > len(theAlly[selectedWhich].skills) - 1:
                            whichAction[selectedWhich] = 0
                        hudRect[0] = width/2 + 50

                    elif actionWhich[selectedWhich] == 'inAct':
                        whichAction[selectedWhich] += 1
                        if whichAction[selectedWhich] > len(theAlly[selectedWhich].action) - 1:
                            whichAction[selectedWhich] = 0
                        hudRect[0] = width/2 + 50

                    elif actionWhich[selectedWhich] == 'chooseItemTarget':
                        if 'ally' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].type:
                            whichOne = theAlly
                        elif 'opponent' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].type:
                            whichOne = theOpponent
                        else:
                            whichOne = theAlly + theOpponent

                        if 'Multiple' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                            whichSelection[selectedWhich][multiSelect] += 1
                            if whichSelection[selectedWhich][multiSelect] > len(whichOne) - 1:
                                whichSelection[selectedWhich][multiSelect] = 0
                            for i in whichSelection[selectedWhich][:multiSelect]:
                                while whichSelection[selectedWhich][multiSelect] == i:
                                    whichSelection[selectedWhich][multiSelect] += 1
                                    if whichSelection[selectedWhich][multiSelect] > len(whichOne) - 1:
                                        whichSelection[selectedWhich][multiSelect] = 0

                            if whichOne == theOpponent:
                                if turnAlly:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theOpponent):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0
                                else:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                            elif whichOne == theAlly:
                                if turnAlly:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= 99:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theAlly):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0
                                else:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theAlly) - 1 - whichSelection[selectedWhich][multiSelect] >= 99:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theAlly) - 1


                        else:
                            whichSelection[selectedWhich] += 1
                            if whichSelection[selectedWhich] > len(whichOne) - 1:
                                whichSelection[selectedWhich] = 0

                            while whichOne[whichSelection[selectedWhich]].hp > 0 and 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                whichSelection[selectedWhich] += 1
                                if whichSelection[selectedWhich] > len(whichOne) - 1:
                                    whichSelection[selectedWhich] = 0

                            if whichOne == theOpponent:
                                if turnAlly:
                                    #print(whichSelection[selectedWhich])
                                    while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = 0
                                else:
                                    whichSelection[selectedWhich] = len(theOpponent) - 1
                                    while theOpponent[whichSelection[selectedWhich]].hp < 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = len(theOpponent) - 1
                            elif not 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                if turnAlly:
                                    #print(whichSelection[selectedWhich])
                                    while theAlly[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theAlly):  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = 0
                                else:
                                    #whichSelection[selectedWhich] = len(theAlly) - 1
                                    while theAlly[whichSelection[selectedWhich]].hp < 0 or len(theAlly) - 1 - whichSelection[selectedWhich] >= 99:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = len(theAlly) - 1

                    elif actionWhich[selectedWhich] == 'chooseDebugTarget':
                        whichSelection[selectedWhich] += 1
                        if whichSelection[selectedWhich] > len(party + opponent) - 1:
                            whichSelection[selectedWhich] = 0

                    elif actionWhich[selectedWhich] == 'chooseActTarget':
                        items = theAlly[selectedWhich].action[whichAction[selectedWhich]]
                        whichOne = theOpponent if 'opponent' in items.useOn else theAlly
                        whichSelection[selectedWhich] += 1
                        if whichSelection[selectedWhich] > len(whichOne) - 1:
                            whichSelection[selectedWhich] = 0

                        canTargetDead = items.canTargetDead
                        if items.considerRange == True:
                            if items.range != None:
                                effectiveRange = items.range
                        else:
                            effectiveRange = 999

                        if turnAlly:
                            while (not canTargetDead and whichOne[whichSelection[selectedWhich]].hp <= 0) or whichSelection[selectedWhich] >= 99:
                                whichSelection[selectedWhich] += 1
                                if whichSelection[selectedWhich] >= len(whichOne):  # Wrap around to the first enemy
                                    whichSelection[selectedWhich] = 0
                        else:
                            while (not canTargetDead and whichOne[whichSelection[selectedWhich]].hp <= 0) or len(whichOne) - 1 - whichSelection[selectedWhich] >= 99:
                                whichSelection[selectedWhich] -= 1
                                if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                                    whichSelection[selectedWhich] = len(whichOne) - 1

                    elif actionWhich[selectedWhich] == 'chooseSkillTarget':
                        if 'ally' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                            whichOne = theAlly
                        elif 'opponent' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                            whichOne = theOpponent
                        else:
                            whichOne = theAlly + theOpponent

                        if 'Multiple' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType:
                            whichSelection[selectedWhich][multiSelect] += 1
                            if whichSelection[selectedWhich][multiSelect] > len(whichOne) - 1:
                                whichSelection[selectedWhich][multiSelect] = 0
                            for i in whichSelection[selectedWhich][:multiSelect]:
                                while whichSelection[selectedWhich][multiSelect] == i:
                                    whichSelection[selectedWhich][multiSelect] += 1
                                    if whichSelection[selectedWhich][multiSelect] > len(whichOne) - 1:
                                        whichSelection[selectedWhich][multiSelect] = 0

                            if whichOne == theOpponent:
                                if turnAlly:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theOpponent):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0
                                else:
                                    while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                            elif whichOne == theAlly:
                                if turnAlly:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] += 1
                                        if whichSelection[selectedWhich][multiSelect] >= len(theAlly):  # Wrap around to the first enemy
                                            whichSelection[selectedWhich][multiSelect] = 0
                                else:
                                    while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theAlly) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                        whichSelection[selectedWhich][multiSelect] -= 1
                                        if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                            whichSelection[selectedWhich][multiSelect] = len(theAlly) - 1


                        else:
                            whichSelection[selectedWhich] += 1
                            if whichSelection[selectedWhich] > len(whichOne) - 1:
                                whichSelection[selectedWhich] = 0

                            if whichOne == theOpponent:
                                if turnAlly:
                                    #print(whichSelection[selectedWhich])
                                    while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = 0
                                else:
                                    #whichSelection[selectedWhich] = len(theOpponent) - 1
                                    while theOpponent[whichSelection[selectedWhich]].hp < 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = len(theOpponent) - 1
                            elif whichOne == theAlly:
                                if turnAlly:
                                    #print(whichSelection[selectedWhich])
                                    while theAlly[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theAlly):  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = 0
                                else:
                                    #whichSelection[selectedWhich] = len(theAlly) - 1
                                    while theAlly[whichSelection[selectedWhich]].hp < 0 or len(theAlly) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = len(theAlly) - 1

                    else:
                        selectedAction += 1
                        if selectedAction > len(actions) - 1:
                            selectedAction = 0

                    playSound('Select_sfx.ogg', 0.9)

                if upPressed:
                    pass
                if downPressed:
                    pass

                if confirm:
                    if actionWhich[selectedWhich] == None:
                        if actions[selectedAction] == 'Fight':
                            if theAlly[selectedWhich].fight == []:
                                splashText(None, True, 0)
                                actionWhich[selectedWhich] = 'chooseFightTarget'
                                theAlly[selectedWhich].tempClass = theAlly[selectedWhich].classes
                                if turnAlly:
                                    print(whichSelection[selectedWhich])
                                    while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] += 1
                                        if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                            whichSelection[selectedWhich] = 0
                                else:
                                    while theOpponent[whichSelection[selectedWhich]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                        whichSelection[selectedWhich] -= 1
                                        if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                            whichSelection[selectedWhich] = len(theOpponent) - 1

                                # Check if a valid enemy was found
                                if theOpponent[whichSelection[selectedWhich]].hp > 0 and whichSelection[selectedWhich] < effectiveRange:
                                    noValidEnemies = False

                                #if noValidEnemies:
                                    #print("No valid enemies to target")
                            else:
                                actionWhich[selectedWhich] = 'inFight'
                                splashText('', False, 0)


                        if actions[selectedAction] == 'Skills':
                            if theAlly[selectedWhich].skills != []:
                                actionWhich[selectedWhich] = 'inSkill'
                                splashText('', False, 0)
                            else:
                                screenText.append(['This rumbler does not have an active skill.', theAlly[selectedWhich].color, 0, False])

                        elif actions[selectedAction] == 'Act':
                            actionWhich[selectedWhich] = 'inAct'
                            splashText('', False, 0)


                        elif actions[selectedAction] == 'Items' and len(theAlly[selectedWhich].inventory) > 0:
                            actionWhich[selectedWhich] = 'inItem'
                            splashText('', False, 0)

                        elif actions[selectedAction] == 'Debug':
                            actionWhich[selectedWhich] = 'inDebug'
                            splashText('', False, 0)


                    elif actionWhich[selectedWhich] == 'chooseFightTarget':
                        if effectiveRange > 0:
                            actionWhich[selectedWhich] = 'Fight'
                            splashText(None, True, 0)
                            selectedWhich += 1

                    elif actionWhich[selectedWhich] == 'inFight':
                        if effectiveRange <= 0:
                            playSound('cannot.ogg')
                            screenText.append([f'All the enemies are out of {theAlly[selectedWhich].name} range.', RED, 0, False])
                        else:
                            splashText(None, True, 0)
                            theAlly[selectedWhich].tempClass = theAlly[selectedWhich].fight[whichAction[selectedWhich]].classType
                            actionWhich[selectedWhich] = 'chooseFightTarget'
                            if turnAlly:
                                #print(whichSelection[selectedWhich])
                                while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                    whichSelection[selectedWhich] += 1
                                    if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                        whichSelection[selectedWhich] = 0
                            else:
                                whichSelection[selectedWhich] = len(theOpponent) - 1
                                while theOpponent[whichSelection[selectedWhich]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                    whichSelection[selectedWhich] -= 1
                                    if whichSelection[selectedWhich] < 0:  # Wrap around to the last enemy
                                        whichSelection[selectedWhich] = len(theOpponent) - 1
                                    if whichSelection[selectedWhich] == len(theOpponent) - 1:
                                        print(effectiveRange, len(theOpponent) - 1 - whichSelection[selectedWhich])
                                        break

                            # Check if a valid enemy was found
                            if theOpponent[whichSelection[selectedWhich]].hp > 0 and whichSelection[selectedWhich] < effectiveRange:
                                noValidEnemies = False

                            #if noValidEnemies:
                                #print("No valid enemies to target")

                    elif actionWhich[selectedWhich] == 'inSkill':
                        checkEnergy = energyTrans + energyGain
                        if usingEnergy < theAlly[selectedWhich].skills[whichAction[selectedWhich]].cost:
                            playSound('cannot.ogg')
                            screenText.append(['NOT ENOUGH AP!!!', RED, 0, False])
                            pass
                        else:

                            if 'ally' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                                whichOne = theAlly
                            elif 'opponent' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                                whichOne = theOpponent
                            else:
                                whichOne = theAlly + theOpponent

                            if 'Multiple' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType:
                                number = theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetAmount
                                #while str(number) not in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                                    #number += 1
                                if number >= len(whichOne):

                                    actionWhich[selectedWhich] = 'Skills'
                                    splashText(None, True, 0)
                                    skillUsed[selectedWhich] = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                                    energyGain -= (theAlly[selectedWhich].skills[whichAction[selectedWhich]].cost)
                                    whichSelection[selectedWhich] = []
                                    for i in range(0, len(whichOne)):
                                        whichSelection[selectedWhich].append(i)
                                    selectedWhich += 1
                                else:
                                    if not isinstance(whichSelection[selectedWhich], list):
                                        whichSelection[selectedWhich] = [0]
                                    actionWhich[selectedWhich] = 'chooseSkillTarget'
                                    splashText('', False, 0)
                                    if whichOne == theOpponent:
                                        if turnAlly:
                                            while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                                whichSelection[selectedWhich][multiSelect] += 1
                                                if whichSelection[selectedWhich][multiSelect] >= len(theOpponent):  # Wrap around to the first enemy
                                                    whichSelection[selectedWhich][multiSelect] = 0
                                        else:
                                            whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                                            while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                                whichSelection[selectedWhich][multiSelect] -= 1
                                                if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                                    whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                                    elif whichOne == theAlly:
                                        if turnAlly:
                                            while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                                whichSelection[selectedWhich][multiSelect] += 1
                                                if whichSelection[selectedWhich][multiSelect] >= len(theAlly):  # Wrap around to the first enemy
                                                    whichSelection[selectedWhich][multiSelect] = 0
                                        else:
                                            whichSelection[selectedWhich][multiSelect] = len(theAlly) - 1
                                            while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theAlly) - 1 - whichSelection[selectedWhich][multiSelect] >= effectiveRange:
                                                whichSelection[selectedWhich][multiSelect] -= 1
                                                if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                                    whichSelection[selectedWhich][multiSelect] = len(theAlly) - 1

                            elif len(theAlly) == 1 and whichOne == theAlly:
                                actionWhich[selectedWhich] = 'Skills'
                                splashText(None, True, 0)
                                skillUsed[selectedWhich] = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                                energyGain -= (theAlly[selectedWhich].skills[whichAction[selectedWhich]].cost)
                                selectedWhich += 1

                            elif 'Self' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType:
                                actionWhich[selectedWhich] = 'Skills'
                                whichSelection[selectedWhich] = selectedWhich
                                splashText(None, True, 0)
                                skillUsed[selectedWhich] = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                                energyGain -= (theAlly[selectedWhich].skills[whichAction[selectedWhich]].cost)
                                selectedWhich += 1

                            elif 'All' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType:
                                actionWhich[selectedWhich] = 'Skills'
                                splashText(None, True, 0)
                                skillUsed[selectedWhich] = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                                energyGain -= (theAlly[selectedWhich].skills[whichAction[selectedWhich]].cost)
                                whichSelection[selectedWhich] = []
                                for i in range(0, len(whichOne)):
                                    whichSelection[selectedWhich].append(i)
                                selectedWhich += 1

                            else:
                                actionWhich[selectedWhich] = 'chooseSkillTarget'
                                splashText('', False, 0)
                                if whichOne == theOpponent:
                                    if turnAlly:
                                        #print(whichSelection[selectedWhich])
                                        while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                            whichSelection[selectedWhich] += 1
                                            if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                                whichSelection[selectedWhich] = 0
                                    else:
                                        whichSelection[selectedWhich] = len(theOpponent) - 1
                                        while theOpponent[whichSelection[selectedWhich]].hp < 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                            whichSelection[selectedWhich] -= 1
                                            if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                                whichSelection[selectedWhich] = len(theOpponent) - 1
                                elif whichOne == theAlly:
                                    if turnAlly:
                                        #print(whichSelection[selectedWhich])
                                        effectiveRange = theAlly[whichSelection[selectedWhich]].range
                                        while theAlly[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                            whichSelection[selectedWhich] += 1
                                            if whichSelection[selectedWhich] >= len(theAlly):  # Wrap around to the last enemy
                                                whichSelection[selectedWhich] = 0
                                    else:
                                        whichSelection[selectedWhich] = len(theAlly) - 1
                                        while theAlly[whichSelection[selectedWhich]].hp < 0 or len(theAlly) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                            whichSelection[selectedWhich] -= 1
                                            if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                                whichSelection[selectedWhich] = len(theAlly) - 1



                    elif actionWhich[selectedWhich] == 'chooseSkillTarget':
                        if 'Multiple' not in theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetType:
                            actionWhich[selectedWhich] = 'Skills'

                            splashText(None, True, 0)
                            skillUsed[selectedWhich] = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                            energyGain -= (theAlly[selectedWhich].skills[whichAction[selectedWhich]].cost)
                            selectedWhich += 1
                        else:
                            if 'ally' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                                whichOne = theAlly
                            elif 'opponent' in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                                whichOne = theOpponent
                            else:
                                whichOne = theAlly + theOpponent
                            if not isinstance(whichSelection[selectedWhich], list):
                                whichSelection[selectedWhich] = []
                            number = theAlly[selectedWhich].skills[whichAction[selectedWhich]].targetAmount
                            multiSelect += 1
                            #while str(number) not in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                                #number += 1
                            if len(whichSelection[selectedWhich]) < number:
                                x = 0
                                while x in whichSelection[selectedWhich]:
                                    x += 1
                                    if x > len(whichOne):
                                        x = 0
                                whichSelection[selectedWhich].append(x)
                            else:
                                actionWhich[selectedWhich] = 'Skills'
                                multiSelect = 0
                                splashText(None, True, 0)
                                skillUsed[selectedWhich] = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                                energyGain -= (theAlly[selectedWhich].skills[whichAction[selectedWhich]].cost)
                                selectedWhich += 1



                    elif actionWhich[selectedWhich] == 'inItem':
                        if 'ally' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].type:
                            whichOne = theAlly
                        elif 'opponent' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].type:
                            whichOne = theOpponent
                        else:
                            whichOne = theAlly + theOpponent

                        noDeadAlly = True
                        for i in whichOne:
                            if i.hp <= 0:
                                noDeadAlly = False
                                break
                        if 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType and noDeadAlly:
                            playSound('cannot.ogg')
                            screenText.append(['No Dead Rumblers.', RED, 0, False])
                            pass
                        elif 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType and intenseMode:
                            playSound('cannot.ogg')
                            screenText.append(['The Item cannot be used...', RED, 0, False])
                            pass
                        else:

                            if 'Multiple' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                number = theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetAmount
                                #while str(number) not in theAlly[selectedWhich].skills[whichAction[selectedWhich]].type:
                                    #number += 1
                                if number >= len(whichOne):

                                    actionWhich[selectedWhich] = 'Items'
                                    splashText(None, True, 0)
                                    skillUsed[selectedWhich] = theAlly[selectedWhich].inventory[whichAction[selectedWhich]]
                                    #energyGain -= (theAlly[selectedWhich].inventory[whichAction[selectedWhich]].cost)
                                    whichSelection[selectedWhich] = []
                                    for i in range(0, len(whichOne)):
                                        whichSelection[selectedWhich].append(i)
                                    selectedWhich += 1
                                else:
                                    if not isinstance(whichSelection[selectedWhich], list):
                                        whichSelection[selectedWhich] = [0]
                                    actionWhich[selectedWhich] = 'chooseItemTarget'
                                    splashText('', False, 0)
                                    if whichOne == theOpponent:
                                        if turnAlly:
                                            while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                                whichSelection[selectedWhich][multiSelect] += 1
                                                if whichSelection[selectedWhich][multiSelect] >= len(theOpponent):  # Wrap around to the first enemy
                                                    whichSelection[selectedWhich][multiSelect] = 0
                                        else:
                                            whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                                            while theOpponent[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich][multiSelect] >= 99:
                                                whichSelection[selectedWhich][multiSelect] -= 1
                                                if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                                    whichSelection[selectedWhich][multiSelect] = len(theOpponent) - 1
                                    elif whichOne == theAlly:
                                        if turnAlly:
                                            while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                                whichSelection[selectedWhich][multiSelect] += 1
                                                if whichSelection[selectedWhich][multiSelect] >= len(theAlly):  # Wrap around to the first enemy
                                                    whichSelection[selectedWhich][multiSelect] = 0
                                        else:
                                            whichSelection[selectedWhich][multiSelect] = len(theAlly) - 1
                                            while theAlly[whichSelection[selectedWhich][multiSelect]].hp <= 0 or len(theAlly) - 1 - whichSelection[selectedWhich][multiSelect] >= 99:
                                                whichSelection[selectedWhich][multiSelect] -= 1
                                                if whichSelection[selectedWhich][multiSelect] < 0:  # Wrap around to the last enemy
                                                    whichSelection[selectedWhich][multiSelect] = len(theAlly) - 1

                            elif len(theAlly) == 1 and whichOne == theAlly:
                                actionWhich[selectedWhich] = 'Items'
                                splashText(None, True, 0)
                                skillUsed[selectedWhich] = theAlly[selectedWhich].inventory[whichAction[selectedWhich]]
                                #energyGain -= (theAlly[selectedWhich].inventory[whichAction[selectedWhich]].cost)
                                selectedWhich += 1

                            elif 'Self' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                actionWhich[selectedWhich] = 'Items'
                                whichSelection[selectedWhich] = selectedWhich
                                splashText(None, True, 0)
                                skillUsed[selectedWhich] = theAlly[selectedWhich].inventory[whichAction[selectedWhich]]
                                #energyGain -= (theAlly[selectedWhich].inventory[whichAction[selectedWhich]].cost)
                                selectedWhich += 1

                            elif 'All' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                actionWhich[selectedWhich] = 'Items'
                                splashText(None, True, 0)
                                skillUsed[selectedWhich] = theAlly[selectedWhich].inventory[whichAction[selectedWhich]]
                                #energyGain -= (theAlly[selectedWhich].inventory[whichAction[selectedWhich]].cost)
                                whichSelection[selectedWhich] = []
                                for i in range(0, len(whichOne)):
                                    whichSelection[selectedWhich].append(i)
                                selectedWhich += 1

                            elif 'Dead' in theAlly[selectedWhich].inventory[whichAction[selectedWhich]].targetType:
                                actionWhich[selectedWhich] = 'chooseItemTarget'
                                splashText('', False, 0)
                                while whichOne[whichSelection[selectedWhich]].hp > 0:
                                    whichSelection[selectedWhich] += 1
                            else:
                                actionWhich[selectedWhich] = 'chooseItemTarget'
                                splashText('', False, 0)
                                if whichOne == theOpponent:
                                    if turnAlly:
                                        #print(whichSelection[selectedWhich])
                                        while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= effectiveRange:
                                            whichSelection[selectedWhich] += 1
                                            if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                                whichSelection[selectedWhich] = 0
                                    else:
                                        whichSelection[selectedWhich] = len(theOpponent) - 1
                                        while theOpponent[whichSelection[selectedWhich]].hp < 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= effectiveRange:
                                            whichSelection[selectedWhich] -= 1
                                            if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                                whichSelection[selectedWhich] = len(theOpponent) - 1
                                else:
                                    if turnAlly:
                                        #print(whichSelection[selectedWhich])
                                        while theAlly[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                            whichSelection[selectedWhich] += 1
                                            if whichSelection[selectedWhich] >= len(theAlly):  # Wrap around to the last enemy
                                                whichSelection[selectedWhich] = 0
                                    else:
                                        whichSelection[selectedWhich] = len(theAlly) - 1
                                        while theAlly[whichSelection[selectedWhich]].hp < 0 or len(theAlly) - 1 - whichSelection[selectedWhich] >= 99:
                                            whichSelection[selectedWhich] -= 1
                                            if whichSelection[selectedWhich] <= 0:  # Wrap around to the first enemy
                                                whichSelection[selectedWhich] = len(theAlly) - 1

                    elif actionWhich[selectedWhich] == 'inDebug':
                        actionWhich[selectedWhich] = 'chooseDebugTarget'
                        splashText('', False, 0)

                    elif actionWhich[selectedWhich] == 'inAct':
                        #global energyGain
                        checkEnergy = energyTrans + energyGain
                        if usingEnergy < -1*theAlly[selectedWhich].action[whichAction[selectedWhich]].energyPoints:
                            playSound('cannot.ogg')
                            screenText.append(['NOT ENOUGH AP!!!', RED, 0, False])
                            pass
                        elif checkEnergy < -1*theAlly[selectedWhich].action[whichAction[selectedWhich]].superPoints:
                            playSound('cannot.ogg')
                            #energyGain -= theAlly[selectedWhich].action[whichAction[selectedWhich]].superPoints
                            screenText.append(['NOT ENOUGH SP!!!', RED, 0, False])
                            pass
                        elif len(theAlly) == 1 and 'ally' in theAlly[selectedWhich].action[whichAction[selectedWhich]].useOn:
                            pass

                        elif 'self' in theAlly[selectedWhich].action[whichAction[selectedWhich]].useOn:
                            actionWhich[selectedWhich] = 'Act'
                            whichSelection[selectedWhich] = selectedWhich
                            splashText(None, True, 0)
                            energyGain += theAlly[selectedWhich].action[whichAction[selectedWhich]].superPoints
                            selectedWhich += 1

                        else:
                            actionWhich[selectedWhich] = 'chooseActTarget'
                            splashText('', False, 0)
                            energyGain += theAlly[selectedWhich].action[whichAction[selectedWhich]].superPoints
                            if turnAlly:
                                #print(whichSelection[selectedWhich])
                                while theOpponent[whichSelection[selectedWhich]].hp <= 0 or whichSelection[selectedWhich] >= 99:
                                    whichSelection[selectedWhich] += 1
                                    if whichSelection[selectedWhich] >= len(theOpponent):  # Wrap around to the last enemy
                                        whichSelection[selectedWhich] = 0
                            else:
                                whichSelection[selectedWhich] = len(theOpponent) - 1
                                while theOpponent[whichSelection[selectedWhich]].hp <= 0 or len(theOpponent) - 1 - whichSelection[selectedWhich] >= 99:
                                    whichSelection[selectedWhich] -= 1
                                    if whichSelection[selectedWhich] < 0:  # Wrap around to the first enemy
                                        whichSelection[selectedWhich] = len(theOpponent) - 1

                    elif actionWhich[selectedWhich] == 'chooseItemTarget':
                        actionWhich[selectedWhich] = 'Items'
                        splashText(None, True, 0)
                        selectedWhich += 1


                    elif actionWhich[selectedWhich] == 'chooseActTarget':
                        actionWhich[selectedWhich] = 'Act'
                        splashText(None, True, 0)
                        energyGain += (theAlly[selectedWhich].action[whichAction[selectedWhich]].energyPoints)
                        selectedWhich += 1

                    elif actionWhich[selectedWhich] == 'chooseDebugTarget':
                        whichOne = party + opponent
                        character.debug[whichAction[selectedWhich]].use(whichOne[whichSelection[selectedWhich]])

                    if speedNum != selectedWhich and speedBasedTurn:
                        speedNum = selectedWhich
                        allyTurn = enemyTurn = False
                        battleSplash = False
                        for num, i in enumerate(actionWhich):
                            if i == None:
                                actionWhich[num] = 'Done'

                    elif speedNum != selectedWhich:
                        if allyTurn:
                            selectedAlly = selectedWhich
                        elif enemyTurn:
                            selectedEnemy = selectedWhich

                        speedNum = selectedWhich

                    playSound('Confirm_sfx.ogg')

                if cancel and whichTurn:
                    if selectedWhich >= len(theAlly):
                        pass
                    elif actionWhich[selectedWhich] in ['chooseFightTarget', 'inItem', 'inAct', 'inSkill', 'inMercy', 'inFight', 'inDebug']:
                        actionWhich[selectedWhich] = None
                        whichSelection[selectedWhich] = 0
                        whichAction[selectedWhich] = 0
                        multiSelect = 0
                        splashText(None, True, 0)

                    elif actionWhich[selectedWhich] in ['chooseItemTarget']:
                        actionWhich[selectedWhich] = 'inItem'
                        whichSelection[selectedWhich] = 0

                    elif actionWhich[selectedWhich] in ['chooseActTarget']:
                        actionWhich[selectedWhich] = 'inAct'
                        whichSelection[selectedWhich] = 0

                    elif actionWhich[selectedWhich] in ['chooseSkillTarget']:
                        actionWhich[selectedWhich] = 'inSkill'
                        whichSelection[selectedWhich] = 0
                        multiSelect = 0

                    elif actionWhich[selectedWhich] in ['chooseDebugTarget']:
                        actionWhich[selectedWhich] = 'inDebug'
                        whichSelection[selectedWhich] = 0
                        multiSelect = 0

                    elif selectedWhich > 0 and speedBasedTurn == False:
                        started = False
                        while theAlly[selectedWhich].hp < 0 or not started:
                            started = True
                            if turnEnemy:
                                selectedEnemy -= 1
                            else:
                                selectedAlly -= 1
                            selectedWhich -= 1
                        if skillUsed[selectedWhich] != 0 and actionWhich[selectedWhich] == 'Skills':
                            energyGain += skillUsed[selectedWhich].cost
                            skillUsed[selectedWhich] = 0
                        if actionWhich[selectedWhich] == 'Act':
                            energyGain -= (theAlly[selectedWhich].action[whichAction[selectedWhich]].energyPoints)
                        actionWhich[selectedWhich] = None
                        whichSelection[selectedWhich] = 0
                        whichAction[selectedWhich] = 0
                        multiSelect = 0

                if selectedWhich >= len(theAlly):
                   # #print(True)
                    allyTurn = enemyTurn = False
                    selectedWhich = len(theAlly) - 1
                    if turnAlly:
                        selectedAlly = len(theAlly) - 1
                    elif turnEnemy:
                        selectedEnemy = len(theAlly) - 1
                    battleSplash = False

                if cancel and theAlly[selectedWhich].hp <= 0:
                    while theAlly[selectedWhich].hp <= 0:
                        if turnEnemy:
                            selectedEnemy -= 1
                        else:
                            selectedAlly -= 1
                        selectedWhich -= 1


                if battleSplash and theAlly[selectedWhich].hp > 0:
                    with open(f'data/dialogue/{theAlly[selectedWhich].dataName}.txt', 'r') as file:
                            code = file.read()
                    diction = eval(code)
                    if not useCustomDialogue:
                        if actionWhich[selectedWhich] == 'chooseFightTarget':
                            if splashy in ['None', '']:
                                splashy = '* '+random.choice(diction['attack'])
                        else:
                            if splashy in ['None', '']:
                                splashy = '* '+random.choice(diction['idle'])
                            if turn <= len(turnDialogue):
                                if splashy[2:] in turnDialogue[turn-1][1]:
                                    splashy = '* '+random.choice(diction['idle'])
                    if useCustomDialogue:
                        splashText('* ' + inTurnText[1], True, text_index)
                        battleText(True, inTurnText[0], emotion=inTurnText[2])
                    else:
                        splashText(splashy, True, text_index)
                        battleText(True, theAlly[selectedWhich].displayName)


                if not (allyTurn or enemyTurn):
                    addInBar()
                    itemUsed = []
                    skillUsed = []
                    actUsed = []
                    actParty = 0
                    itemParty = 0
                    skillParty = 0


                    for num, ally in enumerate(theAlly):
                        if actionWhich[num] == 'Items':
                            itemUsed.append(ally.inventory[whichAction[num]])
                        else:
                            itemUsed.append(None)

                        if actionWhich[num] == 'Act':
                            actUsed.append(ally.action[whichAction[num]])
                        else:
                            actUsed.append(None)

                    while actionWhich[itemParty] != 'Items' and itemParty < len(theAlly) - 1:
                        itemParty += 1

                    while actionWhich[actParty] != 'Act' and actParty < len(theAlly) - 1:
                        actParty += 1

                    for num, ally in enumerate(theAlly):
                        if actionWhich[num] == 'Skills':
                            skillUsed.append(ally.skills[whichAction[num]])
                        else:
                            skillUsed.append(None)

                        if actionWhich[num] == 'Fight':
                            fightUsed.append(ally.fight[whichAction[num]])
                        else:
                            fightUsed.append(None)

                    while actionWhich[skillParty] != 'Skills' and skillParty < len(theAlly) - 1:
                        skillParty += 1


                if actionWhich[selectedWhich] == 'inFight':
                    fight = theAlly[selectedWhich].fight[whichAction[selectedWhich]]
                    skillText = render_text(f'* {fight.name}', WHITE, 40)
                    blitObj(hud, skillText, hudRect[4] + 20, hudRect[5] + 18, 'topleft')

                    numScroll = render_text(f'<{whichAction[selectedWhich]+1}/{len(theAlly[selectedWhich].fight)}>', WHITE, 40)
                    blitObj(hud, numScroll, hudRect[4] + hudRect[2] - 150, hudRect[5] + 18, 'midtop')

                    scrolly = loadImg(("scroll.png", 0.2, color[selectedWhich]))
                    blitObj(hud, scrolly, hudRect[4] + hudRect[2] - 220, hudRect[5] + 14, 'topleft')

                    text_offset = addBattleText(fight.info, 40, 410)

                    furtherInfo = fight.infoClass

                    statChangeText = render_text(furtherInfo, CYAN, 40)

                    blitObj(hud, statChangeText, hudRect[4] + 20, text_offset + 38, 'topleft')

                elif actionWhich[selectedWhich] == 'chooseFightTarget':

                    theSelectHud()

                elif actionWhich[selectedWhich] == 'inSkill':
                    skill = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                    skillText = render_text(f'* {skill.name}', WHITE, 40)
                    blitObj(hud, skillText, hudRect[4] + 20, hudRect[5] + 18, 'topleft')

                    numScroll = render_text(f'<{whichAction[selectedWhich]+1}/{len(theAlly[selectedWhich].skills)}>', WHITE, 40)
                    blitObj(hud, numScroll, hudRect[4] + hudRect[2] - 150, hudRect[5] + 18, 'midtop')

                    scrolly = loadImg(("scroll.png", 0.2, color[selectedWhich]))
                    blitObj(hud, scrolly, hudRect[4] + hudRect[2] - 220, hudRect[5] + 14, 'topleft')

                    text_offset = addBattleText(skill.info, 40, 410)

                    furtherInfo = ''
                    skillColor = WHITE

                    if 'ally' in skill.type:
                        if 'atk' in skill.type or 'def' in skill.type:
                            furtherInfo = 'Type: Stat Boost'
                            skillColor = CYAN

                        if 'hp' in skill.type:
                            furtherInfo = 'Type: Healing'
                            skillColor = GREEN

                        if ('atk' in skill.type or 'def' in skill.type) and 'hp' in skill.type:
                            furtherInfo = 'Type: Stat Boost, Healing'
                            skillColor = PURPLE

                    elif 'opponent' in skill.type:
                        if 'atk' in skill.type or 'def' in skill.type:
                            furtherInfo = 'Type: Stat Debuff'
                            skillColor = BLUE

                        if 'hp' in skill.type:
                            furtherInfo = 'Type: Offense'
                            skillColor = RED

                        if ('atk' in skill.type or 'def' in skill.type) and 'hp' in skill.type:
                            furtherInfo = 'Type: Stat Debuff, Offense'
                            skillColor = ORANGE

                    statChangeText = render_text(furtherInfo, skillColor, 40)

                    blitObj(hud, statChangeText, hudRect[4] + 20, text_offset + 38, 'topleft')

                    cost = render_text(f'{skill.cost}% AP', CYAN, 45)
                    blitObj(hud, cost, hudRect[4] + hudRect[2] - 130, text_offset + 38, 'topleft')

                elif actionWhich[selectedWhich] == 'chooseSkillTarget':
                    textBox = 0
                    items = theAlly[selectedWhich].skills[whichAction[selectedWhich]]
                    if 'opponent' in items.type:
                        if 'Multiple' in items.targetType:
                            x = 500/len(theOpponent) + 1000/len(theOpponent) * whichSelection[selectedWhich][multiSelect]
                            showingEnemy = theOpponent[whichSelection[selectedWhich][multiSelect]]
                        else:
                            x = 500/len(theOpponent) + 1000/len(theOpponent) * whichSelection[selectedWhich]
                            showingEnemy = theOpponent[whichSelection[selectedWhich]]

                        theSelectHud()
                        #showingEnemy = theOpponent[whichSelection[selectedWhich]]

                        # Render info text
                        infoText = render_text(f'{theAlly[selectedWhich].name} prepares to target {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])
                    elif 'ally' in items.type:
                        if 'Multiple' in items.targetType:
                            x = 500/len(theAlly) + 1000/len(theOpponent) * whichSelection[selectedWhich][multiSelect]
                            showingEnemy = theAlly[whichSelection[selectedWhich][multiSelect]]
                        else:
                            x = 500/len(theAlly) + 1000/len(theAlly) * whichSelection[selectedWhich]
                            showingEnemy = theAlly[whichSelection[selectedWhich]]

                        theSelectHud(useAlly=True)
                        #showingEnemy = theAlly[whichSelection[selectedWhich]]

                        # Render info text
                        infoText = render_text(f'{theAlly[selectedWhich].name} prepares to target {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])
                    else:
                        bothParty = theAlly + theOpponent
                        bothColor = colorOfAlly + colorOfEnemy
                        if 'Multiple' in items.targetType:
                            x = 500/len(theAlly) + 1000/len(theOpponent) * whichSelection[selectedWhich][multiSelect]
                            showingEnemy = bothParty[whichSelection[selectedWhich][multiSelect]]
                        else:
                            x = 500/len(theAlly) + 1000/len(theAlly) * whichSelection[selectedWhich]
                            showingEnemy = bothParty[whichSelection[selectedWhich]]

                        theSelectHud(useBoth=True)
                        #showingEnemy = bothParty[whichSelection[selectedWhich]]

                        # Render info text
                        infoText = render_text(f'{bothParty[selectedWhich].name} prepares to target {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])


                elif actionWhich[selectedWhich] == 'inAct':
                    items = theAlly[selectedWhich].action[whichAction[selectedWhich]]
                    itemText = render_text(f'* {items.name}', WHITE, 40)
                    itemRect = (hudRect[4] + 20, hudRect[5] + 18)
                    blitObj(hud, itemText, hudRect[4] + 20, hudRect[5] + 18, 'topleft')

                    numScroll = render_text(f'<{whichAction[selectedWhich]+1}/{len(theAlly[selectedWhich].action)}>', WHITE, 40)
                    numRect = numScroll.get_rect(midtop = (hudRect[4] + hudRect[2] - 150, hudRect[5] + 18))
                    blitObj(hud, numScroll, hudRect[4] + hudRect[2] - 150, hudRect[5] + 18, 'midtop')

                    scrolly = loadImg(("scroll.png", 0.2, color[selectedWhich]))
                    scrollRect = (hudRect[4] + hudRect[2] - 220, hudRect[5] + 14)
                    blitObj(hud, scrolly, hudRect[4] + hudRect[2] - 220, hudRect[5] + 14, 'topleft')

                    text_offset = addBattleText(items.desc, 40, 410)

                    addInfo = ''
                    if items.energyPoints != 0:
                        if items.energyPoints >= 0:
                            statChangeText = render_text(f'+{items.energyPoints}% AP', CYAN, 40)
                        else:
                            statChangeText = render_text(f'Cost: {abs(items.energyPoints)}% AP', CYAN, 40)

                        statRect = (hudRect[4] + 20, text_offset + 38)
                        blitObj(hud, statChangeText, hudRect[4] + 20, text_offset + 38, 'topleft')
                    if items.superPoints < 0:
                        statChangeText = render_text(f'Cost: {abs(items.superPoints)}% SP', RED, 40)

                        statRect = (hudRect[4] + 20, text_offset + 38)
                        blitObj(hud, statChangeText, hudRect[4] + 20, text_offset + 38, 'topleft')

                elif actionWhich[selectedWhich] == 'inDebug':
                    items = character.debug[whichAction[selectedWhich]]
                    itemText = render_text(f'* {items.name}', WHITE, 40)
                    itemRect = (hudRect[4] + 20, hudRect[5] + 18)
                    blitObj(hud, itemText, hudRect[4] + 20, hudRect[5] + 18, 'topleft')

                    numScroll = render_text(f'<{whichAction[selectedWhich]+1}/{len(character.debug)}>', WHITE, 40)
                    numRect = numScroll.get_rect(midtop = (hudRect[4] + hudRect[2] - 150, hudRect[5] + 18))
                    blitObj(hud, numScroll, hudRect[4] + hudRect[2] - 150, hudRect[5] + 18, 'midtop')

                    scrolly = loadImg(("scroll.png", 0.2, color[selectedWhich]))
                    scrollRect = (hudRect[4] + hudRect[2] - 220, hudRect[5] + 14)
                    blitObj(hud, scrolly, hudRect[4] + hudRect[2] - 220, hudRect[5] + 14, 'topleft')

                    text_offset = addBattleText(items.info, 40, 410)

                    addInfo = ''



                elif actionWhich[selectedWhich] == 'chooseActTarget':
                    items = theAlly[selectedWhich].action[whichAction[selectedWhich]]
                    if 'opponent' in items.useOn:
                        theSelectHud()
                        showingEnemy = theOpponent[whichSelection[selectedWhich]]

                         #Render info text
                        infoText = render_text(f'{theAlly[selectedWhich].name} will use it on {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])
                    else:
                        theSelectHud(useAlly=True)
                        showingEnemy = theAlly[whichSelection[selectedWhich]]

                         #Render info text
                        infoText = render_text(f'{theAlly[selectedWhich].name} will use it on {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])

                elif actionWhich[selectedWhich] == 'chooseDebugTarget':
                    bothSide = party + opponent
                    items = character.debug[whichAction[selectedWhich]]
                    theSelectHud(useBoth=True)
                    showingEnemy = bothSide[whichSelection[selectedWhich]]

                     #Render info text
                    infoText = render_text(f'{theAlly[selectedWhich].name} will use it on {showingEnemy.name}', WHITE, 45)
                    infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                    blitObj(hud, infoText, hudRect[0], hudRect[1])

                elif actionWhich[selectedWhich] == 'inItem':
                    items = theAlly[selectedWhich].inventory[whichAction[selectedWhich]]
                    itemText = render_text(f'* {items.name}', WHITE, 40)
                    blitObj(hud, itemText, hudRect[4] + 20, hudRect[5] + 18, 'topleft')

                    numScroll = render_text(f'<{whichAction[selectedWhich]+1}/{len(theAlly[selectedWhich].inventory)}>', WHITE, 40)
                    blitObj(hud, numScroll, hudRect[4] + hudRect[2] - 150, hudRect[5] + 18, 'midtop')

                    scrolly = loadImg(("scroll.png", 0.2, color[selectedWhich]))
                    blitObj(hud, scrolly, hudRect[4] + hudRect[2] - 220, hudRect[5] + 14, 'topleft')

                    text_offset = addBattleText(items.info, 40, 410)

                    furtherInfo = ''
                    skillColor = WHITE


                    if 'Weapon' in items.type:
                        #weaponType = items.type.replace('Weapon', '').capitalize()
                        statChangeText = render_text(f'Weapon: {items.num}ATK', YELLOW, 40)

                    elif 'Armour' in items.type:
                        statChangeText = render_text(f'Armour: {items.num}DEF', CYAN, 40)

                    else:
                        modifierStat = '[white]Item:[/white] '
                        if 'opponent' in items.type:
                            if 'hp' in items.type and items.num < 0:
                                modifierStat += f'[green]+{abs(items.num)}HP[/green] '
                            elif 'hp' in items.type:
                                modifierStat += f'[red]-{abs(items.num)}HP[/red] '
                        else:
                            if 'hp' in items.type and items.num > 0:
                                modifierStat += f'[green]+{abs(items.num)}HP[/green] '
                            elif 'hp' in items.type:
                                modifierStat += f'[red]-{abs(items.num)}HP[/red] '

                        if items.num < 0:
                            sign = '-'
                        elif items.num > 0:
                            sign = '+'
                        if 'atk' in items.type:
                            modifierStat += f'[red]{sign}{abs(items.num)}ATK[/red] '
                        if 'def' in items.type:
                            modifierStat += f'[blue]{sign}{abs(items.num)}DEF[/blue] '
                        if 'spd' in items.type:
                            modifierStat += f'[yellow]{sign}{abs(items.num)}SPD[/yellow] '
                        if 'prod' in items.type:
                            modifierStat += f'[purple]{sign}{abs(items.num)}PRD[/purple] '
                        if 'rge' in items.type:
                            modifierStat += f'[orange]{sign}{abs(items.num)}RGE[/orange] '
                        if 'maxhp' in items.type:
                            modifierStat += f'[cyan]{sign}{abs(items.num)}MAXHP[/cyan] '
                        if 'canRevive' in items.type:
                            modifierStat += f'[cyan]Reviving[/cyan] '


                        statChangeText = render_text(modifierStat, WHITE, 40)

                    statRect = (hudRect[4] + 20, text_offset + 38)
                    blitObj(hud, statChangeText, hudRect[4] + 20, text_offset + 38, 'topleft')

                elif actionWhich[selectedWhich] == 'chooseItemTarget':
                    items = theAlly[selectedWhich].inventory[whichAction[selectedWhich]]
                    if 'opponent' in items.type:
                        if 'Multiple' in items.targetType:
                            x = 500/len(theOpponent) + 1000/len(theOpponent) * whichSelection[selectedWhich][multiSelect]
                            showingEnemy = theOpponent[whichSelection[selectedWhich][multiSelect]]
                        else:
                            x = 500/len(theOpponent) + 1000/len(theOpponent) * whichSelection[selectedWhich]
                            showingEnemy = theOpponent[whichSelection[selectedWhich]]

                        theSelectHud()
                        #showingEnemy = theOpponent[whichSelection[selectedWhich]]

                        # Render info text
                        infoText = render_text(f'{theAlly[selectedWhich].name} prepares to target {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])
                    elif 'ally' in items.type:
                        if 'Multiple' in items.targetType:
                            x = 500/len(theAlly) + 1000/len(theOpponent) * whichSelection[selectedWhich][multiSelect]
                            showingEnemy = theAlly[whichSelection[selectedWhich][multiSelect]]
                        else:
                            x = 500/len(theAlly) + 1000/len(theAlly) * whichSelection[selectedWhich]
                            showingEnemy = theAlly[whichSelection[selectedWhich]]

                        theSelectHud(useAlly=True)
                        #showingEnemy = theAlly[whichSelection[selectedWhich]]

                        # Render info text
                        infoText = render_text(f'{theAlly[selectedWhich].name} prepares to target {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])
                    else:
                        bothParty = theAlly + theOpponent
                        bothColor = colorOfAlly + colorOfEnemy
                        if 'Multiple' in items.targetType:
                            x = 500/len(theAlly) + 1000/len(theOpponent) * whichSelection[selectedWhich][multiSelect]
                            showingEnemy = bothParty[whichSelection[selectedWhich][multiSelect]]
                        else:
                            x = 500/len(theAlly) + 1000/len(theAlly) * whichSelection[selectedWhich]
                            showingEnemy = bothParty[whichSelection[selectedWhich]]

                        theSelectHud(useBoth=True)
                        #showingEnemy = bothParty[whichSelection[selectedWhich]]

                        # Render info text
                        infoText = render_text(f'{bothParty[selectedWhich].name} prepares to target {showingEnemy.name}', WHITE, 45)
                        infoText_rect = infoText.get_rect(center=(hudRect[0], hudRect[1] - 20))
                        blitObj(hud, infoText, hudRect[0], hudRect[1])

def buildEnemyList(validEnemy, desired_length):
    #validEnemy = character.validEnemy
    if desired_length > len(validEnemy):
        raise ValueError("Requested list length exceeds number of unique valid enemies.")

    selected_enemies = []               # The grand list we’re building
    used_enemies = set()               # Track used enemies by identity (we’ll use id or name)

    for index in range(desired_length):
        # First, filter out enemies that haven't been used AND whose range is greater than current index

        eligible = [
            enemy for enemy in validEnemy
            if enemy.name not in used_enemies and enemy.range > index
        ]

        if not eligible:
            print(f"{eligible}, No eligible enemy found for position {index}. Aborting with partial list.")
            break

        # Sort eligible enemies by how close their range is to the current index
        eligible.sort(key=lambda enemy: enemy.range - index)

        # Prioritize the closest match (i.e., range just barely greater than index)
        # To keep it spicy, we can randomly pick from the top 3 closest matches, if there are that many
        top_choices = eligible[:3] if len(eligible) >= 3 else eligible
        chosen = random.choice(top_choices)

        selected_enemies.append(chosen)
        used_enemies.add(chosen.name)

        #print(f"Position {index}: Added {chosen}")

    return selected_enemies

validAlly, validEnemy = character.validAlly, character.validEnemy
character.li_wei.levelUp(0)
character.li_wei.hpSet()

#screenWindow.botPlay.boolean = True
#main([character.allerwave], validEnemy, useSpeedTurn=False, battleData='Endless')
#speedBasedTurn = False
#character.blue_guyEn.level = 100
#character.rayson.newNum[0] = 9999
#character.rayson.setNum[0] = 9999
#asyncio.run(battleRun())
while 1==0:
    screenWindow.sprites.clear()
    screenWindow.animatedSprites.clear()
    effects = {}
    for num, i in enumerate(validAlly + validEnemy):
        i.levelUp(0)
        for buff in i.passiveBuff:
            effects[buff.name] = buff
    theAllies = copy.deepcopy(validAlly)
    theEnemies = copy.deepcopy(validEnemy)

    main([character.li_wei], buildEnemyList(validEnemy, 5), useSpeedTurn=True)
    character.li_wei.armour = character.helmet
    character.li_wei.weapon = character.sword
    useDefensePercent = False
    useDodgeEquation = True
    useExtraDialogue = False

    hud.start_fade(BLACK, 255, 1)
    screen.start_fade(BLACK, 255, 1)
    screenWindow.backGroundScreen.start_fade(BLACK, 255, 1)
    hud.camera_zoom = 3
    screen.camera_zoom = 3
    screenWindow.backGroundScreen.camera_zoom = 3
    asyncio.run(battleRun())


    for num, i in enumerate(validAlly):
        validAlly[num] = theAllies[num]

    for num, i in enumerate(validEnemy):
        validEnemy[num] = theEnemies[num]

    for num, i in enumerate(validAlly + validEnemy):
        passiveBuff = {}
        for buff in i.passiveBuff:
            passiveBuff[effects[buff.name]] = [False, False]
        i.passiveBuff = passiveBuff
