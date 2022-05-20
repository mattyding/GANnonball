import glob
import mido
import config

import numpy as np

def loadData(songLen=3000):
    '''
    get notes from all midi files
    '''
    midi_files = glob.glob('data/*.mid')

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

    data = []

    n = len(midi_files)

    for i in range(n):

        song = np.zeros((int(songLen/config.MIDI_RESOLUTION), config.MIDI_NOTE_RANGE), dtype=float)

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
                noteStarts[note].append(int(currTime/config.MIDI_RESOLUTION)) #TODO: add velocity as tuple or something
            if type == 'note_off':
                if note not in noteEnds:
                    noteEnds[note] = []
                noteEnds[note].append(int(currTime/config.MIDI_RESOLUTION))
        

        notes = list(noteStarts.keys())
        # print(song.shape)
        for note in notes:
            starts = [x for x in noteStarts[note]]
            ends = [x for x in noteEnds[note]]

            starts.sort()
            ends.sort()

            for j in range(len(starts)):
                for k in range(starts[j], ends[j]+1):
                    if k < len(song):
                        song[int(k)][min(int(note - config.MIDI_NOTE_RANGE/2), config.MIDI_NOTE_RANGE)] = 1
                        
        data.append(song)
        print(f"finished processing {midi_files[i]}", end='\r')
    return np.array(data)
            


if __name__ == '__main__':
    loadData()
    print("yuh")