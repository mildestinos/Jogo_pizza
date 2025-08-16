"""
Jogo: Pizza Raid 🍕
Autor: @ericvieira
Descrição: River Raid-like — nave atira em pizzas voadoras, com SFX e chefão Pizzaiolo.
Versão: 2.0 (SFX + Boss + Tela de Vitória)
Data: 2025-08-16
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
YELLOW = (255, 220, 0)    # Massa da pizza que a nave atira
DARK = (0, 0, 0)
OVERLAY = (0, 0, 0, 160)  # semitransparente

# Jogador
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40
PLAYER_SPEED = 7

# Pizza inimiga
PIZZA_RADIUS = 20
PIZZA_SPEED = 3
MAX_PIZZAS = 5

# Tiro
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 10

# Scroll
SCROLL_SPEED = 2

# --- Boss (Pizzaiolo) ---
BOSS_WIDTH = 80
BOSS_HEIGHT = 100
BOSS_SPEED_X = 3
BOSS_ENTRY_Y = 60
BOSS_MAX_HP = 20
BOSS_SCORE_GATE = 150     # pontuação para chamar o chefão

# Tiro do boss
BOSS_BULLET_W = 8
BOSS_BULLET_H = 16
BOSS_BULLET_SPEED = 6
BOSS_SHOOT_COOLDOWN = 45  # frames entre disparos


def desenhar_pizza(screen, pizza_rect):
    center = (pizza_rect.x + PIZZA_RADIUS, pizza_rect.y + PIZZA_RADIUS)
    pygame.draw.circle(screen, YELLOW, center, PIZZA_RADIUS)
    for _ in range(5):
        offset_x = random.randint(-PIZZA_RADIUS + 4, PIZZA_RADIUS - 4)
        offset_y = random.randint(-PIZZA_RADIUS + 4, PIZZA_RADIUS - 4)
        pepperoni = (center[0] + offset_x, center[1] + offset_y)
        pygame.draw.circle(screen, RED, pepperoni, 3)


def desenhar_pizzaiolo(screen, rect):
    # Corpo
    pygame.draw.rect(screen, (230, 230, 230), rect, border_radius=10)
    # Avental
    avental = pygame.Rect(rect.x + 15, rect.y + 30, rect.width - 30, rect.height - 40)
    pygame.draw.rect(screen, (200, 200, 200), avental, border_radius=6)
    # Chapéu de chef
    chapeu = pygame.Rect(rect.centerx - rect.width // 3, rect.y - 15, rect.width // 1.5, 25)
    pygame.draw.rect(screen, (245, 245, 245), chapeu, border_radius=8)
    # Bigode
    pygame.draw.line(screen, (60, 60, 60), (rect.centerx - 12, rect.y + 24), (rect.centerx - 2, rect.y + 24), 3)
    pygame.draw.line(screen, (60, 60, 60), (rect.centerx + 2, rect.y + 24), (rect.centerx + 12, rect.y + 24), 3)


def desenhar_barra_hp(screen, x, y, w, h, hp, hp_max):
    pygame.draw.rect(screen, (80, 80, 80), (x, y, w, h), border_radius=4)
    ratio = max(0, min(1, hp / hp_max))
    pygame.draw.rect(screen, (200, 40, 40), (x + 2, y + 2, int((w - 4) * ratio), h - 4), border_radius=3)


def criar_pizzas():
    pizzas = []
    for _ in range(MAX_PIZZAS):
        x = random.randint(50 + PIZZA_RADIUS, SCREEN_WIDTH - 50 - PIZZA_RADIUS)
        y = random.randint(-600, -20)
        pizzas.append(pygame.Rect(x - PIZZA_RADIUS, y - PIZZA_RADIUS, PIZZA_RADIUS * 2, PIZZA_RADIUS * 2))
    return pizzas


class BossPizzaiolo:
    def __init__(self, sfx_shoot=None):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - BOSS_WIDTH // 2, -BOSS_HEIGHT, BOSS_WIDTH, BOSS_HEIGHT)
        self.hp = BOSS_MAX_HP
        self.vx = BOSS_SPEED_X
        self.cooldown = BOSS_SHOOT_COOLDOWN
        self.active = True
        self.entered = False
        self.bullets = []  # tiros do boss
        self.sfx_shoot = sfx_shoot

    def update(self):
        # Entrada vertical até posição alvo
        if not self.entered:
            self.rect.y += 2
            if self.rect.y >= BOSS_ENTRY_Y:
                self.rect.y = BOSS_ENTRY_Y
                self.entered = True
            return

        # Zig-zag horizontal
        self.rect.x += self.vx
        if self.rect.right >= SCREEN_WIDTH - 50 or self.rect.left <= 50:
            self.vx *= -1

        # Tiro
        self.cooldown -= 1
        if self.cooldown <= 0:
            bx = self.rect.centerx - BOSS_BULLET_W // 2
            by = self.rect.bottom - 10
            self.bullets.append(pygame.Rect(bx, by, BOSS_BULLET_W, BOSS_BULLET_H))
            self.cooldown = BOSS_SHOOT_COOLDOWN
            if self.sfx_shoot:
                self.sfx_shoot.play()

        # Atualiza tiros do boss
        for b in self.bullets[:]:
            b.y += BOSS_BULLET_SPEED
            if b.y > SCREEN_HEIGHT:
                self.bullets.remove(b)

    def draw(self, screen):
        desenhar_pizzaiolo(screen, self.rect)
        for b in self.bullets:
            pygame.draw.rect(screen, (255, 180, 0), b)  # “molho” do boss


def main():
    # Áudio com baixa latência (mono, 44.1kHz, buffer pequeno)
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🍕 Pizza Raid - por @ericvieira")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    font_big = pygame.font.SysFont(None, 56)

    # --- Áudio / SFX ---
    SHOOT_SFX_PATH = "assets/shoot.wav"
    HIT_SFX_PATH = "assets/pizza_pop.wav"
    BOSS_SHOOT_SFX_PATH = "assets/boss_shoot.wav"  # opcional
    BOSS_HIT_SFX_PATH = "assets/boss_hit.wav"      # opcional

    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    pygame.mixer.set_num_channels(16)

    def carregar_som(path, vol=0.7):
        try:
            s = pygame.mixer.Sound(path)
            s.set_volume(vol)
            return s
        except Exception:
            return None

    shoot_sfx = carregar_som(SHOOT_SFX_PATH, 0.75)
    hit_sfx = carregar_som(HIT_SFX_PATH, 0.8)
    boss_shoot_sfx = carregar_som(BOSS_SHOOT_SFX_PATH, 0.7)
    boss_hit_sfx = carregar_som(BOSS_HIT_SFX_PATH, 0.8)

    # --- Estados ---
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    VICTORY = "VICTORY"
    state = PLAYING

    # Botões
    btn_w, btn_h = 200, 60
    btn_restart = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, SCREEN_HEIGHT // 2 + 20, btn_w, btn_h)

    # Variáveis do jogo
    def resetar_jogo():
        nonlocal player_x, player_y, bullets, pizzas, scroll_offset, score, state
        nonlocal boss, boss_active
        player_x = SCREEN_WIDTH // 2
        player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        bullets = []
        pizzas = criar_pizzas()
        scroll_offset = 0
        score = 0
        state = PLAYING
        boss = None
        boss_active = False

    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
    bullets = []
    pizzas = criar_pizzas()
    scroll_offset = 0
    score = 0
    boss = None
    boss_active = False

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
                    if shoot_sfx:
                        shoot_sfx.play()
                # Enter para recomeçar no Game Over/Vitória
                if state in (GAME_OVER, VICTORY) and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                    resetar_jogo()

            # Clique no botão Recomeçar (somente no Game Over/Vitória)
            if state in (GAME_OVER, VICTORY) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

            # Atualiza tiros do jogador + colisões
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.y < 0:
                    bullets.remove(bullet)
                    continue

                # 1) Colisão com Boss (prioridade)
                if boss_active and boss and boss.active and bullet.colliderect(boss.rect):
                    bullets.remove(bullet)
                    boss.hp -= 1
                    if boss_hit_sfx:
                        boss_hit_sfx.play()
                    if boss.hp <= 0:
                        boss.active = False
                        score += 100  # bônus de encerramento
                        state = VICTORY
                    continue

                # 2) Colisão com pizzas
                hit_any = False
                for pizza in pizzas:
                    if bullet.colliderect(pizza):
                        bullets.remove(bullet)
                        pizza.x = random.randint(50 + PIZZA_RADIUS, SCREEN_WIDTH - 50 - PIZZA_RADIUS)
                        pizza.y = random.randint(-600, -20)
                        score += 10
                        if hit_sfx:
                            hit_sfx.play()
                        hit_any = True
                        break
                if hit_any:
                    continue

            # Colisão jogador x pizza (somente se ainda jogando)
            player_rect = pygame.Rect(player_x - PLAYER_WIDTH // 2, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
            if state == PLAYING:
                for pizza in pizzas:
                    if player_rect.colliderect(pizza):
                        state = GAME_OVER
                        break

            # Spawn do Boss quando atingir a meta
            if not boss_active and score >= BOSS_SCORE_GATE:
                boss = BossPizzaiolo(sfx_shoot=boss_shoot_sfx)
                boss_active = True

            # Atualiza Boss (movimento e tiros) e colisões do boss contra o jogador
            if boss_active and boss and boss.active and state == PLAYING:
                boss.update()

                # Colisão dos tiros do boss com o jogador
                for bb in boss.bullets[:]:
                    if player_rect.colliderect(bb):
                        state = GAME_OVER
                        break

                # Colisão direta boss x jogador
                if state == PLAYING and player_rect.colliderect(boss.rect):
                    state = GAME_OVER

            # Scroll visual (continua movendo linhas só em PLAYING)
            scroll_offset = (scroll_offset + SCROLL_SPEED) % 40

        # --- DESENHO ---
        screen.fill(GREEN)  # Margens
        pygame.draw.rect(screen, BLUE, (50, 0, SCREEN_WIDTH - 100, SCREEN_HEIGHT))  # Rio

        for i in range(-1, SCREEN_HEIGHT // 40 + 2):
            y = i * 40 + (scroll_offset if state == PLAYING else scroll_offset)
            pygame.draw.line(screen, WHITE, (50, y), (SCREEN_WIDTH - 50, y), 2)

        # Nave
        p1 = (player_x, player_y)
        p2 = (player_x - PLAYER_WIDTH // 2, player_y + PLAYER_HEIGHT)
        p3 = (player_x + PLAYER_WIDTH // 2, player_y + PLAYER_HEIGHT)
        pygame.draw.polygon(screen, WHITE, [p1, p2, p3])

        # Pizzas
        for pizza in pizzas:
            desenhar_pizza(screen, pizza)

        # Tiros do jogador
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Boss (sprite + barra de vida)
        if boss_active and boss:
            boss.draw(screen)
            if boss.active:
                desenhar_barra_hp(screen, 60, 8, SCREEN_WIDTH - 120, 16, boss.hp, BOSS_MAX_HP)

        # Pontuação
        text = font.render(f"Pontos: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # --- Tela Game Over ---
        if state == GAME_OVER:
            overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay_surface.fill(OVERLAY)
            screen.blit(overlay_surface, (0, 0))

            titulo = font_big.render("GAME OVER", True, WHITE)
            t_rect = titulo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(titulo, t_rect)

            pontos = font.render(f"Pontuação: {score}", True, WHITE)
            p_rect = pontos.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(pontos, p_rect)

            mouse_pos = pygame.mouse.get_pos()
            hovered = btn_restart.collidepoint(mouse_pos)
            pygame.draw.rect(screen, (80, 80, 80) if hovered else (60, 60, 60), btn_restart, border_radius=10)
            pygame.draw.rect(screen, WHITE, btn_restart, 2, border_radius=10)

            label = font.render("Recomeçar (Enter)", True, WHITE)
            l_rect = label.get_rect(center=btn_restart.center)
            screen.blit(label, l_rect)

        # --- Tela Vitória ---
        if state == VICTORY:
            overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay_surface.fill(OVERLAY)
            screen.blit(overlay_surface, (0, 0))

            titulo = font_big.render("VOCÊ VENCEU!", True, WHITE)
            t_rect = titulo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(titulo, t_rect)

            pontos = font.render(f"Pontuação: {score}", True, WHITE)
            p_rect = pontos.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(pontos, p_rect)

            mouse_pos = pygame.mouse.get_pos()
            hovered = btn_restart.collidepoint(mouse_pos)
            pygame.draw.rect(screen, (80, 80, 80) if hovered else (60, 60, 60), btn_restart, border_radius=10)
            pygame.draw.rect(screen, WHITE, btn_restart, 2, border_radius=10)

            label = font.render("Recomeçar (Enter)", True, WHITE)
            l_rect = label.get_rect(center=btn_restart.center)
            screen.blit(label, l_rect)

        pygame.display.flip()

    pygame.quit()


# --- Execução principal do jogo ---
if __name__ == "__main__":
    main()
