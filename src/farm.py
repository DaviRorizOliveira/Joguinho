import pygame
from settings import *
from local import Local
from planta import Planta

class Farm(Local):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

        self.pos_x = x # Posição na tela
        self.pos_y = y # Posição na tela

        self.slots = []

        for a in range(5): # Cria os 5 slots de plantas, os quais serão plantados conforme o desejo do jogador
            planta = Planta(self.pos_x + 70 + a * 110, self.pos_y)
            self.slots.append(planta)
    
    # Constrói o local no mapa, junto com os 5 slots de plantas
    def build_local(self, screen, new_tam_x=None, new_tam_y=None):
        super().build_local(screen, new_tam_x, new_tam_y)
        for a in range(5):
            self.slots[a].build_slot(screen)

    # Método que coloca uma semente de escolha do jogador no slot selecionado, faz também a verificação se o jogador ainda tem uma enxada, caso
    # ele não tenha, nada será plantado
    def coloca_semente(self, slot, semente, player):
        if player.vida_da_enxada != 0:
            if semente == 'tomate' and player.s_tomate > 0:
                self.slots[slot].tipo_planta = semente
                self.slots[slot].planta()
                player.usa_enxada()
                player.s_tomate -= 1
            elif semente == 'batata' and player.s_batata > 0:
                self.slots[slot].tipo_planta = semente
                self.slots[slot].planta()
                player.usa_enxada()
                player.s_batata -= 1
            elif semente == 'trigo' and player.s_trigo > 0:
                self.slots[slot].tipo_planta = semente
                self.slots[slot].planta()
                player.usa_enxada()
                player.s_trigo -= 1
            else:
                pass
        else:
            pass

    # Faz a colheita da planta no slot selecionado, resetando as informações do slot, transformando-o em um slot sem nada plantado
    def colher(self, slot, player):
        if self.slots[slot].tipo_planta == 'tomate':
            player.qtd_tomate += 3
        elif self.slots[slot].tipo_planta == 'batata':
            player.qtd_batata += 3
        elif self.slots[slot].tipo_planta == 'trigo':
            player.qtd_trigo += 3
        self.slots[slot].tipo_planta = None
        self.slots[slot].idade = -1
        self.slots[slot].sprite_atual = -1
        self.slots[slot].status = ''
        self.slots[slot].image = pygame.image.load('imagens/terra.png')
        self.slots[slot].imageimage = pygame.transform.scale(self.image, (45, 75))

    # Verifica se a planta está madura para a colheita, se verdadeiro, realiza a colheita
    def verifica_colheita(self, slot, player):
        if self.slots[slot].idade >= 4:
            self.colher(slot, player)
        else:
            pass