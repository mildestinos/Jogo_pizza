"""
Jogo: Pizza Raid 🍕
Autor: @ericvieira
Descrição: Jogo estilo River Raid onde o jogador pilota uma nave e atira em pizzas voadoras.
Versão: 1.0
Data: 2025-08-14
"""

import pygame
import random

# --- Configurações iniciais ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)      # Rio
GREEN = (0, 150, 0)       # Margens
RED = (200, 0, 0)         # Pepperoni
YELLOW = (255, 220, 0)    # Massa da pizza

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
                if event.key == pygame.K_SPACE:
                    bullet_x = player_x - BULLET_WIDTH // 2
                    bullet_y = player_y
                    bullets.append(pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Movimento jogador
        keys = pygame.key.get_pressed()
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
                print(f"Você perdeu! Pontuação final: {score}")
                running = False

        # Scroll visual
        scroll_offset = (scroll_offset + SCROLL_SPEED) % 40

        # --- DESENHO ---
        screen.fill(GREEN)  # Margens
        pygame.draw.rect(screen, BLUE, (50, 0, SCREEN_WIDTH - 100, SCREEN_HEIGHT))  # Rio

        for i in range(-1, SCREEN_HEIGHT // 40 + 2):
            y = i * 40 + scroll_offset
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

        pygame.display.flip()

    pygame.quit()


# --- Execução principal ---
if __name__ == "__main__":
    main()
  