import os

import cv2
#importing time to specify how long the cam shud be used
import time
from email_sending import send_email
import os
import glob
#we are importing threading coz in here we runnin 2 process at the same time
#(displaying cam and sending mail) causes cam to freeze threadin solves this
from threading import Thread


#opens and uses cam
# 0 here means your first cam incase you have 2 so 0 is integrated cam
#setups cam
video = cv2.VideoCapture(0)

# time.sleep is for how long it shud be open
# it pauses the execution of the current thread for 1 second
# helps avoid black image  incase it is too fast
time.sleep(1)

#we use this logic to create the first img frm which we will compare diff
#and tell if obj comes on cam
first_frame = None


status =0
status_list = []
count=1
#this func delets all images after task done
def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

#---------- REFER FILE NAMED "CODE_LOGIC" TO UNDERSTAND   ------------*

#executes read func multiple times
#every iteration will be a frame

while True:
    status =0
    #check returns true if opening and takin pic worked
    #frame is the image captured it will be in numpy matrix
    check , frame = video.read()


    # converting images frm video processing to greyscale
    # to reduce load coz colour means more data
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # makes calculations more efficent
    # gaussian blur
    # the 2nd arg here is amt of blur
    # the zero is standard deviation
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)





    #this logic ensures first frame of video is captured
    if first_frame is None:
        first_frame = gray_frame_gau


    #finding diff between first frame and rest
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # for white pixels having value 30 or higher we make them white which is 255 (these pixels are the obj)
    # cv2.thresh.... -> creates a binary image by setting pixels above a set threshold value to a maximum
    # value (usually 255/white) and all other pixels below the threshold to 0 (black)
    # this output will be list and we want to extract 2nd item so we add 1 t end
    # play witht the 30 value make sure obj is white and bg is black
    thresh_frame = cv2.threshold(delta_frame, 68, 255, cv2.THRESH_BINARY)[1]

    # removes noise, higher iteration no. - more noise removal
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    #shows the obj when it appears in cam
    cv2.imshow('my video ', dil_frame)



    #adding outline for the obj
    # Finds contours (continuous boundaries) in the dilated image.
    # cv2.RETR_TREE retrieves all contours and their hierarchy.
    # cv2.CHAIN_APPROX_SIMPLE compresses contour points to save memory.
    # 'contours' stores detected shapes, 'check' stores their hierarchy info.
    contours, check = cv2.findContours(dil_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        #extracting the dimensions of the box created round the obj
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
        if rectangle.any():
            status = 1
            #taking photos everytime obj appears
            cv2.imwrite(f"images/{count}.png", frame)
            count+=1
            #fetching all images from folder * does the job
            all_images  = glob.glob(f"images/*.png")
            #finding middle image from list
            index = int(len(all_images)/2)
            #middle image
            object_image = all_images[index]
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        print("JHJJJJJJJJJJ")
        #instead of calling func like this"send_email(object_image)" we use this line
        #comma is there in args becoz it must be a tuple
        email_thread = Thread(target=send_email, args=(object_image,))
        email_thread.daemon = True
        #doing this instead of normal clean_folder call
        clean_thread = Thread(target= clean_folder)
        email_thread.daemon = True

        #this calls the functions aboves ones are declaration
        email_thread.start()
        #can't call clean_folder here coz it will clear while mail is tryin to be sent.



    print(status_list)
    cv2.imshow('video', frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break


video.release()
clean_thread.start()