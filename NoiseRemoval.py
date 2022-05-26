import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

    #  The main aim of this file is to remove the noise from the video Frames
    #  The noise free version of frames are stored in a folder 'Denoised Frames'
  
print("\nCreating Noise Free Frames. Please Wait.....\n")

    #  Loading all the frames in an array named videoFrames
    
videoFrames = []

with open("Frame Names.txt" , "r") as fp:
    videoFrames = [frame.strip() for frame in fp]

    #  We will create a folder with the name 'Denoised Frames'
    #  It will store all the denoised frames generated after filtering

currentDirectory = "./"
frameFolder = "Denoised Frames"
newFolderPath = os.path.join(currentDirectory , frameFolder)
os.mkdir(newFolderPath)

    #  Now Generating Noise Free Residue for each frame
    #  These residue are stored in a folder 'Denoised Frames'

count = 0

for frames in videoFrames:
    print("Generated Deniosed Frame No: %d" %count)
    currentFrame = './Generated Frames/ ' + str(frames)
    noisedFrame = cv2.imread(currentFrame)
    deniosedFrame = cv2.fastNlMeansDenoisingColored(noisedFrame, None, 10, 10, 7, 15)
    cv2.imwrite("./Denoised Frames/ Frame %d.jpg" % count, deniosedFrame)
    count += 1
    
print("\nVideo Noise Removal Succesfully Done !!\n")
  