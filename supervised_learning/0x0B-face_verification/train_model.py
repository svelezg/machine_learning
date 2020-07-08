#!/usr/bin/env python3
"""contains the TrainModel class"""

from triplet_loss import TripletLoss
import tensorflow as tf


class TrainModel:
    """
    TrainModel class
    """

    def __init__(self, model_path, alpha):
        """
        constructor
        :param model_path: path to the base face verification embedding model
            loads the model using with tf.keras.utils.CustomObjectScope({'tf': tf}):
            saves this model as the public instance method base_model
        :param alpha: alpha to use for the triplet loss calculation
        """
        with tf.keras.utils.CustomObjectScope({'tf': tf}):
            self.base_model = tf.keras.models.load_model(model_path)

        A = tf.keras.Input(shape=(96, 96, 3))
        P = tf.keras.Input(shape=(96, 96, 3))
        N = tf.keras.Input(shape=(96, 96, 3))

        network0 = self.base_model(A)
        network1 = self.base_model(P)
        network2 = self.base_model(N)

        tl = TripletLoss(alpha)

        # combine the output of the three branches
        combined = [network0, network1, network2]
        output = tl(combined)

        my_model = tf.keras.models.Model([A, P, N], output)

        my_model.compile(optimizer='adam')

        self.training_model = my_model

    def train(self, triplets, epochs=5, batch_size=32, validation_split=0.3, verbose=True):
        """

        :param triplets: list containing the inputs to self.training_model
        :param epochs: number of epochs to train for
        :param batch_size: batch size for training
        :param validation_split: validation split for training
        :param verbose: boolean that sets the verbosity mode
        :return: History output from the training
        """
        # training
        history = self.training_model.fit(triplets,
                                          batch_size=batch_size,
                                          epochs=epochs,
                                          verbose=verbose,
                                          validation_split=validation_split)

        return history

    def save(self, save_path):
        """
        :param save_path: path to save the model
        :return: saved model
        """
        self.save(save_path)

    @staticmethod
    def f1_score(y_true, y_pred):
        """

        :param y_true:
        :param y_pred:
        :return: the f1 score
        """
        return tf.keras.metrics.F1Score(y_true, y_pred)

    @staticmethod
    def accuracy(y_true, y_pred):
        """

        :param y_true:
        :param y_pred:
        :return: the accuracy
        """
        return tf.keras.metrics.accuracy(y_true, y_pred)

    def best_tau(self, images, identities, thresholds):
        """

        :param images:
        :param identities:
        :param thresholds:
        :return: (tau, f1, acc)
        """
