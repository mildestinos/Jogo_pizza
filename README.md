Ótimo 👍
Vou incluir essa imagem direto no **README.md** para que apareça no GitHub ou no seu repositório.

Segue o README atualizado com a imagem:

---

````markdown
# 🍕 Pizza Raid

Um jogo divertido em **Python** usando **Pygame**, inspirado no clássico River Raid, mas com um toque especial:  
você pilota uma nave e atira em pizzas voadoras! 🎮

---

## 🛠 Tecnologias utilizadas
- **Python** — linguagem de programação
- **Pygame** — biblioteca para criação de jogos 2D
- Criatividade e vontade de aprender

---

## 📜 Como funciona o jogo
1. **Configura o cenário** — define cores, tamanho da tela e velocidade do jogo.
2. **Desenha o jogador** — nossa nave, representada por um triângulo.
3. **Gera inimigos** — pizzas voando pela tela, cada uma com pepperonis aleatórios.
4. **Controla tiros e colisões** — se o tiro acerta a pizza, você ganha pontos.
5. **Gerencia o Game Over** — inclui botão para recomeçar sem fechar o jogo.

---

## 🧠 O que você aprende com este projeto
- Criar **formas e desenhos** no Pygame.
- Controlar **movimento do jogador** com o teclado.
- Detectar **colisões** entre objetos.
- Criar **loops de jogo** e estados (*jogando* e *game over*).
- Trabalhar com **listas** para gerenciar tiros e inimigos.

---

## 📂 Estrutura do código
- **Configurações iniciais** — dimensões da tela, cores, velocidade, tamanhos.
- **Função `desenhar_pizza()`** — desenha a pizza com pepperonis.
- **Função `criar_pizzas()`** — gera pizzas em posições aleatórias.
- **Loop principal (`while`)** — controla eventos, movimentação, colisões e renderização.
- **Estados do jogo** — `PLAYING` e `GAME_OVER` para controlar o fluxo.
- **Botão Recomeçar** — permite reiniciar sem fechar o programa.

---

## 📜 Código comentado
```python
# Exemplo de parte do código
if state == PLAYING:
    # Movimento do jogador
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED

    # Limite de movimento nas margens
    left_limit = 50 + PLAYER_WIDTH // 2
    right_limit = SCREEN_WIDTH - 50 - PLAYER_WIDTH // 2
    player_x = max(left_limit, min(right_limit, player_x))
````

Este trecho controla a movimentação do jogador e garante que ele não saia do rio.

---

## 🚀 Desafios para melhorar o jogo

* Criar **novos tipos de inimigos**.
* Adicionar **efeitos sonoros e música de fundo**.
* Criar um **ranking de pontuação**.
* Melhorar os **gráficos** da nave e das pizzas.
* Criar **power-ups** como tiro duplo ou escudo.

---

## ▶️ Como rodar

1. Certifique-se de ter o Python instalado (versão 3.8+).
2. Instale o Pygame:

   ```bash
   pip install pygame
   ```
3. Baixe o código do jogo.
4. Execute:

   ```bash
   python pizza_raid.py
   ```

---

## 📸 Imagem do jogo

![Pizza Raid](2ff92c60-6ad0-4238-a56e-96b2f3e098bb.png)

---

## 💡 Observação

Este projeto é excelente como **laboratório de aprendizado em Python**.
Você pode modificar o código e testar suas próprias ideias para aprender mais.

---

## 📩 Contribuições

Fique à vontade para enviar melhorias ou criar novas funcionalidades.
Vamos aprender Python juntos! 🚀

```

---

Se quiser, eu já posso **salvar esse README.md na pasta do seu projeto** pronto para commit no GitHub. Quer que eu já gere o arquivo?
```
