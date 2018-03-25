# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module contains any logic to parse the config file
"""
import configparser
from os.path import dirname, abspath, join

CONFIG = None
ROOT = dirname(dirname(abspath(__file__)))


def getConfiguration(cfgfile: str) -> object:
    """
    Read config
    @param cfgfile: filename of the file
    @return: ConfigParser object
    """
    parser = configparser.ConfigParser()
    if parser.read(cfgfile) is False:  # reading was not successfully
        return None
    return parser


def getConfigurationValue(section: str, key: str):
    """
    Get config value
    @param section: the section of the config value
    @param key: the config value name itself
    @return: the value or None, if not found
    """
    global CONFIG
    if CONFIG is None:  # config is empty
        CONFIG = getConfiguration(join(ROOT, "configuration.cfg"))

    if CONFIG is None:  # config is still empty -> failure
        return None

    if section in CONFIG and key in CONFIG[section]:
        value = CONFIG[section][key]
        if value == 'true' or value == 'false':
            return value == 'true'
        return CONFIG[section][key]

    return None
