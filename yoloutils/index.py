import cv2
import numpy as np
from ultralytics import YOLO
import os

dirname = os.path.dirname(__file__)

def generate_mask(image_path, model_path, output_path):
    img = cv2.imread(image_path)
    H, W, _ = img.shape

    model = YOLO(model_path)

    results = model(img)

    for result in results:
        for j, mask in enumerate(result.masks.data):
            mask = mask.numpy() * 255
            mask = cv2.resize(mask, (W, H))
            cv2.imwrite(output_path, mask)

    print("Máscara gerada e salva em:", output_path)

def overlay_mask(image_path, mask_path, output_path):
    image = cv2.imread(image_path)  # carregar imagem original
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)  # carregar máscara em escala de cinza

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar o maior contorno (a azeitona)
    max_contour = max(contours, key=cv2.contourArea)

    # Criar uma máscara em branco do mesmo tamanho que a imagem original
    mask_contour = np.zeros_like(mask)

    # Preencher o maior contorno na máscara em branco
    cv2.drawContours(mask_contour, [max_contour], -1, 255, thickness=cv2.FILLED)

    # Aplicar a máscara do maior contorno na imagem original para obter a azeitona com fundo branco
    overlaid = cv2.bitwise_and(image, image, mask=mask_contour)

    # Criar uma máscara branca com o mesmo tamanho da imagem original
    white_background = np.ones_like(image) * 255

    # Criar uma máscara invertida para criar uma região de interesse para o fundo
    inverted_mask = cv2.bitwise_not(mask_contour)

    # Aplicar a máscara invertida no fundo branco
    background = cv2.bitwise_and(white_background, white_background, mask=inverted_mask)

    # Combinar azeitona com fundo branco, criando a imagem desejada
    overlaid = cv2.bitwise_or(overlaid, background)

    cv2.imwrite(output_path, overlaid)  # salvando o resultado

    print("Imagem resultante salva em:", output_path)


def resize_and_center(image, target_size):
    h, w = image.shape[:2]
    max_dim = max(h, w)

    # Calcula o deslocamento necessário para centralizar a azeitona na imagem
    top = (max_dim - h) // 2
    bottom = max_dim - h - top
    left = (max_dim - w) // 2
    right = max_dim - w - left

    # Adiciona uma borda de cor branca ao redor da imagem
    image_with_border = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # Redimensiona a imagem para o tamanho desejado
    resized_image = cv2.resize(image_with_border, (target_size, target_size))

    return resized_image
    
def generate_and_overlay_mask(image_path, output_path):
    mask_path = os.path.join(dirname, "mask.png")
    model_path = os.path.join(dirname, "IAmodel.pt")
    generate_mask(image_path, model_path, mask_path)
    overlay_mask(image_path, mask_path, output_path)

