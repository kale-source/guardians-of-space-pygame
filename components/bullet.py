import pygame
from core.entity import Entity
from settings import settings


class Bullet(Entity):
    """
    Projétil com carga e dano variável:
    - Tamanho e cor escalam com nível de carga.
    - Dano varia de 1 até BULLET_MAX_DAMAGE baseado na carga.
    - Move para cima em velocidade constante.
    """

    def __init__(self, x, y, charge_ratio=0.0, damage_bonus=0):
        self.charge_ratio = max(0.0, min(1.0, charge_ratio))
        self.damage = max(1, round(1 + (settings.BULLET_MAX_DAMAGE - 1) * self.charge_ratio) + damage_bonus)

        # Tamanho escala com a carga
        mult = 1.0 + (settings.BULLET_MAX_SIZE_MULT - 1.0) * self.charge_ratio
        width = max(1, int(settings.BULLET_BASE_WIDTH * mult))
        height = max(1, int(settings.BULLET_BASE_HEIGHT * mult))

        centered_x = x - width // 2
        super().__init__(centered_x, y - height, width, height)
        self.speed = settings.BULLET_SPEED

    def _build_image(self):
        """
        Desenha a bala com cor baseado na carga:
        - Cor interpola de azul até laranja conforme carga aumenta.
        """
        color = self._lerp_color(settings.BULLET_COLOR, settings.BULLET_CHARGED_COLOR, self.charge_ratio)
        pygame.draw.rect(
            self.image,
            color,
            (0, 0, self.width, self.height),
            border_radius=min(self.width, self.height) // 2,
        )

    def update(self):
        """
        Atualiza posição da bala:
        - Move para cima em velocidade constante.
        """
        self.pos_y -= self.speed
        self._sync_rect()

    def is_off_screen(self):
        """
        Verifica se a bala saiu da tela:
        - Retorna true se a bala passou do topo da tela.
        """
        return self.pos_y + self.height < 0

    @staticmethod
    def _lerp_color(c1, c2, t):
        """
        Interpola linearmente entre duas cores:
        - t varia de 0 a 1 para blendagem suave.
        """
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )