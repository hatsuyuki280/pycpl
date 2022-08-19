#!/bin/env python3
import logging
import yaml

###
# Config Loader
###

def configPreCheck(config):
    pass

def configLoader(configFile='../config/config.yaml'):
    with open(configFile, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        if configPreCheck(config):
            logging.info(f'Config file is loaded.', 'you want to load: {config} from {configFile}')
            return config
        else:
            logging.error(f'Config file is not valid.', 'you want to load: {config} from {configFile}')
            return None

def configWriter(configFile='../config/config.json', config=None):
    if config is not None:
        if configPreCheck(config):
            with open(configFile, 'w') as f:
                yaml.dump(config, f)
                logging.info(f'Config file is written.', 'you want to write: {config} to {configFile}')
                f.close()
            return True
        else:
            logging.error(f'Config file is not valid.', 'you want to write: {config} to {configFile}')
            return False