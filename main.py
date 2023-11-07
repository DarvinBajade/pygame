import pygame
import spritesheet

# Bajade, Darvin Kobe M.
# BSCS 3-1

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MIDTERMS')

background_image = pygame.image.load('background.png').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

sprite_sheet_image = pygame.image.load('Gunner_Black_Idle.png').convert_alpha()
sprite_sheet_image_run = pygame.image.load('Gunner_Black_Run.png').convert_alpha()
bullet_sprite_image = pygame.image.load('Fire_bullet.png').convert_alpha()

sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
sprite_sheet_run = spritesheet.SpriteSheet(sprite_sheet_image_run)
bullet_sprite_sheet = spritesheet.SpriteSheet(bullet_sprite_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

frames_idle = [
    sprite_sheet.get_image(0, 48, 48, 3, BLACK),
    sprite_sheet.get_image(1, 48, 48, 3, BLACK),
    sprite_sheet.get_image(2, 48, 48, 3, BLACK),
    sprite_sheet.get_image(3, 48, 48, 3, BLACK),
    sprite_sheet.get_image(4, 48, 48, 3, BLACK),
]

frames_run = [
    sprite_sheet_run.get_image(0, 48, 48, 3, BLACK),
    sprite_sheet_run.get_image(1, 48, 48, 3, BLACK),
    sprite_sheet_run.get_image(2, 48, 48, 3, BLACK),
    sprite_sheet_run.get_image(3, 48, 48, 3, BLACK),
    sprite_sheet_run.get_image(4, 48, 48, 3, BLACK),
    sprite_sheet_run.get_image(5, 48, 48, 3, BLACK)
]

bullet_frames = [
    bullet_sprite_sheet.get_image(16, 16, 16, 3, BLACK),
    bullet_sprite_sheet.get_image(17, 16, 16, 3, BLACK),
    bullet_sprite_sheet.get_image(18, 16, 16, 3, BLACK),
    bullet_sprite_sheet.get_image(19, 16, 16, 3, BLACK),
]

projectile_image = pygame.Surface((20, 5))
projectile_image.fill((255, 255, 0))

projectiles = []

clock = pygame.time.Clock()

run = True

frame_index = 0
frame_timer = 0
is_idle = True

x = SCREEN_WIDTH // 2
y = SCREEN_HEIGHT - 144
velocity = 5  # Change the velocity for smooth diagonal movement

is_w_pressed = False
is_a_pressed = False
is_s_pressed = False
is_d_pressed = False

shot_interval = 30
current_shot_delay = 0

font = pygame.font.Font(None, 36)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    screen.blit(background_image, (0, 0))

    is_w_pressed = keys[pygame.K_w]
    is_a_pressed = keys[pygame.K_a]
    is_s_pressed = keys[pygame.K_s]
    is_d_pressed = keys[pygame.K_d]

    if is_w_pressed or is_a_pressed or is_s_pressed or is_d_pressed:
        is_idle = False
        frame_timer += 1
        if frame_timer >= 10:
            frame_index = (frame_index + 1) % len(frames_run)
            frame_timer = 0
        if is_w_pressed:
            y -= velocity
        if is_s_pressed:
            y += velocity
        if is_a_pressed:
            x -= velocity
        if is_d_pressed:
            x += velocity
        screen.blit(frames_run[frame_index], (max(0, min(x, SCREEN_WIDTH - 12)), max(0, min(y, SCREEN_HEIGHT - 12))))
    else:
        is_idle = True
        frame_index = 0
        frame_timer += 0.5
        if frame_timer >= 10:
            frame_index = (frame_index + 1) % len(frames_idle)
            frame_timer = 0
        screen.blit(frames_idle[frame_index], (max(0, min(x, SCREEN_WIDTH - 12)), max(0, min(y, SCREEN_HEIGHT - 12))))

    y = max(126, min(y, 381))
    x = max(0, min(x, 855))

    if keys[pygame.K_SPACE] and current_shot_delay <= 0:
        projectile_x = x + 100
        projectile_y = y + 44
        projectiles.append([projectile_x, projectile_y, 0])
        current_shot_delay = shot_interval

    if current_shot_delay > 0:
        current_shot_delay -= 1

    new_projectiles = []
    for projectile in projectiles:
        projectile[0] += 10  # Change the projectile speed
        if projectile[0] < SCREEN_WIDTH:
            frame_index = (projectile[2] + 1) % len(bullet_frames)
            screen.blit(bullet_frames[frame_index], (projectile[0], projectile[1]))
            new_projectiles.append([projectile[0], projectile[1], frame_index])
    projectiles = new_projectiles

    pygame.display.update()

    clock.tick(60)

pygame.quit()