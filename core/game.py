import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from core.state_manager import StateManager
from states.playing_state import PlayingState
from states.game_over_state import GameOverState
from states.upgrade_state import UpgradeState


class Game:
    """
    Ponto central da aplicação.

    Responsabilidades:
        - Inicializar o Pygame e a janela
        - Instanciar e registrar os estados
        - Executar o loop principal (eventos → update → draw)
        - Delegar tudo o mais ao estado ativo via StateManager
    """

    def __init__(self) -> None:
        pygame.init()
        self.screen  = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock   = pygame.time.Clock()
        pygame.display.set_caption(TITLE)

        self._sm = StateManager()
        self._register_states()
        self._sm.change("playing")

        self._running = True

    # ── Loop principal ────────────────────────────────────────────────────────

    def run(self) -> None:
        while self._running:
            self.clock.tick(FPS)
            events = pygame.event.get()

            # Evento de fechar janela — tratado aqui, não nos estados
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False

            state = self._sm.current
            if state:
                state.handle_events(events)
                state.update()
                state.draw(self.screen)

                # Verifica se o estado pediu transição
                if state.done and state.next_state:
                    self._sm.change(state.next_state)

            pygame.display.flip()

        pygame.quit()

    # ── Registro de estados ───────────────────────────────────────────────────

    def _register_states(self) -> None:
        self._sm.register("playing",   PlayingState())
        self._sm.register("game_over", GameOverState())
        self._sm.register("upgrade",   UpgradeState())