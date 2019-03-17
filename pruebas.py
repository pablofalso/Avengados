# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
import parser_escena

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
    def __init__(self, director):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)

        # Creamos el decorado y el fondo
        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        fullname = os.path.join('escenas', 'test.xml')
        self.xmldoc = parser_escena.parse(fullname)

        self.jugador1.establecerPosicion(parser_escena.coordenadasPersonaje('coordenada',self.xmldoc))
        self.jugador1.keyUp_pulsada = False
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador1)
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.jugador1)


    def update(self,tiempo):


        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        self.jugador1.update(tiempo)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)


    def dibujar(self, pantalla):
        pantalla.fill((133,133,133))
        self.grupoSprites.draw(pantalla)


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        if teclasPulsadas[K_UP]:
            self.jugador1.keyUp_pulsada = True
        # Una vez se suelta la tecla se actualiza la variable del jugador para que pueda realizar el segundo salto
        if (not teclasPulsadas[K_UP]) and self.jugador1.keyUp_pulsada:
            self.jugador1.keyUp_pulsada = False
            self.jugador1.keyUp_suelta = True
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_s, K_d)
