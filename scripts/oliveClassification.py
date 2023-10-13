import numpy as np
import os
from scipy.spatial.distance import cdist
from PIL import Image

def olivindex2(files):

    PCol = np.zeros((len(files), 5))
    Clas = np.zeros(len(files))

    for nf, file in enumerate(files):
        im = np.array(Image.open(file))  # Carrega a imagem

        gre = np.tile(np.reshape([89, 90, 21], (1, 1, 3), order='F'), (im.shape[0], im.shape[1], 1))
        gry = np.tile(np.reshape([134, 132, 35], (1, 1, 3), order='F'), (im.shape[0], im.shape[1], 1))
        pur = np.tile(np.reshape([76, 50, 36], (1, 1, 3), order='F'), (im.shape[0], im.shape[1], 1))
        blk = np.tile(np.reshape([37, 24, 19], (1, 1, 3), order='F'), (im.shape[0], im.shape[1], 1))
        whi = np.tile(np.reshape([200, 190, 180], (1, 1, 3), order='F'), (im.shape[0], im.shape[1], 1))
        vaz = np.tile(np.reshape([250, 250, 250], (1, 1, 3), order='F'), (im.shape[0], im.shape[1], 1))

        corclas = np.argmin([
            np.reshape(np.sqrt(np.sum((im - gre) ** 2, axis=2)), -1),
            np.reshape(np.sqrt(np.sum((im - gry) ** 2, axis=2)), -1),
            np.reshape(np.sqrt(np.sum((im - pur) ** 2, axis=2)), -1),
            np.reshape(np.sqrt(np.sum((im - blk) ** 2, axis=2)), -1),
            np.reshape(np.sqrt(np.sum((im - whi) ** 2, axis=2)), -1),
            np.reshape(np.sqrt(np.sum((im - vaz) ** 2, axis=2)), -1)
        ])

        PerCol = [np.sum(corclas == 0), np.sum(corclas == 1), np.sum(corclas == 2), np.sum(corclas == 3), np.sum(corclas == 4)]

        # Verificar e evitar divisão por zero
        total_percol = np.sum(PerCol)
        if total_percol > 0:
            PerCol = np.array(PerCol) / total_percol * 100
        else:
            PerCol = np.zeros(5)

        PCol[nf, :] = PerCol

        if PerCol[0] > 1 or PerCol[1] > 90:  # Azeitonas com pele
            if np.sum(PerCol[2:4]) <= 5 and PerCol[0] >= 50:
                Clas[nf] = 0
            elif np.sum(PerCol[2:4]) <= 5 and PerCol[1] > 50:
                Clas[nf] = 1
            elif np.sum(PerCol[0:2]) > np.sum(PerCol[2:4]):
                Clas[nf] = 2
            elif np.sum(PerCol[0:2]) < np.sum(PerCol[2:4]):
                Clas[nf] = 3
        else:  # Azeitonas cortadas
            if PerCol[4] > 0 and np.sum(PerCol[2:5]) > 0:
                if PerCol[4] / np.sum(PerCol[2:5]) >= 0.9:
                    Clas[nf] = 4
                elif PerCol[4] / np.sum(PerCol[2:5]) <= 0.1:
                    Clas[nf] = 7
                elif PerCol[4] / np.sum(PerCol[2:5]) > 0.5:
                    Clas[nf] = 5
                elif PerCol[4] / np.sum(PerCol[2:5]) < 0.5:
                    Clas[nf] = 6

    PClas = [np.sum(Clas == i) / len(files) * 100 for i in range(8)]

    MI = sum(i * j for i, j in zip(PClas[1:], range(2, 9))) / 100
    TA = len(files)

    print("Índice de Maturação (MI):", MI)
    print("Total de amostras analisadas (TA):", TA)
    print("Porcentagem de amostras em cada classe (PClas):", PClas)
    print("Classe de cada amostra (Clas):", Clas)
    print("Porcentagem de cores (PCol):", PCol)
