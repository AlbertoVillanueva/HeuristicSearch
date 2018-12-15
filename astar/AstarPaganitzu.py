# Built using Python 3.6.7
# Alberto Villanueva
# Cristian Cabrera
# Interface courtesy of pygame


CONFIG = {
	# ficheros
	"crearOutput": False,
	"crearStatistics": False,
	# salida por pantalla
	"imprimirOutput": True,
	"imprimirStatistics": True,
	# extra
	"hayDiagonales": False,
	# heuristicas
	"detectarMuros": False,
	"detectarLlavesPeligrosas": True,
	# interfaz
	###########
	# WARNING # If this is True you must have pygame installed in for it to work
	########### Si esta en True tienes que tener pygame instalado para que funcione
	"interfaz": False, 
	"velocidad": 0.35
}

import sys, time
if CONFIG["interfaz"]:
	import pygame
	class interfaz():
		running = True
		imagenes = {
				'%': pygame.image.load("images/muro.png"),
				'A': pygame.image.load("images/al.png"),
				'K': pygame.image.load("images/llave.png"),
				'O': pygame.image.load("images/roca.png"),
				'E': pygame.image.load("images/salida.png"),
				'S': pygame.image.load("images/serpiente.png"),
		}
		screen = None
		def __init__(self):
			# initialize the pygame module
			pygame.init()
			# load and set the logo
			pygame.display.set_caption("minimal program")
			# create a surface on screen that has the size of 240 x 180
			self.screen = pygame.display.set_mode((len(archivo[0])*32,(len(archivo))*32))
			self.screen.fill((0,0,0))
			for i in range(len(blueprint)):
				for j in range(len(blueprint[i])):
					if blueprint[i][j] != ' ':
						self.screen.blit(self.imagenes[blueprint[i][j]], (j*32,i*32))
			pygame.display.flip()
		def draw(self, estado):
			mapa = [row[:] for row in blueprint]
			if estado.al == SALIDA:
				pygame.draw.rect(self.screen,(0,0,0),(SALIDA[1]*32,SALIDA[0]*32,32,32))
			self.screen.blit(self.imagenes['A'], (estado.al[1]*32,estado.al[0]*32))
			for r in estado.rocas:
				self.screen.blit(self.imagenes['O'], (r[1]*32,r[0]*32))
			for k in range(len(LLAVES)):
				if not estado.llaves[k]:
					self.screen.blit(self.imagenes['K'], (LLAVES[k][1]*32,LLAVES[k][0]*32))
			pygame.display.flip()
		def vaciar(self):
			for i in range(len(blueprint)):
				for j in range(len(blueprint[i])):
					if blueprint[i][j] == ' ':
						pygame.draw.rect(self.screen,(0,0,0),(j*32,i*32,32,32))
			pygame.display.flip()
			
class state():
	'''Clase que representa un estado
	   al es la posicion de al
	   rocas es una lista de las rocas
	   llaves es una lista que dice que llaves se han recogido
	'''
	al = None
	rocas = None
	llaves = None
	def __init__(self, al, rocas, llaves):
		'''Inicializa el estado dadas la posicion de al, las posiciones de las rocas, y las llaves que se han cogido
		   al es una tupla (x,y)
		   rocas es una lista de tuplas (x,y)
		   llaves es una tupla de booleanos con la longitud del numero de llaves
		'''
		#Se asignan los valores
		self.al = al
		self.rocas = rocas
		self.llaves = llaves
	def igual(self, estado):
		'''Devuelve True si `estado` es igual a esta instancia
		   estado es un state
		'''
		# Si todos los elementos del estado son iguales devuelve True, si no False
		return self.al == estado.al and self.llaves == estado.llaves and sorted(self.rocas) == sorted(estado.rocas)
	def quedanLlaves(self):
		'''Devuelve True si queda alguna llave por recoger
		'''
		for k in self.llaves:
			if not k:
				return True
		return False
