import pygame,sys,random
from pygame.math import Vector2

class COBRA:
	def __init__(self):
		self.corpo = [Vector2(8,15),Vector2(7,15),Vector2(6,15)]
		self.direcao = Vector2(0,0)
		self.novo_bloco = False

		self.cabeca_cima = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.cabeca_baixo = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.cabeca_direita = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.cabeca_esquerda = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.rabo_cima = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.rabo_baixo = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.rabo_direita = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.rabo_esquerda = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.corpo_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.corpo_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.corpo_rd = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.corpo_re = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.corpo_cd = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.corpo_ce = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.som_mordida = pygame.mixer.Sound('Sound/crunch.wav')
		
	def desenha_cobra(self):
		self.atualiza_imagens_cabeca()
		self.atualiza_imagens_rabo()

		for index, bloco in enumerate(self.corpo):
			x_pos = int(bloco.x * tamanho_celula)
			y_pos = int(bloco.y * tamanho_celula)
			bloco_rect = pygame.Rect(x_pos,y_pos,tamanho_celula, tamanho_celula)

			if index == 0:
				tela.blit(self.cabeca,bloco_rect)
			elif index == len(self.corpo) - 1:
				tela.blit(self.rabo,bloco_rect)
			else:
				bloco_anterior = self.corpo[index + 1] - bloco
				proximo_bloco = self.corpo[index - 1] - bloco
				if bloco_anterior.x == proximo_bloco.x:
					tela.blit(self.corpo_vertical,bloco_rect)
				elif bloco_anterior.y == proximo_bloco.y:
					tela.blit(self.corpo_horizontal,bloco_rect)
				else:
					if bloco_anterior.x == -1 and proximo_bloco.y == -1 or bloco_anterior.y == -1 and proximo_bloco.x == -1:
						tela.blit(self.corpo_re,bloco_rect)
					elif bloco_anterior.x == -1 and proximo_bloco.y == 1 or bloco_anterior.y == 1 and proximo_bloco.x == -1:
						tela.blit(self.corpo_ce,bloco_rect)
					elif bloco_anterior.x == 1 and proximo_bloco.y == -1 or bloco_anterior.y == -1 and proximo_bloco.x == 1:
						tela.blit(self.corpo_rd,bloco_rect)
					elif bloco_anterior.x == 1 and proximo_bloco.y == 1 or bloco_anterior.y == 1 and proximo_bloco.x == 1:
						tela.blit(self.corpo_cd,bloco_rect)

	def atualiza_imagens_cabeca(self):
		cabeca_atual = self.corpo[1] - self.corpo[0]
		if cabeca_atual == Vector2(1,0): self.cabeca = self.cabeca_esquerda
		elif cabeca_atual == Vector2(-1,0): self.cabeca = self.cabeca_direita
		elif cabeca_atual == Vector2(0,1): self.cabeca = self.cabeca_cima
		elif cabeca_atual == Vector2(0,-1): self.cabeca = self.cabeca_baixo

	def atualiza_imagens_rabo(self):
		rabo_atual = self.corpo[-2] - self.corpo[-1]
		if rabo_atual == Vector2(1,0): self.rabo = self.rabo_esquerda
		elif rabo_atual == Vector2(-1,0): self.rabo = self.rabo_direita
		elif rabo_atual == Vector2(0,1): self.rabo = self.rabo_cima
		elif rabo_atual == Vector2(0,-1): self.rabo = self.rabo_baixo

	def movimenta_cobra(self):
		if self.novo_bloco == True:
			copia_corpo = self.corpo[:]
			copia_corpo.insert(0, copia_corpo[0] + self.direcao)
			self.corpo = copia_corpo[:]
			self.novo_bloco = False
		else:
			copia_corpo = self.corpo[:-1]
			copia_corpo.insert(0, copia_corpo[0] + self.direcao)
			self.corpo = copia_corpo[:]

	def adiciona_novo_bloco(self):
		self.novo_bloco = True

	def toca_som_morida(self):
		self.som_mordida.play()

	def reset(self):
		self.corpo = [Vector2(8,15),Vector2(7,15),Vector2(6,15)]
		self.direcao = Vector2(0,0)


class FRUTA:
	def __init__(self):
		self.randomize()

	def desenha_fruta(self):
		fruta_rect = pygame.Rect(int(self.pos.x * tamanho_celula),int(self.pos.y * tamanho_celula), tamanho_celula, tamanho_celula)
		tela.blit(apple, fruta_rect)

	def randomize(self):
		self.x = random.randint(0,numero_celulas - 1)
		self.y = random.randint(0,numero_celulas - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
	def __init__(self):
		self.cobra = COBRA()
		self.fruta = FRUTA()

	def update(self):
		self.cobra.movimenta_cobra()
		self.verifica_colisao()
		self.verifica_perdeu()

	def desenha_elementos(self):
		self.desenha_grama()
		self.fruta.desenha_fruta()
		self.cobra.desenha_cobra()
		self.desenha_score()

	def verifica_colisao(self):
		if self.fruta.pos == self.cobra.corpo[0]:
			self.fruta.randomize()
			self.cobra.adiciona_novo_bloco()
			self.cobra.toca_som_morida()

		for bloco in self.cobra.corpo[1:]:
			if bloco == self.fruta.pos:
				self.fruta.randomize()

	def verifica_perdeu(self):
		if not 0 <= self.cobra.corpo[0].x < numero_celulas or not 0 <= self.cobra.corpo[0].y < numero_celulas:
			self.game_over()

		for bloco in self.cobra.corpo[1:]:
			if bloco == self.cobra.corpo[0]:
				self.game_over()
		
	def game_over(self):
		self.cobra.reset()

	def desenha_grama(self):
		cor_grama = (167,209,61)
		for row in range(numero_celulas):
			if row % 2 == 0: 
				for col in range(numero_celulas):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * tamanho_celula, row * tamanho_celula, tamanho_celula, tamanho_celula)
						pygame.draw.rect(tela,cor_grama,grass_rect)
			else:
				for col in range(numero_celulas):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * tamanho_celula, row * tamanho_celula, tamanho_celula, tamanho_celula)
						pygame.draw.rect(tela,cor_grama,grass_rect)			

	def desenha_score(self):
		texto_score = str(len(self.cobra.corpo) - 3)
		superficie_score = game_font.render(texto_score,True,(56,74,12))
		score_x = int(tamanho_celula * numero_celulas - 60)
		score_y = int(tamanho_celula * numero_celulas - 40)
		score_rect = superficie_score.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(tela,(167,209,61),bg_rect)
		tela.blit(superficie_score,score_rect)
		tela.blit(apple,apple_rect)
		pygame.draw.rect(tela,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
tamanho_celula = 40
numero_celulas = 20
tela = pygame.display.set_mode((numero_celulas * tamanho_celula, numero_celulas * tamanho_celula))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if evento.type == SCREEN_UPDATE:
			main_game.update()
		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_UP:
				if main_game.cobra.direcao.y != 1:
					main_game.cobra.direcao = Vector2(0,-1)
			if evento.key == pygame.K_RIGHT:
				if main_game.cobra.direcao.x != -1:
					main_game.cobra.direcao = Vector2(1,0)
			if evento.key == pygame.K_DOWN:
				if main_game.cobra.direcao.y != -1:
					main_game.cobra.direcao = Vector2(0,1)
			if evento.key == pygame.K_LEFT:
				if main_game.cobra.direcao.x != 1:
					main_game.cobra.direcao = Vector2(-1,0)

	tela.fill((175,215,70))
	main_game.desenha_elementos()
	pygame.display.update()
	clock.tick(60)