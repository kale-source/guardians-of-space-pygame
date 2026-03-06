import pygame
from settings import settings
from components.player import Player
from components.meteor import Meteor
from components.stars import StarField


class Game:
    """
    Loop principal do jogo com gerenciamento de estados:
    - Controla estados: "playing", "game_over" ou "upgrade".
    - Usa métodos privados para cada estado, mantendo lógica organizada.
    - _init_playing: configura o estado de jogo.
    - _update_playing: atualiza lógica, movimentação, spawn e colisões.
    - _draw_playing: renderiza estado de jogo com HUD.
    - _draw_game_over: renderiza tela de game over com estatísticas.
    - _draw_upgrade: renderiza tela de upgrades com opções.
    """

    def __init__(self):
        """
        Inicializa o Pygame, configura janela e estado inicial:
        - Configura display com dimensões e título.
        - Inicializa clock para controle de FPS.
        - Define estado inicial como "playing".
        """
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(settings.TITLE)
        
        # Estado atual do jogo
        self.game_state = "playing"
        
        # Inicializar jogo
        self._init_playing()

    def run(self):
        """
        Executa o loop principal do jogo:
        - Controla frame rate com clock.
        - Processa eventos do jogador.
        - Atualiza e renderiza baseado no estado atual.
        - Limpa recursos ao sair.
        """
        running = True
        while running:
            self.clock.tick(settings.FPS)
            events = pygame.event.get()

            # Verificar sair
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Executar lógica baseado no estado
            if self.game_state == "playing":
                self._update_playing(events)
                self._draw_playing()
            elif self.game_state == "game_over":
                self._draw_game_over(events)
            elif self.game_state == "upgrade":
                self._draw_upgrade(events)

            pygame.display.flip()

        pygame.quit()

    # ═══════════════════════════════════════════════════════════════════════════
    # ESTADO: PLAYING
    # ═══════════════════════════════════════════════════════════════════════════

    def _init_playing(self):
        """
        Configura o estado de jogo (playing):
        - Cria player, campo de estrelas e grupos de sprites.
        - Inicializa variáveis de controle (level, score, timers).
        - Reseta upgrades para nova sessão.
        """
        self.player = Player(settings.PLAYER_START_X, settings.PLAYER_START_Y)
        self.star_field = StarField()
        self.meteor_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        self.spawn_timer = 0
        self.level = 1
        self.score = 0
        self.escaped_meteors = 0
        self.total_kills = 0
        self._next_upgrade_at = settings.UPGRADE_EVERY_N_KILLS

        self._start_ticks = pygame.time.get_ticks()
        self._last_level_up = 0

    def _update_playing(self, events):
        """
        Atualiza a lógica do jogo:
        - Gerencia o tempo e o level up baseado no tempo.
        - Atualiza o player com input do teclado.
        - Controla o spawn de meteoros baseado no level.
        - Atualiza meteoros e balas, removendo os que saem da tela.
        - Gerencia colisões entre balas e meteoros, e entre player e meteoros, atualizando score, kills e transições de estado conforme necessário.
        """
        # Pequenos hotkeys
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                self.star_field.toggle()

        # Timer
        elapsed_ms = pygame.time.get_ticks() - self._start_ticks
        # Converter para segundos inteiros para facilitar o display e o controle de level up
        self.seconds = elapsed_ms // 1000

        # Level up check
        threshold = self.seconds - (self.seconds % settings.LEVEL_UP_INTERVAL)
        if threshold > 0 and threshold > self._last_level_up:
            self.level += 1
            self._last_level_up = threshold

        # Atualizar player
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.bullet_group)

        # Spawn meteoros
        current_delay = max(
            settings.METEOR_SPAWN_DELAY_MIN,
            settings.METEOR_SPAWN_DELAY - (self.level - 1) * settings.METEOR_SPAWN_DELAY_SCALE,
        )
        self.spawn_timer += 1
        if self.spawn_timer >= current_delay:
            self.meteor_group.add(Meteor(self.level))
            self.spawn_timer = 0

        # Atualizar meteoros
        self.meteor_group.update()
        for meteor in list(self.meteor_group):
            if meteor.is_off_screen():
                meteor.kill()
                self.escaped_meteors += 1
                if self.escaped_meteors >= settings.MAX_ESCAPED_METEORS:
                    self.game_state = "game_over"

        # Atualizar balas
        self.bullet_group.update()
        for bullet in list(self.bullet_group):
            if bullet.is_off_screen():
                bullet.kill()

        # Colisões: balas ↔ meteoros
        hits = pygame.sprite.groupcollide(
            self.bullet_group,          # grupo 1
            self.meteor_group,          # grupo 2
            True,                       # dokill1: mata a bala automaticamente ao colidir
            False,                      # dokill2: NÃO mata o meteoro automaticamente
            pygame.sprite.collide_mask  # método de detecção: pixel-perfect
        )

        for bullet, meteors_hit in hits.items():
            for meteor in meteors_hit:
                meteor.hit(bullet.damage)
                if not meteor.alive():
                    self.score += 1
                    self.total_kills += 1
                    if self.total_kills >= self._next_upgrade_at:
                        self._next_upgrade_at += settings.UPGRADE_EVERY_N_KILLS
                        self.game_state = "upgrade"

        # Colisões: player ↔ meteoro
        hit = pygame.sprite.spritecollide(
            self.player, 
            self.meteor_group,
            dokill=False,
            collided=pygame.sprite.collide_mask,
        )

        if hit:
            self.game_state = "game_over"

    def _draw_playing(self):
        """
        Renderiza o estado de jogo:
        - Desenha background, campo de estrelas, sprites.
        - Renderiza HUD com informações de jogo.
        """
        self.screen.fill((0, 0, 0))
        self.star_field.update_draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.meteor_group.draw(self.screen)
        self.player.draw(self.screen)

        # HUD
        hud = settings.FONT_DETAILS.render(
            f"Segundos: {self.seconds}   Level: {self.level}   "
            f"Score: {self.score}   Escaparam: {self.escaped_meteors}/{settings.MAX_ESCAPED_METEORS}   "
            f"Próximo upgrade: {self._next_upgrade_at - self.total_kills}",
            True, settings.WHITE,
        )
        self.screen.blit(hud, (10, 10))

    # ═══════════════════════════════════════════════════════════════════════════
    # ESTADO: GAME OVER
    # ═══════════════════════════════════════════════════════════════════════════

    def _draw_game_over(self, events):
        """
        Renderiza a tela de game over:
        - Exibe estatísticas finais (tempo, level, score, escapados).
        - Aguarda ESPAÇO para reiniciar o jogo.
        """
        self.screen.fill((0, 0, 0))

        # Título
        title = settings.FONT_MAIN.render("GAME OVER", True, settings.RED)
        title_rect = title.get_rect(center=(settings.WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Estatísticas
        stats_text = (
            f"Tempo: {self.seconds}s\n"
            f"Level: {self.level}\n"
            f"Score: {self.score}\n"
            f"Escaparam: {self.escaped_meteors}"
        )
        for i, line in enumerate(stats_text.split("\n")):
            stat = settings.FONT_SUBTITLE.render(line, True, settings.WHITE)
            self.screen.blit(stat, (settings.WIDTH // 2 - 100, 200 + i * 40))

        # Instrução
        restart_text = settings.FONT_SUBTITLE.render("Pressione ESPAÇO para reiniciar", True, (150, 150, 150))
        restart_rect = restart_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT - 100))
        self.screen.blit(restart_text, restart_rect)

        # Input
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game_state = "playing"
                self._init_playing()

    # ═══════════════════════════════════════════════════════════════════════════
    # ESTADO: UPGRADE
    # ═══════════════════════════════════════════════════════════════════════════

    def _draw_upgrade(self, events):
        """
        Renderiza a tela de seleção de upgrade:
        - Exibe 3 opções: (1) Velocidade, (2) Dano, (3) Cooldown.
        - Aguarda input do jogador e aplica upgrade escolhido.
        - Retorna ao estado "playing" após escolha.
        """
        self.screen.fill((0, 0, 0))

        title = settings.FONT_MAIN.render("UPGRADE!", True, (255, 200, 0))
        title_rect = title.get_rect(center=(settings.WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Opções
        speed_text = settings.FONT_DETAILS.render("(1) Velocidade", True, settings.WHITE)
        damage_text = settings.FONT_DETAILS.render("(2) Dano", True, settings.WHITE)
        cooldown_bullet_text = settings.FONT_DETAILS.render("(3) Diminuir Cooldown", True, settings.WHITE)

        self.screen.blit(speed_text, (settings.WIDTH // 2 - 100, 250))
        self.screen.blit(damage_text, (settings.WIDTH // 2 - 100, 350))
        self.screen.blit(cooldown_bullet_text, (settings.WIDTH // 2 - 100, 450))

        # Input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player.apply_speed_upgrade(settings.UPGRADE_SPEED_BONUS)
                    self.game_state = "playing"
                elif event.key == pygame.K_2:
                    self.player.apply_damage_upgrade(settings.UPGRADE_DAMAGE_BONUS)
                    self.game_state = "playing"
                elif event.key == pygame.K_3:
                    self.player.apply_cooldown_upgrade(settings.UPGRADE_COOLDOWN_BONUS)
                    self.game_state = "playing"