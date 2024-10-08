import Filter_image
import Work_with_cv2
import Create_full_screen
from pynput import keyboard
import cv2
import numpy as np
import tkinter as tk
import logging
import time
import os


# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# data in 0_data.txt:
#  id, [ (% for x), (% for y), (pixels from x), (pixels from y), max_x, max_y , [distanse from center of strip, dist_from_centre_x, dist_from_centre_y, x1, y1, x2, y2], [same as previous 2nd]]
# p - take screenshot, q - quit

SCREEN_CHANGE_TIMER = 0.5



class ScreenCapture:

    
    def __init__(self):
        self.current_x_coordinate = 50
        self.current_y_coordinate = 50
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

    
    def upload_data(self, number, image, cls):
        try:
            status, image_strip, coordinates = Filter_image.filter_image(image)  # TODO 2

            if not status:
                logging.warning('Error in stripping image')
                try:
                    cls.set_grey_screen()
                except Exception as e:
                    logging.exception("Can't color grey screen in upload_data - class not found")
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

            if not os.path.exists('Eyes_data'):
                logging.info("Directory Eyes_data not found and will be created")
                os.makedirs('Eyes_data')

            with open('Eyes_data/0_data.txt', 'a') as file:
                if number != 0:
                    file.write('\n')
                file.write(f'{str(number + 1)} {str(extra_data)}')

            return True
        
        except Exception as e:
            logging.error('Error in upload data function', exc_info=True)
            return False


    def change_circle_coordinates(self):
        (status,
        self.current_x_coordinate, 
        self.current_y_coordinate) = White_screen.update_circle_coordinates()

        if not status:
            logging.warning("Can't change coordenates for circle in \
             change_circle_coordinates")
            return False
        return True

    def when_key_pressed(self, key, Cls_show, Cls):
        try:
            if hasattr(key, 'char'):
                
                if key.char == 'q':
                    logging.info("Exiting due to 'q' key press.")
                    exit_func()
                    return False  # Stop listener

                if key.char == 'p':
                    if Cls.get_is_waiting_gray():
                        logging.info("Too fast please wait")
                        return True
                    status, frame = Cls_show.get_screenshot()

                    if not status:
                        logging.error('Error in Work_with_cv2.get_screenshot')
                        return True
                    
                    status, last_id = self.extract_last_screenshot_id()
                    if not status:
                        logging.warning('Ошибка при извлечении последнего ID скриншота')
                        return True

                    status = self.upload_data(last_id, frame, Cls)
                    if not status:
                        logging.warning('Ошибка при загрузке данных')
                        return True
                    status = self.change_circle_coordinates()
                    if not status:
                        logging.warning('Ошибка при создании новых координат')
                        
            else:
                logging.info('Нажата необрабатываемая клавиша')
            return True

        except Exception as e:
            logging.warning(f'Failure in take_screenshot function - {e}', exc_info=True)
            return True


    def get_screen_size(self):
        root = tk.Tk()
        root.withdraw()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.destroy()
        return screen_width, screen_height


Exit_flag = False
def exit_func():
    global Exit_flag
    Exit_flag = True
    logging.info("Exiting exit_func")
    exit()



if __name__ == '__main__':
    screen_capture = ScreenCapture()
    width, height = screen_capture.get_screen_size()
    logging.info(f'Screen size: {width}x{height}')

    Image_show = Work_with_cv2.Image()
    White_screen = Create_full_screen.Full_screen_image(width, height)

    listener = keyboard.Listener(on_press=lambda key:
                                 screen_capture.when_key_pressed(key, Image_show, White_screen))
    listener.start()

    while True:
        if Exit_flag:
            listener.stop()
            Image_show.end_showing()
            White_screen.end_showing()
            cv2.destroyAllWindows()
            break

        status = Image_show.show()
        if not status:
            break

        status = White_screen.open_screen()
        if not status:
            break