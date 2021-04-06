import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError


# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16   # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
fig, ax2 = plt.subplots(1, figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
# x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

# create a line object with random data
# line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# format spectrum axes
ax2.set_xlim(20, RATE / 2)
ax2.set_title('Analiza widmowa')
ax2.set_xlabel('Częstotliwość (Hz)')
ax2.set_ylabel('Amplituda')
fig.show()

print('stream started')


while True:
    
    # binary data
    data = stream.read(CHUNK)  
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2*CHUNK) + 'B', data)
#     data_int = np.frombuffer(data, dtype='h')  
#     data_np = np.array(data_int, dtype='h')/140 + 255

    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    #line.set_ydata(data_np)
    
    # compute FFT and update line
    yf = fft(data_int)
    ydata=np.abs(yf[0:CHUNK]) / (128 * CHUNK)
    line_fft.set_ydata(ydata)
    for i,j in zip(xf,ydata):
        if i>600 and i<1300 and j >0.3:
            print ('karetka')

    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        
    except TclError:
        
        # calculate average frame rate
        
        
        print('stream stopped')
        break
