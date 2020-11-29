#-------------------------------------------
#----------------Main Function--------------
#-------------------------------------------
import numpy as np #arrays and math
import cv2 #opencv library
import datetime
import os
# import pyrebase
from ndviFunctions import NDVICalc, DVICalc
import pyrebase


#firebase storage 
config = {
  "apiKey": "AIzaSyB-LpbpCA68MLiIgzHcbGqgcMIcEtCyECY",
  "authDomain": "acreeye.firebaseapp.com",
  "databaseURL": "https://acreeye.firebaseio.com",
  "projectId": "acreeye",
  "storageBucket": "acreeye.appspot.com",
  "messagingSenderId": "1031473176901",
  "appId": "1:1031473176901:web:7dcc7cb46541ad39215e2c",
  "measurementId": "G-5DFT5MZQ1D"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
user = auth.sign_in_with_email_and_password("test@gmail.com", "adil1234")

storage = firebase.storage()
db = firebase.database()

path_on_cloud = 'screenshots/example3.jpg'
path_local = 'example.jpg'

imageUrl = storage.child(path_on_cloud).get_url(None)

# 28-11-2020
data = {"imageUrl": imageUrl}
db.child("data").child('28-11-2020').child('images').push(data)


cv2.namedWindow("preview NDVI")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
    height = vc.get(3) #get height
    width = vc.get(4) #get width
    #Text Related
    x = int(width/2)
    y = int(2*height/3) 
    text_color = (255,255,255) #color as (B,G,R)
    font = cv2.FONT_HERSHEY_PLAIN
    thickness = 2
    font_size = 2.0
else:
    rval = False

while rval:
    ndviImage = NDVICalc(frame)
    #dviImage = DVICalc(frame)

    cv2.putText(frame, "Raw Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)
    cv2.putText(ndviImage, "NDVI Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)
    #cv2.putText(dviImage, "DVI Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)

    #newFrame = np.concatenate((ndviImage,dviImage,frame),axis=1)
    newFrame = np.concatenate((ndviImage,frame),axis=1)
    cv2.imshow("preview NDVI", newFrame)

    rval, frame = vc.read()


    key = cv2.waitKey(1)&0xFF #get a key press
    if key == ord('q'): #q for quitting
        break
    elif key == ord('p'): #p for printscreen
        
        path = './screenshots'

        curtime = datetime.datetime.now()
        formattedTime = curtime.strftime("%Y%m%d-%H-%M-%S.jpg")
        print ('filename:%s'%formattedTime)
        cv2.imwrite(os.path.join(path,formattedTime),newFrame)
        print ("Screenshot taken!")

# When everything done, release the capture
vc.release()
cv2.destroyAllWindows()


    #uploading to the cloud 
# def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     #"""Uploads a file to the bucket."""
    
#     bucket_name = config.storageBucket
#     source_file_name = "example.jpg"
#     destination_blob_name = "storage-object-name"

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)

#     blob.upload_from_filename(source_file_name) 

#     print(
#         "File {} uploaded to {}.".format(
#             source_file_name, destination_blob_name
#         )
#     )