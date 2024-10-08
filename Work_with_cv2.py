import cv2
import logging



# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')



class Image:

    def __init__(self):
        self._cap = cv2.VideoCapture(0)
        if not self._cap.isOpened():
            logging.error("Can't open camera in __init__")
            exit()

    def end_showing(self):
        self._cap.release()
        cv2.destroyAllWindows()
        return True

    def update(self):
        
        status, self._frame = self._cap.read()
        if not status:
            self.end_showing()
            logging.warning("Can't read camera in update")
            return False, 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.info("Pressed q - exiting")
            self.end_showing()
            return False, 0
        
        return True, self._frame
    

    def show(self):
        status, self._frame = self.update()
        if status:
            cv2.imshow('Camera Feed', self._frame)
            return True
        return False
    # Press 'q' on the keyboard to exit
#    if cv2.waitKey(1) & 0xFF == ord('q'):
    def get_screenshot(self):
        status, self._frame = self.update()
        if not status:
            logging.warning("Can't get screenshot from get_screenshot")
            return False, 0
        return True, self._frame

