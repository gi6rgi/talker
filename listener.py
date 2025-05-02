import numpy as np
import sounddevice as sd
from multiprocessing import Queue
from time import sleep
import random


SR = 16_000
BLOCK_SIZE = int(SR // 8)

TALKING_STARTED = False
TALKING_IN_PROGRESS = False


def listen(queue: Queue) -> None:
    print(sd.query_devices())

    def callback(indata: np.ndarray, frames: int, time, status) -> None:
        global TALKING_IN_PROGRESS
        global TALKING_STARTED

        # volume = np.max(np.abs(indata.flatten()))
        volume = np.linalg.norm(indata.flatten())
        print(volume)

        if volume < 0.3:
            if TALKING_IN_PROGRESS:
                TALKING_IN_PROGRESS = False
                TALKING_STARTED = False
                queue.put("talking_2")
            else:
                queue.put("static")

        if volume >= 0.3:
            if not TALKING_IN_PROGRESS:
                queue.put("talking_1")
                TALKING_IN_PROGRESS = True
                TALKING_STARTED = True
            elif TALKING_IN_PROGRESS and TALKING_STARTED:
                queue.put("talking_2")
                TALKING_STARTED = False
            else:
                talking_frame = random.randint(3, 6)
                # queue.put("talking_3")
                queue.put(f"talking_{talking_frame}")

    # uncomment when blinking is implemented.
    stream = sd.InputStream(samplerate=SR, device=2, channels=1, callback=callback, blocksize=BLOCK_SIZE)
    stream.start()

    while True:
        sleep(5)
        print("Listener is wokring and healty...")
