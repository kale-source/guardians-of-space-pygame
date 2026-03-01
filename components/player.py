import pygame
from core.entity import Entity
from settings import (
    WIDTH, HEIGHT,
    PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT,
    BULLET_COOLDOWN, BULLET_CHARGE_MAX_FRAMES,
    BULLET_COLOR, BULLET_CHARGED_COLOR,
    WHITE,
)
from components.bullet import Bullet


class Player(Entity):
    """
    Nave controlada pelo jogador.

    Movimento: setas direcionais
    Disparo:
        - Tap em ESPAÇO  → bala normal (charge_ratio = 0)
        - Segurar ESPAÇO → carga acumula até BULLET_CHARGE_MAX_FRAMES
        - Soltar ESPAÇO  → dispara com charge_ratio proporcional ao tempo segurado

    Feedback visual:
        Um arco é desenhado abaixo da nave indicando o nível de carga atual.
        A cor interpola de ciano (vazio) a laranja (cheio).
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed            = PLAYER_SPEED
        self._cooldown_timer  = 0
        self._charge_frames   = 0
        self._space_held      = False
        self.damage_bonus     = 0     # acumulado via upgrades

    # ── Entity interface ──────────────────────────────────────────────────────

    def _build_image(self) -> None:
        w, h = self.width, self.height
        pygame.draw.polygon(
            self.image, WHITE,
            [(w // 2, 0), (0, h), (w, h)],
        )

    def update(
        self,
        keys: pygame.key.ScancodeWrapper,
        bullet_group: pygame.sprite.Group,
        *args,
        **kwargs,
    ) -> None:
        self._move(keys)
        self._handle_charge(keys, bullet_group)
        self._update_charge_visual()

    # ── Lógica privada ────────────────────────────────────────────────────────

    def _move(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_LEFT]:
            self.pos_x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.pos_x += self.speed
        if keys[pygame.K_UP]:
            self.pos_y -= self.speed
        if keys[pygame.K_DOWN]:
            self.pos_y += self.speed

        self.pos_x = max(0.0, min(self.pos_x, WIDTH  - self.width))
        self.pos_y = max(0.0, min(self.pos_y, HEIGHT - self.height))
        self._sync_rect()

    def _handle_charge(
        self,
        keys: pygame.key.ScancodeWrapper,
        bullet_group: pygame.sprite.Group,
    ) -> None:
        space_pressed = bool(keys[pygame.K_SPACE])

        if self._cooldown_timer > 0:
            self._cooldown_timer -= 1

        if space_pressed:
            # Acumula carga enquanto o espaço é segurado (cap em max)
            self._charge_frames = min(self._charge_frames + 1, BULLET_CHARGE_MAX_FRAMES)
        elif self._space_held and not space_pressed:
            # Espaço foi SOLTO: dispara com a carga acumulada
            if self._cooldown_timer == 0:
                ratio = self._charge_frames / BULLET_CHARGE_MAX_FRAMES
                self._fire(bullet_group, charge_ratio=ratio)
                self._cooldown_timer = BULLET_COOLDOWN
            self._charge_frames = 0

        self._space_held = space_pressed

    def _fire(self, bullet_group: pygame.sprite.Group, charge_ratio: float) -> None:
        """Instancia a bala centralizada na ponta da nave."""
        tip_x = self.pos_x + self.width  // 2
        tip_y = self.pos_y
        bullet_group.add(Bullet(tip_x, tip_y, charge_ratio, self.damage_bonus))

    # ── Upgrades ──────────────────────────────────────────────────────────────

    def apply_speed_upgrade(self, bonus: int) -> None:
        if(self.speed >= 30):
            print("Velocidade máxima atingida. Upgrade de velocidade não aplicado.")
            return
        else:   
            self.speed += bonus
            print(f"Velocidade atualizada: {self.speed}")
    
    def apply_damage_upgrade(self, bonus: int) -> None:
        self.damage_bonus += bonus
        print(f"Bônus de dano atualizado: {self.damage_bonus}")

    def _update_charge_visual(self) -> None:
        """
        Redesenha a Surface do player incluindo o indicador de carga.
        Um arco abaixo da nave cresce e muda de cor conforme a carga aumenta.
        """
        self.image.fill((0, 0, 0, 0))

        # Nave
        w, h = self.width, self.height
        pygame.draw.polygon(self.image, WHITE, [(w // 2, 0), (0, h), (w, h)])

        # Indicador de carga — só exibe se estiver carregando
        if self._charge_frames > 0:
            ratio = self._charge_frames / BULLET_CHARGE_MAX_FRAMES

            # Interpola cor: ciano → laranja
            r = int(BULLET_COLOR[0] + (BULLET_CHARGED_COLOR[0] - BULLET_COLOR[0]) * ratio)
            g = int(BULLET_COLOR[1] + (BULLET_CHARGED_COLOR[1] - BULLET_COLOR[1]) * ratio)
            b = int(BULLET_COLOR[2] + (BULLET_CHARGED_COLOR[2] - BULLET_COLOR[2]) * ratio)
            color = (r, g, b)

            # Arco que cresce de 0° a 180° conforme a carga
            arc_rect = pygame.Rect(2, h - 6, w - 4, 10)
            arc_end  = 3.1416 * ratio                   # 0 → π
            if arc_end > 0.05:
                pygame.draw.arc(self.image, color, arc_rect, 0, arc_end, 2)