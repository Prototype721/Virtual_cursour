import Filter_image
import Get_image
from pynput import keyboard
import cv2
import numpy as np
import tkinter as tk
import random
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# data in 0_data.txt:
#  id, [ (% for x), (% for y), (pixels from x), (pixels from y), max_x, max_y , [distanse from center of 1 strip, x1, y1, x2, y2], [distanse from center of 2 strip, x1, y1, x2, y2]]
# p - take screenshot, q - quit


class ScreenCapture:


    def __init__(self):
        self.current_x_coordinate = random.randint(5, 95)
        self.current_y_coordinate = random.randint(5, 95)
        self.width, self.height = self.get_screen_size()


    def extract_last_screenshot_id(self, file_path='Eyes_data/0_data.txt'):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if not lines:
                    return True, 0

                last_line = lines[-1]
                numbers = last_line.split()

                if not numbers:
                    return False, 0
                
                return True, int(numbers[0])
            
        except FileNotFoundError:
            logging.warning("Файл не найден и будет создан.")
            return True, 0
        
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
            return False, 0


    def upload_data(self, number, image, extra_data='#####'):
        try:
            status, image_strip, coordinates = Filter_image.filter_image(image)

            if not status:
                logging.warning('Error in stripping image')
                return False
            

            extra_data = [
                self.current_x_coordinate,
                self.current_y_coordinate,
                self.width * self.current_x_coordinate // 100,
                self.height * self.current_y_coordinate // 100,
                self.width,
                self.height,
                coordinates[0],
                coordinates[1]
            ]

            logging.info(f"Screenshot {number + 1}: {extra_data}")
            cv2.imwrite(f'Eyes_data/{number + 1}.jpg', image)
            cv2.imwrite(f'Eyes_data/{number + 1}_strip.jpg', image_strip)

            with open('Eyes_data/0_data.txt', 'a') as file:
                if number != 0:
                    file.write('\n')
                file.write(f'{str(number + 1)} {str(extra_data)}')

            self.current_x_coordinate = random.randint(5, 95)
            self.current_y_coordinate = random.randint(5, 95)

            return True
        
        except Exception as e:
            logging.error('Error in upload data function', exc_info=True)
            return False


    def when_key_pressed(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char == 'q':
                    logging.info("Exiting due to 'q' key press.")
                    return False  # Stop listener

                if key.char == 'p':
                    status, frame = Get_image.get_screenshot()

                    if not status:
                        logging.error('Error in Get_image.get_screenshot')
                        return True
                    
                    status, last_id = self.extract_last_screenshot_id()
                    if not status:
                        logging.warning('Ошибка при извлечении последнего ID скриншота')
                        return True

                    status = self.upload_data(last_id, frame)
                    if not status:
                        logging.warning('Ошибка при загрузке данных')

            return True
        
        except Exception as e:
            logging.warning(f'Failure in take_screenshot function - {e}', exc_info=True)
            return True


    def open_screen(self):
        white_image = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

        circle_size = (self.width + self.height) // 200

        top_left_x = (self.width * self.current_x_coordinate) // 100
        top_left_y = (self.height * self.current_y_coordinate) // 100

        cv2.putText(white_image, 'p - screenshot, q - quit',
                    (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.circle(white_image,
                   (top_left_x, top_left_y),
                    circle_size, (0, 0, 255), -1)

        cv2.namedWindow('Teaching model screen',
                         cv2.WND_PROP_FULLSCREEN)
        
        cv2.setWindowProperty('Teaching model screen',
                              cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
        
        cv2.imshow('Teaching model screen', white_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            logging.info('Quitting from open_screen function.')
            return False
        
        return True


    def get_screen_size(self):
        root = tk.Tk()
        root.withdraw()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.destroy()
        logging.info(f'Screen size: {screen_width}x{screen_height}')
        return screen_width, screen_height


if __name__ == '__main__':
    screen_capture = ScreenCapture()

    listener = keyboard.Listener(on_press=lambda key:
                                 screen_capture.when_key_pressed(key))
    listener.start()

    while True:
        status = Get_image.show()
        if not status:
            break

        status = screen_capture.open_screen()
        if not status:
            break