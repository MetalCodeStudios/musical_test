import pygame
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

# -- CONFIG --
SPRITE_PATH = "sprites/players/Rekety/Default/idle_0.png"  # Must support alpha
GLOW_COLOR = (255, 255, 255)  # Teal-ish glow
GLOW_RADIUS = 10            # How far the glow spreads

# -- INIT PYGAME --
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Proper Sprite Outline Glow")
clock = pygame.time.Clock()

# -- LOAD SPRITE --
sprite = pygame.image.load(SPRITE_PATH).convert_alpha()
sprite.fill((255, 255, 255, 125), special_flags=pygame.BLEND_RGBA_SUB)
sprite_size = sprite.get_size()


def create_glow(sprite_surf, glow_color=(0, 255, 0), glow_radius=10, glow_strength=5, alpha_boost=6.0):
    """
    Create a glow effect around a Pygame surface's alpha mask.

    Parameters:
        sprite_surf (pygame.Surface): The original sprite (must have alpha).
        glow_color (tuple): RGB color of the glow.
        glow_radius (int): How far the glow spreads (blur radius).
        glow_strength (int): How many times the glow is composited (layer stacking).
        alpha_boost (float): Brightness multiplier on the glow's alpha (e.g. 1.0 = normal, 2.0 = brighter glow).

    Returns:
        pygame.Surface: A new surface with the glow applied around the sprite.
    """

    # Convert Pygame surface to PIL image
    raw_str = pygame.image.tostring(sprite_surf, "RGBA", False)
    pil_image = Image.frombytes("RGBA", sprite_surf.get_size(), raw_str)

    # Extract alpha channel as a glow mask
    alpha = pil_image.split()[3]

    # Blur the alpha to create a soft glow shape
    glow_mask = alpha.filter(ImageFilter.GaussianBlur(glow_radius))

    # Optional: amplify the brightness of the glow mask
    if alpha_boost != 1.0:
        enhancer = ImageEnhance.Brightness(glow_mask)
        glow_mask = enhancer.enhance(alpha_boost)

    # Create a solid glow image using the glow mask and glow color
    glow_image = Image.new("RGBA", pil_image.size, glow_color + (0,))
    glow_image.putalpha(glow_mask)

    # Create a larger surface to allow room for the glow
    final_size = (
        pil_image.width + glow_radius * 2,
        pil_image.height + glow_radius * 2
    )
    result = Image.new("RGBA", final_size, (0, 0, 0, 0))

    # Paste the glow multiple times to increase brightness
    for _ in range(glow_strength):
        result.paste(glow_image, (glow_radius, glow_radius), glow_image)

    # Paste the original sprite on top of the glow
    result.paste(pil_image, (glow_radius, glow_radius), pil_image)

    # Convert back to a Pygame surface
    return pygame.image.fromstring(result.tobytes(), result.size, "RGBA").convert_alpha()

# Create glowing sprite
glow_sprite = create_glow(sprite, glow_color=GLOW_COLOR, glow_radius=50)
glow_sprite = pygame.transform.smoothscale(glow_sprite, (400, 400))

# -- SPRITE POS --
x, y = 100, 100
vx, vy = 2.5, 2

# -- MAIN LOOP --
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move sprite
    x += 0#vx
    y += 0#vy

    if x <= 0 or x + sprite.get_width() >= WIDTH:
        vx *= -1
    if y <= 0 or y + sprite.get_height() >= HEIGHT:
        vy *= -1

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw glow and sprite
    screen.blit(glow_sprite, (x - GLOW_RADIUS, y - GLOW_RADIUS))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
