import pygame
import wave

'''
CHANNELS = 1
swidth = 2
Change_RATE = 3.5

spf = wave.open('out.wav', 'rb')
RATE=spf.getframerate()
signal = spf.readframes(-1)

wf = wave.open('out_adjusted.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(swidth)
wf.setframerate(RATE*Change_RATE)
wf.writeframes(signal)
wf.close()
'''

pygame.mixer.init(48000)
pygame.mixer.music.load("file.wav")
pygame.sndarray.array(pygame.mixer.music)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
