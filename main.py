import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT =900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

WHITE =(255, 255, 255)
RED =(255,0,0)
YELLOW =(255,200,0)
Health_font = pygame.font.SysFont('comicsans',12)
WINNER_FONT = pygame.font.SysFont('comicsans',80)

BLACK =(0,0,0)
FPS =60 
VEL = 5
BULLET_VEL=7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT+2

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('static','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('static','Gun+Silencer.mp3'))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('static','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(55,40)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('static','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(55,40)),270)
BORDER = pygame.Rect(WIDTH/2,0,10,HEIGHT)
SPACE_BACKGROUND = pygame.image.load(os.path.join('static', 'space.png'))

def draw_window(red,yellow,yellow_bullets,red_bullets,RED_HEALTH,YELLOW_HEALTH):
    WIN.blit(SPACE_BACKGROUND, (0, 0))
    red_health_font = Health_font.render("Red Health:"+str(RED_HEALTH),1,WHITE)
    yellow_health_font = Health_font.render("Yellow Health:"+str(YELLOW_HEALTH),1,WHITE)
    border_surface = pygame.Surface((BORDER.width, BORDER.height))
    border_surface.fill(BLACK)

    WIN.blit(red_health_font, (WIDTH - red_health_font.get_width() - 10, 10))
    WIN.blit(yellow_health_font, (10, 10))
    WIN.blit(border_surface, (BORDER.x, BORDER.y))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    for bullet in red_bullets:
         pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
         pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()

def draw_winner(text):
    final_text = WINNER_FONT.render(text, 1, WHITE)
    text_rect = final_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(final_text, text_rect)
    pygame.display.update()
    pygame.time.delay(5000) 


def yellow_movement(keys_pressed,yellow):        
        if keys_pressed[pygame.K_a] and yellow.x-VEL>0:
            yellow.x-=VEL
        if keys_pressed[pygame.K_d] and yellow.x+VEL+55< BORDER.x:
            yellow.x+=VEL
        if keys_pressed[pygame.K_w] and yellow.y-VEL>0:
            yellow.y-=VEL
        if keys_pressed[pygame.K_s] and yellow.y+VEL+40<HEIGHT:
            yellow.y+=VEL

def red_movement(keys_pressed,red):        
        if keys_pressed[pygame.K_UP] and red.y-VEL>0:
            red.y-=VEL
        if keys_pressed[pygame.K_DOWN] and red.y+VEL+40<HEIGHT:
            red.y+=VEL
        if keys_pressed[pygame.K_RIGHT] and red.x+VEL+55<WIDTH:
            red.x+=VEL
        if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x+BORDER.width:
            red.x-=VEL
    
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
     
     for bullet in yellow_bullets:
          bullet.x+=BULLET_VEL
          if red.colliderect(bullet):
               pygame.event.post(pygame.event.Event(RED_HIT))
               yellow_bullets.remove(bullet)
          elif bullet.x>WIDTH:
               yellow_bullets.remove(bullet)
          
    
     for bullet in red_bullets:
          bullet.x-=BULLET_VEL
          if yellow.colliderect(bullet):
               pygame.event.post(pygame.event.Event(YELLOW_HIT))
               red_bullets.remove(bullet)
          elif bullet.x<0:
               red_bullets.remove(bullet)

def main():
    clock = pygame.time.Clock()
    red = pygame.Rect(700, 300, 55, 40)
    yellow = pygame.Rect(100, 300, 55, 40)
    yellow_bullets = []
    red_bullets = []
    RED_HEALTH =10
    YELLOW_HEALTH=10

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0 and len(red_bullets) < MAX_BULLETS + MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + 17.5, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_1 and len(yellow_bullets) < MAX_BULLETS + MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + 55, yellow.y + 17.5, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                RED_HEALTH = RED_HEALTH - 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                YELLOW_HEALTH = YELLOW_HEALTH - 1
                BULLET_HIT_SOUND.play()

        winner_text=""
        if RED_HEALTH<=0:
             winner_text="Yellow wins!"
            
        if YELLOW_HEALTH<=0:
             winner_text="Red wins!"

        if winner_text!="":
             draw_winner(winner_text)
             break
             



        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        
        draw_window(red, yellow, yellow_bullets, red_bullets,RED_HEALTH,YELLOW_HEALTH) 

    pygame.quit()

if __name__== "__main__":
    main()