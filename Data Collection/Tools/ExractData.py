# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 22:11:56 2023

@author: Winfred

What is it?
-building a map to organize the programs needed to extract data from phone, cut the data up, transform cut up data into flac,transform flac data into features


Goal?
Create a script to run all of the programs 

What do I have?
1.)Audio_cutter.py
2.)Ffpmpeg_convert_wav_to_flac
                 -only if the file coming in is a file other than flac 
3.)Feature_extract


"""

#Audio Cutter imports
from pydub import AudioSegment
from pydub.utils import make_chunks
import os

# wav to flac
import ffmpeg


import feature_extract as fe


def cut_audio(input_dir,output_format="3pg", chunk_length_ms=30000):
        
    filenumber =0
    files = os.listdir(input_dir)
   
    print(f"Processing files: {files}")
    for file in files:
       
        file_path = os.path.join(input_dir, file)
       
        try:
            audio = AudioSegment.from_file(file_path , output_format) 
            #chunk_length_ms = 30000 # pydub cal in millisec
            chunks = make_chunks(audio, chunk_length_ms) #Make chunks of 30 sec
            
            #Export all of the individual chunks as wav files
            for chunk in (chunks):
               chunk_name = "win_bk_sc3_{0}.wav".format(filenumber)# increment file number
               chunk_path = os.path.join(input_dir, chunk_name)
               chunk.export(chunk_path, format="wav") 
               print (f"exporting {chunk_name}")
               filenumber+=1
       
        except FileNotFoundError:
            print(f"Error: The file {file} was not found in {input_dir}.")
        
        except Exception as e:
            print(f"Failed to process {file}: {str(e)}")
            



def wav_to_flac(source_dir, tgt_dir ,files_to_ignore):
    #same dir as Audio cutter so I can grab the data
    os.chdir(source_dir)##'Audio_Data_Spring_2023/bk sc3'
    
    files = os.listdir('.')## Get files in directory 
    #files = files
    #path_files = 'C:/Users/Winfred/OneDrive/Documents/Socio App Data/ExtractDataFlac'             #os.getcwd() # should fix problem: place audio data tranfrom into flac in flac dir
  #  print(f"files in directory {files}")
    
    
    for filename in files:
        
        if filename in files_to_ignore:
            continue
        else:
            stream = ffmpeg.input(filename)
            audio = stream.audio
            outputfilename= filename[:-4] + ".flac"
            stream =  ffmpeg.output(audio, tgt_dir+'/'+ outputfilename,
                                    **{'ar': '48000','acodec':'flac', 'sample_fmt':'s16'})
            
            ffmpeg.run(stream)
    
def main():
    flacDirName= "ExtractDataFlac"
    featureDirName="ExtractDataFeatures"
    current_directory = os.getcwd()
    # Prompt showing the current directory first
    print( f"Current directory is '{current_directory}'. ")
   # folder_name = input(prompt)

    # Construct the full path to the folder
  #  folder_path = os.path.join(current_directory, folder_name)
    input_dir = input("Enter the input directory path from current directory: ")
    
    #flac_dir =input("Enter the flac directory path from current directory: ")
    #feature_dir = input("Enter the feature directory path from current directory: ")
     
    #rember the code should IGNORE with the file it already saw initiall before audio cuter runs
    #'C:/Users/Winfred/OneDrive/Documents/Socio App Data/ExtractDataAudio1'
    files_to_ignore = os.listdir(input_dir)
    
    #object1 = AudioCutter('C:/Users/Winfred/OneDrive/Documents/Socio App Data/ExtractDataAudio1') #given more than one audio file as data take the entire dir#    #also changes dir to ExtractDataAudio
    cut_up_audio = cut_audio(input_dir)
    #
    #Convert to flac
    # get data from ExtractDataAudio
    # wav does not need to retrun antyhing becasue fe will take dir names and do the rest
    wav_to_flac(input_dir,cut_up_audio  ,files_to_ignore )
    
   
    
    flacDirName= 'ExtractDataFlac'
    featureDirName='ExtractDataFeatures'
    
    fe.main(flacDirName, featureDirName)
    

if __name__ == "__main__":
    main()
    






























