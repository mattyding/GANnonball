import os, glob
import mido

import numpy as np


segment_time = 30 #

def loadData():
    '''
    get notes from all midi files
    '''
    os.chdir('data/')
    midi_files = glob.glob('*.mid')

    num_msgs = 0
    for midi_file in midi_files:
        for msg in mido.MidiFile(midi_file).tracks[0]:  # only one melody track
            if not msg.is_meta: 
                num_msgs += 1
    
    '''
    data[i] = [note_on/note_off, channel, note, velocity, time]
    
    Ex: 
        mido.Message('note_off', channel=0, note=58, velocity=83, time=276) --> ['off' 0 58 83 276]
    '''

    data = np.zeros((len(midi_files), 30000), dtype=float)

    for i in range(len(midi_files)):
        noteStarts = {}
        noteEnds = {}
        currTime = 0
        for msg in mido.MidiFile(midi_files[i]).tracks[0]:  # only one melody track
            if msg.is_meta: 
               continue

            type = msg.type
            note = msg.note
            velocity = msg.velocity
            time = msg.time
            channel = msg.channel
            currTime += time

            if type == 'note_on':
                if note not in noteStarts:
                    noteStarts[note] = []
                noteStarts[note].append(currTime) #TODO: add velocity as tuple or something
            if type == 'note_off':
                if note not in noteEnds:
                    noteEnds[note] = []
                noteEnds[note].append(currTime)
        

        notes = list(noteStarts.keys())
        for note in notes:
            starts = [x for x in noteStarts[note]]
            ends = [x for x in noteEnds[note]]

            starts.sort()
            ends.sort()

            for j in range(len(starts)):
                data[i][starts[j]:ends[j]] = note

        print(f"finished processing {midi_files[i]}", end='\r')
    return data
            


if __name__ == '__main__':
    print(loadData())