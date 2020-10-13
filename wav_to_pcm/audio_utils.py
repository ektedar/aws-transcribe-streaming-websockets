import pyaudio
import wave

# Transcribe only supports 16kHz audio, therefore 44.1kHz needs to be downsampled before being send into through the ws
def downsample_audio_buffer(buffer, input_sample_rate, output_sample_rate = 16000):
    if input_sample_rate == 44100:
        return buffer
    
    sample_rate_ratio = input_sample_rate / output_sample_rate
    new_length = round(buffer.length / sample_rate_ratio)
    result = float(new_length)

    offset_result = 0
    offset_buffer = 0

    while (offset_result < len(result)):

        next_offset_buffer = round(offset_result + 1) * sample_rate_ratio

        accum = 0
        count = 0

        i = offset_buffer
        while (i < next_offset_buffer) and (i < len(buffer)):
            accum += buffer[i]
            count += 1

        result[offset_result] = accum / count
        offset_result += 1
        offset_buffer = next_offset_buffer
    
    return result


def capture_mic_audio():
    FORMAT = pyaudio.paInt16
    CHANNEL = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECOND = 5
    WAVE_OUTPUT_FILENAME = "mic_output.wav"

    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(
                format=FORMAT, 
                channels=CHANNEL,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
    print("recording...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECOND)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
    
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNEL)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # Return the name of the wav file and the data
    return data, WAVE_OUTPUT_FILENAME
