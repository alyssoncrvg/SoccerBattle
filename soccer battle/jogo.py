import pygame
from pygame.locals import *
import random
pygame.init()
pygame.mixer.init()

# VARIÁVEIS

largura = 800
altura = 600
clock = pygame.time.Clock()
intro = True
jogando = True
rodar_creditos = True
divisao_tela = largura//2


#DESENHANDO A TELA
tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Soccer Battle')

#IMAGENS
bola = pygame.image.load('spritsheet/bola_2.png').convert_alpha()
bola_scale = pygame.transform.scale(bola, (60, 60))

bola_45 = pygame.image.load('spritsheet/bola_2_45.png').convert_alpha()
bola_scale_45 = pygame.transform.scale(bola_45, (120, 120))

bola_inimigo = pygame.image.load('spritsheet/bola.png').convert_alpha()
bola_inimigo_scale = pygame.transform.scale(bola_inimigo, (60, 60))
img_with_flip = pygame.transform.flip(bola_inimigo_scale, True, False)

bola_inimigo_45 = pygame.image.load('spritsheet/bola_45.png').convert_alpha()
bola_inimigo_scale_45 = pygame.transform.scale(bola_inimigo_45, (120, 120))

jogador_vasco = pygame.image.load('spritsheet/jogadorvasco.png').convert_alpha()
jogador_vasco_scale = pygame.transform.scale(jogador_vasco, (80*2,150))

jogador_inimigo = pygame.image.load('spritsheet/jogadorinimigo.png').convert_alpha()
jogador_inimigo_scale = pygame.transform.scale(jogador_inimigo, (80*2,150))
jogador_inimigo_inverter = pygame.transform.flip(jogador_inimigo_scale, True, False)
vasco_img_creditos = pygame.image.load('imagens/vasco_img.png').convert_alpha()

#BOTÕES
vasco_img = pygame.image.load('imagens/vasco.png').convert_alpha()
mau_img = pygame.image.load('imagens/timedomau.png').convert_alpha()
sim_img = pygame.image.load('imagens/sim_1.png').convert_alpha()
nao_img = pygame.image.load('imagens/nao_1.png').convert_alpha()

#MUSICAS
hit = pygame.mixer.Sound('sons/hit.wav')
hit.set_volume(1)
som_ataque = pygame.mixer.Sound('sons/ataque.wav')
som_ataque.set_volume(1)


#CLASSES
class Botao():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.click = False
    
    def desenhar(self):
        acao = False
        #PEGAR POSIÇÃO DO MOUSE
        pos = pygame.mouse.get_pos()
        
        #CHECAR SE MOUSE CLICA IMAGEM
        if self.rect.collidepoint(pos):
            #CLICAR COM O BOTÃO ESQUERDO, O [2] REPRESENTA BOTÃO DIREITO E ==1 REPRESENTA CLICADO
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                acao = True
            #IMAGEM NÃO CLICADA
            if pygame.mouse.get_pressed()[0] == 0:
                self.click == False
        
        #DESENHAR IMAGEM NA TELA
        tela.blit(self.image, (self.rect.x, self.rect.y))

        return acao

class Personagem():
    def __init__(self,x,y_pos):
        self.x = x
        self.y = y_pos
        y_pos_ini = y_pos
        self.rect = pygame.Rect((self.x,self.y, 40, 90))
        self.x_ataque = self.rect.centerx
        self.y_pos_ini = y_pos_ini
        self.y_ataque = self.rect.y
        self.pulo = False
        self.life = 100
        self.atacar = False
        self.dano = 20
        self.ataquecima = False
        self.vitorias = 0

    def desenharPersonagem(self, surface):
        surface.blit(jogador_vasco_scale,(self.rect.x, self.rect.y-60))
        

    def pular(self):
        self.pulo = True
    
    def moverDireita(self):
        if self.rect.right < divisao_tela:
            self.rect.x += 5
    
    def moverEsquerda(self):
        if self.rect.x >0:
            self.rect.x -= 5

    def ataque(self):
        self.atacar = True
    
    def ataqueCima(self):
        self.ataquecima = True

    def update(self, alvo):
        if self.pulo:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 10
                
        else:
            if self.rect.y < self.y_pos_ini:
                self.rect.y +=10
            else:
                self.rect.y = self.y_pos_ini
                self.pulando = False

        if self.atacar:
            attack = pygame.Rect(self.x_ataque + 45, self.y_ataque + 30, 60, 60)
            tela.blit(bola_scale, (self.x_ataque + 45, self.y_ataque + 30))
            self.x_ataque += 10

            if attack.colliderect(alvo.rect):
                hit.play()
                self.x_ataque = self.rect.x
                self.atacar = False
                inimigo.life -= self.dano


            if self.x_ataque > largura:
                self.x_ataque = self.rect.x
                self.atacar = False
        
        if self.ataquecima:
            attack = pygame.Rect(self.x_ataque, self.y_ataque , 60, 60)
            tela.blit(bola_scale_45, (self.x_ataque, self.y_ataque))
            self.x_ataque +=20
            self.y_ataque -= 7

            if self.x_ataque > largura:
                self.x_ataque = self.rect.x
                self.y_ataque = self.rect.y
                self.ataquecima = False

            if attack.colliderect(alvo.rect):
                hit.play()
                self.x_ataque = self.rect.x
                self.y_ataque = self.y_pos_ini
                self.ataquecima = False
                inimigo.life -= self.dano
     
