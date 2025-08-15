"""
Jogo: Pizza Raid 🍕
Autor: @ericvieira
Descrição: Jogo estilo River Raid onde o jogador pilota uma nave e atira em pizzas voadoras.
Versão: 1.1 (Tela de Game Over + Botão Recomeçar)
Data: 2025-08-15
"""

import pygame
import random

# --- Configurações iniciais ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)      # Rio azul conforme atari
GREEN = (0, 150, 0)       # Margens
RED = (200, 0, 0)         # Pepperoni
YELLOW = (255, 220, 0)    # Massa da pizza
DARK = (0, 0, 0)
OVERLAY = (0, 0, 0, 160)  # semitransparente

# Jogador
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40
PLAYER_SPEED = 7

# Pizza inimiga
PIZZA_RADIUS = 15
PIZZA_SPEED = 3
MAX_PIZZAS = 5

# Tiro
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 10

# Scroll
SCROLL_SPEED = 2


def desenhar_pizza(screen, pizza_rect):
    center = (pizza_rect.x + PIZZA_RADIUS, pizza_rect.y + PIZZA_RADIUS)
    pygame.draw.circle(screen, YELLOW, center, PIZZA_RADIUS)
    for _ in range(5):
        offset_x = random.randint(-PIZZA_RADIUS + 4, PIZZA_RADIUS - 4)
        offset_y = random.randint(-PIZZA_RADIUS + 4, PIZZA_RADIUS - 4)
        pepperoni = (center[0] + offset_x, center[1] + offset_y)
        pygame.draw.circle(screen, RED, pepperoni, 3)


def criar_pizzas():
    pizzas = []
    for _ in range(MAX_PIZZAS):
        x = random.randint(50 + PIZZA_RADIUS, SCREEN_WIDTH - 50 - PIZZA_RADIUS)
        y = random.randint(-600, -20)
        pizzas.append(pygame.Rect(x - PIZZA_RADIUS, y - PIZZA_RADIUS, PIZZA_RADIUS * 2, PIZZA_RADIUS * 2))
    return pizzas


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🍕 Pizza Raid - por @ericvieira")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    font_big = pygame.font.SysFont(None, 56)

    # --- Estados ---
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    state = PLAYING

    # Botões
    btn_w, btn_h = 200, 60
    btn_restart = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, SCREEN_HEIGHT // 2 + 20, btn_w, btn_h)

    # Variáveis do jogo
    def resetar_jogo():
        nonlocal player_x, player_y, bullets, pizzas, scroll_offset, score, state
        player_x = SCREEN_WIDTH // 2
        player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        bullets = []
        pizzas = criar_pizzas()
        scroll_offset = 0
        score = 0
        state = PLAYING

    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
    bullets = []
    pizzas = criar_pizzas()
    scroll_offset = 0
    score = 0

    running = True

    while running:
        clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Disparo apenas jogando
                if state == PLAYING and event.key == pygame.K_SPACE:
                    bullet_x = player_x - BULLET_WIDTH // 2
                    bullet_y = player_y
                    bullets.append(pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))
                # Enter para recomeçar no Game Over
                if state == GAME_OVER and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                    resetar_jogo()

            # Clique no botão Recomeçar (somente no Game Over)
            if state == GAME_OVER and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_restart.collidepoint(event.pos):
                    resetar_jogo()

        # Movimento jogador (apenas jogando)
        keys = pygame.key.get_pressed()
        if state == PLAYING:
            if keys[pygame.K_LEFT]:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player_x += PLAYER_SPEED

            left_limit = 50 + PLAYER_WIDTH // 2
            right_limit = SCREEN_WIDTH - 50 - PLAYER_WIDTH // 2
            player_x = max(left_limit, min(right_limit, player_x))

            # Atualiza pizzas
            for pizza in pizzas:
                pizza.y += PIZZA_SPEED + SCROLL_SPEED
                if pizza.y > SCREEN_HEIGHT:
                    pizza.x = random.randint(50 + PIZZA_RADIUS, SCREEN_WIDTH - 50 - PIZZA_RADIUS)
                    pizza.y = random.randint(-600, -20)

            # Atualiza tiros
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.y < 0:
                    bullets.remove(bullet)
                else:
                    for pizza in pizzas:
                        if bullet.colliderect(pizza):
                            bullets.remove(bullet)
                            pizza.x = random.randint(50 + PIZZA_RADIUS, SCREEN_WIDTH - 50 - PIZZA_RADIUS)
                            pizza.y = random.randint(-600, -20)
                            score += 10
                            break

            # Colisão jogador x pizza
            player_rect = pygame.Rect(player_x - PLAYER_WIDTH // 2, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
            for pizza in pizzas:
                if player_rect.colliderect(pizza):
                    # Entra em Game Over (sem sair do jogo)
                    state = GAME_OVER
                    break

            # Scroll visual (continua movendo linhas só em PLAYING)
            scroll_offset = (scroll_offset + SCROLL_SPEED) % 40

        # --- DESENHO ---
        screen.fill(GREEN)  # Margens
        pygame.draw.rect(screen, BLUE, (50, 0, SCREEN_WIDTH - 100, SCREEN_HEIGHT))  # Rio

        for i in range(-1, SCREEN_HEIGHT // 40 + 2):
            y = i * 40 + (scroll_offset if state == PLAYING else scroll_offset)  # mantém posição atual
            pygame.draw.line(screen, WHITE, (50, y), (SCREEN_WIDTH - 50, y), 2)

        # Nave
        p1 = (player_x, player_y)
        p2 = (player_x - PLAYER_WIDTH // 2, player_y + PLAYER_HEIGHT)
        p3 = (player_x + PLAYER_WIDTH // 2, player_y + PLAYER_HEIGHT)
        pygame.draw.polygon(screen, WHITE, [p1, p2, p3])

        # Pizzas
        for pizza in pizzas:
            desenhar_pizza(screen, pizza)

        # Tiros
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Pontuação
        text = font.render(f"Pontos: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # --- Tela Game Over ---
        if state == GAME_OVER:
            # Overlay semitransparente
            overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay_surface.fill(OVERLAY)
            screen.blit(overlay_surface, (0, 0))

            titulo = font_big.render("GAME OVER", True, WHITE)
            t_rect = titulo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(titulo, t_rect)

            pontos = font.render(f"Pontuação: {score}", True, WHITE)
            p_rect = pontos.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(pontos, p_rect)

            # Botão Recomeçar (hover simples)
            mouse_pos = pygame.mouse.get_pos()
            hovered = btn_restart.collidepoint(mouse_pos)
            pygame.draw.rect(screen, (80, 80, 80) if hovered else (60, 60, 60), btn_restart, border_radius=10)
            pygame.draw.rect(screen, WHITE, btn_restart, 2, border_radius=10)

            label = font.render("Recomeçar (Enter)", True, WHITE)
            l_rect = label.get_rect(center=btn_restart.center)
            screen.blit(label, l_rect)

        pygame.display.flip()

    pygame.quit()


# --- Execução principal ---
if __name__ == "__main__":
    main()
