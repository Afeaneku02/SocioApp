# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 07:33:01 2022

@author: Winfred
"""

from pydub import AudioSegment
from pydub.utils import make_chunks
import os

def cut_audio(input_dir, output_dir, chunk_length_ms=30000):
    
    if not os.path.exists(output_dir): ## if a folder is not already there then create one
        os.makedirs(output_dir)
        
    filenumber =0
    files = os.listdir(input_dir)###########
   
    print(f"Processing files: {files}")
    for file in files:
       
        file_path = os.path.join(input_dir, file)
       
        try:
            audio = AudioSegment.from_file(file_path , "3gp") 
            #chunk_length_ms = 30000 # pydub cal in millisec
            chunks = make_chunks(audio, chunk_length_ms) #Make chunks of 30 sec
            
            #Export all of the individual chunks as wav files
            for chunk in (chunks):
                
               chunk_name = "win_bk_sc3_{0}.wav".format(filenumber)# increment file number
               print (f"exporting {chunk_name}")
               chunk_path = os.path.join(output_dir, chunk_name)
               chunk.export(chunk_path, format="wav")
               filenumber+=1
       
        except FileNotFoundError:
            print(f"Error: The file {file} was not found in {input_dir}.")
        
        except Exception as e:
            print(f"Failed to process {file}: {str(e)}")

def main():      
    input_dir = input("Enter the input directory path: ")
    output_dir =input("Enter the output directory path: ")  
    cut_audio(input_dir, output_dir)    
    

if __name__ == "__main__":
    main()