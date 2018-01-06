from __future__ import division

import sys
import numpy
import scipy.signal
import soundfile
from scipy import *


def main():
    thresh = 700
    signal, sample_rate = soundfile.read(sys.argv[1], dtype='int16')
    if len(signal.shape) == 2:
        signal = [s[0] for s in signal]

    signal = signal[::1]

    fft_signal = fft(signal)
    fft_signal_half = fft_signal[1:int(len(fft_signal) / 2)]
    fft_signal_ampl = abs(fft_signal_half) * 2 / len(signal)

    fft_signal_ampl[:80] = 0

    fft_signal_ampl2 = scipy.signal.decimate(fft_signal_ampl, 2, n=5, ftype='iir', zero_phase=True)
    fft_signal_ampl3 = scipy.signal.decimate(fft_signal_ampl, 3, n=5, ftype='iir', zero_phase=True)
    fft_signal_ampl4 = scipy.signal.decimate(fft_signal_ampl, 4, n=5, ftype='iir', zero_phase=True)
    fft_signal_ampl5 = scipy.signal.decimate(fft_signal_ampl, 5, n=5, ftype='iir', zero_phase=True)

    mul_fft_signal_ampl = [0 for x in range(len(fft_signal_ampl5))]
    for i in range(len(fft_signal_ampl5)):
        mul_fft_signal_ampl[i] = fft_signal_ampl[i] * fft_signal_ampl2[i] * fft_signal_ampl3[i] * fft_signal_ampl4[i] * \
                              fft_signal_ampl5[i]

    max_ampl = max(mul_fft_signal_ampl)
    max_freq = 0
    for i in range(len(mul_fft_signal_ampl)):
        if mul_fft_signal_ampl[i] == max_ampl:
            max_freq = i

    if max_freq > thresh:
        print("K")
    else:
        print("M")


if __name__ == '__main__':
    main()
