from pyspeex_noise import AudioProcessor


def test_audio_processor():
    audio_processor = AudioProcessor(0, 0)
    data_in = bytes(320)
    result = audio_processor.Process10ms(data_in)
    assert result.audio == data_in