class Inimigo():
    def __init__(self,x,y_pos):
        self.x = x
        self.y = y_pos
        y_pos_ini = y_pos
        self.rect = pygame.Rect((self.x, self.y, 40, 90))
        self.x_ataque = self.rect.centerx
        self.y_pos_ini = y_pos_ini
        self.y_ataque = self.rect.y
        self.pulo = False
        self.life = 100
        self.atacar = False
        self.dano = 20
        self.ataquecima = False
        self.vitorias = 0

    
    def desenharInimigo(self, surface):
        surface.blit(jogador_inimigo_inverter,(self.rect.x - 120, self.rect.y-60))

    def pular(self):
        self.pulo = True
    
    def moverDireita(self):
        if self.rect.right < largura:
            self.rect.x += 5
    
    def moverEsquerda(self):
        if self.rect.left > divisao_tela:
            self.rect.x -= 5

    def ataque(self):
        self.atacar = True
    
    def ataqueCima(self):
        self.ataquecima = True

    def update(self, alvo):
        if self.pulo:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 10
                
        else:
            if self.rect.y < self.y_pos_ini:
                self.rect.y +=10
            else:
                self.rect.y = self.y_pos_ini
                self.pulando = False

        if self.atacar:
            attack = pygame.Rect(self.x_ataque - 50 , self.y_ataque + 30, 60, 60)
            tela.blit(img_with_flip, (self.x_ataque - 50, self.y_ataque + 30))
            self.x_ataque -= 10

            if attack.colliderect(alvo.rect):
                hit.play()
                self.x_ataque = self.rect.x
                self.atacar = False
                player.life -= self.dano

            if self.x_ataque < 0:
                self.x_ataque = self.rect.x
                self.atacar = False
        
        if self.ataquecima:
            attack = pygame.Rect(self.x_ataque, self.y_ataque , 60, 60)
            tela.blit(bola_inimigo_scale_45, (self.x_ataque, self.y_ataque))
            self.x_ataque -= 20
            self.y_ataque -= 7

            if self.x_ataque < -0:
                self.x_ataque = self.rect.x
                self.y_ataque = self.rect.y
                self.ataquecima = False

            if attack.colliderect(alvo.rect):
                hit.play()
                self.x_ataque = self.rect.x
                self.y_ataque = self.y_pos_ini
                self.ataquecima = False
                player.life -= self.dano
                
class Creditos():
    def __init__(self, texto,x,y):
        self.texto = texto
        self.x = x
        self.y = y
    
    def escreverTextoCreditos(self):
        img = fonte_creditos.render(self.texto,True, (255,255,255))
        tela.blit(img,(self.x ,self.y))
    
    def update(self):
        self.y -= 2

class CreditosVasco():
    def __init__(self, image):
        self.altura_img = image.get_height()
        self.largura = image.get_height()
        self.img = image
        self.x = largura//2 - self.largura//2
        self.y = altura + 370

    def desenharImg(self):
        tela.blit(self.img, (self.x, self.y))
    
    def update(self):
        if self.y > largura//2 - self.altura_img//2 - 100:
            self.y -= 2

#INSTACIAR BOTÕES
botao_vasco = Botao(120,400, vasco_img, 0.5)
botao_mau = Botao(470,400, mau_img,0.4)
botao_sim = Botao(250,400, sim_img, 0.5)
botao_nao = Botao(450,400, nao_img, 0.5)

#INSTANCIAR PERSONAGENS
player = Personagem(0,477)
inimigo = Inimigo(755,477)

