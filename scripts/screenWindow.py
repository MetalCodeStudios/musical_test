import sys
import os
os.environ["SDL_RENDER_SCALE_QUALITY"] = "2"
import xml.etree.ElementTree as ET
import json
import math
import copy
# Save the original stdout
original_stdout = sys.stdout
# Redirect stdout to the console
sys.stdout = sys.__stdout__
import time
import pygame
import ctypes
import random

fullscreen = False
#window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
scaleFactor = 0.5

textures = {}
renderTexture = {}
baseImg = {}
images = {}
texts = {}
shapes = {}
sprites = {}
battleVariables = {}
frame = 0
deltaTime = 1/30
controlVar = [ ['Botplay', False], ['Can Gain Xp', False], ['Hard Mode', False] ]

musicVolume = 1
soundVolume = 1

trigger = {}

mouseDown = mouseHold = False

fontType = 0

# Camera Settings
camZoom = 1 # Default Camera Zoom, 1 means no camera zoom
camColor = None # For the color of Camera Flash
camShake = 0 # To shake the game itself, 0 means no shaking camera
camFade = 0 # For Camera Flash and how long it takes for Camera Flash to fade away

def drawRect(surface, color, x, y=0, width=0, height=0, drawDirect=True, border=0):
    """
    Draws a rectangle on the given surface (CameraSurface or raw Surface).
    Position is absolute — no camera offset.
    """
    if useTexture:
        drawDirect =False
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface
    width = int(width)

    # Support tuple or pygame.Rect for position
    if isinstance(x, (tuple, pygame.Rect)):
        rect = pygame.Rect(x)
    else:
        rect = pygame.Rect(x, y, width, height)

    if rect.width == 0 or rect.height == 0:
        return  # Nothing to draw

    key = ('rect', color, rect.size)
    rect.width *= scaleFactor
    rect.height *= scaleFactor
    rect.x *= scaleFactor
    rect.y *= scaleFactor

    if not drawDirect:
        if key not in shapes:
            rectSurface = pygame.Surface((abs(rect.width), abs(rect.height)), pygame.SRCALPHA)
            pygame.draw.rect(rectSurface, color, (0, 0, rect.width, rect.height))
            shapes[key] = rectSurface

        if useTexture:
            theTexture = loadTexture(key, shapes[key], rect.x, rect.y)
            blitObj(surface, theTexture, rect, pivot_type='topleft')
        else:
            blitObj(draw_surface, shapes[key], rect, pivot_type='topleft')
    else:
        pygame.draw.rect(draw_surface, color, rect, border)

def debug_test(surface):
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface
    print("fnction-scope print is alive!")

def drawCircle(surface, color, center, radius, thickness=0, borderColor=(255, 255, 255), drawDirect=True):
    """
    Draws a circle with optional border. 'center' is only used for final blit position.
    """
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface

    if radius <= 0:
        return  # Invalid radius, skip drawing

    radius *= scaleFactor
    surf_size = 2 * radius
    circSurface = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)

    key = ('circle', color, radius, thickness, borderColor)

    if drawDirect == False:
        if key not in shapes:
            if thickness != 0:
                # Border circle
                pygame.draw.circle(circSurface, borderColor, (radius, radius), radius + thickness)
            pygame.draw.circle(circSurface, color, (radius, radius), radius)
            shapes[key] = circSurface

        if useTexture:
            theTexture = loadTexture(key, shapes[key], rect.x, rect.y)
            #blitObj(surface, theTexture, rect, pivot_type='topleft')
            blitObj(surface, theTexture, center[0], center[1])
        else:
            blitObj(draw_surface, shapes[key], center[0], center[1])
    else:
        if thickness != 0:
                # Border circle
            pygame.draw.circle(draw_surface, borderColor, (center[0]*scaleFactor, center[1]*scaleFactor), radius + thickness)
        pygame.draw.circle(draw_surface, color, (center[0]*scaleFactor, center[1]*scaleFactor), radius)



def drawRing(surface, color, center, radius, ringThickness, borderThickness, borderColor, drawDirect=False):
    """
    Draws a ring with specified thickness and optional border.
    The 'center' is only for the blit placement.
    """
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface

    if radius <= 0 or ringThickness <= 0:
        return
    radius, ringThickness, borderThickness = int(radius)* scaleFactor, int(ringThickness)* scaleFactor, int(borderThickness)* scaleFactor
    outer_radius = (radius + borderThickness)
    surf_size = 2 * outer_radius
    center_pt = (outer_radius, outer_radius)
    #print(outer_radius, surf_size)

    key = ('ring', color, radius, ringThickness, borderThickness, borderColor)

    if not drawDirect:
        if key not in shapes:
            ringSurface = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)

            # Draw outer border
            if borderThickness > 0:
                pygame.draw.circle(ringSurface, borderColor, center_pt, outer_radius)
                pygame.draw.circle(ringSurface, color, center_pt, radius)
                pygame.draw.circle(ringSurface, borderColor, center_pt, radius - ringThickness)
                pygame.draw.circle(ringSurface, (0, 0, 0, 0), center_pt, radius - ringThickness - borderThickness)
            else:
                pygame.draw.circle(ringSurface, color, center_pt, radius, max(int(ringThickness), 1))

            shapes[key] = ringSurface

        blitObj(draw_surface, shapes[key], center[0], center[1])
    else:
        if borderThickness > 0:
            pygame.draw.circle(draw_surface, borderColor, center, outer_radius)
            pygame.draw.circle(draw_surface, color, center, radius)
            pygame.draw.circle(draw_surface, borderColor, center, radius - ringThickness)
            pygame.draw.circle(draw_surface, (0, 0, 0, 0), center, radius - ringThickness - borderThickness)
        else:
            pygame.draw.circle(draw_surface, color, center, radius, ringThickness)






def drawLine(surface, color, start_pos, end_pos, width=1):
    """
    Wrapper for pygame.draw.line.
    Parameters match pygame exactly.
    """
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface
    return pygame.draw.line(draw_surface, color, start_pos, end_pos, width)

def drawPolygon(surface, color, points, width=0):
    """
    Wrapper for pygame.draw.polygon.
    Parameters match pygame exactly.
    """
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface
    return pygame.draw.polygon(draw_surface, color, points, width)

def drawEllipse(surface, color, rect, width=0):
    """
    Wrapper for pygame.draw.ellipse.
    Parameters match pygame exactly.
    """
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface
    return pygame.draw.ellipse(draw_surface, color, rect, width)

def drawArc(surface, color, rect, start_angle, stop_angle, width=1):
    """
    Wrapper for pygame.draw.arc.
    Parameters match pygame exactly.
    """
    draw_surface = surface.surface if hasattr(surface, 'surface') else surface
    return pygame.draw.arc(draw_surface, color, rect, start_angle, stop_angle, width)
imageCache = {}
def blitObj(destSurface, srceSurface, x, y=0, pivot_type="center", custom_pivot_point=None):
    #return True
    oriSurface = destSurface
    srceSurface = srceSurface.surface if hasattr(srceSurface, 'surface') else srceSurface
    destSurface = destSurface.surface if hasattr(destSurface, 'surface') else destSurface
    destSurface = destSurface.window if hasattr(destSurface, 'window') else destSurface
    rect = srceSurface.get_rect()
    if isinstance(x, pygame.Rect):
        y = x.y*scaleFactor
        x = x.x*scaleFactor
    x *= scaleFactor
    y *= scaleFactor
    if useTexture:
        if isinstance(srceSurface, Img):
            if hasattr(oriSurface, 'texture'):
                #renderer = renderer
                srceSurface.x, srceSurface.y = x, y
                srceSurface.renderTexture(renderer, oriSurface, pivot_type)
        return True

    if custom_pivot_point is not None:
        # custom_pivot_point is like (0.5, 0.5) for center, (1.0, 1.0) for bottom-right
        pivot_x = rect.width * custom_pivot_point[0]
        pivot_y = rect.height * custom_pivot_point[1]
    else:
        # Using one of the predefined pivot types
        setattr(rect, pivot_type, (x, y))
        pivot_x = x - rect.x
        pivot_y = y - rect.y
    if id(srceSurface) in imageCache and 1==0:
        cacheKey = imageCache[id(srceSurface)]
        textures[cacheKey] = Texture.from_surface(renderer, srceSurface)
        renderTexture[(cacheKey, (x,y), destSurface)] = Texture.from_surface(renderer, baseImg[cacheKey[0][0]])

    # Adjust top-left position based on pivot
    blit_x = x - pivot_x
    blit_y = y - pivot_y
    destSurface.blit(srceSurface, (blit_x, blit_y))


