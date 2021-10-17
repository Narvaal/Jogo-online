import pygame
from pygame.cursors import sizer_x_strings, sizer_y_strings
from pygame.locals import *
from sys import exit, maxsize
import random
import pathlib
import socket


from pygame.sprite import collide_rect 

#################Parte Web
TCP_IP = 'xxx.xxx.x.xxx' # endereço IP do servidor 
TCP_PORTA = 41908       # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 1024     # definição do tamanho do buffer
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((TCP_IP, TCP_PORTA))
servidor.listen(1)
#print("Servidor dispoivel na porta 5005 e escutando.....") 
conn, addr = servidor.accept()
#print ('Endereço conectado:', addr)
data = ''
def Receber():
    data = conn.recv(TAMANHO_BUFFER)
    posx = 0
    posy = 0
    if data:

        print("[CLIENTE]Data recebida: " + str(data)) 
        try:
            data = str(data)[2:len(data)+2]
            array = data.split(",")
            data = int(array[0])
            posx = int(array[1])
            posy = int(array[2])
        except:
            pass
        #print(data) data tratada     
    return data,posx,posy 

def Enviar(env):
            MENSAGEM = env 
            print("[SERVIDOR]Data envaida" + env) 
            conn.send(MENSAGEM.encode('UTF-8'))



#################Parte pygame 
pygame.init()
pygame.mixer.init()
#Tamanho janela
Size_max_x = 500
Size_max_y = 700


# Cores
COR_P1 = (0,0,255)
COR_P2 = (255,0,0)
COR_BOLA = (0,255,0)
COR_FUNDO = (0,0,0)
COR_DETALHES = (255,255,255)

#Pos
P1_pos_x = 180
P1_pos_y = 10

P2_pos_x = 180
P2_pos_y = 680

Bola_pos_x = Size_max_x / 2
Bola_pos_y = Size_max_y / 2

P1_fora_tela_cima = Size_max_y - 20
P2_fora_tela = 9999

#speed
velocidade_bola_x = 4
velocidade_bola_y = 0
velocidade_x = 0
velocidade_y = 0


velocidade_p2 = 0
# Open a new window
size = (Size_max_y, Size_max_x)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong - Server")
Rodando = True
clock = pygame.time.Clock()
 
# Tamanho dos jogadores 
P1_tamanho = 100
P2_tamanho = 100
Bola_tamanho = 20

# Elementos do jogo
fundo_T = pygame.Surface((Size_max_y,Size_max_x))
fundo = pygame.draw.rect(fundo_T,COR_DETALHES ,(0,0, Size_max_y,Size_max_x))
campo = pygame.draw.rect(fundo_T,COR_FUNDO ,(10,10,Size_max_y - 20, Size_max_x - 20))
linha = pygame.draw.line(fundo_T, COR_DETALHES, [Size_max_y/2, 0], [Size_max_y/2, Size_max_x], 10)
fundo_T = fundo_T.convert()

Player1 = pygame.Rect(10,250, 10,100)
Player2 = pygame.Rect(680,250, 10,100)
Bola = pygame.Rect(*screen.get_rect().center, 0, 0).inflate(20, 20)

Alto_coli = pygame.Rect(0,0, Size_max_y,10)
Baixo_coli = pygame.Rect(0,Size_max_x-10, Size_max_y,10)

Ponto_p1 = pygame.Rect(0,0,10,Size_max_y)
Ponto_p2 = pygame.Rect(690,0,10,Size_max_y)

#flags 
flag_baixo = True
flag_baixo = True

#Objetos jogo
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial",100)
#Score 
bar1_score = 0
bar2_score = 0


#Play sound

l = str(pathlib.Path(__file__).parent.resolve())
effect1 = pygame.mixer.Sound(l +'\pong.wav')
effect2 = pygame.mixer.Sound(l + '\win.wav')



velocidade_jogo_tempo = 5


while Rodando:
    data,posx,posy = Receber()       
    Enviar(str(P1_pos_x) + "," + str(Bola.x) + "," + str(Bola.y) +  "," + str(velocidade_bola_x)+  "," +str(velocidade_bola_y))
    P2_pos_x = data
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
              Rodando = False 

        if event.type == KEYDOWN:
            if event.key == K_UP:
                velocidade_x -= velocidade_jogo_tempo     
                
                flag_cima = True
            elif event.key == K_DOWN:
                velocidade_x += velocidade_jogo_tempo
                flag_baixo = True

        elif event.type == KEYUP:
            if event.key == K_UP:
                velocidade_x = 0
            elif event.key == K_DOWN:
                velocidade_x = 0

    #Desenha na tela
    score1 = font.render(str(bar1_score), True,(255,255,255))
    score2 = font.render(str(bar2_score), True,(255,255,255))
    screen.blit(fundo_T,(0,0))
    pygame.draw.rect(screen, COR_P1, Player1)
    pygame.draw.rect(screen, COR_P2, Player2)
    pygame.draw.rect(screen, COR_BOLA, Bola)
   
    pygame.draw.rect(screen, COR_DETALHES, Baixo_coli)
    pygame.draw.rect(screen, COR_DETALHES, Alto_coli)

    pygame.draw.rect(screen, COR_DETALHES,  Ponto_p1)
    pygame.draw.rect(screen, COR_DETALHES,  Ponto_p2)

    screen.blit(score1,(Size_max_y/2 - 100,Size_max_x/2 - 100))
    screen.blit(score2,(Size_max_y/2 + 45,Size_max_x/2 - 100))

    Player1.y = P2_pos_x
    Player2.y = P1_pos_x

    #Pontos  
    if Bola.colliderect(Ponto_p1):
        effect2.play()
        Bola.x = Size_max_y / 2
        Bola.y =  Size_max_x / 2
        velocidade_bola_x *= -1
        velocidade_bola_y = 2
        bar1_score += 1
    elif Bola.colliderect(Ponto_p2):
        effect2.play()
        Bola.x = Size_max_y / 2
        Bola.y =  Size_max_x / 2
        velocidade_bola_x *= -1
        velocidade_bola_y = -2
        bar2_score += 1
 

    #Colisão  teto
    if Player2.colliderect(Alto_coli) and flag_cima:
        flag_cima = False
        velocidade_x = 0
    elif Player2.colliderect(Baixo_coli) and flag_baixo:
        flag_baixo = False
        velocidade_x = 0

    print(velocidade_x)

    #Colsão bola
    if Player2.colliderect(Bola):
        effect2.play()
        velocidade_bola_x  *= -1 
        if velocidade_x > 0:
            velocidade_bola_y = 3 
        elif velocidade_x < 0:
            velocidade_bola_y = -3 
    #Arrumar essa parte 
    if Player1.colliderect(Bola):
        effect1.play()
        velocidade_bola_x  *= -1 

    if Bola.colliderect(Alto_coli) or Bola.colliderect(Baixo_coli):
        effect1.play()
        velocidade_bola_y *= -1


    # Acumulo velocidades 
    P1_pos_x += velocidade_x 
    Bola.x = posx + velocidade_bola_x
    Bola.y = posy + velocidade_bola_y  

    

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()