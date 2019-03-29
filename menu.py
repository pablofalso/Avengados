# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
import parser_escena
import fase

class Menu(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.decorado = Decorado()

    def update(self, *args):
        return

    def dibujar(self, pantalla):
        self.decorado.dibujar(pantalla)

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        Agua = pygame.Rect(299,127, 218, 56)
        Aire = pygame.Rect(299,223, 218, 56)
        Tierra = pygame.Rect(299,311, 218, 56)
        Woods = pygame.Rect(299,407,218, 56)
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if Agua.collidepoint(mouse_pos):
                    escena = escena = fase.Fase(self.director,'agua.xml')
                    self.director.apilarEscena(escena)
                elif Aire.collidepoint(mouse_pos) :
                    escena = escena = fase.Fase(self.director,'aire.xml')
                    self.director.apilarEscena(escena)
                elif Tierra.collidepoint(mouse_pos) :
                    escena = escena = fase.Fase(self.director,'tierra.xml')
                    self.director.apilarEscena(escena)
                elif Woods.collidepoint(mouse_pos):
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
        self.imagen = GestorRecursos.CargarImagen('menu.png', -1)
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
