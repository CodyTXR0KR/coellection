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
import json
import shutil

from django.core.management.base import BaseCommand, CommandError
from coellection.models import Platform, Game, Amiibo

from .fetch_google_doc import fetch_spreadsheet, make_json, JSON_FILE
from .value_maps import *
from .filters import *

PARAM_ERR =  '{func_name} -- Unknown param: {param_value};'

# TODO: Take a url arg from command line and handle conversion to json
#       file programatically.
##          -- pull down xlsx from url
##          -- convert xlsx to json (modules/py_xls_to_json) & save to tmp
##          -- clean db
##          -- create new objects


## Make this script available to the manage.py interface
## this handles loading all django settings, models, etc.
class Command(BaseCommand):
    help = 'Pull down coellection google doc into django database.'

    def handle(self, *args, **options):
        """ Worker method, handles manage.py interface functionality
        """
        fetch_spreadsheet()
        make_json()
        coellection_json = load_json()

        """ NOTE: To avoid possible downtime/dataloss on process failure the
                  db should be cloned and stored here as a restoration point.
                  This is best handled by hooking into the DB backend directly
                  in a separate script and called here.

                  Since this is heavily dependant on the deployment backend it's
                  up to the user to implement this to suit thier own environment.
        """
        clear_old_models()


        """ New models are created here. This can take awhile if there are a lot
            of rows of data to parse.
        """
        sys.stdout.write('\nRebuilding tables with fresh data...\n')
        # 'key' value is the name of the sheet in the xls 'book'
        for key in coellection_json:
            # These sheets can be ignored
            if key in ['Stats', 'Info']:
                pass
            elif key == 'Systems':  # Map to 'Platform' model.
                for row in coellection_json[key]:
                    make_platform(row)
            elif key == 'Amiibo':  # Map to 'Amiibo' model.
                for row in coellection_json[key]:
                    make_amiibo(row)
            # The remaining sheets are tables of games for a single platform,
            else:  # Map to 'Game' model.
                for row in coellection_json[key]:
                    platform = get_platform(key)
                    make_game(platform, row)


def load_json():
    """ Return json data from disk as dict
    """
    with open(JSON_FILE, 'r') as f:
        json_data = json.load(f)
    f.close()
    return json_data


def clear_old_models():
    """ Since diff comparison between updates isn't implemented the db
        (Coellection models only) is wiped to avoid duplication of data.
    """
    # Objects are deleted, but the tables stay intact for repopulation
    sys.stdout.write("\nWiping table 'Platform'...")
    Platform.objects.all().delete()
    sys.stdout.write("done.\n")
    sys.stdout.write("Wiping table 'Amiibo'...")
    Amiibo.objects.all().delete()
    sys.stdout.write("done.\n")
    sys.stdout.write("Wiping table 'Game'...")
    Game.objects.all().delete()
    sys.stdout.write("done.\n")


def get_bool(value):
    """ Convert string to bool
    """
    if value == 'Yes':
        return True
    elif (value in ['No', 'None', ''] or value == None):
        return False
    else:
        raise Exception(PARAM_ERR.format(
            func_name=get_bool.__name__, param_value=value))


def get_plays(value):
    """ Convert string to integer
    """
    if value in PLAYS:
        return PLAYS[value]
    else:
        raise Exception(PARAM_ERR.format(
            func_name=get_plays.__name__, param_value=value))


def get_condition(value):
    """ Convert string to integer
    """
    if value in CONDITIONS:
        return CONDITIONS[value]
    else:
        raise Exception(PARAM_ERR.format(
            func_name=get_condition.__name__, param_value=value))


def get_platform(value):
    """ Convert string to db slug
    """
    if value in PLATFORMS:
        return PLATFORMS[value]
    else:
        raise Exception(PARAM_ERR.format(
            func_name=get_platform.__name__, param_value=value))


def get_cart_batt_cond(value):
    """ Convert string to integer
    """
    if value is None:
        return 0
    if value == 'None':
        return 0
    if value in CART_BATT:
        return CART_BATT[value]
    else:
        raise Exception(PARAM_ERR.format(
            func_name=get_cart_batt_cond.__name__, param_value=value))


