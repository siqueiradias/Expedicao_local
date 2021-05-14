import pygame
#import wave
import os
import threading
from time import sleep

class WavePlayerLoop(threading.Thread):

    def __init__(self, filepath, repitir=False, loop=True):
        super(WavePlayerLoop, self).__init__()
        self.filepath = os.path.abspath(filepath)
        self.loop = loop
        self.repitir = repitir

    def run(self):
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048) 
        sound = pygame.mixer.Sound(self.filepath)
        while self.loop:
            sound.play()
            sleep(sound.get_length())
            if not(self.repitir):
                self.stop()
    
    def play(self):
        self.start()

    def stop(self):
        self.loop = False
        
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

