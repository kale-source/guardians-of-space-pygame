import pygame
from typing import Tuple
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Configuration uses pydantic_settings to provide type validation,
    environment variable loading, and .env file support.
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )
    
    # ── Aplicação ─────────────────────────────────────────────────────────────
    APP_NAME: str = Field(default="Guardians Of Space", description="Application title")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    
    # ── Tela ───────────────────────────────────────────────────────────────────
    WIDTH: int = Field(default=800, env="WIDTH", description="Screen width in pixels")
    HEIGHT: int = Field(default=600, env="HEIGHT", description="Screen height in pixels")
    FPS: int = Field(default=60, description="Frames per second")
    TITLE: str = Field(default="Guardians Of Space", description="Window title")
    
    # ── Cores ──────────────────────────────────────────────────────────────────
    BLACK: Tuple[int, int, int] = Field(default=(0, 0, 0), description="Black color RGB")
    WHITE: Tuple[int, int, int] = Field(default=(255, 255, 255), description="White color RGB")
    RED: Tuple[int, int, int] = Field(default=(255, 0, 0), description="Red color RGB")
    
    # ── Estrelas ───────────────────────────────────────────────────────────────
    NUM_STARS: int = Field(default=100, description="Number of stars in background")
    STAR_BRIGHTNESS_MIN: int = Field(default=100, description="Minimum star brightness")
    STAR_BRIGHTNESS_MAX: int = Field(default=255, description="Maximum star brightness")
    STAR_BLINK_SPEED: int = Field(default=2, description="Star blink animation speed")
    STAR_SPEED_MIN: float = Field(default=2.0, description="Slow stars (appear distant)")
    STAR_SPEED_MAX: float = Field(default=7.0, description="Fast stars (appear close)")
    
    # ── Player ─────────────────────────────────────────────────────────────────
    PLAYER_SPEED: int = Field(default=6, description="Player movement speed")
    PLAYER_WIDTH: int = Field(default=40, description="Player sprite width")
    PLAYER_HEIGHT: int = Field(default=20, description="Player sprite height")
    
    @property
    def PLAYER_START_X(self) -> int:
        """Player starting X position (centered)"""
        return self.WIDTH // 2
    
    @property
    def PLAYER_START_Y(self) -> int:
        """Player starting Y position (95% of screen height)"""
        return int(self.HEIGHT * 0.95)
    
    # ── Meteoros ───────────────────────────────────────────────────────────────
    METEOR_RADIUS_MIN: int = Field(default=10, description="Minimum meteor radius")
    METEOR_RADIUS_MAX: int = Field(default=30, description="Maximum meteor radius")
    METEOR_SPEED_MIN: float = Field(default=0.5, description="Minimum meteor speed")
    METEOR_SPEED_MAX: float = Field(default=0.5, description="Maximum meteor speed")
    METEOR_SPEED_SCALE: float = Field(default=0.5, description="Speed increment per level")
    METEOR_SPAWN_DELAY: int = Field(default=120, description="Base spawn delay in frames (level 1)")
    METEOR_SPAWN_DELAY_MIN: int = Field(default=15, description="Minimum spawn delay (avoid impossibility)")
    METEOR_SPAWN_DELAY_SCALE: int = Field(default=5, description="Frames reduced per level")
    METEOR_COLORS: Tuple[Tuple[int, int, int], ...] = Field(
        default=(
            (139, 69, 19),
            (210, 105, 30),
            (222, 184, 135),
            (244, 164, 96),
        ),
        description="Meteor color palette (RGB tuples)"
    )
    
    # ── Bala ───────────────────────────────────────────────────────────────────
    BULLET_SPEED: int = Field(default=12, description="Bullet movement speed")
    BULLET_BASE_WIDTH: int = Field(default=4, description="Base bullet width")
    BULLET_BASE_HEIGHT: int = Field(default=10, description="Base bullet height")
    BULLET_COLOR: Tuple[int, int, int] = Field(default=(0, 200, 255), description="Regular bullet color (cyan)")
    BULLET_CHARGED_COLOR: Tuple[int, int, int] = Field(default=(255, 160, 0), description="Charged bullet color (orange)")
    BULLET_COOLDOWN: int = Field(default=15, description="Cooldown frames after shooting")
    BULLET_CHARGE_MAX_FRAMES: int = Field(default=90, description="Frames for max charge (1.5s at 60fps)")
    BULLET_MAX_SIZE_MULT: float = Field(default=4.0, description="Maximum size multiplier when charged")
    BULLET_MAX_DAMAGE: int = Field(default=2, description="Maximum damage for fully charged bullet")
    
    # ── Upgrades ───────────────────────────────────────────────────────────────
    LEVEL_UP_INTERVAL: int = Field(default=20, description="Seconds to level up")
    MAX_ESCAPED_METEORS: int = Field(default=10, description="Meteors allowed to escape before game over")
    UPGRADE_EVERY_N_KILLS: int = Field(default=20, description="Kills to trigger upgrade menu")
    UPGRADE_SPEED_BONUS: int = Field(default=1, description="Speed bonus per upgrade")
    UPGRADE_DAMAGE_BONUS: int = Field(default=1, description="Maximum damage bonus per upgrade")
    
    # ── Fontes ─────────────────────────────────────────────────────────────────
    FONT_MAIN: any = Field(
        default_factory=lambda: pygame.font.SysFont("arial", 40),
        description="Main title font (40px)"
    )
    FONT_SUB: any = Field(
        default_factory=lambda: pygame.font.SysFont("arial", 25),
        description="Subtitle font (25px)"
    )
    FONT_DETAILS: any = Field(
        default_factory=lambda: pygame.font.SysFont("arial", 15),
        description="Details/HUD font (15px)"
    )

# ── Inicialização ──────────────────────────────────────────────────────────────
pygame.font.init()

# Instância global de configurações
settings = Settings()
