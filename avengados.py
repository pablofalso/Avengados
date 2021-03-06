#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
import director
from director import Director
from fase import Fase
from menu import Menu
from titulo import Titulo

if __name__ == '__main__':
    pygame.font.init()
    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial

    escena = Menu(director)


    #escena = Fase(director,'agua.xml')
    escena = Titulo(director)


    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
