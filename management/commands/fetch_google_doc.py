# -*- coding: utf-8 -*-

### coellection(django) ###
### GNU/GPL v2
### Author: Cody Rocker
### Author_email: cody.rocker.83@gmail.com
### 2016
#-----------------------------------
#   Requires:                    """
#    - xlrd 0.9.4                """
#    - Django 1.9.3              """
#-----------------------------------
import os
import sys
import subprocess
import json

import xlrd

from xlrd import open_workbook

## NOTE:  I tried several methods of fecthing this document programatically
##       (API requests, python libraries, etc.) before settling on this hack.
CURL_DOC = "curl 'https://docs.google.com/spreadsheets/d/14YXVLXDhQy-ri6E4pfx9QXTXluWfdYXR37IWdoPNjYM/export?format=xlsx&id=14YXVLXDhQy-ri6E4pfx9QXTXluWfdYXR37IWdoPNjYM' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: https://docs.google.com/spreadsheets/d/14YXVLXDhQy-ri6E4pfx9QXTXluWfdYXR37IWdoPNjYM/edit' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36' --compressed > {out_file}"
XLSX_FILE = os.path.join(os.path.dirname(__file__), "tmp/coellection_tmp.xlsx")
JSON_FILE = os.path.join(os.path.dirname(__file__), "tmp/coellection.json")


def fetch_spreadsheet():
    """ Download (curl) google document to an xlsx file
    """
    sys.stdout.write("\nDownlading coellection spreadsheet from Google...\n")
    subprocess.call(CURL_DOC.format(out_file=XLSX_FILE), shell=True)


def get_sheet_names(book):
    """ Return list of strings containing sheet name 
    """
    sheet_names = book.sheet_names()
    return sheet_names


def parse_sheet(book, sheet_name):
    """ Return list of dict objects containing row data
    """
    sheet = book.sheet_by_name(sheet_name)
    # Read header values into a list to be used as dict keys for row values.
    # Integer values reflect the first index to be read. Row 2 for table headers
    # and row 3 for table values
    keys = [sheet.cell(1, col_index).value for col_index in range(sheet.ncols)]

    dict_list = []
    for row_index in range(2, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value 
             for col_index in range(sheet.ncols)}
        dict_list.append(d)

    return dict_list


def make_json():
    """ Convert the xlsx file to json 
    """
    sys.stdout.write("\nConverting .xlsx to .json...")
    book = open_workbook(XLSX_FILE)
    sheets = get_sheet_names(book)
    book_data = {}
    for sheet in sheets:
        book_data[sheet] = parse_sheet(book, sheet)

    ## The state of the spreadsheets is saved as a json file for later use
    ## in diff comaprisons.
    with open(JSON_FILE, 'w') as outfile:
        json.dump(book_data, outfile)
    sys.stdout.write("done.\n")