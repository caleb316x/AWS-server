import os
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import requests

class AWS:
    def __init__(self):
        print("init waste_classify")

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        self.model = load_model("keras_Model.h5", compile=False)

        # Load the labels
        self.class_names = open("labels.txt", "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    def check_image_dir():
        if os.path.isfile("uploads/esp32-cam.jpg"):
            print("File exists!")
        else:
            print("File does not exist.")

    def classify_image(self,path_image):

        # Replace this with the path to your image
        # imgdata = requests.get("https://hbw.ph/wp-content/uploads/2017/10/hbw-scissors-SP19006B-300x300.jpg", stream=True).raw
        imgdata = requests.get("http://192.168.201.160/image", stream=True).raw
        image = Image.open(imgdata).convert("RGB")
        # image = Image.open(path_image).convert("RGB")

        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        self.data[0] = normalized_image_array

        # Predicts the model
        prediction = self.model.predict(self.data)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)

        if (confidence_score < 0.75):
            print("Class: Waste")
            return "Waste"

        return class_name[2:]