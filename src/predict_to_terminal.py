import os
from anti_cheat import Model



if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    model_path = os.path.join(dirname, 'models', 'ml_model.onnx')
    model = Model(model_path)

    csv_path = os.path.join(dirname, 'csvs', 'data.csv')
    model.predict_to_sql(csv_path)
