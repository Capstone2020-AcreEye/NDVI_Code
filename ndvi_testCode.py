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
import firebase_admin
from firebase_admin import credentials 
from firebase_admin import firestore

##########################################################################################
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
#uploading image to firebase database
#test = db.child("data").child('25-11-2020').child('Images').push(data)
cred = credentials.Certificate('./acreeye-firebase-adminsdk.json')
default_app = firebase_admin.initialize_app(cred)
db1 = firestore.client()

#response = getQuote()
#quote = response.body['quote']
#author = response.body['author']





#Upload the image taken from the camera to the cloud firebase 
def upload_image(storage_location):
    
    #uploading image to the firebase storage 
    print("Uploading Image to storage...")
    #path_on_cloud = 'screenshots/example4.jpg'
    path_on_cloud = 'screenshots/' + storage_location
    path_local = './screenshots/' + storage_location
    storage.child(path_on_cloud).put(path_local)

    #uploading image url from storage to database
    print("adding to database...")
    imageUrl = storage.child(path_on_cloud).get_url(None)
    doc_ref = db1.collection(u'data').document(u'NDVI')
    doc_ref.set({
    u'screenshot': (str(imageUrl))
    }, merge=True)


# 28-11-2020
#data = {"imageUrl": imageUrl}
#db.child("data").child('28-11-2020').child('images').push(data)
##########################################################################################

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
   
    #PRESS 'Q' to quit camera 
    if key == ord('q'): #q for quitting
        break

    #PRESS 'P' to printscreen and upload pic to cloud  
    elif key == ord('p'):  
        path = './screenshots'
        curtime = datetime.datetime.now()
        formattedTime = curtime.strftime("%Y%m%d-%H-%M-%S.jpg")
        print ('filename:%s'%formattedTime)
        cv2.imwrite(os.path.join(path,formattedTime),newFrame)
        print ("Screenshot taken!")
        upload_image(formattedTime)


        

# When everything done, release the capture
vc.release()
cv2.destroyAllWindows()





