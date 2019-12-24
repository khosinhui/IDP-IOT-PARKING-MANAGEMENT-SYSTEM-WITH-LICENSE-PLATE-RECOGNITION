import io, os
from numpy import random
from google.cloud import vision
from Pillow_Utility import draw_borders, Image
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"
client = vision.ImageAnnotatorClient()

file_name = 'malaysia_car_3.jpg'
image_path = os.path.join('/home/pi/venv', file_name)

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.object_localization(image=image)
localized_object_annotations = response.localized_object_annotations

pillow_image = Image.open(image_path)
df = pd.DataFrame(columns=['name', 'score'])
for obj in localized_object_annotations:
    if obj.name=="License plate":
        df = df.append(
            dict(
                name=obj.name,
                score=obj.score
            ),
            ignore_index=True)
        
        r, g, b = random.randint(150, 255), random.randint(
            150, 255), random.randint(150, 255)

        draw_borders(pillow_image, obj.bounding_poly, (r, g, b),
                     pillow_image.size, obj.name, obj.score)

print(df)
pillow_image.show()