class estado():
	al = None
	rocas = None
	llaves = None
	def __init__(self, al, rocas, llaves):
		self.al = al
		self.rocas = rocas
		self.llaves = llaves
class node():
	id = None
	padre = None
	g = None
	f = None
	estado = None
	def h(self):
		return 1
	def __init__(self, id, padre, c, estado):
		self.id = id
		self.padre = padre
		self.g = padre.g+c
		self.f = self.g + self.h()
		self.estado = estado

MUROS=[]
LLAVES = []
SERPIENTES = []
salida = (None,None)
rocas = []
al = (None,None)
f = open('lab_astar/lab1.map','r')
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
id = 0
I = node(id, None, 0, estado(al, rocas, [False]*len(LLAVES)))
def astar():
	ABIERTA = [I,]
	CERRADA = []
	EXITO = False
	while(ABIERTA != [] or EXITO):
		id+=1
		N = ABIERTA[0]
		ABIERTA.pop(0)
		if esFinal(N): 
			EXITO = True
		else:
			S,id = genSucesores(N,id)
			for s in S:
				if s not in CERRADA:
					insertarOrdenado(ABIERTA,s)
	if EXITO:
		print(backtracking(N))	
	else:
		print("Fracaso")
def esFinal(N):
	return N.estado.al == salida
