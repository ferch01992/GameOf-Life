import pygame
import numpy as np
import time
# Creando pantalla.
pygame.init()

# Ancho y alto de la pantalla.
width, height = 1000, 1000
screen = pygame.display.set_mode( ( height, width ) )

# Asignar un color oscuro.
bg = 25, 25, 25

#Pintamos el fondo con el color elegido.
screen.fill( bg )

# Nùmero de celdas.
nxC, nyC = 60, 60

# Dimensiones de las celdas
dimCW = width  / nxC
dimCH = height / nyC

# Estructura de datos, crando una matriz.
# Estado de las celdas Vivas = 1; Muertas = 0;
gameState = np.zeros( ( nxC, nyC ) )

# Automata palo.
# gameState[ 5, 3 ] = 1
# gameState[ 5, 4 ] = 1
# gameState[ 5, 5 ] = 1
# Automata movil.
gameState[ 21, 21 ] = 1
gameState[ 22, 22 ] = 1
gameState[ 22, 23 ] = 1
gameState[ 21, 23 ] = 1
gameState[ 20, 23 ] = 1
# Automata .
# gameState[ 30, 28 ] = 1
# gameState[ 30, 29 ] = 1
# gameState[ 30, 30 ] = 1

# Control de ejecución del mouse y teclado
pauseExect = False

# Bucle para mostrar de manera infinita la pantalla.
while True:

	# Creamos una copia del estado actual del juego.
	newGameState = np.copy( gameState )

	# Limpiamos la pantalla.
	screen.fill( bg )
	time.sleep( 0.1 )

	# Registrar eventos del teclado y raton.
	ev = pygame.event.get()

	for event in ev:
		# Detectamos si se presiona una tecla.
		if event.type == pygame.KEYDOWN:
			pauseExect = not pauseExect

		# Detectamos si se presina el ratón.
		mouseClick = pygame.mouse.get_pressed()

		if sum( mouseClick ) > 0:
			posX, posY = pygame.mouse.get_pos()
			# Detectamos la celda seleccionada con el mouse
			celX, celY = int( np.floor( posX / dimCW ) ), int( np.floor( posY / dimCW ) )
			newGameState[ celX, celY ] = not mouseClick[ 2 ]

	for y in range( 0, nxC ):
		for x in range( 0, nyC ):
			if not pauseExect:
				# Calculamos el numero de vecinos cercanos.
				n_neigh = gameState[ ( x - 1 ) % nxC, ( y - 1 ) % nyC ] + \
						gameState[ ( x )     % nxC, ( y - 1 ) % nyC ] + \
						gameState[ ( x + 1 ) % nxC, ( y - 1 ) % nyC ] + \
						gameState[ ( x - 1 ) % nxC, ( y )     % nyC ] + \
						gameState[ ( x + 1 ) % nxC, ( y )     % nyC ] + \
						gameState[ ( x - 1 ) % nxC, ( y + 1 ) % nyC ] + \
						gameState[ ( x )     % nxC, ( y + 1 ) % nyC ] + \
						gameState[ ( x + 1 ) % nxC, ( y + 1 ) % nyC ]

				# Regla #1: Una célula muerta con exactamente 3 vecinas vivas, 'revive'.
				if gameState[ x, y ] == 0 and n_neigh == 3:
					newGameState[ x, y ] = 1

				# Regla #2: Una célula viva con menos de 2 o más de 3 vecinas vivas, 'muere'.
				elif gameState[ x, y ] == 1 and ( n_neigh < 2 or n_neigh > 3 ):
					newGameState[ x, y ] = 0

			# Creamos el poligono de cada celda a dibujar.
			poly = [
				( ( x )    * dimCW, y         * dimCH ),
				( (x + 1 ) * dimCW, y         * dimCH ),
				( (x + 1 ) * dimCW, ( y + 1 ) * dimCH ),
				( (x)      * dimCW, ( y + 1 ) * dimCH ),
			]

			# Dibujamos la celda para cada par de "X" y "Y".
			if newGameState [ x, y ] == 0:
				pygame.draw.polygon( screen, ( 128, 128, 128 ), poly, 1 )
			else:
				pygame.draw.polygon( screen, ( 255, 255, 255 ), poly, 0 )

	# Actualizamos el estado del juego.
	gameState = np.copy( newGameState )

	pygame.display.flip()