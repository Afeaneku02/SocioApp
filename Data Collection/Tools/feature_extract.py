import os
import librosa
# import librosa.display
import numpy as np
import pandas as pd
from datetime import datetime

# FIGURE OUT A WAY TO TRANSFER THE FLAC FILES TO OTHER DIRECTORY ONCE THEY ARE DONE BEING USED!!!

#homeDir = os.environ["HOME"] + "/"
# pathToFlacDir = ""

def main(flacDirName, featureDirName):
    print("Converting files from " + flacDirName + " to " + featureDirName)

    global pathToFlacDir
    pathToFlacDir = flacDirName + "/" #homeDir + flacDirName + "/"

    # list the files from flac directory
    fileList = os.listdir(pathToFlacDir)
    print(fileList)
    if 'desktop.ini' in fileList:
        fileList.remove('desktop.ini')
    
    print('new')
    print(fileList)
    for file in fileList:
        fList = [file]
        # read them into pandas
        df = pd.DataFrame(fList)

        # Rename first column as file
        df = df.rename(columns={0:'file'})

        # Check dataframe
        print(df.head())

        # Start timer to see how long it takes to extract features
        startTime = datetime.now()

        # Applying the function to the train data by accessing each row of the dataframe
        features_label = df.apply(extract_features, axis=1)

        # Code to see how long it took
        print(datetime.now() - startTime)

        # Checking how the output looks
        print(features_label)

        # Create output file path
        fileName = str(file)
        outFilePath = featureDirName + "/" + fileName[:-5] + '_features.pkl' #homeDir + featureDirName + "/" + fileName[:-5] + '_features.pkl'

        # The next code in markdown saves the numpy array (in case our kernel restarts or
        # anything happens, because it takes long to extract the features)
        pd.to_pickle(features_label, filepath_or_buffer=outFilePath)

        # Also pickle the dataframe, just in case
        # pd.to_pickle(df, filepath_or_buffer= homeDir + str(file) + '_df.pkl')

    return "1"



def extract_features(files):

    # Sets the name to be the path to where the file is in my computer
    # file_name = os.path.join(os.path.abspath('voice')+'\\'+str(files.file))
    file_name = pathToFlacDir + str(files.file)
    print("file_name: " + file_name)

    # Loads the audio file as a floating point time series and assigns the default sample rate
    # Sample rate is set to 22050 by default
    X, sample_rate = librosa.load(file_name, res_type='kaiser_fast')

    # Generate Mel-frequency cepstral coefficients (MFCCs) from a time series
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)

    # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
    stft = np.abs(librosa.stft(X))

    # Computes a chromagram from a waveform or power spectrogram.
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)

    # Computes a mel-scaled spectrogram.
    mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)

    # Computes spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

    # Computes the tonal centroid features (tonnetz)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),
                                              sr=sample_rate).T,axis=0)


    # We add also the classes of each file as a label at the end
    # label = files.label

    return mfccs, chroma, mel, contrast, tonnetz#, label (we don't do the gender label)

#main('Audio_Data_Spring_2023/bk_sc3_flac/', 'Audio_Data_Spring_2023/bk_sc3_features/')
