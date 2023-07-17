from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


class Model:
    """
    Model Builder class
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Constructor for model builder

        Args:
            model_name (str): Name of the model to be built
            **kwargs: Arbitrary keyword arguments for model configurations
        """
        self.model_name = model_name
        self.config = kwargs

    def build_model(self):
        """
        Function to build the model

        Returns:
            model: Built model
        """
        if self.model_name == "linear_regression":
            model = LinearRegression(**self.config['hyper_parameters'])
        elif self.model_name == "random_forest":
            model = RandomForestRegressor(**self.config['hyper_parameters'])
        elif self.model_name == "gradient_boosting_regressor":
            model = GradientBoostingRegressor(**self.config['hyper_parameters'])
        else:
            raise ValueError(f"Unknown model name {self.model_name}")

        return model
