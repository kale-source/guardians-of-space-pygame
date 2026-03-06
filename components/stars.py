import pygame
import random
from settings import settings

class Star:
    """
    Estrela individual com movimento vertical e efeito de piscar:
    - Velocidades variadas criam um parallax simples.
    - Estrelas rápidas (e maiores) parecem mais próximas.
    - Lentas (e menores) parecem mais distantes.
    """

    __slots__ = ("x", "y", "brightness", "direction", "speed", "size")

    def __init__(self, randomize_y: bool = True):
        """
        Inicializa uma estrela com posição e propriedades aleatórias:
        - Posição varia aleatoriamente na tela.
        - Velocidade define tamanho (paralaxe).
        - Brilho inicial aleatório com direção de variação.
        """
        self.x          = random.randint(0, settings.WIDTH)
        self.y          = float(random.randint(0, settings.HEIGHT) if randomize_y else random.randint(-settings.HEIGHT, 0))
        self.speed      = random.uniform(settings.STAR_SPEED_MIN, settings.STAR_SPEED_MAX)
        self.size       = 1 if self.speed < (settings.STAR_SPEED_MIN + settings.STAR_SPEED_MAX) / 2 else 2
        self.brightness = random.randint(settings.STAR_BRIGHTNESS_MIN, settings.STAR_BRIGHTNESS_MAX)
        self.direction  = random.choice((-1, 1))

    def update(self):
        """
        Atualiza a estrela a cada frame:
        - Move verticalmente com parallax baseado em velocidade.
        - Reposiciona no topo com atributos renovados ao sair pela base.
        - Aplica efeito de piscar variando o brilho.
        """
        # deslocamento vertical
        self.y += self.speed

        # se saiu da tela, reaparecer no topo com valores aleatórios
        if self.y > settings.HEIGHT:
            self.y = float(random.randint(-settings.HEIGHT, 0))
            self.x = random.randint(0, settings.WIDTH)
            # renovar velocidade/tamanho para manter aleatoriedade contínua
            self.speed = random.uniform(settings.STAR_SPEED_MIN, settings.STAR_SPEED_MAX)
            self.size = 1 if self.speed < (settings.STAR_SPEED_MIN + settings.STAR_SPEED_MAX) / 2 else 2

        # piscar: ajustar brilho, inverter direção nos limites
        self.brightness += self.direction * settings.STAR_BLINK_SPEED
        if self.brightness <= settings.STAR_BRIGHTNESS_MIN:
            self.brightness = settings.STAR_BRIGHTNESS_MIN
            self.direction = 1
        elif self.brightness >= settings.STAR_BRIGHTNESS_MAX:
            self.brightness = settings.STAR_BRIGHTNESS_MAX
            self.direction = -1

    def draw(self, screen: pygame.Surface):
        """
        Renderiza a estrela na tela:
        - Desenha círculo com brilho atual.
        """
        b = self.brightness
        pygame.draw.circle(screen, (b, b, b), (self.x, int(self.y)), self.size)


class StarField:
    """
    Gerencia o campo de estrelas em movimento do background:
    - Mantém lista de estrelas com movimento paralaxe.
    - Permite ligar/desligar a visibilidade do campo.
    - Atualiza e renderiza todas as estrelas simultaneamente.
    """

    def __init__(self):
        """
        Inicializa o campo de estrelas:
        - Cria lista com NUM_STARS estrelas distribuídas na tela.
        - Estrelas começam visíveis.
        """
        # randomize_y=True distribui as estrelas pela tela inteira no início,
        # evitando que todas apareçam do topo ao mesmo tempo
        self._stars  = [Star(randomize_y=True) for _ in range(settings.NUM_STARS)]
        self.visible = True

    def toggle(self):
        """
        Liga/desliga a visibilidade do campo de estrelas.
        """
        self.visible = not self.visible

    def update_draw(self, screen: pygame.Surface):
        """
        Atualiza e renderiza todas as estrelas:
        - Ignora atualização se o campo não está visível.
        - Atualiza posição e brilho de cada estrela.
        - Desenha estrelas na tela.
        """
        if not self.visible:
            return
        for star in self._stars:
            star.update()
            star.draw(screen)