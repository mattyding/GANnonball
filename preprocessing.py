import os, glob
import mido

import numpy as np


def main():
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
    
    data = np.empty((num_msgs, 5), dtype=object)
    '''
    data[i] = [note_on/note_off, channel, note, velocity, time]
    
    Ex: 
        mido.Message('note_off', channel=0, note=58, velocity=83, time=276) --> ['off' 0 58 83 276]
    '''

    # TODO: some clustering where notes from the same piece are clustered together?
    counter = 0
    for midi_file in midi_files:
        for msg in mido.MidiFile(midi_file).tracks[0]:  # only one melody track
            if msg.is_meta: 
                print(str(msg))
                continue
            
            msg_data = str(msg).split()
            data[counter][0] = msg_data[0].split('_')[1]
            data[counter][1] = int(msg_data[1].split('=')[1])
            data[counter][2] = int(msg_data[2].split('=')[1])
            data[counter][3] = int(msg_data[3].split('=')[1])
            data[counter][4] = int(msg_data[4].split('=')[1])
            counter += 1
        print(f"finished processing {midi_file}", end='\r')
    print(data)
            


if __name__ == '__main__':
    main()