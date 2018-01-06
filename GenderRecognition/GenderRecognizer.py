from __future__ import division
from pylab import *
from numpy import *
from scipy import *
from ipywidgets import *
import math as mt
import soundfile
import sys
import scipy.signal
import glob


def main():
    thresh = 700
    for shift in range(0, 100, 10):
        maleCount = 0
        femaleCount = 0
        maleHit = 0
        femaleHit = 0
        maleFreqSum = 0
        femaleFreqSum = 0
        print("Częstotliwość rozróżniania = ", 700 + shift)
        for name in glob.glob("train/*.wav"):
            signal, sampleRate = soundfile.read(name, dtype='int16')
            if (len(signal.shape) == 2):
                signal = [s[0] for s in signal]
            w = 1
            signal = signal[::w]  # co w-ty element

            fftSignal = fft(signal)
            fftSignalHalf = fftSignal[1:int(len(fftSignal) / 2)]
            fftSignalAmpl = abs(fftSignalHalf) * 2 / len(signal)

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
                if "K" in name:
                    femaleHit += 1
            else:
                if "M" in name:
                    maleHit += 1

            if "M" in name:
                maleCount += 1
                maleFreqSum += maxFreq
            if "K" in name:
                femaleCount += 1
                femaleFreqSum += maxFreq
        print("Ilość mężczyzn : ", maleCount, " rozpoznanych : ", maleHit, " średnio Hz = ", maleFreqSum / maleCount)
        print("Ilość kobiet : ", femaleCount, " rozpoznanych : ", femaleHit, " średnio Hz = ",
              femaleFreqSum / femaleCount)
        print("Częstotliwość rozróżniania = ", 700 + shift, " rozpoznanych ", maleHit + femaleHit, "/",
              maleCount + femaleCount, " = ", (maleHit + femaleHit) / (maleCount + femaleCount) *100, "%")


if __name__ == '__main__':
    main()
