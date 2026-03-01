import pygame
import random
from settings import (
    WIDTH, HEIGHT,
    NUM_STARS, STAR_BRIGHTNESS_MIN, STAR_BRIGHTNESS_MAX, STAR_BLINK_SPEED,
    STAR_SPEED_MIN, STAR_SPEED_MAX,
)


class Star:
    """
    Estrela individual com movimento vertical e efeito de piscar.

    Velocidades variadas criam um parallax simples:
    estrelas rápidas (e maiores) parecem mais próximas,
    lentas (e menores) mais distantes.
    """

    __slots__ = ("x", "y", "brightness", "direction", "speed", "size")

    def __init__(self, randomize_y: bool = True) -> None:
        self.x          = random.randint(0, WIDTH)
        self.y          = float(random.randint(0, HEIGHT) if randomize_y else random.randint(-HEIGHT, 0))
        self.speed      = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)
        self.size       = 1 if self.speed < (STAR_SPEED_MIN + STAR_SPEED_MAX) / 2 else 2
        self.brightness = random.randint(STAR_BRIGHTNESS_MIN, STAR_BRIGHTNESS_MAX)
        self.direction  = random.choice((-1, 1))

    def update(self) -> None:
        # Movimento vertical — reposiciona no topo ao sair pela base
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = float(random.randint(-10, 0))
            self.x = random.randint(0, WIDTH)

        # Efeito de piscar
        self.brightness += self.direction * STAR_BLINK_SPEED
        if self.brightness >= STAR_BRIGHTNESS_MAX:
            self.brightness = STAR_BRIGHTNESS_MAX
            self.direction  = -1
        elif self.brightness <= STAR_BRIGHTNESS_MIN:
            self.brightness = STAR_BRIGHTNESS_MIN
            self.direction  = 1

    def draw(self, screen: pygame.Surface) -> None:
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

    def __init__(self) -> None:
        # randomize_y=True distribui as estrelas pela tela inteira no início,
        # evitando que todas apareçam do topo ao mesmo tempo
        self._stars  = [Star(randomize_y=True) for _ in range(NUM_STARS)]
        self.visible = True

    def toggle(self) -> None:
        self.visible = not self.visible

    def update_draw(self, screen: pygame.Surface) -> None:
        if not self.visible:
            return
        for star in self._stars:
            star.update()
            star.draw(screen)