import numpy as np
import matplotlib.pyplot as plt
import collections
from PIL import Image
from scipy import signal


    #  The main aim of this file is to perform cross correlation on every
    #  pair of consecutive residue frames and on original ones also


videoFrames = []

    #  Loading all the frames in an array named videoFrames

with open("Frame Names.txt" , "r") as fp:
    videoFrames = [frame.strip() for frame in fp]

    
    #  Follwoing code sinppet performs the cross correlation of every original frame
    #  adjacent to each other. It stores the correlation value in an array.

print('\nCorrelation In Original Frames\n')

correlateValueOriginal = []

for residue in range(1 , len(videoFrames)):
    i1 = "./Generated Frames/ Frame " + str(residue - 1) + ".jpg"
    i2 = "./Generated Frames/ Frame " + str(residue) + ".jpg"
    img1 = Image.open(i1)
    img2 = Image.open(i2)
    cor = signal.correlate(img1, img2 , 'valid')
    temp = float(cor)
    correlateValueOriginal.append(round(temp , 3))
    print(correlateValueOriginal[-1])
    
    #  Follwoing code sinppet performs the cross correlation of every residual frame
    #  adjacent to each other . It stores the correlation value in an array.

print('\nCorrelation In Residual Frames\n')

correlateValueResidual = []

for residue in range(1 , len(videoFrames)):
    i1 = "./Residual Frames/ Frame " + str(residue - 1) + ".jpg"
    i2 = "./Residual Frames/ Frame " + str(residue) + ".jpg"
    img1 = Image.open(i1)
    img2 = Image.open(i2)
    cor = signal.correlate(img1, img2 , 'valid')
    temp = float(cor)
    correlateValueResidual.append(round(temp , 3))
    print(correlateValueResidual[-1])
    
    
    #  Now hashing the same values around the process in residual frames

X1 = []
Y1 = []

X2 = []
Y2 = []
    
for i in range(1 , len(videoFrames)):
    X2.append(i)
    X1.append(i)
    
for val in correlateValueOriginal:
    Y1.append(val)
    
for val in correlateValueResidual:
    Y2.append(val)

    #  Now plotting the graphs of the original correlational results

plot1 = plt.figure(1)
plt.plot(X1 , Y1 , '-ok' , color = "red" , linewidth = 0.6)
plt.xlabel('Frame No')
plt.ylabel('Correlational Value')
plt.title('Correlational Original Frame Plotting')

    #  Now plotting the graphs of the residual correlational results

plot2 = plt.figure(2)
plt.plot(X2 , Y2 , '-ok' , color = "blue" , linewidth = 0.6)
plt.xlabel('Frame No')
plt.ylabel('Correlational Value')
plt.title('Correlational Residual Frame Plotting')

plt.show()

    #  Calculating the statistical components: Mean and the Variance
    #  First Calculating the summation of correlation values found above
    
N = len(correlateValueResidual)
correlateMean = 0

for val in correlateValueResidual:
    correlateMean += val

correlateMean /= N

    #  Now Calculating the variance of correlation values found above
    
correlateVariance = 0

for val in correlateValueResidual:
    correlateVariance += ((correlateMean - val) * (correlateMean - val)) / N


    #  Printing the values

print("\nCross Correalated Mean is : " , correlateMean)
print("\nCross Correalated Variance is : " , correlateVariance)


    #  Class Mask defines a binary array and checks
    #  whether a particular frame is forged or not
    #  1 represents forgery and 0 represents purity
    
classMask = []

for val in correlateValueResidual:
    if(abs(val - correlateMean) * abs(val - correlateMean) <= correlateVariance):
        classMask.append(0)
    else:
        classMask.append(1)
        

    #  Follwoing two arrays will store the original frames
    #  and those frames also, which may be forged

originalFrames = []
forgedFrames = []
  
for frameNo in range(0 , len(classMask)):
    if classMask[frameNo] == 1:
        forgedFrames.append(frameNo)
    else:
        originalFrames.append(frameNo)


    #  DECISION TIME
    #  Follwoing code snippet predicts the forgery percentage (if any)
        
if len(forgedFrames) > 1:
    print('\nVideo may be forged !!')
    forgeryChances = (len(forgedFrames) * 100) / len(videoFrames)
    print("\nAmount of Video Forged = " , round(forgeryChances , 3) , end = " ")
    print(str(chr(37)))
    print()
    for frameNo in forgedFrames:
        print("Frame No" , frameNo , "may be forged.")
        
else:
    print('\nVideo Is Not Forged\n')