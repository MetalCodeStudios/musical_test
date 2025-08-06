# Import essential things
import random
import json
# Import essential things
import random
import json
import os
import sys
import pygame
import pygame.gfxdraw
import math
from screenWindow import Button, DynamicMusicPlayer, sprites, loadSprite, draw, updateTween, loadAnimatedSprite, animatedSprites, updateAnimation, playAnimation, scaleFactor
import screenWindow
import reworkingBattle
import character
import string
import io
import copy
import asyncio
from character import playerObj

#import platform

#import battle
theDelta = screenWindow.deltaTime
# Starts up the "game" window
pygame.init()
# Starts up the audio system

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

width = screenWindow.width
height = screenWindow.height

widthy = width #640
heighty = 700 #448

drawRect, drawRing, drawCircle = screenWindow.drawRect, screenWindow.drawRing, screenWindow.drawCircle
scaleObj = screenWindow.scaleObj
loadImg = screenWindow.loadImg
render_text = screenWindow.render_text
rotateObj = screenWindow.rotateObj
blitObj = screenWindow.blitObj

screen = screenWindow.screen
window = screenWindow.window
hud = screenWindow.hud
backGroundScreen = screenWindow.backGroundScreen
ringThing = pygame.Surface((width,height), pygame.SRCALPHA)

# Camera Settings
camZoom = screenWindow.camZoom
camColor = screenWindow.camColor # For the color of Camera Flash
camShake = screenWindow.camShake # To shake the game itself, 0 means no shaking camera
camFade = screenWindow.camFade # For Camera Flash and how long it takes for Camera Flash to fade away

soundVolume = screenWindow.soundVolume # Dictates Sound Volume
musicVolume = screenWindow.musicVolume # Dictates Music Volume

images = screenWindow.images
texts = screenWindow.texts


party = character.party
opponent = character.opponent

clock = screenWindow.clock #Starts up the FPS

trigger = screenWindow.trigger

def getScript(filename):
    # If running as a bundled executable, find files in the PyInstaller temp folder
    if getattr(sys, 'frozen', False):
        # `sys._MEIPASS` is the temp folder created by PyInstaller
        base_path = sys._MEIPASS
    else:
        # For regular script execution
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, filename)

def getCode(name):
    # Get the full path to Battle.py
    scriptPath = getScript(name)

    # Read the script content
    with open(scriptPath, "r") as f:
        code = f.read()

    # Execute the script
    return code

def scaleObj(object, scale):
    x = object.get_width()
    y = object.get_height()
    if isinstance(scale, tuple) and len(scale) == 2:
        return pygame.transform.smoothscale(object, (abs(scale[0]) * x, abs(scale[1]) * y))
    else:
        return pygame.transform.smoothscale(object, (abs(scale) * x, abs(scale) * y))

loadImg, render_text = screenWindow.loadImg, screenWindow.render_text

# Function to play sound
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

def screenBlit(finalscreen): # Function to blit the screen

    global width, height, renderTexture
    width, height = screenWindow.width, screenWindow.height
    #deltaTime = clock.get_time() / 1000
    backGroundScreen.update(theDelta)
    screen.update(theDelta)
    hud.update(theDelta)

    backGroundScreen.render_to(window)
    screen.render_to(window)
    hud.render_to(window)
    if not screenWindow.useWeb:
        screenWindow.renderer.present()
        screenWindow.renderer.clear()
    pygame.display.flip()

surfaceCache = {}
def loadSurface(width, height):
    key = (width, height)
    if key not in surfaceCache:
        print(1)
        surfaceCache[key] = pygame.Surface((max(width*scaleFactor, 1), max(height*scaleFactor, 1)), pygame.SRCALPHA)
    surfaceCache[key].fill((0, 0, 0, 0))
    return surfaceCache[key]
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

def blit_text(surface, text, rect, fontName, size, color):
    """
    Renders and blits text onto a surface within a rectangular boundary.

    Args:
        surface (pygame.Surface): The surface to draw the text on.
        text (str): The text to render.
        rect (pygame.Rect): The rectangular area where the text should be displayed.
        font (pygame.font.Font): The font used to render the text.
        color (tuple): The color of the text.
    """
    font = pygame.font.Font(fontName, int(size*0.9)) # Loads in a font with specified size
    words = text.split(' ')  # Split text into words
    x, y = rect.topleft
    line_spacing = font.size('Tg')[1] + 2  # Line height including spacing
    space_width = font.size(' ')[0]  # Width of a space

    line = []
    for word in words:
        #print(word)
        # Check the width of the current line with the new word added
        test_line = ' '.join(line + [word])
        test_line_width, _ = font.size(test_line)

        if test_line_width + x - rect.x > rect.width or word == '\n':
            # Render the current line
            line_surface = render_text(' '.join(line), color, size)
            text_rect = line_surface.get_rect(center=(x + rect.width/2, y))
            blitObj(surface, line_surface, x + rect.width/2, y)
            #surface.blit(line_surface, text_rect)
            if word != "\n":
                line = [word]  # Start a new line
            else:
                line = []
            y += line_spacing  # Move to the next line

            # Check if text exceeds vertical boundary
            #if y + line_spacing > rect.bottom:
                #break  # Stop adding lines if out of vertical space
        else:
            line.append(word)  # Add word to the current line

    # Render the last line
    if line:
        line_surface = render_text(' '.join(line), color, size)
        text_rect = line_surface.get_rect(center=(x + rect.width/2, y))
        #surface.blit(line_surface, text_rect)
        blitObj(surface, line_surface, x + rect.width/2, y)
    return y - 2*line_spacing

def buildEnemyList(validEnemy, desired_length):
    validEnemy = copy.copy(validEnemy)
    random.shuffle(validEnemy)
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
        for num, i in enumerate(eligible):
            if i.classes == 'Challenge':
                chance = random.randint(1, 100)
                if chance > 1:
                    #print(chance, i.name)
                    del eligible[num]



        if not eligible:
            print(f"No eligible enemy found for position {index}. Aborting with partial list.")
            break

        # Sort eligible enemies by how close their range is to the current index
        eligible.sort(key=lambda enemy: enemy.range - index)

        # Prioritize the closest match (i.e., range just barely greater than index)
        # To keep it spicy, we can randomly pick from the top 3 closest matches, if there are that many
        top_choices = eligible[:3] if len(eligible) >= 3 else eligible
        chosen = random.choice(top_choices)

        selected_enemies.append(chosen)
        used_enemies.add(chosen.name)

    for i in selected_enemies:
        if random.randint(1,5) == 1:
            i.skin = random.choice(i.skinList)

        #print(f"Position {index}: Added {chosen}")

    return selected_enemies

mouseHover, mouseTouch = screenWindow.mouseHover, screenWindow.mouseTouch



fullscreen = screenWindow.fullscreen
inGame = True
fullscreen = True
frame = 0
validAlly = character.validAlly
validEnemy = character.validEnemy
party = [None, None, None, None, None]
mouseScroll = 0
partySelect = 0

selectionSprite = {}

selectedAlly = 0

inSkinSelect = False

skinSelect = 0

skinList = [0, 0, 0, 0, 0]

skinListEn = [0, 0, 0, 0, 0]

partyIndex = 0

option = 0

inOption = False

interrupt = False

debugMode = False

modifyStat = False
inControl = False
inSetting = False
startBattle = False

whichBase = 0

controlVar = screenWindow.controlVar
controlNum = 0
inCharSelect = False
setting = False

mouseHold = False
mouseDown = False
mouseTimer = 0
hud = screenWindow.hud
if not screenWindow.useWeb:
    music = DynamicMusicPlayer(f"sounds/music/menuMusic.ogg", loop=True)
    music.set_speed(0.9)
#else:


for i in validEnemy + validAlly:
    i.levelUp(0)

audio = None
if sys.platform == "emscripten":
    from js import document
    audio = document.getElementById("bgmusic")

##import os
##
##def rename_png_extensions(root_folder):
##    """
##    Walk through the root_folder and rename all files ending with '.PNG' to '.png'.
##    This is case-sensitive and only affects '.PNG' exactly as written.
##    """
##
##    print(f"Starting recursive traversal in: {root_folder}")
##
##    # Walk through every directory and file under root_folder
##    for dirpath, dirnames, filenames in os.walk(root_folder):
##        print(f"Checking directory: {dirpath}")
##
##        for filename in filenames:
##            # Check if the file ends exactly with '.PNG' (uppercase)
##            if filename.endswith('.PNG'):
##                old_path = os.path.join(dirpath, filename)
##                # Create a new filename with the .png extension instead
##                new_filename = filename[:-4] + '.png'
##                new_path = os.path.join(dirpath, new_filename)
##
##                # Sanity check: avoid overwriting existing files
##                if os.path.exists(new_path) and 1==0:
##                    print(f"WARNING: {new_path} already exists. Skipping to avoid overwrite.")
##                    continue
##
##                # Rename the file
##                try:
##                    os.rename(old_path, new_path)
##                    print(f"Renamed: {old_path} → {new_path}")
##                except Exception as e:
##                    print(f"ERROR renaming {old_path}: {e}")
##
##    print("Renaming complete. All .PNG files should now be .png.")
##
### You can hardcode this or take input from the user
##target_folder = 'sprites'
##
### Check if the folder exists
##if not os.path.isdir(target_folder):
##    print(f"ERROR: The directory '{target_folder}' does not exist. Please check the path.")
##else:
##    rename_png_extensions(target_folder)


##import os
##from PIL import Image
##
### Define your sprites directory
##SPRITES_DIR = "sprites"
##
### Supported image formats (you can add more if needed)
##IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
##
### Scale factor (0.5x for reducing to half size)
##SCALE_FACTOR = 0.5
##
### Whether to overwrite the original files or not
##OVERWRITE = True  # Set this to False if you want to save scaled images elsewhere
##OUTPUT_DIR = "scaled_sprites"  # Used only if OVERWRITE is False
##
##
##def scale_image(image_path, scale_factor=0.5, save_path=None):
##    """
##    Scales an image by the given scale factor and saves it to the save_path.
##    If save_path is None, overwrites the original image.
##    """
##    try:
##        with Image.open(image_path) as img:
##            original_size = img.size
##            new_width = int(original_size[0] * scale_factor)
##            new_height = int(original_size[1] * scale_factor)
##            new_size = (new_width, new_height)
##
##            # Resize using high-quality downsampling filter
##            img_resized = img.resize(new_size, Image.LANCZOS)
##
##            if save_path is None:
##                # Overwrite original
##                img_resized.save(image_path)
##                print(f"[✔] Scaled and saved: {image_path} -> {new_size}")
##            else:
##                # Ensure output directory exists
##                os.makedirs(os.path.dirname(save_path), exist_ok=True)
##                img_resized.save(save_path)
##                print(f"[✔] Scaled and saved: {save_path} -> {new_size}")
##    except Exception as e:
##        print(f"[✘] Failed to process image: {image_path}")
##        print(f"    Error: {e}")
##
##
##def walk_and_scale_images(base_dir):
##    """
##    Recursively walks through all subdirectories starting from base_dir,
##    scales images, and overwrites them or saves to OUTPUT_DIR based on settings.
##    """
##    if not os.path.isdir(base_dir):
##        print(f"[✘] The directory '{base_dir}' does not exist.")
##        return
##
##    for root, dirs, files in os.walk(base_dir):
##        for file in files:
##            if file.lower().endswith(IMAGE_EXTENSIONS):
##                original_path = os.path.join(root, file)
##
##                if OVERWRITE:
##                    scale_image(original_path, SCALE_FACTOR)
##                else:
##                    # Create mirrored path in OUTPUT_DIR
##                    relative_path = os.path.relpath(original_path, base_dir)
##                    output_path = os.path.join(OUTPUT_DIR, relative_path)
##                    scale_image(original_path, SCALE_FACTOR, save_path=output_path)
##
##
##if __name__ == "__main__":
##    print(f"Scanning '{SPRITES_DIR}' for images to scale down by 0.5x...")
##    walk_and_scale_images(SPRITES_DIR)
##    print("All images processed.")


