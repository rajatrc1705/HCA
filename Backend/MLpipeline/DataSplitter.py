from sklearn.model_selection import train_test_split
import pandas as pd
from typing import *


class DataSplitter:
    """
    Data Splitter class
    """

    def __init__(self, df: pd.DataFrame, input_cols: List[str], target_col: str, test_size: float = 0.2,
                 random_state: int = 42, stratify: Any = None):
        """
        Constructor for data splitter

        Args:
            df (pd.DataFrame): DataFrame to be split
            input_cols (List[str]): List of column names to be used as input features
            target_col (str): Column name to be used as target
            test_size (float): Size of the test set. Default is 0.2
            random_state (int): Random state for reproducibility. Default is 42
            stratify (Any): Column for stratified sampling. Default is None
        """
        self.X = df[input_cols]
        self.y = df[target_col]
        self.test_size = test_size
        self.random_state = random_state
        self.stratify = stratify

    def split(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Function to split the data into training and test sets

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: Training and test sets (both input features and target)
        """
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=self.test_size,
                                                            random_state=self.random_state,
                                                            stratify=self.y if self.stratify else None)
        return X_train, X_test, y_train, y_test
