#!/usr/bin/env python3
'''
    api-test.py
    Jeff Ondich, 11 April 2016
    Updated 7 October 2020

    An example for CS 257 Software Design. How to retrieve results
    from an HTTP-based API, parse the results (JSON in this case),
    and manage the potential errors.
'''

import sys
import argparse
import json
import urllib.request

API_BASE_URL = 'http://api.covidtracking.com/v1/'
API_KEY = 'cs257'
   

def main(args):
    if args.date:
        
    
if __name__ == '__main__':
    # When I use argparse to parse my command line, I usually
    # put the argparse setup here in the global code, and then
    # call a function called main to do the actual work of
    # the program.
    parser = argparse.ArgumentParser(description='Get Covid data')

    parser.add_argument('date',
                        metavar='date',
                        help='Date for which data is being requested (in ISO format)',
                        type=str)

    args = parser.parse_args()
    main(args)
