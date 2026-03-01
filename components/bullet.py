import pygame
from core.entity import Entity
from settings import (
    BULLET_SPEED,
    BULLET_BASE_WIDTH, BULLET_BASE_HEIGHT,
    BULLET_COLOR, BULLET_CHARGED_COLOR,
    BULLET_MAX_SIZE_MULT, BULLET_MAX_DAMAGE,
    HEIGHT,
)


class Bullet(Entity):
    """
    Projétil disparado pelo player.

    Recebe um charge_ratio (0.0 a 1.0) que escala:
        - Tamanho visual (width e height)
        - Dano causado ao meteoro (1 a BULLET_MAX_DAMAGE)
        - Cor: ciano (normal) → laranja (totalmente carregada)

    Comportamento:
        charge_ratio = 0.0  → bala mínima, 1 de dano
        charge_ratio = 1.0  → bala máxima, BULLET_MAX_DAMAGE de dano
    """

    def __init__(self, x: float, y: float, charge_ratio: float = 0.0, damage_bonus: int = 0) -> None:
        self.charge_ratio = max(0.0, min(1.0, charge_ratio))
        self.damage       = max(1, round(1 + (BULLET_MAX_DAMAGE - 1) * self.charge_ratio) + damage_bonus)

        # Tamanho escala com a carga
        mult   = 1.0 + (BULLET_MAX_SIZE_MULT - 1.0) * self.charge_ratio
        width  = max(1, int(BULLET_BASE_WIDTH  * mult))
        height = max(1, int(BULLET_BASE_HEIGHT * mult))

        # Centraliza a bala no X de origem
        centered_x = x - width // 2

        super().__init__(centered_x, y - height, width, height)
        self.speed = BULLET_SPEED

    # ── Entity interface ──────────────────────────────────────────────────────

    def _build_image(self) -> None:
        color = self._lerp_color(BULLET_COLOR, BULLET_CHARGED_COLOR, self.charge_ratio)
        pygame.draw.rect(
            self.image,
            color,
            (0, 0, self.width, self.height),
            border_radius=min(self.width, self.height) // 2,
        )

    def update(self, *args, **kwargs) -> None:
        self.pos_y -= self.speed
        self._sync_rect()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def is_off_screen(self) -> bool:
        return self.pos_y + self.height < 0

    @staticmethod
    def _lerp_color(
        c1: tuple[int, int, int],
        c2: tuple[int, int, int],
        t: float,
    ) -> tuple[int, int, int]:
        """Interpola linearmente entre duas cores pelo fator t (0.0–1.0)."""
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )