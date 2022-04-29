import pygame
import random
import time
import math

pygame.init()

# General variables
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gengar and the Electrical Mayhem")
bg_pos = [-1197,0]
bg_vel = [0.03, 1]
clock = pygame.time.Clock()
fps = 100
game_over = False
kills = 0
max_health = 250
health = 250
damage = 60
damage_check = 0
damage_bool = False

# Fonts 
font = pygame.font.SysFont("inkfree bold", 32)
kills_text_pos= [15,65]

# Characters
form = [0]
jump = 0  # jump activatopr
dive = 0  # dive ctivatopr
max_jump = 200 # max jump
max_dive = 200 # max dive

# gengar
gengar_size = [100, 100]
gengar_pos = [width/2, height - gengar_size[1]]
gengar_vel = [0.2, 0.7, 0.4] # gengar vel [horizontal, vertically upwards, vertically downwards]
recoil = [[False, 20], [False, 30]]
# recoil[0][1] --> recoil distance from shadow_ball
# recoil[1][1] --> recoil distance from electro_ball hit
# Electabuzz
electabuzz_size = [110, 110]
electabuzz_pos = []
electabuzz_vel = []
electabuzz_count = 1
deploy = [-electabuzz_size[0], width]
speed_factor = 0

# Shadow ball
shadow_ball_size = [75, 86]
shadow_ball_vel = [5, 0]
shadow_ball_pos = []
shadow_ball_bool = []
max_shadow_ball_count = 1

# Electroballs
electro_ball_size = [75, 69]
electro_ball_vel = [0.4, 0]
electro_ball_pos = []

# explosion variables
explosion_form = []
explosion_bool = []
explosion_pos = []
explosion_size = [200, 282]

# images
images = {
    "background": pygame.image.load("images\\dark_bg.png").convert(),

    "grass": pygame.image.load("images\\grass.png").convert_alpha(),

    "shadow_ball": pygame.image.load("images\\shadow_ball.png").convert_alpha(),

    "electro_ball": pygame.image.load("images\\electro_ball.png").convert_alpha(),

    "gengar_health" : pygame.image.load("images\\gengar_health.png").convert_alpha(),

    "gengar": [pygame.image.load("images\\gengar_left.png").convert_alpha(),
               pygame.image.load("images\\gengar_right.png").convert_alpha(),
               pygame.image.load(
                   "images\\gengar_attack_left.png").convert_alpha(),
               pygame.image.load("images\\gengar_attack_right.png").convert_alpha()],

    "electabuzz": [pygame.image.load("images\\electabuzz_left.png").convert_alpha(),
                   pygame.image.load("images\\electabuzz_right.png").convert_alpha(),
                   pygame.image.load("images\\electabuzz_attack_left.png").convert_alpha(),
                   pygame.image.load("images\\electabuzz_attack_right.png").convert_alpha()
                   ]
}

audio = {
    "bgm_main": pygame.mixer.Sound("audio\\bgm_main.mp3"),
    "bgm_1": pygame.mixer.Sound("audio\\bgm_1.mp3"),
    "bgm_2": pygame.mixer.Sound("audio\\bgm_2.mp3"),
    "gengar": pygame.mixer.Sound("audio\\gengar.mp3"),
    "electabuzz": pygame.mixer.Sound("audio\\electabuzz.mp3"),
    "explosion": pygame.mixer.Sound("audio\\explosion.mp3")
}

def explosion(explosion_form, shadow_ball_pos):  
    screen.blit(pygame.image.load(f"images\\explosions\\exp_{explosion_form//2}.png").convert_alpha(), (shadow_ball_pos[0], shadow_ball_pos[1]))
    pygame.display.update()

