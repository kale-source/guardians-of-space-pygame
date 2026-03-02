import pygame
import random
from core.entity import Entity
from settings import settings


class Meteor(Entity):
    """
    Meteoro que cai do topo da tela.

    HP:
        Começa com (1 + level) pontos de vida. Cada acerto de bala chama
        hit(), que decrementa o HP e atualiza a cor para dar feedback visual.
        Ao chegar em 0, o sprite é removido com kill().

    Feedback de dano:
        A cor do meteoro clareia progressivamente conforme perde HP,
        indicando ao jogador que o alvo está sendo destruído.
    """

    def __init__(self, level: int):
        self.radius = random.randint(settings.METEOR_RADIUS_MIN, settings.METEOR_RADIUS_MAX)
        self.max_hp = 1 + level
        self.hp = self.max_hp
        self._base_color = random.choice(settings.METEOR_COLORS)
        size = self.radius * 2

        x = random.randint(self.radius, settings.WIDTH - self.radius) - self.radius
        y = -size

        # entities/meteor.py
        self.speed = random.uniform(settings.METEOR_SPEED_MIN, settings.METEOR_SPEED_MAX) + level * settings.METEOR_SPEED_SCALE
        super().__init__(x, y, size, size)
        self.mask = pygame.mask.from_surface(self.image)

    # ── Entity interface ──────────────────────────────────────────────────────

    def _build_image(self):
        self.image.fill((0, 0, 0, 0))   # limpa para o redraw de dano funcionar
        pygame.draw.circle(
            self.image,
            self._current_color(),
            (self.radius, self.radius),
            self.radius,
        )

    def update(self, *args, **kwargs):
        self.pos_y += self.speed
        self._sync_rect()

    # ── API pública ───────────────────────────────────────────────────────────

    def hit(self, damage: int = 1):
        """
        Recebe um acerto de bala.
        Decrementa HP pelo dano recebido, atualiza visual e destrói se HP <= 0.
        """
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
        else:
            self._build_image()                         # redesenha com nova cor
            self.mask = pygame.mask.from_surface(self.image)   # atualiza máscara

    def is_off_screen(self) -> bool:
        return self.pos_y - self.radius > settings.HEIGHT

    # ── Helpers visuais ───────────────────────────────────────────────────────

    def _current_color(self) -> tuple[int, int, int]:
        """
        Interpola a cor base em direção ao branco conforme o HP diminui.
        HP cheio → cor original | HP quase zero → quase branco.
        """
        ratio    = self.hp / self.max_hp          # 1.0 = cheio, ~0.0 = crítico
        r, g, b  = self._base_color
        r = int(r + (255 - r) * (1 - ratio))
        g = int(g + (255 - g) * (1 - ratio))
        b = int(b + (255 - b) * (1 - ratio))
        return (r, g, b)