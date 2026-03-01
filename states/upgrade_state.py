import pygame
from states.base_state import BaseState
from settings import (
    WIDTH, HEIGHT,
    FONT_MAIN, FONT_DETAILS,
    UPGRADE_SPEED_BONUS, UPGRADE_DAMAGE_BONUS,
    WHITE, BLACK,
)

# Cores locais
GOLD    = (255, 200,  50)
CYAN    = (  0, 200, 255)
ORANGE  = (255, 160,   0)
DIM     = (160, 160, 160)
OVERLAY = (  0,   0,   0)


class UpgradeState(BaseState):
    """
    Tela de seleção de upgrade exibida a cada N meteoros destruídos.

    Opções:
        [1]  Velocidade da nave  +UPGRADE_SPEED_BONUS
        [2]  Potência dos tiros  +UPGRADE_DAMAGE_BONUS de dano base

    O jogador seleciona com 1/2 ou navegando com setas e confirmando com ENTER.
    A escolha é armazenada em self.choice e lida pelo StateManager ao retornar
    para o PlayingState.

    Transições:
        → "playing"  após confirmar uma opção
    """

    def __init__(self) -> None:
        super().__init__()
        self.choice: str | None = None
        self._selected = 0          # índice da opção destacada (0 ou 1)

        self._overlay = pygame.Surface((WIDTH, HEIGHT))
        self._overlay.set_alpha(200)
        self._overlay.fill(BLACK)

        self._options = [
            {
                "key":    "speed",
                "label":  "Velocidade da Nave",
                "desc":   f"+ {UPGRADE_SPEED_BONUS} de velocidade",
                "color":  CYAN,
                "hotkey": "1",
            },
            {
                "key":    "damage",
                "label":  "Potência dos Tiros",
                "desc":   f"+ {UPGRADE_DAMAGE_BONUS} de dano base",
                "color":  ORANGE,
                "hotkey": "2",
            },
        ]

    # ── BaseState interface ───────────────────────────────────────────────────

    def on_enter(self, previous_state: str | None = None) -> None:
        self._selected = 0
        self.choice    = None
        self.done      = False

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_1:
                self._confirm(0)
            elif event.key == pygame.K_2:
                self._confirm(1)
            elif event.key in (pygame.K_LEFT, pygame.K_UP):
                self._selected = (self._selected - 1) % len(self._options)
            elif event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                self._selected = (self._selected + 1) % len(self._options)
            elif event.key == pygame.K_RETURN:
                self._confirm(self._selected)

    def update(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._overlay, (0, 0))

        # Título
        title = FONT_MAIN.render("UPGRADE DISPONÍVEL!", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        hint = FONT_DETAILS.render(
            "Use [1] / [2]  ou  ← → para navegar e ENTER para confirmar",
            True, DIM,
        )
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 140))

        # Cards das opções
        card_w = 220
        card_h = 130
        gap    = 40
        total  = len(self._options) * card_w + (len(self._options) - 1) * gap
        start_x = WIDTH // 2 - total // 2
        card_y  = HEIGHT // 2 - card_h // 2

        for i, opt in enumerate(self._options):
            card_x   = start_x + i * (card_w + gap)
            selected = (i == self._selected)

            # Fundo do card
            border_color = opt["color"] if selected else DIM
            border_width = 3 if selected else 1
            pygame.draw.rect(screen, (20, 20, 30), (card_x, card_y, card_w, card_h), border_radius=10)
            pygame.draw.rect(screen, border_color, (card_x, card_y, card_w, card_h), border_width, border_radius=10)

            # Hotkey
            hotkey_surf = FONT_MAIN.render(f"[{opt['hotkey']}]", True, opt["color"])
            screen.blit(hotkey_surf, (
                card_x + card_w // 2 - hotkey_surf.get_width() // 2,
                card_y + 12,
            ))

            # Label
            label_color = WHITE if selected else DIM
            label_surf  = FONT_DETAILS.render(opt["label"], True, label_color)
            screen.blit(label_surf, (
                card_x + card_w // 2 - label_surf.get_width() // 2,
                card_y + 60,
            ))

            # Descrição do bônus
            desc_surf = FONT_DETAILS.render(opt["desc"], True, opt["color"])
            screen.blit(desc_surf, (
                card_x + card_w // 2 - desc_surf.get_width() // 2,
                card_y + 90,
            ))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _confirm(self, index: int) -> None:
        self.choice     = self._options[index]["key"]
        self.done       = True
        self.next_state = "playing"