def intro1():
    next = False
    bg_pos = [0,0]
    obj1_pos = [200, 450]
    obj2_pos = [300, -100]
    obj1_vel = 1
    t = 0
    pygame.mixer.Channel(0).play(audio["bgm_1"], loops = -1)
    pygame.mixer.Channel(0).set_volume(0.4)
    while not next:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    obj1_pos[1] = 0
                if event.key == pygame.K_RETURN and obj1_pos[1] == 0:
                    next = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if abs(pygame.mouse.get_pos()[0] - obj2_pos[0] - 75) <=  75 and abs(pygame.mouse.get_pos()[1] - obj2_pos[1] - 39) <= 39:
                    next = True
        if obj1_pos[1] > 0:
            obj1_pos[1] -= obj1_vel
        if obj1_pos[1] <= 0:
            obj2_pos[1] = 300 + 25*math.sin(t)
            t += 0.1
        screen.blit(pygame.image.load("images\\intro.png").convert(), (bg_pos[0], bg_pos[1]))
        screen.blit(pygame.image.load("images\\continue.png").convert_alpha(), (obj2_pos[0], obj2_pos[1]))
        screen.blit(pygame.image.load("images\\logo.png").convert_alpha(), (obj1_pos[0], obj1_pos[1]))
        pygame.display.update()
    pygame.mixer.Channel(0).stop()
    pygame.mixer.Channel(3).play(audio["gengar"])


def intro2():
    next = False
    bg_pos[0] = 0
    bg_vel = [4, 2, 10]
    obj1_pos = [800,100]
    obj2_pos = [-300,100]
    obj3_pos = [250, 400]
    obj4_1_pos = [- 1000, - 300]
    obj4_2_pos = [width, - 300]
    switch = 0
    spark_interval = 50
    pygame.mixer.Channel(1).play(audio["bgm_2"])
    pygame.mixer.Channel(1).set_volume(0.4)
    while not next:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and obj3_pos[1] <= 200:
                    next = True
        if bg_pos[0] > -200:
            bg_pos[0] -=  bg_vel[0]
            obj1_pos[0] -= bg_vel[0]
            obj2_pos[0] += bg_vel[0]
        if bg_pos[0] <= -200 and obj3_pos[1] >= 200:
            spark_interval = 2
            obj1_pos[0] += 0.2*bg_vel[0]
            obj2_pos[0] -= 0.2*bg_vel[0]
            obj3_pos[1] -= bg_vel[1]
            obj4_1_pos[0] += bg_vel[2]
            obj4_2_pos[0] -= bg_vel[2]

        switch += 1
        if switch == spark_interval:
            switch = 0
        screen.blit(pygame.image.load("images\\intro2\\night_sky.png"), (bg_pos[0], bg_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\cloud_intro2.png"), (obj4_1_pos[0], obj4_1_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\cloud_intro2.png"), (obj4_2_pos[0], obj4_2_pos[1]))
        if switch % spark_interval == 0:
            screen.blit(pygame.image.load("images\\intro2\\lightning_intro2.png").convert_alpha(), (0,0))
        screen.blit(pygame.image.load("images\\intro2\\electabuzz_intro2.png").convert_alpha(), (obj1_pos[0], obj1_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\electabuzz2_intro2.png").convert_alpha(), (obj2_pos[0], obj2_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\gengar_intro2.png").convert_alpha(), (obj3_pos[0], obj3_pos[1]))        
        pygame.display.update()
    pygame.mixer.Channel(1).stop()

