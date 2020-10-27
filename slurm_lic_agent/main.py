#!/usr/bin/env python3
from argparse import ArgumentParser
import logging
import os
from pathlib import Path
import pwd
import sys

import yaml


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)


logger = logging.getLogger('slurm-lic-agent')


def get_parsed_args(argv):
    """Create argument parser and return cli args.
    """
    parser = ArgumentParser(
        description="SLURM_LIC_AGENT"
    )

    config_file = parser.add_argument(
        "-c",
        "--config",
        dest="config_file_path",
        required=False,
        type=Path,
        help="Configuration file path."
    )
    return parser.parse_args(argv)


def main(argv=sys.argv[1:]):
    args = get_parsed_args(argv)

    if not args.config_file_path:
        logger.warning("No config file specified. Exiting gracefully.")
        sys.exit(0)

    if not args.config_file_path.exists():
        logger.warning(
            f"No config file found at {str(args.config_file_path)}.\n"
            "Exiting gracefully."
        )
        sys.exit(0)

    try:
        slurm_lic_config = yaml.full_load(args.config_file_path.read_text())
    except yaml.YAMLError as e:
        logger.warning(f"Yaml formatting error - {e}") 
        sys.exit(0)

    print(slurm_lic_config)



if __name__ == "__main__":
    main()
