import cv2
import os

    #  The main aim of this file is to generate the residue frames
    #  by image arithmetic on original and noised frames
    
videoFrames = []

    #  Loading all the frames in an array named videoFrames

with open("Frame Names.txt" , "r") as fp:
    videoFrames = [frame.strip() for frame in fp]
    
    #  We will create a folder with the name 'Residual Frames'
    #  It will store all the residue frames generated after filtering

currentDirectory = "./"
frameFolder = "Residual Frames"
newFolderPath = os.path.join(currentDirectory , frameFolder)
os.mkdir(newFolderPath)

print("\nExtracting Video Frame's Residue...... !!\n")

    #  Follwing code snippet will created noise residue frames
    #  The original video frames is subtracted from noise free version
    #  to obtain the resultant noise residual frame.

count = 0
for frame in videoFrames:
    originalFrame = './Generated Frames/ Frame ' + str(count) + '.jpg'
    denoisedFrame = './Denoised Frames/ Frame ' + str(count) + '.jpg'
    if (((1 + count) * 100) / len(videoFrames)) % 25 == 0:
        print((((1 + count) * 100) / len(videoFrames)) , str(chr(37)) + " residue extracted..")
    readImage1 = cv2.imread(originalFrame, 0)
    readImage2 = cv2.imread(denoisedFrame, 0)
    residue = cv2.subtract(readImage2 , readImage1)
    cv2.imwrite("./Residual Frames/ Frame %d.jpg" % count, residue)
    count += 1

print("\nVideo Residue Extracted Successfully !!\n")
