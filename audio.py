import pyaudio
import wave
import os
import threading

class WavePlayerLoop(threading.Thread):

    def __init__(self, filepath, repitir, loop=True):
        super(WavePlayerLoop, self).__init__()
        self.filepath = os.path.abspath(filepath)
        self.loop = loop
        self.repitir = repitir

    def run(self):
        CHUNK = 2048
        wf = wave.open(self.filepath, 'rb')
        player = pyaudio.PyAudio()
        stream = player.open(
            format=player.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        data = wf.readframes(CHUNK)
        while self.loop:
            stream.write(data)
            data = wf.readframes(CHUNK)
            if data == b'':
                self.stop()
            if self.repitir:
                wf.rewind()
        stream.close()
        player.terminate()

    def play(self):
        self.start()

    def stop(self):
        self.loop = False

"""
def principal():
    tocar = WavePlayerLoop("audio/sucesso.wav")
    tocar.play()
    print('Olá')
    #x = input('Sair: ')
    x = "n"
    if x == 's':
        tocar.stop()

if __name__ == "__main__":
    principal()

"""
