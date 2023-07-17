from sklearn.preprocessing import PolynomialFeatures
from typing import *
import pandas as pd


class FeatureEngineer:
    """
    Feature Engineering class
    """

    def __init__(self, df: pd.DataFrame, engineering_type: str, column: str, config: Dict[str, Any] = {}):
        """
        Constructor for feature engineer

        Args:
            df (pd.DataFrame): DataFrame to engineer features on
            engineering_type (str): Type of feature engineering operation to be performed
            columns (List[str]): List of column names on which the operation will be applied
            **kwargs: Arbitrary keyword arguments for feature engineering configurations
        """
        self.df = df
        self.engineering_type = engineering_type
        self.column = column
        self.config = config

    def engineer_features(self) -> pd.DataFrame:
        """
        Function to engineer features

        Returns:
            pd.DataFrame: DataFrame with engineered features
        """
        if self.engineering_type == "one_hot":
            self.df = self._one_hot_encoding(self.df, self.column)
        elif self.engineering_type == "polynomial":
            self.df = self._create_polynomial_features(self.df, self.column, **self.config)
        # add more feature engineering methods as needed

        return self.df

    @staticmethod
    def _one_hot_encoding(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Perform one-hot encoding for the specified columns

        Args:
            df (pd.DataFrame): DataFrame to engineer features on
            columns (List[str]): List of column names on which the operation will be applied

        Returns:
            pd.DataFrame: DataFrame with one-hot encoded features
        """
        onehot_df = pd.get_dummies(df[column]).add_suffix('_onehot')
        df = pd.concat(
            [df.drop(columns=[column]),
             onehot_df],
            axis=1
        )
        return df

    @staticmethod
    def _create_polynomial_features(df: pd.DataFrame, column: str, **kwargs) -> pd.DataFrame:
        """
        Create polynomial features for the specified columns

        Args:
            df (pd.DataFrame): DataFrame to engineer features on
            columns (List[str]): List of column names on which the operation will be applied
            **kwargs: Arbitrary keyword arguments for PolynomialFeatures

        Returns:
            pd.DataFrame: DataFrame with polynomial features
        """
        poly = PolynomialFeatures(**kwargs)
        new_features = poly.fit_transform(df[column])
        new_columns = poly.get_feature_names(input_features=column)
        new_df = pd.DataFrame(new_features, columns=new_columns)

        df = pd.concat([df, new_df], axis=1)
        return df


