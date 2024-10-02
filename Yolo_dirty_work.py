from ultralytics import YOLO
import cv2
import numpy as np
import math


# Load the YOLO model
model = YOLO('Models/yolov8s.pt')


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print('Cant read image')
        break
    
    # Создаем черный экран той же формы, что и изображение
    mask = np.zeros_like(img)


    results = model(img, stream = True)
    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            conf = math.ceil((box.conf[0] * 100)) / 100 # confidence

            if conf > 0.3:
                cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)
    

    # Применяем побитовую операцию AND
    img_strip = cv2.bitwise_and(img, mask)            

    cv2.imshow('Camera Feed', img)
    cv2.imshow('Strip image', img_strip)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break