def end1():
    next = False
    bg_pos[0] = 0
    bg_vel = [1, 0.5, 4]
    obj1_pos = [700,100]
    obj2_pos = [-200,100]
    obj3_pos = [250, 200]
    obj4_1_pos = [-200, - 300]
    obj4_2_pos = [300, - 300]
    switch = 50
    spark_interval = 1
    pygame.mixer.Channel(0).play(audio["bgm_1"], loops = -1)
    pygame.mixer.Channel(0).set_volume(0.4)
    while not next:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and obj3_pos[1] <= 200:
                    next = True
        
        if bg_pos[0] <= -200:
            spark_interval = 100
        elif bg_pos[0] >= -200:
            spark_interval = 2
            bg_pos[0] -=  bg_vel[0]
            obj3_pos[1] += bg_vel[0]
            obj4_1_pos[0] -= bg_vel[2]
            obj4_2_pos[0] += bg_vel[2]
            obj1_pos[0] -= bg_vel[1]
            obj2_pos[0] += bg_vel[1]

        if switch == 0:
            switch = 50
        switch -= 1

        screen.blit(pygame.image.load("images\\intro2\\night_sky.png"), (bg_pos[0], bg_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\cloud_intro2.png"), (obj4_1_pos[0], obj4_1_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\cloud_intro2.png"), (obj4_2_pos[0], obj4_2_pos[1]))
        if switch % spark_interval == 0:
            screen.blit(pygame.image.load("images\\intro2\\lightning_intro2.png").convert_alpha(), (0,0))
        screen.blit(pygame.image.load("images\\intro2\\electabuzz_intro2.png").convert_alpha(), (obj1_pos[0], obj1_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\electabuzz2_intro2.png").convert_alpha(), (obj2_pos[0], obj2_pos[1]))
        screen.blit(pygame.image.load("images\\intro2\\gengar_end1.png").convert_alpha(), (obj3_pos[0], obj3_pos[1]))        
        pygame.display.update()
    pygame.mixer.Channel(1).stop()

# driver code
intro1()
intro2()

pygame.mixer.Channel(2).play(audio["bgm_main"], loops = -1)
pygame.mixer.Channel(2).set_volume(0.4)
while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and jump == 0 and dive == 0:
                jump = 1
            if event.key == pygame.K_DOWN and dive == 0 and jump == 0:
                dive = 1
            if event.key == pygame.K_SPACE and len(shadow_ball_pos) < max_shadow_ball_count:
                shadow_ball_bool.append(True)
                shadow_ball_pos.append([gengar_pos[0], gengar_pos[1]])
                recoil[0][0] = True

    # Gengar navigation
    # Pressed key events
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        form[0] = 0
        gengar_pos[0] -= gengar_vel[0]
        bg_pos[0] += bg_vel[0]
    elif pressed_keys[pygame.K_RIGHT]:
        form[0] = 1
        gengar_pos[0] += gengar_vel[0]
        bg_pos[0] -= bg_vel[0]
    # Horizontal boundary check
    if gengar_pos[0] <= 0:
            gengar_pos[0] = 0
    elif gengar_pos[0] >= width - gengar_size[0]:
            gengar_pos[0] = width - gengar_size[0]
    # Jump motion
    if jump == 1:
        gengar_pos[1] -= gengar_vel[1]
        if gengar_pos[1] <= height - max_jump - gengar_size[1]:
            jump = 2
        if form[0] == 0:
            form[0] = 2
        elif form[0] == 1:
            form[0] = 3
    elif jump == 2:
        gengar_pos[1] += gengar_vel[1]
        if gengar_pos[1] >= height - gengar_size[1]:
            jump = 0
        if form[0] == 0: 
            form[0] = 2
        elif form[0] == 1:
            form[0] = 3
        
    # Dive motion
    if dive == 1:
        gengar_pos[1] += gengar_vel[2]
        if gengar_pos[1] >= height + max_dive + gengar_size[1]:
            dive = 2
    elif dive == 2:
        gengar_pos[1] -= gengar_vel[2]
        if gengar_pos[1] <= height - gengar_size[1]:
            dive = 0

    # Electabuzz position
    if len(electabuzz_pos) < electabuzz_count:
        for i in range(electabuzz_count - len(electabuzz_pos)):
            pygame.mixer.Channel(4).play(audio["electabuzz"])
            speed_factor += 1
            electabuzz_pos.append([deploy[random.randint(0,1)], height - electabuzz_size[1]])
            electabuzz_vel.append([0.05*speed_factor, 0])
            if electabuzz_pos[len(electabuzz_pos)-1][0] > gengar_pos[0]:
                form.append(0) 
            elif electabuzz_pos[len(electabuzz_pos)-1][0] < gengar_pos[0]:
                form.append(1)

    # Electabuzz motion
    for i in range(electabuzz_count):
        if electabuzz_pos[i][0] >= gengar_pos[0]:
            form[i+1] = 0
            electabuzz_pos[i][0] -= electabuzz_vel[i][0]
        elif electabuzz_pos[i][0] < gengar_pos[0]:
            form[i+1] = 1
            electabuzz_pos[i][0] += electabuzz_vel[i][0]

    # Shadow ball motion and recoil
    try:
        for i in range(len(shadow_ball_pos)):
            if shadow_ball_bool[i] and jump == 0:
                if form[0] == 0:
                    form[0] = 2
                    shadow_ball_pos[i][0] -= shadow_ball_vel[0]
                    if recoil[0][0]:
                        gengar_pos[0] += recoil[0][1]
                        recoil[0][0] = False
                elif form[0] == 1:
                    form[0] = 3
                    shadow_ball_pos[i][0] += shadow_ball_vel[0]
                    if recoil[0][0]:
                        gengar_pos[0] -= recoil[0][1]
                        recoil[0][0] = False
                if shadow_ball_pos[i][0] <= -shadow_ball_size[0] or shadow_ball_pos[i][0] >= width:
                    shadow_ball_pos.pop(i)
                    shadow_ball_bool.pop(i)
            
            elif shadow_ball_bool[i]:
                if form[0] == 2:
                    shadow_ball_pos[i][0] -= shadow_ball_vel[0]
                    if recoil[0][0]:
                        gengar_pos[0] += recoil[0][1]
                        recoil[0][0] = False
                elif form[0] == 3:
                    shadow_ball_pos[i][0] += shadow_ball_vel[0]
                    if recoil[0][0]:
                        gengar_pos[0] -= recoil[0][1]
                        recoil[0][0] = False
                if shadow_ball_pos[i][0] <= -shadow_ball_size[0] or shadow_ball_pos[i][0] >= width:
                    shadow_ball_pos.pop(i)
                    shadow_ball_bool.pop(i)
    except:
        pass

    # Electroball motion
    if len(electro_ball_pos) < electabuzz_count:
        for i in range(electabuzz_count - len(electro_ball_pos)):
            if form[i+1] == 0:
                electro_ball_pos.append([electabuzz_pos[len(electro_ball_pos)][0] - electro_ball_size[0], height - electro_ball_size[1]])
            elif form[i+1] == 1:
                electro_ball_pos.append([electabuzz_pos[len(electro_ball_pos)][0] + electro_ball_size[0], height - electro_ball_size[1]])
    for i in range(len(electabuzz_pos)):
        if electro_ball_pos[i][0] < electabuzz_pos[i][0]:
            electro_ball_pos[i][0] -= electro_ball_vel[0]
        elif electro_ball_pos[i][0] >= electabuzz_pos[i][0]:
            electro_ball_pos[i][0] += electro_ball_vel[0]
        if (electro_ball_pos[i][0] <= - electro_ball_size[0] or electro_ball_pos[i][0] >= width):
            electro_ball_pos.pop(i)

    # shadow ball - electroball collision
    for i in range(len(shadow_ball_pos)):
        for j in range(len(electro_ball_pos)):
            if abs(electro_ball_pos[j][0] - shadow_ball_pos[i][0]) <= 20 and abs(electro_ball_pos[j][1] - shadow_ball_pos[i][1]) <= 50:
                pygame.mixer.Channel(5).play(audio["explosion"])
                explosion_form.append(0)
                explosion_bool.append(True)
                explosion_pos.append([(shadow_ball_pos[i][0] + electro_ball_pos[j][0] - explosion_size[0]/2)/2, height - 3*explosion_size[1]/4])
                pygame.display.update()
                time.sleep(0.05) 
                electro_ball_pos.pop(j)
                shadow_ball_pos.pop(i) 
                shadow_ball_bool.pop(i)
                break

    # shadow ball - electabuzz collision
    for i in range(len(shadow_ball_pos)):
        for j in range(len(electabuzz_pos)):
            if abs(electabuzz_pos[j][0] - shadow_ball_pos[i][0]) <= 130 and abs(electabuzz_pos[j][1] - shadow_ball_pos[i][1]) <= 20:
                kills += 1
                pygame.mixer.Channel(4).play(audio["electabuzz"])
                explosion_form.append(0)
                explosion_bool.append(True)
                explosion_pos.append([(shadow_ball_pos[i][0] + electabuzz_pos[j][0] - explosion_size[0]/2)/2, height - 3*explosion_size[1]/4])
                pygame.display.update() 
                time.sleep(0.05) 
                electabuzz_pos.pop(j)
                shadow_ball_pos.pop(i)
                break

    # electro ball - gengar collision
    for i in range(len(electro_ball_pos)):
        if abs(electro_ball_pos[i][0] - gengar_pos[0]) <= 50 and abs(electro_ball_pos[i][1] - gengar_pos[1]) <= 50:
            damage_bool = True
            pygame.mixer.Channel(3).play(audio["gengar"])
            explosion_form.append(0)
            explosion_bool.append(True)
            explosion_pos.append([(electro_ball_pos[i][0] + gengar_pos[0] - explosion_size[0]/2)/2, height - 3*explosion_size[1]/4])
            if gengar_pos[0] >= electro_ball_pos[i][0]:
                gengar_pos[0] += recoil[1][1]
                form[0] = 0
            elif gengar_pos[0] < electro_ball_pos[i][0]:
                gengar_pos[0] -= recoil[1][1]
                form[0] = 1
            electro_ball_pos.pop(i)
            pygame.display.update()
            time.sleep(0.05)
            if health <= 0:
                game_over = True
            break

    # BG Display
    screen.blit(images["background"], (bg_pos[0], bg_pos[1]))

    # Score Display
    kills_text = font.render("KILLS : " + str(kills), True, (255, 255, 255))
    screen.blit(kills_text, (kills_text_pos[0], kills_text_pos[1]))

    # Health display
    if damage_bool:
        if damage_check >= damage:
            damage_check = 0
            damage_bool = False
        health -= 1/16
        damage_check += 1/16
        
    pygame.draw.rect(screen, (0, 0, 0), [15, 25, max_health + 10, 30])
    pygame.draw.rect(screen, (255,0, 0), [20, 30, max_health, 20]) 
    pygame.draw.rect(screen, (0, 255, 0), [20, 30, health, 20])
    screen.blit(images["gengar_health"],(7, -5))

    # Electabuzz display
    for i in range(len(electabuzz_pos)):
        screen.blit(images["electabuzz"][form[i+1]], (electabuzz_pos[i][0], electabuzz_pos[i][1]))
    # Gengar display
    screen.blit(images["gengar"][form[0]], (gengar_pos[0], gengar_pos[1]))
    # Shadow ball display
    for i in range(len(shadow_ball_pos)):
        screen.blit(images["shadow_ball"],(shadow_ball_pos[i][0], shadow_ball_pos[i][1]))
    # # Electroball ball display
    for i in range(len(electro_ball_pos)):
        screen.blit(images["electro_ball"],(electro_ball_pos[i][0], electro_ball_pos[i][1]))
    # Grass display
    screen.blit(images["grass"], (0, height - 55))

    for i in range(len(explosion_bool)):
        try:
            if explosion_bool[i]:
                explosion(explosion_form[i], explosion_pos[i])
                explosion_form[i] += 1
                if explosion_form[i] == 30:
                    explosion_form.pop(i)
                    explosion_bool.pop(i) 
                    explosion_pos.pop(i)
        except:
            pass
        

    # Updates
    pygame.display.update()

    # Resets
    # gengar reset
    if form[0] == 2:
        form[0] = 0
    if form[0] == 3:
        form[0] = 1

    #FPS
    # clock.tick(fps)
pygame.mixer.Channel(2).stop()
end1()
