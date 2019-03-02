# -*- coding: utf-8 -*-

# -------------------------------------------------
# Importar las librerías
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *

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
ATAQUE_MELEE = 4

VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura
RETARDO_ANIMACION_QUIETO = 10
RETARDO_ANIMACION_ANDANDO = 7
RETARDO_ANIMACION_SALTANDO_SUBIENDO = 7
RETARDO_ANIMACION_SALTANDO_BAJANDO = 7

# -------------------------------------------------
# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
class GestorRecursos(object):
    recursos = {}

    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except (pygame.error, message) as error:
                print ('Cannot load image:', fullname)
                raise (SystemExit, message)
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('imagenes', nombre)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------

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
            elif self.numPostura == ATAQUE_MELEE:
                self.retardoMovimiento = 4
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
        if teclasPulsadas[arriba]:
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
        elif teclasPulsadas[ataque_melee]:
            self.movimiento = ATAQUE
            self.inicio_ataque = pygame.time.get_ticks()
            self.atacando = True
        elif self.atacando:
            if (pygame.time.get_ticks() - self.inicio_ataque > 350):
                self.movimiento = QUIETO
                self.atacando = False
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
                self.numPostura = ATAQUE_MELEE
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




# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((800, 600), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Poner el título de la ventana
    pygame.display.set_caption('Avengados')

    # Creamos el objeto jugador
    jugador = Jugador()

    # Creamos el grupo de Sprites de jugadores
    grupoJugadores = pygame.sprite.Group( jugador)

    # Variable para controlar que se ha pulsado la tecla para luego comprobar que se ha soltado
    keyUp_pulsada = False

    # El bucle de eventos
    while True:

        # Hacemos que el reloj espere a un determinado fps
        tiempo_pasado = reloj.tick(60)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

         # Miramos que teclas se han pulsado
        teclasPulsadas = pygame.key.get_pressed()

        # Si la tecla es Escape
        if teclasPulsadas[K_ESCAPE]:
            # Se sale del programa
            pygame.quit()
            sys.exit()
        
        # Controlamos que para realizar el segundo salto se suelte la tecla de saltar antes de repetir el salto
        if teclasPulsadas[K_UP]:
            keyUp_pulsada = True
        # Una vez se suelta la tecla se actualiza la variable del jugador para que pueda realizar el segundo salto
        if (not teclasPulsadas[K_UP]) and keyUp_pulsada:
            keyUp_pulsada = False
            jugador.keyUp_suelta = True

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        jugador.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT,K_a)


        # Actualizamos los jugadores actualizando el grupo
        grupoJugadores.update(tiempo_pasado)

        # Dibujar el fondo de color
        pantalla.fill((133,133,133))

        # Dibujar el grupo de Sprites
        grupoJugadores.draw(pantalla)

        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main()
