import pygame
import sys
import os
from pygame.locals import *

blanco=(255,255,255)
negro=(0,0,0)
rojo=(255,0,0)
WIDTH=800
HEIGHT=500
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Squash')
reloj=pygame.time.Clock()
FPS=40
font = pygame.font.SysFont(None,20)

class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    def update(self):
        self.left,self.top=pygame.mouse.get_pos()

class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,x=500,y=100):
        self.imagen_normal=imagen1
        #self.imagen_seleccion=imagen2
        self.imagen_actual=self.imagen_normal
        self.rect=self.imagen_actual.get_rect()
        self.rect.left,self.rect.top=(x,y)

    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual=self.imagen_normal
        else: self.imagen_actual=self.imagen_normal

        pantalla.blit(self.imagen_actual,self.rect)

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

def creditos():
    cred=pygame.display.set_mode((800,500))
    fondo1=load_image("cred.jpg", "imagenes", alpha=False)
    reloj1=pygame.time.Clock()
    img1=pygame.image.load("imagenes/button5.png")
    prev=Boton(img1,650,430)
    cursor1=Cursor()
    bandera2=False

    while bandera2!=True:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(prev.rect):
                    bandera2=True
        reloj1.tick(40)
        cred.blit(fondo1, (0, 0))
        cursor1.update()
        prev.update(cred,cursor1)
        pygame.display.update()

def instrucciones():
    menu=pygame.display.set_mode((800,500))
    fondo1=load_image("inst.jpg", "imagenes", alpha=False)
    reloj1=pygame.time.Clock()
    img1=pygame.image.load("imagenes/button5.png")
    prev=Boton(img1,620,410)
    cursor1=Cursor()
    bandera=False

    while bandera!=True:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(prev.rect):
                    bandera=True
        reloj1.tick(40)
        menu.blit(fondo1, (0, 0))
        cursor1.update()
        prev.update(menu,cursor1)
        pygame.display.update()

