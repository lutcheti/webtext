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

def sendTextFree(text, login, password, is_testing=False):
    """ Send the message [text] through the Free API
    (so only to the corresponding nb.)."""
    logging.info("Sending using FREE API....")
    if type(text) == type(u'unicodesd'):
        text_enc = text.encode('utf8')
    else:
        text_enc = text
    encodedText = urllib.quote_plus(text_enc) # url-ize the message's content
    url = ('https://smsapi.free-mobile.fr/sendmsg?user=%s&pass=%s&msg=%s'
           % (login, password, encodedText))
    filename = "./tmp/torm.tmp"
    if not(is_testing):
        out = wget.download(url,out=filename)
        os.remove(filename)
    else:
        logging.info("I do not send any SMS (we are testing now!).")

def sendTextEmail(text, operateur, number, is_testing=False):
    """ Send the message [text] through e-mails. """
    logging.info("Sending using EMAIL....")
    if type(text) == type(u'unicodesd'):
        text_enc = text.encode('utf8')
    else:
        text_enc = text

    if operateur == "orange":
        address = number + "@" + "orange.fr"
    else:
        logging.error("I don't know how to send this email.")
        return()

    if not(is_testing):
        # SEND THE EMAIL 'text_enc' to 'address'
    else:
        logging.info("I do not send any SMS (we are testing now!).")


def sendText(text, user, is_testing=False):
    """ Send the message [text] to [user]."""
    logging.info("Starting sendTextFREE.")
    userSend = user['sendSMS']
    if userSend['method'] == "FREE_API":
        sendTextFree(text, userSend['login'], userSend['password'], is_testing=is_testing)
    elif userSend['method'] == "EMAIL":
        sendTextEmail(text, userSend['operateur'], user['number'], is_testing=is_testing)
    else:
        logging.info("Sending capabiility is not defined for user %s." % (user['login']))
        
        
