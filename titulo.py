# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
import parser_escena

class Titulo(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.decorado = Decorado()

    def update(self, *args):
        return

    def dibujar(self, pantalla):
        self.decorado.dibujar(pantalla)

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        NuevaPartida = pygame.Rect(159,265, 383, 38)
        Continuar = pygame.Rect(159,352, 383, 38)
        SalirDelJuego = pygame.Rect(159,440, 383, 38)
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if NuevaPartida.collidepoint(mouse_pos) or Continuar.collidepoint(mouse_pos) or SalirDelJuego.collidepoint(mouse_pos):
                    # prints current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))

    def on_close(self):
        self.director.salirPrograma()

    # El evento relativo al clic del raton
    def on_mouse_press(self, x, y, button):
        # Si se pulsa el boton izquierdo
        if(pygame.mouse.get_pressed == button1):
            # Miramos a ver en que boton se ha pulsado, y se hace la accion correspondiente
            if  (x>=self.NuevaPartida.x) and (x<=(self.NuevaPartida.x + self.NuevaPartida.width)) and (y>=self.NuevaPartida.y) and (y<=(self.NuevaPartida.y + self.NuevaPartida.height)):
                self.director.salirPrograma()


class Decorado:
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
