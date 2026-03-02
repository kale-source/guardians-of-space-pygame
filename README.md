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

### Sistema de Configurações

O projeto utiliza **Pydantic Settings** para gerenciamento robusto de configurações:

- ✅ **Validação de tipos**: Todas as configurações são tipadas e validadas
- ✅ **Carregamento de `.env`**: Variáveis podem ser sobrescritas por arquivo `.env`
- ✅ **Defaults seguros**: Valores padrão bem definidos para cada configuração
- ✅ **Uma única fonte da verdade**: Toda configuração vem da classe `Settings`

**Como usar:**

```python
from settings import settings

# Acessar valores de configuração
screen_width = settings.WIDTH
player_speed = settings.PLAYER_SPEED
font = settings.FONT_MAIN
```

---

## 🎯 Como Jogar

| Tecla | Ação |
|---|---|
| `←` `→` `↑` `↓` | Mover a nave |
| `ESPAÇO` (tap) | Disparar bala normal |
| `ESPAÇO` (segurar) | Carregar tiro — solte para disparar |
| `S` | Ligar/desligar estrelas do fundo |
| `ESC` | Reiniciar após game over |

### Sistema de Tiro Carregado

Segurar `ESPAÇO` por até **1.5 segundos** carrega o tiro progressivamente. Um arco abaixo da nave indica a carga atual, mudando de cor de **ciano → laranja**. Tiros carregados são maiores, mais danosos (até 4x) e causam mais dano a meteoros com muito HP.

### Menu de Upgrade

A cada **20 meteoros destruídos** o jogo pausa e exibe duas opções:

| Opção | Efeito |
|---|---|
| `[1]` Velocidade da Nave | +2 de velocidade de movimento |
| `[2]` Potência dos Tiros | +1 de dano base em todos os disparos |

Use `[1]` / `[2]`, as setas `←` `→` e `ENTER` para navegar e confirmar.

---

## 🏗️ Arquitetura

O projeto segue o padrão **State Machine** combinado com uma hierarquia de entidades baseada em herança, totalmente integrada ao sistema de sprites do Pygame.

### Diagrama de Estados

```
         ┌─────────────┐
    ┌───▶│  PlayingState│◀────────────┐
    │    └──────┬───────┘             │
    │           │ 10 escaped          │ ESC
    │           │ ou colisão          │
    │           ▼                     │
    │    ┌─────────────┐    escolha   │
    │    │GameOverState│──────────────┘  (não acontece)
    │    └─────────────┘
    │
    │    ┌─────────────┐
    └────│UpgradeState │  (a cada 20 kills)
         └─────────────┘
```

### Hierarquia de Entidades

```
pygame.sprite.Sprite
        │
      Entity                 ← pos_x/y (float), image, rect, mask
        │
   ┌────┼────┐
Player Bullet Meteor
```

### Fluxo por Frame

```
Game.run()
  ├── clock.tick(60)
  ├── pygame.event.get()
  ├── state.handle_events(events)
  ├── state.update()
  │     └── [PlayingState]
  │           ├── _tick_timer()
  │           ├── _check_level_up()
  │           ├── _handle_player()
  │           ├── _spawn_meteors()
  │           ├── _update_meteors()
  │           ├── _update_bullets()
  │           ├── _check_bullet_meteor_collisions()
  │           └── _check_player_meteor_collision()
  ├── state.draw(screen)
  ├── pygame.display.flip()
  └── StateManager.change() se state.done
```

---

## 📁 Estrutura de Pastas

```
guardian-of-space-pygame/
│
├── main.py                        # Ponto de entrada
├── settings.py                    # Todas as constantes e configurações
├── .env                           # Variáveis de ambiente (opcional)
│
├── core/
│   ├── entity.py                  # Classe base Entity(pygame.sprite.Sprite)
│   ├── state_manager.py           # Gerencia transições entre estados
│   └── game.py                    # Loop principal + inicialização
│
├── states/
│   ├── base_state.py              # Contrato abstrato (ABC)
│   ├── playing_state.py           # Lógica do jogo em execução
│   ├── game_over_state.py         # Tela de fim de jogo
│   └── upgrade_state.py           # Menu de seleção de upgrade
│
├── entities/
│   ├── player.py                  # Nave do jogador
│   ├── bullet.py                  # Projétil com sistema de carga
│   └── meteor.py                  # Meteoro com HP e feedback visual
│
└── components/
    └── stars.py                   # Campo de estrelas com efeito parallax
```

---

## 🧱 Princípios Aplicados

### Separação de Preocupações
Cada arquivo tem uma única responsabilidade. Renderização, física, input e estados de jogo estão completamente isolados.

### Herança e Polimorfismo
`Entity` provê a base comum — `pos_x/y`, `image`, `rect` e integração com o sistema de sprites do Pygame. Subclasses (`Player`, `Bullet`, `Meteor`) sobrescrevem apenas `_build_image()` e `update()`.

### Máquina de Estados (State Pattern)
`BaseState` define o contrato com `handle_events → update → draw`. O `StateManager` coordena as transições e injeta contexto entre estados via `_inject_context()`, mantendo acoplamento zero entre eles.

### Centralização de Dados
Todo valor configurável vive em `settings.py`. Alterar dificuldade, velocidade, ou frequência de upgrades nunca exige tocar nas classes.

### Colisão Pixel-Perfect
Substituição do cálculo manual com `math.sqrt` por `pygame.sprite.collide_mask`, usando máscaras de bits geradas a partir das Surfaces das entidades.

### Timer Confiável
Substituição da contagem frágil de frames por `pygame.time.get_ticks()`, independente de variações de FPS.

---

## 📈 Progressão e Mecânicas

### Escalonamento por Level
| Atributo | Fórmula |
|---|---|
| Velocidade dos meteoros | `random(1.5, 8.0) + level × 0.5` |
| HP dos meteoros | `1 + level` |
| Delay de spawn | `max(15, 60 - (level - 1) × 5)` frames |

### Upgrades Acumulativos
Os upgrades são permanentes durante a partida e acumulam a cada 20 kills. Não há limite de vezes — um jogador habilidoso pode acumular múltiplos upgrades de dano e velocidade ao longo de uma partida longa.

### Condições de Derrota
- Colisão direta com um meteoro
- 10 meteoros escapando pela base da tela

A tela de game over distingue os dois casos com mensagens diferentes.