import pygame
from sys import exit
#from numpy import abs
def display_score(prev_score = 0):
    curtime = pygame.time.get_ticks()
    return curtime-prev_score
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    game_active = True
    prev_score = 0
    test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    # restart_surf = test_font.render("Press Return to restart Game", False, '#404040')
    # restart_rect = restart_surf.get_rect(midtop=(400, 50))
    sky_surf = pygame.image.load("graphics/Sky.png").convert()
    ground_surf = pygame.image.load("graphics/ground.png").convert()
    ground_rect = ground_surf.get_rect(topleft= (0, 300))
    # score_surf = test_font.render("My Game", False, '#404040')
    # score_rec = score_surf.get_rect(midtop=(400, 50))
    snail = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
    snail_x_pos_start = 800
    snail_rect = snail.get_rect(bottomleft = (snail_x_pos_start, ground_rect.top))
    player = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
    player_rect = player.get_rect(midbottom = (100, ground_rect.top))
    player_jumping = False
    player_jumpload = 0
    player_grav = 0
    player_vel = 0
    contact_timeout = 0
    score_red = 0
    #test_surface.fill('#aa0000')
    #player_stats = [0, 0]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_grav == 0:
                    player_jumping = True
                #print("Jumploading")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and player_jumpload > 0:
                    #print(player_jumpload)
                    #print("JUMPING")
                    player_grav -= player_jumpload/10
                    player_jumpload = 0
                    player_jumping = False
                    #print(player_grav)
                if event.key == pygame.K_RETURN and not game_active:
                    game_active = True
                    snail_rect.left = snail_x_pos_start
                    player_rect.left = 100
                if event.key == pygame.K_ESCAPE and not game_active:
                    pygame.quit()
                    exit()
                        
        if game_active: 
            screen.blit(sky_surf, (0, 0))
            screen.blit(ground_surf, ground_rect)
            # pygame.draw.rect(screen, '#c0e8ec', score_rec)
            # screen.blit(score_surf, score_rec)
            score_surf = test_font.render(f'{display_score(prev_score)//1000}', False, '#a04040' if score_red > 0 else '#404040')
            score_rect = score_surf.get_rect(midtop=(400, 50))
            screen.blit(score_surf, score_rect)
            
            if score_red > 0:
                score_red -= 1
            
            if player_jumping:
                #print(player_jumpload)
                if player_jumpload == 0:
                    player_jumpload = 60
                else:
                    player_jumpload+=200/player_jumpload
            if player_rect.bottom == ground_rect.top:
                if pygame.key.get_pressed()[pygame.K_LEFT]: 
                    player_vel -= 100/(30 if player_vel >= 0 else -player_vel)
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    player_vel += 100/(30 if player_vel <= 0 else player_vel)
                else: 
                    player_vel = 0 if abs(player_vel)<30 else player_vel*0.7
            
            # if player_vel > player_stats[0]:
            #     player_stats[0] = player_vel
            #     print(player_stats)
                
            # if player_vel < player_stats[1]:
            #     player_stats[1] = player_vel
            #     print(player_stats)
                
            if player_rect.left +player_vel/10 > 0 and player_rect.right + player_vel/10 < 800:
                player_rect.left += player_vel/10
            else:
                player_rect.left = 0 if player_rect.left + player_vel/10 <= 0 else 800 - player_rect.width
                player_vel = 0
            
            if player_rect.bottom<ground_rect.top or player_grav<0:
                player_grav+=1
                player_rect.bottom+=player_grav
                #print(player_rect.bottom)
                if player_rect.bottom>=ground_rect.top:
                    player_rect.bottom = ground_rect.top
                    if player_grav > 15 - display_score(prev_score)/333333:
                        reduction = player_grav - 14 + display_score(prev_score)/333
                        prev_score += int(reduction)*10
                        score_red += int(reduction)
                        # print(reduction)
                    player_grav = 0
            if contact_timeout > 0 and contact_timeout//5 % 2 == 0:
                player.set_alpha(128)
            else:    
                player.set_alpha(255)
            screen.blit(player, player_rect)
            if snail_rect.right < 0:
                snail_rect.left = snail_x_pos_start
            else:
                snail_rect.left -= (2 + display_score(prev_score)/33333)
            screen.blit(snail, snail_rect)
            
            if contact_timeout > 0:
                contact_timeout -= 1
            
            if player_rect.colliderect(snail_rect) and contact_timeout == 0:
                prev_score+=10000
                contact_timeout = 120
                score_red = 120
                if display_score(prev_score) < 0:
                    print(display_score(prev_score))
                    game_active = False
                #pass
    #            print("snail collided with player")
        else:
            prev_score += display_score(prev_score)
            restart_surf = test_font.render("Press Return to restart or ESC to exit", False, '#404040')
            restart_rec = restart_surf.get_rect(midtop=(400, 100))
            screen.blit(restart_surf, restart_rec)
            #score_rec.bottom = 0
            #screen.blit(restart_surf, restart_rect)
        
        pygame.display.update()
        clock.tick(60)
    
if __name__ == "__main__":
    main()