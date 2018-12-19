from config import CONFIG
import time
MUROS=[]
LLAVES = []
SERPIENTES = []
SALIDA = []
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
		'''Devuelve True si `estado` es igual
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
	def hayLlave(self, pos):
		'''Devuelve True si hay una llave en `pos`
		   pos es una tupla (x,y)
		'''
		if pos in LLAVES:
			return not self.llaves[LLAVES.index(pos)]
		return False
	def esFinal(self):
		'''Devuelve True si es un estado final
		   N es un node
		'''
		return self.al == tuple(SALIDA)
	def esSitioPeligroso(self, pos):
		'''Devuelve True si `pos` es una posicion peligrosa
		   pos es una tupla (x,y)
		'''
		return self.haySerpienteIz(pos)[0] or self.haySerpienteDer(pos)[0]
	def haySerpienteIz(self, pos):
		'''Devuelve True si `pos` tiene una serpiente a la izquierda
		   Devuelve la posicion de la serpiente
		   pos es una tupla (x,y)
		'''
		i = pos[1]-1
		# Nos movemos hacia la izquierda hasta encontrar el primer muro o roca
		while not MUROS[pos[0]][i] and (pos[0],i) not in self.rocas:
			if self.hayLlave((pos[0],i)):
				break
			i-=1
		# Si es una serpiente es un sitio peligroso y devolvemos True
		return (pos[0],i) in SERPIENTES, (pos[0],i)
	def haySerpienteDer(self, pos):
		'''Devuelve True si `pos` tiene una serpiente a la derecha
		   Devuelve la posicion de la serpiente
		   pos es una tupla (x,y)
		'''
		i = pos[1]+1
		# Nos movemos hacia la derecha hasta encontrar el primer muro o roca
		while not MUROS[pos[0]][i] and (pos[0],i) not in self.rocas:
			if self.hayLlave((pos[0],i)):
				break
			i+=1
		# Si es una serpiente es un sitio peligroso y devolvemos True
		return (pos[0],i) in SERPIENTES, (pos[0],i)
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
	def __init__(self, padre, c, estado, heuristica):
		'''Inicializa el nodo dado el padre del nodo, el coste para llegar desde el padre hasta el nodo, y el estado del nuevo nodo
		   padre es un puntero a una instancia de node
		   c es un numero
		   estado es un state
		   heuristica es la heuristica que se usa
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
		if heuristica == "h1":
			self.f = self.g + self.h1()
		elif heuristica == "h2":
			self.f = self.g + self.h2()
		elif heuristica == "djk":
			self.f = self.g

	def h1(self):
		'''Devuelve el valor heuristico usando la primera heurística
		'''
		coste = 0
		# si quedan llaves añadir la distancia hasta la llave mas lejana y la distancia desde esa llave hasta la salida
		if self.estado.quedanLlaves():
			llaveLejos = max((self.distancia(LLAVES[k],self.estado.al),LLAVES[k]) for k in range(len(LLAVES)) if not self.estado.llaves[k])
			coste += 2*(llaveLejos[0] + self.distancia(llaveLejos[1],tuple(SALIDA)))
		# si no quedan llaves añadir la distancia hasta la salida
		else:
			coste += 2*self.distancia(self.estado.al,tuple(SALIDA))
		# para cada llave
		for i in range(len(LLAVES)):
			# si hay serpientes y aun no hemos cogido esta llave añadir el minimo coste para tapar la(s) serpiente que ponen en peligro la llave
			if SERPIENTES != [] and not self.estado.llaves[i]:
				hayIz, serpiente = self.estado.haySerpienteIz(LLAVES[i])
				if hayIz:
					coste += 2*min(self.taparSerpiente(serpiente,LLAVES[i],r) for r in self.estado.rocas)
				hayDer, serpiente = self.estado.haySerpienteDer(LLAVES[i])
				if hayDer:
					coste += 2*min(self.taparSerpiente(serpiente,LLAVES[i],r) for r in self.estado.rocas)
		return coste
	def h2(self):
		'''Devuelve el valor heuristico usando la segunda heurística
		'''
		coste = 0
		# si quedan llaves añadir la distancia hasta la llave mas lejana y la distancia desde esa llave hasta la salida
		if self.estado.quedanLlaves():
			llaveLejos = max((self.distancia(LLAVES[k],tuple(SALIDA)),LLAVES[k]) for k in range(len(LLAVES)) if not self.estado.llaves[k])
			coste += 2*(llaveLejos[0] + self.distancia(llaveLejos[1],self.estado.al))
		# si no quedan llaves añadir la distancia hasta la salida
		else:
			coste += 2*self.distancia(self.estado.al,tuple(SALIDA))
		# para cada llave
		for i in range(len(LLAVES)):
			# si hay serpientes y aun no hemos cogido esta llave añadir el minimo coste para tapar la(s) serpiente que ponen en peligro la llave
			if SERPIENTES != [] and not self.estado.llaves[i]:
				hayIz, serpiente = self.estado.haySerpienteIz(LLAVES[i])
				if hayIz:
					coste += 2*min(self.taparSerpiente(serpiente,LLAVES[i],r) for r in self.estado.rocas)
				hayDer, serpiente = self.estado.haySerpienteDer(LLAVES[i])
				if hayDer:
					coste += 2*min(self.taparSerpiente(serpiente,LLAVES[i],r) for r in self.estado.rocas)
		return coste
	def distancia(self, pos1, pos2):
		'''Devuelve la distancia desde `pos1` hasta `pos2`
		   pos1 es una tupla (x,y)
		   pos2 es una tupla (x,y)
		'''
		filas = abs(pos1[0]-pos2[0])
		columnas = abs(pos1[1]-pos2[1])
		return min(filas,columnas)-1+abs(filas-columnas)
	def manhattan(self, pos1, pos2):
		'''Devuelve la distancia manhattan desde `pos1` hasta `pos2`
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
			return min(self.manhattan(roca,(serpiente[0], huecoIz)),self.manhattan(roca,(serpiente[0], huecoDer)))
	def estaEn(self,l):
		'''Devuelve True si esta en la lista `l`
		   Devuelve la posicion del estado en `l`, si no esta en `l` devuelve None
		   l es una lista de node
		'''
		# Iteramos por toda la lista
		for i in range(len(l)):
			# Si el estado en i es igual devolvemos True y la posicion de dicho estado
			if self.estado.igual(l[i].estado):
				return True, i
		# Si ningun estado era igual devolvemos Flase y None por posicion
		return False, None
	def genSucesores(self,heuristica):
		'''Devuelve una lista con los sucesores
		'''
		# Iniciamos la lista de sucesores vacia
		sucesores = []
		# Definimos los posibles movimientos que se pueden realizar
		movimientos = [(1,0),(-1,0),(0,1),(0,-1)]
		diagonales = [(1,1),(-1,1),(1,-1),(-1,-1)]
		# Para casa posible movimiento m
		for m in movimientos:
			# Calculamos la nueva posicion para ese movimiento
			nuevaPos = (self.estado.al[0]+m[0],self.estado.al[1]+m[1])
			# Calculamos la nueva posicion para la roca (en caso de que moviera roca)
			nuevaPosRoca = (self.estado.al[0]+2*m[0],self.estado.al[1]+2*m[1])
			# Miramos si la accion es mover una roca
			mueveRoca = nuevaPos in self.estado.rocas
			# Miramos si la nueva posicion de la roca seria una llave
			nuevaPosRocaEsLlave = False
			if nuevaPos in LLAVES:
				if not self.estado.llaves[LLAVES.index(nuevaPos)]:
					nuevaPosRocaEsLlave = True
			# Si las precondiciones para mover una roca se cumplen
			if mueveRoca and not MUROS[nuevaPosRoca[0]][nuevaPosRoca[1]] and nuevaPosRoca not in self.estado.rocas and not nuevaPosRocaEsLlave and (m in movimientos[2:] or not self.estado.esSitioPeligroso(nuevaPos)):
				# Mueve la roca
				nuevasRocas = self.estado.rocas[:]
				nuevasRocas.remove(nuevaPos)
				nuevasRocas.append(nuevaPosRoca)
				# Se mueve
				sucesores.append(node(self, 4, state(nuevaPos,nuevasRocas,self.estado.llaves[:]),heuristica))
			# Si las precondiciones para moverse se cumplen
			elif (not mueveRoca and not MUROS[nuevaPos[0]][nuevaPos[1]] and not self.estado.esSitioPeligroso(nuevaPos)) or (not self.estado.quedanLlaves() and nuevaPos == tuple(SALIDA)):
				# Recoge la llave si la hay
				nuevasLlaves = self.estado.llaves[:]
				if nuevaPos in LLAVES:
					nuevasLlaves[LLAVES.index(nuevaPos)] = True
				# Se mueve
				sucesores.append(node(self, 2, state(nuevaPos,self.estado.rocas[:],nuevasLlaves),heuristica))
		# Para cada movimiento diagonal
		for d in diagonales:
			# Calculamos la nueva posicion para ese movimiento
			nuevaPos = (self.estado.al[0]+d[0],self.estado.al[1]+d[1])
			# Calculamos las posiciones de los muros adyacentes en esa direccion
			lateral1 = (self.estado.al[0],self.estado.al[1]+d[1])
			lateral2 = (self.estado.al[0]+d[0],self.estado.al[1])
			# si se cumplen las precondiciones
			if (not MUROS[nuevaPos[0]][nuevaPos[1]] and not((MUROS[lateral1[0]][lateral1[1]] or lateral1 in self.estado.rocas) and (MUROS[lateral2[0]][lateral2[1]] or lateral2 in self.estado.rocas)) and not self.estado.esSitioPeligroso(nuevaPos)) or (not self.estado.quedanLlaves() and nuevaPos == tuple(SALIDA)):
				# Recoge la llave si la hay
				nuevasLlaves = self.estado.llaves[:]
				if nuevaPos in LLAVES:
					nuevasLlaves[LLAVES.index(nuevaPos)] = True
				# Se mueve
				sucesores.append(node(self, 2, state(nuevaPos,self.estado.rocas[:],nuevasLlaves),heuristica))
		return sucesores
	def insertarOrdenado(self, lista):
		'''Inserta el nodo en `lista` ordenado de menor a mayor
		   En caso de empate inserta lo mas cercano al principio
		   lista es una lista de node
		'''
		# si la lista esta vacia insertamos el nodo
		if not len(lista):
			lista.append(self)
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
				if self.f == lista[medio].f:
					primero=medio
					break
				# Si f del nodo es mas pequeño que el medio buscamos en la mitad anterior
				elif self.f<lista[medio].f:
					ultimo=medio-1
				# Si f del nodo es mas grande que el medio buscamos en la mitad posterior
				elif self.f>lista[medio].f:
					primero=medio+1
			# Si f del nodo es mas pequeño lo insertamos antes
			if self.f<lista[primero].f:
				lista.insert(primero, self)
			# Si es mas grando lo insertamos despues
			elif self.f>lista[primero].f:
				lista.insert(primero+1, self)
			# Si f es igual
			else:
				# Retrocedemos hasta el primero nodo que tenga la misma f
				while lista[primero].f == self.f:
					primero-=1
					if primero == -1:
						break
				# Insertamos antes del primer nodo que es igual
				lista.insert(primero+1,self)
	def backtracking(self):
		'''Devuelve una lista con el camino que ha hecho para llegar hasta este nodo
		'''
		path = []
		nodo = self
		while nodo != None:
			path.append(nodo.estado.al)
			nodo = nodo.padre
		return path[:0:-1]
	def animar(self, ventana):
		estados = []
		nodo = self
		while nodo != None:
			estados.append(nodo.estado)
			nodo = nodo.padre
		estados = estados[::-1]
		for e in estados:
			ventana.vaciar()
			ventana.draw(e)
			time.sleep(CONFIG["velocidad"])