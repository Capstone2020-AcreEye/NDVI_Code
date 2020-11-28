#-------------------------------------------
#----------------Main Function--------------
#-------------------------------------------
import numpy as np #arrays and math
import cv2 #opencv library
import datetime
import os
import pyrebase
from ndviFunctions import NDVICalc, DVICalc
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage


#firebase storage 
config = {
    "storageBucket": "acreeye.appspot.com"
}


# Use the application default credentials
cred = credentials.Certificate('./acreeye-key.json')
firebase_admin.initialize_app(cred, config)

bucket = storage.bucket()
#print(bucket)
fileName = "./screenshots/example.jpg"
blob = bucket.blob(fileName)
blob.upload_from_filename(fileName)

#db = firestore.client()



# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# path_on_cloud = "images/example.jpg"
# path_local = "/screenshots/example.jpg"
# storage.child(path_on_cloud).put(path_local)


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


