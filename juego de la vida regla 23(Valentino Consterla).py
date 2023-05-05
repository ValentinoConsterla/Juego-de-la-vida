import pygame # instalacion: new terminal> pip intall pygame
import numpy as np # instalacion: new terminal> pip intall numpy
import time #para los tiempos de ejecucion

pygame.init()

width, height =1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

#tamaño matriz
nxC, nyC = 50, 50

#dimensiones de cada celda individual
dimCW = width / nxC
dimCH = height / nyC

#Estado de las celdas. vitalidad de la celula 1(viva)/0(muerta)
gameState = np.zeros((nxC, nyC))

#palos girando
gameState[3, 5] = 1
gameState[4, 5] = 1
gameState[5, 5] = 1
gameState[7, 5] = 1
gameState[8, 5] = 1
gameState[9, 5] = 1

#figura 1
gameState[23, 5] = 1
gameState[24, 5] = 1
gameState[25, 5] = 1
gameState[27, 5] = 1
gameState[28, 5] = 1
gameState[29, 5] = 1
gameState[24, 4] = 1
gameState[28, 4] = 1
gameState[24, 6] = 1
gameState[28, 6] = 1
#Pausa de las iteraciones
pauseExect = False

#Bucle de ejecucion
while True:
    
    newGameState = np.copy(gameState)

    #tiempo de ejecucion (evitamos forzar el equipo en ejecutar a altas velocidades)
    time.sleep(0.1)
    #limpieza de la pantalla
    screen.fill(bg)
    
    
    #Control teclado y mouse
    ev = pygame.event.get()
    
    for event in ev:
        #cualquier tecla pausara el juego
        if event.type == pygame.KEYDOWN:
            pauseExect=not pauseExect
        
        #controles del raton(click izquierdo: celula viva| click derecho: celula muerta)    
        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]
            
            
    for y in range(0, nxC):
        for x in range(0, nyC):
            
            if not pauseExect:
            
                #Calculo N° vecinos cercanos
                n_neigh =   gameState[(x - 1) % nxC, (y - 1)  % nyC] + \
                            gameState[(x)     % nxC, (y - 1)  % nyC] + \
                            gameState[(x + 1) % nxC, (y - 1)  % nyC] + \
                            gameState[(x - 1) % nxC, (y)      % nyC] + \
                            gameState[(x + 1) % nxC, (y)      % nyC] + \
                            gameState[(x - 1) % nxC, (y + 1)  % nyC] + \
                            gameState[(x)     % nxC, (y + 1)  % nyC] + \
                            gameState[(x + 1) % nxC, (y + 1)  % nyC]

                #Regla 1: si una celula muerta tiene 3 vecinos vivos, esta nace/revive
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                #Regla 2: si una celula viva tiene 2 o 3 vecinos este sobrevive.
                elif gameState[x, y] == 1 and (n_neigh == 2 or n_neigh == 3):
                    newGameState[x, y] = 1
                
                # Regla #3 : si una celula viva tiene menos de 2 vecinos fallece por aislamiento.
                else:
                    newGameState[x, y] = 0
            #Creacion poligono de cada celda
            poly = [((x)   * dimCW,  y * dimCH),
                    ((x+1)   * dimCW,  y * dimCH),
                    ((x+1)   * dimCW,  (y+1) * dimCH),
                    ((x)   * dimCW,   (y+1) * dimCH)]

            #Dibujo de las celdas por cada par de "x" e "y"
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen,(128, 128, 128), poly, 1 )
            else:
                pygame.draw.polygon(screen,(255, 255, 255), poly, 0 )

    #Actualizacion estado del juego
    gameState = np.copy(newGameState)

    #Actualizacion de la pantalla
    pygame.display.flip()
    
#recordatorios en caso de romper algo en el juego (y tambien porque se me olvido la contraseña del github)
#28-04-23: añadido y arreglado el tema del conteo de celdas| añadido las celulas al morir o sobrevivir
#01-05-23: juego de la vida terminado| arreglado el tema de las celulas vivas sobrepuestas (gracias internet)
#02-05-23: mouse antes solo pintaba, ahora borra tambien| introduccion del teclado para pausar el juego
#03-05-23: solucionado el problema de que al pausar se ponia en negro (recordatorio:la posicion de las partes del codigo si afectan dentro o no de un for,if,while,etc.)