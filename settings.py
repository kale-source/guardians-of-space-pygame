import pygame
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações centralizadas do jogo:
    - Dimensões, FPS e título da janela.
    - Parâmetros de gameplay (velocidades, delays, limites).
    - Configuração de cores, fontes e upgrade.
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )
    
    # Aplicação
    APP_NAME: str = Field(default="Guardians Of Space", description="Nome do jogo")
    APP_VERSION: str = Field(default="1.0.0", description="Versão do jogo")
    
    # Tela
    WIDTH: int = Field(default=800, description="Largura da janela")
    HEIGHT: int = Field(default=600, description="Altura da janela")
    FPS: int = Field(default=60, description="Frames por segundo")
    TITLE: str = Field(default="Guardians Of Space", description="Título da janela")
    
    # Cores
    BLACK: tuple = Field(default=(0, 0, 0), description="Cor preta")
    WHITE: tuple = Field(default=(255, 255, 255), description="Cor branca")
    RED: tuple = Field(default=(255, 0, 0), description="Cor vermelha")
    
    # Estrelas
    NUM_STARS: int = Field(default=100, description="Número de estrelas")
    STAR_BRIGHTNESS_MIN: int = Field(default=100, description="Brilho mínimo das estrelas")
    STAR_BRIGHTNESS_MAX: int = Field(default=255, description="Brilho máximo das estrelas")
    STAR_BLINK_SPEED: int = Field(default=2, description="Velocidade de piscar das estrelas")
    STAR_SPEED_MIN: float = Field(default=2.0, description="Velocidade mínima das estrelas")
    STAR_SPEED_MAX: float = Field(default=7.0, description="Velocidade máxima das estrelas")
    
    # Player
    PLAYER_SPEED: int = Field(default=6, description="Velocidade do jogador")
    PLAYER_WIDTH: int = Field(default=40, description="Largura do jogador")
    PLAYER_HEIGHT: int = Field(default=20, description="Altura do jogador")
    
    @property
    def PLAYER_START_X(self):
        """"Posição inicial X do jogador, centralizada horizontalmente."""
        return self.WIDTH // 2
    
    @property
    def PLAYER_START_Y(self):
        """"Posição inicial Y do jogador, posicionada na parte inferior da tela."""
        return int(self.HEIGHT * 0.95)
    
    # Meteoros
    METEOR_RADIUS_MIN: int = Field(default=10, description="Raio mínimo dos meteoros")
    METEOR_RADIUS_MAX: int = Field(default=30, description="Raio máximo dos meteoros")
    METEOR_SPEED_MIN: float = Field(default=0.5, description="Velocidade mínima dos meteoros")
    METEOR_SPEED_MAX: float = Field(default=0.5, description="Velocidade máxima dos meteoros")
    METEOR_SPEED_SCALE: float = Field(default=0.5, description="Escala de velocidade dos meteoros")
    METEOR_SPAWN_DELAY: int = Field(default=120, description="Atraso para spawn dos meteoros")
    METEOR_SPAWN_DELAY_MIN: int = Field(default=15, description="Atraso mínimo para spawn dos meteoros")
    METEOR_SPAWN_DELAY_SCALE: int = Field(default=5, description="Escala de atraso para spawn dos meteoros")
    METEOR_COLORS: tuple = Field(
        default=(
            (139, 69, 19),
            (210, 105, 30),
            (222, 184, 135),
            (244, 164, 96),
        ),
        description="Cores dos meteoros",
    )
    
    # Bala
    BULLET_SPEED: int = Field(default=12, description="Velocidade da bala")
    BULLET_BASE_WIDTH: int = Field(default=4, description="Largura base da bala")
    BULLET_BASE_HEIGHT: int = Field(default=10, description="Altura base da bala")
    BULLET_COLOR: tuple = Field(default=(0, 200, 255), description="Cor da bala")
    BULLET_CHARGED_COLOR: tuple = Field(default=(255, 160, 0), description="Cor da bala carregada")
    BULLET_COOLDOWN: int = Field(default=15, description="Tempo de recarga da bala")
    BULLET_CHARGE_MAX_FRAMES: int = Field(default=90, description="Número máximo de frames para carregar a bala")
    BULLET_MAX_SIZE_MULT: float = Field(default=4.0, description="Multiplicador máximo do tamanho da bala")
    BULLET_MAX_DAMAGE: int = Field(default=2, description="Dano máximo da bala")

    # Upgrades
    LEVEL_UP_INTERVAL: int = Field(default=20, description="Intervalo para subir de nível")
    MAX_ESCAPED_METEORS: int = Field(default=10, description="Número máximo de meteoros que podem escapar")
    UPGRADE_EVERY_N_KILLS: int = Field(default=15, description="Subir de nível a cada N inimigos eliminados")
    UPGRADE_SPEED_BONUS: int = Field(default=1, description="Bônus de velocidade ao subir de nível")
    UPGRADE_DAMAGE_BONUS: int = Field(default=1, description="Bônus de dano ao subir de nível")
    UPGRADE_COOLDOWN_BONUS: int = Field(default=1, description="Bônus de recarga ao subir de nível")

    # Fontes
    FONT_MAIN: object = Field(
        default_factory=lambda: pygame.font.SysFont("arial black", 60),
        description="Fonte principal para títulos",
    )
    FONT_DETAILS: object = Field(
        default_factory=lambda: pygame.font.SysFont("arial", 20),
        description="Fonte para detalhes",
    )

    FONT_SUBTITLE: object = Field(
        default_factory=lambda: pygame.font.SysFont("arial black", 40),
        description="Fonte para subtítulos",
    )

pygame.font.init()
settings = Settings()
