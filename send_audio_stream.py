import socket
import json
import io
from scipy.io import wavfile
from aws_signature_v4 import return_url, get_audio_event
from wav_to_pcm.pcm_channels import pcm_channels
from wav_to_pcm.audio_utils import capture_mic_audio, downsample_audio_buffer

def convert_audio_to_binary(audio_file):
    """
    This function grabs the audio chunk, appends the necssary headers for AWS Transcribe and then returns a binary JSON

    @params : Audio Chunks
    output  : Binary JSON 
    """
    sample_rate, raw = wavfile.read(audio_file) # Capture microphone audio bytes

    # Check if the audio file is empty or not
    if len(raw) == 0:
        return None

    pcm_encoded_audio, _ = pcm_channels(audio_file)
    # print(sample_rate)
    if sample_rate != 16000:
        # Need to send in the raw audio binary value and not pcm_encoded version. Find a way to get the sample rate of the audio other than pcm channels
        downsampled_buffer = downsample_audio_buffer(raw, sample_rate, 16000)

        # Check if I am passing in the right buffer as the parameter here.  Not sure
        audio_event_message = get_audio_event(pcm_encoded_audio)

        # Convert the JSON object + header into a Binary Event Stream
        binary = json.dumps(audio_event_message).encode()

    return binary


def send_to_socket(audio_file):
    """
    This function packages the audio and the headers into a binary event and sends it to AWS Transcribe.

    @param: Audio File
    """
    pass
    # ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # presigned_url = return_url()  # Gets the pre-signed url to be used for AWS Transcribe streaming

    # ws.connect((str(presigned_url), 8443))

    # pcm_audio = convert_audio_to_binary(audio_file)

    # attach_headers = get_audio_event(pcm_audio)

    # ws.send(bytes(attach_headers))

    # msg = ws.recv()
    # print(msg)

if __name__ == "__main__":
    send_to_socket('mic_output.wav')
    # print(output)