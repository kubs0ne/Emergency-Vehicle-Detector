import pyaudio
import os
import struct
import numpy as np
from scipy.fftpack import fft
import time

C = 1024 * 2             
F = pyaudio.paInt16  
CH = 1             
R = 44100              

p = pyaudio.PyAudio()

stream = p.open(
    format=F,
    channels=CH,
    rate=R,
    input=True,
    output=True,
    frames_per_buffer=C
)
xf = np.linspace(0, R, C)
while True:
    
    data = stream.read(C)  
    data_int = struct.unpack(str(2*C) + 'B', data)
    data_np = np.array(data_int, dtype='b')[::2] + 128
    yf = fft(data_int)
    ydata=np.abs(yf[0:C]) / (128 * C)
    for i,j in zip(xf,ydata):
        if i>600 and i<1300 and j >0.4:
            print ('karetka')

    
