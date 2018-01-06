
import soundfile
import sys

def main():
    signal, sampleRate = soundfile.read(sys.argv[1], dtype='int16')
    signal = [s[0] for s in signal]




if __name__ == '__main__':
    main()