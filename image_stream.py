import queue

import cv2


def start_streaming(display_queue: queue.Queue):
    STATIC = "images/cartoon/still.png"
    START_BLINKING = "images/cartoon/blink1.png"
    EYES_CLOSED = "images/cartoon/blink3.png"
    END_BLINKING = "images/cartoon/blink4.png"

    TALKING_1 = "images/talking/talking1.png"
    TALKING_2 = "images/talking/talking2.png"
    TALKING_3 = "images/talking/talking3.png"
    TALKING_4 = "images/talking/talking4.png"
    TALKING_5 = "images/talking/talking5.png"
    TALKING_6 = "images/talking/talking6.png"
    TALKING_7 = "images/talking/talking7.png"
    TALKING_8 = "images/talking/talking8.png"
    TALKING_9 = "images/talking/talking9.png"

    images = {
        "static": cv2.imread(STATIC),
        "start_blinking": cv2.imread(START_BLINKING),
        "end_blinking": cv2.imread(END_BLINKING),
        "eyes_closed": cv2.imread(EYES_CLOSED),
        "talking_1": cv2.imread(TALKING_1),
        "talking_2": cv2.imread(TALKING_2),
        "talking_3": cv2.imread(TALKING_3),
        "talking_4": cv2.imread(TALKING_4),
        "talking_5": cv2.imread(TALKING_5),
        "talking_6": cv2.imread(TALKING_6),
        "talking_7": cv2.imread(TALKING_7),
        "talking_8": cv2.imread(TALKING_8),
        "talking_9": cv2.imread(TALKING_9),
    }

    for name, img in images.items():
        if img is None:
            print(f"Warning: Could not load image for {name}")

    cv2.namedWindow("Talking Animation", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Talking Animation", 800, 600)

    current_image = images["static"]

    while True:
        try:
            try:
                image_to_show = display_queue.get_nowait()
                if image_to_show in images and images[image_to_show] is not None:
                    current_image = images[image_to_show]
            except queue.Empty:
                pass

            cv2.imshow("Talking Animation", current_image)

            key = cv2.waitKey(1)
            if key == 27:
                break
        except Exception as e:
            print(f"Error displaying image: {e}")
            break

    cv2.destroyAllWindows()
