import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
import parser_escena

#pantalla de inicio en la que puedes seleccionar entre crear nueva partida, continuar o salir.

class pantallaInicio(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.menu = menu()

    def update(self,tiempo):
        print("pipo")

    def dibujar(self, pantalla):
        pantalla.fill((133,133,133))
        # Ponemos primero el fondo
        #self.fondo.dibujar(pantalla)
        # Después el decorado
        self.menu.dibujar(pantalla)
        # Luego los Sprites
        #self.grupoSprites.draw(pantalla)



    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        ''' if teclasPulsadas[K_UP]:
            self.jugador1.keyUp_pulsada = True
        # Una vez se suelta la tecla se actualiza la variable del jugador para que pueda realizar el segundo salto
        if (not teclasPulsadas[K_UP]) and self.jugador1.keyUp_pulsada:
            self.jugador1.keyUp_pulsada = False
            self.jugador1.keyUp_suelta = True
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN,K_KP_ENTER) '''


class menu:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('titulo.png', -1)
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
