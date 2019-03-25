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

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 200
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR
MINIMO_Y_JUGADOR = 100
MAXIMO_Y_JUGADOR = ALTO_PANTALLA - MINIMO_Y_JUGADOR
MAXIMO_Y = -1000
MAXIMO_X = 3200

# -------------------------------------------------
# Clase Fase

class Agua(Escena):
    def __init__(self, director, xml):

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
        self.scrolly = 0
        self.distancia_scroll_derecha = ANCHO_PANTALLA/2
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)
        self.decorado = Decorado()
        # Creamos los sprites de los jugadores
        self.jugador = Jugador()
        self.jugador.keyUp_pulsada = False

        fullname = os.path.join('escenas', xml)
        self.xmldoc = parser_escena.parse(fullname)
        self.jugador.establecerPosicion(parser_escena.coordenadasPersonaje('Mike',self.xmldoc))

        # Creamos las plataformas
        listaPlataformas = parser_escena.listaCoordenadasPlataforma(self.xmldoc)
        self.grupoPlataformas = pygame.sprite.Group()
        for coordenadas in listaPlataformas:
            self.grupoPlataformas.add(Plataforma(coordenadas))

        # Creamos las paredes
        listaParedes = parser_escena.listaCoordenadasPared(self.xmldoc)
        self.grupoParedes = pygame.sprite.Group()
        for coordenadas in listaParedes:
            self.grupoParedes.add(Pared(coordenadas))

        # Creamos los enemigos comunes
        listaEnemigosComunes = parser_escena.listaCoordenadasPersonaje('EnemigoComun', self.xmldoc)
        self.grupoEnemigos = pygame.sprite.Group()
        for coordenadas in listaEnemigosComunes:
            enemigo = Enemigo()
            enemigo.establecerPosicion(coordenadas)
            self.grupoEnemigos.add(enemigo)

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador, self.grupoEnemigos)
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.grupoSpritesDinamicos, self.grupoPlataformas, self.grupoParedes)

    def actualizarScrollHorizontal(self, jugador):
        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if jugador.rect.left < MINIMO_X_JUGADOR:
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))
                
                return False# No se ha actualizado el scroll
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - desplazamiento

                return True; # Se ha actualizado el scroll
        
        # Si el jugador de la derecha se encuentra más allá del borde derecho
        if (jugador.rect.right > MAXIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= MAXIMO_X:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador.establecerPosicion((self.scrollx + MAXIMO_X_JUGADOR - jugador.rect.width, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll
            else:
                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento

                return True # Se ha actualizado el scroll

        # Si el jugador está en el limite de la pantalla
        return False

    def actualizarScrollVertical(self, jugador):
        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if jugador.rect.top < MINIMO_Y_JUGADOR:
            desplazamiento = MINIMO_Y_JUGADOR - jugador.rect.top

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrolly <= MAXIMO_Y:
                self.scrolly = MAXIMO_Y
                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador.establecerPosicion((jugador.posicion[0], MINIMO_Y_JUGADOR))
                
                return False# No se ha actualizado el scroll
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrolly = self.scrolly - desplazamiento

                return True; # Se ha actualizado el scroll
        
        # Si el jugador de la derecha se encuentra más allá del borde derecho
        if (jugador.rect.bottom > MAXIMO_Y_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.bottom - MAXIMO_Y_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrolly + ALTO_PANTALLA >= -MAXIMO_Y:
                self.scrolly = self.decorado.rect.bottom - ALTO_PANTALLA

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador.establecerPosicion((jugador.posicion[0], self.scrolly + MAXIMO_Y_JUGADOR - jugador.rect.height))

                return False; # No se ha actualizado el scroll
            else:
                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrolly = self.scrolly + desplazamiento

                return True # Se ha actualizado el scroll

        # Si el jugador está en el limite de la pantalla
        return False

    
    def actualizarScroll(self, jugador):
        cambioScroll = self.actualizarScrollHorizontal(jugador) or self.actualizarScrollVertical(jugador)

        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, self.scrolly))

            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrollx)

            

    def update(self,tiempo):
        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        if self.jugador.hp <= 0:
            self.director.salirPrograma()
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover(self.jugador)
        self.grupoSpritesDinamicos.update(tiempo, self.grupoPlataformas, self.grupoParedes, self.grupoEnemigos)
        self.actualizarScroll(self.jugador)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)


    def dibujar(self, pantalla):
        pantalla.fill((133,133,133))
        # Ponemos primero el fondo
        #self.fondo.dibujar(pantalla)
        # Después el decorado
        #self.decorado.dibujar(pantalla)
        # Luego los Sprites
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
            self.jugador.keyUp_pulsada = True
        # Una vez se suelta la tecla se actualiza la variable del jugador para que pueda realizar el segundo salto
        if (not teclasPulsadas[K_UP]) and self.jugador.keyUp_pulsada:
            self.jugador.keyUp_pulsada = False
            self.jugador.keyUp_suelta = True
        self.jugador.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_s, K_d)




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

class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('prueba.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (800, 600))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