class CameraSurface:
    def __init__(self, name, native_res, fullscreen=False, parallax_factor=1.0):
        self.name = name
        self.native_width, self.native_height = native_res
        self.fullscreen = fullscreen
        self.surface = pygame.Surface(native_res, pygame.SRCALPHA)
        self.tint_surface = pygame.Surface((self.native_width, self.native_height), pygame.SRCALPHA)
        if useWeb:
            self.texture = None
        else:
            self.texture = Texture(renderer, native_res, target=True) #Unused as of now, may be used for draw() due to Sprites and AnimatedClass having imageName, sclaing, angle, etc as seperate atrributes
        #May need a cache Texture though
        sys.stdout = original_stdout
        # Camera properties
        self.cameraX = 0
        self.cameraY = 0
        self.camera_zoom = 1.0
        self.camera_rotation = 0
        self.camera_shake = 0
        self.camera_fade = 0
        self.camera_color = (0, 0, 0)
        self.parallax = parallax_factor

        # Tweens
        self.zoom_tween = None
        self.fade_tween = None
        self.shake_tween = None
        self.rotate_tween = None
        self.move_tween = None

    def fill(self, color):
        self.surface.fill(color)

    def get_rect(self, topleft=(0, 0), midtop=(0, 0), topright=(0, 0), midright=(0, 0), center=(0, 0), midleft=(0, 0), bottomleft=(0, 0), midbottom=(0, 0), bottomright=(0, 0)):
        return self.surface.get_rect()

    def blit(self, srceSurface, x, y=0, pivot_type="topleft", custom_pivot_point=None):
        if isinstance(x, tuple):
            y = x[1]
            x = x[0]
        if isinstance(x, pygame.Rect):
            y = x.y
            x = x.x
        rect = srceSurface.get_rect()

        if custom_pivot_point is not None:
            pivot_x = rect.width * custom_pivot_point[0]
            pivot_y = rect.height * custom_pivot_point[1]
        else:
            setattr(rect, pivot_type, (x, y))
            pivot_x = x - rect.x
            pivot_y = y - rect.y

        blit_x = x - pivot_x
        blit_y = y - pivot_y

        self.surface.blit(srceSurface, (blit_x, blit_y))

    # Tweening commands
    def start_zoom(self, target_zoom, duration):
        self.zoom_tween = {
            'start': self.camera_zoom,
            'end': target_zoom,
            'duration': duration,
            'elapsed': 0
        }

    def start_shake(self, intensity, duration):
        self.shake_tween = {
            'start': intensity,
            'end': 0,
            'duration': duration,
            'elapsed': 0
        }

    def start_fade(self, color, alpha, duration):
        self.camera_color = color
        self.camera_fade = alpha
        self.fade_tween = {
            'start': self.camera_fade,
            'end': alpha,
            'duration': duration,
            'elapsed': 0
        }

    def start_rotation(self, angle, duration):
        self.rotate_tween = {
            'start': self.camera_rotation,
            'end': angle,
            'duration': duration,
            'elapsed': 0
        }

    def move_to(self, targetX, targetY, duration):
        self.move_tween = {
            'startX': self.cameraX,
            'startY': self.cameraY,
            'endX': targetX,
            'endY': targetY,
            'duration': duration,
            'elapsed': 0
        }

    def update(self, deltaTime):
        # Zoom
        if self.zoom_tween or True:
            #t = self.zoom_tween
            #t['elapsed'] += deltaTime
            #p = min(t['elapsed'] / t['duration'], 1)
            self.camera_zoom -= (self.camera_zoom - 1) / 7 * deltaTime#t['start'] + (t['end'] - t['start']) * (1 - (1 - p) ** 2)
            self.camera_zoom = 1 if self.camera_zoom <= 0 else self.camera_zoom
            #if p >= 100: self.zoom_tween = None

        # Shake
        if self.shake_tween:
            t = self.shake_tween
            t['elapsed'] += deltaTime
            p = min(t['elapsed'] / t['duration'], 1)
            self.camera_shake -= 2 * deltaTime #int(t['start'] + (t['end'] - t['start']) * ease_out_quad(p))
            self.camera_shake = 0.1 if self.camera_shake <= 0 else self.camera_shake
            if p >= 100: self.shake_tween = None

        # Fade
        if self.fade_tween and True:
            t = self.fade_tween
            t['elapsed'] += deltaTime
            p = min(t['elapsed'] / t['duration'], 1)
            self.camera_fade -= (self.camera_fade) / 15 #* (deltaTime) #int(t['start'] + (t['end'] - t['start']) * ease_out_quad(p))
            self.camera_fade = 0 if self.camera_fade < 0.1 else self.camera_fade
            if p >= 100: self.fade_tween = None

        # Rotation
        if self.rotate_tween:
            t = self.rotate_tween
            t['elapsed'] += deltaTime
            p = min(t['elapsed'] / t['duration'], 1)
            self.camera_rotation -= (self.camera_rotation) / 5 * deltaTime
            #self.camera_rotation = t['start'] + (t['end'] - t['start']) * ease_out_quad(p)
            if p >= 100: self.rotate_tween = None

        # Move
        if self.move_tween:
            t = self.move_tween
            t['elapsed'] += deltaTime
            p = min(t['elapsed'] / t['duration'], 1)
            self.cameraX -= (self.cameraX) / 5 * deltaTime #t['startX'] + (t['endX'] - t['startX']) * ease_out_quad(p)
            self.cameraY -= (self.cameraY) / 5 * deltaTime #t['startY'] + (t['endY'] - t['startY']) * ease_out_quad(p)
            if p >= 100: self.move_tween = None

    def clear(self, color=(0,0,0,0)):
        if useWeb:
            self.surface.fill(color)
        else:
            renderer.target = self.texture
            self.texture.blend_mode = pygame.BLENDMODE_BLEND
            renderer.draw_color = color
            renderer.clear()
            renderer.target = None

    def render_to(self, destSurface):
        # Apply camera shake to position
        #Texture.from_surface(renderer, surface)
        self.update(deltaTime)
        destWidth, destHeight = destSurface.get_size()
        destSurface = destSurface.window if hasattr(destSurface, 'window') else destSurface
        shakeX = random.randint(int(-self.camera_shake), int(self.camera_shake)) if self.camera_shake > 0 else 0
        shakeY = random.randint(int(-self.camera_shake), int(self.camera_shake)) if self.camera_shake > 0 else 0

        # Calculate transformation pivot point
        centerX = destWidth // 2 + self.cameraX#destSurface.get_width() // 2
        centerY = destHeight // 2 + self.cameraY#destSurface.get_height() // 2

        # Translate and zoom camera view
        parallaxX = self.cameraX * self.parallax
        parallaxY = self.cameraY * self.parallax
        if parallaxX != 0 and parallaxY != 0 and 1==0:
            offset_surface = pygame.Surface((self.native_width, self.native_height), pygame.SRCALPHA)
            offset_surface.blit(self.surface, (-parallaxX, -parallaxY))
        else:
            offset_surface = self.surface

        # Scale + rotate
        if self.camera_zoom != 1 and useWeb:
            scaled_surface = scaleObj(offset_surface, self.camera_zoom)
        else:
            scaled_surface = offset_surface
        if self.camera_rotation != 0 and useWeb:
            rotated_surface = pygame.transform.rotate(scaled_surface, self.camera_rotation)
        else:
            rotated_surface = scaled_surface

        final_rect = rotated_surface.get_rect(center=(centerX + shakeX, centerY + shakeY))
        if not useWeb:
            final_rect.width *= self.camera_zoom
            final_rect.height *= self.camera_zoom
        final_rect.center = (centerX + shakeX, centerY + shakeY)

        #print(self.name, final_rect)

        # Clear the renderer
        if not useWeb:
            if useTexture:
                self.texture.draw()
            else:
                texture = Texture.from_surface(renderer, self.surface)
                texture.draw(dstrect=final_rect, angle=self.camera_rotation)
                del texture
        else:
            #finalSurf = scaleObj(self.surface, self.camera_zoom)
            source_width, source_height = self.surface.get_size()

            crop_x = (source_width - width) // 2
            crop_y = (source_height - height) // 2

            # Safety clamp: if source is smaller than crop, we adjust to avoid negative rects
            crop_x = max(0, crop_x)
            crop_y = max(0, crop_y)
            CROP_WIDTH = min(width, source_width)
            CROP_HEIGHT = min(height, source_height)

            # Make a rect representing the crop area from the center
            crop_rect = pygame.Rect(crop_x, crop_y, CROP_WIDTH, CROP_HEIGHT)
            destSurface.blit(rotated_surface, final_rect, crop_rect)

        # Render the texture
        #renderer.blit(texture)  # Render the texture

        # Present the result on the screen
        #renderer.present()
        #destSurface.blit(rotated_surface, final_rect)

        # Fade overlay
        if self.camera_fade > 0 and not useWeb:
            oldTarget = renderer.target
            fade_surf = Texture(renderer, (destWidth, destHeight), target=True)#pygame.Surface(destSurface.size)
            renderer.target = fade_surf
            fade_surf.blend_mode= pygame.BLENDMODE_BLEND
            renderer.draw_color = (int(self.camera_color[0]), int(self.camera_color[1]), int(self.camera_color[2]), int(self.camera_fade))
            #fade_surf.color = (int(self.camera_color[0]), int(self.camera_color[1]), int(self.camera_color[2]), int(self.camera_fade))
            fade_surf.alpha = self.camera_fade
            renderer.clear()
            renderer.target = oldTarget
            fade_surf.draw(dstrect=(0,0))
            del fade_surf
        elif useWeb and self.camera_fade > 0:
            #self.tint_surface.fill(s
            self.tint_surface.fill(self.camera_color)
            self.tint_surface.set_alpha(self.camera_fade)
            destSurface.blit(self.tint_surface, (0,0))
            #texture = Texture.from_surface(renderer, fade_surf)
            #texture.draw(dstrect=(0,0))
            #destSurface.blit(fade_surf, (0, 0))

    def resize(self, new_resolution):
        #self.native_width, self.native_height = new_resolution
        self.surface = pygame.Surface(new_resolution, pygame.SRCALPHA)

class startWindow:
    def __init__(self, title="Intense Rumble", width=1000*scaleFactor, height=700*scaleFactor):
        self._width = width
        self._height = height
        if not useWeb:
            self.window = Window(title, size=(width, height))
            #self.window.borderless = True
            self.window.set_icon(pygame.image.load(f'sprites/windowIcon.png'))# No resizable nonsense
            self.renderer = Renderer(self.window)
            self.renderer.logical_size = (width, height)
        else:
            pygame.init()
            self.window = pygame.display.set_mode((width, height))
            pygame.display.set_icon(pygame.image.load(f'sprites/windowIcon.png'))
            pygame.display.set_caption(title)
            self.renderer = None

        ## Optional: Set logical size for consistent rendering if you plan to scale content

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_rect(self):
        return pygame.Rect(0, 0, self._width, self._height)

    def get_size(self):
        if fullscreen:
            return pygame.display.get_desktop_sizes()[0]
        return self._width, self._height

    def get_renderer(self):
        return self.renderer

useWeb = True
if not useWeb:
    from pygame._sdl2 import Window, Renderer, Texture, sdl2
    window = startWindow()
    renderer = window.get_renderer()
    pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)
    from pyo import *
else:
    #window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF, depth=0, vsync=True)
    window = startWindow()
    renderer = None
width, height = 1000, 700 #Window Dimension
widthy, heighty = width*scaleFactor, height*scaleFactor
screenX, screenY = 1, 1
screen = CameraSurface('screen', (widthy, heighty))
hud = CameraSurface('hud', (widthy, heighty))
backGroundScreen = CameraSurface('background', (widthy, heighty), parallax_factor=0.5)
#pygame.display.set_icon(pygame.image.load(f'sprites/windowIcon.png'))
#window2 = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock() #Starts up the FPS # Window Tag I think
useTexture = False
def changeSize(x, y, fullscreen=False):
    global widthy, heighty, screenX, screenY, screen, window, width, height, renderer
    #widthy, heighty = x, y
    #width, height = x, y
    if fullscreen:
        width, height = pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]
        #widthy, heighty = window.get_size()
        screenX, screenY = 1, 1
        window.window.size = (width, height)
        window._width, window._height = width, height
        renderer.logical_size = (width, height)
        window.window.set_fullscreen(True)
        #window.window.size = (1, 1)
    else:
        #screenX, screenY = widthy / width, heighty / height
        width, height = 1000, 700
        window.window.set_windowed()
        window.window.size = (1000, 700)
        renderer.logical_size = (1000, 700)
        #renderer.logical_size = (1000, 700)
    #window.window.size = (x, y)
    #renderer.logical_size = (1000, 700)
    #screen = pygame.Surface((widthy, heighty), pygame.SRCALPHA)
    window._width, window._height = width, height
    screen.surface = pygame.Surface((width, height), pygame.SRCALPHA)
    hud.surface = pygame.Surface((width, height), pygame.SRCALPHA)
    backGroundScreen.surface = pygame.Surface((width, height), pygame.SRCALPHA)

def rotateObj(object, angle):
    return pygame.transform.rotate(object, angle)

