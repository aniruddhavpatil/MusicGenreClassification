import numpy as np
import sys
import wave
# import sunau
import scipy.io.wavfile
from scipy.fftpack import dct
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from pydub import AudioSegment
import scipy
from scipy.signal import hamming

def mel(n):
    return 1125 * np.log(1 + float(n)/700)

def meli(n):
    return 700 * (np.exp(float(n)/1125) - 1)

def createbankpoints(l,h):
    n = 42
    step = (h - l)/n
    outmel = np.zeros(n+1)
    outnormal = np.zeros(n+1)
    done = False
    i = 0
    val = l
    while not done:
        if i > n - 1:
            done = True
        outmel[i] = val
        outnormal[i] = meli(val)
        val += step
        i += 1
    return outmel,outnormal

def calc_mfcc(filename):
    (rate,sig) = wav.read(filename)
    startFrame = np.round(2*rate)
    endFrame = np.round(28*rate)
    sig = sig[startFrame:endFrame]

    winstep = 0.01
    winlen = 0.02
    nfft = 512
    remn = 257

    lowerfreq = mel(30)
    highfreq = mel(6000)
    bankpoints,bankpointsnormal = createbankpoints(lowerfreq,highfreq)

    bins = np.array([])

    for i in bankpointsnormal:
        bins = np.append(bins, np.floor((nfft + 1) * float(i)/rate))

    flbank = np.zeros((remn, len(bins)))

    for i in range(1,len(bins) - 1):
        for j in range(1,remn - 1):
            if j < bins[i-1]:
                flbank[j][i] = 0
            elif bins[i-1] <= j and j <= bins[i]:
                flbank[j][i] = float(j - bins[i-1])/(bins[i] - bins[i-1])
            elif bins[i] <= j and j <= bins[i+1]:
                flbank[j][i] = float(bins[i+1] - j)/(bins[i+1] - bins[i])
            else:
                flbank[j][i] = 0

    framestep = np.int64(winstep * rate)
    mel_map = np.array([])

    features = []
    for i in range(0,len(sig), framestep - 1):
        tempsig = sig[i: i+ framestep-1]
        tempsig = hamming(len(tempsig)) * tempsig
        tempfft = scipy.fftpack.fft(tempsig,n=512)
        tempfft = tempfft[0:257]
        power = np.square(np.abs(tempfft))/len(tempfft)
        flenergies = np.array([])
        for i in np.transpose(flbank):
            if np.dot(i,power) != 0:
                flenergies = np.append(flenergies, np.log(np.dot(i,power)))
        dctenergies = scipy.fftpack.dct(flenergies)
        dctenergies = dctenergies[0:25]
        features.append(dctenergies)
    # features = np.transpose(np.array(features))
    # cov = np.cov(features)
    # mn = np.mean(features,axis=1)
    #
    # # print rate
    # # return mfcc(sig,rate)
    # features = mfcc(
    #             signal=sig[startFrame:endFrame],
    #             samplerate=rate,
    #             winlen=0.02,
    #             winfunc=np.hamming,
    #             winstep=0.01,
    #             appendEnergy=False,
    #             ceplifter=0,
    #             preemph=0,
    #             numcep=15,
    #             )
    # print features
    # # d_mfcc_feat = delta(mfcc_feat, 2)
    # # fbank_feat = logfbank(sig,rate)
    # print startFrame,endFrame,endFrame - startFrame, output.shape,rate
    return np.array(features)

# calc_mfcc(sys.argv[1])
