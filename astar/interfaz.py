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
	blueprint = None
	screen = None
	llaves = None
	def __init__(self,blueprint, llaves):
		self.blueprint = blueprint
		self.llaves = llaves
		# initialize the pygame module
		pygame.init()
		# load and set the logo
		pygame.display.set_caption("minimal program")
		# create a surface on screen that has the size of 240 x 180
		self.screen = pygame.display.set_mode((len(self.blueprint[0])*32,(len(self.blueprint))*32))
		self.screen.fill((0,0,0))
		for i in range(len(self.blueprint)):
			for j in range(len(self.blueprint[i])):
				if self.blueprint[i][j] != ' ':
					self.screen.blit(self.imagenes[self.blueprint[i][j]], (j*32,i*32))
		pygame.display.flip()
	def draw(self, estado):
		mapa = [row[:] for row in self.blueprint]
		if self.blueprint[estado.al[0]][estado.al[1]]  == 'E':
			pygame.draw.rect(self.screen,(0,0,0),(estado.al[1]*32,estado.al[0]*32,32,32))
		self.screen.blit(self.imagenes['A'], (estado.al[1]*32,estado.al[0]*32))
		for r in estado.rocas:
			self.screen.blit(self.imagenes['O'], (r[1]*32,r[0]*32))
		for k in range(len(self.llaves)):
			if not estado.llaves[k]:
				self.screen.blit(self.imagenes['K'], (self.llaves[k][1]*32,self.llaves[k][0]*32))
		pygame.display.flip()
	def vaciar(self):
		for i in range(len(self.blueprint)):
			for j in range(len(self.blueprint[i])):
				if self.blueprint[i][j] == ' ':
					pygame.draw.rect(self.screen,(0,0,0),(j*32,i*32,32,32))
		pygame.display.flip()