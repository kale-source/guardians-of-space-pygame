import pygame
from states.base_state import BaseState
from components.player import Player
from components.meteor import Meteor
from components.stars import StarField
from settings import settings


class PlayingState(BaseState):
    """
    Estado principal: gerencia player, meteoros, balas, progressão e colisões.

    Transições:
        → "game_over"  quando um meteoro colide com o player
    """

    def __init__(self) -> None:
        super().__init__()
        self._setup()

    # ── BaseState interface ───────────────────────────────────────────────────

    def on_enter(self, previous_state: str | None = None) -> None:
        if previous_state != "upgrade":
            self._setup()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.star_field.toggle()

    def update(self) -> None:
        self._tick_timer()
        self._check_level_up()
        self._handle_player()
        self._spawn_meteors()
        self._update_meteors()
        self._update_bullets()
        self._check_bullet_meteor_collisions()
        self._check_player_meteor_collision()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        self.star_field.update_draw(screen)
        self.bullet_group.draw(screen)
        self.meteor_group.draw(screen)
        self.player.draw(screen)
        self._draw_hud(screen)

    # ── Setup / reset ─────────────────────────────────────────────────────────

    def _setup(self) -> None:
        self.player      = Player(settings.PLAYER_START_X, settings.PLAYER_START_Y)
        self.star_field  = StarField()

        self.meteor_group: pygame.sprite.Group = pygame.sprite.Group()
        self.bullet_group: pygame.sprite.Group = pygame.sprite.Group()

        self.spawn_timer      = 0
        self.level            = 1
        self.score            = 0
        self.escaped_meteors  = 0
        self.total_kills      = 0    # total acumulado para trigger de upgrade
        self._next_upgrade_at = settings.UPGRADE_EVERY_N_KILLS

        self._start_ticks   = pygame.time.get_ticks()
        self._last_level_up = 0

    # ── Lógica privada ────────────────────────────────────────────────────────

    def _tick_timer(self) -> None:
        elapsed_ms   = pygame.time.get_ticks() - self._start_ticks
        self.seconds = elapsed_ms // 1000

    def _check_level_up(self) -> None:
        threshold = self.seconds - (self.seconds % settings.LEVEL_UP_INTERVAL)
        if threshold > 0 and threshold > self._last_level_up:
            self.level         += 1
            self._last_level_up = threshold

    def _handle_player(self) -> None:
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.bullet_group)     # passa o grupo de balas

    def _spawn_meteors(self) -> None:
        current_delay = max(
            settings.METEOR_SPAWN_DELAY_MIN,
            settings.METEOR_SPAWN_DELAY - (self.level - 1) * settings.METEOR_SPAWN_DELAY_SCALE,
        )
        self.spawn_timer += 1
        if self.spawn_timer >= current_delay:
            self.meteor_group.add(Meteor(self.level))
            self.spawn_timer = 0

    def _update_meteors(self) -> None:
        self.meteor_group.update()
        for meteor in list(self.meteor_group):
            if meteor.is_off_screen():  # type: ignore[attr-defined]
                meteor.kill()
                self.escaped_meteors += 1
                if self.escaped_meteors >= settings.MAX_ESCAPED_METEORS:
                    self.done       = True
                    self.next_state = "game_over"

    def _update_bullets(self) -> None:
        self.bullet_group.update()
        for bullet in list(self.bullet_group):
            if bullet.is_off_screen():  # type: ignore[attr-defined]
                bullet.kill()

    def _check_bullet_meteor_collisions(self) -> None:
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
                    self.score       += 1
                    self.total_kills += 1
                    if self.total_kills >= self._next_upgrade_at:
                        self._next_upgrade_at += settings.UPGRADE_EVERY_N_KILLS
                        self.done       = True
                        self.next_state = "upgrade"

    def apply_upgrade(self, choice: str) -> None:
        """Chamado pelo StateManager ao retornar do UpgradeState."""
        if choice == "speed":
            self.player.apply_speed_upgrade(settings.UPGRADE_SPEED_BONUS)
        elif choice == "damage":
            self.player.apply_damage_upgrade(settings.UPGRADE_DAMAGE_BONUS)

    def _check_player_meteor_collision(self) -> None:
        hit = pygame.sprite.spritecollide(
            self.player, self.meteor_group,
            dokill=False,
            collided=pygame.sprite.collide_mask,
        )
        if hit:
            self.done       = True
            self.next_state = "game_over"

    def _draw_hud(self, screen: pygame.Surface) -> None:
        hud = settings.FONT_DETAILS.render(
            f"Segundos: {self.seconds}   Level: {self.level}   "
            f"Score: {self.score}   Escaparam: {self.escaped_meteors}/{settings.MAX_ESCAPED_METEORS}   "
            f"Próximo upgrade: {self._next_upgrade_at - self.total_kills}",
            True, settings.WHITE,
        )
        screen.blit(hud, (10, 10))