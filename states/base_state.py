from abc import ABC, abstractmethod
import pygame

class BaseState(ABC):
    """
    Contrato que todo estado do jogo deve implementar.

    O StateManager chama handle_events → update → draw a cada frame,
    garantindo que a interface seja uniforme independente do estado.
    """

    def __init__(self):
        self.next_state: str | None = None   # None = permanece no estado atual
        self.done: bool = False              # True = solicita troca de estado

    # ── Ciclo de vida (chamados pelo Game loop) ────────────────────────────────

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]):
        """Processa eventos de input."""
        ...

    @abstractmethod
    def update(self):
        """Atualiza a lógica do estado."""
        ...

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """Renderiza o estado na tela."""
        ...

    # ── Hooks opcionais ───────────────────────────────────────────────────────

    def on_enter(self, previous_state: str | None = None):
        """Chamado ao entrar no estado. Ideal para reset/inicialização."""
        pass

    def on_exit(self):
        """Chamado ao sair do estado. Ideal para limpeza de recursos."""
        pass
