# pyspeex-noise

Noise suppression and automatic gain control using speex.

``` python
from pyspeex_noise import AudioProcessor

auto_gain = 4000
noise_suppression = -30
audio_processor = AudioProcessor(auto_gain, noise_suppression)

# Process 10ms chunks of 16-bit mono PCM @16Khz
while audio := get_10ms_of_audio():
    assert len(audio) == 160 * 2  # 160 samples
    clean_audio = audio_processor.Process10ms(audio).audio
```
