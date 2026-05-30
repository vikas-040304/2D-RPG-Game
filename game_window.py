import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jujutsu Sorcerer RPG - 2D Edition")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

if not os.path.exists("assets"):
    os.makedirs("assets")

def load_image(path, size, fallback_color=None):
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            return fallback_color
    return fallback_color

def load_sound(path):
    if os.path.exists(path):
        try:
            return pygame.mixer.Sound(path)
        except:
            return None
    return None

player_sprite = load_image("assets/player.png", (50, 50), (220, 20, 60))
enemy_sprite = load_image("assets/enemy.png", (50, 50), (50, 200, 50))
boss_sprite = load_image("assets/boss.png", (100, 100), (128, 0, 128))
bg_sprite = load_image("assets/background.png", (800, 600), (10, 10, 15))
domain_sprite = load_image("assets/domain.png", (800, 600), (80, 0, 0))
shoot_sound = load_sound("assets/shoot.wav")
hit_sound = load_sound("assets/hit.wav")

def main():
    game_state = "START" 
    
    player_x, player_y = 100, 450
    player_hp = 100
    player_velocity_y = 0
    is_jumping = False
    GRAVITY = 1
    
    enemy_x, enemy_y = 800, 450
    projectiles = []
    score = 0
    
    boss_active = False
    boss_hp = 100
    
    bg_x1, bg_x2 = 0, 800
    
    domain_active = False
    domain_timer = 0

    def reset_game():
        nonlocal player_x, player_y, player_hp, player_velocity_y, is_jumping, enemy_x, enemy_y, projectiles, score, boss_active, boss_hp, bg_x1, bg_x2, domain_active, domain_timer
        player_x, player_y = 100, 450
        player_hp = 100
        player_velocity_y = 0
        is_jumping = False
        enemy_x, enemy_y = 800, 450
        projectiles = []
        score = 0
        boss_active = False
        boss_hp = 100
        bg_x1, bg_x2 = 0, 800
        domain_active = False
        domain_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state in ["START", "GAME_OVER", "WIN"]:
                    if event.key == pygame.K_RETURN:
                        reset_game()
                        game_state = "PLAYING"
                elif game_state == "PLAYING":
                    if event.key == pygame.K_SPACE and player_hp > 0:
                        projectiles.append([player_x + 50, int(player_y + 25)])
                        if shoot_sound:
                            shoot_sound.play()
                    if event.key == pygame.K_UP and not is_jumping:
                        player_velocity_y = -15
                        is_jumping = True
                    if event.key == pygame.K_d and not domain_active and score >= 50:
                        domain_active = True
                        domain_timer = 180 
                        score -= 50

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: player_x -= 5
            if keys[pygame.K_RIGHT]: player_x += 5

            if is_jumping:
                player_y += player_velocity_y
                player_velocity_y += GRAVITY
                if player_y >= 450:
                    player_y = 450
                    is_jumping = False
                    player_velocity_y = 0

            bg_x1 -= 2
            bg_x2 -= 2
            if bg_x1 <= -800: bg_x1 = 800
            if bg_x2 <= -800: bg_x2 = 800

            if score >= 100 and not boss_active and boss_hp > 0:
                boss_active = True
                enemy_x = 800
                enemy_y = 400

            if boss_active:
                enemy_x -= 2
                enemy_rect = pygame.Rect(enemy_x, enemy_y, 100, 100)
            else:
                enemy_x -= 3
                enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 50)

            if enemy_x < -100: 
                enemy_x = 800
            
            player_rect = pygame.Rect(player_x, player_y, 50, 50)

            if enemy_rect.colliderect(player_rect):
                player_hp -= 50 if boss_active else 25
                enemy_x = 800
                if hit_sound:
                    hit_sound.play()
                if player_hp <= 0:
                    game_state = "GAME_OVER"

            for p in projectiles[:]:
                p[0] += 10
                proj_rect = pygame.draw.circle(screen, (0, 255, 255), (p[0], p[1]), 10)
                if p[0] > 800:
                    projectiles.remove(p)
                elif proj_rect.colliderect(enemy_rect):
                    projectiles.remove(p)
                    if hit_sound:
                        hit_sound.play()
                    
                    if boss_active:
                        boss_hp -= 20
                        if boss_hp <= 0:
                            boss_active = False
                            enemy_x = 800
                            enemy_y = 450
                            score += 50
                            game_state = "WIN"
                    else:
                        enemy_x = 800
                        score += 10
                        
            if domain_active:
                domain_timer -= 1
                if boss_active:
                    boss_hp -= 1
                    if boss_hp <= 0:
                        boss_active = False
                        enemy_x = 800
                        enemy_y = 450
                        score += 50
                        game_state = "WIN"
                else:
                    if enemy_x < 800:
                        enemy_x = 800
                        score += 5
                if domain_timer <= 0:
                    domain_active = False

        if domain_active:
            if isinstance(domain_sprite, pygame.Surface):
                screen.blit(domain_sprite, (0, 0))
            else:
                screen.fill(domain_sprite)
        else:
            if isinstance(bg_sprite, pygame.Surface):
                screen.blit(bg_sprite, (bg_x1, 0))
                screen.blit(bg_sprite, (bg_x2, 0))
            else:
                screen.fill(bg_sprite)
        
        if game_state == "START":
            title_text = font.render("Jujutsu Sorcerer RPG", True, (255, 255, 255))
            start_text = font.render("Press ENTER to Start", True, (0, 255, 0))
            screen.blit(title_text, (280, 200))
            screen.blit(start_text, (280, 250))
            
        elif game_state == "PLAYING":
            if isinstance(player_sprite, pygame.Surface):
                screen.blit(player_sprite, (player_x, player_y))
            else:
                pygame.draw.rect(screen, player_sprite, pygame.Rect(player_x, player_y, 50, 50))
                
            if boss_active:
                if isinstance(boss_sprite, pygame.Surface):
                    screen.blit(boss_sprite, (enemy_x, enemy_y))
                else:
                    pygame.draw.rect(screen, boss_sprite, pygame.Rect(enemy_x, enemy_y, 100, 100))
                pygame.draw.rect(screen, (255, 0, 0), (enemy_x, enemy_y - 15, 100, 5))
                pygame.draw.rect(screen, (0, 255, 0), (enemy_x, enemy_y - 15, boss_hp, 5))
            else:
                if isinstance(enemy_sprite, pygame.Surface):
                    screen.blit(enemy_sprite, (enemy_x, enemy_y))
                else:
                    pygame.draw.rect(screen, enemy_sprite, pygame.Rect(enemy_x, enemy_y, 50, 50))
            
            for p in projectiles:
                pygame.draw.circle(screen, (0, 255, 255), (p[0], p[1]), 10)

            pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y - 15, 50, 5))
            pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y - 15, player_hp / 2, 5))
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            domain_text = font.render("Domain: PRESS 'D' (Cost: 50)", True, (255, 165, 0) if score >= 50 else (100, 100, 100))
            screen.blit(score_text, (10, 10))
            screen.blit(domain_text, (10, 40))
            
            if domain_active:
                domain_alert = font.render("DOMAIN EXPANSION ACTIVE!", True, (255, 0, 0))
                screen.blit(domain_alert, (250, 100))
            
        elif game_state == "GAME_OVER":
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_text = font.render("Press ENTER to Restart", True, (255, 255, 255))
            screen.blit(game_over_text, (320, 200))
            screen.blit(restart_text, (270, 250))
            
        elif game_state == "WIN":
            win_text = font.render("YOU DEFEATED THE BOSS! YOU WIN!", True, (255, 215, 0))
            restart_text = font.render("Press ENTER to Play Again", True, (255, 255, 255))
            screen.blit(win_text, (200, 200))
            screen.blit(restart_text, (250, 250))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()