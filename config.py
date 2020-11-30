import argparse
from pathlib import Path
import json
import logging.config

config = {}
parser = argparse.ArgumentParser(description='Analytics Flask Server')
parser.add_argument('--config', required=True, help='set config file location')
# parser.add_argument('--logging', required=False, help='set server logging option for analytics', action='store_true')
# parser.add_argument('--logging_config', required=False, help='set config location of logging')

args = parser.parse_args()

if Path(args.config).exists():
    with open(args.config) as json_file:    # Read configuration
        config = json.load(json_file)
else:
    print("provided configuration file was not found")
    quit()

# if args.logging:
#     if args.logging_config:
#         if Path(args.logging_config).exists():
#             logging.config.fileConfig(args.logging_config)
#         else:
#             print('invalid file path for logging config')
#             quit()
#     else:
#         print('logging configuration has not be provided')
#         quit()





