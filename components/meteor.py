import pygame
import random
from core.entity import Entity
from settings import settings


class Meteor(Entity):
    """
    Meteoro que cai com HP e muda de cor quando acertado:
    - Tamanho varia aleatoriamente.
    - HP aumenta com o level do jogo.
    - Cor branca conforme recebe dano.
    - Remove-se da tela quando escapa pela base.
    """

    def __init__(self, level):
        self.radius = random.randint(settings.METEOR_RADIUS_MIN, settings.METEOR_RADIUS_MAX)
        self.max_hp = 1 + level
        self.hp = self.max_hp
        self._base_color = random.choice(settings.METEOR_COLORS)
        size = self.radius * 2

        x = random.randint(self.radius, settings.WIDTH - self.radius) - self.radius
        y = -size

        self.speed = random.uniform(settings.METEOR_SPEED_MIN, settings.METEOR_SPEED_MAX) + level * settings.METEOR_SPEED_SCALE
        super().__init__(x, y, size, size)
        self.mask = pygame.mask.from_surface(self.image)

    def _build_image(self):
        """
        Desenha o meteoro como um círculo:
        - Cor varia conforme o nível de HP.
        """
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(
            self.image,
            self._current_color(),
            (self.radius, self.radius),
            self.radius,
        )

    def update(self):
        """
        Atualiza posição do meteoro:
        - Move para baixo com velocidade baseada no level.
        """
        self.pos_y += self.speed
        self._sync_rect()

    def hit(self, damage=1):
        """
        Aplica dano ao meteoro:
        - Reduz HP baseado no dano recebido.
        - Atualiza cor visual do meteoro.
        - Remove meteoro do jogo se HP <= 0.
        """
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
        else:
            self._build_image()
            self.mask = pygame.mask.from_surface(self.image)

    def is_off_screen(self):
        """
        Verifica se o meteoro saiu da tela pela base.
        """
        return self.pos_y - self.radius > settings.HEIGHT

    def _current_color(self):
        """
        Interpola cor do meteoro baseado em HP:
        - Quando danificado, intepola para branco.
        """
        ratio = self.hp / self.max_hp
        r, g, b = self._base_color
        r = int(r + (255 - r) * (1 - ratio))
        g = int(g + (255 - g) * (1 - ratio))
        b = int(b + (255 - b) * (1 - ratio))
        return (r, g, b)