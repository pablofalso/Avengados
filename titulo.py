# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
import parser_escena

class Titulo(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.imagen = GestorRecursos.CargarImagen('titulo.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (800, 600))
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        self.NuevaPartida = GestorRecursos.CargarImagen('nuevaPartida.png', -1)
        self.NuevaPartida = pygame.transform.scale(self.NuevaPartida, (400, 300))
        self.rect1 = self.NuevaPartida.get_rect()
        # La subimagen que estamos viendo
        self.rectSubimagen1 = pygame.Rect(0, 0, 400, 200)
        self.rectSubimagen1.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        #self.Button = Button("",(270, 270), on_mouse_press(400,200,button_01),self.NuevaPartida)
        self.Continuar = GestorRecursos.CargarImagen('continuar.png', -1)
        self.Continuar = pygame.transform.scale(self.Continuar, (400, 300))
        self.rect2 = self.Continuar.get_rect()
        # La subimagen que estamos viendo
        self.rectSubimagen2 = pygame.Rect(0, 0, 400, 200)
        self.rectSubimagen2.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        #self.Button = Button("",(270, 270), on_mouse_press(400,200,button_01),self.NuevaPartida)
        self.salirDelJuego = GestorRecursos.CargarImagen('salirDelJuego.png', -1)
        self.salirDelJuego = pygame.transform.scale(self.salirDelJuego, (400, 300))
        self.rect3 = self.salirDelJuego.get_rect()
        # La subimagen que estamos viendo
        self.rectSubimagen3 = pygame.Rect(0, 0, 400, 200)
        self.rectSubimagen3.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        #self.Button = Button("",(270, 270), on_mouse_press(400,200,button_01),self.NuevaPartida)
    def update(self, *args):
        return

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
        pantalla.blit(self.NuevaPartida,self.rect1, self.rectSubimagen1)
        pantalla.blit(self.Continuar,self.rect2, self.rectSubimagen2)
        pantalla.blit(self.salirDelJuego,self.rect3, self.rectSubimagen3)

            # Ponemos las animaciones

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        button = pygame.Rect(0, 0, 300, 200)
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if button.collidepoint(mouse_pos):
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