gameState = 'Main Menu'
gameMode = ['Arena Scuffle', 'Freeplay', 'Endless']
gameModeType = None
#Rumble Mode, Freeplay Mode, Sophia Mathematical Escape Room
transitionInfo = {}
def doTransition(varName, varValue=True, color=BLACK, surface=hud.surface, asset=[]):
    if transitionInfo == {}:
        transitionInfo['VarName'] = varName
        transitionInfo['VarValue'] = varValue
        transitionInfo['Frame'] = 0
        transitionInfo['Surface'] = surface
        transitionInfo['Asset'] = asset
        transitionInfo['AssetFrame'] = 0
        transitionInfo['Color'] = color

def transitionUpdate():
    if transitionInfo != {}:
        if globals()[transitionInfo['VarName']] != transitionInfo['VarValue']:
            transitionInfo['Frame'] += 1
        else:
            transitionInfo['Frame'] -= 1

        transitionInfo['AssetFrame'] += 1
        if transitionInfo['Asset'] != []:
            indexNum = min(len(transitionInfo['Asset'])-1, transitionInfo['AssetFrame'])
            loadImg(transitionInfo['Asset'][indexNum])
        drawRect(transitionInfo['Surface'], transitionInfo['Color'], (0, 0, width, 50*transitionInfo['Frame']))
        drawRect(transitionInfo['Surface'], transitionInfo['Color'], (0, height-50*transitionInfo['Frame'], width, 50*transitionInfo['Frame']*2))
        if 50*transitionInfo['Frame'] >= 400:
            globals()[transitionInfo['VarName']] = transitionInfo['VarValue']
            sprites.clear()
            animatedSprites.clear()

        if globals()[transitionInfo['VarName']] == transitionInfo['VarValue'] and transitionInfo['Frame'] == 0:
            transitionInfo.clear()



