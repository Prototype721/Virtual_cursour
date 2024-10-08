import Custom_model_work
import Filter_image
import Work_with_cv2
import Cursour_work
from pynput import keyboard
import cv2
import numpy as np
import tkinter as tk
import logging
import time



SCREEN_CHANGE_TIMER = 0.5

last_call_time = time.time()


def when_key_pressed(key, Cls_img, Cls_filtr, Cls_neiral, Cls_cursour):
    try:
        if hasattr(key, 'char'):
            

            if key.char == 'q':
                logging.info("Exiting due to 'q' key press.")
                exit_func()
                return False  # Stop listener


            if key.char == 'p':
                if (time.time()-last_call_time) < SCREEN_CHANGE_TIMER:
                    logging.info("Too fast please wait")
                    return True
                status, frame = Cls_img.get_screenshot()

                if not status:
                    logging.error('Error in Work_with_cv2.get_screenshot') # TODO add Filter
                    return True
                
                status, frame_strip, objects = Cls_filtr.filter_image(frame)
                if not status:
                    logging.warning('Ошибка в обнаружении глаз')
                    return True
                # TODO uncomment
                #status, x, y = Cls_neiral.model_coordinates(frame_strip, objects)
                if not status:
                    logging.warning('Ошибка в неиронной сети')
                    return True
                
                status = Cls_cursour.move_mouse(200, 200)
                #status = Cls_cursour.move_mouse(x, y) # TODO uncomment
                if not status:
                    logging.warning('Ошибка при перемещении курсора')


            if key.char == 'o':
                status = Cls_cursour.click_mouse()
                if not status:
                    logging.warning('Ошибка при нажатии click_mouse')
                    return True
        else:
            logging.info('Нажата необрабатываемая клавиша')
        return True

    except Exception as e:
        logging.warning(f'Failure in take_screenshot function - {e}', exc_info=True)
        return True




def get_screen_size(ppo):
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
    exit()




if __name__ == '__main__':
    width, height = get_screen_size()

    Image_show = Work_with_cv2.Image()

    listener = keyboard.Listener(on_press=lambda key:
                                 when_key_pressed(key, Image_show, Filter_image, Custom_model_work, Cursour_work))
    listener.start()

    while True:
        if Exit_flag:
            listener.stop()
            Image_show.end_showing()
            cv2.destroyAllWindows()
            break

        status = Image_show.show()
        if not status:
            break