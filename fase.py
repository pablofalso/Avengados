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

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
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


        fullname = os.path.join('escenas', xml)
        self.xmldoc = parser_escena.parse(fullname)
        self.textura = parser_escena.texturas(self.xmldoc)
        self.limitex, self.limitey = parser_escena.limites(self.xmldoc)
        self.limite_inferior = Plataforma([pygame.Rect(0, self.limitey, self.limitex, 5),self.limitex, 5], self.textura)
        self.limite_derecha = Pared([pygame.Rect(self.limitex, 0, 5, self.limitey),5, self.limitey])
        self.fondo = parser_escena.decorado(self.xmldoc)
        self.decorado = Decorado(self.fondo)


        # Creamos los sprites de los jugadores
        self.jugador = Jugador(self.limite_inferior)
        self.jugador.keyUp_pulsada = False
        self.jugador.establecerPosicion(parser_escena.coordenadasPersonaje('Mike',self.xmldoc))

        # Creamos las plataformas
        listaPlataformas = parser_escena.listaCoordenadasPlataforma(self.xmldoc)
        self.grupoPlataformas = pygame.sprite.Group()
        for coordenadas in listaPlataformas:
            self.grupoPlataformas.add(Plataforma(coordenadas, self.textura))

        listaSuelo = parser_escena.listaCoordenadasSuelo(self.xmldoc)
        self.grupoSuelo = pygame.sprite.Group()
        for coordenadas in listaSuelo:
            self.grupoPlataformas.add(Suelo(coordenadas))

        listaRelleno = parser_escena.listaCoordenadasRelleno(self.xmldoc)
        self.grupoRelleno = pygame.sprite.Group()
        for coordenadas in listaRelleno:
            self.grupoPlataformas.add(Relleno(coordenadas, self.textura))

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

        listaUpgradesVida = parser_escena.coordenadasUpgrades('vida', self.xmldoc)
        self.grupoUpgradeVida = pygame.sprite.Group()
        for coordenadas in listaUpgradesVida:
            self.grupoUpgradeVida.add(UpgradeVida(coordenadas))

        listaUpgradesDano = parser_escena.coordenadasUpgrades('daño', self.xmldoc)
        self.grupoUpgradeDano = pygame.sprite.Group()
        for coordenadas in listaUpgradesDano:
            self.grupoUpgradeDano.add(UpgradedeDano(coordenadas))



        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador, self.grupoEnemigos)
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.grupoSpritesDinamicos, self.grupoPlataformas, self.grupoParedes, self.grupoSuelo, self.grupoUpgradeVida, self.grupoUpgradeDano)
        self.grupoBolasDeFuego = pygame.sprite.Group()


    def actualizarScrollHorizontal(self,jugador, tiempo):
       if (jugador.mirando == DERECHA and jugador.rect.right >= ANCHO_PANTALLA/2 and jugador.posicion[0] <= 3200 - ANCHO_PANTALLA/2):
           self.scrollx =  self.scrollx + jugador.velocidadx * tiempo
           return True
       if (jugador.mirando == IZQUIERDA and jugador.rect.left <= ANCHO_PANTALLA/2 and self.scrollx >=0 and jugador.posicion[0] >= ANCHO_PANTALLA/2):
           self.scrollx =  self.scrollx + jugador.velocidadx * tiempo
           return True
       return False

    def actualizarScrollVertical(self, jugador, tiempo):
        if (jugador.rect.bottom >= ALTO_PANTALLA/2):
            self.scrolly =  self.scrolly + (jugador.velocidady * tiempo)
            return True
        if (jugador.rect.top <= ALTO_PANTALLA/2 and self.scrolly > 0):
            self.scrolly =  self.scrolly + (jugador.velocidady * tiempo)
            return True

        return False

    def actualizarScroll(self, jugador, tiempo):
        cambioScrollH = self.actualizarScrollHorizontal(jugador, tiempo)
        cambioScrollV = self.actualizarScrollVertical(jugador, tiempo)

        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScrollH or cambioScrollV:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, self.scrolly))

            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            #self.decorado.update(self.scrollx)

    def update(self,tiempo):
        if (self.jugador.movimiento == ATAQUE_DISTANCIA and self.jugador.fuego):
            bola = BolaDeFuego(self.jugador, self.jugador.posicion[0], self.jugador.posicion[1]-15)
            self.grupoBolasDeFuego.add(bola)
            self.jugador.fuego = False
            self.grupoSprites.add(bola)
            self.grupoSpritesDinamicos.add(bola)
        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        if self.jugador.hp <= 0:
            pygame.time.wait(500)
            self.director.salirPrograma()
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover(self.jugador)
        self.grupoSpritesDinamicos.update(tiempo, self.grupoPlataformas, self.grupoParedes, self.grupoEnemigos, self.grupoBolasDeFuego,
        self.grupoUpgradeVida, self.grupoUpgradeDano)
        self.actualizarScroll(self.jugador, tiempo)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)


    def dibujar(self, pantalla):
        pantalla.fill((133,133,133))
        # Ponemos primero el fondo
        #self.fondo.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
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
    def __init__(self,plataforma, textura):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = plataforma[0]
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        #self.image = pygame.Surface((plataforma[1], plataforma[2]))
        #test = GestorRecursos.CargarImagen('plat.png', -1)
        self.image = pygame.image.load(os.path.join('imagenes', textura)).convert()
        self.image = pygame.transform.scale(self.image, (self.rect.width, 15))
        self.image.convert_alpha()
        #self.image.blit(test, self.rect)
        #self.image.fill((0,0,0))


class Suelo(MiSprite):
    def __init__(self,plataforma):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = plataforma[0]
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((plataforma[1], plataforma[2]))
        #self.image = pygame.image.load(os.path.join('imagenes','wallTest.png')).convert()
        #self.image = pygame.transform.scale(self.image, (400, 600))
        #self.image.convert_alpha()
        #self.image.blit(test, self.rect)
        self.image.fill((0,0,0))


class Relleno(MiSprite):
    def __init__(self,plataforma, textura):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = plataforma[0]
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        #self.image = pygame.Surface((plataforma[1], plataforma[2]))
        self.image = pygame.image.load(os.path.join('imagenes',textura)).convert()
        self.image = pygame.transform.scale(self.image, (self.rect.height, self.rect.width))
        self.image.convert_alpha()
        #self.image.blit(test, self.rect)
        #self.image.fill((0,0,0))


class Pared(MiSprite):
    def __init__(self,plataforma):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = plataforma[0]
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))
        #self.image.fill((0,0,0))

class Decorado:
    def __init__(self, fondo):
        self.imagen = GestorRecursos.CargarImagen(fondo, -1)
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
