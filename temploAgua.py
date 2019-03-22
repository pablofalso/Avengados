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
MINIMO_X_JUGADOR = 0
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Agua(Escena):
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
        self.distancia_scroll_derecha = ANCHO_PANTALLA/2
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        fullname = os.path.join('escenas', 'agua.xml')
        self.xmldoc = parser_escena.parse(fullname)

        self.jugador1.establecerPosicion(parser_escena.coordenadasPersonaje('coordenada',self.xmldoc))
        self.jugador1.keyUp_pulsada = False
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        enemigo1 = Enemigo()
        enemigo1.establecerPosicion((1100, 300))

        # Creamos un grupo con los enemigos
        self.grupoEnemigos = pygame.sprite.Group( enemigo1 )

        plataforma1 = Plataforma(parser_escena.coordenadasPlataforma('plataforma1',self.xmldoc))
        plataforma2 = Plataforma(parser_escena.coordenadasPlataforma('plataforma2',self.xmldoc))
        plataforma3 = Plataforma(parser_escena.coordenadasPlataforma('plataforma3',self.xmldoc))
        plataforma4 = Plataforma(parser_escena.coordenadasPlataforma('plataforma4',self.xmldoc))
        plataforma5 = Plataforma(parser_escena.coordenadasPlataforma('plataforma5',self.xmldoc))
        plataforma6 = Plataforma(parser_escena.coordenadasPlataforma('plataforma6',self.xmldoc))
        plataforma7 = Plataforma(parser_escena.coordenadasPlataforma('plataforma7',self.xmldoc))
        pared1 = Pared(parser_escena.coordenadasPared('pared1',self.xmldoc))
        pared2 = Pared(parser_escena.coordenadasPared('pared2',self.xmldoc))
        pared3 = Pared(parser_escena.coordenadasPared('pared3',self.xmldoc))
        #pared4 = Pared(parser_escena.coordenadasPared('pared3',self.xmldoc))

        # y el grupo con las mismas
        self.grupoPlataformas = pygame.sprite.Group(plataforma1, plataforma2, plataforma3, plataforma4,plataforma5, plataforma6, plataforma7)
        self.grupoParedes = pygame.sprite.Group(pared1, pared2, pared3)
        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador1, enemigo1)
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.jugador1, plataforma1, plataforma2, plataforma3, plataforma4, plataforma5, plataforma6, plataforma7, pared1, pared2, pared3, enemigo1)
        self.grupoEnemigos = pygame.sprite.Group(enemigo1)


    # Devuelve True o False según se ha tenido que desplazar el scroll

    def actualizarScrollHorizontal(self,jugador1):
        if (jugador1.mirando == DERECHA and jugador1.rect.right >= ANCHO_PANTALLA/2):
            self.scrollx =  self.scrollx + 3
            return True
        if (jugador1.mirando == IZQUIERDA and jugador1.rect.left <= ANCHO_PANTALLA/2 and self.scrollx >=0):
            self.scrollx =  self.scrollx - 3
            return True
        return False

    def actualizarScroll(self, jugador1):
        cambioScroll = self.actualizarScrollHorizontal(jugador1)
        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, 0))


            # Ademas, actualizamos el decorado para que se muestre una parte distinta


    def update(self,tiempo):


        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover(self.jugador1)
        self.grupoSpritesDinamicos.update(tiempo, self.grupoPlataformas, self.grupoParedes, self.grupoEnemigos)
        self.actualizarScroll(self.jugador1)
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




#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
    def __init__(self,plataforma):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = plataforma[0]
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((plataforma[1], plataforma[2]))
        self.image.fill((0,0,0))


class Pared(MiSprite):
    def __init__(self,plataforma):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = plataforma[0]
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((plataforma[1], plataforma[2]))
        self.image.fill((0,0,0))
