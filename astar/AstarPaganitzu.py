class state():
	al = None
	rocas = None
	llaves = None
	def __init__(self, al, rocas, llaves):
		self.al = al
		self.rocas = rocas
		self.llaves = llaves
class node():
	padre = None
	g = None
	f = None
	estado = None
	def __init__(self, padre, c, estado):
		self.padre = padre
		if padre != None:
			self.g = padre.g+c
		else:
			self.g = 0
		self.estado = estado
		self.f = self.g + self.h()
	def h(self):
		coste = 0
		if sum(self.estado.llaves) < len(self.estado.llaves):
			llaveLejos = max((abs(LLAVES[k][0]-self.estado.al[0])+abs(LLAVES[k][1]-self.estado.al[1]),LLAVES[k]) for k in range(len(LLAVES)) if not self.estado.llaves[k])
			return 2*(llaveLejos[0]+ abs(llaveLejos[1][0]-salida[0])+abs(llaveLejos[1][1]-salida[1]))
		return 2*(abs(self.estado.al[0]-salida[0])+abs(self.estado.al[1]-salida[1]))
	def estaEn(self,l):
		for i in range(len(l)):
			if self.estado.al == l[i].estado.al and self.estado.llaves == l[i].estado.llaves and sorted(self.estado.rocas) == sorted(l[i].estado.rocas):
				return True, i
		return False, None
def astar():
	ABIERTA = [I,]
	CERRADA = []
	EXITO = False
	while ABIERTA != [] and not EXITO:
		N = ABIERTA[0]
		ABIERTA.pop(0)
		if esFinal(N): 
			EXITO = True
		else:
			S = genSucesores(N)
			CERRADA.append(N)
			for s in S:
				estaEnAbierta, indice = s.estaEn(ABIERTA)
				if estaEnAbierta:
					if s.f < ABIERTA[indice].f:
						del ABIERTA[indice]
						insertarOrdenado(ABIERTA,s)
				else:
					estaEnCerrada, indice = s.estaEn(CERRADA)
					if not estaEnCerrada:
						insertarOrdenado(ABIERTA,s)
	if EXITO:
		print(backtracking(N))	
	else:
		print("Fracaso")
	
def esFinal(N):
	return N.estado.al == salida
def genSucesores(nodo):
	estado = nodo.estado
	sucesores = []
	movimientos = [(1,0),(-1,0),(0,1),(0,-1)]
	for m in movimientos:
		nuevaPos = (estado.al[0]+m[0],estado.al[1]+m[1])
		if sum(estado.llaves) == len(LLAVES) and nuevaPos == salida:
			sucesores.append(node(nodo,2, state(nuevaPos,estado.rocas[:],estado.llaves[:])))
		elif not MUROS[nuevaPos[0]][nuevaPos[1]] and not esSitioPeligroso(nuevaPos,estado):
			if nuevaPos in estado.rocas:
				unaMasHaciaEsaDireccionPrimo = (nuevaPos[0]+m[0],nuevaPos[1]+m[1])
				if not(unaMasHaciaEsaDireccionPrimo in estado.rocas or MUROS[unaMasHaciaEsaDireccionPrimo[0]][unaMasHaciaEsaDireccionPrimo[1]] or hayLlave(unaMasHaciaEsaDireccionPrimo,estado)):
					nuevasRocas = estado.rocas[:]
					nuevasRocas.remove(nuevaPos)
					nuevasRocas.append(unaMasHaciaEsaDireccionPrimo)
					sucesores.append(node(nodo, 4, state(nuevaPos,nuevasRocas,estado.llaves[:])))
			else:
				nuevasLlaves = estado.llaves[:]
				if nuevaPos in LLAVES:
					nuevasLlaves[LLAVES.index(nuevaPos)] = True
				sucesores.append(node(nodo, 2, state(nuevaPos,estado.rocas[:],nuevasLlaves)))
	return sucesores
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
				if primero == -1:
					break
			lista.insert(primero+1,nodo)

def backtracking(N):
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

#archivo='%%%%%%%%%%\n%    %%% %\n% O   K  E\n%A      %%\n%%%%%%%%%%\n'
#archivo='%%%%%%%%%%%%\n%A  K%%%   %\n% O        %\n%S      %%%%\n%%%%%E%%%%%%'
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