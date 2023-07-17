from DataLoader import DataLoader
from Preprocessor import Preprocessor
from FeatureEngineer import FeatureEngineer
from InitializePipeline import InitializePipeline
from Model import Model
from DataSplitter import DataSplitter
from ModelTrainer import ModelTrainer
from ModelTester import ModelTester
from ModelEvaluation import ModelEvaluation
import numpy as np
from typing import *


class PipelineExecuter:
    """
    Pipeline Executer class to orchestrate the execution of a Machine Learning pipeline
    """

    def __init__(self, config: Dict):
        """
        Constructor for PipelineExecuter

        Args:
            config (Dict): configuration dictionary with all the pipeline configuration
        """
        self.config = config

    def execute_pipeline(self):
        """
        Function to execute the pipeline
        """
        print("Loading data...")
        dataloader = DataLoader(filepath=self.config['data_filepath'], filetype='csv')
        df = dataloader.load_data()

        print("Preprocessing data: replacing values...")
        preprocessor1 = Preprocessor(df=df, preprocessing_type='replace_values',
                                     columns=['genre'], config={'none': 'Other', np.nan: 'other'})
        df = preprocessor1.preprocess()

        print("Engineering features: one-hot encoding...")
        feature_engineer = FeatureEngineer(df=df, engineering_type='one_hot', column='genre')
        df = feature_engineer.engineer_features()

        print("Preprocessing data: min-max scaling...")
        preprocessor2 = Preprocessor(df=df, preprocessing_type='minmax_scaler',
                                     columns=self.config['features'],
                                     config=self.config['scaler_parameters'])
        df = preprocessor2.preprocess()

        print("Splitting data into training and testing sets...")
        datasplitter = DataSplitter(df, self.config['features'], target_col=self.config['target'],
                                    test_size=self.config['test_size'])
        X_train, X_test, y_train, y_test = datasplitter.split()

        print("Building model...")
        model = Model(model_name=self.config['model_type'],
                      hyper_parameters=self.config['hyper_parameters'])
        trained_model = model.build_model()

        print("Training model...")
        model_trainer = ModelTrainer(X_train, y_train, trained_model)
        trained_model = model_trainer.train()

        print("Testing model...")
        model_tester = ModelTester(X_test, y_test, trained_model)
        predictions = model_tester.test()

        print("Evaluating model...")
        evaluator = ModelEvaluation(y_true=y_test, y_pred=predictions, metrics=['r2_score'])
        metrics = evaluator.calculate_metrics()

        print("Metrics:", metrics)

