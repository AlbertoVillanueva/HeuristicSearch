from config import CONFIG
from node import node, state, MUROS, SALIDA, LLAVES, SERPIENTES
import sys, time
f = open(sys.argv[1],'r')
archivo = f.read()
f.close()
archivo = archivo.split('\n')
heuristica = 1
al = (-1,1)
# Configuramos el archivo
if "" in archivo:
	archivo.remove("")
rocas = []
for i in range(len(archivo)):
	fila = []
	for j in range(len(archivo[i])):
		if archivo[i][j] == 'A':
			al = (i,j)
		if archivo[i][j] == 'E':
			SALIDA.append(i)
			SALIDA.append(j)
		if archivo[i][j] == 'O':
			rocas.append((i,j)) 
		if archivo[i][j] == 'K':
			LLAVES.append((i,j))
		if archivo[i][j] == 'S':
			SERPIENTES.append((i,j))
		fila.append(archivo[i][j] == '%' or archivo[i][j] == 'E' or archivo[i][j] == 'S')
	MUROS.append(fila)
# Creamos el nodo inicial

I = node(None, 0, state(al, rocas, [False]*len(LLAVES)),heuristica)
import pygame
from interfaz import interfaz
blueprint = [list(row[:]) for row in archivo]
for i in range(len(blueprint)):
	for j in range(len(blueprint[i])):
		if blueprint[i][j] == 'O' or blueprint[i][j] == 'A' or blueprint[i][j] == 'K':
			blueprint[i][j] = ' '
ventana = interfaz(blueprint, LLAVES)
ventana.draw(I.estado)
while ventana.running:
	# event handling, gets all event from the eventqueue
	for event in pygame.event.get():
		# only do something if the event is of type QUIT
		if event.type == pygame.QUIT:
			# change the value to False, to exit the main loop
			ventana.running = False