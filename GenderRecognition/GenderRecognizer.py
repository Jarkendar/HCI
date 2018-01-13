from __future__ import division
from numpy import *
from scipy import *
import soundfile
import sys
import scipy.signal


def nearest2Power(length):
    pow = 0
    number = 2
    while (number ** pow < length):
        pow += 1
    return number ** (pow - 1)


def main():
    thresh = 460
    signal, sampleRate = soundfile.read(sys.argv[1], dtype='int16')
    if (len(signal.shape) == 2):
        signal = [s[0] for s in signal]
    w = 1
    signal = signal[::w]  # co w-ty element

    signal2 = zeros(nearest2Power(len(signal)))
    for i in range(len(signal2)):
        signal2[i] = signal[i]

    fftSignal = fft(signal2)
    fftSignalHalf = fftSignal[1:int(len(fftSignal) / 2)]
    fftSignalAmpl = abs(fftSignalHalf) * 2 / len(signal2)

    fftSignalAmpl[:80] = 0

    fftSignalAmpl2 = scipy.signal.decimate(fftSignalAmpl, 2, n=5, ftype='iir', zero_phase=True)
    fftSignalAmpl3 = scipy.signal.decimate(fftSignalAmpl, 3, n=5, ftype='iir', zero_phase=True)
    fftSignalAmpl4 = scipy.signal.decimate(fftSignalAmpl, 4, n=5, ftype='iir', zero_phase=True)
    fftSignalAmpl5 = scipy.signal.decimate(fftSignalAmpl, 5, n=5, ftype='iir', zero_phase=True)

    mulFFTSingalAmpl = [0 for x in range(len(fftSignalAmpl5))]
    for i in range(len(fftSignalAmpl5)):
        mulFFTSingalAmpl[i] = fftSignalAmpl[i] * fftSignalAmpl2[i] * fftSignalAmpl3[i] * fftSignalAmpl4[i] * \
                              fftSignalAmpl5[i]

    maxAmpl = max(mulFFTSingalAmpl)
    maxFreq = 0

    for i in range(len(mulFFTSingalAmpl)):
        if (mulFFTSingalAmpl[i] == maxAmpl):
            maxFreq = i

    if (maxFreq > thresh):
        print("K")
    else:
        print("M")


if __name__ == '__main__':
    main()
