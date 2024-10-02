from ultralytics import YOLO
import cv2
import numpy as np
import math

model = YOLO('Models/yolov8s.pt')
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print('No sucsess')
        break

    results = model(img, stream = True)
    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            conf = math.ceil((box.conf[0] * 100)) / 100 # confidence
            cls = int(box.cls[0]) # class id

            if conf > 0.3:
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                cv2.putText(img, f'{conf} - {cls}',
                    (max(5, x1), max(15, y1-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (100, 0, 255), 2)
                

    cv2.imshow('Camera Feed', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break