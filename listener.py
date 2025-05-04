import time
from multiprocessing import Queue

from audio_processor import AudioProcessor

TALKING_STARTED = False
TALKING_IN_PROGRESS = False
CURRENT_TALKING_FRAME = 3


def listen(queue: Queue, audio_file: str = "tts_example.mp3") -> None:
    global TALKING_IN_PROGRESS
    global TALKING_STARTED
    global CURRENT_TALKING_FRAME

    audio_processor = AudioProcessor(audio_file)

    # TODO: adjust this if there are any sights or smthg.
    VOLUME_THRESHOLD = 0.01

    for _, volume in audio_processor.get_audio_chunks():
        # Normalize volume to a 0-1 range. Meditate on it pls.
        normalized_volume = min(volume * 10, 1.0)

        if normalized_volume < VOLUME_THRESHOLD:
            if TALKING_IN_PROGRESS:
                TALKING_IN_PROGRESS = False
                TALKING_STARTED = False
                queue.put("talking_2")  # End talking animation
            else:
                queue.put("static")
        else:
            if not TALKING_IN_PROGRESS:
                queue.put("talking_1")  # Start talking animation
                TALKING_IN_PROGRESS = True
                TALKING_STARTED = True
            elif TALKING_IN_PROGRESS and TALKING_STARTED:
                queue.put("talking_2")
                TALKING_STARTED = False
            else:
                # TODO: try to select talking frame based on volume intensity?
                # talking_frame = min(int(normalized_volume * 6) + 3, 6)

                CURRENT_TALKING_FRAME += 1
                if CURRENT_TALKING_FRAME > 9:
                    CURRENT_TALKING_FRAME = 3
                queue.put(f"talking_{CURRENT_TALKING_FRAME}")

        # delay to match audio playback?
        time.sleep(0.01)