def squash(bool):
    cpu=bool
    COLOR=(48,197,117)
    WHITE=(255,255,255)
    RED=(255,0,0)
    LINETHICKNESS = 15
    IMG_DIR="imagenes"
    SCREEN_WIDTH=800
    SCREEN_HEIGHT=500
    SONIDO_DIR="sonidos"
    class Pelota(pygame.sprite.Sprite):
        "La bola y su comportamiento en la pantalla"

        def __init__(self,sonido_golpe, jugador):

            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("bola.png", IMG_DIR, alpha=True)
            self.rect = self.image.get_rect()
            self.rect.centerx = jugador.rect.centerx
            self.rect.centery = jugador.rect.centery
            self.speed = [22,22]
            self.sonido_golpe = sonido_golpe

        def velocidad(self):
            new=self.speed[1]
            self.speed=[new-1,new-1]
        def reiniciar(self, jugador):
            jugador.humano2()
            self.rect.centerx = jugador.rect.centerx
            self.rect.centery = jugador.rect.centery
            self.speed = [2, 2]

        def update(self):
            x1=bola.rect.centerx
            y1=bola.rect.centery
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
            x2=bola.rect.centerx
            y2=bola.rect.centery
            return cae,pared,x1,y1,x2,y2
        def colision(self, objetivo):
            col=False
            if self.rect.colliderect(objetivo.rect):
                self.speed[1] = -self.speed[1]
                self.speed[0] = self.speed[0]
                self.sonido_golpe.play()
                col=True

            return col

    class Player(pygame.sprite.Sprite):
        "Define el comportamiento de las paletas de ambos jugadores"
        puntaje=0
        def __init__(self, x):
            pygame.sprite.Sprite.__init__(self)
            if(x>500):
                self.image = load_image("paleta2.png", IMG_DIR, alpha=True)
            else:
                self.image = load_image("paleta.png", IMG_DIR, alpha=True)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = 350


        def reiniciar(self, x):
            self.rect.centerx = x
            self.rect.centery = 350

        def humano(self):
            # Controlar que la paleta no salga de la pantalla
            if self.rect.bottom >= SCREEN_HEIGHT-LINETHICKNESS:#abajo
                self.rect.bottom = SCREEN_HEIGHT-LINETHICKNESS
            elif self.rect.top <= 250:#arriba
                self.rect.top = 250
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

        def humano2(self):
            # Controlar que la paleta no salga de la pantalla
            if self==jugador1:
                if self.rect.bottom >= 400:#abajo
                    self.rect.bottom = 400
                elif self.rect.top <= 250:#arriba
                    self.rect.top = 250
                elif self.rect.left <=LINETHICKNESS: #izquierda
                    self.rect.left=LINETHICKNESS
                elif self.rect.right >=215:#derecha
                    self.rect.right= 215
            elif self==jugador2:
                if self.rect.bottom >= 400:#abajo
                    self.rect.bottom = 400
                elif self.rect.top <= 250:#arriba
                    self.rect.top = 250
                elif self.rect.left <=585: #izquierda
                    self.rect.left=585
                elif self.rect.right >=785:#derecha
                    self.rect.right= 785

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
        def cpu(self, xbuscar):
            self.speed = [6,6]

            if self.rect.bottom >= SCREEN_HEIGHT-LINETHICKNESS:#abajo
                self.rect.bottom = SCREEN_HEIGHT-LINETHICKNESS
            elif self.rect.top <= LINETHICKNESS:#arriba
                self.rect.top = LINETHICKNESS
            elif self.rect.left <=LINETHICKNESS: #izquierda
                self.rect.left=LINETHICKNESS
            elif self.rect.right >=SCREEN_WIDTH-LINETHICKNESS:#derecha
                self.rect.right= SCREEN_WIDTH-LINETHICKNESS
            if(xbuscar!=False):
                if xbuscar >= 0 and xbuscar >= LINETHICKNESS or xbuscar <=SCREEN_WIDTH-LINETHICKNESS:
                    if self.rect.centerx > xbuscar:
                        self.rect.centerx -= self.speed[1]
                    if self.rect.centerx < xbuscar:
                        self.rect.centerx += self.speed[1]


    def dibujo():
            clock.tick(60)
            textM="Press M to return the menu"
            text="Score: "+str(jugador1.puntaje)
            text2="Score: "+str(jugador2.puntaje)
            mensaje = fuente.render(text, 1, (255, 255, 255))
            mensaje2 = fuente.render(text2, 1, (255, 255, 255))
            mensaje3=font.render(textM,1,(255,255,255))
            drawArena()
            PANTALLA.blit(mensaje, (40,40))
            PANTALLA.blit(mensaje2, (580,40))
            PANTALLA.blit(mensaje3, (320,20))
            PANTALLA.blit(bola.image, bola.rect)
            PANTALLA.blit(jugador1.image, jugador1.rect)
            PANTALLA.blit(jugador2.image, jugador2.rect)
            #Lineas
            pygame.draw.line(PANTALLA, (193, 82, 38), (15, 250), (785, 250), 4)
            pygame.draw.line(PANTALLA, (193, 82, 38), (400, 250), (400, 485), 4)
            pygame.draw.line(PANTALLA, (193, 82, 38), (15, 400), (215, 400), 4)
            pygame.draw.line(PANTALLA, (193, 82, 38), (585, 400), (785, 400), 4)
            pygame.draw.line(PANTALLA, (193, 82, 38), (215, 250), (215, 400), 4)
            pygame.draw.line(PANTALLA, (193, 82, 38), (585, 250), (585, 400), 4)

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
        if cpu:
            if juego==True:
                jugador1.humano()
                jugador1.movimiento()
            else:
                jugador1.humano2()
                jugador1.movimiento()

        else:
            jugador1.humano()
            jugador1.movimiento()
            jugador2.humano()
            jugador2.movimiento2()
    def regresioncpu():
        xi=[x1,x2]
        yi=[y1,y2]
        n=len(xi)
        mult, sum1,sumax,sumay,=0,0,0,0
        for i in range (n):
            sumax+=xi[i]
            sumay+=yi[i]
            mult+=xi[i]*yi[i]
            sum1+=xi[i]**2
        expo=sumax**2
        a1=(n*mult-(sumax*sumay))/(n*sum1-expo)
        xmedia=sumax/n
        ymedia=sumay/n
        a0=ymedia-(a1*xmedia)
        xbuscar=(350-a0)/a1
        return xbuscar

    def regresion():
        xi=[x1,x2]
        yi=[y1,y2]
        n=len(xi)
        mult, sum1,sumax,sumay,=0,0,0,0
        for i in range (n):
            sumax+=xi[i]
            sumay+=yi[i]
            mult+=xi[i]*yi[i]
            sum1+=xi[i]**2
        expo=sumax**2
        a1=(n*mult-(sumax*sumay))/(n*sum1-expo)
        xmedia=sumax/n
        ymedia=sumay/n
        a0=ymedia-(a1*xmedia)

        for m in range(15,785):
            y=a0+a1*m
            if(y>=485):
                continue
            elif(y<=15):
                continue
            pygame.draw.line(PANTALLA,RED, (m,y),(m,y), 1)

        pygame.display.update()
    def terminar():
        var=True
        if jugador1.puntaje==10 or jugador2.puntaje==10:

            print "puntaje"
            print jugador1.puntaje
            if jugador1.puntaje==10:
                text="Felicidades Jugador 1, HA GANADO"
                mensaje = fuente.render(text, 1, (255, 255, 255))
                PANTALLA.blit(mensaje, (0,HEIGHT/2))
                pygame.display.update()
                var=False
            else:
                text="Felicidades Jugador 2, HA GANADO"
                mensaje = fuente.render(text, 1, (255, 255, 255))
                PANTALLA.blit(mensaje, (0,HEIGHT/2))
                pygame.display.update()
                var=False

        return var

    def main():
        global x1,y1,x2,y2
        x1,y1,x2,y2=0,0,0,0
        global cont
        global juego
        juego=False
        cont=0
        pygame.init()
        pygame.mixer.init()
        global PANTALLA
        PANTALLA=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Squash")
        global fuente
        fuente= pygame.font.Font("letra2.ttf", 40)
        sonido_golpe = load_sound("rebote.mp3", SONIDO_DIR)
        global jugador1
        jugador1= Player(100)
        global jugador2
        jugador2= Player (700)
        global bola
        bola= Pelota(sonido_golpe, jugador1)
        jugador2.cpu(False)
        global clock
        clock = pygame.time.Clock()
        global muro
        muro=False
        pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
        #pygame.mixer.music.load("cancion.mp3")
        #pygame.mixer.music.play(-1,0.0)
        salir=False

        turn1,turn2=True,False

        while salir!=True:
            terminar()
            objetos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir=True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        salir=True
                    if event.key==K_LSHIFT and turn1==True:
                        juego=True
                    if(cpu!=True):
                        if event.key==K_RSHIFT and turn2==True:
                            juego=True
                    if event.key==K_m: #regresar al menu
                        gameLoop()

            if(turn1==True and juego==True):
                if(bola.colision(jugador1)):
                    if(muro!=True and cont!=0):
                        print "Jugador 1 La Pelota la ha tocado a destiempo"
                        reiniciar(jugador2)
                        jugador2.puntaje+=1
                        if jugador2.puntaje==10:
                            juego=terminar()
                        else:
                            turn1=False
                            turn2=True
                            juego=False
                            muro=False
                            cont=0

                    else:
                        bola.velocidad()
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
                        if jugador1.puntaje==10:
                            juego=terminar()
                        else:
                            turn2=False
                            turn1=True
                            juego=False
                            muro=False
                            cont=0

                    else:
                        bola.velocidad()
                        turn1=True
                        turn2=False
                        cont+=1
                        muro=False
                else:
                    turn1=False
                    turn2=True

            if juego==True:
                cae,pared,x1,y1,x2,y2=bola.update()

                if cpu:
                    if(turn2==True):
                        jugador2.cpu(regresioncpu())
                else:
                    regresion()

                if cae:
                    if(turn1==True and turn2==False):
                        print"La Pelota se le cayo al jugador 1"
                        reiniciar(jugador2)
                        jugador2.puntaje+=1
                        if jugador2.puntaje==10:
                            juego=terminar()
                        else:
                            turn1=False
                            turn2=True
                            muro=False
                            cont=0
                            juego=False
                        if cpu:
                            juego=True
                    elif(turn2==True and turn1==False):
                        print "La Pelota se le cayo al jugador 2"
                        reiniciar(jugador1)
                        jugador1.puntaje+=1
                        if jugador1.puntaje==10:
                            juego=terminar()
                        else:
                            turn1=True
                            turn2=False
                            muro=False
                            cont=0
                            juego=False
                else:
                    if(pared==True):
                        muro=True
            elif(juego!=True):
                jugador1.humano2()
                jugador2.humano2()
                #juego detenido, validar saque
                if(turn1==True):
                    x1=bola.rect.centerx
                    y1=bola.rect.centery
                    bola.reiniciar(jugador1)
                else:
                    x1=bola.rect.centerx
                    y1=bola.rect.centery
                    bola.reiniciar(jugador2)
                    if(cpu):
                        juego=True

            dibujo()
            pygame.display.update()

    if __name__ == "__main__":
        main()

