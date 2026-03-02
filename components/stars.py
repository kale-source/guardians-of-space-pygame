import pygame
import random
from settings import settings

class Star:
    """
    Estrela individual com movimento vertical e efeito de piscar.

    Velocidades variadas criam um parallax simples:
    estrelas rápidas (e maiores) parecem mais próximas,
    lentas (e menores) mais distantes.
    """

    __slots__ = ("x", "y", "brightness", "direction", "speed", "size")

    def __init__(self, randomize_y: bool = True):
        self.x          = random.randint(0, settings.WIDTH)
        self.y          = float(random.randint(0, settings.HEIGHT) if randomize_y else random.randint(-settings.HEIGHT, 0))
        self.speed      = random.uniform(settings.STAR_SPEED_MIN, settings.STAR_SPEED_MAX)
        self.size       = 1 if self.speed < (settings.STAR_SPEED_MIN + settings.STAR_SPEED_MAX) / 2 else 2
        self.brightness = random.randint(settings.STAR_BRIGHTNESS_MIN, settings.STAR_BRIGHTNESS_MAX)
        self.direction  = random.choice((-1, 1))

    def update(self):
        # Movimento vertical — reposiciona no topo ao sair pela base
        self.y += self.speed
        if self.y > settings.HEIGHT:
            self.y = float(random.randint(-10, 0))
            self.x = random.randint(0, settings.WIDTH)

        # Efeito de piscar
        self.brightness += self.direction * settings.STAR_BLINK_SPEED
        if self.brightness >= settings.STAR_BRIGHTNESS_MAX:
            self.brightness = settings.STAR_BRIGHTNESS_MAX
            self.direction  = -1
        elif self.brightness <= settings.STAR_BRIGHTNESS_MIN:
            self.brightness = settings.STAR_BRIGHTNESS_MIN
            self.direction  = 1

    def draw(self, screen: pygame.Surface):
        b = self.brightness
        pygame.draw.circle(screen, (b, b, b), (self.x, int(self.y)), self.size)


class StarField:
    """
    Gerencia o campo de estrelas em movimento do background.

    Uso:
        field = StarField()
        field.toggle()             # liga/desliga
        field.update_draw(screen)  # atualiza e desenha num único passo
    """

    def __init__(self):
        # randomize_y=True distribui as estrelas pela tela inteira no início,
        # evitando que todas apareçam do topo ao mesmo tempo
        self._stars  = [Star(randomize_y=True) for _ in range(settings.NUM_STARS)]
        self.visible = True

    def toggle(self):
        self.visible = not self.visible

    def update_draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        for star in self._stars:
            star.update()
            star.draw(screen)