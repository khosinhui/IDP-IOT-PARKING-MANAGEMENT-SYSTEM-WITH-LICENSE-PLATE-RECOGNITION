import io, os
from numpy import random
from google.cloud import vision
from Pillow_Utility import draw_borders,crop_image,Image
import pandas as pd
from datetime import datetime
from picamera import PiCamera
from time import sleep
from firebase import firebase


firebase = firebase.FirebaseApplication('https://lpr-g2.firebaseio.com/', None)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"
client = vision.ImageAnnotatorClient()
# camera = PiCamera()

def capture_and_recognize():
    with open('log.txt',mode ='a') as file:
        now = datetime. now()
        current_time = now. strftime("%H:%M:%S")
        file.write(current_time +" ")

     #using camera
    with PiCamera() as camera:
        camera.start_preview()
        sleep(2)
        camera.capture('capture.jpg')
        camera.stop_preview()
#    print("Input filename - ")
#    filename = input()
    with io.open('capture.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations

    pillow_image = Image.open('capture.jpg')
    df = pd.DataFrame(columns=['name', 'score'])

    cropImage = ""

    for obj in localized_object_annotations:
        if obj.name=="License plate" and obj.score>0.60:
            cropImage = crop_image(pillow_image, obj.bounding_poly, pillow_image.size)
        
    if cropImage == "":
#         print("Error to detect License plate!")
        with open('log.txt',mode ='a') as file:
            now = datetime. now()
            current_time = now. strftime("%H:%M:%S")
            file.write(" error " +current_time + "\n")
        return "No plate"
    else:

        cropImage.save('crop.jpg')

        #detect text after crop

        with io.open('crop.jpg', 'rb') as image_file:
            content = image_file.read()

        # construct an image instance
        image = vision.types.Image(content=content)

        # annotate Image Response
        response = client.text_detection(image=image)  # returns TextAnnotation
        df = pd.DataFrame(columns=['locale', 'description'])

        texts = response.text_annotations
        i=0
        for text in texts:
            df = df.append(
                dict(
                    locale=text.locale,
                    description=text.description
                ),
                ignore_index=True
            )


        plate = df['description'][0].replace('\n','').replace(' ','')
        print("\nPlate Detected: "+ plate)
        with open('log.txt',mode ='a') as file:
            now = datetime. now()
            current_time = now. strftime("%H:%M:%S")
            file.write(plate + " " +current_time + "\n")
        return plate


previous_plate = ""
while(1):
    
    #capture the picture and recognize
    plate = capture_and_recognize()
    
    if plate == "No plate":
        print("No plate detected")
        firebase.put('https://lpr-g2.firebaseio.com/',"Current_Plate","None")
        previous_plate = ""
        #show no plate detected - close barrier
    
    else:
        if plate == previous_plate:
            print("Wait")
            #show plate means waiting pass
        else:
            #check from database
            val = firebase.get('https://lpr-g2.firebaseio.com/', plate)    

            if str(val) == "None":
                print("No car plate data in the database")
                #show no plate in database - close barrier
                firebase.put('https://lpr-g2.firebaseio.com/',"Current_Plate",plate+" not in database")
                sleep(1000)
                firebase.put('https://lpr-g2.firebaseio.com/',"Current_Plate","None")
            
            else:
                if val <= 0:
                    print("Insufficient Balance")
                    previous_plate = plate
                    #show insufficient balance - close barrier
                    firebase.put('https://lpr-g2.firebaseio.com/',"Current_Plate",plate+" insufficient balance")
                               
                else:
                    print("Account balance before deduct: "+str(val))
                    firebase.put('https://lpr-g2.firebaseio.com/',plate,val-1)
                    print("Account balance before deduct: "+str(val-1))
                    #show plate means pass - open barrier
                    firebase.put('https://lpr-g2.firebaseio.com/',"Current_Plate","Welcome "+plate)
                    previous_plate = plate

                #display pass or not
            