antiAlias = True
def scaleObj(object, scale, usesmooth=antiAlias):
    x = object.get_width()
    y = object.get_height()
    if isinstance(scale, tuple) and len(scale) == 2:
        if useTexture:
            object.scaleX = scale[0]
            object.scaleY = scale[1]
            return object
        if usesmooth:
            return pygame.transform.smoothscale(object, (abs(scale[0]) * x, abs(scale[1]) * y))
        else:
            return pygame.transform.scale(object, (abs(scale[0]) * x, abs(scale[1]) * y))
    else:
        if useTexture:
            object.scaleX = scale
            object.scaleY = scale
            return object
        if usesmooth:
            return pygame.transform.smoothscale(object, (abs(scale) * x, abs(scale) * y))
        else:
            return pygame.transform.scale(object, (abs(scale) * x, abs(scale) * y))

#import pygame
import re

#pygame.init()

texts = {}

color_map = {
    "red": (255, 0, 0),
    "blue": (0, 128, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 100, 0),
    "white": (255, 255, 255),
    "cyan": (0, 200, 255),
    "purple": (255, 0, 255),
    "black": (0, 0, 0),
    "default": (0, 0, 0),
}

# Load fonts
def get_font(size, bold=False, italic=False):
    if fontType == 0:
        font = pygame.font.Font("gameFont.otf", int(size * scaleFactor * 0.9))
    else:
        font = pygame.font.Font("undertale.ttf", int(size * scaleFactor * 0.9))
    font.set_bold(bold)
    font.set_italic(italic)
    return font

def parse_color(tag):
    if tag.startswith('#'):
        try:
            r = int(tag[1:3], 16)
            g = int(tag[3:5], 16)
            b = int(tag[5:7], 16)
            return (r, g, b)
        except:
            return color_map["default"]
    return color_map.get(tag, color_map["default"])

def parse_text(text):
    tag_pattern = re.compile(r'\[(/?)(\#?[a-zA-Z0-9]+|b|i)\]')
    segments = []
    stack = []

    last_end = 0
    for match in tag_pattern.finditer(text):
        start, end = match.span()
        is_end = match.group(1) == '/'
        tag = match.group(2)

        if start > last_end:
            seg_text = text[last_end:start]
            current_color = color_map["default"]
            bold = False
            italic = False

            for t in stack:
                if t == "b":
                    bold = True
                elif t == "i":
                    italic = True
                else:
                    current_color = parse_color(t)

            segments.append((seg_text, current_color, bold, italic))

        if not is_end:
            stack.append(tag)
        else:
            if tag in stack:
                stack.remove(tag)
        last_end = end

    if last_end < len(text):
        seg_text = text[last_end:]
        current_color = color_map["default"]
        bold = False
        italic = False
        for t in stack:
            if t == "b":
                bold = True
            elif t == "i":
                italic = True
            else:
                current_color = parse_color(t)
        segments.append((seg_text, current_color, bold, italic))

    return segments

def render_text(text, color, size, border=False, border_color=(0, 0, 0), border_thickness=1, max_width=None, angle=0, frame=0):
    global texts
    color_map['default'] = color
    key = text + str(color) + str(size) + str(border) + str(border_color) + str(border_thickness) + str(angle) + str(max_width)
    if key in texts:
        return texts[key]

    border_thickness_scaled = round(border_thickness * scaleFactor)

    # Break into lines (manual \n)
    lines_raw = text.split('\n')
    all_lines = []

    for raw_line in lines_raw:
        segments = parse_text(raw_line)
        if not max_width:
            all_lines.append(segments)
        else:
            # Word wrap
            wrapped_lines = []
            current_line = []
            line_width = 0
            for seg_text, seg_color, seg_bold, seg_italic in segments:
                words = seg_text.split(" ")
                for i, word in enumerate(words):
                    display_word = word + (" " if i < len(words) - 1 else "")
                    font = get_font(size, seg_bold, seg_italic)
                    surf = font.render(display_word, antiAlias, seg_color)
                    word_width = surf.get_width()

                    if line_width + word_width > max_width and current_line:
                        wrapped_lines.append(current_line)
                        current_line = []
                        line_width = 0

                    current_line.append((display_word, seg_color, seg_bold, seg_italic))
                    line_width += word_width
            if current_line:
                wrapped_lines.append(current_line)
            all_lines.extend(wrapped_lines)

    # Render lines
    rendered_lines = []
    max_line_width = 0
    total_height = 0

    for line in all_lines:
        line_surfs = []
        line_height = 0
        line_width = 0

        for seg_text, seg_color, seg_bold, seg_italic in line:
            font = get_font(size, seg_bold, seg_italic)
            if border:
                #print(seg_text)
                base = font.render(seg_text, antiAlias, border_color).convert_alpha()
                bordered = pygame.Surface(
                    (base.get_width() + border_thickness_scaled * 2,
                     base.get_height() + border_thickness_scaled * 2),
                    pygame.SRCALPHA
                )

                for dx in range(-border_thickness_scaled, border_thickness_scaled + 1):
                    for dy in range(-border_thickness_scaled, border_thickness_scaled + 1):
                        if dx != 0 or dy != 0:
                            bordered.blit(base, (border_thickness_scaled + dx, border_thickness_scaled + dy))

                main = font.render(seg_text, antiAlias, seg_color).convert_alpha()
                bordered.blit(main, (border_thickness_scaled, border_thickness_scaled))
                seg_surf = bordered
            else:
                #print(seg_text)
                seg_surf = font.render(seg_text, antiAlias, seg_color).convert_alpha()

            line_surfs.append(seg_surf)
            line_width += seg_surf.get_width()
            line_height = max(line_height, seg_surf.get_height())

        line_surface = pygame.Surface((line_width, line_height), pygame.SRCALPHA)
        x = 0
        for seg_surf in line_surfs:
            line_surface.blit(seg_surf, (x, 0))
            x += seg_surf.get_width()

        rendered_lines.append(line_surface)
        max_line_width = max(max_line_width, line_width)
        total_height += line_height

    # Combine all lines into final surface
    final_surface = pygame.Surface((max_line_width, total_height), pygame.SRCALPHA)
    y = 0
    for line_surf in rendered_lines:
        final_surface.blit(line_surf, (0, y))
        y += line_surf.get_height()

    # Apply rotation
    final_surface = pygame.transform.rotate(final_surface, angle)
    texts[key] = final_surface
    return final_surface


# -------- Img Class -------- #
class Img:
    def __init__(self, name, texture, x=0, y=0, scaleX=1.0, scaleY=1.0, angle=0, flipx=False, flipy=False, color=WHITE, opacity=255):
        self.name = name
        self.texture = texture
        #self.texture.target = True
        self.texture.blend_mode = pygame.BLENDMODE_BLEND
        self.x = x
        self.y = y
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.angle = angle
        self.flipx = flipx
        self.flipy = flipy

        self.width = texture.width
        self.height = texture.height

        self.pivot = (0, 0)
        self.color = color
        self.opacity = opacity

    def get_width(self):
        w = int(self.width * self.scaleX)
        return w

    def get_height(self):
        h = int(self.height * self.scaleY)
        return h

    def get_size(self):
        w = int(self.width * self.scaleX)
        h = int(self.height * self.scaleY)
        return w, h

    def get_alpha(self):
        return self.opacity

    def set_alpha(self, alpha):
        self.opacity = alpha

    def blendColor(self, rgba_tuple):
        self.color_mod = rgba_tuple
        self.texture.color = rgba_tuple[:3]
        self.texture.alpha = rgba_tuple[3]

    def setPivot(self, pivot_tuple):
        self.pivot = pivot_tuple

    def get_rect(self, **kwargs):
        """
        Returns a pygame.Rect correctly positioned based on a given anchor keyword.

        Valid kwargs include: center, topleft, midtop, midbottom, bottomleft,
        bottomright, topright, midleft, midright.

        Example:
            sprite.get_rect(center=(100, 200))
        """
        w = int(self.width * self.scaleX)
        h = int(self.height * self.scaleY)
        rect = pygame.Rect(0, 0, w, h)

        # Determine which keyword was used
        valid_keys = [
            'center', 'topleft', 'midtop', 'midbottom',
            'bottomleft', 'bottomright', 'topright',
            'midleft', 'midright'
        ]

        for key in valid_keys:
            if key in kwargs:
                setattr(rect, key, kwargs[key])
                break
        else:
            # If no valid anchor point is provided, fall back to self.x, self.y as topleft
            rect.topleft = (self.x, self.y)

        return rect


    def renderTexture(self, renderer, destTexture=None, pivotPoint='center'):
        # Get the destination rect using the new get_rect
        dst_rect = self.get_rect(**{pivotPoint: (self.x, self.y)})
        if self.width == 0 or self.height == 0:
            return None
        #self.texture.color = self.color
        #self.texture.set_alpha(int(self.opacity))
        #renderer.target = self.texture
        #renderer.draw_color = (self.color[0], self.color[1], self.color[2], self.opacity)
        #renderer.clear()
        #renderer.target = None

        if destTexture is not None:
            renderer.target = destTexture.texture
            self.texture.draw(
                dstrect=dst_rect,
                angle=self.angle,
                flip_x=self.flipx,
                flip_y=self.flipy,
            )
            renderer.target = None
        else:
            self.texture.draw(
                dstrect=dst_rect,
                angle=self.angle,
                flip_x=self.flipx,
                flip_y=self.flipy,
            )


_texture_cache = {}
# -------- Image Loader with Caching -------- #
def loadTexture(name, path, x=0, y=0, scaleX=1.0, scaleY=1.0, angle=0, flipx=False, flipy=False, opacity=255, color=WHITE):
    """Loads a texture (cached), and returns an Img object."""
    global _texture_cache

    # Use absolute path for cache key to avoid duplicates
    if not isinstance(path, pygame.Surface):
        abs_path = os.path.abspath(path)
    else:
        abs_path = name
        if abs_path in _texture_cache:
            texture = _texture_cache[abs_path]
        else:
            # Upload texture to GPU
            if path.get_rect().width != 0 or path.get_rect().height != 0:
                #texture = Texture(renderer, p)
                texture = Texture.from_surface(renderer, path)
            else:
                texture = Texture.from_surface(renderer, pygame.Surface((1,1), pygame.SRCA))
                #pygame._sdl2.Texture.

                # Cache it
            _texture_cache[abs_path] = texture

        return Img(name, texture, x, y, scaleX, scaleY, angle, flipx, flipy)

    if abs_path in _texture_cache:
        texture = _texture_cache[abs_path]
    else:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        # Load surface and convert it with alpha
        surface = pygame.image.load(path).convert_alpha()

        # Upload texture to GPU
        texture = Texture.from_surface(renderer, surface)

        # Cache it
        _texture_cache[abs_path] = texture

    return Img(name, texture, x, y, scaleX, scaleY, angle, flipx, flipy)


