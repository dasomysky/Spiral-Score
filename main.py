import numpy as np
import matplotlib.pyplot as plt
import mido
from mido import MidiFile
import time
from matplotlib.animation import FuncAnimation

aria = MidiFile('/Users/rhye/Desktop/UGRP/test2.mid')
#output = mido.open_output('IAC Driver Bus 1')

r_data = []
theta_data = []
messages = [msg for msg in aria if msg.type == 'note_on']


def midi2polar(noteVal):
    freq = (440.0/32) * (2**((noteVal-9)/12))
    return [1/freq, 2*np.pi*np.log2(freq/261.45)]

def max_r():
    max = 128
    for msg in messages: 
        if msg.note < max: max = msg.note
    print (max)
    return midi2polar(max)[0]

def storyboard():
# returns r, theta at a given timestamp
    
    stbd = []
    for msg in messages:
        if msg.type == 'note_on':
            [r, theta] = midi2polar(msg.note)
            if msg.velocity != 0:
                r_data.append(r)
                theta_data.append(theta)
        
            if msg.velocity == 0:
                r_data.remove(r)
                theta_data.remove(theta)
        
            temp = {'r': r_data.copy(), 'theta': theta_data.copy(), 'time': msg.time}
            stbd.append(temp)
            
            
    return stbd

def copyist(storyboard):
# draws the spiral score
    maxr = max_r()*1.1

    for frame in storyboard:
        
        plt.axes(projection = 'polar')
        plt.grid(True)
        plt.ylim(0,maxr) 
        plt.autoscale(False)
        plt.thetagrids(range(0,360,30), ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B') )   
        plt.draw()
        r = frame['r']
        theta = frame['theta']
        plt.polar(theta, r, 'o')
        if frame['time'] != 0:
            plt.pause(frame['time'])
        else: continue
        plt.clf()
        
    plt.show()

copyist(storyboard())

# time이 0 일 때 frame merge 할 것

