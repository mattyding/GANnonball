import mido


def main():
    mid = mido.MidiFile('data/CannonballAdderley_HighFly_FINAL.mid', clip=True)
    for track in mid.tracks:
        for msg in track:
            print(msg)


if __name__ == '__main__':
    main()