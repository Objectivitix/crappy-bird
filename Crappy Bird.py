import math
from random import randint
import pgzrun


WIDTH = 600
HEIGHT = 600

print("\n\n--------------------")
print("Welcome to Crappy Bird!!\n")
print("Controls:")
print("Space or up arrow to fart, s or down arrow to dive.\n")

print("Backstory:")
print("The year was 2013. Flappy Bird had the most glorious time ever.")
print("People were loving him, praising him, he was the king of mobile arcade games.")
print("However, it didn't last long.")
print("Soon came the hate. Flappy Bird was insulted, discriminated, and abandonned.")
print("He lost his throne, and was exiled to the Craplands.")
print("There, he was tortured by the smell of the place and its inhabitants. Life was awful.")
print("Flappy Bird became Crappy Bird.")
print("Now, he couldn't take it anymore.")
print("He flies around Craplands looking for a road to freedom, a road that leads out of misery.\n")

print("Credits:")
print("Made in Python, game directly inspired by Flappy Bird.", end="")
print("This is a fan-made version. Music - Nyan Cat(Original)")
print("--------------------\n\n\n")

while True:
    try:
        difficulty = int(
            input('\nSelect difficulty. Type 1, 2, or 3. \n1 = Easy, \n2 = Medium, \n3 = Hard.   '))
    except ValueError:
        print('You did not enter a valid input. Please try again.')
    else:
        break

print('\nHave fun!')

Yv = 0
obsSpeed = 3.2
monsterSpeed = 2.2
score = 0
bossShot = 0

highScore = None

victory = False
gameStart = False
gameOver = False
bossTime = False
bossOnce = True
endFart = True

obstacles = [
    Actor('obstacle-1-1', (700, 300)),
    Actor('obstacle-1-2', (700, 300)),
    Actor('obstacle-2-1', (700, 300)),
    Actor('obstacle-2-2', (700, 300))
]

monster = Actor('crap-monster', (700, 300))
poopBoss = Actor('poop-bot', (800, 300))
nuke = Actor('nuke', (900, 300))
bird = Actor('crapbird', (difficulty*90, 200))
portal = Actor('portal', (700, 300))
victoryIndicator = Actor('victory', (300, 200))


def draw():
    global endFart
    if not gameOver and gameStart:
        if not victory:
            screen.blit('crappedcity', (0, 0))
            screen.draw.text('Score: '+str(score), topleft=(20, 20), fontsize=30)
            screen.draw.text('High score: '+str(highScore), topleft=(20, 45), fontsize=30)
            for i in range(0, 4):
                obstacles[i].draw()
            bird.draw()
            monster.draw()
            poopBoss.draw()
            nuke.draw()
            portal.draw()
        else:
            music.stop()
            screen.blit('normalcity', (0, 0))
            screen.draw.text('Score: '+str(score), topleft=(20, 20), fontsize=30)
            screen.draw.text('High score: '+str(highScore), topleft=(20, 45), fontsize=30)
            screen.draw.text('You helped Flappy Bird escape Craplands!',
                             center=(300, 320), fontsize=35, color='black')
            bird.draw()
            victoryIndicator.draw()
    elif gameOver:
        music.stop()
        if endFart:
            endFart = False
            sounds.endfart.play()
        screen.draw.text('Score: '+str(score), topleft=(20, 20), fontsize=30)
        clock.schedule(game_over, 0.3)
    else:
        screen.draw.text('PRESS SPACE TO START', center=(300, 300), fontsize=60)


