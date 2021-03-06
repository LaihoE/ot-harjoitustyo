import math
import os
import joblib
import pandas as pd
import numpy as np
import onnxruntime
from db import Database


class Model:
    def __init__(self, model_path):
        """
        Initializes Machine-learning model

        :param model_path:
        """
        self.ort_session = onnxruntime.InferenceSession(model_path)

    def _load_csv_data(self, file_path):
        """
        Loads csv file with pandas.

        :param file_path:
        :return: df
        """
        return pd.read_csv(file_path, header=None)

    def _transform_data(self, data):
        """
        Takes in raw csv-data and splits it into data that is used in the prediction
        and into data that is only used in the end. The function also transforms the
        prediction data.

        :param data:
        :return: ml_data, other data: ml data is a numpy array and other is dict
        """
        # Data comes in rows of 1x1728 (rolled out to a row) so we unroll the data
        data = data.to_numpy().reshape(-1, 192, 9)
        # All the data isn't used for the prediction but will be needed later so we slice it here.
        # Each value in the dictionary is a list
        # Each list in the dictionary is the same length
        other_data = {"file_names": data[:, 0, 0],
                      "player_names": data[:, 0, 1],
                      "player_ids": data[:, 0, 2],
                      "ticks": data[:, 0, 3]
                      }
        # Data that is input into the model.
        ml_data = np.float32(data[:, :, 4:])

        # We scale the data for better model performance (not important to understand),
        # if interested see more:
        # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
        dirname = os.path.dirname(__file__)
        path_to_scaler = os.path.join(dirname, 'utils', 'scaler.gz')
        scaler = joblib.load(path_to_scaler)

        # Reshape data into 2d and back to 3d after scaling.
        # Pylint seems to complain about this one (false-positive?)
        # Disabling pylint lines wasn't liked so i left it in
        ml_data = ml_data.reshape((-1, 5))
        ml_data = scaler.transform(ml_data)
        ml_data = ml_data.reshape((-1, 192, 5))

        return ml_data, other_data

    def _predict(self, file_path, batch_size):
        """
        Does the actual prediction. Returns predictions combined with "other" data. Throws away
        data used in prediction after it's done.
        Predictions are done in batches to fit into RAM/VRAM


        :param file_path: Path to csv file
        :param batch_size: How many samples per prediction. Trade-off between memory and speed
        :return: other_data: A dictionary containing predictions and data related to the predictions
        """

        print("Reading data...")
        csv_data = self._load_csv_data(file_path)
        ml_data, other_data = self._transform_data(csv_data)

        # The predictions list will be the same length as the rest of the data
        # allowing easy indexing of them all
        total_batches = math.ceil(ml_data.shape[0] / batch_size)
        predictions = []
        print("Starting predictions...")
        for batch in range(total_batches):
            # Slice current batch
            data_this_batch = ml_data[batch_size *
                                      batch: batch_size * batch + batch_size, :, :]
            # Prep the data for input into ml model
            ort_inputs = {self.ort_session.get_inputs()
                [0].name: data_this_batch}
            # Does the actual prediction
            ort_outs = np.array(self.ort_session.run(None, ort_inputs))
            # index the cheating conf
            cheating_confidence = list(ort_outs[0][:, 1])
            # Add batch to predictions list
            predictions.extend(cheating_confidence)
        predictions = np.array(predictions)
        print("Predictions done")
        # Add predictions to other data
        # Now we dont need the ml_data anymore
        other_data["predictions"] = predictions
        return other_data

    def predict_to_terminal(self, file_name, threshold=0.97, batch_size=1000):
        """
        Predicts and outputs the predictions to terminal.

        :param file_name:
        :param threshold:
        :param batch_size: How many samples per prediction. Trade-off between memory and speed
        :return: None
        """

        data_dict = self._predict(file_name, batch_size)
        # Each key in data_dict is a feature for example who was the shooter or how likely the
        # player was to cheat during that shot. Each value in the dict is a list with the length
        # equal to the total amount of shots in the game

        # Print a header
        print("Prediction\t", "Player_name\t",
              "player_id\t", "tick\t", "file_name\t")

        for shot in range(len(data_dict["predictions"])):
            # If the shot was highly likely to be cheating
            if data_dict["predictions"][shot] > threshold:
                print(data_dict["predictions"][shot], "\t",
                      data_dict["player_names"][shot], "\t",
                      data_dict["player_ids"][shot], "\t",
                      data_dict["ticks"][shot], "\t",
                      data_dict["file_names"][shot])

    def predict_to_sql(self, file_name, batch_size=1000):
        """
        Takes in a file name and creates the predictions and inserts them into SQL.

        :param file_name: a csv file path
        :param batch_size: How many samples per prediction. Trade-off between memory and speed
        :return: success: True if everything works ok
        """
        data_dict = self._predict(file_name, batch_size)

        dirname = os.path.dirname(__file__)
        path_to_db = os.path.join(dirname, 'database', 'database.db')
        database = Database(path_to_db)
        database.insert_prediction(data_dict, 'mytable')
        return True
