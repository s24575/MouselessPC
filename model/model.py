from typing import List, Tuple

import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np

from utils.consts import Consts
from utils.utils import HandGesture


class Model:
    MODEL_SAVE_PATH = 'model/keypoint_classifier/keypoint_classifier.hdf5'
    MODEL_TFLITE_SAVE_PATH = 'model/keypoint_classifier/keypoint_classifier.tflite'

    def __init__(self, hand_gestures: List[HandGesture],
                 dataset_path: str = Consts.LANDMARKS_PATH,
                 num_threads=1):
        self.hand_gestures = hand_gestures
        self.img_size = Consts.HAND_IMG_SIZE
        self.dataset_path = dataset_path
        self.model = None
        self.RANDOM_SEED = 42
        self.batch_size = 128
        self.num_threads = num_threads

    def init(self):
        self.interpreter = tf.lite.Interpreter(model_path=self.MODEL_TFLITE_SAVE_PATH,
                                               num_threads=self.num_threads)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def train(self):
        X_dataset = np.loadtxt(self.dataset_path, delimiter=',', dtype='float32', usecols=list(range(1, (21 * 2) + 1)))
        y_dataset = np.loadtxt(self.dataset_path, delimiter=',', dtype='int32', usecols=0)

        X_train, X_test, y_train, y_test = train_test_split(X_dataset, y_dataset, train_size=0.75,
                                                            random_state=self.RANDOM_SEED)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Input((21 * 2,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(20, activation='relu'),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(len(self.hand_gestures), activation='softmax')
        ])

        # Model checkpoint callback
        cp_callback = tf.keras.callbacks.ModelCheckpoint(self.MODEL_SAVE_PATH, verbose=1, save_weights_only=False)
        # Callback for early stopping
        es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)

        # Model compilation
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        model.fit(
            X_train,
            y_train,
            epochs=1000,
            batch_size=self.batch_size,
            validation_data=(X_test, y_test),
            callbacks=[cp_callback, es_callback]
        )

        # Model evaluation
        val_loss, val_acc = model.evaluate(X_test, y_test, batch_size=self.batch_size)
        print(f"Validation loss: {val_acc}, Validation accuracy: {val_acc}")

        # Save as a model dedicated to inference
        model.save(self.MODEL_SAVE_PATH, include_optimizer=False)

        # Transform model (quantization)
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_quantized_model = converter.convert()

        open(self.MODEL_TFLITE_SAVE_PATH, 'wb').write(tflite_quantized_model)

    def predict(self, landmark_list) -> Tuple[HandGesture, float]:
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))
        result_chance = np.max(np.squeeze(result))

        return self.hand_gestures[result_index], result_chance
