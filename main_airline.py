import os
import glob
import pdfplumber
from pathlib import Path
from urllib.error import HTTPError
import shutil
import pathlib
import datetime
import json
import configparser
import re
import time
import sys
import time
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.runtime.client_request_exception import ClientRequestException
from ast import literal_eval
from string import ascii_lowercase
from itertools import groupby
# import pandas as pd
from office365.sharepoint.files.move_operations import MoveOperations
from Air_Inv_Ext import airinvex


config_obj = configparser.ConfigParser()
config_obj.read('/code/config.ini')

sppaths = config_obj['spdl_path']
spparam = config_obj['spdoclib']
sprlpath = config_obj['sp_relative_path']
fol_loc = config_obj['folder_path']

spsite = spparam['rootsite']
spdoclib = spparam['site_url']
spusername = spparam['uname']
sppassword = spparam['upass']
cid = spparam['cid']
cs = spparam['cs']

sproot = sppaths['root']
spprocessed = sppaths['processed']
spproblematic = sppaths['problematic']
spduplicate = sppaths['duplicate'] ###Add duplicate path

lsppath = fol_loc['spdl']

sprppro = sprlpath['processed']
sprproot= sprlpath['root']
sprpproblem = sprlpath['problematic']
sprpduplicate = sprlpath['duplicate'] ###Add duplicate path

def move_to_folder_processed(folder):
    file_from = ctx.web.get_folder_by_server_relative_url(folder).execute_query()
    file_to = file_from.move_to(sprppro).execute_query()
    print("'{0}' moved into '{1}'".format(folder, sprppro))

def try_get_folder(url):
    try:
        return ctx.web.get_folder_by_server_relative_url(url).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)
        
ctx = ClientContext(spdoclib).with_credentials(ClientCredential(cid, cs))

root_folder = ctx.web.get_folder_by_server_relative_path(sproot)
pro_folder = ctx.web.get_folder_by_server_relative_path(spprocessed)
                                                                                                                                                        
def try_get_folder(url):
    try:
        return ctx.web.get_folder_by_server_relative_url(url).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)
        
root_folder.expand(["Folders"]).get().execute_query()
metaurl = ''
for folder in root_folder.folders:
    folder = try_get_folder(folder.serverRelativeUrl)
    files = folder.get_files(True).execute_query()
    for f in files:

        metaurl = f.properties['ServerRelativeUrl']
        finalurl = spsite+metaurl
        file_name = os.path.basename(finalurl)
        path = os.path.join(lsppath, file_name)

        with open(path,'wb') as local_file:
            p_file = ctx.web.get_file_by_server_relative_url(metaurl).download(local_file).execute_query()
    
        if '.pdf' in file_name or '.PDF' in file_name:
            print('pdf',file_name)
            pdf = pdfplumber.open(path)
            text = pdf.pages[0].extract_text()
            airinvex(path)
            # exec(open(r'D:\Airline Invoice Code\Airline_Invoice_Extraction.py').read(), {'path': path })
        os.remove(path)
    move_to_folder_processed(folder.serverRelativeUrl )


    

