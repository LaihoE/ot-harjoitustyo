import csv
import sklearn
import joblib
import pandas as pd
import math
import numpy as np
import onnxruntime
import os


class Model:

    def __init__(self):
        # init ml_model
        self.ort_session = onnxruntime.InferenceSession('models/ml_model.onnx')

    def _load_csv_data(self, file_path):
        """
        Reads csv
        """
        return pd.read_csv(file_path, header=None)

    def _transform_data(self, data):
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
        ml_data = np.float32(data[:, :, 4:])  # Data that is input into the model.

        # We scale the data for better model performance (not important to understand),
        # if interested see more: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html 
        scaler = joblib.load('utils/scaler.gz')
        ml_data = scaler.transform(ml_data.reshape(-1, 5)).reshape(-1, 192, 5)
        
        return ml_data, other_data

    def _predict(self, file_path ,batch_size):
        csv_data = self._load_csv_data(file_path)
        ml_data, other_data = self._transform_data(csv_data)
        
        total_batches = math.ceil(ml_data.shape[0] / batch_size)
        predictions = []
        # We need to do the predictions in batches to not run out of ram/vram
        # The predictions list will be the same length as the rest of the data
        # allowing easy indexing of them all
        for batch in range(total_batches):
            # Slice current batch
            data_this_batch = ml_data[batch_size * batch: batch_size * batch + batch_size, :, :]
            # Prep the data for input into ml model
            ort_inputs = {self.ort_session.get_inputs()[0].name: data_this_batch}
            # Does the actual prediction
            ort_outs = np.array(self.ort_session.run(None, ort_inputs))
            # index the cheating conf
            cheating_confidence = list(ort_outs[0][:, 1])
            # Add batch to predictions list
            predictions.extend(cheating_confidence)
        predictions = np.array(predictions)

        # Add predictions to other data
        # Now we dont need the ml_data anymore
        other_data["predictions"] = predictions
        return other_data

    def predict_to_terminal(self, file_name, threshold=0.97, batch_size=1000):
        data_dict = self._predict(file_name, batch_size)
        # Each key in data_dict is a feature for example who was the shooter or how likely the player was to
        # cheat during that shot. Each value in the dict is a list with the length equal to
        # the total amount of shots in the game

        # Print a header
        print("Prediction\t", "Player_name\t", "player_id\t", "tick\t", "file_name\t")

        for shot in range(len(data_dict["predictions"])):
            # If the shot was highly likely to be cheating
            if data_dict["predictions"][shot] > threshold:
                # Slice data for print
                print(data_dict["predictions"][shot],"\t",
                      data_dict["player_names"][shot],"\t",
                      data_dict["player_ids"][shot],"\t",
                      data_dict["ticks"][shot],"\t",
                      data_dict["file_names"][shot])
                      
                      
if __name__ == "__main__":
    m = Model()
    m.predict_to_terminal("./csvs/exampledata.csv")
