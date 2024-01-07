from typing import List
import cv2
import numpy as np

import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np

from utils.gesture_manager import HandGesture
from utils.hand_gesture_image_collector import HandGestureImageCollector

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models


class Model:
    MODEL_PATH = "model/data"

    def __init__(self, hand_gestures: List[HandGesture], img_size: int):
        self.hand_gestures = [x.name for x in hand_gestures]
        self.img_size = img_size
        self.model = None

    def load_from_file(self):
        self.model = tf.keras.models.load_model(self.MODEL_PATH)

    def save_to_file(self):
        self.model.save(self.MODEL_PATH)

    def train(self):
        # Define your data paths
        train_data_dir = r'model\data\images'
        validation_data_dir = r'model\data\images'
        test_data_dir = r'model\data\images'

        num_classes = len(self.hand_gestures)
    
        # Set up data generators with data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )

        validation_datagen = ImageDataGenerator(rescale=1./255)

        # Set up model
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(self.img_size, self.img_size, 3))
        base_model.trainable = False

        self.model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(64, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])

        # Compile the model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Set up data generators
        batch_size = 32
        train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=batch_size,
            class_mode='categorical'
        )

        validation_generator = validation_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=batch_size,
            class_mode='categorical'
        )

        # Train the model
        history = self.model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size + 1,
            epochs=10,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // + 1
        )

        # Evaluate the model
        test_generator = validation_datagen.flow_from_directory(
            test_data_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )

        test_loss, test_acc = self.model.evaluate(test_generator, steps=test_generator.samples // batch_size + 1)
        print(f'Test accuracy: {test_acc}')
        print(f'Test loss: {test_loss}')

        # self.model.save('model/data/model')

    def predict(self, img_white):
        # model = tf.keras.models.load_model('model/data/model')

        img_array = image.img_to_array(img_white)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Make a prediction
        predictions = self.model.predict(img_array, verbose=None)

        # Decode and print the prediction
        predicted_chance = np.max(predictions)
        predicted_class = np.argmax(predictions)
        predicted_gesture = self.hand_gestures[predicted_class]

        return predicted_gesture, predicted_chance
