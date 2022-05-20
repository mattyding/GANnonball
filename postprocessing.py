import numpy as np
import mido
import config


def vecToMidi(vec):
    # get the difference
    new_vec = np.concatenate([np.array([[0] * config.MIDI_NOTE_RANGE]), np.array(vec)], axis=0)
    new_vec = np.repeat(new_vec, config.MIDI_RESOLUTION, axis=0)
    changes = new_vec[1:] - new_vec[:-1]
    # create a midi file with an empty track
    mid_new = mido.MidiFile()
    track = mido.MidiTrack()
    mid_new.tracks.append(track)
    # add difference in the empty track
    last_time = 0
    for ch in changes:
        if set(ch) == {0}:  # no change
            last_time += 1
        else:
            on_notes = np.where(ch > 0)[0]
            on_notes_vol = ch[on_notes]
            off_notes = np.where(ch < 0)[0]
            first_ = True
            for n, v in zip(on_notes, on_notes_vol):
                # print(n, v)
                new_time = last_time if first_ else 0
                track.append(mido.Message('note_on', note=int(n + 21 + config.MIDI_NOTE_RANGE/2), velocity=int(v*100),
                                          time=int(new_time)))
                first_ = False
            for n in off_notes:
                new_time = last_time if first_ else 0
                track.append(mido.Message('note_off', note=int(n + 21 + config.MIDI_NOTE_RANGE/2), velocity=0, time=new_time))
                first_ = False
            last_time = 0
    return mid_new