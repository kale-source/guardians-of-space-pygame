import pygame


class Entity(pygame.sprite.Sprite):
    """
    Classe base simples para entidades do jogo:
    - Herda de pygame.sprite.Sprite para uso com grupos e colisões.
    - Gerencia posição, dimensões e renderização de sprites.
    """
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.pos_x = float(x)
        self.pos_y = float(y)
        
        # Criar surface transparente
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        
        self._build_image()

    def _build_image(self):
        """
        Constrói a imagem do sprite:
        - Subclasses fazem override para desenhar na self.image.
        """
        pass

    def _sync_rect(self):
        """
        Sincroniza o retângulo de colisão com a posição em ponto flutuante.
        """
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def draw(self, screen: pygame.Surface):
        """
        Renderiza o sprite na tela.
        """
        screen.blit(self.image, self.rect)
