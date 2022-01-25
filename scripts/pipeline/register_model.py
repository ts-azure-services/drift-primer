import argparse
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from azureml.core.model import Model, Dataset
from azureml.core.run import Run, _OfflineRun
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def getArgs(argv=None):
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--model_name", help='Model name', required=True)
    parser.add_argument("--model_path", help='Model path', required=True)
    return parser.parse_args(argv)

def main():
    """Main operational flow"""
    args = getArgs()
    logging.info(f'Model name is: {args.model_name}')
    logging.info(f'Model path is: {args.model_path}')

    run = Run.get_context()

    # Get best model
    model = Model.register(workspace=ws, model_path=args.model_path, model_name=args.model_name)
    logging.info(f"Registered version {0} of model {1}".format(model.version, model.name))

if __name__ == "__main__":
    main()
