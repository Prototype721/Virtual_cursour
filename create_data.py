import Get_image
from pynput import keyboard
import cv2
import numpy as np
import tkinter as tk
import random
# p - take screenshot, q - quit

# data in 0_data.txt:
#  id, [ (% for x), (% for y), (pixels from x), (pixels from y), max_x, max_y ]

#------------ \/ get screenshot \/ ---------------------------------

def extract_last_screenshot_id():
    try:
        with open('Eyes_data/0_data.txt', 'r') as file:
            lines = file.readlines()
            if not lines:
                return True, 0
            
            last_line = lines[-1]
            # Извлечение первого числа из последней строки
            numbers = [s for s in last_line.split()]
            if not numbers:
                return False
            
            return True, numbers[0]

    except FileNotFoundError:
        print("Файл не найден и будет создан.")
        return True, 0
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False, 0


def upload_data(number, image, extra_data = '#####'):
    global current_x_coordinate
    global current_y_coordinate
    status, width, height = get_screen_size()
    try:
        extra_data = [current_x_coordinate,
                current_y_coordinate,
                width*current_x_coordinate//100,
                height*current_y_coordinate//100,
                width,
                height]
        print(str(number+1), extra_data)
        cv2.imwrite(f'Eyes_data/{number+1}.jpg', image)

        with open('Eyes_data/0_data.txt', 'a') as file:
            if (number) != 0:
                file.write('\n')
            file.write(f'{str(number+1)} {str(extra_data)}')
        
        current_x_coordinate = random.randint(5, 95)
        current_y_coordinate = random.randint(5, 95)

        return True
    
    except Exception as e:
        print('Error in upload data function', e)

        return False


def take_screenshot(key):
    try:
        if key.char == 'q':
        # Stop listener
            return False

        if key.char == 'p':
            status, frame = Get_image.get_screenshot()

            if not status:
                print('Error in Get_image.get_screenshot')
                
            else:
                status, data = extract_last_screenshot_id()
                try:
                    data = int(data)
                except:
                    print('Error in getting last digit from file')
                    status = False
            if not status:
                print('Ошика в extract_last_screenshot_id из take_screenshot')
            else:
                status = upload_data(data, frame)
                
            if not status:
                print('Error in upload_data')

        return True
    
    except Exception as e:
        print(f'Failure in take_screenshot function - ',e)

        return True


#------------ \/ open white screen \/ ---------------------------------


current_x_coordinate = random.randint(5, 95)
current_y_coordinate = random.randint(5, 95)


def open_screen(width = 1920, height = 1080):
    global current_x_coordinate
    global current_y_coordinate
    
    white_image = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Define the top-left corner and size of the red circle
    circle_size = (width+height)//2//100  # Size of the circle
    top_left_x = (width) // 100 * current_x_coordinate
    top_left_y = (height) // 100 * current_y_coordinate

    cv2.putText(white_image, 'p - screenshot, q - quit',
                 (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    # Draw a red circle on the white image
    cv2.circle(white_image, (top_left_x, top_left_y), 
                  circle_size, 
                  (0, 0, 255), -1)  # Color in BGR format

    # Create a named window
    cv2.namedWindow('Teaching model screen', cv2.WND_PROP_FULLSCREEN)

    # Set the window to full screen
    cv2.setWindowProperty('Teaching model screen', 
                          cv2.WND_PROP_FULLSCREEN, 
                          cv2.WINDOW_FULLSCREEN)

    # Display the image
    cv2.imshow('Teaching model screen', white_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return 2
    return 0


def get_screen_size():
    # Create a hidden Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return True, screen_width, screen_height 


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=take_screenshot)
    listener.start()
    status, width, height = get_screen_size()
    while True:
        flag = Get_image.show()

        if flag > 0:
            break
        
        flag = open_screen(width, height)

        if flag > 0:
            break