# -*- coding: utf-8 -*-

# Importar las librerías
import pygame, sys
from pygame.locals import *

# Inicializar la librería de pygame
pygame.init()

BLANCO = (255,255,255)

# Creamos la pantalla
pantalla = pygame.display.set_mode((800,600))

# Bucle infinito
while True:

        # Para cada evento posible
        for evento in pygame.event.get():

                # Si el evento es la pulsación de la tecla Escape
                if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                        # Se sale del programa
                        pygame.quit()
                        sys.exit()


        # Rellenamos la pantalla de color negro
        pantalla.fill((0,0,0))


        # Actualizamos la pantalla
        pygame.display.update()

class Jugador(pygame.sprite.Sprite):
    "Jugador"

    def __init__(self):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self);
        # Se carga la imagen
        self.imagen = load_image('Jugador.png', -1)
        self.imagen = self.imagen.convert_alpha()
        # El rectangulo y la posicion que tendra
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (100,100)


    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((800, 600), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Poner el título de la ventana
    pygame.display.set_caption('Ejemplo de uso de Sprites')

    # Cargar la imagen del hombre
    jugador = Jugador()

    # Variable que controla la posición del Sprite (horizontal)
    pos = 100

    # El bucle de eventos
    while True:

        # Hacemos que el reloj espere a un determinado fps
        reloj.tick(60)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Modificar posición en función de la tecla pulsada
        teclasPulsadas = pygame.key.get_pressed()
        if teclasPulsadas[K_LEFT]:
            jugador.rect.centerx -= 1
        if teclasPulsadas[K_RIGHT]:
            jugador.rect.centerx += 1
        # Si la tecla es Escape
        if teclasPulsadas[K_ESCAPE]:
            # Se sale del programa
            pygame.quit()
            sys.exit()

        # Dibujar el fondo de color
        pantalla.fill((133,133,133))

        # Dibujar el Sprite
        jugador.dibujar(pantalla)

        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main()
