# Copyright (c) 2018 RoastinMalware
# See the LICENSE file for more information

"""
This module contains any logic to parse the config file
"""
import configparser
import os

def getConfiguration(cfgfile: str) -> object:
    """
    Read config
    @param cfgfile: filename of the file
    @return: ConfigParser object
    """
    parser = configparser.ConfigParser()
    if len(parser.read(cfgfile)) == 0: #reading was not successfully        
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
    if CONFIG is None: # config is empty        
        CONFIG=getConfiguration("configuration.cfg")

    if CONFIG is None: # config is still empty -> failure
        return None

    if section in CONFIG and key in CONFIG[section]:
        return CONFIG[section][key]    
   
    return None

CONFIG = None