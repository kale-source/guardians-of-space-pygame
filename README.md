# 🚀 Guardians of Space

> Shooter espacial desenvolvido em Python com Pygame para a disciplina de **Computação Gráfica**, demonstrando domínio de Engenharia de Software, Programação Orientada a Objetos e princípios de arquitetura limpa.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Gameplay](#-gameplay)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Jogar](#-como-jogar)
- [Arquitetura](#-arquitetura)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Cálculos e Coordenadas Espaciais](#-cálculos-e-coordenadas-espaciais)
- [Por Que as Estrelas Não Interferem](#-por-que-as-estrelas-não-interferem)
- [Princípios Aplicados](#-princípios-aplicados)
- [Progressão e Mecânicas](#-progressão-e-mecânicas)

---

## 🎮 Sobre o Projeto

Guardians of Space é um shooter de sobrevivência com visão top-down onde o jogador pilota uma nave espacial e deve destruir ou desviar de meteoros que caem continuamente. O jogo foi **refatorado de uma arquitetura monolítica** para um sistema modular com separação clara de responsabilidades, escalável para adição de novos inimigos, bosses e mecânicas sem gerar código espaguete.

---

## 🕹️ Gameplay

- Desvie e destrua meteoros que caem do topo da tela
- O jogo termina se você **for atingido** por um meteoro ou se **10 meteoros escaparem**
- A cada 20 segundos o level sobe, aumentando velocidade e frequência dos meteoros
- A cada 20 meteoros destruídos, escolha um **upgrade** para sua nave
- Sobreviva o maior tempo possível e maximize seu score

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.12+ | Linguagem principal |
| Pygame | 2.6+ | Engine gráfica e de input |
| Pydantic | 2.0+ | Validação de configurações |
| Pydantic Settings | 2.0+ | Gerenciamento de settings com type checking |

---

## 📦 Pré-requisitos

- Python 3.12 ou superior
- pip

---

## 🚀 Instalação

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/guardian-of-space-pygame.git
cd guardian-of-space-pygame
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install pygame python-dotenv pydantic pydantic-settings
```

**4. Execute o jogo**
```bash
python main.py
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto para personalizar a resolução:

```env
WIDTH=800
HEIGHT=600
```

Se o arquivo não existir, os valores padrão (`800x600`) são usados automaticamente.

---

## 🎮 Como Jogar

| Controle | Ação |
|---|---|
| **Setas** ou **WASD** | Mover nave |
| **ESPAÇO** | Segurar para carregar disparo / Soltar para atirar |
| **S** | Toggle das estrelas (debug) |

**Dicas:**
- Mantenha a nave centralizada para maior mobilidade
- Carregue o disparo para aumentar dano (até 4x) e tamanho da bala
- Escolha upgrades estratégicos: velocidade para desviar, dano para destruir, cooldown para atirar mais rápido

---

## 🏗️ Arquitetura

O projeto segue uma **arquitetura modular em camadas** com total separação de responsabilidades:

### Fluxo de Dados

```
settings.py (Configuração)
    ↓
main.py (Entry point)
    ↓
core/game.py (Game Loop & State Machine)
    ├→ components/ (Entidades do jogo)
    │   ├→ player.py
    │   ├→ meteor.py
    │   ├→ bullet.py
    │   └→ stars.py
    └→ core/entity.py (Base class)
```

### Camadas Principais

#### 1️⃣ **Camada de Configuração** (`settings.py`)
- **Responsabilidade:** Gerenciar todas as constantes e parâmetros do jogo
- **Tecn:** Pydantic + Pydantic Settings para validação e type checking
- **Benefício:** Alterações fáceis sem mexer no código; suporte a `.env`

```python
WIDTH: int = 800
HEIGHT: int = 600
PLAYER_SPEED: int = 6
```

#### 2️⃣ **Camada de Entidades** (`core/entity.py`)
- **Responsabilidade:** Base genérica para todos os objetos do jogo
- **Herança:** `pygame.sprite.Sprite`
- **Funcionalidades:**
  - Gerenciamento de posição (`pos_x`, `pos_y`) em **float**
  - Sincronização automática com `rect` (int) para renderização
  - Suporte a máscaras de colisão per-pixel
  - Método `_build_image()` para subclasses customizarem o visual

```python
class Entity(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: int, height: int):
        self.pos_x = float(x)  # Precisão em float
        self.pos_y = float(y)
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
```

#### 3️⃣ **Camada de Componentes** (`components/`)
Cada entidade do jogo herda de `Entity` e implementa sua própria lógica:

**Player** (`player.py`)
- Movimento com limites de tela
- Sistema de carga de disparo
- Aplicação de upgrades (velocidade, dano, cooldown)

**Meteor** (`meteor.py`)
- Movimento vertical descendente
- Sistema de HP (danificável)
- Mudança dinâmica de cor baseado em dano
- Máscara de colisão por pixel usando `pygame.mask`

**Bullet** (`bullet.py`)
- Movimento vertical ascendente
- Tamanho e dano escaláveis por carga
- Cor interpolada (lerp) entre dois estados

**StarField** (`stars.py`)
- Campo de fundo com 100+ estrelas
- Efeito de parallax (velocidades variadas)
- Piscada dinâmica (não interfere em colisões)

#### 4️⃣ **Camada de Lógica** (`core/game.py`)
- **State Machine:** "playing", "game_over", "upgrade"
- **Physics:** Atualização de posições a cada frame
- **Colisões:** Detecção per-pixel com `pygame.sprite.collide_mask`
- **Event Loop:** Entrada do usuário e saída gráfica

---

## 📁 Estrutura de Pastas

```
guardians-of-space-pygame/
├── main.py                    # Entry point do jogo
├── settings.py                # Configurações centralizadas
├── README.md                  # Este arquivo
├── .env.example              # Template de variáveis de ambiente
├── .gitignore
├── core/
│   ├── __init__.py
│   ├── entity.py             # Base class para todas as entidades
│   └── game.py               # Game loop e state machine
└── components/
    ├── __init__.py
    ├── player.py             # Nave do jogador
    ├── meteor.py             # Inimigos que caem
    ├── bullet.py             # Projéteis
    └── stars.py              # Background de estrelas
```

---

## 🧮 Cálculos e Coordenadas Espaciais

### Por Que Precisamos de Cálculos no Espaço?

No Pygame (e em qualquer engine gráfica), o sistema de coordenadas é **cartesiano**, mas com uma peculiaridade: **Y cresce para baixo** (não como em matemática pura). Isso exige cálculos específicos para movimento correto.

#### Sistema de Coordenadas Pygame

```
(0,0) ──────────────→ X (aumenta para direita)
  │
  │
  ↓ Y (aumenta para BAIXO)
  │
  │
(800, 600)
```

**Diferença Crítica:**
- **Matemática Pura:** Y aumenta para cima
- **Pygame:** Y aumenta para baixo
- **Consequência:** Lógica de movimento deve considerar isso explicitamente

### 1️⃣ Movimento Linear com Velocidade Escalar

Qualquer movimento consiste em três componentes:

**Equação Geral:**
$$\text{nova\_posição} = \text{posição\_atual} + \text{velocidade} \times \Delta t$$

**No Pygame (discretizado por frame):**
$$\text{nova\_posição} = \text{posição\_atual} + \text{velocidade}$$

#### Exemplo: Player se movendo para cima

```python
if keys[pygame.K_UP]:
    self.pos_y -= self.speed  # DECREMENTAR Y para ir "para cima"
```

Por quê? Porque em Pygame, Y=0 está no topo. Para mover visualmente "para cima", devemos **reduzir** Y.

#### Exemplo: Meteoro caindo

```python
def update(self):
    self.pos_y += self.speed  # INCREMENTAR Y para cair
```

Como Y aumenta para baixo, incrementar a posição faz o meteoro cair naturalmente.

#### Exemplo: Bala subindo

```python
def update(self):
    self.pos_y -= self.speed  # DECREMENTAR Y para subir
```

### 2️⃣ Movimento em Qualquer Direção: Componentes X e Y

Para movimento em qualquer ângulo, decompomos em componentes:

**Vetor de Movimento:**
$$\vec{v} = (v_x, v_y)$$

**Aplicação por Frame:**
```python
self.pos_x += velocity_x
self.pos_y += velocity_y
```

#### Exemplo Real: Meteoro em Queda Oblíqua

Se quiséssemos um meteoro que cai e se move horizontalmente:

```python
# Cai + move levemente para esquerda
self.pos_y += self.speed_y  # Cai
self.pos_x -= self.drift_x  # Move esquerda
```

### 3️⃣ Sincronização Float → Int

No Pygame, **posições precisam ser inteiras** para renderização (pixels), mas internamente usamos **floats** para precisão matemática:

```python
class Entity:
    def __init__(self, x: float, y: float, ...):
        self.pos_x = float(x)        # Precisão em float
        self.pos_y = float(y)
        self.rect = pygame.Rect(...)  # Inteiro para renderização

    def _sync_rect(self):
        """Sincroniza posição float com rect inteiro"""
        self.rect.x = int(self.pos_x)  # Converte float → int
        self.rect.y = int(self.pos_y)
```

**Por que?**
- Movimento em float mantém suavidade mesmo com velocidades < 1 pixel/frame
- Renderizar sem float causaria "saltos" visuais
- Exemplo: velocidade = 0.5 pixels/frame
  - Frame 1: pos_x = 0.5 (render em x=0)
  - Frame 2: pos_x = 1.0 (render em x=1)
  - **Sem float:** alternar entre 0 e 1 sem transição suave

### 4️⃣ Limites de Tela: Clamping

Para impedir que a nave saia da tela, usamos **clamping** (limitação):

$$\text{pos} = \max(0, \min(\text{pos}, \text{max\_pos}))$$

**Código:**
```python
# Limitar bounding box
self.pos_x = max(0.0, min(self.pos_x, settings.WIDTH - self.width))
self.pos_y = max(0.0, min(self.pos_y, settings.HEIGHT - self.height))
self._sync_rect()
```

**Lógica:**
1. `max(0.0, pos_x)` → Garante que não saia pela esquerda
2. `min(pos_x, WIDTH - width)` → Garante que não saia pela direita
3. Mesma lógica para Y (cima/baixo)

### 5️⃣ Detecção de Colisão com Coordenadas

Colisões usam **máscaras per-pixel**, que são construídas a partir da surface renderizada:

```python
# Em Meteor
self.mask = pygame.mask.from_surface(self.image)

# Em Game Loop
hits = pygame.sprite.groupcollide(
    bullet_group, meteor_group,
    True, False,
    pygame.sprite.collide_mask  # ← Usar máscara, não rect
)
```

**Vantagem:** Colisão precisa, não só por caixa limitante, mas pelos **pixels reais** da imagem.

---

## ⭐ Por Que as Estrelas Não Interferem

Esta é uma questão de **separação de responsabilidades e arquitetura de colisão**.

### O Problema

Você poderia pensar: "Se desenhamos 100+ estrelas na tela, por que não colidem com a nave?"

### A Resposta

#### 1️⃣ **Não São Sprites no Sentido de Pygame**

```python
# StarField usa objetos simples, NÃO pygame.sprite.Sprite
class Star:
    def __init__(self):
        self.x = ...
        self.y = ...
        # SEM herança de pygame.sprite.Sprite!
    
    def draw(self, screen):
        pygame.draw.circle(screen, color, (self.x, int(self.y)), size)
```

**Consequência:** Não fazem parte de nenhum `pygame.sprite.Group`, portanto não participam de `groupcollide()`.

```python
# Colisão APENAS entre grupos sprite explícitos
hits = pygame.sprite.groupcollide(
    bullet_group,      # ← Sprites
    meteor_group,      # ← Sprites
    True, False,
    pygame.sprite.collide_mask
)
```

#### 2️⃣ **São Apenas Visuais do Background**

As estrelas desempenham papel narrativo/visual:
- ✅ Criar atmosfera de espaço
- ✅ Efeito de parallax (profundidade)
- ❌ Interagir com física do jogo

**Design Decision:** Mantê-las fora do loop de colisão melhora performance e clareza.

#### 3️⃣ **Toggle para Debug**

Existe um hotkey para ligar/desligar as estrelas:

```python
# Em game.py._update_playing()
for event in events:
    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        self.star_field.toggle()
```

Isso prova que são visuais <u>decorativos</u>, não mecânica de jogo.

### Analogia Visual

Imagine um jogo de carro top-down:
- **Marcações da estrada** = Visuais (sem colisão)
- **Outros carros** = Sprites com colisão
- **Fundo estrelado** = Visuais (sem colisão)

No Guardians of Space:
- **Estrelas** = Marcações da estrada (visuais)
- **Nave, meteoros, balas** = Entidades com colisão

---

## 🎯 Princípios Aplicados

### SOLID

| Princípio | Aplicação | Benefício |
|---|---|---|
| **S** - Single Responsibility | Cada classe `Entity` tem um propósito único | Fácil manutenção |
| **O** - Open/Closed | Aberto para extensão (herança), fechado para modificação | Adicionar novos inimigos sem mexer na base |
| **L** - Liskov Substitution | Qualquer `Entity` pode substituir outra | Polimorfismo natural |
| **I** - Interface Segregation | `_build_image()`, `update()` bem definidos | Contrato claro |
| **D** - Dependency Inversion | Dependências injetadas (`settings`) | Baixo acoplamento |

### DRY (Don't Repeat Yourself)

- **Entity:** Base única para todas as entidades
- **Settings:** Constantes centralizadas
- **Métodos auxiliares:** `_sync_rect()`, `_lerp_color()` reutilizáveis

### Clean Code

- Nomes descritivos: `escaped_meteors`, `charge_ratio`, `_build_image()`
- Métodos pequenos e focados
- Comentários explicam **por quê**, não **o quê**
- Uso de type hints

---

## 📈 Progressão e Mecânicas

### Sistema de Levels

A cada 20 segundos:
- Aumenta velocidade dos meteoros
- Aumenta frequência de spawn

```python
current_delay = max(
    settings.METEOR_SPAWN_DELAY_MIN,
    settings.METEOR_SPAWN_DELAY - (level - 1) * settings.METEOR_SPAWN_DELAY_SCALE
)
```

### Sistema de Score

- **+1 ponto** por meteoro destruído
- **-10 vidas** se 10 meteoros escaparem
- **Teto:** Quando atingir X kills, escolhe upgrade

### Upgrades Disponíveis

1. **Velocidade** (+6 pixels/frame)
2. **Dano** (+1 ao máximo de dano)
3. **Cooldown** (-1 ao delay entre tiros)

### Dificuldade Progressiva

```
Tempo →
  0-20s:  Easy     (meteoros lentos, poucos)
 20-40s:  Medium   (velocidade +50%, spawn -50%)
 40-60s:  Hard     (velocidade +100%, spawn -75%)
 60+s:    Extreme  (máxima velocidade, spawn mínimo)
```

---

## 🔧 Extensibilidade

O projeto foi arquitetado para expansão fácil:

### Adicionar Novo Inimigo

```python
# components/alien.py
class Alien(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30)
        self.health = 5
    
    def _build_image(self):
        # Draw seu visual
        pass
    
    def update(self):
        # Sua lógica de movimento
        pass
```

Pronto! Adicione ao `game.py`:
```python
alien_group = pygame.sprite.Group()
hits = pygame.sprite.groupcollide(bullet_group, alien_group, ...)
```

### Adicionar Nova Mecânica

Simplesmente estenda `settings.py` e a lógica em `game.py`. Nada quebra a base.

---

## 📝 Conclusão

Guardians of Space demonstra **engenharia de software prática**: separação de responsabilidades, cálculos precisos de física 2D, e arquitetura escalável. É tanto um jogo funcional quanto um **portfolio de boas práticas**.

**Próximas melhorias potenciais:**
- [ ] Sistema de soundscape
- [ ] Partículas e efeitos visuais
- [ ] Mais tipos de inimigos
- [ ] Boss fights
- [ ] Leaderboard persistente
- [ ] Modo multiplayer
