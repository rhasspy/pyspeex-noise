import array
import math
import statistics
import wave
from pathlib import Path

from pyspeex_noise import AudioProcessor

_DIR = Path(__file__).parent

SAMPLES_10MS = 160
BYTES_10MS = SAMPLES_10MS * 2


def _get_energy(chunk: bytes):
    """RMS"""
    chunk_array = array.array("h", chunk)
    energy = -math.sqrt(sum(x**2 for x in chunk_array) / len(chunk_array))
    debiased_energy = math.sqrt(
        sum((x + energy) ** 2 for x in chunk_array) / len(chunk_array)
    )

    return debiased_energy


def test_no_processing():
    """Test that audio is not changed if no auto gain or noise suppression is applied."""
    audio_processor = AudioProcessor(0, 0)
    data_in = bytes(320)
    result = audio_processor.Process10ms(data_in)
    assert result.audio == data_in


def test_noise_suppression():
    """Test default settings on a noisy file."""
    audio_processor = AudioProcessor(4000, -30)
    noisy_energy = []
    clean_energy = []

    with wave.open(str(_DIR / "noise.wav"), "rb") as wav_file:
        assert wav_file.getframerate() == 16000
        assert wav_file.getsampwidth() == 2
        assert wav_file.getnchannels() == 1

        chunk = wav_file.readframes(SAMPLES_10MS)
        while len(chunk) == BYTES_10MS:
            clean_chunk = audio_processor.Process10ms(chunk).audio
            noisy_energy.append(_get_energy(chunk))
            clean_energy.append(_get_energy(clean_chunk))
            chunk = wav_file.readframes(SAMPLES_10MS)

    # A lot less energy
    assert (statistics.mean(noisy_energy) / statistics.mean(clean_energy)) > 30
