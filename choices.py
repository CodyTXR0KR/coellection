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
from django.utils.translation import ugettext_lazy as _

PLAYS_CHOICES = (
    (0, _("No")),
    (1, _("Yes")),
    (2, _("Untested")),
)

CONDITION_CHOICES = (
    (0, _("N/A")),
    (1, _("Missing")),
    (2, _("Awful")),
    (3, _("Poor")),
    (4, _("Fine")),
    (5, _("Good")),
    (6, _("Mint")),
    (7, _("New")),
)

CART_BATT_CHOICES = (
    (0, _("None")),
    (1, _("Bad")),
    (2, _("Good")),
)

PLATFORM_CHOICES = (
    ('nes', _('NES')),
    ('snes', _('SNES')),
    ('n64', _('N64')),
    ('gamecube', _('GameCube')),
    ('wii', _('Wii')),
    ('wii-u', _('Wii U')),
    ('gameboy', _('GameBoy')),
    ('gameboy-color', _('GameBoy Color')),
    ('gameboy-adv', _('GameBoy Advance')),
    ('nintendo-ds', _('DS')),
    ('nintendo-3ds', _('3DS')),
    ('sega-master-system', _('Sega Master Sys')),
    ('sega-genesis', _('Sega Genesis')),
    ('sega-cd', _('Sega CD')),
    ('sega-32x', _('Sega 32x')),
    ('sega-saturn', _('Sega Saturn')),
    ('dreamcast', _('Dreamcast')),
    ('gamegear', _('GameGear')),
    ('xbox', _('Xbox')),
    ('xbox-360', _('Xbox 360')),
    ('xbox-one', _('Xbox One')),
    ('psx', _('Playstation 1')),
    ('ps2', _('Playstation 2')),
    ('ps3', _('Playstation 3')),
    ('ps4', _('Playstation 4')),
    ('psp', _('PSP')),
    ('ps-vita', _('PS Vita')),
    ('neo-geo-aes', _('NeoGeo AES')),
    ('neo-geo-mvs', _('NeoGeo MVS')),
    ('neo-geo-cd', _('NeoGeo CD')),
    ('neo-geo-pocket', _('NeoGeo Pocket')),
    ('pc', _('PC')),
)