import pygame
from states.base_state import BaseState
from settings import WIDTH, HEIGHT, FONT_MAIN, FONT_SUB, FONT_DETAILS, WHITE, RED

class GameOverState(BaseState):
    """
    Tela exibida quando o player colide com um meteoro.

    Recebe o contexto (segundos, level, score) do PlayingState via on_enter
    e exibe o overlay de derrota.

    Transições:
        → "playing"  ao pressionar ESC (reinicia o jogo)
    """

    def __init__(self):
        super().__init__()
        self.seconds = 0
        self.level   = 1
        self.score   = 0

        # Overlay semitransparente reutilizável
        self._overlay = pygame.Surface((WIDTH, HEIGHT))
        self._overlay.set_alpha(150)
        self._overlay.fill((0, 0, 0))

    # ── BaseState interface ───────────────────────────────────────────────────

    def on_enter(self, previous_state: str | None = None):
        """
        Recebe os dados finais da partida.
        O PlayingState deve popular self.context antes de sinalizar a troca.
        """
        ctx = getattr(self, "context", {})
        self.seconds = ctx.get("seconds", 0)
        self.level   = ctx.get("level",   1)
        self.score   = ctx.get("score",   0)
        self.done    = False

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.done       = True
                self.next_state = "playing"

    def update(self):
        pass  # Estado estático — sem lógica de atualização

    def draw(self, screen: pygame.Surface):
        # Overlay escurece o fundo (o estado anterior já foi desenhado antes)
        screen.blit(self._overlay, (0, 0))

        title = FONT_MAIN.render("Você foi atingido por um meteoro!", True, RED)
        hint  = FONT_SUB.render("Pressione ESC para reiniciar", True, WHITE)
        stats = FONT_DETAILS.render(
            f"Tempo: {self.seconds}s   Level: {self.level}   Score: {self.score}",
            True, WHITE,
        )

        cx = WIDTH  // 2
        cy = HEIGHT // 2

        screen.blit(title, (cx - title.get_width() // 2, cy - 60))
        screen.blit(hint,  (cx - hint.get_width()  // 2, cy +  0))
        screen.blit(stats, (cx - stats.get_width() // 2, cy + 50))
