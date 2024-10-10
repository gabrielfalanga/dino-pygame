import pygame
import random

# inicializa o pygame
pygame.init()

# tamanho da tela
TELA_LARGURA = 1280
TELA_ALTURA = 720

# imagens
IMG_CHAO = pygame.transform.scale(pygame.image.load('assets/ground.png'),
                                  (pygame.image.load('assets/ground.png').get_width() * 1.5,
                                   pygame.image.load('assets/ground.png').get_height() * 1.5))
IMG_NUVEM = pygame.transform.scale(pygame.image.load('assets/cloud.png'),
                                   (pygame.image.load('assets/ground.png').get_width() * 1.5,
                                    pygame.image.load('assets/ground.png').get_height() * 1.5))
IMGS_DINO = {
    'normal': [
        pygame.transform.scale(
            pygame.image.load('assets/Dino1.png'),
            (pygame.image.load('assets/Dino1.png').get_width() * 1.5,
             pygame.image.load('assets/Dino1.png').get_height() * 1.5)
        ),
        pygame.transform.scale(
            pygame.image.load('assets/Dino2.png'),
            (pygame.image.load('assets/Dino2.png').get_width() * 1.5,
             pygame.image.load('assets/Dino2.png').get_height() * 1.5)
        )
    ],
    'pulo': pygame.transform.scale(
            pygame.image.load('assets/DinoJumping.png'),
            (pygame.image.load('assets/DinoJumping.png').get_width() * 1.5,
             pygame.image.load('assets/DinoJumping.png').get_height() * 1.5)
            ),
    'agachado': [
        pygame.transform.scale(
            pygame.image.load('assets/DinoDucking1.png'),
            (pygame.image.load('assets/DinoDucking1.png').get_width() * 1.5,
             pygame.image.load('assets/DinoDucking1.png').get_height() * 1.5)
        ),
        pygame.transform.scale(
            pygame.image.load('assets/DinoDucking2.png'),
            (pygame.image.load('assets/DinoDucking2.png').get_width() * 1.5,
             pygame.image.load('assets/DinoDucking2.png').get_height() * 1.5)
        )
    ]
}
IMGS_PTERO = [
    pygame.transform.scale(pygame.image.load('assets/Ptero1.png'),
        (pygame.image.load('assets/Ptero1.png').get_width() * 1.5,
         pygame.image.load('assets/Ptero1.png').get_height() * 1.5)
        ),
    pygame.transform.scale(pygame.image.load('assets/Ptero2.png'),
        (pygame.image.load('assets/Ptero2.png').get_width() * 1.5,
         pygame.image.load('assets/Ptero2.png').get_height() * 1.5)
        )
]
IMGS_CACTOS = [
    pygame.transform.scale(pygame.image.load('assets/cacti/cactus1.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('assets/cacti/cactus2.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('assets/cacti/cactus3.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('assets/cacti/cactus4.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('assets/cacti/cactus5.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('assets/cacti/cactus6.png'), (75, 75))
]

# fonte para os textos
pygame.font.init()
FONTE_TEXTO = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)


# classes
class Dino:
    # imagens
    IMGS = IMGS_DINO
    # animação de correr
    TEMPO_ANIMACAO = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.altura_inicial = y
        self.velocidade_y = 0  # pulo
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS['pulo']
        self.rect = self.imagem.get_rect(bottomleft=(x, y))
        self.pulando = False
        self.agachado = False

    def pular(self):
        if self.y == self.altura_inicial:  # só pode pular se estiver no chão
            self.velocidade_y = -10.5  # força do pulo
            self.tempo = 0
            self.pulando = True

    def agachar(self):
        if self.y == self.altura_inicial:  # se estiver no chão
            self.agachado = True
        else:
            self.velocidade_y = 100

    def levantar(self):
        self.agachado = False

    def mover(self):
        self.tempo += 1

        # cálculo do deslocamento
                # aceleração     # t²               # V             # t
        deslocamento = 1 * (self.tempo ** 2) + self.velocidade_y * self.tempo

        # restrição do deslocamento - limita a gravidade
        if deslocamento >= 30:
            deslocamento = 30

        # deslocar o dino
        self.y += deslocamento

        # impedir que o dino caia abaixo do chão
        if self.y >= self.altura_inicial:
            self.y = self.altura_inicial
            self.pulando = False  # quando atinge o chão, não está mais pulando

        # atualizar o rect
        self.rect = self.imagem.get_rect(bottomleft=(self.x, self.y))

    def exibir(self, tela):
        # mudar imagem da animação
        self.contagem_imagem += 1

        # se estiver no ar (pulando)
        if self.pulando:
            self.imagem = self.IMGS['pulo']
        # se estiver agachado
        elif self.agachado:
            # alternar entre as imagens agachado
            if self.contagem_imagem < self.TEMPO_ANIMACAO:
                self.imagem = self.IMGS['agachado'][0]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
                self.imagem = self.IMGS['agachado'][1]
            else:
                self.contagem_imagem = 0
        # se estiver normal no chão
        else:
            # alternar entre as imagens de corrida
            if self.contagem_imagem < self.TEMPO_ANIMACAO:
                self.imagem = self.IMGS['normal'][0]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
                self.imagem = self.IMGS['normal'][1]
            else:
                self.contagem_imagem = 0

        # atualizar o rect
        self.rect = self.imagem.get_rect(bottomleft=(self.x, self.y))

        # exibir o dino
        tela.blit(self.imagem, self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cacto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 10
        self.imagem = random.choice(IMGS_CACTOS)
        self.rect = self.imagem.get_rect(bottomleft=(x, y))
        self.passou = False

    def mover(self):
        self.x -= self.velocidade

    def exibir(self, tela):
        self.rect = self.imagem.get_rect(bottomleft=(self.x, self.y))
        tela.blit(self.imagem, self.rect)

    def colidiu(self, dino: Dino):
        # masks
        dino_mask = dino.get_mask()
        cacto_mask = pygame.mask.from_surface(self.imagem)

        # distância entre dino e cacto
        distancia = ((self.x - dino.x), (self.y - round(dino.y)))

        # colisão
        ponto_colisao = dino_mask.overlap(cacto_mask, distancia)

        if ponto_colisao:
            return True
        else:
            return False


class Ptero:
    pass


class Chao:
    LARGURA = IMG_CHAO.get_width()
    IMAGEM = IMG_CHAO

    def __init__(self, y):
        self.y = y
        self.velocidade = 10
        self.x1 = 0
        self.x2 = self.LARGURA
        self.x3 = self.LARGURA * 2

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade
        self.x3 -= self.velocidade

        # se sair da tela, aparece de novo do outro lado
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x3 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA
        if self.x3 + self.LARGURA < 0:
            self.x3 = self.x2 + self.LARGURA

    def exibir(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))
        tela.blit(self.IMAGEM, (self.x3, self.y))


class Nuvem:
    pass


def desenhar_tela(tela, dinos: [Dino], cactos: [Cacto], chao: Chao, pontos: int):
    # preencher tela
    tela.fill((255, 255, 255))

    # exibir dinos
    for dino in dinos:
        dino.exibir(tela)

    # exibir cactos
    for cacto in cactos:
        cacto.exibir(tela)

    # exibir chão
    chao.exibir(tela)

    #pontos
    texto_pontos = FONTE_TEXTO.render(f'HI 0   {pontos}', 1, (0, 0, 0))
    tela.blit(texto_pontos, (TELA_LARGURA - 20 - texto_pontos.get_width(), 20))

    # atualizar a tela
    pygame.display.update()


def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Dino Game")
    dinos = [Dino(TELA_LARGURA / 4, TELA_ALTURA / 1.83)]
    cactos = [Cacto(1300, TELA_ALTURA / 1.83)]
    chao = Chao(370)
    pontos = 0
    clock = pygame.time.Clock()

    rodando = True
    while rodando:
        clock.tick(60)

        teclas = pygame.key.get_pressed()

        for dino in dinos:
            if teclas[pygame.K_DOWN]:
                dino.agachar()
            elif dino.agachado:
                dino.levantar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                    for dino in dinos:
                        dino.pular()

        # mover os elementos
        for dino in dinos:
            dino.mover()
        chao.mover()

        # lógica de colisão e adição de cactos
        adicionar_cacto = False
        remover_cactos = []
        for cacto in cactos:
            for i, dino in enumerate(dinos):
                if cacto.colidiu(dino):
                    dinos.pop(i)
                if not cacto.passou and dino.x > (cacto.x + cacto.imagem.get_width()) and not dino.pulando:
                    cacto.passou = True
                    adicionar_cacto = True
            cacto.mover()
            if cacto.x + cacto.imagem.get_width() < 0:
                remover_cactos.append(cacto)

        if adicionar_cacto:
            pontos += 1
            cactos.append(Cacto(1300, TELA_ALTURA / 1.83))

        for cacto in remover_cactos:
            cactos.remove(cacto)

        desenhar_tela(tela, dinos, cactos, chao, pontos)


if __name__ == '__main__':
    main()

# funções para rodar o jogo
# def desenhar_tela(tela, dinos: [Dino], cactos: [Cacto], pteros: [Ptero], chao: Chao, pontos: int):
#     # dinos
#     for dino in dinos:
#         dino.exibir(tela)
#     # cactos
#     for cacto in cactos:
#         cacto.exibir(tela)
#     # pteros
#     for ptero in pteros:
#         ptero.exibir(tela)
#     # pontos
#     texto_pontos = FONTE_TEXTO.render(f'HI 0\t{pontos}', antialias=1, color=(0, 0, 0))
#     tela.blit(texto_pontos, (TELA_LARGURA - 20 - texto_pontos.get_width(), 20))
#     # chao
#     chao.exibir(tela)
#     # atualizar a tela
#     pygame.display.update()
#
