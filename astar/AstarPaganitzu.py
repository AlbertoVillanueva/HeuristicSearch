# Built using Python 3.6.7
# Alberto Villanueva
# Cristian Cabrera
# Interface courtesy of pygame (www.pygame.org)

from config import CONFIG
from node import node, state, MUROS, SALIDA, LLAVES, SERPIENTES
import sys, time

# Abrimos el archivo
f = open(sys.argv[1],'r')
heuristica = sys.argv[2]
archivo = f.read()
f.close()
archivo = archivo.split('\n')
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
if CONFIG["interfaz"]:
	import pygame
	from interfaz import interfaz
	blueprint = [list(row[:]) for row in archivo]
	for i in range(len(blueprint)):
		for j in range(len(blueprint[i])):
			if blueprint[i][j] == 'O' or blueprint[i][j] == 'A' or blueprint[i][j] == 'K':
				blueprint[i][j] = ' '
	ventana = interfaz(blueprint, LLAVES)
	ventana.draw(I.estado)
# Empezamos el temporizador
START = time.time()
# Inicializamos ABIERTA con el estado inicial I, CERRADA vacia y EXITO a Falso
ABIERTA = [I,]
CERRADA = []
EXITO = False
# Mientras que ABIERTA no esta vacia y no haya EXITO
while ABIERTA != [] and not EXITO:
	# Quitar el primero nodo, N, de ABIERTA
	N = ABIERTA[0]
	ABIERTA.pop(0)
	# Si N es estado final entonces hay EXITO
	if N.estado.esFinal(): 
		EXITO = True
	# Si no
	else:
		# Expandir N generando el conjunto S de sucesores de N
		S = N.genSucesores(heuristica)
		# Meter N en CERRADA 
		CERRADA.append(N)
		# Para cada sucesor s en S
		for s in S:
			estaEnAbierta, indice = s.estaEn(ABIERTA)
			# Si s esta en ABIERTA y la funci on de evaluaci on f() de s es mejor, se elimina el que ya estaba en ABIERTA y se introduce s en orden
			if estaEnAbierta and s.f <= ABIERTA[indice].f:
				if s.f != ABIERTA[indice].f:
					del ABIERTA[indice]
					s.insertarOrdenado(ABIERTA)
			else:
				estaEnCerrada, indice = s.estaEn(CERRADA)
				# Si s no esta ni en ABIERTA ni en CERRADA se inserta en orden en ABIERTA
				if not estaEnCerrada:
					s.insertarOrdenado(ABIERTA)
END = time.time()
# Si exito imprimir el camino desde N hasta I
if EXITO:
	path = N.backtracking()
	if CONFIG["crearOutput"]:
		f = open(sys.argv[1]+".output",'w')
		f.write(str(path[0]))
		for p in range(1,len(path)):
			f.write("→")
			f.write(str(path[p]))
		f.close()
	tTotal = str(int((END-START)*1000)/1000)+'s'
	if CONFIG["crearStatistics"]:
		f = open(sys.argv[1]+".statistics",'w')
		f.write("Tiempo total: "+tTotal+"\n")
		f.write("Coste total: "+str(N.g)+"\n")
		f.write("Longitud de la ruta: "+ str(len(path)-1)+"\n")
		f.write("Nodos expandidos: "+ str(len(CERRADA)+1))
		f.close()
	if CONFIG["imprimirOutput"]:
		camino = ["→"+str(path[p]) for p in range(1,len(path))] 
		print(str(path[0])+"".join(camino))
	if CONFIG["imprimirStatistics"]:
		print("Tiempo total: "+tTotal)
		print("Coste total: "+str(N.g))
		print("Longitud de la ruta: "+ str(len(path)-1))
		print("Nodos expandidos: "+ str(len(CERRADA)+1))
	if CONFIG["interfaz"]:
		N.animar(ventana)
		# main loop
		while ventana.running:
			# event handling, gets all event from the eventqueue
			for event in pygame.event.get():
				# only do something if the event is of type QUIT
				if event.type == pygame.QUIT:
					# change the value to False, to exit the main loop
					ventana.running = False
# Si no imprimir "Fracaso"
else:
	print("Fracaso")