from typing import Generator
import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioProcessor:
    def __init__(self, audio_file: str):
        self.audio_file = audio_file
        self.data, self.sample_rate = sf.read(audio_file)
        if len(self.data.shape) > 1:
            self.data = self.data.mean(axis=1)  # Convert to mono if stereo

        self.data = self.data.astype(np.float32)
        self.chunk_size = int(self.sample_rate // 10)

    def get_audio_chunks(self) -> Generator[tuple[np.ndarray, float], None, None]:
        """Yield audio chunks and their volume levels while playing audio"""
        # Start audio stream
        stream = sd.OutputStream(
            samplerate=self.sample_rate, channels=1, dtype=np.float32
        )
        stream.start()

        try:
            for i in range(0, len(self.data), self.chunk_size):
                chunk = self.data[i : i + self.chunk_size]
                if len(chunk) < self.chunk_size:
                    chunk = np.pad(chunk, (0, self.chunk_size - len(chunk)))

                stream.write(chunk)

                volume = np.sqrt(np.mean(chunk**2))
                yield chunk, volume
        finally:
            stream.stop()
            stream.close()

    def get_sample_rate(self) -> int:
        return self.sample_rate
