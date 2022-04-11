import unittest
from anti_cheat import Model
import numpy as np
import os


class TestModel(unittest.TestCase):
    def setup():
        pass

    def test_model_initialized_succesful(self):
        # init model
        dirname = os.path.dirname(__file__)
        model_path = os.path.join(dirname, '..', 'models', 'ml_model.onnx')
        model = Model(model_path)
        # Create correct shape array of ones and predict (1 sample with 192 rows and 5 columns)
        testdata = np.float32(np.ones((1, 192, 5)))
        ort_inputs = {model.ort_session.get_inputs()[0].name: testdata}
        ort_outs = np.array(model.ort_session.run(None, ort_inputs))
        cheating_confidence = list(ort_outs[0][:, 1])
        # Make sure the model gives expected confidence. Round to 5 decimals due to margin of error
        self.assertEqual(round(np.float32(cheating_confidence[0]), 5), round(
            np.float32(0.03877572), 5))