def genSucesores(nodo, id):
	estado = nodo.estado
	sucesores = []
	#mover hacia arriba
	nuevaPos = (estado.al[0],estado.al[1]+1)
	if sum(estado.llaves) == len(LLAVES) and nuevaPos == salida:
		sucesores.append(node(id ,nodo,2, estado(nuevaPos,estado.rocas,estado.llaves)))
		id+=1
	elif not MUROS[nuevaPos[0]][nuevaPos[1]] and esSitioPeligroso(nuevaPos):
		if nuevaPos in estado.rocas:
			unaMasHaciaEsaDireccionPrimo = (nuevaPos[0],nuevaPos[1]+1)
			if not(unaMasHaciaEsaDireccionPrimo in estado.rocas or MUROS[unaMasHaciaEsaDireccionPrimo[0]][unaMasHaciaEsaDireccionPrimo[1]] or hayLlave(unaMasHaciaEsaDireccionPrimo)):
				nuevasRocas = estado.rocas[:]
				nuevasRocas.remove(nuevaPos)
				nuevasRocas.append(unaMasHaciaEsaDireccionPrimo)
				sucesores.append(node(id ,nodo, 4, estado(nuevaPos,nuevasRocas,estado.llaves)))
				id+=1
		else:
			nuevasLlaves = estado.llaves[:]
			if nuevaPos in LLAVES:
				nuevasLlaves[LLAVES.index(nuevaPos)] = True
			sucesores.append(node(id ,nodo, 2, estado(nuevaPos,nuevasRocas,nuevasLlaves)))
			id+=1
	#mover hacia abajo
	nuevaPos = (estado.al[0],estado.al[1]-1)
	if sum(estado.llaves) == len(LLAVES) and nuevaPos == salida:
		sucesores.append(node(id ,nodo,2, estado(nuevaPos,estado.rocas,estado.llaves)))
		id+=1
	elif not MUROS[nuevaPos[0]][nuevaPos[1]] and esSitioPeligroso(nuevaPos):
		if nuevaPos in estado.rocas:
			unaMasHaciaEsaDireccionPrimo = (nuevaPos[0],nuevaPos[1]-1)
			if not(unaMasHaciaEsaDireccionPrimo in estado.rocas or MUROS[unaMasHaciaEsaDireccionPrimo[0]][unaMasHaciaEsaDireccionPrimo[1]] or hayLlave(unaMasHaciaEsaDireccionPrimo)):
				nuevasRocas = estado.rocas[:]
				nuevasRocas.remove(nuevaPos)
				nuevasRocas.append(unaMasHaciaEsaDireccionPrimo)
				sucesores.append(node(id ,nodo, 4, estado(nuevaPos,nuevasRocas,estado.llaves)))
				id+=1
		else:
			nuevasLlaves = estado.llaves[:]
			if nuevaPos in LLAVES:
				nuevasLlaves[LLAVES.index(nuevaPos)] = True
			sucesores.append(node(id ,nodo, 2, estado(nuevaPos,nuevasRocas,nuevasLlaves)))
			id+=1
	#mover hacia izquierda
	nuevaPos = (estado.al[0]-1,estado.al[1])
	if sum(estado.llaves) == len(LLAVES) and nuevaPos == salida:
		sucesores.append(node(id ,nodo,2, estado(nuevaPos,estado.rocas,estado.llaves)))
		id+=1
	elif not MUROS[nuevaPos[0]][nuevaPos[1]] and esSitioPeligroso(nuevaPos):
		if nuevaPos in estado.rocas:
			unaMasHaciaEsaDireccionPrimo = (nuevaPos[0]-1,nuevaPos[1])
			if not(unaMasHaciaEsaDireccionPrimo in estado.rocas or MUROS[unaMasHaciaEsaDireccionPrimo[0]][unaMasHaciaEsaDireccionPrimo[1]] or hayLlave(unaMasHaciaEsaDireccionPrimo)):
				nuevasRocas = estado.rocas[:]
				nuevasRocas.remove(nuevaPos)
				nuevasRocas.append(unaMasHaciaEsaDireccionPrimo)
				sucesores.append(node(id ,nodo, 4, estado(nuevaPos,nuevasRocas,estado.llaves)))
				id+=1
		else:
			nuevasLlaves = estado.llaves[:]
			if nuevaPos in LLAVES:
				nuevasLlaves[LLAVES.index(nuevaPos)] = True
			sucesores.append(node(id ,nodo, 2, estado(nuevaPos,nuevasRocas,nuevasLlaves)))
			id+=1
	#mover hacia derecha
	nuevaPos = (estado.al[0]+1,estado.al[1])
	if sum(estado.llaves) == len(LLAVES) and nuevaPos == salida:
		sucesores.append(node(id ,nodo,2, estado(nuevaPos,estado.rocas,estado.llaves)))
		id+=1
	elif not MUROS[nuevaPos[0]][nuevaPos[1]] and esSitioPeligroso(nuevaPos):
		if nuevaPos in estado.rocas:
			unaMasHaciaEsaDireccionPrimo = (nuevaPos[0]+1,nuevaPos[1])
			if not(unaMasHaciaEsaDireccionPrimo in estado.rocas or MUROS[unaMasHaciaEsaDireccionPrimo[0]][unaMasHaciaEsaDireccionPrimo[1]] or hayLlave(unaMasHaciaEsaDireccionPrimo)):
				nuevasRocas = estado.rocas[:]
				nuevasRocas.remove(nuevaPos)
				nuevasRocas.append(unaMasHaciaEsaDireccionPrimo)
				sucesores.append(node(id ,nodo, 4, estado(nuevaPos,nuevasRocas,estado.llaves)))
				id+=1
		else:
			nuevasLlaves = estado.llaves[:]
			if nuevaPos in LLAVES:
				nuevasLlaves[LLAVES.index(nuevaPos)] = True
			sucesores.append(node(id ,nodo, 2, estado(nuevaPos,nuevasRocas,nuevasLlaves)))
			id+=1
	return sucesores, id
def insertarOrdenado(lista, nodo):
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
			lista.insert(primero+1,nodo)

def backtracking(N):
	path = []
	nodo = N
	while nodo.padre != None:
		path.append(nodo.padre)
	return path
def esSitioPeligroso(pos):
	i = pos[1]-1
	while (pos[0],i) not in MUROS:
		i-=1
	if (pos[0],i) in SERPIENTES:
		return True
	i = pos[1]+1
	while (pos[0],i) not in MUROS:
		i+=1
	if (pos[0],i) in SERPIENTES:
		return True
	return False
def hayLlave(pos, estado):
	if pos in LLAVES:
		return not estado.llaves[LLAVES.index(pos)]):
	return False