import pygame
from pygame.locals import *
import os
import sys

COLOR=(75,72,125)
WHITE=(255,255,255)
LINETHICKNESS = 15
IMG_DIR="imagenes"
SCREEN_WIDTH=800
SCREEN_HEIGHT=500
SONIDO_DIR="sonidos"
class Pelota(pygame.sprite.Sprite):
    "La bola y su comportamiento en la pantalla"
    global xi,yi
    xi,yi=[],[]

    def __init__(self,sonido_golpe, jugador):

        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = jugador.rect.centerx
        self.rect.centery = jugador.rect.centery
        self.speed = [10,10]
        self.sonido_golpe = sonido_golpe

    def reiniciar(self, jugador):
        self.rect.centerx = jugador.rect.centerx
        self.rect.centery = jugador.rect.centery
        self.speed = [10, 10]

    def update(self, cont):
        print cont
        pared,cae=False,False
        if self.rect.left < LINETHICKNESS or self.rect.right > SCREEN_WIDTH-LINETHICKNESS:
            pared=True
            self.speed[0] = -self.speed[0]
        if self.rect.top < LINETHICKNESS or self.rect.bottom > SCREEN_HEIGHT-LINETHICKNESS:
            pared=True
            self.speed[1] = -self.speed[1]
            if self.rect.bottom> SCREEN_HEIGHT-LINETHICKNESS:
                cae=True
        self.rect.move_ip((self.speed[0], self.speed[1]))
        return cae,pared
    def colision(self, objetivo):
        col=False
        if self.rect.colliderect(objetivo.rect):
            self.speed[1] = -self.speed[1]
            self.speed[0] = -self.speed[0]
            self.sonido_golpe.play()
            col=True

        return col

