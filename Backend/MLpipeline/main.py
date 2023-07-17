from InitializePipeline import InitializePipeline
from PipelineExecuter import PipelineExecuter

if __name__ == '__main__':
    print("Initializing pipeline...")
    config = InitializePipeline(config_file_path='./configs.yaml').get_config()
    pipeline_executer = PipelineExecuter(config)
    print("Executing the pipeline")
    pipeline_executer.execute_pipeline()


