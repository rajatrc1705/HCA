import numpy as np
import pandas as pd
from typing import *


class ModelTester:
    """
    Model Tester class
    """

    def __init__(self, X_test: pd.DataFrame, y_test: pd.Series, model: Any):
        """
        Constructor for ModelTester

        Args:
            X_test (pd.DataFrame): Test features
            y_test (pd.Series): Test target
            model (Any): Trained model
        """
        self.X_test = X_test
        self.y_test = y_test
        self.model = model

    def test(self) -> np.ndarray:
        """
        Test the model with the provided test data

        Returns:
            np.ndarray: Predictions
        """
        predictions = self.model.predict(self.X_test)
        return predictions
