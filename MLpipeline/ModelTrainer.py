from typing import Any
import pandas as pd


class ModelTrainer:
    """
    Model Trainer class
    """

    def __init__(self, X_train: pd.DataFrame, y_train: pd.Series, model: Any):
        """
        Constructor for ModelTrainer

        Args:
            X_train (pd.DataFrame): Training features
            y_train (pd.Series): Training target
            model (Any): Untrained model
        """
        self.X_train = X_train
        self.y_train = y_train
        self.model = model

    def train(self) -> Any:
        """
        Train the model with the provided training data

        Returns:
            model: Trained model
        """
        self.model.fit(self.X_train, self.y_train)
        return self.model