def gameLoop():
    salir=False
    nuevo=False
    while salir!=True:
        while nuevo==True:

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_m:
                        gameLoop()
                    if event.key==pygame.K_q:
                        salir=True
                        nuevo=False
                if event.type == pygame.QUIT:
                    salir=True
                    nuevo=False

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton1.rect):
                    print "1 player"
                    squash(True)
                if cursor1.colliderect(boton2.rect):
                    print "multiplayer"
                    squash(False)
                if cursor1.colliderect(boton3.rect):
                    print "instructions"
                    instrucciones()
                if cursor1.colliderect(boton4.rect):
                    print "credits"
                    creditos()

            if event.type == pygame.QUIT:
                salir=True

        img1=pygame.image.load("imagenes/button.png")
        img2=pygame.image.load("imagenes/button2.png")
        img3=pygame.image.load("imagenes/button3.png")
        img4=pygame.image.load("imagenes/button4.png")

        boton1=Boton(img1,600,120)
        boton2=Boton(img2,590,185)
        boton3=Boton(img3,578,250)
        boton4=Boton(img4,600,315)
        cursor1=Cursor()
        fondo1=load_image("back1.jpg", "imagenes", alpha=False)
        screen.blit(fondo1, (0, 0))
        cursor1.update()
        boton1.update(screen,cursor1)
        boton2.update(screen, cursor1)
        boton3.update(screen, cursor1)
        boton4.update(screen, cursor1)
        pygame.display.update()
        reloj.tick(FPS)
    pygame.quit()
    quit()

gameLoop()