class node():
	'''Clase que representa un estado con informacion adicional
	   padre es un puntero al padre del que ha surgido este nodo
	   g es el coste acumulado del nodo
	   f es la funcion de evaluacion
	   estado es el propio estado del nodo
	'''
	padre = None
	g = None
	f = None
	estado = None
	def __init__(self, padre, c, estado):
		'''Inicializa el nodo dado el padre del nodo, el coste para llegar desde el padre hasta el nodo, y el estado del nuevo nodo
		   padre es un puntero a una instancia de node
		   c es un numero
		   estado es un state
		'''
		# Se asigna el padre
		self.padre = padre
		# Si no es el nodo inicial se calcula g mediante g del padre y el coste
		if padre != None:
			self.g = padre.g+c
		else:
			self.g = 0
		# Se asigna el estado
		self.estado = estado
		# Se asigna la funcion de evaluacion calculando la heuristica
		self.f = self.g + self.h()
	def h(self):
		'''Devuelve el valor heuristico para el `estado`
		'''
		coste = 0
		# si quedan llaves añadir la distancia hasta la llave mas lejana y la distancia desde esa llave hasta la salida
		if self.estado.quedanLlaves():
			llaveLejos = max((self.distancia(LLAVES[k],self.estado.al),LLAVES[k]) for k in range(len(LLAVES)) if not self.estado.llaves[k])
			coste += 2*(llaveLejos[0]+ self.distancia(llaveLejos[1],SALIDA))
			coste += 2*(len(self.estado.llaves)-sum(self.estado.llaves)-1)
		# si no quedan llaves añadir la distancia hasta la salida
		else:
			coste += 2*self.distancia(self.estado.al,SALIDA)
		# si queremos detectar las llaves que esten en peligro
		if CONFIG["detectarLlavesPeligrosas"]:
			# para cada llave
			for i in range(len(LLAVES)):
				# si hay serpientes y aun no hemos cogido esta llave añadir el minimo coste para tapar la(s) serpiente que ponen en peligro la llave
				if SERPIENTES != [] and not self.estado.llaves[i]:
					hay, serpiente = haySerpienteIz(LLAVES[i],self.estado)
					if hay:
						coste += 2*min(self.taparSerpiente(serpiente,LLAVES[i],r) for r in self.estado.rocas)
					hay, serpiente = haySerpienteDer(LLAVES[i],self.estado)
					if hay:
						coste += 2*min(self.taparSerpiente(serpiente,LLAVES[i],r) for r in self.estado.rocas)
		return coste
	def distancia(self, pos1, pos2):
		'''Devuelve la distancia desde `pos1` hasta `pos2`
		   pos1 es una tupla (x,y)
		   pos2 es una tupla (x,y)
		'''
		return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])
	def taparSerpiente(self, serpiente, posicion, roca):
		'''Devuelve la distancia que hay que mover `roca` para que tape la `serpiente` respecto a la `posicion`
		   serpiente, posicion y roca son tuplas (x,y)
		'''
		huecoIz = min(serpiente[1],posicion[1])+1
		huecoDer = max(serpiente[1],posicion[1])
		if roca[1] in range(huecoIz,huecoDer):
			return abs(roca[0]-serpiente[0])
		else: 
			return min(self.distancia(roca,(serpiente[0], huecoIz)),self.distancia(roca,(serpiente[0], huecoDer)))
	def estaEn(self,l):
		'''Devuelve True si el `estado` esta en la lista `l`
		   Devuelve la posicion del estado en `l`, si `estado` no esta en `l` devuelve None
		   l es una lista de node
		'''
		# Iteramos por toda la lista
		for i in range(len(l)):
			# Si el estado en i es igual devolvemos True y la posicion de dicho estado
			if self.estado.igual(l[i].estado):
				return True, i
		# Si ningun estado era igual devolvemos Flase y None por posicion
		return False, None
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
		if esFinal(N): 
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
	
def esFinal(N):
	'''Devuelve True si `N` es un estado final
	   N es un node
	'''
	return N.estado.al == SALIDA
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
		elif not MUROS[nuevaPos[0]][nuevaPos[1]] and not esSitioPeligroso(nuevaPos,nodo.estado):
			# Si en la nueva posicion hay alguna roca
			if nuevaPos in nodo.estado.rocas:
				# Calculamos la posicion a la que la roca se moveria
				siguientePos = (nuevaPos[0]+m[0],nuevaPos[1]+m[1])
				# Si podemos moverla alli (Si no hay otras rocas, muros o llaves)
				if not(siguientePos in nodo.estado.rocas or MUROS[siguientePos[0]][siguientePos[1]] or hayLlave(siguientePos,nodo.estado)):
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
def esSitioPeligroso(pos,estado):
	'''Devuelve True si `pos` es una posicion peligrosa en `estado`
	   pos es una tupla (x,y)
	   estado es un state
	'''
	return haySerpienteIz(pos,estado)[0] or haySerpienteDer(pos,estado)[0]
def haySerpienteIz(pos,estado):
	'''Devuelve True si `pos` tiene una serpiente a la izquierda en `estado`
	   Devuelve la posicion de la serpiente
	   pos es una tupla (x,y)
	   estado es un state
	'''
	i = pos[1]-1
	# Nos movemos hacia la izquierda hasta encontrar el primer muro o roca
	while not MUROS[pos[0]][i] and (pos[0],i) not in estado.rocas:
		i-=1
	# Si es una serpiente es un sitio peligroso y devolvemos True
	return (pos[0],i) in SERPIENTES, (pos[0],i)
def haySerpienteDer(pos,estado):
	'''Devuelve True si `pos` tiene una serpiente a la derecha en `estado`
	   Devuelve la posicion de la serpiente
	   pos es una tupla (x,y)
	   estado es un state
	'''
	i = pos[1]+1
	# Nos movemos hacia la derecha hasta encontrar el primer muro o roca
	while not MUROS[pos[0]][i] and (pos[0],i) not in estado.rocas:
		i+=1
	# Si es una serpiente es un sitio peligroso y devolvemos True
	return (pos[0],i) in SERPIENTES, (pos[0],i)
def hayLlave(pos, estado):
	'''Devuelve True si en el `estado` hay una llave en `pos`
	   pos es una tupla (x,y)
	   estado es un state
	'''
	if pos in LLAVES:
		return not estado.llaves[LLAVES.index(pos)]
	return False


MUROS=[]
LLAVES = []
SERPIENTES = []
SALIDA = (None,None)


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
			SALIDA = (i,j)
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
I = node(None, 0, state(al, rocas, [False]*len(LLAVES)))
if CONFIG["interfaz"]:
	blueprint = [list(row[:]) for row in archivo]
	for i in range(len(blueprint)):
		for j in range(len(blueprint[i])):
			if blueprint[i][j] == 'O' or blueprint[i][j] == 'A' or blueprint[i][j] == 'K':
				blueprint[i][j] = ' '
	ventana = interfaz()
	ventana.draw(I.estado)
START = time.time()
astar()