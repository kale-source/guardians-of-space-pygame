import pygame
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do jogo"""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )
    
    # Aplicação
    APP_NAME: str = Field(default="Guardians Of Space")
    APP_VERSION: str = Field(default="1.0.0")
    
    # Tela
    WIDTH: int = Field(default=800)
    HEIGHT: int = Field(default=600)
    FPS: int = Field(default=60)
    TITLE: str = Field(default="Guardians Of Space")
    
    # Cores
    BLACK: tuple = Field(default=(0, 0, 0))
    WHITE: tuple = Field(default=(255, 255, 255))
    RED: tuple = Field(default=(255, 0, 0))
    
    # Estrelas
    NUM_STARS: int = Field(default=100)
    STAR_BRIGHTNESS_MIN: int = Field(default=100)
    STAR_BRIGHTNESS_MAX: int = Field(default=255)
    STAR_BLINK_SPEED: int = Field(default=2)
    STAR_SPEED_MIN: float = Field(default=2.0)
    STAR_SPEED_MAX: float = Field(default=7.0)
    
    # Player
    PLAYER_SPEED: int = Field(default=6)
    PLAYER_WIDTH: int = Field(default=40)
    PLAYER_HEIGHT: int = Field(default=20)
    
    @property
    def PLAYER_START_X(self):
        return self.WIDTH // 2
    
    @property
    def PLAYER_START_Y(self):
        return int(self.HEIGHT * 0.95)
    
    # Meteoros
    METEOR_RADIUS_MIN: int = Field(default=10)
    METEOR_RADIUS_MAX: int = Field(default=30)
    METEOR_SPEED_MIN: float = Field(default=0.5)
    METEOR_SPEED_MAX: float = Field(default=0.5)
    METEOR_SPEED_SCALE: float = Field(default=0.5)
    METEOR_SPAWN_DELAY: int = Field(default=120)
    METEOR_SPAWN_DELAY_MIN: int = Field(default=15)
    METEOR_SPAWN_DELAY_SCALE: int = Field(default=5)
    METEOR_COLORS: tuple = Field(
        default=(
            (139, 69, 19),
            (210, 105, 30),
            (222, 184, 135),
            (244, 164, 96),
        )
    )
    
    # Bala
    BULLET_SPEED: int = Field(default=12)
    BULLET_BASE_WIDTH: int = Field(default=4)
    BULLET_BASE_HEIGHT: int = Field(default=10)
    BULLET_COLOR: tuple = Field(default=(0, 200, 255))
    BULLET_CHARGED_COLOR: tuple = Field(default=(255, 160, 0))
    BULLET_COOLDOWN: int = Field(default=15)
    BULLET_CHARGE_MAX_FRAMES: int = Field(default=90)
    BULLET_MAX_SIZE_MULT: float = Field(default=4.0)
    BULLET_MAX_DAMAGE: int = Field(default=2)
    
    # Upgrades
    LEVEL_UP_INTERVAL: int = Field(default=20)
    MAX_ESCAPED_METEORS: int = Field(default=10)
    UPGRADE_EVERY_N_KILLS: int = Field(default=15)
    UPGRADE_SPEED_BONUS: int = Field(default=1)
    UPGRADE_DAMAGE_BONUS: int = Field(default=1)
    UPGRADE_COOLDOWN_BONUS: int = Field(default=1)
    
    # Fontes
    FONT_MAIN: object = Field(
        default_factory=lambda: pygame.font.SysFont("arial black", 60),
    )
    FONT_DETAILS: object = Field(
        default_factory=lambda: pygame.font.SysFont("arial", 20),
    )

    FONT_SUBTITLE: object = Field(
        default_factory=lambda: pygame.font.SysFont("arial black", 40)
    )

pygame.font.init()
settings = Settings()
