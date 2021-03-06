import argparse
import sys
import os
import importlib
import utils

parser = argparse.ArgumentParser(description='QML')
add_arg = parser.add_argument
add_arg("-c", "--config", dest="config_name", help="Configuration name")
add_arg("-s","--save-fig", dest="save_fig", help="Save resulting image if used", action='store_true')
add_arg("--hide", dest='hide_display', help="Hide the display of results", action='store_true')
add_arg("--overwrite", help="Overwrite plot and log files iff true", action='store_true')
add_arg("--debug", help="Debug mode", action='store_true')



if __name__ == "__main__":
    
    args = parser.parse_args()
    config_file = importlib.import_module(f"src.configs.{args.config_name}")
    config = config_file.config
    print(f">>> Configuration:\n{config}")
    model_name = config['model']
    model_file = importlib.import_module(f"src.models.{model_name}")
    model_class = model_file.Model

    model = model_class(config, save_fig=args.save_fig, overwrite=args.overwrite, debug=args.debug, hide_display=args.hide_display)
    model.train()
    model.evaluate()