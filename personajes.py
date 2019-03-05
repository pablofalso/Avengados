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

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO_SUBIENDO = 2
SPRITE_SALTANDO_BAJANDO = 3
SPRITE_ATAQUE_MELEE = 4

VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura
RETARDO_ANIMACION_QUIETO = 10
RETARDO_ANIMACION_ANDANDO = 7
RETARDO_ANIMACION_SALTANDO_SUBIENDO = 7
RETARDO_ANIMACION_SALTANDO_BAJANDO = 7
RETARDO_ANIMACION_ATAQUE_MELEE = 4

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
        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas('coordenadas.txt')
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [6,11,2,2,5]
        self.coordenadasHoja = []
        #for linea in range(0, n): para n movimientos
        for linea in range(0, 5):
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

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, ataque_melee):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        # La animación de atacando no se puede interrumpir
        if self.atacando:
            if (pygame.time.get_ticks() - self.inicio_ataque > 450):
                self.movimiento = QUIETO
                self.atacando = False
        # Primero comprobamos la tecla del ataque_melee para poder atacar cuando vas corriendo
        # Así puedes atacar sin soltar las teclas de movimiento
        elif teclasPulsadas[ataque_melee]:
            # Si estás en el aire, no puedes atacar
            if self.movimiento != ARRIBA:
                # Se pone numImagenPostura a 0 porque me da la sensación de que a veces la animación empieza por la mitad
                self.numImagenPostura = 0
                self.movimiento = ATAQUE
                self.inicio_ataque = pygame.time.get_ticks()
                self.atacando = True
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
            if not (self.numPostura == SPRITE_SALTANDO_SUBIENDO or self.numPostura == SPRITE_SALTANDO_BAJANDO):
                self.numPostura = SPRITE_ATAQUE_MELEE
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

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()
        return
