import pygame

class Entity(pygame.sprite.Sprite):
    """
    Classe base para todas as entidades do jogo.

    Centraliza atributos comuns (posição, dimensões, image, rect) e herda
    de pygame.sprite.Sprite para participar dos grupos de sprites e do
    sistema de colisão nativo do Pygame.

    Subclasses devem:
        - Chamar super().__init__(x, y, width, height)
        - Sobrescrever _build_image() para desenhar sua própria Surface
        - Sobrescrever update() com a lógica de movimento/comportamento
    """
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__()

        self.width = width
        self.height = height

        # Surface transparente que será desenhada pela subclasse
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))

        # Posição em float para movimento suave (rect usa inteiros)
        self.pos_x = float(x)
        self.pos_y = float(y)

        self._build_image()

    # ── Interface pública ─────────────────────────────────────────────────────
    def update(self, *args, **kwargs):
        """Lógica de atualização. Sobrescrever nas subclasses."""
        pass

    def draw(self, screen: pygame.Surface):
        """Desenha a entidade na tela via rect sincronizado."""
        screen.blit(self.image, self.rect)

    # ── Helpers internos ──────────────────────────────────────────────────────
    def _build_image(self):
        """Constrói o visual da entidade na self.image. Sobrescrever nas subclasses."""
        pass

    def _sync_rect(self):
        """Sincroniza self.rect com a posição float (pos_x, pos_y)."""
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
