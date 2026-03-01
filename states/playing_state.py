import pygame
from states.base_state import BaseState
from components.player import Player
from components.meteor import Meteor
from components.stars import StarField
from settings import (
    WIDTH, HEIGHT,
    PLAYER_START_X, PLAYER_START_Y,
    METEOR_SPAWN_DELAY,
    LEVEL_UP_INTERVAL,
    FONT_DETAILS,
    WHITE,
)


class PlayingState(BaseState):
    """
    Estado principal: gerencia player, meteoros, balas, progressão e colisões.

    Transições:
        → "game_over"  quando um meteoro colide com o player
    """

    def __init__(self):
        super().__init__()
        self._setup()

    # ── BaseState interface ───────────────────────────────────────────────────

    def on_enter(self, previous_state: str | None = None):
        self._setup()

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.star_field.toggle()

    def update(self):
        self._tick_timer()
        self._check_level_up()
        self._handle_player()
        self._spawn_meteors()
        self._update_meteors()
        self._update_bullets()
        self._check_bullet_meteor_collisions()
        self._check_player_meteor_collision()

    def draw(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        self.star_field.update_draw(screen)
        self.bullet_group.draw(screen)
        self.meteor_group.draw(screen)
        self.player.draw(screen)
        self._draw_hud(screen)

    # ── Setup / reset ─────────────────────────────────────────────────────────

    def _setup(self):
        self.player      = Player(PLAYER_START_X, PLAYER_START_Y)
        self.star_field  = StarField()

        self.meteor_group: pygame.sprite.Group = pygame.sprite.Group()
        self.bullet_group: pygame.sprite.Group = pygame.sprite.Group()

        self.spawn_timer = 0
        self.level       = 1
        self.score       = 0

        self._start_ticks   = pygame.time.get_ticks()
        self._last_level_up = 0

    # ── Lógica privada ────────────────────────────────────────────────────────

    def _tick_timer(self):
        elapsed_ms   = pygame.time.get_ticks() - self._start_ticks
        self.seconds = elapsed_ms // 1000

    def _check_level_up(self):
        threshold = self.seconds - (self.seconds % LEVEL_UP_INTERVAL)
        if threshold > 0 and threshold > self._last_level_up:
            self.level         += 1
            self._last_level_up = threshold

    def _handle_player(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.bullet_group)     # passa o grupo de balas

    def _spawn_meteors(self):
        self.spawn_timer += 1
        if self.spawn_timer >= METEOR_SPAWN_DELAY:
            self.meteor_group.add(Meteor(self.level))
            self.spawn_timer = 0

    def _update_meteors(self):
        self.meteor_group.update()
        for meteor in list(self.meteor_group):
            if meteor.is_off_screen():  # type: ignore[attr-defined]
                meteor.kill()

    def _update_bullets(self):
        self.bullet_group.update()
        for bullet in list(self.bullet_group):
            if bullet.is_off_screen():  # type: ignore[attr-defined]
                bullet.kill()

    def _check_bullet_meteor_collisions(self):
        """
        Para cada bala, verifica colisão com meteoros via máscara.

        groupcollide retorna {bullet: [meteoros_atingidos]}.
        dokill=True nas balas garante que cada tiro some ao acertar.
        Os meteoros NÃO são destruídos aqui — isso é responsabilidade
        do meteor.hit(), que decide se o HP chegou a 0.
        """
        hits: dict = pygame.sprite.groupcollide(
            self.bullet_group,
            self.meteor_group,
            True,                   # dokilla — bala some ao acertar
            False,                  # dokillb — meteoro sobrevive (hit() decide o destino)
            pygame.sprite.collide_mask,
        )
        for bullet, meteors_hit in hits.items():
            for meteor in meteors_hit:
                meteor.hit(bullet.damage)        # type: ignore[attr-defined]
                if not meteor.alive():
                    self.score += 1

    def _check_player_meteor_collision(self):
        hit = pygame.sprite.spritecollide(
            self.player, self.meteor_group,
            dokill=False,
            collided=pygame.sprite.collide_mask,
        )
        if hit:
            self.done       = True
            self.next_state = "game_over"

    def _draw_hud(self, screen: pygame.Surface):
        hud = FONT_DETAILS.render(
            f"Segundos: {self.seconds}   Level: {self.level}   Score: {self.score}",
            True, WHITE,
        )
        screen.blit(hud, (10, 10))