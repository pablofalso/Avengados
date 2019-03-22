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
SPRITE_SALTANDO = 2
SPRITE_SALTANDO_SUBIENDO = 2
SPRITE_SALTANDO_BAJANDO = 3
SPRITE_ATAQUE_MELEE = 4
SPRITE_DASH = 5
SPRITE_ATAQUE_DISTANCIA = 6

VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.4 # Pixeles por milisegundo
VELOCIDAD_DASH = 2 # Pixeles por milisegundo

RETARDO_ANIMACION_QUIETO = 10
RETARDO_ANIMACION_ANDANDO = 7
RETARDO_ANIMACION_SALTANDO_SUBIENDO = 7
RETARDO_ANIMACION_SALTANDO_BAJANDO = 7
RETARDO_ANIMACION_ATAQUE_MELEE = 4
RETARDO_ANIMACION_DASH = 7
RETARDO_ANIMACION_ATAQUE_DISTANCIA = 7

CD_DASH = 500 # En milisegundos
DURACION_DASH = 100 # En milisegundos


# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0,0)
        self.velocidadx = 0
        self.velocidady = 0 
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

class Personaje(MiSprite):
    "Cualquier personaje"

    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion):
        
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        self.coordenadasHoja = []
        for linea in range(0, len(numImagenes)):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4
        
        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)  
        self.retardoMovimiento = 0

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100, 100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()

    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        if movimiento == ARRIBA:
            # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
            if self.numPostura == SPRITE_SALTANDO:
                self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        else:
            self.movimiento = movimiento

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion[self.numPostura]
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def update(self, tiempo, grupoPlataformas): 

        # Las velocidades a las que iba hasta este momento
        velocidadx = self.velocidadx
        velocidady = self.velocidady

        # Si vamos a la izquierda o a la derecha        
        if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

            # Si no estamos en el aire
            if self.numPostura != SPRITE_SALTANDO:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_SALTANDO

        # Si queremos saltar
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0



        # Además, si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO:

            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma != None) and (velocidady>0) and (plataforma.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_QUIETO
                # Y estará quieto en el eje y
                velocidady = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                velocidady += GRAVEDAD * tiempo

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return

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
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA
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



    def update(self, tiempo, grupoPlataformas):
        plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
        #Primero se mira si está encima de una plataforma, si no está cae
        if plataforma == None:
            self.numPostura = SPRITE_SALTANDO_BAJANDO
        #Si esta colisionando entonces para
        elif ((plataforma.rect.bottom >= self.rect.bottom or self.velocidady > 0)) and self.numPostura == SPRITE_SALTANDO_BAJANDO:
            self.velocidady = 0
            self.numPostura = SPRITE_QUIETO
            self.establecerPosicion((self.posicion[0], plataforma.posicion[1]))
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
            self.velocidady = -0.5

        if (self.numPostura == SPRITE_SALTANDO_SUBIENDO) or (self.numPostura == SPRITE_SALTANDO_BAJANDO):
            self.velocidady += 0.01
            if self.velocidady > 0:
                self.numPostura == SPRITE_SALTANDO_BAJANDO
        if self.movimiento == QUIETO :
            if self.numPostura != SPRITE_SALTANDO_SUBIENDO and self.numPostura != SPRITE_SALTANDO_BAJANDO :
                self.numPostura = SPRITE_QUIETO
                self.dobleSalto_segundoSalto = False
            self.velocidadx = 0
        if self.movimiento == ATAQUE:
               self.numPostura = SPRITE_ATAQUE_MELEE
        if self.movimiento == DASH:
            self.numPostura = SPRITE_DASH
            self.retardoMovimiento = -1
            if self.mirando == DERECHA:
                self.velocidadx = 2
            else:
                self.velocidadx = -2
        if self.movimiento == ATAQUE_DISTANCIA:
            self.numPostura = SPRITE_ATAQUE_DISTANCIA

        self.actualizarPostura()
        MiSprite.update(self,tiempo)
        return

class BolaDeFuego(pygame.sprite.Sprite):
    "BolaDeFuego"
    def __init__(self, posicionx, posiciony):
        print("fireball")

# -------------------------------------------------
# Clase NoJugador

class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    def __init__(self,archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion)

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def mover_cpu(self, jugador):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return

# -------------------------------------------------
# Clase EnemigoComun

class EnemigoComun(NoJugador):
    "El enemigo 'EnemigoComun'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'EnemigoBasico.png','coordenadasEnemigoBasico.txt', [4, 4, 8, 8], VELOCIDAD_JUGADOR/2, 0, [10,10,10,10])

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador):

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:
            if jugador.posicion[0]<self.posicion[0]:
                Personaje.mover(self,IZQUIERDA)
            else:
                Personaje.mover(self,DERECHA)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)