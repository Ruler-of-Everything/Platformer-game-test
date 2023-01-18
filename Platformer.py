import turtle
import sys
import math
import random

LARGURA = 1200
ALTURA = 800

TILESIZE = 40
MAPWIDTH = 5
MAPHEIGHT = 2

GRAVIDADE = -0.01

PRETO = (0,0,0)
BRANCO = (255,255,255)
VERDE = (0,255,0)
AZUL = (0,0,255)
VERMELHO = (255,0,0)
AMARELO = (255,0,0)
# Criar ecrã
wn = turtle.Screen()
wn.colormode(255)
wn.title("Título")
wn.setup(LARGURA,ALTURA)
wn.bgcolor(PRETO)
wn.tracer(0)

# Criar pen
pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.color(BRANCO)
pen.hideturtle()


class Sprite():
    def __init__(self, x,y,width,height):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height
        self.color = BRANCO
        self.fric = 0.99

    def goto(self,x,y):
        self.x = x
        self.y = y

    def render(self):
        pen.pencolor(self.color)
        pen.fillcolor(self.color)
        pen.penup()
        pen.goto(self.x-self.width/2.0, self.y+self.height/2.0)
        pen.pendown()
        pen.begin_fill()
        pen.goto(self.x+self.width/2.0, self.y+self.height/2.0)
        pen.goto(self.x+self.width/2.0, self.y-self.height/2.0)
        pen.goto(self.x-self.width/2.0, self.y-self.height/2.0)
        pen.goto(self.x-self.width/2.0, self.y+self.height/2.0)
        pen.end_fill()
        pen.penup()

    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x-other.x)*2) < (self.width + other.width)
        y_collision = (math.fabs(self.y-other.y)*2) < (self.height + other.height)
        return(x_collision and y_collision)

class Player(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self,x,y,width,height)
        self.color = VERDE
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVIDADE

    def jump(self):
        self.dy = 2

    def left(self):
        self.dx -= 1

    def right(self):
        self.dx += 1
        
# Objetos do jogo
player = Player(-550, -250, 40, 40)

blocks = [Sprite(-650,-350 ,350,50), Sprite (275, -250, 125, 60),Sprite(575, -150, 175, 50),Sprite (295, 0, 150, 50),Sprite(-700, 200 ,600,50)]
balas = [ ]
          
def player_jump():
    for block in blocks:
        if player.is_aabb_collision(block):
            player.jump()
            break
            
# Input
wn.listen()
wn.onkeypress(player.left, "a")
wn.onkeypress(player.right, "d")
wn.onkeypress(player.jump, "space")
# Ciclo do jogo
while True:
    player.move()
    
    for block in blocks:
        if player.is_aabb_collision(block):
            
            if player.x < block.x - block.width/2.0 and player.dx > 0:
                player.dx = 0
                player.x = block.x - block.width/2.0 - player.width/2.0
            
            elif player.x > block.x + block.width/2.0 and player.dx < 0:
                player.dx = 0
                player.x = block.x + block.width/2.0 + player.width/2.0
            
            elif player.y > block.y:
                player.dy = 0
                player.y = block.y + block.height/2.0 + player.height/2.0 - 1
        
          
            elif player.y < block.y:
                player.dy = 0
                player.y = block.y - block.height/2.0 - player.height/2.0 

    #Caiu fora do mapa?
    if player.y < -400:
        player.goto(-550,-250)
        player.dx = 0
        player.dy = 0
        
    #Desenhar objectos
    player.render()
    for block in blocks:
        block.render()
    for bala in balas :
        bala.render()
        bala.x += 5
    #atualizar
    wn.update()

    #limpar ecrã
    pen.clear()
