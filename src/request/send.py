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
from __future__ import unicode_literals # implicitly declaring all strings as unicode strings

""" Using either carrier API's or the raspberry pi, we define functions
that send SMSs."""

import os
import sys
import wget                     # wget command (for api free)
import urllib                   # used to transform text into url
import logging
from os.path import expanduser

# -- Setup Logging --
logging = logging.getLogger(__name__)
# -- Static data (install). --
REQUEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(REQUEST_DIR) + "/../"
# -- User Data --
execfile(expanduser(PROJECT_DIR+'config_backends.py'))


def sendTextFree(text, login, password, is_testing=False):
    """ Send the message [text] through the Free API
    (so only to the corresponding nb.)."""
    logging.info("Sending using FREE API....")
    if type(text) == type(u'unicodesd'):
        text_enc = text.encode('utf8')
    else:
        text_enc = text
    encodedText = urllib.quote_plus(text_enc) # url-ize the message's content
    logging.info("Encodings OK...")
    url = ('https://smsapi.free-mobile.fr/sendmsg?user=%s&pass=%s&msg=%s'
           % (login, password, encodedText))
    filename = "./tmp/torm.tmp"
    if not(is_testing):
        try:
            out = wget.download(url,out=filename)
            os.remove(filename)
            logging.info("Everything went well....")
        except IOError as e:
            logging.error("sendTextFree > wget | I/O error({0}): {1}".format(e.errno, e.strerror))
            exit(0)
    else:
        logging.warning("I do not send any SMS (we are testing now!).")
    logging.info("END")


def sendTextRasp(text, number, is_testing=False):
    """ Send the mesage [text] to [number] (of the form +XXYY...) through the Raspberry's SIM. """
    logging.info("Sending using Raspberry's SIM.")
    if type(text) == type(u'unicodesd'):
        logging.info("Text is unicodesd, we go to UTF8.")
        text_enc = text.encode('utf8')
    else:
        text_enc = text
    encodedText = urllib.quote_plus(text_enc) # url-ize the message's content
    IP_RASP = CONF['config_api']['ip_raspberry']
    api_key = CONF['config_api']['api_secret_key']
    number = urllib.quote_plus(number)
    url = ("https://" + IP_RASP + "/webtext/api/sendSMS.php?content=%s&number=%s&pass=%s"
           % (encodedText, number, api_key))
    filename = "./tmp/torm.tmp"
    logging.info(url)
    if not(is_testing):
        try:
            out = wget.download(url,out=filename)
            os.remove(filename)
        except IOError as e:
            logging.error("sendTextRasp > wget | I/O error({0}): {1}".format(e.errno, e.strerror))
            exit(0)
    else:
        logging.info("I do not send any SMS (we are testing now!).")
    

def sendText(texts, user, optionsDict, is_testing=False):
    """ Send the message [text] to [user]."""
    logging.info("Starting sendText.")
    userSend = user['sendSMS']
    method = userSend['method']
    if method == "FREE_API":
        for text in texts:
            sendTextFree(text, userSend['login'], userSend['password'], is_testing=is_testing)
    elif method == "RASP":
        number = user['number']  # string
        for text in texts:
            sendTextRasp(text, number, is_testing=is_testing)
    else:
        logging.info("Sending capabiility is not defined for user %s." % (user['login']))
        
        
