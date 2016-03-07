# filter tables that have green/black label columns.
GREEN_LABELS = ['psx', 'ps2', 'ps3']

# these two lists use two separate column headings to represent essentially the same data,
# the value will be mapped to 'dust_cover' in the django db.
DUST_COVERS = ['nes', 'snes', 'gameboy', 'gameboy-color', 'gamegear']
COVERS = ['gamecube', 'wii', 'nintendo-ds', 'nintendo-3ds', 'sega-cd', 'sega-saturn', 'dreamcast', 'xbox', 'xbox-360', 'xbox-one', 'psx', 'ps2', 'ps3', 'ps4', 'psp', 'pc']

# filter tables that have a C_Box column.
CUSTOM_BOXES = ['nes', 'snes', 'n64', 'gameboy', 'gameboy-color', 'gameboy-adv']

# filter tables that use the 'Bat' column header.
BATTERIES = ['nes', 'snes', 'n64', 'gameboy', 'gameboy-color', 'gameboy-adv', 'sega-master-system', 'sega-genesis', 'sega-32x', 'gamegear', 'neo-geo-aes', 'neo-geo-mvs', 'neo-geo-cd', 'neo-geo-pocket']

# these two lists use two separate column headings to represent essentially the same data,
# the value will be mapped to 'media_cond' in the django db.
## NOTE: CARTS is also used to filter for tables that use the 'Labels' column header
CARTS = ['nes', 'snes', 'n64', 'gameboy', 'gameboy-color', 'gameboy-adv', 'nintendo-ds', 'nintendo-3ds', 'sega-master-system', 'sega-genesis', 'sega-32x', 'gamegear', 'ps-vita', 'neo-geo-aes', 'neo-geo-mvs', 'neo-geo-cd', 'neo-geo-pocket']
DISCS = ["gamecube", "wii", "wii-u", "sega-cd", "sega-saturn", "dreamcast", "xbox", "xbox-360", "xbox-one", "psx", "ps2", "ps3", "ps4"]