import cv2


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

def show():
    ret, frame = cap.read()

    if not ret:
        print("Error: Frame could not be captured.")
        end_showing()
        return False

    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Press 'q' on the keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        end_showing()
        return False
    return True

    


def get_screenshot():
    ret, frame = cap.read()

    if not ret:
        print("Error: Frame could not be captured.")
        end_showing()
        return False, 0
    
    return True, frame


def end_showing():
    cap.release()
    cv2.destroyAllWindows()
