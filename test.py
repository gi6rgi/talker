from multiprocessing import Process
from image_stream import start_streaming
from listener import listen
from multiprocessing import Queue

display_queue = Queue()


def main() -> None:
    image_streaming_proc = Process(target=start_streaming, args=(display_queue,))
    listener_streaming_proc = Process(target=listen, args=(display_queue,))
    image_streaming_proc.start()
    listener_streaming_proc.start()

    image_streaming_proc.join()
    listener_streaming_proc.join()


if __name__ == "__main__":
    main()
