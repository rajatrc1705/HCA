from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from typing import *
import numpy as np


class ModelEvaluation:
    """
    Model Evaluator class
    """

    def __init__(self, y_true: Union[np.ndarray, List[float]], y_pred: Union[np.ndarray, List[float]],
                 metrics: List[str] = ['r2_score']):
        """
        Constructor for Model Evaluator

        Args:
            y_true (Union[np.ndarray, List[float]]): Actual target values
            y_pred (Union[np.ndarray, List[float]]): Predicted target values
            metrics (List[str]): List of metric names to be calculated. Default is ['r2_score']
        """
        self.y_true = y_true
        self.y_pred = y_pred
        self.metrics = metrics
        self.metric_functions = {'r2_score': r2_score, 'mean_squared_error': mean_squared_error,
                                 'mean_absolute_error': mean_absolute_error}
        # We can similarly add more metrics

    def calculate_metrics(self) -> dict:
        """
        Function to calculate the metrics

        Returns:
            dict: Dictionary with metric names as keys and calculated metric scores as values
        """
        results = {}
        for metric in self.metrics:
            if metric in self.metric_functions:
                results[metric] = self.metric_functions[metric](self.y_true, self.y_pred)
            else:
                raise ValueError(
                    f'Metric {metric} is not supported. Please choose among {list(self.metric_functions.keys())}')
        return results
