from array import array
import pyaudio
import wave
import pygame
import RPi.GPIO as GPIO
import time
from time import sleep

A = 11
B = 12
T = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(A, GPIO.IN)
GPIO.setup(B, GPIO.IN)
GPIO.setup(T, GPIO.IN)

pressed_A = False
pressed_B = False

# RECORDING INFO
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1024
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "memo.wav"
 
recorded = False

delete_time = 0
delete_limit = 5

reminder_time = time.time()
reminder_limit = 20

talking_time = time.time()
talking_limit = 2

noise_samples = 5

while True:

    if(not GPIO.input(T)):  #change or comment out for testing!!!
        #print(GPIO.input(T))
        reminder_limit = 120
    elif(GPIO.input(T)):
        #print(GPIO.input(T))
        reminder_limit = 600
        
    current = time.time()
    if (not GPIO.input(A) and not pressed_A):
        print("A PRESS")
        pressed_A = True

        if not recorded:
            print("begin recording")
            frames = []
            bgnoise = 0
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
            started = False
            talking = False
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                as_ints = array('h', data)
                max_value = max(as_ints)
                # print(max_value)
                if i < noise_samples:
                    bgnoise += max_value / noise_samples
                    print("sample")
                else:
                    if max_value > 3 * bgnoise:
                        print("LOUD")
                        started = True
                        talking = True
                        talking_time = time.time()
                    else:
                        print("QUIET")
                        talking = False
                        if started and time.time() - talking_time > talking_limit:
                            print("done")
                            break
                frames.append(data)
                
            print("finished recording")
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()

            recorded = True
            reminder_time = time.time()
        else:
            print("replay by request")
            pygame.mixer.init(48000)
            pygame.mixer.music.load("file.wav")
            pygame.sndarray.array(pygame.mixer.music)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            reminder_time = time.time()
            
    elif (not GPIO.input(B) and not pressed_B and recorded):
        print("B PRESS")
        if current - delete_time > delete_limit:
            pressed_B = True
            print("delete warning")
            pygame.mixer.init(48000)
            pygame.mixer.music.load("file.wav")
            pygame.sndarray.array(pygame.mixer.music)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

            delete_time = time.time()
            reminder_time = time.time()
        elif current - delete_time <= delete_limit :
            recorded = False
            print("deleted")
    if time.time() - reminder_time > reminder_limit and recorded:
        print("reminder")
        pygame.mixer.init(48000)
        pygame.mixer.music.load("file.wav")
        pygame.sndarray.array(pygame.mixer.music)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        reminder_time = time.time()

    # Released buttons
    if (GPIO.input(A) and pressed_A):
        print("A UP")
        pressed_A = False
    if (GPIO.input(B) and pressed_B):
        print("B UP")
        pressed_B = False
        
    sleep(0.01)
