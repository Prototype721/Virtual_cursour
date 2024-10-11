from ultralytics import YOLO
import cv2
import numpy as np
import math
import logging

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


MIN_AREA = 30

# Load the YOLO model
model = YOLO('Models/Custom_yolov8_3.pt')

def filter_image(img):

    size_of_x = len(img[0])
    size_of_y = len(img)
    objects = []

    results = model(img, stream = True, verbose = False) 

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            conf = math.ceil((box.conf[0] * 100)) / 100 # confidence

            if conf > 0.3 and (abs(x1-x2)*abs(y1-y2)) > MIN_AREA:
                from_center_x = (x1 + x2 - size_of_x)/2
                from_center_y = (-1)*(y1+y2-size_of_y)/2
                from_center = round((from_center_x**2 + from_center_y**2)**0.5)
                objects.append([from_center,from_center_x,from_center_y, x1, y1, x2, y2])
    
    objects.sort(key= lambda id: id[0])

    if len(objects) < 2:
        logging.warning('Не смогли обнаружить глаза')
        return False, 0, 0
    
    objects = objects[:2] # выбираем 2 прямоугольника, ближайших к центру

    status, img_strip = create_collage(img, objects[0][3:], objects[1][3:])

    if not status:
        logging.warning("Ошибка в обрезании коллажа")
        return False, 0, 0
    
    return True, img_strip, objects



def create_collage(image, rect1, rect2): # изменен порядок, чтобы правый глаз был справа, т.к. в cv2 изображение трансформировано
    try:
        if rect1[0] > rect2[0]:
            rect1, rect2 = rect2, rect1
        # Обрезаем прямоугольники
        box1 = (rect1[1], rect1[0], rect1[3], rect1[2])  # (y1, x1, y2, x2)
        box2 = (rect2[1], rect2[0], rect2[3], rect2[2])  # (y1, x1, y2, x2)

        cropped1 = image[box1[0]:box1[2], box1[1]:box1[3]]
        cropped2 = image[box2[0]:box2[2], box2[1]:box2[3]]

        # Определяем размеры для коллажа
        height1, width1 = cropped1.shape[:2]
        height2, width2 = cropped2.shape[:2]

        collage_height = max(height1, height2)
        collage_width = width1 + width2

        # Создаем новое изображение для коллажа
        collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

        # Вставляем обрезанные изображения в коллаж
        collage[:height1, :width1] = cropped1
        collage[:height2, width1:width1 + width2] = cropped2

        # Сохраняем результат
        return True, collage
    
    except Exception as e:
        logging.error(f'Ошибка при создании коллажа: {e}')
        return False, 0


