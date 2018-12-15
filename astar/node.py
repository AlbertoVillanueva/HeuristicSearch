from config import CONFIG
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
	def hayLlave(self, pos):
		'''Devuelve True si en el `estado` hay una llave en `pos`
		pos es una tupla (x,y)
		estado es un state
		'''
		if pos in LLAVES:
			return not self.llaves[LLAVES.index(pos)]
		return False
	def esFinal(self):
		'''Devuelve True si `N` es un estado final
		N es un node
		'''
		return self.al == tuple(SALIDA)
	def esSitioPeligroso(self, pos):
		'''Devuelve True si `pos` es una posicion peligrosa en `estado`
		pos es una tupla (x,y)
		estado es un state
		'''
		return self.haySerpienteIz(pos)[0] or self.haySerpienteDer(pos)[0]
	def haySerpienteIz(self, pos):
		'''Devuelve True si `pos` tiene una serpiente a la izquierda en `estado`
		Devuelve la posicion de la serpiente
		pos es una tupla (x,y)
		estado es un state
		'''
		i = pos[1]-1
		# Nos movemos hacia la izquierda hasta encontrar el primer muro o roca
		while not MUROS[pos[0]][i] and (pos[0],i) not in self.rocas:
			i-=1
		# Si es una serpiente es un sitio peligroso y devolvemos True
		return (pos[0],i) in SERPIENTES, (pos[0],i)
	def haySerpienteDer(self, pos):
		'''Devuelve True si `pos` tiene una serpiente a la derecha en `estado`
		Devuelve la posicion de la serpiente
		pos es una tupla (x,y)
		estado es un state
		'''
		i = pos[1]+1
		# Nos movemos hacia la derecha hasta encontrar el primer muro o roca
		while not MUROS[pos[0]][i] and (pos[0],i) not in self.rocas:
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
					hay, serpiente = self.estado.haySerpienteIz(LLAVES[i])
					if hay:
						coste += 2*min(self.taparSerpiente(serpiente,LLAVES[i],r) for r in self.estado.rocas)
					hay, serpiente = self.estado.haySerpienteDer(LLAVES[i])
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