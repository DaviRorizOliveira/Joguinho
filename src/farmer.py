import pygame
from settings import *
from interacoes import Interações

# Classe que faz a construção do player
class Farmer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = { # Sprites do personagem
            'down': [
                pygame.image.load('imagens/player_sprites/down_01.png'),
                pygame.image.load('imagens/player_sprites/down_02.png'),
                pygame.image.load('imagens/player_sprites/down_03.png')
            ],
            'left': [
                pygame.image.load('imagens/player_sprites/left_01.png'),
                pygame.image.load('imagens/player_sprites/left_02.png'),
                pygame.image.load('imagens/player_sprites/left_03.png')
            ],
            'right': [
                pygame.image.load('imagens/player_sprites/right_01.png'),
                pygame.image.load('imagens/player_sprites/right_02.png'),
                pygame.image.load('imagens/player_sprites/right_03.png')
            ],
            'up': [
                pygame.image.load('imagens/player_sprites/up_01.png'),
                pygame.image.load('imagens/player_sprites/up_02.png'),
                pygame.image.load('imagens/player_sprites/up_03.png')
            ]
        }

        self.dinheiro = 0 # Quantidade de dinheiro inicial
        self.nome = "Robin" # Nome da personagem
        
        # "Hit-Box" da imagem do player
        self.TAM_HEIGHT = 47
        self.TAM_WIDTH = 25
        
        # Variáveis auxiliares para a velocidade do player e velocidade de mudança das sprites, respectivamente
        self.MOVMENT_SPEED = 200
        self.CHANGE_SPRITE_SPEED = 5
        
        # Posiciona o player no centro da tela
        self.player_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)

        # Define a posição e a sprite inicial do personagem
        self.direction = 'down'
        self.atual = 0
        self.image = self.sprites[self.direction][self.atual]

        # Ferramentas do personagem
        self.tem_enxada = True
        self.vida_da_enxada = 5

        # Inventário do personagem, 1-tomates, 2-batatas, 3-trigo, 4-leite, 5-ovos, 6-lã
        self.qtd_tomate = 0
        self.qtd_batata = 0
        self.qtd_trigo = 0
        self.qtd_leite = 0
        self.qtd_ovo = 0
        self.qtd_la = 0

        # Inventário de sementes
        self.s_tomate = 1
        self.s_batata = 1
        self.s_trigo = 1

        # Criação das interações que ocorrem entre o personagem e os locais do mapa
        self.interações = Interações()

    # Método que utiliza a enxada ao plantar
    def usa_enxada(self):
        self.vida_da_enxada -= 1
        if self.vida_da_enxada == 0:
            self.tem_enxada = False

    def get_inventario(self):
        return self.tem_enxada

    # Método que constrói o jogador na tela e chama o método update_pos
    def build_player(self, screen, dt, casa, cercado, farm, mercado, popup):
        screen.blit(self.image, self.player_pos - pygame.Vector2(self.image.get_size()) / 2)
        self.update_pos(dt, casa, cercado, farm, mercado, popup, screen)

    # Método que atualiza o sprite a medida que o jogador anda
    def update_sprite(self, dt):
        self.atual = (self.atual + dt * self.CHANGE_SPRITE_SPEED) % len(self.sprites[self.direction])
        self.image = self.sprites[self.direction][int(self.atual)]

    # Método que realiza a colisão do jogador, tanto com os demais locais do mapa, quanto com os limites da tela 1280x720
    def clamp_position(self, casa, cercado, mercado, farm):
        self.player_pos.x = max(self.TAM_WIDTH, min(self.player_pos.x, WIDTH - self.TAM_WIDTH))
        self.player_pos.y = max(self.TAM_HEIGHT, min(self.player_pos.y, HEIGHT - self.TAM_HEIGHT))

        if casa.is_collision(self):
            casa.handle_collision(self)
        if cercado.is_collision(self):
            cercado.handle_collision(self)
        if farm.is_collision(self):
            farm.handle_collision(self)
        if mercado.is_collision(self):
            mercado.handle_collision(self)

    # Método que atualiza a posição do jogador na tela a medida que ele se movimenta, e chama a classe de interações, que faz as verificações
    # se o jogador está tentando interagir com os demias locais
    def update_pos(self, dt, casa, cercado, farm, mercado, popup, screen):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.MOVMENT_SPEED * dt
            self.direction = 'up'
            self.update_sprite(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.MOVMENT_SPEED * dt
            self.direction = 'down'
            self.update_sprite(dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.MOVMENT_SPEED * dt
            self.direction = 'left'
            self.update_sprite(dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.MOVMENT_SPEED * dt
            self.direction = 'right'
            self.update_sprite(dt)

        new_player_pos = self.player_pos + pygame.Vector2(dx, dy)

        self.player_pos = new_player_pos
        
        self.clamp_position(casa, cercado, mercado, farm)
        self.interações.testa_interações(self, casa, cercado, farm, mercado, popup, screen)
    
    # Método que printa um popup com o inventário do jogador
    def printa_inventario(self, screen):
        screen.blit(FONTE1.render(f'1 - Tens {self.qtd_tomate} tomates', True, BLACK), (325, 185))
        screen.blit(FONTE1.render(f'2 - Tens {self.qtd_batata} batatas', True, BLACK), (325, 210))
        screen.blit(FONTE1.render(f'3 - Tens {self.qtd_trigo} quilos de trigo', True, BLACK), (325, 235))
        screen.blit(FONTE1.render(f'4 - Tens {self.qtd_leite} litros de leite', True, BLACK), (325, 260))
        screen.blit(FONTE1.render(f'5 - Tens {self.qtd_ovo} ovos', True, BLACK), (325, 285))
        screen.blit(FONTE1.render(f'6 - Tens {self.qtd_la} quilos de lã', True, BLACK), (325, 310))
        screen.blit(FONTE1.render(f'7 - Tens {self.s_tomate} sementes de tomate', True, BLACK), (325, 335))
        screen.blit(FONTE1.render(f'8 - Tens {self.s_batata} sementes de batata', True, BLACK), (325, 360))
        screen.blit(FONTE1.render(f'9 - Tens {self.s_trigo} sementes de trigo', True, BLACK), (325, 385))