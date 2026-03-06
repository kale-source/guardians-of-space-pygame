import pygame
from core.entity import Entity
from settings import settings
from components.bullet import Bullet


class Player(Entity):
    """
    Nave do jogador com movimento e disparo acumulável:
    - Movimento com setas e WASD, limitado às bordas da tela.
    - Sistema de carga para disparos com dano variável.
    - Upgrades de velocidade, dano e cooldown.
    """

    def __init__(self, x, y):
        super().__init__(x, y, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
        self.speed = settings.PLAYER_SPEED
        self.cooldown = settings.BULLET_COOLDOWN
        self._cooldown_timer = 0
        self._charge_frames = 0
        self._space_held = False
        self.damage_bonus = 0

    def _build_image(self):
        """
        Desenha a nave como um triângulo branco.
        """
        w, h = self.width, self.height
        pygame.draw.polygon(
            self.image, settings.WHITE,
            [(w // 2, 0), (0, h), (w, h)],
        )

    def update(self, keys, bullet_group):
        """
        Atualiza a lógica do jogador:
        - Processa movimento baseado nas teclas pressionadas.
        - Gerencia carga e disparo de balas.
        - Atualiza visual de carga.
        """
        self._move(keys)
        self._handle_charge(keys, bullet_group)
        self._update_charge_visual()

    def _move(self, keys):
        """
        Movimento com setas e WASD, limitado à tela:
        - Processa entrada do teclado para movimento.
        - Limita posição dentro dos limites da tela.
        """
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos_x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pos_y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pos_y += self.speed

        # Limitar bounding box
        self.pos_x = max(0.0, min(self.pos_x, settings.WIDTH - self.width))
        self.pos_y = max(0.0, min(self.pos_y, settings.HEIGHT - self.height))
        self._sync_rect()

    def _handle_charge(self, keys, bullet_group):
        """
        Gerencia carga e disparo de balas:
        - Acumula carga enquanto ESPAÇO está pressionado.
        - Dispara quando ESPAÇO é solto, gerando bala com carga apropriada.
        - Controla cooldown entre disparos.
        """
        space_pressed = bool(keys[pygame.K_SPACE])

        if self._cooldown_timer > 0:
            self._cooldown_timer -= 1

        if space_pressed:
            self._charge_frames = min(self._charge_frames + 1, settings.BULLET_CHARGE_MAX_FRAMES)
        elif self._space_held and not space_pressed:
            if self._cooldown_timer == 0:
                ratio = self._charge_frames / settings.BULLET_CHARGE_MAX_FRAMES
                self._fire(bullet_group, charge_ratio=ratio)
                self._cooldown_timer = settings.BULLET_COOLDOWN
            self._charge_frames = 0

        self._space_held = space_pressed

    def _fire(self, bullet_group, charge_ratio):
        """
        Cria e dispara uma bala na ponta da nave:
        - Define posição na ponta do triângulo.
        - Passa ratio de carga e bonus de dano à bala.
        """
        tip_x = self.pos_x + self.width // 2
        tip_y = self.pos_y
        bullet_group.add(Bullet(tip_x, tip_y, charge_ratio, self.damage_bonus))

    def apply_speed_upgrade(self, bonus):
        """
        Aplica upgrade de velocidade:
        - Aumenta velocidade de movimento do jogador.
        - Verifica limite máximo de velocidade.
        """
        if self.speed >= 30:
            print("Velocidade máxima atingida!")
        else:
            self.speed += bonus
            print(f"Velocidade: {self.speed}")

    def apply_damage_upgrade(self, bonus):
        """
        Aplica upgrade de dano:
        - Aumenta dano bônus aplicado às balas.
        """
        self.damage_bonus += bonus
        print(f"Dano bônus: {self.damage_bonus}")
    
    def apply_cooldown_upgrade(self, cooldown_bonus):
        """
        Aplica upgrade de cooldown:
        - Diminui tempo de espera entre disparos.
        """
        self.cooldown -= cooldown_bonus
        print(f"Cooldown diminuido: {self.cooldown}")

    def _update_charge_visual(self):
        """
        Desenha um arco de carga abaixo da nave, mudando de cor conforme a carga aumenta (azul para laranja). 
        O arco é proporcional ao tempo de carga, dando feedback visual ao jogador sobre o poder do próximo disparo.

        O arco é desenhado usando pygame.draw.arc, com um retângulo delimitador posicionado abaixo da nave.
        """
        self.image.fill((0, 0, 0, 0))

        w, h = self.width, self.height
        pygame.draw.polygon(self.image, settings.WHITE, [(w // 2, 0), (0, h), (w, h)])

        if self._charge_frames > 0:
            ratio = self._charge_frames / settings.BULLET_CHARGE_MAX_FRAMES

            r = int(settings.BULLET_COLOR[0] + (settings.BULLET_CHARGED_COLOR[0] - settings.BULLET_COLOR[0]) * ratio)
            g = int(settings.BULLET_COLOR[1] + (settings.BULLET_CHARGED_COLOR[1] - settings.BULLET_COLOR[1]) * ratio)
            b = int(settings.BULLET_COLOR[2] + (settings.BULLET_CHARGED_COLOR[2] - settings.BULLET_COLOR[2]) * ratio)
            color = (r, g, b)

            arc_rect = pygame.Rect(2, h - 6, w - 4, 10)
            arc_end = 3.1416 * ratio
            if arc_end > 0.05:
                pygame.draw.arc(self.image, color, arc_rect, 0, arc_end, 2)