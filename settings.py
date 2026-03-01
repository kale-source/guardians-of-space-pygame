import os
import pygame
from dotenv import load_dotenv

load_dotenv()

# ── Tela ──────────────────────────────────────────────────────────────────────
WIDTH  = int(os.getenv("WIDTH",  800))
HEIGHT = int(os.getenv("HEIGHT", 600))
FPS    = 60
TITLE  = "Guardians Of Space"

# ── Cores ─────────────────────────────────────────────────────────────────────
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255, 0,   0)

# ── Estrelas ──────────────────────────────────────────────────────────────────
NUM_STARS            = 100
STAR_BRIGHTNESS_MIN  = 100
STAR_BRIGHTNESS_MAX  = 255
STAR_BLINK_SPEED     = 2
STAR_SPEED_MIN       = 2.0   # estrelas lentas → parecem distantes
STAR_SPEED_MAX       = 7.0   # estrelas rápidas → parecem próximas

# ── Player ────────────────────────────────────────────────────────────────────
PLAYER_SPEED  = 6
PLAYER_WIDTH  = 40
PLAYER_HEIGHT = 20
PLAYER_START_X = WIDTH  // 2
PLAYER_START_Y = int(HEIGHT * 0.95)

# ── Meteoros ──────────────────────────────────────────────────────────────────
METEOR_RADIUS_MIN    = 10
METEOR_RADIUS_MAX    = 30
METEOR_SPEED_MIN     = 0.5
METEOR_SPEED_MAX     = 0.5
METEOR_SPEED_SCALE   = 0.5   # acréscimo por level
METEOR_SPAWN_DELAY        = 120    # frames base entre spawns (level 1)
METEOR_SPAWN_DELAY_MIN    = 15    # limite mínimo para não ficar impossível
METEOR_SPAWN_DELAY_SCALE  = 5     # frames reduzidos por level
METEOR_COLORS        = (
    (139, 69,  19),
    (210, 105, 30),
    (222, 184, 135),
    (244, 164, 96),
)

# ── Bala ─────────────────────────────────────────────────────────────────────
BULLET_SPEED             = 12
BULLET_BASE_WIDTH        = 4
BULLET_BASE_HEIGHT       = 10
BULLET_COLOR             = (0, 200, 255)     # ciano
BULLET_CHARGED_COLOR     = (255, 160, 0)     # laranja para bala carregada
BULLET_COOLDOWN          = 15                # frames de cooldown após disparar

BULLET_CHARGE_MAX_FRAMES = 90                # frames para carga máxima (1.5s a 60fps)
BULLET_MAX_SIZE_MULT     = 4.0               # multiplicador máximo de tamanho
BULLET_MAX_DAMAGE        = 2      

# ── Upgrades ──────────────────────────────────────────────────────────────────
LEVEL_UP_INTERVAL     = 20   # segundos para subir de level
MAX_ESCAPED_METEORS   = 10   # meteoros que podem escapar antes do game over  
UPGRADE_EVERY_N_KILLS  = 5    # destruições para abrir o menu de upgrade
UPGRADE_SPEED_BONUS    = 1     # bônus de velocidade por upgrade
UPGRADE_DAMAGE_BONUS   = 1     # bônus de dano máximo por upgrade         # dano máximo da bala totalmente carregada

# ── Progressão ────────────────────────────────────────────────────────────────
LEVEL_UP_INTERVAL     = 20   # segundos para subir de level
MAX_ESCAPED_METEORS   = 10   # meteoros que podem escapar antes do game over

# ── Fontes ────────────────────────────────────────────────────────────────────
pygame.font.init()
FONT_MAIN    = pygame.font.SysFont("arial", 40)
FONT_SUB     = pygame.font.SysFont("arial", 25)
FONT_DETAILS = pygame.font.SysFont("arial", 15)