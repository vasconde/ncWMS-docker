#!/usr/bin/python3

# receives a dataset path
# puts it in ncWMS
# returns the WMS URL

import os
import sys
import requests
from requests.auth import HTTPDigestAuth
import argparse


NCWMS_URL = 'http://localhost:8181/ncWMS2/'
NCWMS_USER_PASS = ('admin', 'admin123')

def loadEnvVars ():

    if (os.getenv('NC_HOST')):
        if (os.getenv('NC_PORT')):
            NCWMS_URL = ':'.join([os.getenv('NC_HOST'), os.getenv('NC_PORT')]) + '/ncWMS2/'
        else:
            NCWMS_URL = os.getenv('NC_HOST') + '/ncWMS2/'

    if (os.getenv('NC_USER') and os.getenv('NC_PASS')):
        NCWMS_USER_PASS = (os.getenv('NC_USER'), os.getenv('NC_PASS'))


def addDataset (id, title, location):

    dataset_metadata = {"id" : id, "title" : title, "location" : location}

    res = requests.post(NCWMS_URL + 'admin/addDataset',
        data=dataset_metadata,
        auth=HTTPDigestAuth(*NCWMS_USER_PASS))

    return res

def removeDataset(id):

    res = requests.post(NCWMS_URL + 'admin/removeDataset',
        data={"id" : id},
        auth=HTTPDigestAuth(*NCWMS_USER_PASS))

    return res

# examples:
# ./add_remove_dataset.py --add --id smw_AVEIRO__20210517 --title smw_AVEIRO__20210517 --path /usr/local/tomcat/data/smw_AVEIRO__20210517.nc
# ./add_remove_dataset.py --remove --id smw_AVEIRO__20210517
if __name__ == "__main__":

    loadEnvVars ()

    parser = argparse.ArgumentParser(description='Add and remove datasets to ncWMS.')

    parser.add_argument("-a", "--add", action="store_true", help="Add dataset")
    parser.add_argument("-r", "--remove", action="store_true", help="Remove dataset")
    #parser.add_argument("-u", "--username", help="User name")
    #parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-id", "--id", help="Dataset ID")
    parser.add_argument("-t", "--title", help="Title ID")
    parser.add_argument("-pt", "--path", help="Path ID")
    
    args = parser.parse_args()

 
    if (args.add):
        
        if (args.id and args.title and args.path):

            res = addDataset(args.id, args.title, args.path)

            #print(res.status_code)
            if(res.status_code == 200):
                print(NCWMS_URL + 'wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0&DATASET=' + args.id)

        else:

            print('id, title and path arguments are required!')

    elif (args.remove):

        if (args.id):
            
            res = removeDataset(args.id)
        
            print(res.text)

        else:

            print('id argument are required!')

    else:

        print("Neither add nor remove arguments were selected!")
        

    sys.exit()