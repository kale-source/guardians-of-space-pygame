# 🚀 Guardians of Space

> Shooter espacial desenvolvido em Python com Pygame para a disciplina de **Computação Gráfica**, demonstrando conceitos de Programação Orientada a Objetos, arquitetura modular e padrão State Machine.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Como Jogar](#-como-jogar)
- [Mecânicas](#-mecânicas)
- [Arquitetura](#-arquitetura)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Pré-requisitos e Instalação](#-pré-requisitos-e-instalação)
- [Configuração](#-configuração)
- [Extensões Possíveis](#-extensões-possíveis)

---

## 🎮 Sobre o Projeto

**Guardians of Space** é um shooter de sobrevivência com visão top-down onde o jogador pilota uma nave espacial e deve destruir ou desviar de meteoros que caem continuamente. O objetivo é sobreviver o maior tempo possível, acumulando pontos e aproveitando upgrades periódicos.

O projeto foi arquitetado com separação clara de responsabilidades, sendo escalável para adição de novos inimigos, bosses e mecânicas sem gerar código espaguete.

---

## 🕹️ Como Jogar

### Controles

| Tecla | Ação |
|---|---|
| `←` `→` `↑` `↓` ou `W` `A` `S` `D` | Mover a nave |
| `ESPAÇO` (tap) | Disparar bala normal |
| `ESPAÇO` (segurar + soltar) | Carregar e disparar tiro potencializado |
| `T` | Ligar/desligar estrelas do fundo |
| `ESPAÇO` | Reiniciar após game over |

### Sistema de Tiro Carregado

Segurar `ESPAÇO` por até **1.5 segundos** carrega o tiro progressivamente. Um arco abaixo da nave indica a carga atual, mudando de cor de **ciano → laranja**. Tiros carregados são maiores, mais danosos (até 4x) e causam mais dano a meteoros com muito HP.

### HUD (Heads-Up Display)

O canto superior esquerdo da tela exibe em tempo real:

| Indicador | Descrição |
|---|---|
| `Segundos` | Tempo total desde o início da partida |
| `Level` | Nível atual — aumenta a cada intervalo de tempo |
| `Score` | Meteoros destruídos na sessão |
| `Escaparam` | Meteoros que fugiram — ao chegar em 10, game over |
| `Próximo upgrade` | Mortes restantes até a próxima tela de upgrade |

### Condições de Derrota

- Colisão direta da nave com um meteoro
- **10 meteoros** escapando pela base da tela

A tela de game over distingue os dois casos com mensagens diferentes e exibe as estatísticas finais da partida.

---

## ⚙️ Mecânicas

### Meteoros

Os meteoros surgem do topo da tela com velocidade e HP que escalam conforme o nível atual. Eles mudam de cor ao ser atingidos e são removidos quando o HP chega a zero ou quando saem pela borda inferior.

### Progressão por Level

O nível sobe automaticamente a cada `LEVEL_UP_INTERVAL` segundos, acelerando o spawn e aumentando as estatísticas dos meteoros:

| Atributo | Fórmula |
|---|---|
| Velocidade dos meteoros | `random(1.5, 8.0) + level × 0.5` |
| HP dos meteoros | `1 + level` |
| Delay de spawn | `max(15, 60 - (level - 1) × 5)` frames |

### Sistema de Upgrades

A cada **15 meteoros destruídos** (`UPGRADE_EVERY_N_KILLS`), o jogo pausa e apresenta três opções de melhoria permanente para a nave:

| Opção | Efeito |
|---|---|
| `[1]` Velocidade da Nave | +`UPGRADE_SPEED_BONUS` de velocidade de movimento |
| `[2]` Potência dos Tiros | +`UPGRADE_DAMAGE_BONUS` de dano base por bala |
| `[3]` Recarga | Redução de `UPGRADE_COOLDOWN_BONUS` no cooldown entre disparos |

Os upgrades são permanentes e acumulativos durante a partida — não há limite de vezes. Use `[1]`, `[2]` ou `[3]` para escolher e voltar imediatamente ao jogo.

### Colisões

- **Balas vs. meteoros**: usa `collide_mask` para detecção pixel-perfect. Meteoros perdem HP e somem quando chegam a zero; score e total de kills são atualizados.
- **Player vs. meteoros**: qualquer contato resulta em game over imediato.

---

## 🏗️ Arquitetura

O projeto segue o padrão **State Machine** combinado com uma hierarquia de entidades baseada em herança, integrada ao sistema de sprites do Pygame.

### Estados do Jogo

```
         ┌─────────────┐
    ┌───▶│ PlayingState │◀──────────────┐
    │    └──────┬───────┘               │
    │           │ 10 escaparam          │ ESPAÇO
    │           │ ou colisão            │
    │           ▼                       │
    │    ┌─────────────┐              (reinicia)
    │    │GameOverState│
    │    └─────────────┘
    │
    │    ┌──────────────┐
    └────│ UpgradeState │  (a cada 15 kills)
         └──────────────┘
```

### Hierarquia de Entidades

```
pygame.sprite.Sprite
        │
      Entity          ← pos_x/y (float), image, rect, mask
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
  └── pygame.display.flip()
```

---

## 📁 Estrutura de Pastas

```
guardians-of-space-pygame/
│
├── main.py                  # Ponto de entrada
├── settings.py              # Todas as constantes e configurações
├── .env                     # Variáveis de ambiente (opcional)
│
├── core/
│   ├── entity.py            # Classe base Entity(pygame.sprite.Sprite)
│   ├── state_manager.py     # Gerencia transições entre estados
│   └── game.py              # Loop principal + inicialização
│
├── states/
│   ├── base_state.py        # Contrato abstrato (ABC)
│   ├── playing_state.py     # Lógica do jogo em execução
│   ├── game_over_state.py   # Tela de fim de jogo
│   └── upgrade_state.py     # Menu de seleção de upgrade
│
├── components/
│   ├── player.py            # Nave do jogador
│   ├── bullet.py            # Projétil com sistema de carga
│   ├── meteor.py            # Meteoro com HP e feedback visual
│   └── stars.py             # Campo de estrelas com efeito parallax
```

---

## 📦 Pré-requisitos e Instalação

**Requisitos:**
- Python 3.12 ou superior
- pip

**Passos:**

```bash
# 1. Clone o repositório
git clone https://github.com/kale-source/guardians-of-space-pygame.git
cd guardians-of-space-pygame

# 2. Crie e ative um ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install pygame python-dotenv pydantic pydantic-settings

# 4. Execute o jogo
python main.py
```

---

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto para personalizar a resolução da janela:

```env
WIDTH=800
HEIGHT=600
```

Se o arquivo não existir, os valores padrão (`800x600`) são usados automaticamente. Todos os demais parâmetros de gameplay (velocidade, dificuldade, upgrades etc.) podem ser ajustados diretamente em `settings.py`.

O projeto utiliza **Pydantic Settings** para gerenciamento robusto de configurações com validação de tipos e uma única fonte da verdade para todas as constantes do jogo.

---

## 🔧 Extensões Possíveis

- Adicionar sons e efeitos visuais de explosão
- Implementar diferentes tipos de meteoros ou inimigos
- Adicionar um boss ao final de cada ciclo de levels
- Salvar highscore em arquivo local
- Ajustar balanceamento dos parâmetros via `settings.py`

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.12+ | Linguagem principal |
| Pygame | 2.6+ | Engine gráfica e de input |
| Pydantic | 2.0+ | Validação de configurações |
| Pydantic Settings | 2.0+ | Gerenciamento de settings com type checking |