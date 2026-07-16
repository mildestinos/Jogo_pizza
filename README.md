# 🍕 Pizza Raid

Jogo 2D desenvolvido em Python com Pygame, inspirado na dinâmica dos jogos clássicos de nave. O jogador percorre o rio, enfrenta pizzas voadoras e, ao atingir 150 pontos, encara o chefão Pizzaiolo.

## Funcionalidades

- Movimento lateral com limites do cenário
- Sistema de disparos e colisões
- Pontuação e reinício da partida
- Chefão com barra de vida e disparos próprios
- Tela de vitória e de game over
- Efeitos sonoros com alternativa gerada pelo próprio jogo
- Suporte à criação de executável com PyInstaller

## Requisitos

- Python 3.8 ou superior
- Pygame 2.5 ou superior

## Instalação

```bash
python -m venv .venv
```

Ative o ambiente virtual:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux ou macOS**

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Como jogar

```bash
python pizza_raid.py
```

| Comando | Ação |
|---|---|
| Seta esquerda | Mover para a esquerda |
| Seta direita | Mover para a direita |
| Espaço | Disparar |
| Enter | Reiniciar após o fim da partida |
| Esc | Sair |

## Criar o executável

```bash
python -m pip install pyinstaller
pyinstaller pizza_raid.spec
```

O executável será criado na pasta `dist`.

## Estrutura principal

- `pizza_raid.py`: código do jogo
- `pizza_raid.spec`: configuração do PyInstaller
- `requirements.txt`: dependências do projeto

## Próximas evoluções

- Ranking local de pontuação
- Novos inimigos e níveis de dificuldade
- Testes automatizados para pontuação e colisões
- Sprites e animações personalizados
