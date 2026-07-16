# Pizza Raid

Jogo 2D desenvolvido em Python com Pygame. O projeto aplica conceitos de orientação a objetos, eventos, colisões, controle de estado e empacotamento de aplicações desktop.

## Sobre o jogo

O participante percorre o cenário, enfrenta pizzas voadoras e, ao atingir 150 pontos, encara o chefão Pizzaiolo.

## Funcionalidades

- Movimento lateral com limites do cenário
- Sistema de disparos e colisões
- Pontuação e reinício da partida
- Chefão com barra de vida e disparos próprios
- Telas de vitória e game over
- Efeitos sonoros com alternativa gerada pelo jogo
- Geração de executável com PyInstaller

## Tecnologias

- Python 3.8+
- Pygame 2.5+
- PyInstaller

## Instalação

```bash
git clone https://github.com/mildestinos/Jogo_pizza.git
cd Jogo_pizza
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

Instale as dependências e execute:

```bash
python -m pip install -r requirements.txt
python pizza_raid.py
```

## Controles

| Comando | Ação |
|---|---|
| Seta esquerda | Mover para a esquerda |
| Seta direita | Mover para a direita |
| Espaço | Disparar |
| Enter | Reiniciar após o encerramento |
| Esc | Sair |

## Gerar executável

```bash
python -m pip install pyinstaller
pyinstaller pizza_raid.spec
```

O executável será disponibilizado na pasta `dist`.

## Estrutura principal

- `pizza_raid.py`: código-fonte do jogo
- `pizza_raid.spec`: configuração do PyInstaller
- `requirements.txt`: dependências do projeto

## Competências demonstradas

- Programação em Python
- Desenvolvimento com loop de eventos
- Detecção de colisões
- Controle de estados do jogo
- Gestão de dependências
- Empacotamento de aplicações

## Roadmap

- Ranking local de pontuação
- Novos inimigos e níveis de dificuldade
- Testes automatizados para pontuação e colisões
- Organização dos artefatos de build fora do código-fonte
- Sprites e animações personalizados

## Autor

Desenvolvido por [Eric Vieira](https://github.com/mildestinos).
