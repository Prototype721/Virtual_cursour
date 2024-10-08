import cv2
import numpy as np
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


SCREEN_CHANGE_TIMER = 0.5


class Full_screen_image:
    
    def __init__(self, wight = 1600, height = 900):
        self._x_coordinate = 50
        self._y_coordinate = 50
        self.width = wight
        self.height = height
        self._is_waiting_gray = False
        self._time_to_change_screen_color = time.time()

        self._ones_image = np.ones((self.height, self.width, 3), dtype=np.uint8)
        self.white_image = self._ones_image * 255
        self.gray_image = self._ones_image * 150


    def end_showing(self):
        logging.info("End showing full screen")
        cv2.destroyAllWindows()
        return True

    def get_is_waiting_gray(self):
        return self._is_waiting_gray 
    
    def set_grey_screen(self): # TODO 2
        self._time_to_change_screen_color = time.time()
        self._is_waiting_gray  = True
        return True 
    
    def update_circle_coordinates(self):
        self._x_coordinate = random.randint(5, 95)
        self._y_coordinate = random.randint(5, 95)
        #self._x_coordinate = 100
        #self._y_coordinate = 100
        return (True, self._x_coordinate, self._y_coordinate)
    

    def open_screen(self):
        
        # Если не смогли обнаружить 2 глаза, то меняем цвет фона
        if (time.time() - self._time_to_change_screen_color) < SCREEN_CHANGE_TIMER:
            image = self.gray_image.copy()
            self._is_waiting_gray  = True
        else:
            image = self.white_image.copy()
            self._is_waiting_gray  = False

        circle_size = (self.width + self.height) // 200

        self.top_left_x = (self.width * self._x_coordinate) // 100
        self.top_left_y = (self.height * self._y_coordinate) // 100

        cv2.circle(image,
                  (self.top_left_x, self.top_left_y),
                   circle_size, (0, 0, 255), -1)

        cv2.putText(image, 'p - screenshot, q - quit',
                    (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.namedWindow('Teaching model screen',
                        cv2.WND_PROP_FULLSCREEN)
        
        cv2.setWindowProperty('Teaching model screen',
                            cv2.WND_PROP_FULLSCREEN,
                            cv2.WINDOW_FULLSCREEN)
        
        cv2.imshow('Teaching model screen', image)
        cv2.waitKey(1)
        return True