def update():
    global Yv, gameOver, gameStart, score, bossTime, bossOnce, victory, highScore
    score = round(score, 1)
    if not gameOver and gameStart:
        with open('highscore.txt', 'r') as f:
            highScore = f.readline()
        if not victory:
            bird.y -= Yv
            Yv -= 0.18
            if score > 300:
                animate(portal, pos=(-200, 300), duration=3)
            if keyboard.space or keyboard.up:
                sounds.birdfart.play()
                if Yv < 3:
                    Yv += 1.5
            if keyboard.s or keyboard.down:
                bird.y += 0.2
            if score > float(highScore):
                with open('highscore.txt', 'w') as f:
                    f.write(str(score))
            if bird.y < 100:
                bird.y = 100
            if score > 100 and bossOnce:
                bossTime = True
                bossOnce = False
                clock.schedule(boss_time, 2)
            xDis, yDis = nuke.x - bird.x, nuke.y - bird.y
            Dis = math.hypot(xDis, yDis)
            for i in range(0, 4):
                if bird.colliderect(obstacles[i]) or bird.colliderect(monster) or Dis < 125 or bird.y > 650:
                    gameOver = True
                    gameStart = False
            if bird.colliderect(portal):
                sounds.lavictoire.play()
                victory = True
        else:
            bird.image = ('flapbird')
            bird.pos = (300, 400)
    else:
        if keyboard.space:
            gameStart = True
            music.play('poopy-cat')
            clock.schedule(spawn_obstacles_one, 3)
            clock.schedule(spawn_obstacles_two, 4.5)
            clock.schedule(monster_time, 4.5)


def spawn_obstacles_one():
    global obstacles, obsSpeed
    if (not gameOver) and (gameStart) and (not bossTime) and (not victory):
        randY = randint(0, 50)
        obstacles[0].pos = (700, randY)
        obstacles[1].pos = (700, randY+550)
        animate(obstacles[0], pos=(-100, obstacles[0].y), duration=obsSpeed, on_finished=score_up)
        animate(obstacles[1], pos=(-100, obstacles[1].y), duration=obsSpeed)
        clock.schedule(spawn_obstacles_one, obsSpeed)
        if obsSpeed > 1.8 - difficulty/7:
            obsSpeed -= difficulty*0.05


def spawn_obstacles_two():
    global obstacles, obsSpeed
    if (not gameOver) and (gameStart) and (not bossTime) and (not victory):
        randY = randint(0, 50)
        obstacles[2].pos = (700, randY)
        obstacles[3].pos = (700, randY+550)
        animate(obstacles[2], pos=(-100, obstacles[2].y), duration=obsSpeed, on_finished=score_up)
        animate(obstacles[3], pos=(-100, obstacles[3].y), duration=obsSpeed)
        clock.schedule(spawn_obstacles_two, obsSpeed)
        if obsSpeed > 1.8 - difficulty/7:
            obsSpeed -= difficulty*0.05


def monster_time():
    global monsterSpeed
    monsterY = [randint(-100, -60), randint(60, 100)]
    monster.pos = (700, bird.y+monsterY[randint(0, 1)])
    if not gameOver and gameStart and not victory:
        animate(monster, pos=(-100, monster.y), duration=monsterSpeed)
        clock.schedule(monster_time, monsterSpeed*2)
        if monsterSpeed > 1.4 - difficulty/7:
            monsterSpeed -= difficulty*0.05


def boss_time():
    if bossShot < 8:
        animate(poopBoss, pos=(480, randint(150, 450)), duration=1, on_finished=boss_shoot)
    else:
        animate(poopBoss, pos=(800, 300), duration=1, on_finished=back_to_normal)


def boss_shoot():
    global bossShot
    bossShot += 1
    nuke.pos = (900, poopBoss.y)
    animate(nuke, pos=(-200, poopBoss.y), duration=1.6, on_finished=boss_time)


def back_to_normal():
    global bossTime, score
    bossTime = False
    score += 15
    clock.schedule(spawn_obstacles_one, obsSpeed+1)
    clock.schedule(spawn_obstacles_two, obsSpeed/2+obsSpeed+1)
    clock.schedule(monster_time, 4.5)


def game_over():
    screen.blit('poop-on-the-haters', (0, 0))


def score_up():
    global score
    if (not gameOver) and (not victory):
        score += 1


pgzrun.go()
