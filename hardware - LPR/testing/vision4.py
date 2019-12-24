import io, os
from numpy import random
from google.cloud import vision
from Pillow_Utility import draw_borders,crop_image, Image,draw_borders_plate
import pandas as pd
from datetime import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"
client = vision.ImageAnnotatorClient()



with open('abc.txt',mode ='a') as file:
    now = datetime. now()
    current_time = now. strftime("%H:%M:%S")
    file.write(current_time +" ")

file_name = 'malaysia_car_3.jpg'
image_path = os.path.join('/home/pi/venv/images', file_name)

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.object_localization(image=image)
localized_object_annotations = response.localized_object_annotations

pillow_image = Image.open(image_path)
df = pd.DataFrame(columns=['name', 'score'])

cropImage = ""

for obj in localized_object_annotations:
    if obj.name=="License plate" and obj.score>0.80:
        cropImage = crop_image(pillow_image, obj.bounding_poly, pillow_image.size)
        r, g, b = random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)
    
if cropImage == "":
    print("Error to detect License plate!")
else:
    crop_image_path = os.path.join('/home/pi/venv/crop', file_name)

    cropImage.save(crop_image_path)

    #detect text after crop

    with io.open(crop_image_path, 'rb') as image_file:
        content = image_file.read()

    # construct an image instance
    image = vision.types.Image(content=content)

    # annotate Image Response
    response = client.text_detection(image=image)  # returns TextAnnotation
    df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )

    #print(df)
    plate = df['description'][0].replace('\n','').replace(' ','')
    draw_borders_plate(pillow_image, obj.bounding_poly, (r, g, b),pillow_image.size, plate)
    pillow_image.show()
    print("\nPlate Detected: "+ plate)
    with open('abc.txt',mode ='a') as file:
        now = datetime. now()
        current_time = now. strftime("%H:%M:%S")
        file.write(plate + " " +current_time + "\n")



