import numpy as np
import imageio.v2 as iio

def olivindex2(files):

    # Depois de analisar todas as n imagens
    # Total de amostras em cada classe (exemplos)
    tc0 = 0 # Amostras na classe 0
    tc1 = 0 # Amostras na classe 1
    tc2 = 0  # Amostras na classe 2
    tc3 = 0  # Amostras na classe 3
    tc4 = 0  # Amostras na classe 4
    tc5 = 0  # Amostras na classe 5
    tc6 = 0 # Amostras na classe 6
    tc7 = 0 # Amostras na classe 7

    for file in files:
        im = iio.imread(file)

        # Tamanho da imagem
        m, n, _ = im.shape

        # Cria padrões de cor de referências com mesma dimensão da imagem (array m x n x 3)
        gre = np.tile(np.array([89, 90, 21]).reshape(1, 1, 3), (m, n, 1))
        gry = np.tile(np.array([134, 132, 35]).reshape(1, 1, 3), (m, n, 1))
        pur = np.tile(np.array([76, 50, 36]).reshape(1, 1, 3), (m, n, 1))
        blk = np.tile(np.array([37, 24, 19]).reshape(1, 1, 3), (m, n, 1))
        whi = np.tile(np.array([200, 190, 180]).reshape(1, 1, 3), (m, n, 1))
        vaz = np.tile(np.array([250, 250, 250]).reshape(1, 1, 3), (m, n, 1))

        # Distância Euclidiana entre RGB de cada pixel da imagem e RGB de cada cor padrão
        dgre = np.sqrt(np.sum((im - gre) ** 2, axis=2))
        dgry = np.sqrt(np.sum((im - gry) ** 2, axis=2))
        dpur = np.sqrt(np.sum((im - pur) ** 2, axis=2))
        dblk = np.sqrt(np.sum((im - blk) ** 2, axis=2))
        dwhi = np.sqrt(np.sum((im - whi) ** 2, axis=2))
        dvaz = np.sqrt(np.sum((im - vaz) ** 2, axis=2))

        # Converte matrizes (m x n pixels) de distâncias em vetores (n*m pontos)
        dgre = dgre.flatten()
        dgry = dgry.flatten()
        dpur = dpur.flatten()
        dblk = dblk.flatten()
        dwhi = dwhi.flatten()
        dvaz = dvaz.flatten()

        # Organiza as distâncias em uma matriz (n de cores x n*m pontos)
        de = np.vstack((dgre, dgry, dpur, dblk, dwhi, dvaz))

        # Classifica o pixel em cada ladrão de cor baseado na menor distância
        corclas = np.argmin(de, axis=0)

        # Soma e porcentagem de pixels em cada cor padrão
        PerCol = [
            np.sum(corclas == 0),
            np.sum(corclas == 1),
            np.sum(corclas == 2),
            np.sum(corclas == 3),
            np.sum(corclas == 4)
        ]

        PerCol = np.array(PerCol) / np.sum(PerCol) * 100

        # Classificação da amostra em cada classe de maturação
        if PerCol[0] > 1 or PerCol[1] > 90:  # Azeitonas com pele
            if np.sum(PerCol[2:4]) <= 5 and PerCol[0] >= 50:
                tc0 += 1
            elif np.sum(PerCol[2:4]) <= 5 and PerCol[1] > 50:
                tc1 += 1
            elif np.sum(PerCol[0:2]) > np.sum(PerCol[2:4]):
                tc2 += 1
            elif np.sum(PerCol[0:2]) < np.sum(PerCol[2:4]):
                tc3 += 1
        else:  # Azeitonas cortadas
            if PerCol[4] / np.sum(PerCol[2:5]) >= 0.9:
                tc4 += 1
            elif PerCol[4] / np.sum(PerCol[2:5]) <= 0.1:
                tc7 += 1
            elif PerCol[4] / np.sum(PerCol[2:5]) > 0.5:
                tc5 += 1
            elif PerCol[4] / np.sum(PerCol[2:5]) < 0.5:
                tc6 += 1

    nt = tc0 + tc1 + tc2 + tc3 + tc4 + tc5 + tc6 + tc7  # Total de amostras analisadas

    # Porcentagem de amostras em cada classe
    pc0 = float("{:.2f}".format(tc0 / nt * 100))
    pc1 = float("{:.2f}".format(tc1 / nt * 100))
    pc2 = float("{:.2f}".format(tc2 / nt * 100))
    pc3 = float("{:.2f}".format(tc3 / nt * 100))
    pc4 = float("{:.2f}".format(tc4 / nt * 100))
    pc5 = float("{:.2f}".format(tc5 / nt * 100))
    pc6 = float("{:.2f}".format(tc6 / nt * 100))
    pc7 = float("{:.2f}".format(tc7 / nt * 100))

    # Índice de maturação
    IM = (pc1 + 2 * pc2 + 3 * pc3 + 4 * pc4 + 5 * pc5 + 6 * pc6 + 7 * pc7) / nt

    return {
        "classes" : [tc0, tc1, tc2, tc3, tc4, tc5, tc6, tc7],
        "percentAmostras" : [pc0, pc1, pc2, pc3, pc4, pc5, pc6, pc7],
        "indiceMaturacao" : float("{:.2f}".format(IM)),
        "totalAmostras": nt,
    }
