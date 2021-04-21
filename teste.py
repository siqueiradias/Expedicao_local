from threading import Thread
from time import sleep
import pygame

def tocar_audio(audio):
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048) 
    print ("hey I finaly got this working!" )
    sounds = [] 
    sounds.append(pygame.mixer.Sound('audio/sucesso.wav')) 
    sounds.append(pygame.mixer.Sound('audio/erro.wav')) 
    #sounds.append(pygame.mixer.Sound('D:/Users/John/Music/Music/turret.OGG')) 
    #sounds.append(pygame.mixer.Sound('D:/Users/John/Music/Music/portalend.OGG')) 
    for sound in sounds:
        sound.play()
        sleep(sound.get_length())
    sounds[audio]
    sound.play()
    sleep(sounds[audio].get_length())

def teste(valor):
    for i in range(valor):
        print("Valor: ", i)
        sleep(1)

thread1 = Thread(tocar_audio(1))
thread2 = Thread(teste(10))
thread2.start()
#thread1.start()
#thread1.join()
thread2.join()
print ("thread finished...exiting")