import os
import cv2
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

    #  The main aim of this file is to perform Optical Flow Algorithm for
    #  every two consecutive frames and check for forgery present (if any)
  
print("\nPerforming Optical Flow on Video Frames. Please Wait......\n")

print('Reading Video....\n')

    #  Loading all the frames in an array named videoFrames
    
videoFrames = []

with open("Frame Names.txt" , "r") as fp:
    videoFrames = [frame.strip() for frame in fp]

    #  Defining some useful lists

frameList = []              #  Stores frame no
opticalFlowValues=[]        #  Stores optical Flow value for every frame
variationFactor = []        #  Stores frame varaition factor
anamolyFactor = []          #  Stores anamoly score
forgedFrames = []          #  Stores namea of frames which may be forged
foundFirst = False


    #   Now performing the optical flow by reading pair of two consecutive frames
    #   firstFrame points to Frame1 and secondFrame points to Frame2 used in optical flow

for frames in videoFrames:
    s = 0
    currentFrame = './Generated Frames/ ' + str(frames)
    if foundFirst == False:
        firstFrame = cv2.imread(currentFrame)
        foundFirst = True
        a = firstFrame.size
        s=np.arange(a)
        cvtFrame1 = cv2.cvtColor(firstFrame,cv2.COLOR_BGR2GRAY)
        continue
    
    #  Reading frames and converting RGB to grayscale
    
    secondFrame = cv2.imread(currentFrame)
    cvtFrame2 = cv2.cvtColor(secondFrame,cv2.COLOR_BGR2GRAY)
    
    
    #  Performing optical flow algorithm on every consecutive frame pair
    
    currentOpticalFlow = cv2.calcOpticalFlowFarneback(cvtFrame1 , cvtFrame2 , None , 0.5 , 3 , 15 , 3 , 5 , 1.2 , 0)
    mag, ang = cv2.cartToPolar(currentOpticalFlow[...,0] , currentOpticalFlow[...,1])
    
    opticalFlowHere = np.resize(mag,(1,a))
    
    for i in opticalFlowHere[0]:
        s=s+i
    print(s)
    
    #  Storing the value of optical flows in an array
    
    opticalFlowValues.append(s)
    
    #  Make firstFrame pointing to secondFrame for next pass
    
    firstFrame = secondFrame


    #  Storing the frame no in an array

for frameID in range(0 , len(videoFrames) - 1):
    frameList.append(frameID)
    
    #  Storing the varaiation factor value in an array

variationFactor.append(1)
sumofVariations = 0

for current in range(1 , len(videoFrames) - 2):
    tempSum = opticalFlowValues[current - 1] + opticalFlowValues[current + 1]
    meanValueHere = (2 * opticalFlowValues[current]) / tempSum
    variationFactor.append(meanValueHere)
    
variationFactor.append(1)

    #  Calculating mean of variation factor values

for current in variationFactor:
    sumofVariations += current
    
meanValue = (1.0 * sumofVariations) / len(variationFactor)

    #  Calculating variance of variation factor values 

variance = 0
for current in variationFactor:
    tempVariance = current - meanValue
    variance += tempVariance * tempVariance

variance = (1.0 * variance) / len(variationFactor)

    #  Calculating standarad deviation from variance

standardDeviation = math.sqrt(variance)

    #  calculating the ambiguity score value for each frame

for current in variationFactor:
    tempVar = (1.0 * abs(current - meanValue))
    tempVar = tempVar / standardDeviation
    anamolyFactor.append(tempVar)
    
anamolyMean = 0

for value in anamolyFactor:
    anamolyMean += value
    
anamolyMean /= len(anamolyFactor)

    #  Identifying all the forged frames, which have value greater than threshold
    
thresholdValue = anamolyMean

for current in range(0 , len(anamolyFactor)):
    if(anamolyFactor[current] > thresholdValue):
        forgedFrames.append("Frame " + str(current))

 
    #  Now plotting the graphs of the Frame vs Ambiguity Score

plot1 = plt.figure(1)
plt.title('Frame vs Ambiguity Score Visulatizaton')
plt.xlabel('Frame Number')
plt.ylabel('Magnitude of Ambiguity')
plt.plot(frameList , anamolyFactor , color = "red")

    #  Now plotting the graphs of the Frame vs Variation
    
plot2 = plt.figure(2)
plt.title('Frame vs Variation Visulatizaton')
plt.xlabel('Frame Number')
plt.ylabel('Variation Factor')
plt.plot(frameList , variationFactor , color = "blue")

plt.show()


    #  DECISION TIME
    #  Follwoing code snippet predicts the forgery percentage (if any)
        
if len(forgedFrames) > 1:
    print('\nVideo may be forged !!')
    forgeryChances = (len(forgedFrames) * 100) / len(videoFrames)
    print("\nAmount of Video Forged = " , round(forgeryChances , 3) , end = " ")
    print(str(chr(37)))
    print()
    for frameNo in forgedFrames:
        print(frameNo , "may be forged.")
        
else:
    print('\nVideo Is Not Forged\n')

cv2.destroyAllWindows()