opponent = [None, None, None, None, None]
opponentSelect = 0
inOpponent = False
inPlayer = False
battleData = None
selectedAward = 0
codeString = ''
previewMode = False
inMoreInfo = False
infoType = 0
infoSelect = 0
extraScroll = 0
async def main():
    if screenWindow.useWeb:
        pygame.mixer.init()
        #pygame.mixer.music.load(f'sounds/music/menuMusic.ogg')
        #pygame.mixer.music.play(loops=-1)
        if sys.platform == "emscripten":
            audio.src = 'music/menuMusic.mp3'
        else:
            playSound(f'music/menuMusic.ogg', 1, True)
    global inGame, fullscreen, frame, validAlly, validEnemy, party, selectionSprite, selectedAlly, inSkinSelect, skinSelect, inMoreInfo, skinList, skinListEn, partyIndex, option
    global inOption, interrupt, debugMode, modifyStat, inControl, inSetting, whichBase, setting, inCharSelect, widthy, heighty, music, partySelect, mouseScroll
    global gameState, startBattle, opponent, opponentSelect, inOpponent, battleData, selectedAward, codeString, previewMode, infoType, infoSelect, extraScroll
    hud.cameraY=0
    #pygame.mixer.music.set_volume(musicVolume)
    screenWindow.achievementObj['First Comer!'].trigger()
    while inGame:
        await asyncio.sleep(0)
        clock.tick(30) # Set the framerate to 20fps
        #pygame.mixer.music.set_volume(screenWindow.musicVolume)
        screenWindow.deltaTime = 1/60
        frame += 1
        confirm = False
        cancel = False
        rightPressed = False
        leftPressed = False
        upPressed = False
        downPressed = False
        special = False
        #startBattle = False
        interrupt = False
        setting = False
        scrollUp = False
        scrollDown = False
        windowScaleX = widthy/width
        windowScaleY = heighty/height
        pygameKeyEvent = pygame.event.get()
        for event in pygameKeyEvent: # For every event
            if event.type == pygame.QUIT: # If the event is quit, basically pressing the X at the top right of the window
                inGame = False # Quit the game without SAVING!

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scrollUp = True
                elif event.button == 5:
                    scrollDown = True

            elif event.type == pygame.KEYDOWN: # If the event involved a key on the keyboard being pressed once

                if event.key == pygame.K_F4:
                    fullscreen = not fullscreen
                    screenWindow.fullscreen = fullscreen
                    if screenWindow.fullscreen:
                        #screen = pygame.transform.rotate(screen, allyTween[2]/6)
                        screenWindow.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

                    else:
                        screenWindow.window = pygame.display.set_mode((1000, 700))

                if event.key == pygame.K_1:
                    debugMode = not debugMode


                if event.key == screenWindow.keyBind['Confirm']:
                    confirm = True
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    special = True
                elif event.key == pygame.K_AT:
                    setting = True
                elif event.key == screenWindow.keyBind['Cancel']:
                    cancel = True
                elif event.key == pygame.K_RIGHT:
                    rightPressed = True
                elif event.key == pygame.K_LEFT:
                    leftPressed = True
                elif event.key == pygame.K_UP:
                    upPressed = True
                elif event.key == pygame.K_DOWN:
                    downPressed = True
                #elif commandMode:
                elif event.key == pygame.K_BACKSPACE: # If the key pressed is backspace
                    codeString = codeString[:-1] # Remove the last character from the user's input
                elif event.key == pygame.K_RETURN:
                    confirm = True
                elif event.key == pygame.K_BACKSPACE:
                    cancel = True
                else: # If the key pressed is not backspace
                    codeString += event.unicode
        resetCode = True
        code_1 = '231109' #Allerwave
        code_2 = '271109' #The Creator
        code_3 = '111111'
        code_4 = '567567'
        for num, i in enumerate(codeString):
            resetCode = False
            if num + 1 > len(code_1):
                resetCode = True
                break
            if i != code_1[num]:
                resetCode = True
                break
        #if codeString.lower() in code_1:# or codeString.lower() not in 'the creator':
            #resetCode = False
        if resetCode:
            for num, i in enumerate(codeString):
                resetCode = False
                if num + 1 > len(code_2):
                    resetCode = True
                    break
                if i != code_2[num]:
                    resetCode = True
                    break

        if resetCode:
            for num, i in enumerate(codeString):
                resetCode = False
                if num + 1 > len(code_3):
                    resetCode = True
                    break
                if i != code_3[num]:
                    resetCode = True
                    break
        if resetCode:
            for num, i in enumerate(codeString):
                resetCode = False
                if num + 1 > len(code_4):
                    resetCode = True
                    break
                if i != code_4[num]:
                    resetCode = True
                    break
        if resetCode:
            #print(True)
            codeString = ''
        if codeString.lower() == code_1:
            screenWindow.achievementObj['The Programmer'].trigger()
            screenWindow.achievementObj['The Programmer'].desc = 'The one behind the code.'
            validAlly.append(playerObj['Allerwave'])
            codeString = ''
        if codeString.lower() == code_2:
            screenWindow.achievementObj['The Creator'].trigger()
            screenWindow.achievementObj['The Creator'].desc = 'The overseer of this world.'
            validAlly.append(playerObj['The Creator'])
            codeString = ''
        if codeString.lower() == code_3:
            startBattle = True
            battleData = 'vsZephyr'
            #inCharSelect = False
            codeString = ''
        if codeString.lower() == code_4:
            startBattle = True
            battleData = 'Skeleton Fight'
            #inCharSelect = False
            codeString = ''

                #playSound('Confirm_sfx.ogg')

        #botPlay.draw()

        if screenWindow.useWeb:
            pygame.mixer.music.set_volume(screenWindow.musicVolume) # Set the music volum
        hud_rect = hud.get_rect(center=(width/2, 390))
        fps = clock.get_fps()
        fps_text = render_text(f"FPS: {int(fps)}/30", WHITE, 30)
        blitObj(screen, fps_text, 10, 10, pivot_type='topleft')
        draw(backGroundScreen)
        draw(screen)
        updateTween()
        updateAnimation()
        #screen.surface.blit(hud.surfa, (0, 0))
        draw(hud)        #drawRect(screen.surface, (70, 70, 70) ,(0, 0, width, 100))
        for i in screenWindow.achievementObj.values():
            i.update()
        transitionUpdate()
        screenBlit(screen)
        hud.surface.fill((0, 0, 0, 0))
        backGroundScreen.surface.fill((0, 0, 0, 0))
        screen.surface.fill((0, 0, 0, 0))
        #screen.surface.fill(GRAY)
        #screen.blit(background, (0, -300))
        #print('Hello World')
        #window.fill(BLACK) # Fill the window with WHITE
        mouse_pos = pygame.mouse.get_pos() # Get the mouse position
        mouse_buttons = pygame.mouse.get_pressed() # Get the mouse buttons

        # Super funni thing to make mouse input work properly :]
        if any(mouse_buttons): # If any of the mouse buttons are pressed
            if screenWindow.mouseHold: # If the mouse button are held down
                screenWindow.mouseDown = False # Automatically stop the input of 'mouse being clicked once' to the game
            else: # If the mouse button are not held down, though his means that in the first frame after bthe mouse was clicked
                screenWindow.mouseDown, screenWindow.mouseHold = True, True # Sends to the game an input of the mouse having been clicked once and also sends an input that the mouse is also currently being held down for later frames
        else: # If no mouse buttons are pressed
            screenWindow.mouseHold, screenWindow.mouseDown = False, False # Automatically stop the input of 'mouse being clicked once' and 'mouse held down continuously' to the game

        mouseHold, mouseDown = screenWindow.mouseHold, screenWindow.mouseDown


        mouseHover()
        #if screenWindow.useWeb:
        pygame.mixer.music.set_volume(round(screenWindow.musicVolume, 2))

        #draw(hud)

        downArrow = loadSprite('down', f'controls/down.png', (180, 580), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)
        upArrow = loadSprite('up', f'controls/up.png', (180, 420), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud)

        resetMusic = loadSprite('setting', f'controls/special.png', (920, 480), mouseCollide=True, opacity=255/3, baseScale=80/250, layer=hud, color=PURPLE)

        if mouseTouch(upArrow, True, True):
            upPressed = True
        if mouseTouch(downArrow, True, True):
            downPressed = True
        if mouseTouch(resetMusic, True, True):
            previewMode = not previewMode

        if gameState == 'Main Menu':
            drawRect(hud.surface, (150, 50, 150) ,(0, 0, width, 100))
            drawRect(hud.surface, (200, 100, 200) ,(0, 100, width, 500))
            drawRect(hud.surface, (150, 50, 150) ,(0, height-100, width, 100))
            classes = ['Melee', 'Range', 'Thrower', 'Support', 'Tank', 'Controller', 'All rounder']
            #theFrame = frame%120
            for num, classy in enumerate(classes):
                x = 500*(num+1) - (15*(frame%233)) - 100
                if x < -1100:
                    x = 500*(num+len(classes)+1) - (15*(frame%233)) - 100
                y = 50*math.sin(frame/15+num) + height/2
                classObj = loadImg((f'classes/{classy}.png', 1))
                blitObj(hud.surface, classObj, x, y)

            buttons = [screenWindow.buttonList['Play'], screenWindow.buttonList['Setting'], screenWindow.buttonList['Achievement'], screenWindow.buttonList['Quit']]
            for num, button in enumerate(buttons):

                button.x = width/2
                button.y = height/2 + num*80 + 50
                button.width = 250
                button.height = 50
                button.mainColor = (70, 160, 200)
                button.hoverColor = (70, 200, 200)
                button.thickness = 10
                button.draw()

                if button.clicked:
                    if button.name == 'Play':
                        theAsset = []
                        for num, i in enumerate(validAlly):
                            theAsset.append(f'selectionIcon/{i.name}.png')
                        doTransition('gameState', 'Game Select', color=BLACK, asset=theAsset)
                    elif button.name == 'Setting':
                        theAsset = []
                        for num, i in enumerate(validAlly):
                            theAsset.append(f'selectionIcon/{i.name}.png')
                        doTransition('gameState', 'Setting Select', color=BLACK, asset=theAsset)
                    elif button.name == 'Achievement':
                        theAsset = []
                        for num, i in enumerate(validAlly):
                            theAsset.append(f'selectionIcon/{i.name}.png')
                        doTransition('gameState', 'Achievement Select', color=BLACK, asset=theAsset)
                    elif button.name == 'Quit':
                        theAsset = []
                        for num, i in enumerate(validAlly):
                            theAsset.append(f'selectionIcon/{i.name}.png')
                        doTransition('inGame', False)#, color=BLACK, asset=theAsset)

            #logoObj = loadImg(('mainLogo.png', 0.7))
            logoObj = loadImg(('windowIcon.png', 0.7))
            blitObj(hud.surface, logoObj, width/2, 180+20*math.sin(frame/30))
            logoText = render_text('Intense Rumble', (250, 250, 250), 80, True, (0, 0, 0), 5)
            blitObj(hud.surface, logoText, width/2, 300+20*math.sin(frame/30))
            #logoText = render_text('Rumble', (250, 250, 250), 80, True, (0, 0, 0), 5)
            #blitObj(hud.surface, logoText, width/2, 230+20*math.sin(frame/30))

        if gameState == 'Achievement Select':
            for i in range(0, 5):
                drawRect(backGroundScreen.surface, (min((i+1)*50, 255), 0, 0) ,(0, i*40, width, 500-i*80+250))

            button = screenWindow.buttonList['Back']#, screenWindow.buttonList['Battle']]
            button.x = width - 100
            button.y = 50
            button.mainColor = (255, 255, 0)
            button.hoverColor = (255, 255, 130)
            button.width = 150
            button.thickness = 10
            button.draw()
            if button.clicked:
                doTransition('gameState', 'Main Menu', color=BLACK)

            button = screenWindow.buttonList['>']#, screenWindow.buttonList['Battle']]
            button.y = 380
            button.x = width/2 + 150
            button.mainColor = (200, 0, 200)
            button.hoverColor = (200, 130, 200)
            button.width = 100
            button.thickness = 10
            button.draw()
            if rightPressed or button.clicked:
                selectedAward += 1
                selectedAward = 0 if selectedAward >= len(screenWindow.achievementObj) else selectedAward

            button = screenWindow.buttonList['<']#, screenWindow.buttonList['Battle']]
            button.y = 380
            button.x = width/2 - 150
            button.mainColor = (200, 0, 200)
            button.hoverColor = (200, 130, 200)
            button.width = 100
            button.thickness = 10
            button.draw()
            if leftPressed or button.clicked:
                selectedAward -= 1
                selectedAward = len(screenWindow.achievementObj) - 1 if selectedAward < 0 else selectedAward


            for num, award in enumerate(screenWindow.achievementObj.values()):
                x = width/2 + 400*(num - selectedAward)
                y = 250

                if selectedAward == num:
                    scale = 2
                else:
                    scale = 1.5

                icon = loadSprite(award.name, f'achievement/{award.name}.png', (x, y))
                name = award.name
                desc = award.desc
                if award.triggered == False:
                    icon.image = f'achievement/Locked.png'
                    name = '???'
                else:
                    icon.image = f'achievement/{award.name}.png'

                icon.tweenScale(scale, 'circOut', 0.2, True)
                icon.tweenPos((x, y), 'circOut', 0.2, True)

                if selectedAward == num:
                    drawRect(hud, (0, 0, 0, 135), 0, 500-100*(1-icon.scale/2), width, 50, True, 0)
                    descText = render_text(desc, WHITE, 55, True, BLACK, 3)
                    blitObj(hud, descText, width/2, 500-100*(1-icon.scale/2) + 25)

                nameText = render_text(name, WHITE, 60-30*(1-icon.scale/2), True, BLACK, 3)
                blitObj(hud, nameText, icon.pos[0], y-50-50*icon.scale)

        if gameState == 'Setting Select':
            for i in range(0, 5):
                drawRect(backGroundScreen.surface, (min((i+1)*50, 255), 0, min((i+1)*50, 255)) ,(0, i*40, width, 500-i*80+250))

            button = screenWindow.buttonList['Back']#, screenWindow.buttonList['Battle']]
            button.x = width - 100
            button.y = 50
            button.mainColor = (255, 255, 0)
            button.hoverColor = (255, 255, 130)
            button.width = 150
            button.thickness = 10
            button.draw()
            if button.clicked:
                doTransition('gameState', 'Main Menu', color=BLACK)

            confirmButton = screenWindow.buttonList['confirm']
            cancelButton = screenWindow.buttonList['cancel']

            confirmButton.name = f'Confirm: {pygame.key.name(screenWindow.keyBind["Confirm"]).upper()}'
            if confirmButton.clicked:
                confirmButton.selected = True
                cancelButton.selected = False

            if confirmButton.selected:
                confirmButton.mainColor = (200, 0, 200)
                confirmButton.hoverColor = (200, 70, 200)
            else:
                confirmButton.mainColor = (70, 160, 200)
                confirmButton.hoverColor = (70, 200, 200)

            confirmButton.draw()

            cancelButton.name = f'Cancel: {pygame.key.name(screenWindow.keyBind["Cancel"]).upper()}'
            if cancelButton.clicked:
                cancelButton.selected = True
                confirmButton.selected = False

            if cancelButton.selected:
                cancelButton.mainColor = (200, 0, 200)
                cancelButton.hoverColor = (200, 70, 200)
            else:
                cancelButton.mainColor = (70, 160, 200)
                cancelButton.hoverColor = (70, 200, 200)

            cancelButton.draw()

            for event in pygameKeyEvent:
                if event.type == pygame.KEYDOWN:
                    if confirmButton.selected:
                        screenWindow.keyBind["Confirm"] = event.key
                        confirmButton.selected = False
                    elif cancelButton.selected:
                        screenWindow.keyBind["Cancel"] = event.key
                        cancelButton.selected = False

                elif not (confirmButton.selected or cancelButton.selected):
                    break
            musicSlider = screenWindow.musicSlider
            musicSlider.handle_event(pygameKeyEvent)
            musicSlider.draw(hud)

            soundSlider = screenWindow.soundSlider
            soundSlider.handle_event(pygameKeyEvent)
            soundSlider.draw(hud)



        if gameState == 'Game Select':
            if gameModeType == None:
                drawRect(screen.surface, (0, 150, 150) ,(0, 0, width, height))
                for i in range(0, 5):
                    drawRect(screen.surface, (min(i*50, 255), 170, 150) ,(0, 100+i*40, width, 500-i*80))
                button = screenWindow.buttonList['Back']#, screenWindow.buttonList['Battle']]
                button.x = width - 100
                button.y = 50
                button.mainColor = (255, 255, 0)
                button.hoverColor = (255, 255, 130)
                button.width = 150
                button.thickness = 10
                button.draw()
                if button.clicked:
                    doTransition('gameState', 'Main Menu', color=BLACK)

                    #doTransition('gameState', 'Main Menu', color=BLACK)
                for num, gameModes in enumerate(gameMode):
                    gameSprite = loadSprite(gameModes, f'{gameModes}.png', (0, 0), baseScale=0.5)
                    gameSprite.opacity = 255
                    x = 100
                    y = 150 + 150*num
                    gameSprite.tweenPos((x,y), 'circOut', 0.3, True)

                    playButton = Button(f'Play_{num}', 0, 0)
                    playButton.x = gameSprite.pos[0] + (gameSprite.getSize()[0]/2)/scaleFactor + 100
                    playButton.y = gameSprite.pos[1] + (gameSprite.getSize()[1]/2)/scaleFactor - (playButton.height+playButton.thickness)/2
                    playButton.width = 100
                    playButton.name = 'Play'
                    playButton.mainColor = (0, 200, 0)
                    playButton.hoverColor = (130, 200, 130)
                    playButton.draw()
                    if playButton.clicked:
                        doTransition('gameModeType', num, color=BLACK)

                    gameText = render_text(gameModes, WHITE, 60, True, BLACK, 4)
                    blitObj(hud.surface, gameText, playButton.x - playButton.width/2, gameSprite.pos[1] - (gameSprite.getSize()[1]/2)/scaleFactor, pivot_type='topleft')

                    playButton = Button(f'Info_{num}', 0, 0)
                    playButton.x = gameSprite.pos[0] + (gameSprite.getSize()[0]/2)/scaleFactor + 250
                    playButton.y = gameSprite.pos[1] + (gameSprite.getSize()[1]/2)/scaleFactor - (playButton.height+playButton.thickness)/2
                    playButton.width = 100
                    playButton.name = 'Info'
                    playButton.mainColor = (0, 200, 200)
                    playButton.hoverColor = (130, 200, 200)
                    #playButton.draw()
                    #if playButton.clicked:
                    #    doTransition('gameModeType', num, color=BLACK)

            if gameModeType == 0 or gameModeType == 2:
                for num, gameModes in enumerate(gameMode):
                    gameSprite = loadSprite(gameModes, f'{gameModes}.png', (0, 0))
                    gameSprite.opacity = 0
                button = screenWindow.buttonList['Back']#, screenWindow.buttonList['Battle']]
                #button.x = width - 150
                #button.y = 150
                #button.mainColor = (200, 200, 0)
                #button.hoverColor = (200, 200, 130)
                #button.width = 150
                #button.thickness = 10
                button.draw()
                if button.clicked:
                    if inMoreInfo:
                        inMoreInfo = False
                        infoType = 0
                    elif inSkinSelect:
                        inSkinSelect = False
                        party[partySelect] = None
                        skinSelect = 0
                    elif inCharSelect:
                        inCharSelect = False
                    elif inSetting:
                        inSetting = False
                    elif not inCharSelect:
                        doTransition('gameModeType', None, color=BLACK)



                button = screenWindow.buttonList['O']#, screenWindow.buttonList['Battle']]
                plus = loadSprite('plus0', f'plus.png', (0, 200), mouseCollide=True)
                button.name = ">>"
                button.x = plus.pos[0] - 150
                button.y = plus.pos[1]
                button.mainColor = (0, 255, 0)
                button.hoverColor = (0, 255, 130)
                button.width = 50
                button.height = 50
                button.thickness = 10
                button.draw()
                if button.clicked:
                    allyNum = 0
                    for i in party:
                        if i != None:
                            del screenWindow.animatedSprites[i.name + "__Character" + str(allyNum)]
                            allyNum += 1
                    party = buildEnemyList(validAlly, 5)
                    party.reverse()

                if inSkinSelect:
                    button = screenWindow.buttonList['Confirm']#, screenWindow.buttonList['Battle']]
                    button.x = width - 300
                    button.y = 50
                    button.mainColor = (0, 200, 0)
                    button.hoverColor = (130, 200, 130)
                    button.width = 150
                    button.thickness = 10
                    button.draw()
                    if button.clicked:
                        for num, skin in enumerate(party[partySelect].skinList):
                            icon = loadSprite(skin + party[partySelect].name, f'players/{party[partySelect].name}/{skin}/idle_0.png', (0, 0), doCrop=False)
                            icon.opacity = 0
                        inCharSelect = inSkinSelect = False
                        partySelect+=1
                        if partySelect>4:
                            partySelect=4
                        skinSelect = 0

                #if not inCharSelect:
                plus = loadSprite('plus2', f'plus.png', (0, 200), mouseCollide=True)
                button = screenWindow.buttonList['Battle']#, screenWindow.buttonList['Battle']]
                button.x = width/2 - 150
                button.y = plus.pos[1] - 150
                button.mainColor = (200, 0, 0)
                button.hoverColor = (200, 70, 70)
                button.width = 200
                button.thickness = 10
                button.draw()
                if button.clicked:
                    startBattle = True

                #plus = loadSprite('plus2', f'plus.png', (0, 200), mouseCollide=True)
                button = screenWindow.buttonList['Tutorial']#, screenWindow.buttonList['Battle']]
                button.x = width/2
                button.y = (height - plus.pos[1]) + 150
                button.mainColor = (200, 0, 0)
                button.hoverColor = (200, 70, 70)
                button.width = 250
                button.thickness = 10
                button.draw()
                if button.clicked:
                    startBattle = True
                    battleData = 'Tutorial'

                #plus = loadSprite('plus2', f'plus.png', (0, 200), mouseCollide=True)
                button = screenWindow.buttonList['Setting']#, screenWindow.buttonList['Battle']]
                button.x = width/2 + 150
                button.y = plus.pos[1] - 150
                button.mainColor = (200, 0, 200)
                button.hoverColor = (200, 70, 200)
                button.width = 200
                button.thickness = 10
                button.draw()
                if button.clicked:
                    inSetting = True
                    #doTransition('startBattle', True, color=BLACK)


                for i in range(0, 5):
                    drawRect(backGroundScreen.surface, (min(i*50, 255), 200, 200) ,(0, 100+i*40, width, 500-i*80))

                if rightPressed:
                    if not inSkinSelect:
                        partySelect += 1
                        if partySelect > 4:
                            partySelect = 0

                if leftPressed:
                    if not inSkinSelect:
                        partySelect -= 1
                        if partySelect < 0:
                            partySelect = 4

                if confirm:
                    if not inCharSelect:
                        inCharSelect = True
                    if inSkinSelect:
                        if party[partySelect] != None:
                            for num, skin in enumerate(party[partySelect].skinList):
                                icon = loadSprite(skin + party[partySelect].name, f'players/{party[partySelect].name}/{skin}/idle_0.png', (0, 0), doCrop=False)
                                icon.opacity = 0
                        inCharSelect = inSkinSelect = False
                        partySelect+=1
                        if partySelect>4:
                            partySelect=4
                        skinSelect = 0
                        inMoreInfo = False
                        infoType = 0
                        extraScroll = 0




                if cancel:
                    if inSkinSelect:
                        inSkinSelect = False
                        party[partySelect] = None
                        skinSelect = 0
                    elif inCharSelect:
                        inCharSelect = False
                    elif inSetting:
                        inSetting = False
                    elif not inCharSelect:
                        party[partySelect] = None



                #if special:
                    #inSetting = not inSetting
                if inSetting:
                    for num, i in enumerate(screenWindow.trigger.values()):
                        x = 300 + 400*(num%2)
                        y = 200 + 100 * (num//2)
                        i.x = x
                        i.y = y
                        i.draw()



                if startBattle and not inCharSelect:

                    partyBack = []
                    character.opponent = []
                    for num, i in enumerate(party):
                        if i != None:
                            partyBack.append(i)

                    backParty = []
                    partyDict = {}
                    partyList = {}
                    for i in partyBack:
                        if i.name in partyDict:
                            partyAlly = copy.deepcopy(i)
                            partyAlly.inventory = i.inventory
                            backParty.append(partyAlly)
                            if i.name not in partyList:
                                anotherAlly = copy.deepcopy(i)
                                anotherAlly.inventory = i.inventory
                                partyList[i.name] = [anotherAlly]
                                backParty[backParty.index(i)] = anotherAlly
                            partyList[i.name].append(partyAlly)
                        else:
                            partyDict[i.name] = i
                            backParty.append(i)
                    for i in partyList:
                        if len(partyList[i]) > 1:
                            for num, ally in enumerate(partyList[i]):
                                ally.name += f" {chr(num+65)}"
                    partyBack = backParty


                    theEnemyLeft = []
                    for num, i in enumerate(validEnemy):
                        foundAlly = False
                        for ally in partyBack:
                            if ally.name == i.name:
                                foundAlly = True
                                break
                        if not foundAlly:
                            theEnemyLeft.append(i)

                    #raise ValueError('Screw u')

                    character.opponent = random.sample(validEnemy, len(partyBack))

                    character.party = partyBack
                    if character.party != [] or battleData != None:
                        screenWindow.sprites.clear()
                        screenWindow.animatedSprites.clear()
                        #with open('battle.py', 'r') as file:
                            #battleCode = file.read()
                        #exec(battleCode)
                        effects = {}
                        for num, i in enumerate(validAlly + validEnemy):
                            for buff in i.passiveBuff:
                                effects[buff.name] = buff
                            i.hpSet()
                        theAllies = copy.deepcopy(validAlly)
                        theEnemies = copy.deepcopy(validEnemy)
                        if not screenWindow.useWeb:
                            music.pause()
                        if screenWindow.useWeb:
                            screenWindow.texts.clear()
                            screenWindow.images.clear()
                        #for i in validEnemy:
                            #print(i.name)
                        pygame.mixer.stop()
                        battleData = "Endless" if (gameModeType==2 and battleData==None) else battleData
                        reworkingBattle.main(partyBack, buildEnemyList(validEnemy, len(partyBack)), useSpeedTurn=True, battleData=battleData)
                        #if screenWindow.useWeb:
                            #screenWindow.texts.clear()
                            #screenWindow.images.clear()
                        hud.start_fade(BLACK, 255, 1)
                        screen.start_fade(BLACK, 255, 1)
                        screenWindow.backGroundScreen.start_fade(BLACK, 255, 1)
                        hud.camera_zoom = 3
                        screen.camera_zoom = 3
                        screenWindow.backGroundScreen.camera_zoom = 3
                        #pygame.mixer.stop()
                        await reworkingBattle.battleRun()
                        battleData = None
                        pygame.mixer.stop()
                        #reworkingBattle.main(partyBack, [character.Zephyr])
                        #effects = {}
                        for num, i in enumerate(validAlly):
                            validAlly[num] = theAllies[num]
                            character.playerObj[i.name] = theAllies[num]

                        for num, i in enumerate(validEnemy):
                            validEnemy[num] = theEnemies[num]
                            #print(type(i))
                            character.opponentObj[i.name] = theEnemies[num]

                        for num, i in enumerate(validAlly + validEnemy):
                            passiveBuff = {}
                            for buff in i.passiveBuff:
                                passiveBuff[effects[buff.name]] = [False, False]
                            i.passiveBuff = passiveBuff
                        if not screenWindow.useWeb:
                            music = DynamicMusicPlayer(f"sounds/music/menuMusic.ogg", loop=True)
                            music.set_speed(0.9)
                        else:
                            #pygame.mixer.music.load(f'sounds/music/menuMusic.ogg')
                            #pygame.mixer.music.play(loops=-1)
                            if sys.platform == "emscripten":
                                audio.src = 'music/menuMusic.mp3'
                            else:
                                playSound(f'music/menuMusic.ogg', 1, True)

                        hud.camera_shake = 0
                        backGroundScreen.camera_zoom = 1
                        backGroundScreen.camera_rotation = 0
                        backGroundScreen.camera_shake = 0
                        party = [None, None, None, None, None]
                        partyBack = []
                        screenWindow.sprites.clear()
                        screenWindow.animatedSprites.clear()
                    startBattle = False

                for num in range(0, 5):
                    x = 150 + num*700/5 + 700/10
                    plus = loadSprite('plus' + str(num), f'plus.png', (0, 200), mouseCollide=True)
                    if party[num] != None:
                        plus.image = f'selectionIcon/{party[num].name}.png'
                        plus.baseScale = 0.5
                        #, (x, 300), mouseCollide=True, baseScale=0.5)
                        #plus.opacity=0
                        #icon = loadImg((f'selectionIcon/{party[num].name}.png', scale=0.5))
                        #blitObj(screen, icon, x, 300)
                    else:
                        plus.image = f'plus.png'
                        plus.baseScale = 1

                    if inCharSelect or inSetting:
                        plus.tweenPos((x, -200), 'circIn', 0.3+(4-num)*0.05, True)
                        plus.tweenOpacity(0, 'circOut', 0.3, True)
                    else:
                        plus.tweenPos((x, 200), 'circOut', 0.3+num*0.05, True)
                        plus.tweenOpacity(255, 'circIn', 0.1, True)

                    if not inCharSelect or inSetting:
                        xButton = Button(f'-{num}', 0, 0)
                        xButton.x = plus.pos[0] + 50 - (xButton.width+xButton.thickness)/2
                        xButton.y = plus.pos[1] - 50 - (xButton.height+xButton.thickness)/2
                        xButton.width = 35
                        xButton.height = 35
                        xButton.name = '-'
                        xButton.mainColor = (200, 0, 0)
                        xButton.hoverColor = (200, 130, 130)
                        xButton.draw()
                        if xButton.clicked:
                            if party[num] != None:
                                allyNum = 0
                                for i in party:
                                    if i != None:
                                        del screenWindow.animatedSprites[i.name + "__Character" + str(allyNum)]
                                        allyNum += 1
                            party[num] = None

                        elif mouseTouch(plus, True, True):
                            inCharSelect = True
                            partySelect = num

                tempParty = []
                for stuff in party:
                   if stuff != None:
                       tempParty.append(stuff)
                anim = ['idle', 'attackPrep', 'attack', 'hurt', 'skill', 'death', 'dodge']
                for num, ally in enumerate(tempParty):
                    x = 500*((width/2)/500)/len(tempParty) + 1000*(width/1000)/len(tempParty) * num
                    y = 400 #+ 3*num - 3*len(party)
                    charSprite = loadAnimatedSprite(ally.name + "__Character" + str(num), ally.name, pos=(width+400, y), baseScale=0.4)
                    charSprite.skin = ally.skin
                    charX = charSprite.pos[0]
                    charY = charSprite.pos[1]
                    screenWindow.drawEllipse(screen, (0, 0, 0, 50), (charX-90, charY+200-50, 180, 30))
                    if frame%7 == 0 and previewMode:
                        animIndex = anim.index(charSprite.currentAnim) + 1
                        if animIndex > 6:
                            animIndex = 0
                        playAnimation(charSprite, anim[animIndex], False)
                    elif not previewMode:
                        playAnimation(charSprite, "idle", False)
                    if not inCharSelect:
                        charSprite.tweenPos((x, y), "circOut", 0.3, True)
                    else:
                        charSprite.tweenPos((width+400, y), "circIn", 0.1, True)
                    charSprite.opacity = 255
                    charSprite.draw(ally.offsetX, ally.offsetY)
                    charSprite.opacity = 0


                if inCharSelect:
                    if scrollDown or downPressed:
                        mouseScroll -= 100
                    if scrollUp or upPressed:
                        mouseScroll += 100
                #mouseScroll = 0 if mouseScroll < 0 else 700 if mouseScroll > 700 else mouseScroll
                for num, ally in enumerate(validAlly):
                    x = 50 + (num%3)*700/3 + 350/3
                    y = (num//3)*200 + 200 + mouseScroll
                    if (ally in party and ally != party[partySelect] and not inSkinSelect) and ally.beSelectOnce == True:
                        allySprite = loadSprite(ally.name, f'selectionIcon/{ally.name}.png', baseScale=0.75, pos=(x, y), mouseCollide=True, layer=screenWindow.backGroundScreen)
                        allySprite.image = f"achievement/Locked.png"
                        allySprite.baseScale = 1.5
                        allySprite.mouseCollide = False


                    if not inCharSelect:
                        x = -100
                    if ally not in party or ally == party[partySelect] or inSkinSelect or ally.beSelectOnce == False:
                        allySprite = loadSprite(ally.name, f'selectionIcon/{ally.name}.png', baseScale=0.75, pos=(x, y), mouseCollide=True, layer=screenWindow.backGroundScreen)
                        allySprite.image = f'selectionIcon/{ally.name}.png'
                        allySprite.mouseCollide = True
                        allySprite.mouseCollide = True
                        allySprite.baseScale = 0.75
                        classIcon = loadImg((f'classes/{ally.classes}.png', 0.55))
                        #rumblerText = render_text(str(num+1).zfill(3), WHITE, 50, True, BLACK, 2)q
                        if inSkinSelect:
                            rumblerText = render_text(str(num+1).zfill(3), WHITE, 50, True, BLACK, 2)
                        else:
                            rumblerText = render_text(ally.name, WHITE, 50, True, BLACK, 2)
                        blitObj(screen.surface, classIcon, allySprite.pos[0] - (allySprite.getSize()[0]/3)/scaleFactor , allySprite.pos[1] + (allySprite.getSize()[1]/3)/scaleFactor)
                        blitObj(screen.surface, rumblerText, allySprite.pos[0] , allySprite.pos[1] - (allySprite.getSize()[1]/3)/scaleFactor)
                        if not inSkinSelect:
                            drawRect(screen.surface, (0, 140, 220) ,(0, 0, width, 100))
                            #drawRect(screen.surface, (0, 200, 200) ,(0, 100, width, 500))
                            drawRect(screen.surface, (0, 140, 220) ,(0, height-100, width, 100))
                        if mouseTouch(allySprite, True, True) and not mouseTouch(upArrow, True, True) and not mouseTouch(downArrow, True, True):
                            inSkinSelect=True
                            party[partySelect] = ally
                            #inMoreInfo = True
                            #infoType = 2


                    charSprite = loadAnimatedSprite(ally.name + "_Character", ally.name, pos=(-200, 250), baseScale=0.5, flipX=True)
                    charX = -400
                    charY = 300

                    if inSkinSelect:
                        x = -100
                        if ally == party[partySelect]:
                            allySprite.mouseCollide = False
                            allySprite.mouseCollide = False
                            button = screenWindow.buttonList['>']#, screenWindow.buttonList['Battle']]
                            button.x = 180
                            button.y = 320
                            if inMoreInfo:
                                button.x = 580
                                button.y = 310

                            button.mainColor = (200, 0, 200)
                            button.hoverColor = (200, 130, 200)
                            button.width = 50
                            button.thickness = 10
                            if inMoreInfo:
                                if infoType == 0:
                                    if len(party[partySelect].fight) <= 1:
                                        button.mainColor = (180, 180, 180)
                                        button.hoverColor = (130, 130, 130)
                                elif infoType == 1:
                                    skillList = party[partySelect].skills + list(party[partySelect].passiveBuff)
                                    if len(skillList) <= 1:
                                        button.mainColor = (180, 180, 180)
                                        button.hoverColor = (130, 130, 130)
                                
                            if inMoreInfo and infoType == 2:
                                button.width = 100
                                button.y = 420
                                button.x = width - 380
                               # button = screenWindow.buttonList['Back']#, screenWindow.buttonList['Battle']]



                            button.draw()
                            if rightPressed or button.clicked:
                                #pass
                                if not inMoreInfo:
                                    skinSelect += 1
                                    skinSelect = 0 if skinSelect >= len(party[partySelect].skinList) else skinSelect
                                    #print(charSprite.pos)
                                else:
                                    if infoType == 0:
                                        infoSelect += 1
                                        infoSelect = 0 if infoSelect >= len(party[partySelect].fight) else infoSelect
                                    elif infoType == 1:
                                        skillList = skillList = party[partySelect].skills + list(party[partySelect].passiveBuff)
                                        infoSelect += 1
                                        infoSelect = 0 if infoSelect >= len(skillList) else infoSelect
                                    else:
                                        skinSelect += 1
                                        skinSelect = 0 if skinSelect >= len(party[partySelect].skinList) else skinSelect
                                        #print(charSprite.pos)

                            button = screenWindow.buttonList['<']#, screenWindow.buttonList['Battle']]
                            button.x = 80
                            button.y = 320
                            if inMoreInfo:
                                button.x = 110
                                button.y = 310

                            button.mainColor = (200, 0, 200)
                            button.hoverColor = (200, 130, 200)
                            button.width = 50
                            button.thickness = 10
                            if inMoreInfo:
                                if infoType == 0:
                                    if len(party[partySelect].fight) <= 1:
                                        button.mainColor = (180, 180, 180)
                                        button.hoverColor = (130, 130, 130)
                                elif infoType == 1:
                                    skillList = party[partySelect].skills + list(party[partySelect].passiveBuff)
                                    if len(skillList) <= 1:
                                        button.mainColor = (180, 180, 180)
                                        button.hoverColor = (130, 130, 130)
                                    
                            if inMoreInfo and infoType == 2:
                                #button = screenWindow.buttonList['<']#, screenWindow.buttonList['Battle']]
                                button.x = 380
                                button.y = 420
                                button.width = 100



                            button.draw()
                            #print(1, charSprite.pos)
                            if leftPressed or button.clicked:
                                #pass
                                if not inMoreInfo:
                                    skinSelect -= 1
                                    skinSelect = len(party[partySelect].skinList) - 1 if skinSelect < 0 else skinSelect
                                else:
                                    if infoType == 0:
                                        infoSelect -= 1
                                        infoSelect = len(party[partySelect].fight) - 1 if infoSelect < 0 else infoSelect
                                    elif infoType == 1:
                                        skillList = skillList = party[partySelect].skills + list(party[partySelect].passiveBuff)
                                        infoSelect -= 1
                                        infoSelect = len(skillList) - 1 if infoSelect < 0 else infoSelect
                                    else:
                                        skinSelect -= 1
                                        skinSelect = len(party[partySelect].skinList) - 1 if skinSelect < 0 else skinSelect

##                            button = screenWindow.buttonList['Info']#, screenWindow.buttonList['Battle']]
##                            button.x = 80
##                            button.y = 320
##                            button.mainColor = (0, 200, 200)
##                            button.hoverColor = (130, 200, 200)
##                            button.width = 140
##                            button.thickness = 10
##                            button.draw()
##                            if button.clicked:
##                                inMoreInfo = True




                            darkColor = []
                            for i in party[partySelect].color:
                                darkColor.append(i*0.65)
                            drawRect(backGroundScreen.surface, darkColor, (0, 450, width, height-450))
                            darkColor = []
                            for i in party[partySelect].color:
                                darkColor.append(i*0.75)
                            for i in range(0, 5):
                                theColor = (
                                            min(party[partySelect].color[0]+i*20, 255),
                                            min(party[partySelect].color[1]+i*20, 255),
                                            min(party[partySelect].color[2]+i*20, 255)
                                            )
                                drawRect(backGroundScreen.surface, theColor,(0, 100+i*40, width, 500-i*80))
                            #drawRect(screen.surface, party[partySelect].color, (0, 0, width, 450))
                            drawRect(screen.surface, darkColor, (0, 0, width, 100))
                            x = 130
                            y = 200
                            charX = width - 200
                            charY = 300
                            if inMoreInfo:
                                x = -100
                                if infoType == 2:
                                    charX = width + 500

                            for num, skin in enumerate(party[partySelect].skinList):
                                    icon = loadSprite(skin + party[partySelect].name, f'players/{party[partySelect].name}/{skin}/idle_0.png', (0, 0), doCrop=False)
                                    icon.opacity = 0

                            if inMoreInfo and infoType == 2:
                                for num, skin in enumerate(party[partySelect].skinList):
                                    theX = width/2 + 400*(num - skinSelect)
                                    theY = 250

                                    if skinSelect == num:
                                        scale = 0.5
                                    else:
                                        scale = 0.3

                                    #icon.opacity = 255
                                    icon = loadSprite(skin + party[partySelect].name, f'players/{party[partySelect].name}/{skin}/idle_0.png', (theX, theY), doCrop=False)
                                    name = skin
                                    desc = skin
                                    icon.opacity = 255


                                    icon.tweenScale(scale, 'circOut', 0.2, True)
                                    icon.tweenPos((theX, theY), 'circOut', 0.2, True)

                                    if skinSelect == num:
                                        drawRect(hud, (0, 0, 0, 135), 0, 500-100*(icon.scale/2), width, 50, True, 0)
                                        descText = render_text(party[partySelect].skinList[skinSelect], WHITE, 55, True, BLACK, 3)
                                        blitObj(hud, descText, width/2, 500-100*(icon.scale/2) + 25)

                                    #nameText = render_text(party[partySelect].skinList[skinSelect], WHITE, 60-30*(1-icon.scale/2), True, BLACK, 3)
                                    #blitObj(hud, nameText, icon.pos[0], theY-50-50*icon.scale)


                               # if infoType != 2:
                               #     charX = width + 500

                            charSprite.skin = party[partySelect].skinList[skinSelect]
                            party[partySelect].skin = party[partySelect].skinList[skinSelect]
                            statList = ['health', 'attack', 'defense', 'speed', 'productivity', 'range']
                            shortStat = {'level':'LVL', 'health':'HP', 'attack':'ATK', 'defense':'DEF', 'speed':'SPD', 'productivity':'PRD', 'range':'RGE', 'mana':'MP'}
                            ally = party[partySelect]
                            ally.levelUp(0)
                            playerStat = {'level':ally.level, 'health':ally.maxhp, 'attack':ally.attack, 'defense':ally.defense, 'speed':ally.speed, 'productivity':ally.productivity, 'range':ally.range, 'mana':ally.maxMana}
                            setStat = {'health':ally.base[0], 'attack':ally.base[1], 'defense':ally.base[2], 'speed':ally.base[3], 'productivity':ally.base[5], 'range':ally.base[4]}
                            statusX = 55
                            statusY = 100
                            statWidth = 580
                            statHeight = 210
                            statScale = 0.95
                            #if inMoreInfo:
                            #print(2, charSprite.pos)

                            for statNum, stat in enumerate(statList):
                                if inMoreInfo:
                                    break
                                statX = statusX + 200 + 130*(statNum//2)*statScale/0.95
                                statY = statusY + 15 + (statNum%2)*120*statScale/0.95 + 5*math.sin((frame/8)*math.pi+statNum/8)
                                statImg = loadImg((f'stats/{stat}.png', statScale))
                                blitObj(hud, statImg, statX, statY, pivot_type='topleft')
                                statText = render_text(f'{str(playerStat[stat])} ({str(setStat[stat])})', WHITE, 40*statScale/0.95, True, BLACK, 2)
                                statScaleNum = statScale*100
                                blitObj(hud, statText, statX+statScaleNum/2, statY+statScaleNum/(4/3))
                                shortText = render_text(str(shortStat[stat]), WHITE, 50*statScale/0.95, True, BLACK, 2)
                                blitObj(hud, shortText, statX+statScaleNum/2, statY)
                            darkColor = []
                            for i in party[partySelect].color:
                                darkColor.append(i*0.85)
                            #if not inMoreInfo:
                            textThing = party[partySelect].info
                            if inMoreInfo and infoType == 0:
                                textThing = party[partySelect].fight[infoSelect].info
                                textThing += party[partySelect].fight[infoSelect].extraInfo
                                if party[partySelect].fight[infoSelect].useHitChance and 1==0:
                                    for i in range(1, 6):
                                        Range = i
                                        text = "Range " + str(i) + ": " + str(eval( party[partySelect].fight[infoSelect].hitChanceEquation))# + ' \n'
                                        #textThing += text


                            elif inMoreInfo and infoType == 1:
                                skillList = party[partySelect].skills + list(party[partySelect].passiveBuff)
                                if skillList == []:
                                    textThing = 'No Info'
                                else:
                                    textThing = skillList[infoSelect].info
                            elif inMoreInfo and infoType == 2:
                                textThing = ''


                            if inMoreInfo and infoType != 2:
                                #stats
                                def addText(text, x=90, y=100, img='attack', pivot='topleft'):
                                        
                                    textObj = render_text(text, WHITE, 50, True, BLACK, 2)
                                    rectThing = textObj.get_rect(topleft=(x + 60, y))
                                    rectThing.width /= scaleFactor
                                    rectThing.height /= scaleFactor
                                    drawRect(hud.surface, (0, 0, 0, 50), rectThing)
                                    blitObj(hud, textObj, x + 60, y, pivot_type='topleft')

                                    statImg = loadImg((f'stats/{img}.png', 0.52))
                                    blitObj(hud, statImg, x, rectThing.y, pivot_type='topleft')

                                if infoType == 0:
                                    moreText = 'Damage: '
                                    moreText += str(party[partySelect].fight[infoSelect].attack)
                                    if moreText == 'Damage: Default':
                                        moreText = 'Damage: ' + str(party[partySelect].attack)

                                    addText(moreText, 180, 150)
                                    moreText = 'Range: '
                                    moreText += str(party[partySelect].fight[infoSelect].range)
                                    if moreText == 'Range: Default':
                                        moreText = 'Range: ' + str(party[partySelect].range)
                                    addText(moreText, 180, 210, img='range')

                                    moreText = 'Attack Count: '
                                    moreText += str(len(party[partySelect].fight[infoSelect].bars))
                                    #if moreText == 'Attack Count: Default':
                                    #    moreText = 'Attack Count: ' + str(party[partySelect].range)
                                    addText(moreText, 180, 270, img='bars')
                                    

                                elif infoType == 1:
                                    skillList = party[partySelect].skills + list(party[partySelect].passiveBuff)
                                    if skillList != []:
                                        if isinstance(skillList[infoSelect], character.Skill):
                                            moreText = 'Cost: '
                                            moreText += str(skillList[infoSelect].cost)
                                            if moreText == 'Cost: Default':
                                                moreText = 'Cost: ' + str(skillList[infoSelect].cost)
                                            addText(moreText, 180, 150, 'mana')

                                            if 'hp' in skillList[infoSelect].type and 'opponent' in skillList[infoSelect].type and skillList[infoSelect].num != 0:

                                                moreText = 'Damage: '
                                                moreText += str(skillList[infoSelect].num)
                                                if moreText == 'Damage: Default':
                                                    moreText = 'Damage: ' + str(skillList[infoSelect].num)
                                                addText(moreText, 180, 270, 'attack')

                                            elif skillList[infoSelect].num != 0 and 'hp' in skillList[infoSelect].type:

                                                moreText = 'Heal: '
                                                moreText += str(abs(skillList[infoSelect].num))
                                                if moreText == 'Heal: Default':
                                                    moreText = 'Heal: ' + str(abs(skillList[infoSelect].num))
                                                addText(moreText, 180, 270, 'health')

                                            moreText = 'Target Type: '
                                            moreText += str(skillList[infoSelect].targetType)
                                            if moreText == 'Target type: Default':
                                                moreText = 'Target type: ' + str(skillList[infoSelect].targetType)
                                            addText(moreText, 180, 210, 'accuracy')
                                        else:
                                            moreText = 'Passive'
                                            #moreText += str(skillList[infoSelect].cost)
                                            if moreText == 'Passive':
                                                moreText = 'Passive'
                                            addText(moreText, 180, 270, 'critical')
                                            

                                drawRect(hud.surface, darkColor, (80, 350, 530, 180))
                                drawRect(hud.surface, BLACK, (85, 355, 520, 170))
                                nameText = ''
                                if infoType == 0:
                                    nameText = party[partySelect].fight[infoSelect].name

                                elif infoType == 1:
                                    skillList = party[partySelect].skills + list(party[partySelect].passiveBuff)
                                    if skillList != []:
                                        nameText = skillList[infoSelect].name
                                    else:
                                        nameText = 'No Available Skill'
                                else:
                                    nameText = party[partySelect].skinList[skinSelect]
                                nameObj = render_text(nameText, WHITE, 50)
                                blitObj(hud, nameObj, 50 + 580/2, 355 + 20)
                            if infoType != 2:
                                infoSurface = loadSurface(510, 160)
                                drawRect(hud.surface, darkColor, (80, 400, 530, 180))
                                drawRect(hud.surface, BLACK, (90, 410, 510, 160))
                                extraLine = blit_text(infoSurface, textThing, pygame.Rect(0, 20 - extraScroll, 510, 160), "gameFont.otf", 46, WHITE)
                                blitObj(hud, infoSurface, 90, 410, pivot_type='topleft')

                                # Down
                                button = screenWindow.buttonList['v']#, screenWindow.buttonList['Battle']]
                                button.x = 40
                                button.y = 550
                                button.mainColor = (200, 0, 200)
                                button.hoverColor = (200, 130, 200)
                                button.width = 50
                                button.thickness = 10
                                button.draw()
                                if button.clicked or downPressed:
                                    if extraScroll < 26*extraLine:
                                        extraScroll += 50

                                button = screenWindow.buttonList['^']#, screenWindow.buttonList['Battle']]
                                button.x = 40
                                button.y = 430
                                button.mainColor = (200, 0, 200)
                                button.hoverColor = (200, 130, 200)
                                button.width = 50
                                button.thickness = 10
                                button.draw()
                                if button.clicked or upPressed:
                                    if extraScroll > 0:
                                        extraScroll -= 50

                            button = screenWindow.buttonList['Stats']#, screenWindow.buttonList['Battle']]
                            button.x = 150
                            button.y = 650
                            button.mainColor = (0, 200, 200)
                            button.hoverColor = (130, 200, 200)
                            button.width = 170
                            button.thickness = 10
                            button.draw()
                            if button.clicked:
                                inMoreInfo = False
                                infoType = 0
                                infoSelect = 0
                                extraScroll = 0

                            button = screenWindow.buttonList['Attacks']#, screenWindow.buttonList['Battle']]
                            button.x = 350
                            button.y = 650
                            button.mainColor = (200, 0, 0)
                            button.hoverColor = (200, 130, 130)
                            button.width = 170
                            button.thickness = 10
                            button.draw()
                            if button.clicked:
                                inMoreInfo = True
                                infoType = 0
                                infoSelect = 0
                                extraScroll = 0

                            button = screenWindow.buttonList['Abilities']#, screenWindow.buttonList['Battle']]
                            button.x = 550
                            button.y = 650
                            button.mainColor = (0, 0, 200)
                            button.hoverColor = (130, 130, 200)
                            button.width = 170
                            button.thickness = 10
                            button.draw()
                            if button.clicked:
                                inMoreInfo = True
                                infoType = 1
                                infoSelect = 0
                                extraScroll = 0

                            button = screenWindow.buttonList['Skins']#, screenWindow.buttonList['Battle']]
                            button.x = 750
                            button.y = 650
                            button.mainColor = (150, 0, 200)
                            button.hoverColor = (150, 130, 200)
                            button.width = 170
                            button.thickness = 10
                            button.draw()
                            if button.clicked:
                                inMoreInfo = True
                                infoType = 2
                                infoSelect = 0
                                extraScroll = 0

                            nameText = render_text(f'{party[partySelect].name}     |     {party[partySelect].skin}', WHITE, 60, True, BLACK, 3)
                            blitObj(hud.surface, nameText, x=55, y=20, pivot_type='topleft')
                            #drawRect()

                            #print(2, charSprite.pos)

                    charSprite.tweenPos((charX, charY), "circOut", 0.4, True)



                        #inCharSelect = False


                    allySprite.tweenPos((x, y), "circOut", 0.1, True)
                mouseScroll = -1500 if mouseScroll < -1500 else 0 if mouseScroll > 0 else mouseScroll

        if gameModeType == 1:
                for num, gameModes in enumerate(gameMode):
                    gameSprite = loadSprite(gameModes, f'{gameModes}.png', (0, 0))
                    gameSprite.opacity = 0
                button = screenWindow.buttonList['Back']#, screenWindow.buttonList['Battle']]
                #button.x = width - 150
                #button.y = 150
                #button.mainColor = (200, 200, 0)
                #button.hoverColor = (200, 200, 130)
                #button.width = 150
                #button.thickness = 10
                button.draw()
                if button.clicked:
                    if inSkinSelect:
                        inSkinSelect = False
                        party[partySelect] = None
                        skinSelect = 0
                    elif inCharSelect:
                        inCharSelect = False
                    elif inSetting:
                        inSetting = False
                    elif not inCharSelect:
                        doTransition('gameModeType', None, color=BLACK)

                button = screenWindow.buttonList['O']#, screenWindow.buttonList['Battle']]
                plus = loadSprite('plus0', f'plus.png', (0, 200), mouseCollide=True)
                button.name = ">>"
                button.x = plus.pos[0] - 150
                button.y = plus.pos[1]
                button.mainColor = (0, 255, 0)
                button.hoverColor = (0, 255, 130)
                button.width = 50
                button.height = 50
                button.thickness = 10
                button.draw()
                if button.clicked:
                    tempParty = []
                    for i in party:
                        if i != None:
                            tempParty.append(i)
                    for num, i in enumerate(tempParty):
                        if i != None:
                            del screenWindow.animatedSprites[i.name + "__Character_" + str(num)]
                    skinList = [0, 0, 0, 0, 0]
                    party = buildEnemyList(validAlly, 5)
                    party.reverse()

                button = screenWindow.buttonList['O']#, screenWindow.buttonList['Battle']]
                plus = loadSprite('plus0', f'plus.png', (0, 200), mouseCollide=True)
                button.name = ">>"
                button.x = plus.pos[0] - 150
                button.y = height - plus.pos[1]
                button.mainColor = (0, 255, 0)
                button.hoverColor = (0, 255, 130)
                button.width = 50
                button.height = 50
                button.thickness = 10
                button.draw()
                if button.clicked:
                    tempEnemy = []
                    for i in opponent:
                        if i != None:
                            tempEnemy.append(i)
                    for num, i in enumerate(tempEnemy):
                        if i != None:
                            del screenWindow.animatedSprites[i.name + "___Character_" + str(num)]
                    skinListEn = [0, 0, 0, 0, 0]
                    opponent = buildEnemyList(validEnemy, 5)
                    #opponent.reverse()

                if inSkinSelect:
                    button = screenWindow.buttonList['Confirm']#, screenWindow.buttonList['Battle']]
                    button.x = width - 300
                    button.y = 50
                    button.mainColor = (0, 200, 0)
                    button.hoverColor = (130, 200, 130)
                    button.width = 150
                    button.thickness = 10
                    button.draw()
                    if button.clicked:
                        inCharSelect = inSkinSelect = False
                        partySelect+=1
                        if partySelect>4:
                            partySelect=4
                        skinSelect = 0
                        inMoreInfo = False
                        infoType = 0
                        extraScroll = 0



                #if not inCharSelect:
                plus = loadSprite('plus2', f'plus.png', (0, 200), mouseCollide=True)
                button = screenWindow.buttonList['Battle']#, screenWindow.buttonList['Battle']]
                button.x = width/2 - 150
                button.y = plus.pos[1] - 150
                button.mainColor = (200, 0, 0)
                button.hoverColor = (200, 70, 70)
                button.width = 200
                button.thickness = 10
                button.draw()
                if button.clicked:
                    startBattle = True

                button = screenWindow.buttonList['Tutorial']#, screenWindow.buttonList['Battle']]
                button.x = width/2
                button.y = (height - plus.pos[1]) + 150
                button.mainColor = (200, 0, 0)
                button.hoverColor = (200, 70, 70)
                button.width = 250
                button.thickness = 10
                button.draw()
                if button.clicked:
                    startBattle = True
                    battleData = 'Tutorial'

                #plus = loadSprite('plus2', f'plus.png', (0, 200), mouseCollide=True)
                button = screenWindow.buttonList['Setting']#, screenWindow.buttonList['Battle']]
                button.x = width/2 + 150
                button.y = plus.pos[1] - 150
                button.mainColor = (200, 0, 200)
                button.hoverColor = (200, 70, 200)
                button.width = 200
                button.thickness = 10
                button.draw()
                if button.clicked:
                    inSetting = True
                    #doTransition('startBattle', True, color=BLACK)


                for i in range(0, 5):
                    drawRect(backGroundScreen.surface, (min(i*50, 255), 200, 200) ,(0, 100+i*40, width, 500-i*80))

                if rightPressed:
                    if not inSkinSelect:
                        partySelect += 1
                        if partySelect > 4:
                            partySelect = 0

                if leftPressed:
                    if not inSkinSelect:
                        partySelect -= 1
                        if partySelect < 0:
                            partySelect = 4

                if confirm:
                    if not inCharSelect:
                        inCharSelect = True
                    if inSkinSelect:
                        inCharSelect = inSkinSelect = False
                        partySelect+=1
                        if partySelect>4:
                            partySelect=4
                        skinSelect = 0


                if cancel:
                    if inSkinSelect:
                        inSkinSelect = False
                        party[partySelect] = None
                        skinSelect = 0
                        skinList[partySelect] = 0
                    elif inCharSelect:
                        inCharSelect = False
                    elif inSetting:
                        inSetting = False
                    elif not inCharSelect:
                        party[partySelect] = None




                #if special:
                    #inSetting = not inSetting
                if inSetting:
                    for num, i in enumerate(screenWindow.trigger.values()):
                        x = 300 + 400*(num%2)
                        y = 200 + 100 * (num//2)
                        i.x = x
                        i.y = y
                        i.draw()



                if startBattle and not inCharSelect:
                    partyBack = []
                    character.opponent = []
                    tempSkin = []
                    tempSkinEn = []
                    for num, i in enumerate(party):
                        if i != None:
                            tempSkin.append(skinList[num])
                            partyBack.append(i)

                    opponentBack = []
                    character.opponent = []
                    for num, i in enumerate(opponent):
                        if i != None:
                            tempSkinEn.append(skinListEn[num])
                            opponentBack.append(i)

                    theEnemyLeft = []
                    for num, i in enumerate(validEnemy):
                        foundAlly = False
                        for ally in partyBack:
                            if ally.name == i.name:
                                foundAlly = True
                                break
                        if not foundAlly:
                            theEnemyLeft.append(i)

                    backParty = []
                    partyDict = {}
                    partyList = {}
                    for i in partyBack:
                        if i.name in partyDict:
                            partyAlly = copy.deepcopy(i)
                            partyAlly.inventory = i.inventory
                            backParty.append(partyAlly)
                            if i.name not in partyList:
                                anotherAlly = copy.deepcopy(i)
                                anotherAlly.inventory = i.inventory
                                partyList[i.name] = [anotherAlly]
                                backParty[backParty.index(i)] = anotherAlly
                            partyList[i.name].append(partyAlly)
                        else:
                            partyDict[i.name] = i
                            backParty.append(i)
                    for i in partyList:
                        if len(partyList[i]) > 1:
                            for num, ally in enumerate(partyList[i]):
                                ally.name += f" {chr(num+65)}"
                    partyBack = backParty



                    backParty = []
                    partyDict = {}
                    partyList = {}
                    for i in opponentBack:
                        if i.name in partyDict:
                            partyAlly = copy.deepcopy(i)
                            partyAlly.inventory = i.inventory
                            backParty.append(partyAlly)
                            if i.name not in partyList:
                                anotherAlly = copy.deepcopy(i)
                                anotherAlly.inventory = i.inventory
                                partyList[i.name] = [anotherAlly]
                                backParty[backParty.index(i)] = anotherAlly
                                #print(id(anotherAlly), anotherAlly.name)
                            partyList[i.name].append(partyAlly)
                        else:
                            partyDict[i.name] = i
                            backParty.append(i)
                    for i in partyList:
                        if len(i) > 1:
                            for num, ally in enumerate(partyList[i]):
                                ally.name += f" {chr(num+65)}"
                                #print(id(ally), ally.name)
                    opponentBack = backParty
                    #for i in opponentBack:
                       # print(id(i), i.name)




                    #raise ValueError('Screw u')

                    character.opponent = opponentBack#random.sample(validEnemy, len(partyBack))

                    character.party = partyBack
                    for num, i in enumerate(partyBack):
                        i.skin = i.skinList[tempSkin[num]]
                    for num, i in enumerate(opponentBack):
                        i.skin = i.skinList[tempSkinEn[num]]
                    if (character.party != [] and character.opponent != []) or battleData != None:
                        screenWindow.sprites.clear()
                        screenWindow.animatedSprites.clear()
                        #with open('battle.py', 'r') as file:
                            #battleCode = file.read()
                        #exec(battleCode)
                        effects = {}
                        for num, i in enumerate(validAlly + validEnemy):
                            for buff in i.passiveBuff:
                                effects[buff.name] = buff
                            i.hpSet()
                        theAllies = copy.deepcopy(validAlly)
                        theEnemies = copy.deepcopy(validEnemy)
                        if not screenWindow.useWeb:
                            music.pause()
                        if screenWindow.useWeb:
                            screenWindow.texts.clear()
                            screenWindow.images.clear()
                        pygame.mixer.stop()
                        reworkingBattle.main(partyBack, opponentBack, usingDebug=True, battleData=battleData)#buildEnemyList(validEnemy, len(partyBack)), useSpeedTurn=True)
                        #if screenWindow.useWeb:
                            #screenWindow.texts.clear()
                            #screenWindow.images.clear()
                        hud.start_fade(BLACK, 255, 1)
                        screen.start_fade(BLACK, 255, 1)
                        screenWindow.backGroundScreen.start_fade(BLACK, 255, 1)
                        hud.camera_zoom = 3
                        screen.camera_zoom = 3
                        screenWindow.backGroundScreen.camera_zoom = 3
                        await reworkingBattle.battleRun()
                        pygame.mixer.stop()
                        battleData = None
                        #reworkingBattle.main(partyBack, [character.Zephyr])
                        #effects = {}
                        for num, i in enumerate(validAlly):
                            validAlly[num] = theAllies[num]
                            character.playerObj[i.name] = theAllies[num]

                        for num, i in enumerate(validEnemy):
                            validEnemy[num] = theEnemies[num]
                            character.opponentObj[i.name] = theEnemies[num]

                        for num, i in enumerate(validAlly + validEnemy):
                            passiveBuff = {}
                            for buff in i.passiveBuff:
                                passiveBuff[effects[buff.name]] = [False, False]
                            i.passiveBuff = passiveBuff
                        if not screenWindow.useWeb:
                            music = DynamicMusicPlayer(f"sounds/music/menuMusic.ogg", loop=True)
                            music.set_speed(0.9)
                        else:
                            #pygame.mixer.music.load(f'sounds/music/menuMusic.ogg')
                            #pygame.mixer.music.play(loops=-1)
                            playSound('music/menuMusic.ogg', -1)

                        hud.camera_shake = 0
                        backGroundScreen.camera_zoom = 1
                        backGroundScreen.camera_rotation = 0
                        party = [None, None, None, None, None]
                        opponent = [None, None, None, None, None]
                        skinListEn = [0, 0, 0, 0, 0]
                        skinList = [0, 0, 0, 0, 0]
                        partyBack = []
                        screenWindow.sprites.clear()
                        screenWindow.animatedSprites.clear()
                    startBattle = False

                for num in range(0, 5):
                    x = 150 + num*700/5 + 700/10
                    plus = loadSprite('plus' + str(num), f'plus.png', (0, 200), mouseCollide=True)
                    if party[num] != None:
                        plus.image = f'selectionIcon/{party[num].name}.png'
                        plus.baseScale = 0.5
                        #, (x, 300), mouseCollide=True, baseScale=0.5)
                        #plus.opacity=0
                        #icon = loadImg((f'selectionIcon/{party[num].name}.png', scale=0.5))
                        #blitObj(screen, icon, x, 300)
                    else:
                        plus.image = f'plus.png'
                        plus.baseScale = 1

                    if inCharSelect or inSetting:
                        plus.tweenPos((x, -200), 'circIn', 0.3+(4-num)*0.05, True)
                        plus.tweenOpacity(0, 'circOut', 0.3, True)
                    else:
                        plus.tweenPos((x, 200), 'circOut', 0.3+num*0.05, True)
                        plus.tweenOpacity(255, 'circIn', 0.1, True)

                    if not inCharSelect or inSetting:
                        xButton = Button(f'-{num}', 0, 0)
                        xButton.x = plus.pos[0] + 50 - (xButton.width+xButton.thickness)/2
                        xButton.y = plus.pos[1] - 50 - (xButton.height+xButton.thickness)/2
                        xButton.width = 35
                        xButton.height = 35
                        xButton.name = '-'
                        xButton.mainColor = (200, 0, 0)
                        xButton.hoverColor = (200, 130, 130)
                        xButton.draw()
                        if xButton.clicked:
                            if party[num] != None:
                                tempAlly = []
                                for stuff in party:
                                   if stuff != None:
                                       tempAlly.append(stuff)
                                for numAlly, ally in enumerate(tempAlly):
                                    del screenWindow.animatedSprites[ally.name + "__Character_" + str(numAlly)]
                            party[num] = None
                            skinList[num] = 0

                        elif mouseTouch(plus, True, True):
                            inCharSelect = True
                            partySelect = num
                            inOpponent = False

                for num in range(0, 5):
                    x = 150 + num*700/5 + 700/10
                    plus = loadSprite('plus' + str(num) + str(num), f'plus.png', (0, 500), mouseCollide=True)
                    if opponent[num] != None:
                        plus.image = f'selectionIcon/{opponent[num].name}.png'
                        plus.baseScale = 0.5
                        #, (x, 300), mouseCollide=True, baseScale=0.5)
                        #plus.opacity=0
                        #icon = loadImg((f'selectionIcon/{party[num].name}.png', scale=0.5))
                        #blitObj(screen, icon, x, 300)
                    else:
                        plus.image = f'plus.png'
                        plus.baseScale = 1

                    if inCharSelect or inSetting:
                        plus.tweenPos((x, height+200), 'circIn', 0.3+(4-num)*0.05, True)
                        plus.tweenOpacity(0, 'circOut', 0.3, True)
                    else:
                        plus.tweenPos((x, 500), 'circOut', 0.3+num*0.05, True)
                        plus.tweenOpacity(255, 'circIn', 0.1, True)

                    if not inCharSelect or inSetting:
                        xButton = Button(f'-{num}{num}', 0, 0)
                        xButton.x = plus.pos[0] + 50 - (xButton.width+xButton.thickness)/2
                        xButton.y = plus.pos[1] + 50 + (xButton.height+xButton.thickness)/2
                        xButton.width = 35
                        xButton.height = 35
                        xButton.name = '-'
                        xButton.mainColor = (200, 0, 0)
                        xButton.hoverColor = (200, 130, 130)
                        xButton.draw()
                        if xButton.clicked:
                            if opponent[num] != None:
                                tempEnemy = []
                                for stuff in opponent:
                                   if stuff != None:
                                       tempEnemy.append(stuff)
                                for numAlly, ally in enumerate(tempEnemy):
                                    del screenWindow.animatedSprites[ally.name + "___Character_" + str(numAlly)]
                            opponent[num] = None
                            skinListEn[num] = 0

                        elif mouseTouch(plus, True, True):
                            inCharSelect = True
                            opponentSelect = num
                            inOpponent = True

                tempParty = []
                tempSkin = []
                for num, stuff in enumerate(party):
                   if stuff != None:
                       tempParty.append(stuff)
                       tempSkin.append(skinList[num])
                anim = ['idle', 'attackPrep', 'attack', 'hurt', 'skill', 'death', 'dodge']


                for num, ally in enumerate(tempParty):
                    x = 200*((width/2)/500)/len(tempParty) + 400*(width/1000)/len(tempParty) * num
                    y = 350 #+ 3*num - 3*len(party)
                    charSprite = loadAnimatedSprite(ally.name + f"__Character_{num}", ally.name, pos=(width+400, y), baseScale=0.2)
                    charSprite.skin = ally.skinList[tempSkin[num]]
                    #print(tempSkin, ally.skinList[tempSkin[num]])
                    charX = charSprite.pos[0]
                    charY = charSprite.pos[1]
                    screenWindow.drawEllipse(screen, (0, 0, 0, 50), (charX-70, charY+200-130, 140, 20))
                    if frame%7 == 0 and previewMode:
                        animIndex = anim.index(charSprite.currentAnim) + 1
                        if animIndex > 6:
                            animIndex = 0
                        playAnimation(charSprite, anim[animIndex], False)
                    elif not previewMode:
                        playAnimation(charSprite, 'idle', False)
                    if not inCharSelect:
                        charSprite.tweenPos((x, y), "circOut", 0.3, True)
                    else:
                        charSprite.tweenPos((width+400, y), "circIn", 0.1, True)

                tempEnemy = []
                tempSkin = []
                for num, stuff in enumerate(opponent):
                   if stuff != None:
                       tempEnemy.append(stuff)
                       tempSkin.append(skinListEn[num])
                anim = ['idle', 'attackPrep', 'attack', 'hurt', 'skill', 'death', 'dodge']
                for num, ally in enumerate(tempEnemy):
                    x = 600*((width/2)/500) + 200*((width/2)/500)/len(tempEnemy) + 400*(width/1000)/len(tempEnemy) * num
                    y = 350 #+ 3*num - 3*len(party)
                    charSprite = loadAnimatedSprite(ally.name + f"___Character_{num}", ally.name, pos=(width+400, y), baseScale=0.2, flipX=True)
                    charSprite.skin = ally.skinList[tempSkin[num]]
                    #print(tempSkin, skinListEn, tempSkin[num])
                    #print(ally.name + f"___Character_{num}")
                    #charSprite.skin = ally.skin
                    charX = charSprite.pos[0]
                    charY = charSprite.pos[1]
                    screenWindow.drawEllipse(screen, (0, 0, 0, 100), (charX-70, charY+200-130, 140, 20))
                    if frame%7 == 0 and previewMode:
                        animIndex = anim.index(charSprite.currentAnim) + 1
                        if animIndex > 6:
                            animIndex = 0
                        playAnimation(charSprite, anim[animIndex], False)
                    elif not previewMode:
                        playAnimation(charSprite, 'idle', False)
                    if not inCharSelect:
                        charSprite.tweenPos((x, y), "circOut", 0.3, True)
                    else:
                        charSprite.tweenPos((width+400, y), "circIn", 0.1, True)


                if inCharSelect:
                    if scrollDown or downPressed:
                        mouseScroll -= 100
                    if scrollUp or upPressed:
                        mouseScroll += 100
                #mouseScroll = 0 if mouseScroll < 0 else 700 if mouseScroll > 700 else mouseScroll
                whichOne = party if not inOpponent else opponent
                whichSelect = partySelect if not inOpponent else opponentSelect
                whichAll = validAlly if not inOpponent else validEnemy
                for num, ally in enumerate(whichAll):
                    x = 50 + (num%3)*700/3 + 350/3
                    y = (num//3)*200 + 200 + mouseScroll
                    if not inCharSelect:
                        x = -100

                    allySprite = loadSprite(ally.name, f'selectionIcon/{ally.name}.png', baseScale=0.75, pos=(x, y), mouseCollide=True, layer=screenWindow.backGroundScreen)
                    allySprite.mouseCollide = True
                    classIcon = loadImg((f'classes/{ally.classes}.png', 0.55))
                    rumblerText = render_text(str(num+1).zfill(3), WHITE, 50, True, BLACK, 2)
                    if inSkinSelect:
                        rumblerText = render_text(str(num+1).zfill(3), WHITE, 50, True, BLACK, 2)
                    else:
                        rumblerText = render_text(ally.name, WHITE, 50, True, BLACK, 2)
                    blitObj(screen.surface, classIcon, allySprite.pos[0] - (allySprite.getSize()[0]/3)/scaleFactor , allySprite.pos[1] + (allySprite.getSize()[1]/3)/scaleFactor)
                    blitObj(screen.surface, rumblerText, allySprite.pos[0] , allySprite.pos[1] - (allySprite.getSize()[1]/3)/scaleFactor)
                    if not inSkinSelect:
                        drawRect(screen.surface, (0, 140, 220) ,(0, 0, width, 100))
                        #drawRect(screen.surface, (0, 200, 200) ,(0, 100, width, 500))
                        drawRect(screen.surface, (0, 140, 220) ,(0, height-100, width, 100))
                    if mouseTouch(allySprite, True, True) and not mouseTouch(upArrow, True, True) and not mouseTouch(downArrow, True, True):
                        inSkinSelect=True
                        whichOne[whichSelect] = ally


                    charSprite = loadAnimatedSprite(ally.name + "_Character", ally.name, pos=(-200, 250), baseScale=0.5, flipX=True)
                    charX = -400
                    charY = 300

                    if inSkinSelect:
                        x = -100
                        if ally == whichOne[whichSelect]:
                            allySprite.mouseCollide = False
                            button = screenWindow.buttonList['>']#, screenWindow.buttonList['Battle']]
                            button.x = 180
                            button.y = 320
                            button.mainColor = (200, 0, 200)
                            button.hoverColor = (200, 130, 200)
                            button.width = 40
                            button.thickness = 10
                            button.draw()
                            if rightPressed or button.clicked:
                                skinSelect += 1
                                skinSelect = 0 if skinSelect >= len(whichOne[whichSelect].skinList) else skinSelect
                                if isinstance(ally, character.Player):
                                    skinList[whichSelect] = skinSelect
                                else:
                                    skinListEn[whichSelect] = skinSelect

                            button = screenWindow.buttonList['<']#, screenWindow.buttonList['Battle']]
                            button.x = 80
                            button.y = 320
                            button.mainColor = (200, 0, 200)
                            button.hoverColor = (200, 130, 200)
                            button.width = 40
                            button.thickness = 10
                            button.draw()
                            if leftPressed or button.clicked:
                                skinSelect -= 1
                                skinSelect = len(whichOne[whichSelect].skinList) - 1 if skinSelect < 0 else skinSelect
                                if isinstance(ally, character.Player):
                                    skinList[whichSelect] = skinSelect
                                else:
                                    skinListEn[whichSelect] = skinSelect





                            darkColor = []
                            for i in whichOne[whichSelect].color:
                                darkColor.append(i*0.65)
                            drawRect(backGroundScreen.surface, darkColor, (0, 450, width, height-450))
                            darkColor = []
                            for i in whichOne[whichSelect].color:
                                darkColor.append(i*0.75)
                            for i in range(0, 5):
                                theColor = (
                                            min(whichOne[whichSelect].color[0]+i*20, 255),
                                            min(whichOne[whichSelect].color[1]+i*20, 255),
                                            min(whichOne[whichSelect].color[2]+i*20, 255)
                                            )
                                drawRect(backGroundScreen.surface, theColor,(0, 100+i*40, width, 500-i*80))
                            #drawRect(screen.surface, party[partySelect].color, (0, 0, width, 450))
                            drawRect(screen.surface, darkColor, (0, 0, width, 100))
                            x = 130
                            y = 200
                            charX = width - 200
                            charY = 300

                            charSprite.skin = whichOne[whichSelect].skinList[skinSelect]
                            whichOne[whichSelect].skin = whichOne[whichSelect].skinList[skinSelect]
                            statList = ['health', 'attack', 'defense', 'speed', 'productivity', 'range']
                            shortStat = {'level':'LVL', 'health':'HP', 'attack':'ATK', 'defense':'DEF', 'speed':'SPD', 'productivity':'PRD', 'range':'RGE', 'mana':'MP'}
                            ally = whichOne[whichSelect]
                            ally.levelUp(0)
                            playerStat = {'level':ally.level, 'health':ally.maxhp, 'attack':ally.attack, 'defense':ally.defense, 'speed':ally.speed, 'productivity':ally.productivity, 'range':ally.range, 'mana':ally.maxMana}
                            setStat = {'health':ally.base[0], 'attack':ally.base[1], 'defense':ally.base[2], 'speed':ally.base[3], 'productivity':ally.base[5], 'range':ally.base[4]}
                            statusX = 55
                            statusY = 100
                            statWidth = 580
                            statHeight = 210
                            for statNum, stat in enumerate(statList):
                                statX = statusX + 200 + 130*(statNum//2)
                                statY = statusY + 15 + (statNum%2)*120 + 5*math.sin((frame/8)*math.pi+statNum/8)
                                statImg = loadImg((f'stats/{stat}.png', 0.95))
                                blitObj(hud, statImg, statX, statY, pivot_type='topleft')
                                statText = render_text(f'{str(playerStat[stat])} ({str(setStat[stat])})', WHITE, 40, True, BLACK, 2)
                                blitObj(hud, statText, statX+95/2, statY+95/(4/3))
                                shortText = render_text(str(shortStat[stat]), WHITE, 50, True, BLACK, 2)
                                blitObj(hud, shortText, statX+95/2, statY)
                            darkColor = []
                            for i in whichOne[whichSelect].color:
                                darkColor.append(i*0.85)
                            drawRect(hud.surface, darkColor, (50, 400, 580, 250))
                            drawRect(hud.surface, BLACK, (60, 410, 560, 230))
                            blit_text(hud.surface, whichOne[whichSelect].info, pygame.Rect(60, 425, 560, 280), "gameFont.otf", 40, WHITE)

                            nameText = render_text(f'{whichOne[whichSelect].name}     |     {whichOne[whichSelect].skin}', WHITE, 60, True, BLACK, 3)
                            blitObj(hud.surface, nameText, x=55, y=20, pivot_type='topleft')
                            #drawRect()

                    charSprite.tweenPos((charX, charY), "circOut", 0.4, True)



                        #inCharSelect = False


                    allySprite.tweenPos((x, y), "circOut", 0.1, True)
                mouseScroll = -1500 if mouseScroll < -1500 else 0 if mouseScroll > 0 else mouseScroll





asyncio.run(main())
if not screenWindow.useWeb:
    #sys.exit()
    pygame.quit()
    music.stop()
    sys.exit()






