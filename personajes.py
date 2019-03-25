import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *

HP = 3
CD_RECIBIRDANO = 1500
# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
ATAQUE = 5
DASH = 6
ATAQUE_DISTANCIA = 7

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO_SUBIENDO = 2
SPRITE_SALTANDO_BAJANDO = 3
SPRITE_ATAQUE_MELEE = 4
SPRITE_DASH = 5
SPRITE_ATAQUE_DISTANCIA = 6

VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
VELOCIDAD_DASH = 3 * VELOCIDAD_JUGADOR # Pixeles por milisegundo

RETARDO_ANIMACION_QUIETO = 10
RETARDO_ANIMACION_ANDANDO = 7
RETARDO_ANIMACION_SALTANDO_SUBIENDO = 7
RETARDO_ANIMACION_SALTANDO_BAJANDO = 7
RETARDO_ANIMACION_ATAQUE_MELEE = 4
RETARDO_ANIMACION_DASH = 7
RETARDO_ANIMACION_ATAQUE_DISTANCIA = 7

CD_DASH = 500 # En milisegundos
DURACION_DASH = 100 # En milisegundos


#Valores para el enemigo

ENEMIGO_MOVIENDOSE = 0
ENEMIGO_CAYENDO = 1
ENEMIGO_QUIETO = 2



# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0,0)
        self.velocidad = (0, 0)
        self.scroll = (0,0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def incrementarPosicion(self, incremento):
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((self.posicion[0]+incrementox, self.posicion[1]+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidadx*tiempo
        incrementoy = self.velocidady*tiempo
        self.incrementarPosicion((incrementox, incrementoy))

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly



class Jugador(MiSprite):
    "Jugador"
    def __init__(self):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self)
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen('MikeSprite.png',-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        self.hp = HP
        self.ultimo_golpe = 0
        # Lado hacia el que esta mirando
        self.mirando = DERECHA
        self.atacando = False
        self.dasheando = False
        self.velocidadx = 0
        self.scroll=(0,0)
        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas('mikedenadas.txt')
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [6,11,2,2,6,1,5]
        self.coordenadasHoja = []
        #for linea in range(0, n): para n movimientos
        for linea in range(0, 7):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # Variables para dobleSalto
        self.dobleSalto_desbloqueado = True
        # Es 'True' cuando ya se ha realizado el segundo salto, y se pone a 'False' al tocar el suelo
        self.dobleSalto_segundoSalto = False
        # Variable para controlar si se suelta la tecla de salto después de saltar por primera vez
        self.keyUp_suelta = False

        self.dash_desbloqueado = True
        # Variable para controlar el tiempo desde que se utilizó el último dash
        self.inicio_dash = 0

        self.atacando_distancia = False

        # La posicion inicial del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # La posicion x e y que ocupa

        # Velocidad en el eje y (para los saltos)
        #  En el eje x se utilizaria si hubiese algun tipo de inercia
        self.velocidady = 0

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            if self.numPostura == SPRITE_QUIETO:
                self.retardoMovimiento = RETARDO_ANIMACION_QUIETO
            elif self.numPostura == SPRITE_ANDANDO:
                self.retardoMovimiento = RETARDO_ANIMACION_ANDANDO
            elif self.numPostura == SPRITE_SALTANDO_SUBIENDO:
                self.retardoMovimiento = RETARDO_ANIMACION_SALTANDO_SUBIENDO
            elif self.numPostura == SPRITE_SALTANDO_BAJANDO:
                self.retardoMovimiento = RETARDO_ANIMACION_SALTANDO_BAJANDO
            elif self.numPostura == SPRITE_ATAQUE_MELEE:
                self.retardoMovimiento = RETARDO_ANIMACION_ATAQUE_MELEE
            elif self.numPostura == SPRITE_DASH:
                self.retardoMovimiento = RETARDO_ANIMACION_DASH
            elif self.numPostura == SPRITE_ATAQUE_DISTANCIA:
                self.retardoMovimiento = RETARDO_ANIMACION_ATAQUE_DISTANCIA
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == DERECHA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == IZQUIERDA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, ataque_melee, dash, ataque_distancia):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        # La animación de atacando no se puede interrumpir
        if self.atacando:
            if (self.numImagenPostura == 5):
                self.movimiento = QUIETO
                self.atacando = False
        # La animación de dasheando no se puede interrumpir
        elif self.dasheando:
            if (pygame.time.get_ticks() - self.inicio_dash > DURACION_DASH):
                self.movimiento = QUIETO
                self.dasheando = False
        elif self.atacando_distancia:
            if (self.numImagenPostura == 4):
                self.movimiento = QUIETO
                self.atacando_distancia = False
                BolaDeFuego(self.posicion[0], self.posicion[1])
        # Primero comprobamos la tecla del ataque_melee para poder atacar cuando vas corriendo
        # Así puedes atacar sin soltar las teclas de movimiento
        elif teclasPulsadas[ataque_melee]:
            # Si estás en el aire, no puedes atacar
            if not(self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO):
                self.numImagenPostura = 0
                self.movimiento = ATAQUE
                self.atacando = True
        elif teclasPulsadas[dash]:
            if self.dash_desbloqueado:
                # Si estás en el aire, no puedes dashear
                #if not(self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO):
                if pygame.time.get_ticks() - self.inicio_dash > CD_DASH:
                    self.movimiento = DASH
                    self.dasheando = True
                    self.inicio_dash = pygame.time.get_ticks()
        elif teclasPulsadas[ataque_distancia]:
            self.movimiento = ATAQUE_DISTANCIA
            self.atacando_distancia = True
            self.numImagenPostura = 0
        elif teclasPulsadas[arriba]:
            self.keyUp_pulsada = True
            # Si estamos en el aire y han pulsado arriba
            if self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO:
                # Si el doble salto esta desbloqueado, se ha soltado la tecla de saltar y vuelto a pulsar
                # y solo se ha realizado un salto sin tocar el suelo
                if self.dobleSalto_desbloqueado and self.keyUp_suelta and (not self.dobleSalto_segundoSalto):
                    self.movimiento = ARRIBA
                    self.dobleSalto_segundoSalto = True
                else:
                    self.movimiento =  QUIETO
            else:
                self.movimiento = ARRIBA
                self.keyUp_suelta = False
        elif teclasPulsadas[izquierda]:
            self.movimiento = IZQUIERDA
        elif teclasPulsadas[derecha]:
            self.movimiento = DERECHA
        else:
            self.movimiento = QUIETO



    def update(self, tiempo, grupoPlataformas, grupoParedes, grupoEnemigos):
        enemigos = pygame.sprite.spritecollideany(self, grupoEnemigos)
        if enemigos != None:
            if self.movimiento != ATAQUE and pygame.time.get_ticks() - self.ultimo_golpe > CD_RECIBIRDANO:
                self.ultimo_golpe = pygame.time.get_ticks()
                self.hp -= 1
                if self.hp == 0:
                    print('LA PALMASTE BOY')
        if self.posicion[0] <= 0:
            self.establecerPosicion((2, self.posicion[1]))
        if self.posicion[0] > 3200:
            print("LOGICO")
            self.establecerPosicion((3200, self.posicion[1]))
        plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
        pared  = pygame.sprite.spritecollideany(self, grupoParedes)
        #Primero se mira si está encima de una plataforma, si no está cae
        if plataforma == None:
            self.numPostura = SPRITE_SALTANDO_BAJANDO
        #Si esta colisionando entonces para
        elif ((plataforma.rect.bottom >= self.rect.top and self.velocidady > 0)):
            self.velocidady = 0
            self.numPostura = SPRITE_QUIETO
            self.establecerPosicion((self.posicion[0], plataforma.posicion[1]))
        if pared != None:
            if (self.mirando == IZQUIERDA):
                self.establecerPosicion((pared.posicion[0]+5, self.posicion[1]))
            else:
                if (self.posicion[0] < pared.posicion[0]):
                    self.establecerPosicion((pared.posicion[0]-45, self.posicion[1]))
        if self.movimiento == IZQUIERDA or self.movimiento == DERECHA:
            if not (self.numPostura == SPRITE_SALTANDO_SUBIENDO) and not (self.numPostura == SPRITE_SALTANDO_BAJANDO):
                self.numPostura = SPRITE_ANDANDO
            self.mirando = self.movimiento
            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                self.velocidadx = -0.2
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                self.velocidadx = 0.2
        if self.movimiento == ARRIBA:
            self.numPostura = SPRITE_SALTANDO_SUBIENDO
            self.velocidady = -0.3

        if (self.numPostura == SPRITE_SALTANDO_SUBIENDO) or (self.numPostura == SPRITE_SALTANDO_BAJANDO):
            self.velocidady += 0.008
            if self.velocidady > 0:
                self.numPostura == SPRITE_SALTANDO_BAJANDO
        if self.movimiento == QUIETO :
            if self.numPostura != SPRITE_SALTANDO_SUBIENDO and self.numPostura != SPRITE_SALTANDO_BAJANDO :
                self.numPostura = SPRITE_QUIETO
                self.dobleSalto_segundoSalto = False
            self.velocidadx = 0
        if self.movimiento == ATAQUE:
               self.numPostura = SPRITE_ATAQUE_MELEE
               enemigo = pygame.sprite.spritecollideany(self, grupoEnemigos)
               if (enemigo != None):
                   #enemigo.numPostura = 1
                   enemigo.kill()
               self.velocidadx = 0
        if self.movimiento == DASH:
            self.numPostura = SPRITE_DASH
            self.retardoMovimiento = -1
            if self.mirando == DERECHA:
                self.velocidadx = 1
            else:
                self.velocidadx = -1
        if self.movimiento == ATAQUE_DISTANCIA:
            self.velocidadx = 0
            self.numPostura = SPRITE_ATAQUE_DISTANCIA

        self.actualizarPostura()
        MiSprite.update(self,tiempo)
        return


#Empieza la clase del enemigo
class Enemigo(MiSprite):
    "Enemigo"
    def __init__(self):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self)
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen('EnemigoBasico.png',-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = ENEMIGO_MOVIENDOSE
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA
        self.atacando = False
        self.dasheando = False
        self.empezar_andar = 0
        self.velocidadx = 0
        self.scroll=(0,0)
        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas('coordenadasEnemigoBasico.txt')
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [10,4,6,6]
        self.coordenadasHoja = []
        #for linea in range(0, n): para n movimientos
        for linea in range(0, 4):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # En que postura esta inicialmente
        self.numPostura = ENEMIGO_MOVIENDOSE

        # La posicion inicial del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # La posicion x e y que ocupa

        # Velocidad en el eje y (para los saltos)
        #  En el eje x se utilizaria si hubiese algun tipo de inercia
        self.velocidady = 0

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva posturaQUIETO
        if (self.retardoMovimiento < 0):
            if self.numPostura == ENEMIGO_QUIETO:
                self.retardoMovimiento = RETARDO_ANIMACION_QUIETO
            elif self.numPostura == ENEMIGO_MOVIENDOSE:
                self.retardoMovimiento = 2
            elif self.numPostura == ENEMIGO_CAYENDO:
                self.retardoMovimiento = 10
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == DERECHA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == IZQUIERDA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def mover(self, jugador):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        # La animación de atacando no se puede interrumpir
        if (pygame.sprite.collide_rect(self, jugador)):
            if jugador.movimiento == ATAQUE:
                self.remove()
        if (abs(self.posicion[0]-jugador.posicion[0]) <= 200):
            if (self.posicion[0] > jugador.posicion[0]):
                self.mirando = IZQUIERDA
                self.movimiento = IZQUIERDA
            else:
                self.mirando = DERECHA
                self.movimiento = DERECHA
        elif (abs(self.posicion[0]-jugador.posicion[0]) <= 10):
            if (self.posicion[0] > jugador.posicion[0]):
                self.mirando = IZQUIERDA
                self.movimiento = IZQUIERDA
            else:
                self.mirando = DERECHA
                self.movimiento = DERECHA
            #self.movimiento = ATAQUE_ENEMIGO
        else:
            if (pygame.time.get_ticks() - self.empezar_andar >= 1000):
                if self.mirando == 1:
                    self.mirando = DERECHA
                    self.movimiento = DERECHA
                else:
                    self.mirando = IZQUIERDA
                    self.movimiento = IZQUIERDA
                self.empezar_andar = pygame.time.get_ticks()




    def update(self, tiempo, grupoPlataformas, grupoParedes,grupoEnemigos):
        plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
        pared  = pygame.sprite.spritecollideany(self, grupoParedes)
        #Primero se mira si está encima de una plataforma, si no está cae
        if plataforma == None:
            self.numPostura = ENEMIGO_CAYENDO
        #Si esta colisionando entonces para
        elif ((plataforma.rect.bottom >= self.rect.top and self.velocidady > 0)):
            self.velocidady = 0
            self.numPostura = SPRITE_QUIETO
            self.establecerPosicion((self.posicion[0], plataforma.posicion[1]))
        if pared != None:
            if (self.mirando == IZQUIERDA):
                self.establecerPosicion((pared.posicion[0]+5, self.posicion[1]))
            else:
                if (self.posicion[0] < pared.posicion[0]):
                    self.establecerPosicion((pared.posicion[0]-45, self.posicion[1]))
        if self.movimiento == IZQUIERDA or self.movimiento == DERECHA:
            if not (self.numPostura == ENEMIGO_CAYENDO):
                self.numPostura = ENEMIGO_MOVIENDOSE
            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                self.velocidadx = -0.1
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                self.velocidadx = 0.1
        if self.numPostura == ENEMIGO_CAYENDO:
            self.velocidady+=0.008


        self.actualizarPostura()
        MiSprite.update(self,tiempo)
        return

class BolaDeFuego(pygame.sprite.Sprite):
    "BolaDeFuego"
    def __init__(self, posicionx, posiciony):
        print("fireball")