#INSTANCIAR CREDITOS
roteiro = Creditos('Roteiro:', largura//2 -10, altura + 50)
nome_roteiro = Creditos('Alysson Pereira', largura//2 - 50, altura + 90)
persongens = Creditos('Personagens:', largura//2 - 35, altura + 130)
nome_personagens = Creditos('Alysson Pereira', largura//2 - 50, altura + 170)
trilha_sonora = Creditos('Trilha Sonora:', largura//2 - 40, altura + 210)
nome_trilha_sonora = Creditos('Alguns canais do youtube', largura//2 - 90, altura + 250)
instagram = Creditos('Instragram:', largura//2 - 20, altura+ 290)
nome_instagram = Creditos('@alyssoncrvg', largura//2 -40, altura + 330)
vasco_creditos = CreditosVasco(vasco_img_creditos)

#TELA DE FUNDO
cenario_montanha = pygame.image.load("imagens/cenario_montanhas.jpg").convert_alpha()
cenario_estadio = pygame.image.load("imagens/estadio.png").convert_alpha()
cenario_pantano = pygame.image.load("imagens/cenario_pantano.jpg").convert_alpha()
cenario_rodivia = pygame.image.load("imagens/cenario_rodovia.png").convert_alpha()

cenarios = [cenario_estadio, cenario_montanha, cenario_pantano, cenario_rodivia]

#FUNÇÕES
def desenharBackground(background):
    escala_bg = pygame.transform.scale(background,(largura, altura) )
    tela.blit(escala_bg, (0,0))

def sortearBackground():
    sortear = random.randint(0,len(cenarios)-1)
    print(f'foi sorteado o {sortear}')
    return sortear

#BARRA DE SAÚDE
def desenharBarraSaude(saude,x,y):
    barra_vida = saude/100
    pygame.draw.rect(tela, (255,255,255), (x -2,y-2, 202, 32))
    pygame.draw.rect(tela, (255,0,0), (x,y, 200, 30))
    pygame.draw.rect(tela, (255,255,0), (x,y, 200 * barra_vida, 30) )

#FONTES
fonte = pygame.font.Font('fontes/Turok.ttf', 80)
fontevitoria = pygame.font.Font('fontes/Turok.ttf', 40)
font = pygame.font.SysFont('arial', 40, True, False)
fonte_creditos = pygame.font.SysFont('arial', 20, True, False)

def escreverTexto(texto, x, y):
    img = fonte.render(texto, True, (255,0,0))
    tela.blit(img, (x,y))

def escreverTextoVitoria(texto, x, y):
        img = fontevitoria.render(texto, True, (255,255,0))
        tela.blit(img, (x,y))

def start_game():
    global intro
    intro = True
    pygame.mixer.music.load('sons/Amigadaminhamulher.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    while intro:

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
        #COR DE FUNDO TELA
        tela.fill((202, 228, 241))

        #CAIXA DE TEXTO
        mensagem = f'Player 1 escolher seu Time'
        texto_format = font.render(mensagem, True, (0,0,0))

        tela.blit(texto_format, (170, 50))

        #DESENHAR BOTÕES NA TELA
        if botao_vasco.desenhar():
            intro = False
            pygame.mixer.music.stop()
        if botao_mau.desenhar():
            x = random.randint(220,600)
            y = random.randint(60, 600)
            botao_mau.__init__(x,y,mau_img,0.4)
            
        pygame.display.update()     
        clock.tick(15)  

def jogo():
    global jogando
    contagem = 3
    atualizar_contagem = pygame.time.get_ticks()
    jogando = True
    sorteio_cenario = sortearBackground()
    pygame.mixer.music.load('sons/Minadocondominio.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    

    while jogando:
        desenharBackground(cenarios[sorteio_cenario])
        
        #PLACAR
        escreverTexto(f'{player.vitorias}:{inimigo.vitorias}',350,10)

        #CONTAGEM
        if contagem <=0:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    
                    if event.type == KEYDOWN:
                        #PULAR
                        if event.key == K_w:
                            if player.rect.y != player.y_pos_ini:
                                pass
                            else:
                                player.pular()

                        if event.key == K_UP:
                            if inimigo.rect.y != inimigo.y_pos_ini:
                                pass
                            else:
                                inimigo.pular()
                        
                        if not player.atacar and not player.ataquecima:
                            if event.key == K_f:
                                    player.x_ataque = player.rect.x
                                    if player.rect.y != player.y_pos_ini: 
                                        pass
                                    else:
                                        som_ataque.play()
                                        player.ataque()
                        
                        if not inimigo.atacar and not inimigo.ataquecima:
                            if event.key == K_DOWN:
                            
                                inimigo.x_ataque = inimigo.rect.x
                                if inimigo.rect.y != inimigo.y_pos_ini: 
                                    pass
                                else:
                                    som_ataque.play()
                                    inimigo.ataque()

                        if not player.atacar and not player.ataquecima:
                            if event.key == K_e:
                                player.x_ataque = player.rect.x
                                player.y_ataque = player.rect.y
                                if player.rect.y != player.y_pos_ini: 
                                    pass
                                else:
                                    som_ataque.play()
                                    player.ataqueCima()
                        
                        if not inimigo.atacar and not inimigo.ataquecima:
                            if event.key == K_RSHIFT:
                                inimigo.x_ataque = inimigo.rect.x
                                inimigo.y_ataque = inimigo.rect.y
                                if inimigo.rect.y != inimigo.y_pos_ini: 
                                    pass
                                else:
                                    som_ataque.play()
                                    inimigo.ataqueCima()
                        
            #PRESSIONAR TECLADO
            keys = pygame.key.get_pressed()
            #MOVER PARA A DIREITA
            if keys[pygame.K_d]:
                player.moverDireita()
            #MOVER PARA A ESQUERDA
            if keys[pygame.K_a]:
                player.moverEsquerda()     
            if keys[pygame.K_LEFT]:
                inimigo.moverEsquerda() 
            if keys[pygame.K_RIGHT]:
                inimigo.moverDireita()    
            

        else:
                #CAIXA DE TEXTO
                escreverTexto(str(contagem),largura//2, altura//3)
                
                if (pygame.time.get_ticks() - atualizar_contagem) >= 1000:
                    contagem -= 1
                    atualizar_contagem = pygame.time.get_ticks()
                    print(contagem)
        
        

        player.desenharPersonagem(tela)
      
        inimigo.desenharInimigo(tela)

        #DESENHAR SAÚDE NA TELA
        desenharBarraSaude(player.life, 30, 40)
        desenharBarraSaude(inimigo.life, 570, 40)

        player.update(inimigo)

        inimigo.update(player)

        if inimigo.life <= 0:
            player.dano = 0
            inimigo.dano = 0
            player.vitorias += 1
            inimigo.life += 0.01

        if inimigo.life== 0.01:
            pygame.mixer.music.pause()
            escreverTextoVitoria(f'O VASCARLHÃO VENÇEU!!!',200,200)
            escreverTextoVitoria('Deseja continuar? ', 250, 300)
            escreverTextoVitoria('Pressione S p/ Sim ou N p/ Não ', 100, 400)

            if keys[pygame.K_s]:
                player.rect.x = player.x
                player.rect.y = player.y_pos_ini
                inimigo.rect.x = inimigo.x
                inimigo.rect.y = inimigo.y_pos_ini
                inimigo.life= 100
                player.life = 100
                player.dano = 20
                inimigo.dano = 20
                contagem = 4
                sorteio_cenario = sortearBackground()
                pygame.mixer.music.unpause()
                continue
            
            if keys[pygame.K_n]:
                pygame.mixer.music.stop()
                jogando = False
        
        if player.life <= 0 and inimigo.life!=player.life:
            inimigo.vitorias += 1
            player.life += 0.01
            player.dano = 0
            inimigo.dano = 0

        if player.life==0.01 and inimigo.life!=player.life:
            pygame.mixer.music.pause()
            escreverTextoVitoria(f"TIME DO MAU VENCEU :'(",200,200)
            escreverTextoVitoria('Deseja continuar? ', 250, 300)
            escreverTextoVitoria('Pressione S p/ Sim ou N p/ Não ', 100, 400)

            if keys[pygame.K_s]:
                player.rect.x = player.x
                player.rect.y = player.y_pos_ini
                inimigo.rect.x = inimigo.x
                inimigo.rect.y = inimigo.y_pos_ini
                player.life= 100
                inimigo.life = 100
                contagem = 4
                player.dano = 20
                inimigo.dano = 20
                sorteio_cenario = sortearBackground()
                pygame.mixer.music.unpause()
                continue
            
            if keys[pygame.K_n]:
                pygame.mixer.music.stop()
                jogando = False

        pygame.display.update()     
        clock.tick(60) 

def creditos():
    pygame.mixer.music.load('sons/vascodagamaetime.mp3')
    pygame.mixer.music.play(-1)
    while rodar_creditos:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #COR DE FUNDO TELA
        tela.fill((0, 0, 0))
        roteiro.escreverTextoCreditos()
        nome_roteiro.escreverTextoCreditos()
        persongens.escreverTextoCreditos()
        nome_personagens.escreverTextoCreditos()
        trilha_sonora.escreverTextoCreditos()
        nome_trilha_sonora.escreverTextoCreditos()
        instagram.escreverTextoCreditos()
        nome_instagram.escreverTextoCreditos()
        vasco_creditos.desenharImg()


        roteiro.update()
        nome_roteiro.update()
        persongens.update()
        nome_personagens.update()
        trilha_sonora.update()
        nome_trilha_sonora.update()
        instagram.update()
        nome_instagram.update()
        vasco_creditos.update()

        
        pygame.display.update()     
        clock.tick(60) 


#LOOP DO JOGO
run = True
while run:
    clock.tick(30)
    if intro:
        start_game()

    if not intro and jogando:
        jogo()

    if not jogando and rodar_creditos:
        creditos()

    #CAPTURAR EVENTOS QUE ACONTECEM NO TECLADO
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #ATUALIZAR A TELA DO JOGO
    pygame.display.update()

pygame.quit()
