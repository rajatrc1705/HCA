from typing import Union
import pandas as pd


class DataLoader:
    """
    Data Loader class
    """

    def __init__(self, filepath: str, filetype: str):
        """
        Constructor for data loader

        Args:
            filepath (str): File path to dataset
            filetype (str): Type of file to load ('csv', 'excel', 'parquet', etc.)
        """
        self.filepath = filepath
        self.filetype = filetype

    def load_data(self) -> Union[pd.DataFrame, None]:
        """
        Function to load the data

        Returns:
            DataFrame: Loaded data
        """
        if self.filetype == 'csv':
            df = pd.read_csv(self.filepath)
        elif self.filetype == 'excel':
            df = pd.read_excel(self.filepath)
        elif self.filetype == 'parquet':
            df = pd.read_parquet(self.filepath)
        # We can add more readers here
        else:
            raise ValueError(f"Unsupported filetype: {self.filetype}")

        return df
