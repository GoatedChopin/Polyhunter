import pygame
import random
def everything():
    dis_width = 600
    dis_height = 400
    
    def wininit(dis_width = 600, dis_height = 400):
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        WIN = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('Survivinator')
        return WIN
    WIN = wininit()
    
    font = pygame.font.SysFont('hpsimplified', 15)
    bigfont = pygame.font.SysFont('hpsimplified', 25)
    
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (213, 50, 80)
    
    FPS = 60
    vel = 2
    bullet_vel = vel*2
    
    bike_width, bike_height = 10, 10
    bike = pygame.Rect(dis_width/2,dis_height/2,bike_width,bike_height)
    b_halfwidth, b_halfheight = bike_width/4, bike_height/4
    
    bullets = {}
    bull_uniqueid = 0
    bullet_width, bullet_height = bike_width/2, bike_height/2
    
    enemies = {}
    en_uniqueid = 0
    enemy_width, enemy_height = 10, 10
    enemy_vel = vel*2
    
    points = 0
    
    def draw_window():
        WIN.fill(black)    
        WIN.blit(dis_points(),(0,0))
        pygame.draw.rect(WIN,white,[bike.x,bike.y,bike_width,bike_height])
        for bullet in bullets.keys():
            pygame.draw.rect(WIN, white, [bullets[bullet][0].x, bullets[bullet][0].y, bullet_width, bullet_height])
        for enemy in enemies.keys():
            pygame.draw.rect(WIN, red, [enemies[enemy][0].x, enemies[enemy][0].y, enemy_width, enemy_height])
        pygame.display.update()
    
    def shoot(direction):
        nonlocal bull_uniqueid
        if direction == 'left':
            bullet_xchange = -1
            bullet_ychange = 0
            bullets[bull_uniqueid] = [pygame.Rect(b_halfwidth+bike.x-bike_width,b_halfheight+bike.y,bullet_width,bullet_height),bullet_xchange, bullet_ychange]
            bull_uniqueid += 1
        if direction == 'right':
            bullet_xchange = 1
            bullet_ychange = 0
            bullets[bull_uniqueid] = [pygame.Rect(b_halfwidth+bike.x+bike_width,b_halfheight+bike.y,bullet_width,bullet_height),bullet_xchange, bullet_ychange]
            bull_uniqueid += 1
        if direction == 'up':
            bullet_xchange = 0
            bullet_ychange = -1
            bullets[bull_uniqueid] = [pygame.Rect(b_halfwidth+bike.x,b_halfheight+bike.y-bike_height,bullet_width,bullet_height),bullet_xchange, bullet_ychange]
            bull_uniqueid += 1
        if direction == 'down':
            bullet_xchange = 0
            bullet_ychange = 1
            bullets[bull_uniqueid] = [pygame.Rect(b_halfwidth+bike.x,b_halfheight+bike.y+bike_height,bullet_width,bullet_height),bullet_xchange, bullet_ychange]
            bull_uniqueid += 1
    
    def bullet_bound():
        nonlocal bullets
        deletion_keys_b = []
        for bullet in bullets.keys(): 
            if (bullets[bullet][0].x <= 0) | (bullets[bullet][0].y <= 0) | (bullets[bullet][0].x > dis_width) | (bullets[bullet][0].y > dis_height):
                deletion_keys_b.append(bullet)
        for key in deletion_keys_b:
            bullets.pop(key)
    
    def summon():
        nonlocal enemies
        nonlocal en_uniqueid
        deletion_enemies = []
        summons = random.randint(-100,5)
        if summons > 0:
            for summon in range(summons):
                location = random.randint(1,4)
                if location == 1:   # top
                    enemies[en_uniqueid] = [pygame.Rect(random.randint(0,dis_width),0,enemy_width,enemy_height),random.randint(-1,1),1]
                    en_uniqueid += 1
                if location == 2:   # right
                    enemies[en_uniqueid] = [pygame.Rect(dis_width,random.randint(0,dis_height),enemy_width,enemy_height),-1,random.randint(-1,1)]
                    en_uniqueid += 1
                if location == 3:   # bottom
                    enemies[en_uniqueid] = [pygame.Rect(random.randint(0,dis_width),dis_height,enemy_width,enemy_height),random.randint(-1,1),-1]
                    en_uniqueid += 1
                if location == 4:   # left
                    enemies[en_uniqueid] = [pygame.Rect(0,random.randint(0,dis_height),enemy_width,enemy_height),1,random.randint(-1,1)]
                    en_uniqueid += 1
        for enemy in enemies.keys(): 
            if (enemies[enemy][0].x <= 0) | (enemies[enemy][0].y <= 0) | (enemies[enemy][0].x > dis_width) | (enemies[enemy][0].y > dis_height):
                deletion_enemies.append(enemy)
        for enemy in deletion_enemies:
            enemies.pop(enemy)
        
            
    def collisions():
        nonlocal run
        nonlocal enemies
        nonlocal points
        
        deletion_enemies = []
        en_rects = []
        b_rects = []
        
        for enemy in enemies.keys():
            en_rects.append(enemies[enemy][0])
        for bullet in bullets.keys():
            b_rects.append(bullets[bullet][0])
            
        if bike.collidelist(en_rects) != -1:
            run = False
            end_screen()
    
        for enemy in enemies.keys():
            if enemies[enemy][0].collidelist(b_rects) != -1:
                deletion_enemies.append(enemy)
                points += 10
        for enemy in deletion_enemies:
            enemies.pop(enemy)
            
    def dis_points():
        nonlocal points
        current_points = font.render('Score: ' + str(int(points)), True, white)
        return current_points
    
    run = True
    def main():
        nonlocal run
        nonlocal points
        points = 0
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                bike.x -= vel
            if keys_pressed[pygame.K_RIGHT]:
                bike.x += vel
            if keys_pressed[pygame.K_DOWN]:
                bike.y += vel
            if keys_pressed[pygame.K_UP]:
                bike.y -= vel
            if keys_pressed[pygame.K_LEFT] & keys_pressed[pygame.K_SPACE]:
                shoot('left')
            if keys_pressed[pygame.K_RIGHT] & keys_pressed[pygame.K_SPACE]:
                shoot('right')
            if keys_pressed[pygame.K_DOWN] & keys_pressed[pygame.K_SPACE]:
                shoot('down')
            if keys_pressed[pygame.K_UP] & keys_pressed[pygame.K_SPACE]:
                shoot('up')
    
            for bullet in bullets.keys():
                bullets[bullet][0].x += bullets[bullet][1] * bullet_vel
                bullets[bullet][0].y += bullets[bullet][2] * bullet_vel
            
            bullet_bound()
            summon()
            collisions()
            
            for enemy in enemies.keys():
                enemies[enemy][0].x += enemies[enemy][1] * enemy_vel
                enemies[enemy][0].y += enemies[enemy][2] * enemy_vel
                
            draw_window()
            
            points += 1.0/60.0
    
    def end_screen():
        nonlocal run
        finalscore = bigfont.render('You lost! Final Score: ' + str(int(points)), True, white)
        instructions = font.render('Press C to play again, Q to quit', True, white)
        WIN = wininit()    
        WIN.fill(black)
        WIN.blit(finalscore,(dis_width//2 - finalscore.get_width()//2, dis_height//2 - finalscore.get_height()//2))
        WIN.blit(instructions, (dis_width//2 - instructions.get_width()//2, dis_height//2 + finalscore.get_height() * 2))
        pygame.display.update()
        clock = pygame.time.Clock()
        
        while not run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                    if event.key == pygame.K_c:
                        run = True
                        everything()
    
    if __name__ == '__main__':
        main()
everything()