## The django db models refactor ['Cart', 'Disc(s)', 'UMD', 'Media'] table headers to 'media_cond'
## so platform specific filering/handling is used to return appropriate values
def get_media_cond(platform, row):
    """ Return an integer for media_cond model property
    """
    if platform in CARTS:
        return get_condition(row['Cart'])
    elif platform in DISCS:
        return get_condition(row['Disc(s)'])
    elif platform in ["psp"]:
        return get_condition(row['UMD'])
    elif platform in ["pc"]:
        return get_condition(row["Media"])
    else:
        raise Exception(PARAM_ERR.format(
            func_name=get_media_cond.__name__, param_value=platform))


def make_platform(row_data):
    """ Map row_data to new django platform model object
    """
    item = Platform(
        title=row_data['Title'],
        upc=row_data['UPC'],
        serial=row_data['Serial'],
        model=row_data['Model'],
        donor=row_data['Donor'],
        notes=row_data['Notes'],
        modded=get_bool(row_data['Mod']),
        plays=get_plays(row_data['Plys']),
        box=get_condition(row_data['Box']),
        manual=get_condition(row_data['Man']),
        insert=get_condition(row_data['Ins']),
        vid_cable=get_condition(row_data['Vid Cbl']),
        pwr_cable=get_condition(row_data['Pwr Cbl']))
    try:
        item.save()
        sys.stdout.write('Saved Platform: {0}\n'.format(item.title))
        sys.stdout.flush()
    except Exception as e:
        # dump values for debug on exception
        sys.stdout.write('row={0};\n{2}'.format(row_data, e))
        sys.exit(1)


def make_amiibo(row_data):
    """ Map row_data to new django amiibo model object
    """
    item = Amiibo(
        title=row_data['Title'],
        upc=row_data['UPC'],
        donor=row_data['Donor'],
        notes=row_data['Notes'],
        plays=get_plays(row_data['Plys']),
        box=get_condition(row_data['Box']),
        figure=get_condition(row_data['Figure']))
    try:
        item.save()
        sys.stdout.write('Saved Amiibo: {0}\n'.format(item.title))
        sys.stdout.flush()
    except Exception as e:
        # dump values for debug on exception
        sys.stdout.write('row={0};\n{1}'.format(row_data, e))
        sys.exit(1)


def make_game(platform, row_data):
    """ Map row_data to new django game model object
    """
    item = Game(
        title =row_data['Title'],
        platform=platform,
        upc=row_data['UPC'],
        donor=row_data['Donor'],
        plays=get_plays(row_data['Plys']),
        media_cond=get_media_cond(platform, row_data),
        box=get_condition(row_data['Box']),
        manual=get_condition(row_data['Man']),
        insert=get_condition(row_data['Ins']))

    """ Assign platform specific fields """
    # Map green/black label(playstation) and pc media format data to Notes
    if platform in GREEN_LABELS:
        item.notes = 'Green label: {0}; {1}'.format(
            row_data['BL'], row_data['Notes'])
    elif platform == 'pc':
        # encode/strip functions called to handle special (fraction) characters
        item.notes = 'Media Type: {0}; Box Type: {1}; {2}'.format(
            row_data['M. Type'].encode('utf-8').strip(), row_data['B. Type'],
            row_data['Notes'].encode('utf-8').strip())
    else:
        item.notes = row_data['Notes']
    # Map 'DCvr' and 'Cover' to 'dust_cover'
    if platform in DUST_COVERS:
        item.dust_cover = get_condition(row_data['DCvr'])
    if platform in COVERS:
        item.dust_cover = get_condition(row_data['Cover'])
    # This value is only assigned on early nintendo platforms
    if platform in CUSTOM_BOXES:
        item.c_box = get_bool(row_data['CBox'])
    # Labels are only graded on cartridge based platforms,
    if platform in CARTS:
        item.label = get_condition(row_data['Label'])
    # but not all cartridge platforms have a column for batteries?
    if platform in BATTERIES:
        item.battery = get_cart_batt_cond(row_data['Bat'])

    try:
        item.save()
        sys.stdout.write('Saved Game: {0}; ({1})\n'.format(item.title, item.platform))
        sys.stdout.flush()
    except Exception as e:
        # dump values for debug on exception
        sys.stdout.write('key={0}; row={1};\n{2}'.format(platform, row_data, e))
        sys.exit(1)