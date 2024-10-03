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
    mask = np.zeros_like(img)
    objects = []

    results = model(img) 

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            conf = math.ceil((box.conf[0] * 100)) / 100 # confidence

            if conf > 0.3 and (abs(x1-x2)*abs(y1-y2)) > MIN_AREA:

                from_center = round(((x1 + x2 - size_of_x)**2 + (y1+y2-size_of_y)**2)**0.5//2)
                objects.append([from_center, x1, y1, x2, y2])
    
    objects.sort(key= lambda id: id[0])

    if len(objects) < 2:
        logging.warning('Не смогли обнаружить глаза')
        return False, 0, 0
    
    objects = objects[:2] # выбираем 2 прямоугольника, ближайших к центру

    for _, x1, y1, x2, y2 in objects:
        cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)

    # Применяем побитовую операцию AND
    img_strip = cv2.bitwise_and(img, mask)            

    return True, img_strip, objects