class Player(pygame.sprite.Sprite):
    "Define el comportamiento de las paletas de ambos jugadores"
    puntaje=0
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = 450

    def reiniciar(self, x):
        self.rect.centerx = x
        self.rect.centery = 450

    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT-LINETHICKNESS:#abajo
            self.rect.bottom = SCREEN_HEIGHT-LINETHICKNESS
        elif self.rect.top <= LINETHICKNESS:#arriba
            self.rect.top = LINETHICKNESS
        elif self.rect.left <=LINETHICKNESS: #izquierda
            self.rect.left=LINETHICKNESS
        elif self.rect.right >=SCREEN_WIDTH-LINETHICKNESS:#derecha
            self.rect.right= SCREEN_WIDTH-LINETHICKNESS
        elif self.rect.right>=SCREEN_WIDTH-LINETHICKNESS and self.rect.top <=LINETHICKNESS:#arriba-derecha
            self.rect.right= SCREEN_WIDTH-LINETHICKNESS
            self.rect.top = LINETHICKNESS
        elif self.rect.left<=LINETHICKNESS and self.rect.top <=LINETHICKNESS:#arriba-izquierda
            self.rect.left= LINETHICKNESS
            self.rect.top = LINETHICKNESS
        elif self.rect.right>=SCREEN_WIDTH-LINETHICKNESS and self.rect.bottom <=SCREEN_HEIGHT-LINETHICKNESS:#abajo-derecha
            self.rect.right= SCREEN_WIDTH-LINETHICKNESS
            self.rect.bottom = SCREEN_HEIGHT-LINETHICKNESS
        elif self.rect.left<=LINETHICKNESS and self.rect.bottom <=SCREEN_HEIGHT-LINETHICKNESS:#abajo-izquierda
            self.rect.left= LINETHICKNESS
            self.rect.bottom = SCREEN_HEIGHT-LINETHICKNESS

    def movimiento(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.centery -= 5
        elif keys[pygame.K_s]:
            self.rect.centery += 5
        elif keys[pygame.K_a]:
            self.rect.centerx -= 5
        elif keys[pygame.K_d]:
            self.rect.centerx += 5
    def movimiento2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.centery -= 5
        elif keys[pygame.K_DOWN]:
            self.rect.centery += 5
        elif keys[pygame.K_LEFT]:
            self.rect.centerx -= 5
        elif keys[pygame.K_RIGHT]:
            self.rect.centerx += 5
    def cpu(self, pelota):
        self.speed = [1,1]
        if self.rect.bottom >= SCREEN_HEIGHT-LINETHICKNESS:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= LINETHICKNESS:
            self.rect.top = LINETHICKNESS
        elif self.rect.left <=LINETHICKNESS:
            self.rect.left=LINETHICKNESS
        elif self.rect.right >=SCREEN_WIDTH-LINETHICKNESS:
            self.rect.right= SCREEN_WIDTH

        if pelota.speed[0] >= 0 and pelota.rect.centerx >= LINETHICKNESS or pelota.rect.centerx <=SCREEN_WIDTH-LINETHICKNESS:
            if self.rect.centerx > pelota.rect.centerx:
                self.rect.centerx -= self.speed[1]
            if self.rect.centerx < pelota.rect.centerx:
                self.rect.centerx += self.speed[1]

def dibujo():
        clock.tick(60)
        text="Score: "+str(jugador1.puntaje)
        text2="Score: "+str(jugador2.puntaje)
        mensaje = fuente.render(text, 1, (255, 255, 255))
        mensaje2 = fuente.render(text2, 1, (255, 255, 255))
        drawArena()
        PANTALLA.blit(mensaje, (30,40))
        PANTALLA.blit(mensaje2, (550,40))
        PANTALLA.blit(bola.image, bola.rect)
        PANTALLA.blit(jugador1.image, jugador1.rect)
        PANTALLA.blit(jugador2.image, jugador2.rect)
def drawArena():
    PANTALLA.fill(COLOR)
    #Draw outline of arena
    pygame.draw.rect(PANTALLA, WHITE, ((0,0),(SCREEN_WIDTH,SCREEN_HEIGHT)), LINETHICKNESS*2)

def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print "Error, no se puede cargar la imagen: ", ruta
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except pygame.error, message:
        print "No se pudo cargar el sonido:", ruta
        sonido = None
    return sonido


def reiniciar(jugador):
    jugador1.reiniciar(100)
    jugador2.reiniciar(700)
    bola.reiniciar(jugador)
def objetos():
    jugador1.humano()
    jugador1.movimiento()
    jugador2.humano()
    jugador2.movimiento2()
def main():
    global cont
    cont=0
    pygame.init()
    pygame.mixer.init()
    global PANTALLA
    PANTALLA=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Squash")
    global fuente
    fuente= pygame.font.Font("shanghai.ttf", 50)
    #fondo = load_image("fondo.jpg", IMG_DIR, alpha=False)
    sonido_golpe = load_sound("rebote.mp3", SONIDO_DIR)
    global jugador1
    jugador1= Player(100)
    global jugador2
    jugador2= Player (700)
    global bola
    bola= Pelota(sonido_golpe, jugador1)
    global clock
    clock = pygame.time.Clock()
    global muro
    muro=False
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    #pygame.mixer.music.load("cancion.mp3")
    #pygame.mixer.music.play(-1,0.0)
    salir=False
    juego=False
    turn1,turn2=True,False


    while salir!=True:
        objetos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir=True
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    salir=True
                if event.key==K_LSHIFT and turn1==True:
                    juego=True
                if event.key==K_RSHIFT and turn2==True:
                    juego=True
        if(turn1==True and juego==True):
            if(bola.colision(jugador1)):
                if(muro!=True and cont!=0):
                    print "Jugador 1 La Pelota la ha tocado a destiempo"
                    reiniciar(jugador2)
                    jugador2.puntaje+=1
                    turn1=False
                    turn2=True
                    juego=False
                    muro=False
                    cont=0
                else:
                    turn1=False
                    turn2=True
                    cont+=1
                    muro=False
            else:
                turn1=True
                turn2=False

        elif(turn2==True and juego==True):
            if(bola.colision(jugador2)):
                if(muro!=True and cont!=0):
                    print "Jugador 2 La Pelota la ha tocado a destiempo"
                    reiniciar(jugador1)
                    jugador1.puntaje+=1
                    turn2=False
                    turn1=True
                    juego=False
                    muro=False
                    cont=0
                else:
                    turn1=True
                    turn2=False
                    cont+=1
                    muro=False
            else:
                turn1=False
                turn2=True


        if(juego):
            cae,pared=bola.update(cont)
            if(cae):
                if(turn1==True and turn2==False):
                    print"La Pelota se le cayo al jugador 1"
                    reiniciar(jugador2)
                    jugador2.puntaje+=1
                    turn1=False
                    turn2=True
                    muro=False
                    cont=0
                    juego=False
                elif(turn2==True and turn1==False):
                    print "La Pelota se le cayo al jugador 2"
                    reiniciar(jugador1)
                    jugador1.puntaje+=1
                    turn1=True
                    turn2=False
                    muro=False
                    cont=0
                    juego=False

            else:
                #juego detenido, validar saque
                if(pared==True):
                    muro=True


        if(juego!=True):
            if(turn1==True):
                bola.reiniciar(jugador1)
            else:
                bola.reiniciar(jugador2)
        dibujo()
        pygame.display.flip()

    pygame.quit()
if __name__ == "__main__":
    main()