# -- coding: utf-8 --
###########################################################################
#                                                                         #
#                       WebText                                           #
#                                                                         #
#                       Lucca Hirschi                                     #
#                       <lucca.hirschi@ens-lyon.fr>                       #
#                                                                         #
#    Copyright 2014 Lucca Hirschi                                         #
#                                                                         #
#    This file is part of OwnShare.                                       #
#    OwnShare is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by #
#    the Free Software Foundation, either version 3 of the License, or    #
#    (at your option) any later version.                                  #
#                                                                         #
#    OwnShare is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
#    GNU General Public License for more details.                         #
#                                                                         #
#    You should have received a copy of the GNU General Public License    #
#    along with OwnShare.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                         #
###########################################################################

""" Backend for JCdecaux's API. """

from __future__ import unicode_literals # implicitly declaring all strings as unicode strings

import os
import sys
import wget                     # wget command (for api free)
import subprocess               # for launching bash programs
import urllib                  # used to transform text into url
import urllib2                  # used to transform text into url
import logging
import json
from os.path import expanduser

import pprint

# -- Setup Logging --
logging = logging.getLogger(__name__)

REQUEST_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../"
PROJECT_DIR = os.path.dirname(REQUEST_DIR) + "/../../"
BACK_DATA_DIR = PROJECT_DIR + "data/backends/jcdecaux/"

execfile(expanduser(PROJECT_DIR+'config_backends.py'))

# for debugging Only
pp = pprint.PrettyPrinter(indent=4)

def loadJson(city):
    folder = BACK_DATA_DIR
    if city == 'Paris':
        json_data = open(folder + "Paris.json")
    elif city == 'Lyon':
        json_data = open(folder + "Lyon.json")
    elif city == 'Marseill':
        json_data = open(folder + "Marseille.json")
    else:
        logging.error("There is no static file City.json in data/backends/jcdecaux/.\n")
        return(None)
    data = json.load(json_data)
    return(data, json_data)


def searchVelib(where):
    """ Fetch available stations and bikes around a given location."""
    logging.info("Starting searchVelib")
    (dataStatic, toClose) = loadJson("Paris")
    pp.pprint(dataStatic[0:4])


# searchVelib("Chapelle")