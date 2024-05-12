from pygame import *
from random import randint
from time import time as timer

font.init()
font2 = font.SysFont('Arial', 36) #шрифт

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))                
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):     
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_passed = key.get_pressed()
        if keys_passed [K_a] and x2 < 395:
            self.rect.x-=self.speed
        if keys_passed [K_d] and x2 < 395:
            self.rect.x+=self.speed    
    def fire(self): #создание bulletа
        Sprite_top = self.rect.top
        Sprite_center_x = self.rect.centerx
        bullet = Bullet('pulya.png',Sprite_center_x, Sprite_top,-10)
        bullets.add(bullet)
        
        

propusk = 0 #пропущено монстерсов
popal = 0

class Enemy(GameSprite):
    def update(self):
        global propusk
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            propusk += 1

class Bullet (GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<=0:
            bullet = self.kill()

        
num_vystr = 0
rel_time = False
start_timer = 0       



win_width = 700
win_height = 500
window = display.set_mode((700, 500))
display.set_caption('Жоски шутер от Мистера Биста!!!')
Background = transform.scale(image.load('космосфон.png'),(700, 500))

sprite1 = Player('карабль.png', 305, 430, 6)

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('monstr.png', randint(80,win_width - 80), 0, randint(1,3))
    monsters.add(monster)

mixer.init()
mixer.music.load('фоновыймузонкрутой.ogg')
mixer.music.play()

vystrel = mixer.Sound('vystrel.ogg')

text_los = font2.render('Пропущено: ' + str(propusk), True,(255,255,255))
text_win = font2.render('Счёт: '+ str(popal), True,(255,255,255))

cock = time.Clock() #clock
FPS = 60

x1 = 100
y1 = 100
x2 = 200
y2 = 100

game = True



while game:
    window.blit(Background, (0, 0))
    for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE and num_vystr != 5:
                    num_vystr += 1
                    vystrel.play()
                    sprite1.fire()

    
    sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    for i in sprites_list:
        popal += 1
        monster = Enemy('monstr.png', randint(80,win_width - 80), 0, randint(1,2))
        monsters.add(monster)

    sprites_list2 = sprite.spritecollide(sprite1, monsters, False)
    if sprites_list2:
        end = font2.render('Поражение :(', True, (255,0,0))
        window.blit(end,(250,250))
        game = False 
    
    if popal >= 10:
        win = font2.render('Победа :)', True, (0,255,0))
        window.blit(win,(250,250))
        game = False

    if propusk >= 10:
        end = font2.render('Поражение :(', True, (255,0,0))
        window.blit(end,(250,250))
        game = False 

    if num_vystr == 5:
        start_timer = timer()
        rel_time = True
        num_vystr = 0
    tek_timer = timer()
    if tek_timer - start_timer < 3:
        rel = font2.render('Перезарядка!', True, (255,0,0))
        window.blit(rel,(250,550))
        


    rel2 = font2.render(str(tek_timer), True, (255,0,0))
    window.blit(rel2,(50,240))
    rel3 = font2.render(str(start_timer), True, (255,0,0))
    window.blit(rel3,(50,170))
    sprite1.reset()
    text_los = font2.render('Пропущено: ' + str(propusk), True,(255,255,255))
    window.blit(text_los,(50,100))
    text_win = font2.render('Счёт: '+ str(popal), True,(255,250,255))
    window.blit(text_win,(50,70))
    sprite1.update()
    monsters.draw(window)
    monsters.update()
    bullets.update()
    bullets.draw(window)
    display.update()
    cock.tick(FPS) 