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
		if sum(self.estado.llaves) < len(self.estado.llaves):
			llaveLejos = max((abs(LLAVES[k][0]-self.estado.al[0])+abs(LLAVES[k][1]-self.estado.al[1]),LLAVES[k]) for k in range(len(LLAVES)) if not self.estado.llaves[k])
			return 2*(llaveLejos[0]+ abs(llaveLejos[1][0]-salida[0])+abs(llaveLejos[1][1]-salida[1]))
		return 2*(abs(self.estado.al[0]-salida[0])+abs(self.estado.al[1]-salida[1]))
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
	# Si exito imprimir el camino desde N hasta I
	if EXITO:
		print(backtracking(N))	
	# Si no imprimir "Fracaso"
	else:
		print("Fracaso")
	
def esFinal(N):
	'''Devuelve True si `N` es un estado final
	   N es un node
	'''
	return N.estado.al == salida
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
		# Si tenemos todas las llaves y la nueva posicion es la salida añadimos el descendiente
		if sum(nodo.estado.llaves) == len(LLAVES) and nuevaPos == salida:
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
	if not len(lista):
		lista.append(nodo)
	else:
		primero = 0
		ultimo = len(lista)-1
		while primero < ultimo:
			medio = primero+(ultimo-primero)//2
			if nodo.f == lista[medio].f:
				primero=medio
				break
			elif nodo.f<lista[medio].f:
				ultimo=medio-1
			elif nodo.f>lista[medio].f:
				primero=medio+1

		if nodo.f<lista[primero].f:
			lista.insert(primero, nodo)
		elif nodo.f>lista[primero].f:
			lista.insert(primero+1, nodo)
		else:
			while lista[primero].f == nodo.f:
				primero-=1
				if primero == -1:
					break
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
	path = path[::-1]
	directions = {(0,1):"Right",(0,-1):"Left",(1,0):"Down",(-1,0):"Up"}
	path_directions = []
	for i in range(len(path)-1):
		diff = (-path[i][0]+path[i+1][0],-path[i][1]+path[i+1][1])
		path_directions.append(directions[diff])
	return path_directions
def esSitioPeligroso(pos,estado):
	'''Devuelve True si `pos` es una posicion peligrosa en `estado`
	   pos es una tupla (x,y)
	   estado es un state
	'''
	i = pos[1]-1
	while not MUROS[pos[0]][i] and (pos[0],i) not in estado.rocas:
		i-=1
	if (pos[0],i) in SERPIENTES:
		return True
	i = pos[1]+1
	while not MUROS[pos[0]][i] and (pos[0],i) not in estado.rocas:
		i+=1
	if (pos[0],i) in SERPIENTES:
		return True
	return False
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
salida = (None,None)
rocas = []
al = (None,None)

f = open('lab_astar/lab4.map','r')
archivo = f.read()
f.close()
archivo = archivo.split('\n')
for i in range(len(archivo)):
	fila = []
	for j in range(len(archivo[i])):
		if archivo[i][j] == 'A':
			al = (i,j)
		if archivo[i][j] == 'E':
			salida = (i,j)
		if archivo[i][j] == 'O':
			rocas.append((i,j)) 
		if archivo[i][j] == 'K':
			LLAVES.append((i,j))
		if archivo[i][j] == 'S':
			SERPIENTES.append((i,j))
		fila.append(True) if archivo[i][j] == '%' or archivo[i][j] == 'E' or archivo[i][j] == 'S' else fila.append(False)
	MUROS.append(fila)
print("MUROS:")
[print(m) for m in MUROS]
print("LLAVES:",LLAVES)
print("SERPIENTES:",SERPIENTES)
print("SALDIA:",salida)
I = node(None, 0, state(al, rocas, [False]*len(LLAVES)))
astar()