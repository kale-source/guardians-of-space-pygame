from __future__ import annotations
from states.base_state import BaseState

class StateManager:
    """
    Gerencia o ciclo de vida e as transições entre estados do jogo.

    Responsabilidades:
        - Registrar estados por chave string
        - Executar os hooks on_exit / on_enter a cada transição
        - Passar contexto entre estados quando necessário
        - Expor o estado ativo via a propriedade `current`

    Uso:
        sm = StateManager()
        sm.register("playing",   PlayingState())
        sm.register("game_over", GameOverState())
        sm.change("playing")

        # No loop:
        sm.current.handle_events(events)
        sm.current.update()
        sm.current.draw(screen)

        if sm.current.done:
            sm.change(sm.current.next_state)
    """

    def __init__(self):
        self._states: dict[str, BaseState] = {}
        self._current_key: str | None = None

    # ── Registro ──────────────────────────────────────────────────────────────
    def register(self, key: str, state: BaseState):
        """Associa uma chave a uma instância de BaseState."""
        self._states[key] = state

    # ── Acesso ────────────────────────────────────────────────────────────────
    @property
    def current(self) -> BaseState | None:
        """Retorna o estado atualmente ativo."""
        return self._states.get(self._current_key)  # type: ignore[arg-type]

    # ── Transições ────────────────────────────────────────────────────────────
    def change(self, key: str):
        """
        Troca o estado ativo para `key`.

        Fluxo:
            1. Chama on_exit() no estado atual
            2. Injeta contexto no próximo estado (se houver)
            3. Chama on_enter() no novo estado
        """
        if key not in self._states:
            raise KeyError(f"Estado '{key}' não registrado no StateManager.")

        previous_key = self._current_key

        if self.current:
            self.current.on_exit()

        self._current_key = key
        next_state = self._states[key]
        next_state.done = False

        self._inject_context(previous_key, key)
        next_state.on_enter(previous_state=previous_key)

    # ── Injeção de contexto ───────────────────────────────────────────────────

    def _inject_context(self, from_key: str | None, to_key: str):
        """
        Transfere dados relevantes entre estados na transição.

        Centralizar aqui evita que os estados precisem se conhecer
        diretamente, mantendo o acoplamento baixo.
        """
        if from_key == "playing" and to_key == "game_over":
            playing   = self._states.get("playing")
            game_over = self._states.get("game_over")

            if playing and game_over:
                game_over.context = {  # type: ignore[attr-defined]
                    "seconds": getattr(playing, "seconds", 0),
                    "level":   getattr(playing, "level",   1),
                    "score":   getattr(playing, "score",   0),
                }