scaledCache = {}
coloredCache = {}
rotatedCache = {}
def strong_tint(sprite, tint_color):
    sprite = sprite.convert_alpha()
    tinted = sprite.copy()

    # Normalize tint_color to RGBA (always 4 elements)
    if len(tint_color) == 3:
        tint_color = (*tint_color, 255)

    # Step 1: Multiply to shift toward tint color
    mult_overlay = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
    mult_overlay.fill(tint_color)
    tinted.blit(mult_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Step 2: Add a subtle glow for brightness (25% of tint color)
    glow_overlay = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
    glow_strength = tuple(min(int(c * 0.4), 255) for c in tint_color[:3]) + (0,)
    glow_overlay.fill(glow_strength)
    tinted.blit(glow_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    return tinted


if not useWeb:
    from PIL import Image

    def crop_surface(surface):
        # Convert Pygame surface to string data, then to PIL Image
        pil_img = Image.frombytes("RGBA", surface.get_size(), pygame.image.tostring(surface, "RGBA"))
        bbox = pil_img.getbbox()
        if not bbox:
            return surface  # No visible pixels, return original
        cropped_pil = pil_img.crop(bbox)
        cropped_surface = pygame.image.fromstring(cropped_pil.tobytes(), cropped_pil.size, "RGBA")
        return cropped_surface


def loadImg(image, flipX=False, angle=0, flipY=False, doCrop=False, blendMode='MULT', ignoreColor=(255, 255, 255, 255)):
    global images
    #images.clear()
    scaling = False
    scaleX = 1
    scaleY = 1
    coloring = WHITE
    color = False
    loadedImage = image
    if isinstance(image, tuple):
        trueImage = str(image[0])
        loadedImage = image[0]
        if len(image) > 1:
            scaling = True
            trueImage += str(image[1])
            if isinstance(image[1], tuple):
                scaleX = image[1][0]
                scaleY = image[1][1]
            else:
                scaleX = scaleY = image[1]
        if len(image) > 2:
            coloring = []
            for i in image[2]:
                coloring.append(int(i))
            if len(coloring) == 3:
                coloring.append(255)
            coloring = tuple(coloring)
            image = (image[0], image[1], coloring)
            color = True
            trueImage += str(image[2])
    else:
        trueImage = image

    if useTexture:
        return loadTexture(loadedImage, f'sprites/{loadedImage}', scaleX=scaleX, scaleY=scaleY, angle=angle, flipx=flipX, flipy=flipY)
    trueImage = str(trueImage + str(flipX) + str(angle%360)) + str(blendMode)
    if trueImage in images:
        pass
    else:
        if loadedImage not in baseImg:
            original_surface = scaleObj(pygame.image.load(f'sprites/{loadedImage}').convert_alpha(), scaleFactor)
            if not useWeb and doCrop:
                cropped_surface = crop_surface(original_surface)
                baseImg[loadedImage] = cropped_surface
            else:
                baseImg[loadedImage] = original_surface
        images[trueImage] = baseImg[loadedImage]
        if scaling or color:
            #images[trueImage] = pygame.transform.rotate(images[trueImage], angle%360)
            if scaling:
                if (image[0], image[1]) in scaledCache:
                    images[trueImage] = scaledCache[(image[0], image[1])]#scaleObj(images[trueImage], image[1]).convert_alpha()
                else:
                    images[trueImage] = scaleObj(images[trueImage], image[1]).convert_alpha()
                    scaledCache[(image[0], image[1])] = images[trueImage]
            if (image[0], angle, scaleX, scaleY) in rotatedCache:
                images[trueImage] = rotatedCache[(image[0], angle, scaleX, scaleY)]
            else:
                images[trueImage] = pygame.transform.rotate(images[trueImage], angle%360)
                rotatedCache[(image[0], angle, scaleX, scaleY)] = images[trueImage]
            if color:
                images[trueImage] = images[trueImage].copy()
                if blendMode == 'MULT':
                    images[trueImage].fill(image[2], special_flags=pygame.BLEND_RGBA_MULT)
                elif blendMode == 'ADD':
                    images[trueImage].fill( ( 255,255,255, 0 ), special_flags=pygame.BLEND_RGBA_SUB)
                    images[trueImage].fill( ( image[2][0],image[2][1],image[2][2], 0 ), special_flags=pygame.BLEND_RGBA_ADD)
                    if len(image[2]) == 4:
                        images[trueImage].set_alpha(image[2][3])
                    #images[trueImage] = strong_tint(images[trueImage], image[2])
            if flipX:
                images[trueImage] = pygame.transform.flip(images[trueImage], flipX, False)
        #images[trueImage] = scaleObj(images[trueImage], scaleFactor)
           #print(angle)


    return images[trueImage] # Returns the loaded image for later use

class DynamicMusicPlayer:
    def __init__(self, filepath, loop=True, initial_speed=1.0, bpm=175, steps_per_beat=4):
        self.server = Server(verbosity=0)
        #self.server.setProperty("logger", None)
        self.server.boot()
        self.server.start()

        # Restore the original stdout if needed
        sys.stdout = original_stdout

        self.loop = loop
        self.speed = initial_speed
        self.filepath = filepath
        self.playing = True

        # Time tracking
        self.start_time = time.time()
        self.pause_time = None
        self.elapsed_time_before_pause = 0.0

        # Music timing
        self.bpm = bpm
        self.steps_per_beat = steps_per_beat
        self.seconds_per_beat = 60.0 / bpm
        self.seconds_per_step = self.seconds_per_beat / steps_per_beat

        # Current rhythmic position
        self.cur_beat = 0
        self.cur_step = 0

        # Speed signal
        self.speed_sig = SigTo(value=self.speed, time=0.1)
        self.player = (SfPlayer(filepath, speed=self.speed_sig, loop=loop, mul=2)).out()

    def set_speed(self, speed):
        if self.playing:
            self._update_elapsed_time()
        self.speed = speed
        self.speed_sig.value = speed
        self.start_time = time.time()

    def fade_in(self, duration=2.0):
        self.fade = Fader(fadein=duration).play()
        self.player.mul = self.fade

    def fade_out(self, duration=2.0):
        self.fade = Fader(fadeout=duration).play()
        self.player.mul = self.fade

    def stop(self):
        self._update_elapsed_time()
        self.player.stop()
        self.server.stop()
        self.playing = False

    def pause(self):
        if self.playing:
            self._update_elapsed_time()
            self.player.stop()
            self.pause_time = time.time()
            self.playing = False

    def resume(self):
        if not self.playing:
            self.start_time = time.time()
            self.player = SfPlayer(self.filepath, speed=self.speed_sig, loop=self.loop, mul=0.6).out()
            self.player.out()
            self.playing = True

    def _update_elapsed_time(self):
        if self.start_time:
            elapsed = (time.time() - self.start_time) * self.speed
            self.elapsed_time_before_pause += elapsed

    def get_position(self, formatted=True):
        if self.playing:
            current_time = (time.time() - self.start_time) * self.speed
        else:
            current_time = 0
        pos = self.elapsed_time_before_pause + current_time
        if formatted:
            mins = int(pos // 60)
            secs = int(pos % 60)
            millis = int((pos * 1000) % 1000)
            return f"{mins:02}:{secs:02}.{millis:03}"
        return pos

    def restart(self):
        self.stop()
        self.server.start()
        self.start_time = time.time()
        self.elapsed_time_before_pause = 0.0
        self.player = SfPlayer(self.filepath, speed=self.speed_sig, loop=self.loop, mul=0.6).out()
        self.playing = True

    def update(self):
        """Update beat and step information based on current playback time and speed-adjusted BPM."""
        if self.playing:
            current_time = (time.time() - self.start_time) * self.speed
        else:
            current_time = 0

        pos = self.elapsed_time_before_pause + current_time

        # Recalculate timing based on adjusted tempo
        effective_bpm = self.bpm * self.speed
        seconds_per_beat = 60.0 / effective_bpm
        seconds_per_step = seconds_per_beat / self.steps_per_beat

        self.cur_beat = int(pos / seconds_per_beat)
        self.cur_step = int(pos / seconds_per_step)


class Sprite:
    def __init__(self, name, image, pos=(0, 0), baseScale=1, scale=1, flipX=False, angle=0, color=(255, 255, 255), opacity=255, mouseCollide=False,
                 pivotType="Center", layer=screen, doCrop=True):
        self.name = name
        self.image = image
        self.flipX = flipX
        self.mouseCollide = mouseCollide
        self.pivotType = pivotType
        self.layer = layer
        self.baseScale=baseScale
        self.doCrop = doCrop

        self.scaleX = 1
        self.scaleY = 1

        # Position tween variables
        pos = [pos[0], pos[1]]
        self.pos = pos
        self.oriPos = pos
        self.targetPos = pos
        self.tweenActivePos = False
        self.tweenPosType = 'linear'
        self.timePos = 0
        self.durationPos = 0
        self.throwParams = None  # Parameters for the throw motion

        # Scale tween variables
        self.scale = scale
        self.oriScale = scale
        self.targetScale = scale
        self.tweenActiveScale = False
        self.tweenScaleType = 'linear'
        self.timeScale = 0
        self.durationScale = 0

        self.angle = angle
        self.oriAngle = angle
        self.targetAngle = angle
        self.tweenActiveAngle = False
        self.tweenAngleType = 'linear'
        self.timeAngle = 0
        self.durationAngle = 0

        # Color tween variables
        self.color = color
        self.tintColor = WHITE
        self.oriColor = color
        self.targetColor = color
        self.tweenActiveColor = False
        self.tweenColorType = 'linear'
        self.timeColor = 0
        self.durationColor = 0


        # Opacity tween variables
        self.opacity = opacity
        self.oriOpacity = opacity
        self.targetOpacity = opacity
        self.tweenActiveOpacity = False
        self.tweenOpacityType = 'linear'
        self.timeOpacity = 0
        self.durationOpacity = 0

    def draw(self, x=0, y=0):
        image = loadImg((self.image, (self.baseScale * self.scale * self.scaleX, self.baseScale * self.scale * self.scaleY), self.color + (self.opacity,)), self.flipX, self.angle, doCrop=self.doCrop, blendMode='MULT')
        if useTexture:
            image.x = self.pos[0] + x
            image.y = self.pos[1] + y
            image.renderTexture(renderer, screen)
        else:
            imageRect = image.get_rect()
            setattr(imageRect, self.pivotType.lower(), ((self.pos[0] + x)*scaleFactor, (self.pos[1] + y)*scaleFactor))
            #imageRect = getattr(imageRect, i.pivotType.lower())
            self.layer.surface.blit(image, imageRect)

    def getRect(self, bool=False):
        if isinstance(self, AnimatedSprite):
        # Get the mask of the second sprite
            if bool:
                img = loadImg((self.getCurrentFrame(), (self.baseScale * self.scale * screenX, self.baseScale * self.scale * screenY), self.color), self.flipX, self.angle)
            else:
                img = loadImg((self.getCurrentFrame(), self.baseScale * self.scale, self.color), self.flipX, self.angle)
        else:
            if bool:
                img = loadImg((self.image, (self.baseScale * self.scale * screenX, self.baseScale * self.scale * screenY), self.color), self.flipX, self.angle, doCrop=True)
            else:
                img = loadImg((self.image, self.baseScale * self.scale, self.color), self.flipX, self.angle, doCrop=True)
        if bool:
            rect = img.get_rect(center=(scaleFactor * self.pos[0] * screenX, scaleFactor * self.pos[1] * screenY))
        else:
            rect = img.get_rect(center=(self.pos))
        #print(img.get_rect(center=self.pos))
        return rect

    def getSize(self, bool=False):
        if isinstance(self, AnimatedSprite):
        # Get the mask of the second sprite
            if bool:
                img = loadImg((self.getCurrentFrame(), (self.baseScale * self.scale * screenX, self.baseScale * self.scale * screenY), self.color), self.flipX, sprite.angle)
            else:
                img = loadImg((self.getCurrentFrame(), self.baseScale * self.scale, self.color), self.flipX, sprite.angle)
        else:
            # Get the mask of the second sprite
            if bool:
                img = loadImg((self.image, (self.baseScale * self.scale * screenX, self.baseScale * self.scale * screenY), self.color), self.flipX, self.angle)
            else:
                img = loadImg((self.image, self.baseScale * self.scale, self.color), self.flipX, self.angle)

        return img.get_size()

    def checkMouse(self, bool=False):
        rect = self.getRect(bool)
        mouse_pos = pygame.mouse.get_pos()
        if self.mouseCollide and rect.collidepoint(mouse_pos):
            return True
        else:
            return False


    def checkCollision(self, sprite):
        # Get the mask of the first sprite
        useTexture = True
        if useTexture:
            mask1 = self.getRect()
            mask2 = sprite.getRect()
            #pygame.draw.rect(screen.surface, WHITE, mask1)
            #pygame.draw.rect(screen.surface, BLACK, mask2)
            if mask1.colliderect(mask2):
                return True
            else:
                return False

        if isinstance(self, AnimatedSprite):
            mask1 = pygame.mask.from_surface(loadImg((self.getCurrentFrame(), self.scale, self.color), self.flipX, self.angle))
        else:
            mask1 = pygame.mask.from_surface(loadImg((self.image, self.scale, self.color), self.flipX, self.angle))

        if isinstance(sprite, AnimatedSprite):
        # Get the mask of the second sprite
            mask2 = pygame.mask.from_surface(loadImg((sprite.getCurrentFrame(), sprite.scale, sprite.color), sprite.flipX, sprite.angle))
        else:
            # Get the mask of the second sprite
            mask2 = pygame.mask.from_surface(loadImg((sprite.image, sprite.scale, sprite.color), sprite.flipX, sprite.angle))

        # Get the offset to account for the relative positions of the sprites
        offset = (int(sprite.pos[0] - self.pos[0]), int(sprite.pos[1] - self.pos[1]))
        #bound1 = mask1.get_bounding_rects()
        #bound2 = mask2.get_bounding_rects()
        #print(bound2)
        mask1_surface = mask1.to_surface(setcolor=WHITE, unsetcolor=(0, 0, 0, 0))
        #screen.blit(mask1_surface, mask1_surface.get_rect(center=self.pos))
        mask2_surface = mask2.to_surface(setcolor=WHITE, unsetcolor=(0, 0, 0, 0))
        #screen.blit(mask2_surface, mask2_surface.get_rect(center=sprite.pos))

        #drawRect(screen, RED, bound1)
        #drawRect(screen, RED, bound2)
        # Check if the masks overlap at the given offset
        if mask1.overlap(mask2, offset):
            return True  # Collision detected
        #if self.getRect().colliderect(sprite.getRect()):
            return True
        else:
            return False  # No collision


    def tweenClear(self, type):
        if type == 'all' or type == 'pos':
            pos = self.pos
            self.pos = pos
            self.oriPos = pos
            self.targetPos = pos
            self.tweenActivePos = False
            self.tweenPosType = 'linear'
            self.timePos = 0
            self.durationPos = 0
            self.throwParams = None

        if type == 'all' or type == 'scale':
            scale = self.scale
            self.scale = scale
            self.oriScale = scale
            self.targetScale = scale
            self.tweenActiveScale = False
            self.tweenScaleType = 'linear'
            self.timeScale = 0
            self.durationScale = 0

        if type == 'all' or type == 'angle':
            angle = self.angle
            self.angle = angle
            self.oriAngle = angle
            self.targetAngle = angle
            self.tweenActiveAngle = False
            self.tweenAngleType = 'linear'
            self.timeAngle = 0
            self.durationAngle = 0

        if type == 'all' or type == 'color':
            color = self.color
            # Color tween variables
            self.color = color
            self.oriColor = color
            self.targetColor = color
            self.tweenActiveColor = False
            self.tweenColorType = 'linear'
            self.timeColor = 0
            self.durationColor = 0

        if type == 'all' or type == 'opacity':
            opacity = self.opacity
            # Opacity tween variables
            self.opacity = opacity
            self.oriOpacity = opacity
            self.targetOpacity = opacity
            self.tweenActiveOpacity = False
            self.tweenOpacityType = 'linear'
            self.timeOpacity = 0
            self.durationOpacity = 0

    def tweenPos(self, newPos, tweenType='linear', duration=1, interrupt=False):
        if self.tweenActivePos == False or interrupt == True:
            if self.targetPos != list(newPos):
                self.timePos = 0
                self.targetPos = list(newPos)
                self.oriPos = self.pos
                self.tweenActivePos = True
                self.tweenPosType = tweenType
                self.durationPos = duration

    def tweenScale(self, newScale, tweenType='linear', duration=1, interrupt=False):
        if self.tweenActiveScale == False or interrupt == True:
            if self.targetScale != newScale:
                self.timeScale = 0
                self.targetScale = newScale
                self.oriScale = self.scale  # Assuming 'scale' is a variable that stores the current scale.
                self.tweenActiveScale = True
                self.tweenScaleType = tweenType
                self.durationScale = duration

    def tweenAngle(self, newAngle, tweenType='linear', duration=1, interrupt=False):
        if self.tweenActiveAngle == False or interrupt == True:
            if self.targetAngle != newAngle:
                self.timeAngle = 0
                self.targetAngle = newAngle
                self.oriAngle = self.angle  # Assuming 'angle' is a variable that stores the current angle.
                self.tweenActiveAngle = True
                self.tweenAngleType = tweenType
                self.durationAngle = duration

    def tweenColor(self, newColor, tweenType='linear', duration=1, interrupt=False):
        if self.tweenActiveColor == False or interrupt == True:
            if self.targetColor != newColor:
                self.timeColor = 0
                self.targetColor = newColor
                self.oriColor = self.color  # Assuming 'color' is a variable that stores the current color.
                self.tweenActiveColor = True
                self.tweenColorType = tweenType
                self.durationColor = duration

    def tweenOpacity(self, newOpacity, tweenType='linear', duration=1, interrupt=False):
        if self.tweenActiveOpacity == False or interrupt == True:
            if self.targetOpacity != newOpacity:
                self.timeOpacity = 0
                self.targetOpacity = newOpacity
                self.oriOpacity = self.opacity  # Assuming 'opacity' is a variable that stores the current opacity.
                self.tweenActiveOpacity = True
                self.tweenOpacityType = tweenType
                self.durationOpacity = duration


    def tweenThrow(self, targetPos, duration=1, peakHeight=100, interrupt=False):
        """
        Creates a throw-like tween where the sprite moves upwards and falls down to a target position.

        Parameters:
            targetPos (tuple): The final position (x, y) where the sprite will land.
            duration (float): The duration of the throw motion.
            peakHeight (float): The height the sprite will reach at the midpoint of the throw.
        """
        if interrupt or self.tweenActivePos == False:
            if self.targetPos != targetPos:
                #print(True, targetPos, self.pos)
                self.tweenActivePos = True
                self.timePos = 0
                self.targetPos = list(targetPos)
                self.durationPos = duration
                self.tweenPosType = 'custom'  # Use a custom tween type for throw motion
                # Precalculate parameters for the trajectory
                startX, startY = self.pos
                endX, endY = targetPos
                self.throwParams = {
                'startX': startX,
                'startY': startY,
                'endX': endX,
                'endY': endY,
                'peakHeight': peakHeight,
                'duration': duration
                }

    def tweenUpdate(self, deltaTime):
        # Update position with custom tween
        if self.timePos < self.durationPos:
            self.timePos += deltaTime
            t = min(self.timePos / self.durationPos, 1)
            if t == 1:
                self.tweenActivePos = False
                self.pos = self.targetPos

            if self.tweenPosType == 'custom':  # Throw motion
                self.pos = list(self.throwInterpolate(t, **self.throwParams))
            else:
                self.pos = [
                    int(self.interpolate(self.oriPos[0], self.targetPos[0], t, self.tweenPosType)),
                    int(self.interpolate(self.oriPos[1], self.targetPos[1], t, self.tweenPosType))
                ]

        # Update scale
        if self.timeScale < self.durationScale:
            self.timeScale += deltaTime
            t = min(self.timeScale / self.durationScale, 1)
            self.scale = self.interpolate(self.oriScale, self.targetScale, t, self.tweenScaleType)
            if t == 1 or useWeb:
                self.tweenActiveScale = False
                self.scale = self.targetScale

        # Update angle
        if self.timeAngle < self.durationAngle:
            self.timeAngle += deltaTime
            t = min(self.timeAngle / self.durationAngle, 1)
            self.angle = self.interpolate(self.oriAngle, self.targetAngle, t, self.tweenAngleType)
            if t == 1:
                self.tweenActiveAngle = False
                self.angle = self.targetAngle

        # Update color
        if self.timeColor < self.durationColor:
            self.timeColor += deltaTime
            t = min(self.timeColor / self.durationColor, 1)
            self.color = tuple(
                self.interpolate(self.oriColor[i], self.targetColor[i], t, self.tweenColorType)
                for i in range(3)
            )
            if t == 1:
                self.tweenActiveColor = False
                self.color = self.targetColor

        # Update opacity
        if self.timeOpacity < self.durationOpacity:
            self.timeOpacity += deltaTime
            t = min(self.timeOpacity / self.durationOpacity, 1)
            self.opacity = self.interpolate(self.oriOpacity, self.targetOpacity, t, self.tweenOpacityType)
            if t == 1:
                self.tweenActiveOpacity = False
                self.opacity = self.targetOpacity

    def throwInterpolate(self, t, startX, startY, endX, endY, peakHeight, duration):
        """
        Calculates the throw motion based on the current time fraction `t`.

        Parameters:
            t (float): A value between 0 and 1 indicating progress through the tween.
            startX, startY: The starting position of the sprite.
            endX, endY: The final position of the sprite.
            peakHeight: The height of the trajectory's peak above the straight line.
            duration: Total duration of the motion.

        Returns:
            (float, float): The interpolated position (x, y).
        """
        # Horizontal interpolation (linear)
        x = self.linear(startX, endX, t)

        # Parabolic vertical interpolation
        # The arch's apex occurs at t = 0.5
        peakY = min(startY, endY) - peakHeight  # Calculate the peak's Y position
        #parabola = 4 * (t - 0.5) ** 2  # Creates a parabola that reaches its minimum at t = 0.5
        y = endY - (peakHeight * 4)*(-(t**2) + t)

        return x, y


    def interpolate(self, start, end, t, tweenType):
        if tweenType == 'linear':
            return self.linear(start, end, t)
        elif tweenType == 'easeIn':
            return self.easeIn(start, end, t)
        elif tweenType == 'easeOut':
            return self.easeOut(start, end, t)
        elif tweenType == 'easeInOut':
            return self.easeInOut(start, end, t)
        elif tweenType == 'quadIn':
            return self.quadIn(start, end, t)
        elif tweenType == 'quadOut':
            return self.quadOut(start, end, t)
        elif tweenType == 'quadInOut':
            return self.quadInOut(start, end, t)
        elif tweenType == 'circIn':
            return self.circIn(start, end, t)
        elif tweenType == 'circOut':
            return self.circOut(start, end, t)
        elif tweenType == 'circInOut':
            return self.circInOut(start, end, t)
        elif tweenType == 'sineIn':
            return self.sineIn(start, end, t)
        elif tweenType == 'sineOut':
            return self.sineOut(start, end, t)
        elif tweenType == 'sineInOut':
            return self.sineInOut(start, end, t)
        elif tweenType == 'logIn':
            return self.logIn(start, end, t)
        elif tweenType == 'logOut':
            return self.logOut(start, end, t)
        elif tweenType == 'logInOut':
            return self.logInOut(start, end, t)
        else:
            raise ValueError(f"Unknown tween type: {tweenType}")

    # Easing functions
    def linear(self, start, end, t):
        return start + (end - start) * t

    def easeIn(self, start, end, t):
        return start + (end - start) * (t ** 2)

    def easeOut(self, start, end, t):
        return start + (end - start) * (1 - (1 - t) ** 2)

    def easeInOut(self, start, end, t):
        if t < 0.5:
            return start + (end - start) * (2 * t ** 2)
        else:
            return start + (end - start) * (1 - 2 * (1 - t) ** 2)

    def quadIn(self, start, end, t):
        return start + (end - start) * (t ** 2)

    def quadOut(self, start, end, t):
        return start + (end - start) * (t * (2 - t))

    def quadInOut(self, start, end, t):
        if t < 0.5:
            return start + (end - start) * (2 * t ** 2)
        else:
            return start + (end - start) * (-1 + (4 - 2 * t) * t)

    def circIn(self, start, end, t):
        return start + (end - start) * (1 - math.sqrt(1 - t ** 2))

    def circOut(self, start, end, t):
        return start + (end - start) * (math.sqrt(1 - (t - 1) ** 2))

    def circInOut(self, start, end, t):
        if t < 0.5:
            return start + (end - start) * (0.5 * (1 - math.sqrt(1 - (2 * t) ** 2)))
        else:
            return start + (end - start) * (0.5 * (math.sqrt(1 - (2 * (1 - t)) ** 2) + 1))

    def sineIn(self, start, end, t):
        return start + (end - start) * (1 - math.cos((t * math.pi) / 2))

    def sineOut(self, start, end, t):
        return start + (end - start) * math.sin((t * math.pi) / 2)

    def sineInOut(self, start, end, t):
        return start + (end - start) * (0.5 * (1 - math.cos(math.pi * t)))

    def logIn(self, start, end, t):
        if t == 0:
            return start
        return start + (end - start) * math.log1p(t * (math.e - 1))

    def logOut(self, start, end, t):
        if t == 1:
            return end
        return start + (end - start) * (1 - math.log1p((1 - t) * (math.e - 1)))

    def logInOut(self, start, end, t):
        if t < 0.5:
            return self.logIn(start, (start + end) / 2, 2 * t)
        else:
            return self.logOut((start + end) / 2, end, 2 * t - 1)

class AnimatedSprite(Sprite):
    def __init__(self, name, character, animName, skin='Default', baseScale=1, scale=1, flipX=False, angle=0, color=(255, 255, 255), opacity=255, pos=(0, 0),
                 mouseCollide=False, pivotType="Center", xmlUsed=False, layer=screen):
        # Call the parent Sprite class constructor to initialize basic sprite attributes
        super().__init__(name=name, image=None, pos=pos, baseScale=baseScale, scale=scale, flipX=flipX, angle=angle, color=color, opacity=opacity, mouseCollide=mouseCollide, pivotType=pivotType, layer=layer)

        # Animation parameters
        self.character = character  # Character folder name
        self.skin = skin  # Skin of the character
        self.xmlUsed = xmlUsed
        self.xmlImage = {}
        self.oriXml = {}
        if self.xmlUsed:
        # Load texture atlas
            self.loadTextureAtlas()  # Load the textures from the sprite sheet
        self.animData = self.loadAnimationData()  # Load animation data from JSON
        self.timerAnim = None
        self.setAnimation(animName)  # Set initial animation state
        self.currentFrameIndex = 0  # Current frame index
        self.timeSinceLastFrame = 0  # Timer to control frame rate
        self.currentAnim = 'idle'
        #print(self.timerAnim)
        #self.box =
        #self.xmlImage = {}
        #print(self.currentAnim)

    def loadTextureAtlas(self):
        """Load the sprite sheet and parse the XML file to extract the sub-textures."""
        xmlPath = f'sprites/players/{self.character}/{self.skin}/' + f'{self.character}.xml'
        try:
            tree = ET.parse(xmlPath)
            root = tree.getroot()
            image_path = f'players\\{self.character}\\{self.skin}\\' + f'{self.character}.png'#os.path.join('xml', f'{self.character}.png')#root.get('imagePath')  # Path to the sprite sheet image

            self.sheet = loadImg(image_path)  # Load the sprite sheet image

            backPos = (0, 0)
            firstImg = True
            offsetX = offsetY = 0
            # Parse the subtextures and store them in a dictionary
            for sub_texture in root.findall('SubTexture'):
                name = sub_texture.get('name')
                x = int(sub_texture.get('x'))
                y = int(sub_texture.get('y'))
                width = int(sub_texture.get('width'))
                height = int(sub_texture.get('height'))
                frameX = int(sub_texture.get('frameX'))
                frameY = int(sub_texture.get('frameY'))
                frameWidth = int(sub_texture.get('frameWidth'))
                frameHeight = int(sub_texture.get('frameHeight'))
                a = self.angle
                # Crop the sub-image from the sprite sheet and store in dictionary
                centerX, centerY = self.pos[0] + self.scale*(-frameX + width/2), self.pos[1] + self.scale*(-frameY + height/2), #-frameX + width/2, -frameY + height/2
                xSide, ySide = (centerX - backPos[0]), (centerY - backPos[1])
                hypothenuse = math.sqrt((xSide)**2 + (ySide)**2)
                sub_image = self.sheet.subsurface(pygame.Rect(x, y, width, height))
                adjuster = math.atan2(ySide, xSide)
                self.xmlImage[name] = {
                    'image': rotateObj(scaleObj(sub_image, self.scale), -a),
                    'frame': pygame.Rect(frameX, frameY, frameWidth, frameHeight),
                    'info': [self.pos, self.scale, self.angle, self.color, self.opacity],
                    'oriPos': (x, y),
                    'pos': self.pos if firstImg else ( self.pos[0] + hypothenuse*math.cos(a*math.pi/180 + adjuster),
                                                        self.pos[1] + hypothenuse*math.sin(a*math.pi/180 + adjuster))
                }
                self.oriXml[name] = {
                    'image': sub_image,
                    'frame': pygame.Rect(frameX, frameY, frameWidth, frameHeight),
                    'dimension': pygame.Rect(x, y, width, height),
                    'pos': self.pos if firstImg else ( self.pos[0] + hypothenuse*math.cos(a*math.pi/180 + adjuster),
                                                        self.pos[1] + hypothenuse*math.sin(a*math.pi/180 + adjuster))
                }
                backPos = (centerX, centerY) if firstImg == True else backPos
                if firstImg:
                    offsetX = self.scale*(-frameX + width/2)
                    offsetY = self.scale*(-frameY + height/2)
                firstImg = False
            #self.oriXml = copy.copy(self.xmlImage)
        except FileNotFoundError:
            raise Exception(f"Texture atlas XML not found at '{xmlPath}'.")

    def updateXml(self):
        backPos = (0,0)
        firstImg = True
        for name in self.oriXml:
            xmlInfo = self.oriXml[name]
            if self.xmlImage[name]['info'] == [self.pos, self.scale, self.angle, self.color, self.opacity]:
                continue
            sub_image = xmlInfo['image']
            frameX = xmlInfo['frame'].x
            frameY = xmlInfo['frame'].y
            frameWidth = xmlInfo['frame'].width
            frameHeight = xmlInfo['frame'].height
            x = xmlInfo['dimension'].x
            y = xmlInfo['dimension'].y
            width = xmlInfo['dimension'].width
            height = xmlInfo['dimension'].height
            a = self.angle
            # Crop the sub-image from the sprite sheet and store in dictionary
            centerX, centerY = self.pos[0] + self.scale*(-frameX + width/2), self.pos[1] + self.scale*(-frameY + height/2), #-frameX + width/2, -frameY + height/2
            xSide, ySide = (centerX - backPos[0]), (centerY - backPos[1])
            hypothenuse = math.sqrt((xSide)**2 + (ySide)**2)
            adjuster = math.atan2(ySide, xSide)
            self.xmlImage[name] = {
                'image': rotateObj(scaleObj(sub_image, self.scale), -a),
                'frame': pygame.Rect(frameX, frameY, frameWidth, frameHeight),
                'info': [self.pos, self.scale, self.angle, self.color, self.opacity],
                'oriPos': (x, y),
                'pos': self.pos if firstImg else ( self.pos[0] + hypothenuse*math.cos(a*math.pi/180 + adjuster),
                                                    self.pos[1] + hypothenuse*math.sin(a*math.pi/180 + adjuster))
            }
            backPos = (centerX, centerY) if firstImg == True else backPos
            firstImg = False

    def loadAnimationData(self):
        """Load the animation data from the JSON file."""
        jsonPath = os.path.join('data', 'animation', f'{self.character}.json')
        try:
            with open(jsonPath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Animation data for '{self.character}' not found at '{jsonPath}'.")

    def setAnimation(self, animName):
        """Switch to a different animation state."""
        #print(animName, self.timerAnim, 1)
        if self.name in timer and self.timerAnim != None:
            #print(self.timerAnim, animName)
            animName = self.timerAnim
            #return False
        if animName in self.animData:
            anim = self.animData[animName]
            doesNotExist = False
            try:
                self.currentAnim
            except:
                doesNotExist = True
            else:
                if self.currentAnim != animName:
                    doesNotExist = True

            if doesNotExist:
                self.currentAnim = animName
                self.loop = anim['useLoop']
                self.frameRate = anim['frameRate']
                if not self.xmlUsed:
                    self.frames = anim['anim']
                else:
                    self.frames = []
                    for i in self.xmlImage:
                        if animName in i:
                            self.frames.append(i)
                self.loopThrough = anim.get('loopThrough', [])
                self.currentFrameIndex = 0
                self.timeSinceLastFrame = 0
        else:
            raise Exception(f"Animation '{animName}' not found in animation data.")

    def changeAngle(self, angle):
        self.angle += angle
        self.xmlImage = {}
        if self.xmlUsed:
        # Load texture atlas
            self.loadTextureAtlas()  # Load the textures from the sprite sheet

    def animate(self, deltaTime):
        """Update the animation state based on elapsed time."""
        self.timeSinceLastFrame += deltaTime * 1000

        # Advance frame if enough time has passed
        if self.timeSinceLastFrame >= 1000 / self.frameRate:
            self.timeSinceLastFrame = 0
            self.currentFrameIndex += 1

            if self.loop:
                # Loop within the specified range if defined
                if self.loopThrough != []:
                    start, end = self.loopThrough[0], self.loopThrough[1]
                    if self.currentFrameIndex > end:
                        self.currentFrameIndex = start
                else:
                    # Loop through the full range
                    if self.currentFrameIndex >= len(self.frames):
                        self.currentFrameIndex = 0
            else:
                # Stop at the last frame if not looping
                if self.currentFrameIndex >= len(self.frames):
                    self.currentFrameIndex = len(self.frames) - 1


    def getCurrentFrame(self):
        """Get the current frame image path."""
        if not self.xmlUsed:
            return f'players/{self.character}/{self.skin}/{self.frames[self.currentFrameIndex]}'
            self.image = loadImg(self.getCurrentFrame(), self.scale, self.color)
        else:
            """Get the current frame image."""
            #return self.xmlImage
            frame_name = self.frames[self.currentFrameIndex]
            frame_data = self.xmlImage.get(frame_name)

            if frame_data:
                return frame_data['image'], frame_data['pos'], frame_data['frame']
            else:
                return None

    def setPosition(self, pos):
        """Set the position of the sprite."""
        self.pos = pos

    def draw(self, x=0, y=0):
        #print(self.name, self.pos)
        image = loadImg((self.getCurrentFrame(), (self.baseScale * self.scale * self.scaleX, self.baseScale * self.scale * self.scaleY), self.color + (self.opacity,)), self.flipX, self.angle, blendMode='MULT')
        doColorTint = False
        if self.tweenActiveColor:
            doColorTint = True
            tintOpacity = 255*(1 - (self.timeColor/self.durationColor))
            tintColor = loadImg((self.getCurrentFrame(), (self.baseScale * self.scale * self.scaleX, self.baseScale * self.scale * self.scaleY), self.tintColor + (tintOpacity,)), self.flipX, self.angle, blendMode='ADD')
            tintColor.set_alpha(tintColor.get_alpha()*self.opacity/255)

        if useTexture:
            image.x = self.pos[0] + x
            image.y = self.pos[1] + y
            image.renderTexture(renderer, screen)
        else:
            imageRect = image.get_rect()
            setattr(imageRect, self.pivotType.lower(), ((self.pos[0] + x)*scaleFactor, (self.pos[1] + y)*scaleFactor))
            #imageRect = getattr(imageRect, i.pivotType.lower())
            self.layer.surface.blit(image, imageRect)
            if doColorTint:
                #print(True)
                imageRect = tintColor.get_rect()
                setattr(imageRect, self.pivotType.lower(), ((self.pos[0] + x)*scaleFactor, (self.pos[1] + y)*scaleFactor))
                #imageRect = getattr(imageRect, i.pivotType.lower())
                self.layer.surface.blit(tintColor, imageRect)



class Trigger:
    def __init__(self, name='', boolean=False, color=WHITE, x=0, y=0, size=50):
        self.name = name
        self.boolean = boolean
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        trigger[self.name] = self

    def getRect(self):
        realX = (self.x - self.size/2) * screenX
        realY = (self.y - self.size/2) * screenY
        return pygame.Rect(realX * scaleFactor, realY * scaleFactor, self.size * screenX * scaleFactor, self.size * screenY * scaleFactor)


    def checkMouse(self):
        rect = self.getRect()
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            return True
        else:
            return False


    def draw(self, boolOne=False, boolTwo=False):
        #global mouseDown, mouseHold
        #mouseDown, mouseHold = boolOne, boolTwo
        thickness = 5
        realX = self.x - self.size/2
        realY = self.y - self.size/2
        if self.checkMouse():
            drawRect(hud, YELLOW, (realX - 5, realY - 5, self.size + 2*thickness, self.size + 2*thickness))
            if mouseDown:
                self.boolean = not self.boolean

        drawRect(hud, BLACK , (realX, realY, self.size, self.size))
        drawRect(hud, WHITE , (realX + thickness, realY + thickness, self.size - 2*thickness, self.size - 2*thickness))
        if self.boolean:
            drawCircle(hud.surface, YELLOW, (self.x, self.y) , (self.size/2)-2*thickness)#, 3*self.size)

        text = render_text(self.name, self.color, self.size, True, BLACK, 3)
        textRect = text.get_rect(topright=(realX - 20, realY))
        blitObj(hud.surface, text, realX, realY-30, pivot_type='center')
        #drawRect(hud, PURPLE, self.getRect())


    def update(self):
        self.draw()


def playAnimation(animatedSprite, animationName, forceLoopBool=True, duration=0, resetDuration=False):
    """
    Function to play a specific animation on an AnimatedSprite object.

    :param animatedSprite: The instance of the AnimatedSprite class to modify.
    :param animationName: The name of the animation to play (e.g., 'idle', 'attack').
    :param forceLoopBool: Boolean to control whether the animation should loop or stop at the last frame.
    """
    # Ensure the specified animation exists in the animation data
    if animationName not in animatedSprite.animData:
        #raise ValueError(f"Animation '{animationName}' not found for character '{animatedSprite.character}'")
        #print(True, animationName)
        return False

    if duration != 0:
        runTimer(animatedSprite.name, duration, resetDuration)
        animatedSprite.timerAnim = animationName
        #print(True)
    # Update the animation properties for the AnimatedSprite instance
    animatedSprite.setAnimation(animationName)  # Set the new animation using the built-in method
    return True
    #animatedSprite.loop = forceLoopBool  # Override the loop behavior if specified



def loadSprite(spriteName, image='meter.png', pos=(0,0), baseScale=1, scale=1, flipX=False, angle=0, color=(255, 255, 255), opacity=255, replace=False,
               mouseCollide=False, pivotType='center', layer=screen, doCrop=True):
    if spriteName not in sprites.keys() or replace:
        sprites[spriteName] = Sprite(spriteName, image, pos, baseScale, scale, flipX, angle, color, opacity, mouseCollide=mouseCollide, pivotType=pivotType, layer=layer, doCrop=doCrop)
    return sprites[spriteName]

# Assuming `sprites` is a dictionary where we store all instances of AnimatedSprite
animatedSprites = {}

def loadAnimatedSprite(spriteName, character, pos=(0, 0), baseScale=1, scale=1, flipX=False, angle=0, animationName='idle', color=(255, 255, 255), opacity=255,
                       replace=False, mouseCollide=False, pivotType='Center', xmlUsed=False, layer=screen):
    """
    Load or retrieve an AnimatedSprite object, creating a new one if not cached or if replace is True.

    :param spriteName: Unique name to identify the sprite in the cache.
    :param character: Name of the character to load.
    :param pos: Position tuple (x, y) of the sprite.
    :param scale: Scale factor of the sprite.
    :param flipX: Boolean indicating if the sprite should be flipped horizontally.
    :param angle: Rotation angle of the sprite in degrees.
    :param animationName: Initial animation to set (default is 'idle').
    :param color: Color tint to apply to the sprite (default is white).
    :param opacity: Opacity level of the sprite (0-255, default is fully opaque).
    :param replace: Boolean to force recreation of the sprite, even if it is cached.
    :param mouseCollide: Boolean indicating if the sprite should be clickable.
    :return: The AnimatedSprite instance.
    """
    global animatedSprites  # Ensure we are modifying the global sprite cache

    # Initialize the sprite cache if it doesn't exist
    if 'animatedSprites' not in globals():
        animatedSprites = {}

    # Check if the sprite is already cached and whether to replace it
    if spriteName not in animatedSprites or replace:
        # Create a new AnimatedSprite and add it to the cache
        animatedSprites[spriteName] = AnimatedSprite(
            name=spriteName,
            character=character,
            animName=animationName,
            pos=pos,
            baseScale=baseScale,
            scale=scale,
            flipX=flipX,
            angle=angle,
            color=color,
            opacity=opacity,
            mouseCollide=mouseCollide,
            pivotType=pivotType,
            xmlUsed = xmlUsed
        )

    return animatedSprites[spriteName]



# Updated function to handle both Sprite and AnimatedSprite objects
def updateTween():
    for i in sprites.values():
        i.tweenUpdate(deltaTime)  # Updates the tweening for all sprites (both regular and animated)

    for i in animatedSprites.values():
        i.tweenUpdate(deltaTime)  # Updates the tweening for animated sprites
        if i.xmlUsed:
        # Load texture atlas
            i.updateXml()  # Load the textures from the sprite sheet


# Updated function to handle both Sprite and AnimatedSprite objects
def draw(layer=screen):
    gameRect = screen.get_rect()
    for i in animatedSprites.values():
        if not i.xmlUsed:
            if i.opacity == 0 or i.layer != layer:
                continue
            # Draw AnimatedSprite objects
            # Ensure we load the current frame of the animation using the animation state
            image = loadImg((i.getCurrentFrame(), i.baseScale * i.scale, i.color + (i.opacity,)), i.flipX, i.angle, blendMode='MULT')
            if useTexture:
                image.x = i.pos[0]
                image.y = i.pos[1]
                image.renderTexture(renderer, screen)
            else:
                imageRect = image.get_rect()
                setattr(imageRect, i.pivotType.lower(), (i.pos[0]*scaleFactor, i.pos[1]*scaleFactor))
                #imageRect = getattr(imageRect, i.pivotType.lower())
                i.layer.surface.blit(image, imageRect)

        if i.xmlUsed:
            # Get the current frame image for the sprite
            current_frame = i.getCurrentFrame()

            #for frame_name in xmlImage:
                #frame_data = xmlImage.get(frame_name)
                #current_frame = frame_data['image'], frame_data['pos']
            # Draw the current frame at the sprite's position
            #if current_frame:
                # Assuming you have a screen surface (or use the appropriate surface object)
            imageRect = current_frame[0].get_rect()
            setattr(imageRect, 'center', current_frame[1])
            i.layer.blit(current_frame[0], imageRect)  # Drawing the sprite at its position
                #screen.blit(current_frame[0], current_frame[1])
            #for frame_name in xmlImage:
                #currentPos = xmlImage.get(frame_name)['pos']
            pygame.draw.circle(screen.surface, RED, current_frame[1], 9)

    for i in sprites.values():
        if i.opacity == 0 or i.layer != layer:
            continue
        # Draw regular Sprite objects
        image = loadImg((i.image, i.baseScale * i.scale, i.color + (i.opacity,)), i.flipX, i.angle, doCrop=True, blendMode='MULT')
        if useTexture:
            image.x = i.pos[0]
            image.y = i.pos[1]
            image.renderTexture(renderer, screen)
        else:
            imageRect = image.get_rect()
            setattr(imageRect, i.pivotType.lower(), (i.pos[0]*scaleFactor, i.pos[1]*scaleFactor))
            #imageRect = getattr(imageRect, i.pivotType.lower())
            i.layer.surface.blit(image, imageRect)

def mouseHover():
    for i in sprites.values():
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
            drawRect(i.layer.surface, YELLOW, (rect.x - thickness, rect.y - thickness, size[0] + 2*thickness, size[1] + 2*thickness))

mouseDown = False
mouseTimer = 0
mouseHold = False

def mouseTouch(sprite, useClick=True, useHold=False, timeTaken=15, delay=5):
    global mouseTimer
    if sprite.checkMouse(True):
        if useClick:
            if mouseDown:
                if sprite.targetScale != 0.9:
                    sprite.tweenScale(0.9, 'circOut', 0.03, True)
                    playSound('Confirm_sfx.ogg')

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
timer = {}
def runTimer(name, time, overwrite=False):
    if name not in timer or overwrite:
        timer[name] = {"Duration": time, "Elapsed": 0}

def updateTimer():
    for stuff in timer:
        timer[stuff]["Elapsed"] += 1/30
        #print(stuff, timer[stuff])
    timerCopy = timer.copy()
    for stuff in timerCopy:
        if timerCopy[stuff]["Duration"] <= timerCopy[stuff]["Elapsed"]:
            del timer[stuff]

def updateAnimation():
    """Updates all animated sprites' animations."""
    updateTimer()
    for sprite in animatedSprites.values():
        if sprite.name in timer and sprite.timerAnim != None:
            sprite.setAnimation(sprite.timerAnim)

        # Call the animate method on each AnimatedSprite to update the current frame
        sprite.animate(deltaTime)  # This will handle the animation frame progression

def addTuple(tupleType, num):
    finalTuple = []
    for i in tupleType:
        finalTuple.append(max(i+num, 0))
    return tuple(finalTuple)

soundCache = {}

# Function to play sound
def playSound(name):
    if name not in soundCache:
        soundCache[name] = pygame.mixer.Sound(f'sounds/{name}') # Loads in the sound from the sounds folder
    sound = soundCache[name]
    sound.set_volume(soundVolume) # Sets the sound volume based off user current sound volume
    sound.play() # Plays the sound


buttonList = {}
class Button(Sprite):
    def __init__(self, name, x, y, width=250, height=50, thickness=10, mainColor=(70, 160, 200), hoverColor=(70, 200, 200), clickColor=(200, 200, 200), textSize=45, textColor=WHITE, destSurface=hud.surface):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = thickness
        self.mainColor = mainColor
        self.hoverColor = hoverColor
        self.clickColor = clickColor
        self.textSize = textSize
        self.textColor = textColor
        self.destSurface = destSurface
        self.clicked = False
        self.hold = False
        self.selected = False
        buttonList[self.name] = self

    def draw(self):
        buttonWidth = self.width
        buttonHeight = self.height

        x = self.x
        y = self.y
        thickness = self.thickness

        buttonRect = pygame.Rect(x-buttonWidth/2-thickness/2, y-buttonHeight/2-thickness/2, buttonWidth+thickness, buttonHeight+thickness)
        hitBox = pygame.Rect(
            (x-buttonWidth/2-thickness/2)*scaleFactor,
            (y-buttonHeight/2-thickness/2)*scaleFactor,
            (buttonWidth+thickness)*scaleFactor,
            (buttonHeight+thickness)*scaleFactor
            )
        mouse_pos = pygame.mouse.get_pos()
        if hitBox.collidepoint(mouse_pos):
            if mouseHold:
                drawRect(self.destSurface, addTuple(self.clickColor, -30), buttonRect)
                drawRect(self.destSurface, self.clickColor, (x-buttonWidth/2, y-buttonHeight/2, buttonWidth, buttonHeight))
                self.hold = True
                if mouseDown:
                    self.clicked = True
                    playSound('Confirm_sfx.ogg')
                else:
                    self.clicked = False
            else:
                self.hold = self.clicked = False
                drawRect(self.destSurface, addTuple(self.hoverColor, -30), buttonRect)
                drawRect(self.destSurface, self.hoverColor, (x-buttonWidth/2, y-buttonHeight/2, buttonWidth, buttonHeight))

        else:
            self.hold = self.clicked = False
            drawRect(self.destSurface, addTuple(self.mainColor, -30), buttonRect)
            drawRect(self.destSurface, self.mainColor, (x-buttonWidth/2, y-buttonHeight/2, buttonWidth, buttonHeight))

        theName = self.name
        if self.name == 'v':
            buttonText = render_text('^', self.textColor, self.textSize, True, BLACK, 3, angle=180)
            y -= 5
        else:
            buttonText = render_text(theName, self.textColor, self.textSize, True, BLACK, 3)
        #if self.name == 'v':
            #buttonText = rotateObj(buttonText, 180)
        blitObj(self.destSurface, buttonText, x, y)

class keyButton(Button):
    def __init__(self, name, x, y, width=250, height=50, thickness=10, mainColor=(70, 160, 200), hoverColor=(70, 200, 200), clickColor=(200, 200, 200), textSize=45, textColor=WHITE, destSurface=hud.surface, key=pygame.K_RETURN):
         super().__init__(name, x, y, width, height, thickness, mainColor, hoverColor, clickColor, textSize, textColor, destSurface)
         self.key = key
         self.selected = False

achievementObj = {}
class Achievement:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.triggered = False
        self.frame = 0
        self.x = width/2
        self.y = 0
        achievementObj[name] = self

    def trigger(self):
        if self.triggered == False:
            self.triggered = True
            #print(True)
            playSound('Achievement_sfx.ogg')

    def update(self):
        if self.triggered and self.frame/25 <= math.pi:
            self.frame += 1
            achievementImg = loadImg((f'achievement/{self.name}.png', 1.5))
            blitObj(hud, achievementImg, width/2, -80+160*math.sin(self.frame/25))
            text = render_text(self.name, WHITE, 55, True, BLACK, 3)
            blitObj(hud, text, width/2, -5+160*math.sin(self.frame/25))


Achievement("First Comer!", "Open the game for the first time!")
Achievement("Thin Win!", "Win a solo game playing as Thin!")
Achievement("Tutorial Complete!", "Finish the Tutorial!")
Achievement("Victorious!", "Win in a 5v5!")
Achievement("The Creator", "Type a code in the main menu.")
Achievement("The Programmer", "Enter the code in the main menu.")

class Slider:
    def __init__(self, name, x, y, width, height, min_val, max_val, initial_val, color=CYAN, var='musicVolume'):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.grabbed = False
        self.color = CYAN
        self.var = var

    def draw(self, screen):
        globals()[self.var] = self.value
        text = render_text(self.name + ': ' + str(round(self.value*100)) + '%', WHITE, 55, True, BLACK, 2)
        blitObj(screen, text, self.x, self.y-self.height/2-30)
        drawRect(screen, BLACK, (self.x-self.width/2, self.y-self.height/2, self.width, self.height))
        slider_pos = (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        drawRect(screen, self.color, (self.x-self.width/2, self.y-self.height/2, slider_pos, self.height))
        handle_rect = pygame.Rect(self.x + slider_pos - 10 -self.width/2, self.y - 5-self.height/2, 20, self.height + 10)
        drawRect(screen, WHITE, handle_rect)


    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                hitBoxRect = pygame.Rect(scaleFactor*(self.x-self.width/2), scaleFactor*(self.y-self.height/2), scaleFactor*self.width, scaleFactor*self.height)
                if hitBoxRect.collidepoint(event.pos):
                    self.grabbed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.grabbed = False
            elif event.type == pygame.MOUSEMOTION:
                if self.grabbed:
                    self.value = ((event.pos[0] - (self.x-self.width/2)*scaleFactor)) / (self.width * scaleFactor) * (self.max_val - self.min_val) + self.min_val
                    self.value = max(self.min_val, min(self.max_val, self.value))

keyBind = {'Confirm':pygame.K_RETURN, 'Cancel':pygame.K_BACKSPACE, 'Special':pygame.K_RCTRL}

botPlay = Trigger('Botplay', x=500, y=350)
enemyAutoAttack = Trigger('RNG Attacks', boolean=True)
easyMode = Trigger('Easy Mode')
hardMode = Trigger('Hard Mode')
quickLoad = Trigger('Fast Fight Load', boolean=True)
extraDialogue = Trigger('Extra Dialogue', boolean=True)
multiplayer = Trigger('Multiplayer', boolean=False)
usemobile = Trigger('Use Mobile', boolean=True)
useAnim = Trigger('Use Animation', boolean=False)

musicSlider = Slider('Music Volume', 500, 350, 250, 30, 0, 1, 1)
soundSlider = Slider('Sound Volume', 500, 450, 250, 30, 0, 1, 1, color=GREEN, var='soundVolume')

Button('Play', width/2, height/2)
Button('Info', width/2, height/2)
Button('Setting', width/2, height/2)
Button('Achievement', width/2, height/2)
Button('Quit', width/2, height/2)
Button('Back', width/2, height/2)
Button('Battle', width/2, height/2)
Button('Tutorial', width/2, height/2)
Button('Confirm', width/2, height/2)
Button('Stats', width/2, height/2)
Button('Attacks', width/2, height/2)
Button('Abilities', width/2, height/2)
Button('Skins', width/2, height/2)
Button('<', width/2, height/2)
Button('>', width/2, height/2)
Button('^', width/2, height/2)
Button('v', width/2, height/2)
Button('Class', width/2, height/2)
Button(f'confirm', 250, 200, width=300)
Button(f'cancel', 750, 200, width=300)
Button('O', width/2, height/2)












