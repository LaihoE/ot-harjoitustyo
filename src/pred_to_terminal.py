import os
from anti_cheat import Model


if __name__ == '__main__':
    path_to_csv = 'csvs/data.csv'

    dirname = os.path.dirname(__file__)
    model_path = os.path.join(dirname, 'utils', 'ml_model.onnx')
    model = Model(model_path)
    model.predict_to_terminal(path_to_csv)