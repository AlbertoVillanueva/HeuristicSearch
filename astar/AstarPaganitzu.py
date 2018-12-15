# Built using Python 3.6.7
# Alberto Villanueva
# Cristian Cabrera
# Interface courtesy of pygame (www.pygame.org)

from config import CONFIG
from node import node, state, MUROS, SALIDA, LLAVES, SERPIENTES
import sys, time


def astar():
	'''Hace busqueda heurisitca usando el algoritmo A*
	'''
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
			S = genSucesores(N)
			# Meter N en CERRADA 
			CERRADA.append(N)
			# Para cada sucesor s en S
			for s in S:
				estaEnAbierta, indice = s.estaEn(ABIERTA)
				# Si s esta en ABIERTA y la funci on de evaluaci on f() de s es mejor, se elimina el que ya estaba en ABIERTA y se introduce s en orden
				if estaEnAbierta and s.f < ABIERTA[indice].f:
						del ABIERTA[indice]
						insertarOrdenado(ABIERTA,s)
				else:
					estaEnCerrada, indice = s.estaEn(CERRADA)
					# Si s no esta ni en ABIERTA ni en CERRADA se inserta en orden en ABIERTA
					if not estaEnCerrada:
						insertarOrdenado(ABIERTA,s)
	END = time.time()
	# Si exito imprimir el camino desde N hasta I
	if EXITO:
		path = backtracking(N)
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
			animar(N)
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
def genSucesores(nodo):
	'''Devuelve una lista con los sucesores de `nodo`
	   nodo es un node
	'''
	# Iniciamos la lista de sucesores vacia
	sucesores = []
	# Definimos los posibles movimientos que se pueden realizar
	movimientos = [(1,0),(-1,0),(0,1),(0,-1)]
	# Para casa posible movimiento m
	for m in movimientos:
		# Calculamos la nueva posicion para ese movimiento
		nuevaPos = (nodo.estado.al[0]+m[0],nodo.estado.al[1]+m[1])
		# Si tenemos todas las llaves y la nueva posicion es la SALIDA añadimos el descendiente
		if not nodo.estado.quedanLlaves() and nuevaPos == SALIDA:
			sucesores.append(node(nodo,2, state(nuevaPos,nodo.estado.rocas[:],nodo.estado.llaves[:])))
		# Si en la nueva posicion no hay muros y no es un sitio peligroso
		elif not MUROS[nuevaPos[0]][nuevaPos[1]] and not nodo.estado.esSitioPeligroso(nuevaPos):
			# Si en la nueva posicion hay alguna roca
			if nuevaPos in nodo.estado.rocas:
				# Calculamos la posicion a la que la roca se moveria
				siguientePos = (nuevaPos[0]+m[0],nuevaPos[1]+m[1])
				# Si podemos moverla alli (Si no hay otras rocas, muros o llaves)
				if not(siguientePos in nodo.estado.rocas or MUROS[siguientePos[0]][siguientePos[1]] or nodo.estado.hayLlave(siguientePos)):
					# Calculamos las nuevas posiciones de las rocas y lo añadimos el descendiente
					nuevasRocas = nodo.estado.rocas[:]
					nuevasRocas.remove(nuevaPos)
					nuevasRocas.append(siguientePos)
					sucesores.append(node(nodo, 4, state(nuevaPos,nuevasRocas,nodo.estado.llaves[:])))
			# SI en la nueva posicion no hay rocas
			else:
				# Añadimos el descendiente recogiendo las llaves que haya en la nueva posicion
				nuevasLlaves = nodo.estado.llaves[:]
				if nuevaPos in LLAVES:
					nuevasLlaves[LLAVES.index(nuevaPos)] = True
				sucesores.append(node(nodo, 2, state(nuevaPos,nodo.estado.rocas[:],nuevasLlaves)))
	# Devolvemos los sucesores
	return sucesores
def insertarOrdenado(lista, nodo):
	'''Inserta `nodo` en `lista` ordenado de menor a mayor
	   En caso de empate inserta lo mas cercano al principio
	   lista es una lista de node
	   nodo es un node
	'''
	# si la lista esta vacia insertamos el nodo
	if not len(lista):
		lista.append(nodo)
	else:
		# Hacemos busqueda binaria hasta encontrar el valor mas cercano
		# Empezamos buscando en toda la lista
		primero = 0
		ultimo = len(lista)-1
		# Mientras no tengamos longitud 1 
		while primero < ultimo:
			# Calculamos la posicion media de la seccion en la que estamos
			medio = primero+(ultimo-primero)//2
			# Si hemos encontrado nuestro objetivo terminamos
			if nodo.f == lista[medio].f:
				primero=medio
				break
			# Si f del nodo es mas pequeño que el medio buscamos en la mitad anterior
			elif nodo.f<lista[medio].f:
				ultimo=medio-1
			# Si f del nodo es mas grande que el medio buscamos en la mitad posterior
			elif nodo.f>lista[medio].f:
				primero=medio+1
		# Si f del nodo es mas pequeño lo insertamos antes
		if nodo.f<lista[primero].f:
			lista.insert(primero, nodo)
		# Si es mas grando lo insertamos despues
		elif nodo.f>lista[primero].f:
			lista.insert(primero+1, nodo)
		# Si f es igual
		else:
			# Retrocedemos hasta el primero nodo que tenga la misma f
			while lista[primero].f == nodo.f:
				primero-=1
				if primero == -1:
					break
			# Insertamos antes del primer nodo que es igual
			lista.insert(primero+1,nodo)
def backtracking(N):
	'''Devuelve una lista con el camino que ha hecho para llegar hasta `N`
	   N es un node
	'''
	path = []
	nodo = N
	while nodo != None:
		path.append(nodo.estado.al)
		nodo = nodo.padre
	return path[:0:-1]
def animar(N):
	estados = []
	nodo = N
	while nodo != None:
		estados.append(nodo.estado)
		nodo = nodo.padre
	estados = estados[::-1]
	for e in estados:
		ventana.vaciar()
		ventana.draw(e)
		time.sleep(CONFIG["velocidad"])

f = open(sys.argv[1],'r')
#f = open("lab_astar/lab3.map",'r')
archivo = f.read()
f.close()
archivo = archivo.split('\n')
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
print("LLAVES:",LLAVES)
print("SERPIENTES:",SERPIENTES)
print("SALIDA:",SALIDA)
print()
SALIDA = tuple(SALIDA)
I = node(None, 0, state(al, rocas, [False]*len(LLAVES)))
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
START = time.time()
astar()