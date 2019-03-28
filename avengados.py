#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
import director
from director import *
from pruebas import Fase
from temploAgua import Agua
from temploAire import Aire
from temploTierra import Tierra

if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    escena = Tierra(director,'tierra.xml')
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
