# encoding: utf-8
'''
@author:     Daniel Hnyk

@copyright:  2015 Daniel Hnyk

@license:    BSD

@contact:    kotrfa@gmail.com
@deffield    updated: 19.04.2015
'''

'''
TODO
-----
* border execeptions - if there are really twice...
'''

import sys
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from time import sleep

__all__ = []
__version__ = 0.2
__date__ = '2015-04-18'
__updated__ = '2017-08-14'

program_name = os.path.basename( sys.argv[0] )
program_version = "v%s" % __version__
program_build_date = str( __updated__ )
program_version_message = '%%(prog)s %s (%s)' % ( program_version, program_build_date )
program_shortdesc = __import__( '__main__' ).__doc__.split( "\n" )[1]
program_license = '''%s

Created by Daniel Hnyk on %s.
Copyright 2015 Daniel Hnyk. All rights reserved.

Licensed under the BSD.

Distributed on an "AS IS" basis without warranties
or conditions of any kind, either express or implied.

USAGE
''' % ( program_shortdesc, str( __date__ ) )

# Setup argument parser
parser = ArgumentParser( description = program_license, formatter_class = RawDescriptionHelpFormatter )
parser.add_argument( "-v", "--verbose", dest = "verbose", action = "store_true", help = "Verbose mode." )
parser.add_argument( "-d", "--driver", choices = ["firefox", "phantomjs"], default = "firefox", help = "Which driver should be used (default: %(default)s)" )
parser.add_argument( "-f", "--file", default = "input.html", help = "Input file formated in HTML which should be pasted into Long Description (default: %(default)s)" )
parser.add_argument( "-c", "--codes", required = True, type = str, help = "Codes of geacaches separated by comma. E.g. 'GC3YJME,GC3YJMX'" )
parser.add_argument( '-V', '--version', action = 'version', version = program_version_message )
parser.add_argument( "-m", "--maternal_url", default = "http://www.geocaching.com/geocache/", type = str, help = "Maternal URL of geocaches (default: %(default)s)" )
parser.add_argument( "-l", "--logins", required = True, help = "Login names and passwords in 'user1:passwd1,user2:passwd2'" )
parser.add_argument( '-s', "--submit", action = 'store_true', help = "If changes should be submited." )
parser.add_argument( '-t', "--date", type = str, required = True, help = "Set LogDate. E.g. '2017-12-28'" )
parser.add_argument( '-b', "--border", default = "<!--DONTCHANGE-->", help = "Every long description must contain this string exactly TWICE. Everything between these two occurences will be replaced. (default: %(default)s)" )
parser.add_argument( '--log', default = "out.log", help = "Name of log file. (default: %(default)s)" )

# Process arguments
args = parser.parse_args()

codes = args.codes.split( "," )
users = args.logins.split( "," )
logdate = args.date

content = ""
with open( args.file, "r", encoding = "utf8" ) as ifile:
    content = ifile.read()
# print( content )

dr = ""
if args.driver == "firefox":
    dr = webdriver.Firefox()
elif args.driver == "phantomjs":
    dr = webdriver.PhantomJS()

dr.set_window_size( 1400, 1000 )

def verb( st ):
    if args.verbose:
        print( st )

    with open( args.log, "a", encoding = "utf8" ) as logfile:
        logfile.write( st + "\n" )

class Cache():

    code = ""
    url = ""

    def click( self, xpath ):
        dr.find_element_by_xpath( xpath ).click()

    def sign_out( self ):
        # sign out
        self.click( "//*[contains(@class, 'li-user-toggle')]" )
        self.click( "//*[contains(@class, 'sign-out')]" )
        #body = dr.find_element_by_tag_name( "body" )
        #body.send_keys( Keys.ALT + Keys.SHIFT + 's' )
        #self.click( '//*[@id="ctl00_hlSignOut"]' )

        sleep( 1 )


    def __init__( self, code ):
        self.code = code
        self.url = args.maternal_url + code


        verb( "Processing: " + self.code )
        trying = True
        for user in users:
            if trying:
                login_name, password = user.split( ":" )
                verb( "Username: " + login_name )

                dr.get( self.url )
                name_of_cache = dr.find_element_by_xpath( '//*[@id="ctl00_ContentBody_CacheName"]' ).text
                verb( "Name of cache: " + name_of_cache )

                try:
                    # sign in form
                    self.click( '//*[@id="hlSignIn"]' )

                    lgn = dr.find_element_by_xpath( '//*[@id="Username"]' )
                    lgn.send_keys( login_name )

                    psw = dr.find_element_by_xpath( '//*[@id="Password"]' )
                    psw.send_keys( password )

                    # check box remember me (maybe not necessary)
                    #self.click( '//*[@id="ctl00_cbRememberMe"]' )

                    # submit login form
                    self.click( '//*[@id="Login"]' )

                except NoSuchElementException:
                    verb( "You are already login" )

                try:
                    # click on edit link
                    self.click( '//*[@id="ctl00_ContentBody_GeoNav_logButton"]' )

                    # select log date
                    dr.execute_script("document.getElementById('LogDate').value='" + logdate + "'")
                    sleep( 0.5 )

                    # inser to text area of long description
                    textarea = dr.find_element_by_xpath( '//*[@id="LogText"]' )
                    text = textarea.get_attribute( "value" )

                    verb( 'LogDate' )
                    verb( logdate )
                    textarea.send_keys( content )
                    verb( content )

                    if args.submit:
                        # submit edit
                        dr.find_element_by_xpath( '//span[contains(text(),"Post")]' ).click()
                        sleep( 0.5 )

                    #self.sign_out()
                    trying = False
                except NoSuchElementException:
                    verb( "You have no rights to edit this geocache!" )

                    #self.sign_out()
                    dr.get( self.url )

        #sleep( 1.5 )
        #body = dr.find_element_by_tag_name("body")
        #body.send_keys( Keys.CONTROL + 't' )


if __name__ == "__main__":

    for code in codes:
        Cache(code)

    sys.exit( 0 )
