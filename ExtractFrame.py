import cv2
import os

    #  The main aim of this file is to segment down
    #  video in the frames for further classification

print()

    #  Asks the user to entered the name of the video
    #  This is the video user wants to detect the forgery of

videoString = input("Enter Name of The Video : ")
videoString1 = './Video Dataset/' + videoString + ".avi";
videoString2 = './Video Dataset/' + videoString + ".mp4";

    #  If the name of the video enetered by the user is available
    #  This software will read that video and start genearting the frames 
if(os.path.exists(str(videoString1))):
    videoString = videoString1
else:
    videoString = videoString2
    
if(os.path.exists(str(videoString1)) or os.path.exists(str(videoString2))):
    
      videoName = cv2.VideoCapture(str(videoString))
      frameExists , newFrame = videoName.read()
      
      #  We will create a folder with the name 'Generated Frames'
      #  It will store all the frames generated from the video
      
      currentDirectory = "./"
      frameFolder = "Generated Frames"
      newFolderPath = os.path.join(currentDirectory , frameFolder)
      os.mkdir(newFolderPath)
      
      #  Following code snippet start generating the frames
      #  Frames are saved in .jpg format
      
      frameNo = 0
      with open("Frame Names.txt" , "w+") as fp:
          while frameExists:
              frameName = "Frame " + str(frameNo) + ".jpg" + "\n"
              cv2.imwrite("./Generated Frames/ Frame %d.jpg" % frameNo, newFrame)
              fp.write(str(frameName))
              frameExists , newFrame = videoName.read()
              frameNo += 1
      
      print("\nVideo Segmentation Done Successfully !!\n")
   
   
   #  If the name of video entered is invalid, following message is printed
            
else:
  print("\nCould Not Find The Video In The Database !! Try Again\n")
  
  