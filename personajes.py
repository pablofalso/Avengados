import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *

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

CD_DASH = 1000 # En milisegundos
DURACION_DASH = 100 # En milisegundos
class Jugador(pygame.sprite.Sprite):
    "Jugador"

    def __init__(self):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self)
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen('MikeSprite.png',-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA
        self.atacando = False
        self.dasheando = False
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
        self.posicionx = 300
        self.posiciony = 300
        self.rect.left = self.posicionx
        self.rect.bottom = self.posiciony
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
                BolaDeFuego(self.posicionx, self.posiciony)
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
                if not(self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO): 
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



    def update(self, tiempo):
        # Si vamos a la izquierda
        if self.movimiento == IZQUIERDA:
            # Si no estamos en el aire, la postura actual sera estar caminando
            if not (self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO):
                self.numPostura = SPRITE_ANDANDO
            # Esta mirando a la izquierda
            self.mirando = IZQUIERDA
            # Actualizamos la posicion
            self.posicionx -= VELOCIDAD_JUGADOR * tiempo
            self.rect.left = self.posicionx
        # Si vamos a la derecha
        elif self.movimiento == DERECHA:
            # Si no estamos en el aire, la postura actual sera estar caminando
            if not (self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO):
                self.numPostura = SPRITE_ANDANDO
            # Esta mirando a la derecha
            self.mirando = DERECHA
            # Actualizamos la posicion
            self.posicionx += VELOCIDAD_JUGADOR * tiempo
            self.rect.left = self.posicionx
        # Si estamos saltando
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO_SUBIENDO
            # Le imprimimos una velocidad en el eje y
            self.velocidady = VELOCIDAD_SALTO_JUGADOR
        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not (self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO):
                self.numPostura = SPRITE_QUIETO
        elif self.movimiento == ATAQUE:
               self.numPostura = SPRITE_ATAQUE_MELEE
        elif self.movimiento == DASH:
            self.numPostura = SPRITE_DASH
            self.retardoMovimiento = -1
        elif self.movimiento == ATAQUE_DISTANCIA:
            self.numPostura = SPRITE_ATAQUE_DISTANCIA

        # Si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO:
            # Actualizamos la posicion
            self.posiciony -= self.velocidady * tiempo
            # Si llegamos a la posicion inferior, paramos de caer y lo ponemos como quieto
            if (self.posiciony>300):
                self.numPostura = SPRITE_QUIETO
                # Se actualiza la variable para controlar si se ha realizado el segundo salto
                self.dobleSalto_segundoSalto = False
                self.posiciony = 300
                self.velocidady = 0
            # Si no, aplicamos el efecto de la gravedad
            else:
                self.velocidady -= 0.008
                if self.velocidady <= 0:
                    self.numPostura = SPRITE_SALTANDO_BAJANDO
            # Nos ponemos en esa posicion en el eje y
            self.rect.bottom = self.posiciony
        elif self.numPostura == SPRITE_DASH:
            # Actualizamos la posicion
            if self.mirando == IZQUIERDA:
                self.posicionx -= VELOCIDAD_DASH * tiempo
            else:
                self.posicionx += VELOCIDAD_DASH * tiempo
            self.rect.left = self.posicionx

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()
        return

class BolaDeFuego(pygame.sprite.Sprite):
    "BolaDeFuego"
    def __init__(self, posicionx, posiciony):
        print("fireball")