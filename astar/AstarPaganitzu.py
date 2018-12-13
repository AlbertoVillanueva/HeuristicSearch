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
	
	return sucesores, id
		

def insertarOrdenado(lista, nodo):
def backtracking():
def esSitioPeligroso(nuevaPos):
def hayLlave(pos):
	if pos in LLAVES:
		return not estado.llaves[LLAVES.index(pos)]):
	return False