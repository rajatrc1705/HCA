from typing import *
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class Preprocessor:
    """
    Data Preprocessor class
    """

    def __init__(self, df: pd.DataFrame, preprocessing_type: str, columns: List[str], **kwargs):
        """
        Constructor for data preprocessor

        Args:
            df (pd.DataFrame): DataFrame to be preprocessed
            preprocessing_type (str): Type of preprocessing operation to be performed
            columns (List[str]): List of column names on which the operation will be applied
            **kwargs: Arbitrary keyword arguments for preprocessing configurations
        """
        self.df = df
        self.preprocessing_type = preprocessing_type
        self.columns = columns
        self.config = kwargs

    def preprocess(self) -> pd.DataFrame:
        """
        Function to preprocess the data

        Returns:
            pd.DataFrame: Preprocessed DataFrame
        """
        if self.preprocessing_type == "standard_scaler":
            self.df = self._standard_scaler(self.df, self.columns, **self.config)
        elif self.preprocessing_type == "minmax_scaler":
            self.df = self._minmax_scaler(self.df, self.columns, **self.config)
        elif self.preprocessing_type == "replace_values":
            self.df = self._replace_values(self.df, self.columns, **self.config)
        # add more preprocessing methods as needed

        return self.df

    @staticmethod
    def _standard_scaler(df: pd.DataFrame, columns: List[str], **kwargs) -> pd.DataFrame:
        """
        Apply standard scaling on the specified columns

        Args:
            df (pd.DataFrame): DataFrame to be scaled
            columns (List[str]): List of column names to be scaled
            **kwargs: Arbitrary keyword arguments for scaler configurations

        Returns:
            pd.DataFrame: Scaled DataFrame
        """
        scaler = StandardScaler(**kwargs['config'])
        df[columns] = scaler.fit_transform(df[columns])

        return df

    @staticmethod
    def _minmax_scaler(df: pd.DataFrame, columns: List[str], **kwargs) -> pd.DataFrame:
        """
        Apply min-max scaling on the specified columns

        Args:
            df (pd.DataFrame): DataFrame to be scaled
            columns (List[str]): List of column names to be scaled
            **kwargs: Arbitrary keyword arguments for scaler configurations

        Returns:
            pd.DataFrame: Scaled DataFrame
        """
        kwargs['config']['feature_range'] = tuple(kwargs['config']['feature_range'])
        scaler = MinMaxScaler(**kwargs['config'])
        df[columns] = scaler.fit_transform(df[columns])

        return df

    @staticmethod
    def _replace_values(df: pd.DataFrame, columns: List[str], **kwargs) -> pd.DataFrame:
        """
        Replace specified values in DataFrame

        Args:
            df (pd.DataFrame): DataFrame in which to replace values
            columns (List[str]): List of column names in which to replace values
            **kwargs: Arbitrary keyword arguments for value mappings

        Returns:
            pd.DataFrame: DataFrame with replaced values
        """
        for column in columns:
            df[column] = df[column].replace(kwargs['config'])

        return df

