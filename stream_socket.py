import pickle
import json
import websocket
from aws_signature_v4 import return_url, get_audio_event
from send_audio_stream import convert_audio_to_binary

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        pcm_audio = convert_audio_to_binary('mic_output.wav')
        attached_headers = get_audio_event(pcm_audio)

        for i in range(len(pcm_audio)):
            time.sleep(1)
            ws.send(pickle.loads(attached_headers))
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    presigned_url = return_url()
    ws = websocket.WebSocketApp(presigned_url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()