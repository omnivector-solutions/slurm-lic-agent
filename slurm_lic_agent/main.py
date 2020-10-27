#!/usr/bin/env python3
import asyncio
from argparse import ArgumentParser
import logging
import os
from pathlib import Path
import pwd
import sys

import websockets
import yaml


def _connect_to_websocket_server(websocket_uri):
    async def echo():
        async with websockets.connect(websocket_uri) as websocket:
            async for message in websocket:
                print(message)

    asyncio.get_event_loop().run_until_complete(echo())


def _create_logger(log_file_path=None):
    log_format = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename=log_file_path, format=log_format)
    return logging.getLogger('slurm-lic-agent')


def _get_parsed_args(argv):
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

    log_file = parser.add_argument(
        "-l",
        "--log-file",
        dest="log_file_path",
        required=False,
        type=str,
        help="Log file path."
    )
    return parser.parse_args(argv)


def main(argv=sys.argv[1:]):
    args = _get_parsed_args(argv)

    # Check for logging config and configure the logger appropriately.
    log_path = args.log_file_path or None
    logger = _create_logger(log_path)

    # If no config file argument given, there isn't much we can do.
    if not args.config_file_path:
        logger.warning("No config file specified. Exiting gracefully.")
        sys.exit(0)

    # Similarly, if the config file location is specified but doesn't exist,
    # there isn't much we can do.
    if not args.config_file_path.exists():
        logger.warning(
            f"No config file found at {str(args.config_file_path)}.\n"
            "Exiting gracefully."
        )
        sys.exit(0)


    # Load the yaml or log and exit.
    try:
        slurm_lic_config = yaml.full_load(args.config_file_path.read_text())
    except yaml.YAMLError as e:
        logger.warning(f"Yaml formatting error - {e}") 
        sys.exit(0)

    websocket_uri = slurm_lic_config.get('websocket_uri')
    auth_token = slurm_lic_config.get('auth_token')

    if not (websocket_uri and auth_token):
        logger.warning("Need 'websocket_uri' and 'auth_token'.") 
        sys.exit(0)


    _connect_to_websocket_server(websocket_uri)


if __name__ == "__main__":
    main()
