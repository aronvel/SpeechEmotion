from aubio import source
from numpy import array,ma
import aubio as au
import glob as gb
import scipy.io.wavfile as sc
import analyse as an

# Function  to get the pitch from a wav file
def getPitch(filename):
    from aubio import pitch
    for f in gb.glob(filename):
            frate, inputdata = sc.read(f)
    downsample = 1
    samplerate = frate / downsample
    window = 1024 / downsample # fft size

    hopsize = 256/ downsample
    sound = source(filename, samplerate, hopsize)
    samplerate = sound.samplerate
    tolerance = 0.8

    # Setting the FFT Algorithm
    pitchlist = pitch("yin", window, hopsize, samplerate)
    pitchlist.set_unit("midi")

    # Setting the tolerance level to 80 percent
    pitchlist.set_tolerance(tolerance)
    total_frames = 0
    pitches = []
    confidences=[]
    while True:
        samples, read = sound()
        pitch = pitchlist(samples)[0]
        confidence = pitchlist.get_confidence()
        confidences+=[confidence]
        pitches += [pitch]
        total_frames += read
        if read < hopsize: break

    # getting the file list of pitch from various sound samples
    pitches = array(pitches[1:])
    confidences = array(confidences[1:])
    cleaned_pitches = pitches

    loudness = abs(an.loudness(inputdata))
    
    # EXtracting all those pitch levels that are above the confidence values
    cleaned_pitches = ma.masked_where(confidences < tolerance, cleaned_pitches,copy=False)
    cleaned_pitches = cleaned_pitches[~cleaned_pitches.mask]

    # condition to check whether there exists a fundamental frequency for the given sound signal
    if len(cleaned_pitches)==0:
        maxValue = 0
    else:
        maxValue = max(cleaned_pitches)
    return maxValue,loudness

if __name__=="__main__":
    print getPitch("/mnt/c/Users/dell/Desktop/testt.wav")

