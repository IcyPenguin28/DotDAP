from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import DotDWorld


# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

# Lookup reference: 1-99: Blue Gem Clusters
#                   101-120: Health Gems
#                   201-220: Mana Gems
#                   301-308: Elite Enemies
#                   401-420: Armor Chests
LOCATION_NAME_TO_ID = {
    "Catacombs Blue Gem 1/10": 1,
    "Catacombs Blue Gem 2/10": 2,
    "Catacombs Blue Gem 3/10": 3,
    "Catacombs Blue Gem 4/10": 4,
    "Catacombs Blue Gem 5/10": 5,
    "Catacombs Blue Gem 6/10": 6,
    "Catacombs Blue Gem 7/10": 7,
    "Catacombs Blue Gem 8/10": 8,
    "Catacombs Blue Gem 9/10": 9,
    "Catacombs Blue Gem 10/10": 10,
    "Twilight Falls Blue Gem 1/7": 11,
    "Twilight Falls Blue Gem 2/7": 12,
    "Twilight Falls Blue Gem 3/7": 13,
    "Twilight Falls Blue Gem 4/7": 14,
    "Twilight Falls Blue Gem 5/7": 15,
    "Twilight Falls Blue Gem 6/7": 16,
    "Twilight Falls Blue Gem 7/7": 17,
    "Valley of Avalar Blue Gem 1/19": 18,
    "Valley of Avalar Blue Gem 2/19": 19,
    "Valley of Avalar Blue Gem 3/19": 20,
    "Valley of Avalar Blue Gem 4/19": 21,
    "Valley of Avalar Blue Gem 5/19": 22,
    "Valley of Avalar Blue Gem 6/19": 23,
    "Valley of Avalar Blue Gem 7/19": 24,
    "Valley of Avalar Blue Gem 8/19": 25,
    "Valley of Avalar Blue Gem 9/19": 26,
    "Valley of Avalar Blue Gem 10/19": 27,
    "Valley of Avalar Blue Gem 11/19": 28,
    "Valley of Avalar Blue Gem 12/19": 29,
    "Valley of Avalar Blue Gem 13/19": 30,
    "Valley of Avalar Blue Gem 14/19": 31,
    "Valley of Avalar Blue Gem 15/19": 32,
    "Valley of Avalar Blue Gem 16/19": 33,
    "Valley of Avalar Blue Gem 17/19": 34,
    "Valley of Avalar Blue Gem 18/19": 35,
    "Valley of Avalar Blue Gem 19/19": 36,
    "Dragon City Blue Gem 1/9": 37,
    "Dragon City Blue Gem 2/9": 38,
    "Dragon City Blue Gem 3/9": 39,
    "Dragon City Blue Gem 4/9": 40,
    "Dragon City Blue Gem 5/9": 41,
    "Dragon City Blue Gem 6/9": 42,
    "Dragon City Blue Gem 7/9": 43,
    "Dragon City Blue Gem 8/9": 44,
    "Dragon City Blue Gem 9/9": 45,
    "Ruins of Warfang Blue Gem 1/13": 46,
    "Ruins of Warfang Blue Gem 2/13": 47,
    "Ruins of Warfang Blue Gem 3/13": 48,
    "Ruins of Warfang Blue Gem 4/13": 49,
    "Ruins of Warfang Blue Gem 5/13": 50,
    "Ruins of Warfang Blue Gem 6/13": 51,
    "Ruins of Warfang Blue Gem 7/13": 52,
    "Ruins of Warfang Blue Gem 8/13": 53,
    "Ruins of Warfang Blue Gem 9/13": 54,
    "Ruins of Warfang Blue Gem 10/13": 55,
    "Ruins of Warfang Blue Gem 11/13": 56,
    "Ruins of Warfang Blue Gem 12/13": 57,
    "Ruins of Warfang Blue Gem 13/13": 58,
    "The Dam Blue Gem 1/5": 59,
    "The Dam Blue Gem 2/5": 60,
    "The Dam Blue Gem 3/5": 61,
    "The Dam Blue Gem 4/5": 62,
    "The Dam Blue Gem 5/5": 63,
    "The Destroyer Blue Gem 1/8": 64,
    "The Destroyer Blue Gem 2/8": 65,
    "The Destroyer Blue Gem 3/8": 66,
    "The Destroyer Blue Gem 4/8": 67,
    "The Destroyer Blue Gem 5/8": 68,
    "The Destroyer Blue Gem 6/8": 69,
    "The Destroyer Blue Gem 7/8": 70,
    "The Destroyer Blue Gem 8/8": 71,
    "Burned Lands Blue Gem 1/10": 72,
    "Burned Lands Blue Gem 2/10": 73,
    "Burned Lands Blue Gem 3/10": 74,
    "Burned Lands Blue Gem 4/10": 75,
    "Burned Lands Blue Gem 5/10": 76,
    "Burned Lands Blue Gem 6/10": 77,
    "Burned Lands Blue Gem 7/10": 78,
    "Burned Lands Blue Gem 8/10": 79,
    "Burned Lands Blue Gem 9/10": 80,
    "Burned Lands Blue Gem 10/10": 81,
    "Floating Islands Blue Gem 1/18": 82,
    "Floating Islands Blue Gem 2/18": 83,
    "Floating Islands Blue Gem 3/18": 84,
    "Floating Islands Blue Gem 4/18": 85,
    "Floating Islands Blue Gem 5/18": 86,
    "Floating Islands Blue Gem 6/18": 87,
    "Floating Islands Blue Gem 7/18": 88,
    "Floating Islands Blue Gem 8/18": 89,
    "Floating Islands Blue Gem 9/18": 90,
    "Floating Islands Blue Gem 10/18": 91,
    "Floating Islands Blue Gem 11/18": 92,
    "Floating Islands Blue Gem 12/18": 93,
    "Floating Islands Blue Gem 13/18": 94,
    "Floating Islands Blue Gem 14/18": 95,
    "Floating Islands Blue Gem 15/18": 96,
    "Floating Islands Blue Gem 16/18": 97,
    "Floating Islands Blue Gem 17/18": 98,
    "Floating Islands Blue Gem 18/18": 99,
    "Catacombs Health Gem 1/1": 101,
    "Twilight Falls Health Gem 1/1": 102,
    "Valley of Avalar Health Gem 1/3": 103,
    "Valley of Avalar Health Gem 2/3": 104,
    "Valley of Avalar Health Gem 3/3": 105,
    "Dragon City Health Gem 1/3": 106,
    "Dragon City Health Gem 2/3": 107,
    "Dragon City Health Gem 3/3": 108,
    "Attack of the Golem Health Gem 1/1": 109,
    "Ruins of Warfang Health Gem 1/3": 110,
    "Ruins of Warfang Health Gem 2/3": 111,
    "Ruins of Warfang Health Gem 3/3": 112,
    "The Dam Health Gem 1/2": 113,
    "The Dam Health Gem 2/2": 114,
    "The Destroyer Health Gem 1/2": 115,
    "The Destroyer Health Gem 2/2": 116,
    "Burned Lands Health Gem 1/2": 117,
    "Burned Lands Health Gem 2/2": 118,
    "Floating Islands Health Gem 1/2": 119,
    "Floating Islands Health Gem 2/2": 120,
    "Catacombs Mana Gem 1/1": 201,
    "Twilight Falls Mana Gem 1/2": 202,
    "Twilight Falls Mana Gem 2/2": 203,
    "Valley of Avalar Mana Gem 1/3": 204,
    "Valley of Avalar Mana Gem 2/3": 205,
    "Valley of Avalar Mana Gem 3/3": 206,
    "Dragon City Mana Gem 1/2": 207,
    "Dragon City Mana Gem 2/2": 208,
    "Attack of the Golem Mana Gem 1/1": 209,
    "Ruins of Warfang Mana Gem 1/3": 210,
    "Ruins of Warfang Mana Gem 2/3": 211,
    "Ruins of Warfang Mana Gem 3/3": 212,
    "The Dam Mana Gem 1/2": 213,
    "The Dam Mana Gem 2/2": 214,
    "The Destroyer Mana Gem 1/2": 215,
    "The Destroyer Mana Gem 2/2": 216,
    "Burned Lands Mana Gem 1/3": 217,
    "Burned Lands Mana Gem 2/3": 218,
    "Burned Lands Mana Gem 3/3": 219,
    "Floating Islands Mana Gem 1/1": 220,
    "Catacombs Elite Enemy 1/1": 301,
    "Twilight Falls Elite Enemy 1/1": 302,
    "Valley of Avalar Elite Enemy 1/1": 303,
    "Ruins of Warfang Elite Enemy 1/1": 304,
    "The Dam Elite Enemy 1/1": 305,
    "Burned Lands Elite Enemy 1/1": 306,
    "Floating Islands Elite Enemy 1/2": 307,
    "Floating Islands Elite Enemy 2/2": 308,
    "Twilight Falls Armor Chest 1/2": 401,
    "Twilight Falls Armor Chest 2/2": 402,
    "Valley of Avalar Armor Chest 1/4": 403,
    "Valley of Avalar Armor Chest 2/4": 404,
    "Valley of Avalar Armor Chest 3/4": 405,
    "Valley of Avalar Armor Chest 4/4": 406,
    "Dragon City Armor Chest 1/3": 407,
    "Dragon City Armor Chest 2/3": 408,
    "Dragon City Armor Chest 3/3": 409,
    "Attack of the Golem Armor Chest 1/1": 410,
    "Ruins of Warfang Armor Chest 1/2": 411,
    "Ruins of Warfang Armor Chest 2/2": 412,
    "The Dam Armor Chest 1/2": 413,
    "The Dam Armor Chest 2/2": 414,
    "The Destroyer Armor Chest 1/2": 415,
    "The Destroyer Armor Chest 2/2": 416,
    "Burned Lands Armor Chest 1/2": 417,
    "Burned Lands Armor Chest 2/2": 418,
    "Catacombs Cleared": 501,
    "Twilight Falls Cleared": 502,
    "Valley of Avalar Cleared": 503,
    "Dragon City Cleared": 504,
    "Attack of the Golem Cleared": 505,
    "Ruins of Warfang Cleared": 506,
    "The Dam Cleared": 507,
    "The Destroyer Cleared": 508,
    "Burned Lands Cleared": 509,
    "Floating Islands Cleared": 510
}

# If the flag at one of these addresses == 1, then the item at the location has been collected
LOCATION_FLAG_ADDRESS_TO_NAME = {
    0xa3edc4: "Catacombs Blue Gem 1/10",
    0xa3ee0c: "Catacombs Blue Gem 2/10",
    0xa3ee30: "Catacombs Blue Gem 3/10",
    0xa3ee54: "Catacombs Blue Gem 4/10",
    0xa3ee78: "Catacombs Blue Gem 5/10",
    0xa3ee9c: "Catacombs Blue Gem 6/10",
    0xa3eec0: "Catacombs Blue Gem 7/10",
    0xa3eee4: "Catacombs Blue Gem 8/10",
    0xa3ef2c: "Catacombs Blue Gem 9/10",
    0xa3ef50: "Catacombs Blue Gem 10/10",
    0xa3eb84: "Twilight Falls Blue Gem 1/7",
    0xa3ebcc: "Twilight Falls Blue Gem 2/7",
    0xa3ec5c: "Twilight Falls Blue Gem 3/7",
    0xa3ec80: "Twilight Falls Blue Gem 4/7",
    0xa3eca4: "Twilight Falls Blue Gem 5/7",
    0xa3ecc8: "Twilight Falls Blue Gem 6/7",
    0xa3ecec: "Twilight Falls Blue Gem 7/7",
    0xa3dc9c: "Valley of Avalar Blue Gem 1/19",
    0xa3dce4: "Valley of Avalar Blue Gem 2/19",
    0xa3dd50: "Valley of Avalar Blue Gem 3/19",
    0xa3de4c: "Valley of Avalar Blue Gem 4/19",
    0xa3de70: "Valley of Avalar Blue Gem 5/19",
    0xa3dedc: "Valley of Avalar Blue Gem 6/19",
    0xa3df00: "Valley of Avalar Blue Gem 7/19",
    0xa3df24: "Valley of Avalar Blue Gem 8/19",
    0xa3df48: "Valley of Avalar Blue Gem 9/19",
    0xa3df6c: "Valley of Avalar Blue Gem 10/19",
    0xa3df90: "Valley of Avalar Blue Gem 11/19",
    0xa3dfd8: "Valley of Avalar Blue Gem 12/19",
    0xa3dffc: "Valley of Avalar Blue Gem 13/19",
    0xa3e020: "Valley of Avalar Blue Gem 14/19",
    0xa3e08c: "Valley of Avalar Blue Gem 15/19",
    0xa3e284: "Valley of Avalar Blue Gem 16/19",
    0xa3eb60: "Valley of Avalar Blue Gem 17/19",
    0xa3ed34: "Valley of Avalar Blue Gem 18/19",
    0xa3ed58: "Valley of Avalar Blue Gem 19/19",
    0xa3e62c: "Dragon City Blue Gem 1/9",
    0xa3e698: "Dragon City Blue Gem 2/9",
    0xa3e6bc: "Dragon City Blue Gem 3/9",
    0xa3e74c: "Dragon City Blue Gem 4/9",
    0xa3e770: "Dragon City Blue Gem 5/9",
    0xa3e794: "Dragon City Blue Gem 6/9",
    0xa3e7b8: "Dragon City Blue Gem 7/9",
    0xa3e7dc: "Dragon City Blue Gem 8/9",
    0xa3e800: "Dragon City Blue Gem 9/9",
    0xa3e890: "Ruins of Warfang Blue Gem 1/13",
    0xa3e8b4: "Ruins of Warfang Blue Gem 2/13",
    0xa3e98c: "Ruins of Warfang Blue Gem 3/13",
    0xa3e9b0: "Ruins of Warfang Blue Gem 4/13",
    0xa3e9d4: "Ruins of Warfang Blue Gem 5/13",
    0xa3e9f8: "Ruins of Warfang Blue Gem 6/13",
    0xa3ea1c: "Ruins of Warfang Blue Gem 7/13",
    0xa3ea40: "Ruins of Warfang Blue Gem 8/13",
    0xa3ea64: "Ruins of Warfang Blue Gem 9/13",
    0xa3ea88: "Ruins of Warfang Blue Gem 10/13",
    0xa3eaac: "Ruins of Warfang Blue Gem 11/13",
    0xa3ead0: "Ruins of Warfang Blue Gem 12/13",
    0xa3eaf4: "Ruins of Warfang Blue Gem 13/13",
    0xa3e3a4: "The Dam Blue Gem 1/5",
    0xa3e3c8: "The Dam Blue Gem 2/5",
    0xa3e4c4: "The Dam Blue Gem 3/5",
    0xa3e4e8: "The Dam Blue Gem 4/5",
    0xa3e50c: "The Dam Blue Gem 5/5",
    0xa3e188: "The Destroyer Blue Gem 1/8",
    0xa3e1ac: "The Destroyer Blue Gem 2/8",
    0xa3e2a8: "The Destroyer Blue Gem 3/8",
    0xa3e2cc: "The Destroyer Blue Gem 4/8",
    0xa3e314: "The Destroyer Blue Gem 5/8",
    0xa3e338: "The Destroyer Blue Gem 6/8",
    0xa3e35c: "The Destroyer Blue Gem 7/8",
    0xa3e380: "The Destroyer Blue Gem 8/8",
    0xa3e140: "Burned Lands Blue Gem 1/10",
    0xa3ed7c: "Burned Lands Blue Gem 2/10",
    0xa3ef74: "Burned Lands Blue Gem 3/10",
    0xa3ef98: "Burned Lands Blue Gem 4/10",
    0xa3efbc: "Burned Lands Blue Gem 5/10",
    0xa3efe0: "Burned Lands Blue Gem 6/10",
    0xa3f004: "Burned Lands Blue Gem 7/10",
    0xa3f028: "Burned Lands Blue Gem 8/10",
    0xa3f04c: "Burned Lands Blue Gem 9/10",
    0xa3f094: "Burned Lands Blue Gem 10/10",
    0xa3d9cc: "Floating Islands Blue Gem 1/18",
    0xa3d9f0: "Floating Islands Blue Gem 2/18",
    0xa3da14: "Floating Islands Blue Gem 3/18",
    0xa3da5c: "Floating Islands Blue Gem 4/18",
    0xa3daa4: "Floating Islands Blue Gem 5/18",
    0xa3dac8: "Floating Islands Blue Gem 6/18",
    0xa3db10: "Floating Islands Blue Gem 7/18",
    0xa3db34: "Floating Islands Blue Gem 8/18",
    0xa3db58: "Floating Islands Blue Gem 9/18",
    0xa3dba0: "Floating Islands Blue Gem 10/18",
    0xa3dbc4: "Floating Islands Blue Gem 11/18",
    0xa3dbe8: "Floating Islands Blue Gem 12/18",
    0xa3dc0c: "Floating Islands Blue Gem 13/18",
    0xa3dc30: "Floating Islands Blue Gem 14/18",
    0xa3dcc0: "Floating Islands Blue Gem 15/18",
    0xa3df90: "Floating Islands Blue Gem 16/18",
    0xa3e0d4: "Floating Islands Blue Gem 17/18",
    0xa3e0f8: "Floating Islands Blue Gem 18/18",
    0xa3eda0: "Catacombs Health Gem 1/1",
    0xa3ec38: "Twilight Falls Health Gem 1/1",
    0xa3dd08: "Valley of Avalar Health Gem 1/3",
    0xa3dd2c: "Valley of Avalar Health Gem 2/3",
    0xa3dd74: "Valley of Avalar Health Gem 3/3",
    0xa3e5e4: "Dragon City Health Gem 1/3",
    0xa3e608: "Dragon City Health Gem 2/3",
    0xa3e6e0: "Dragon City Health Gem 3/3",
    0xa3e59c: "Attack of the Golem Health Gem 1/1",
    0xa3e8d8: "Ruins of Warfang Health Gem 1/3",
    0xa3e944: "Ruins of Warfang Health Gem 2/3",
    0xa3e968: "Ruins of Warfang Health Gem 3/3",
    0xa3e3ec: "The Dam Health Gem 1/2",
    0xa3e458: "The Dam Health Gem 2/2",
    0xa3e11c: "The Destroyer Health Gem 1/2",
    0xa3e1d0: "The Destroyer Health Gem 2/2",
    0xa3e068: "Burned Lands Health Gem 1/2",
    0xa3e260: "Burned Lands Health Gem 2/2",
    0xa3da38: "Floating Islands Health Gem 1/2",
    0xa3da80: "Floating Islands Health Gem 2/2",
    0xa3ede8: "Catacombs Mana Gem 1/1",
    0xa3ebf0: "Twilight Falls Mana Gem 1/2",
    0xa3ec14: "Twilight Falls Mana Gem 2/2",
    0xa3de04: "Valley of Avalar Mana Gem 1/3",
    0xa3de94: "Valley of Avalar Mana Gem 2/3",
    0xa3deb8: "Valley of Avalar Mana Gem 3/3",
    0xa3e5c0: "Dragon City Mana Gem 1/2",
    0xa3e704: "Dragon City Mana Gem 2/2",
    0xa3e578: "Attack of the Golem Mana Gem 1/1",
    0xa3e86c: "Ruins of Warfang Mana Gem 1/3",
    0xa3e8fc: "Ruins of Warfang Mana Gem 2/3",
    0xa3e920: "Ruins of Warfang Mana Gem 3/3",
    0xa3e410: "The Dam Mana Gem 1/2",
    0xa3e434: "The Dam Mana Gem 2/2",
    0xa3e164: "The Destroyer Mana Gem 1/2",
    0xa3e2f0: "The Destroyer Mana Gem 2/2",
    0xa3e044: "Burned Lands Mana Gem 1/3",
    0xa3eba8: "Burned Lands Mana Gem 2/3",
    0xa3f0dc: "Burned Lands Mana Gem 3/3",
    0xa3daec: "Floating Islands Mana Gem 1/1",
    0xa3ef08: "Catacombs Elite Enemy 1/1",
    0xa3ed10: "Twilight Falls Elite Enemy 1/1",
    0xa3e0b0: "Valley of Avalar Elite Enemy 1/1",
    0xa3eb18: "Ruins of Warfang Elite Enemy 1/1",
    0xa3e530: "The Dam Elite Enemy 1/1",
    0xa3e23c: "Burned Lands Elite Enemy 1/1",
    0xa3db7c: "Floating Islands Elite Enemy 1/2",
    0xa3dc54: "Floating Islands Elite Enemy 2/2",
    0xa3dc78: "Twilight Falls Armor Chest 1/2",
    0xa3eb3c: "Twilight Falls Armor Chest 2/2",
    0xa3dd98: "Valley of Avalar Armor Chest 1/4",
    0xa3ddbc: "Valley of Avalar Armor Chest 2/4",
    0xa3dde0: "Valley of Avalar Armor Chest 3/4",
    0xa3de28: "Valley of Avalar Armor Chest 4/4",
    0xa3e650: "Dragon City Armor Chest 1/3",
    0xa3e674: "Dragon City Armor Chest 2/3",
    0xa3e728: "Dragon City Armor Chest 3/3",
    0xa3e554: "Attack of the Golem Armor Chest 1/1",
    0xa3e824: "Ruins of Warfang Armor Chest 1/2",
    0xa3e848: "Ruins of Warfang Armor Chest 2/2",
    0xa3e47c: "The Dam Armor Chest 1/2",
    0xa3e4a0: "The Dam Armor Chest 2/2",
    0xa3e1f4: "The Destroyer Armor Chest 1/2",
    0xa3e218: "The Destroyer Armor Chest 2/2",
    0xa3f070: "Burned Lands Armor Chest 1/2",
    0xa3f0b8: "Burned Lands Armor Chest 2/2",
    0x9fecd3: "Catacombs Cleared",
    0x9fecd4: "Twilight Falls Cleared",
    0x9fecd5: "Valley of Avalar Cleared",
    0x9fecd6: "Dragon City Cleared",
    0x9fecd7: "Attack of the Golem Cleared",
    0x9fecd8: "Ruins of Warfang Cleared",
    0x9fecda: "The Dam Cleared",
    0x9fecdb: "The Destroyer Cleared",
    0x9fecdc: "Burned Lands Cleared",
    0x9fecdd: "Floating Islands Cleared",
}

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class DotDLocation(Location):
    game = "The Legend of Spyro: Dawn of the Dragon"

# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Soem functions want location addresses to be an "int | None",
# so, while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: DotDWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: DotDWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    catacombs = world.get_region("Catacombs")
    twilight_falls = world.get_region("Twilight Falls")
    valley_of_avalar = world.get_region("Valley of Avalar")
    dragon_city = world.get_region("Dragon City")
    attack_of_the_golem = world.get_region("Attack of the Golem")
    ruins_of_warfang = world.get_region("Ruins of Warfang")
    the_dam = world.get_region("The Dam")
    the_destroyer = world.get_region("The Destroyer")
    burned_lands = world.get_region("Burned Lands")
    floating_islands = world.get_region("Floating Islands")
    malefors_lair = world.get_region("Malefor's Lair")

    # We can add locations to region by simply using the region.add_locations_helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also ened to pass your overridden Location class.
    catacombs_locations = get_location_names_with_ids(
        [
            "Catacombs Blue Gem 1/10",
            "Catacombs Blue Gem 2/10",
            "Catacombs Blue Gem 3/10",
            "Catacombs Blue Gem 4/10",
            "Catacombs Blue Gem 5/10",
            "Catacombs Blue Gem 6/10",
            "Catacombs Blue Gem 7/10",
            "Catacombs Blue Gem 8/10",
            "Catacombs Blue Gem 9/10",
            "Catacombs Blue Gem 10/10",
            "Catacombs Health Gem 1/1",
            "Catacombs Mana Gem 1/1",
            "Catacombs Elite Enemy 1/1",
            "Catacombs Cleared"
        ]
    )

    twilight_falls_locations = get_location_names_with_ids(
        [
            "Twilight Falls Blue Gem 1/7",
            "Twilight Falls Blue Gem 2/7",
            "Twilight Falls Blue Gem 3/7",
            "Twilight Falls Blue Gem 4/7",
            "Twilight Falls Blue Gem 5/7",
            "Twilight Falls Blue Gem 6/7",
            "Twilight Falls Blue Gem 7/7",
            "Twilight Falls Health Gem 1/1",
            "Twilight Falls Mana Gem 1/2",
            "Twilight Falls Mana Gem 2/2",
            "Twilight Falls Elite Enemy 1/1",
            "Twilight Falls Armor Chest 1/2",
            "Twilight Falls Armor Chest 2/2",
            "Twilight Falls Cleared"
        ]
    )

    valley_of_avalar_locations = get_location_names_with_ids(
        [
            "Valley of Avalar Blue Gem 1/19",
            "Valley of Avalar Blue Gem 2/19",
            "Valley of Avalar Blue Gem 3/19",
            "Valley of Avalar Blue Gem 4/19",
            "Valley of Avalar Blue Gem 5/19",
            "Valley of Avalar Blue Gem 6/19",
            "Valley of Avalar Blue Gem 7/19",
            "Valley of Avalar Blue Gem 8/19",
            "Valley of Avalar Blue Gem 9/19",
            "Valley of Avalar Blue Gem 10/19",
            "Valley of Avalar Blue Gem 11/19",
            "Valley of Avalar Blue Gem 12/19",
            "Valley of Avalar Blue Gem 13/19",
            "Valley of Avalar Blue Gem 14/19",
            "Valley of Avalar Blue Gem 15/19",
            "Valley of Avalar Blue Gem 16/19",
            "Valley of Avalar Blue Gem 17/19",
            "Valley of Avalar Blue Gem 18/19",
            "Valley of Avalar Blue Gem 19/19",
            "Valley of Avalar Health Gem 1/3",
            "Valley of Avalar Health Gem 2/3",
            "Valley of Avalar Health Gem 3/3",
            "Valley of Avalar Mana Gem 1/3",
            "Valley of Avalar Mana Gem 2/3",
            "Valley of Avalar Mana Gem 3/3",
            "Valley of Avalar Elite Enemy 1/1",
            "Valley of Avalar Armor Chest 1/4",
            "Valley of Avalar Armor Chest 2/4",
            "Valley of Avalar Armor Chest 3/4",
            "Valley of Avalar Armor Chest 4/4",
            "Valley of Avalar Cleared"
        ]
    )

    dragon_city_locations = get_location_names_with_ids(
        [
            "Dragon City Blue Gem 1/9",
            "Dragon City Blue Gem 2/9",
            "Dragon City Blue Gem 3/9",
            "Dragon City Blue Gem 4/9",
            "Dragon City Blue Gem 5/9",
            "Dragon City Blue Gem 6/9",
            "Dragon City Blue Gem 7/9",
            "Dragon City Blue Gem 8/9",
            "Dragon City Blue Gem 9/9",
            "Dragon City Health Gem 1/3",
            "Dragon City Health Gem 2/3",
            "Dragon City Health Gem 3/3",
            "Dragon City Mana Gem 1/2",
            "Dragon City Mana Gem 2/2",
            "Dragon City Armor Chest 1/3",
            "Dragon City Armor Chest 2/3",
            "Dragon City Armor Chest 3/3",
            "Dragon City Cleared"
        ]
    )

    attack_of_the_golem_locations = get_location_names_with_ids(
        [
            "Attack of the Golem Health Gem 1/1",
            "Attack of the Golem Mana Gem 1/1",
            "Attack of the Golem Armor Chest 1/1",
            "Attack of the Golem Cleared"
        ]
    )

    ruins_of_warfang_locations = get_location_names_with_ids(
        [
            "Ruins of Warfang Blue Gem 1/13",
            "Ruins of Warfang Blue Gem 2/13",
            "Ruins of Warfang Blue Gem 3/13",
            "Ruins of Warfang Blue Gem 4/13",
            "Ruins of Warfang Blue Gem 5/13",
            "Ruins of Warfang Blue Gem 6/13",
            "Ruins of Warfang Blue Gem 7/13",
            "Ruins of Warfang Blue Gem 8/13",
            "Ruins of Warfang Blue Gem 9/13",
            "Ruins of Warfang Blue Gem 10/13",
            "Ruins of Warfang Blue Gem 11/13",
            "Ruins of Warfang Blue Gem 12/13",
            "Ruins of Warfang Blue Gem 13/13",
            "Ruins of Warfang Health Gem 1/3",
            "Ruins of Warfang Health Gem 2/3",
            "Ruins of Warfang Health Gem 3/3",
            "Ruins of Warfang Mana Gem 1/3",
            "Ruins of Warfang Mana Gem 2/3",
            "Ruins of Warfang Mana Gem 3/3",
            "Ruins of Warfang Elite Enemy 1/1",
            "Ruins of Warfang Armor Chest 1/2",
            "Ruins of Warfang Armor Chest 2/2",
            "Ruins of Warfang Cleared"
        ]
    )

    the_dam_locations = get_location_names_with_ids(
        [
            "The Dam Blue Gem 1/5",
            "The Dam Blue Gem 2/5",
            "The Dam Blue Gem 3/5",
            "The Dam Blue Gem 4/5",
            "The Dam Blue Gem 5/5",
            "The Dam Health Gem 1/2",
            "The Dam Health Gem 2/2",
            "The Dam Mana Gem 1/2",
            "The Dam Mana Gem 2/2",
            "The Dam Elite Enemy 1/1",
            "The Dam Armor Chest 1/2",
            "The Dam Armor Chest 2/2",
            "The Dam Cleared"
        ]
    )

    the_destroyer_locations = get_location_names_with_ids(
        [
            "The Destroyer Blue Gem 1/8",
            "The Destroyer Blue Gem 2/8",
            "The Destroyer Blue Gem 3/8",
            "The Destroyer Blue Gem 4/8",
            "The Destroyer Blue Gem 5/8",
            "The Destroyer Blue Gem 6/8",
            "The Destroyer Blue Gem 7/8",
            "The Destroyer Blue Gem 8/8",
            "The Destroyer Health Gem 1/2",
            "The Destroyer Health Gem 2/2",
            "The Destroyer Mana Gem 1/2",
            "The Destroyer Mana Gem 2/2",
            "The Destroyer Armor Chest 1/2",
            "The Destroyer Armor Chest 2/2",
            "The Destroyer Cleared"
        ]
    )

    burned_lands_locations = get_location_names_with_ids(
        [
            "Burned Lands Blue Gem 1/10",
            "Burned Lands Blue Gem 2/10",
            "Burned Lands Blue Gem 3/10",
            "Burned Lands Blue Gem 4/10",
            "Burned Lands Blue Gem 5/10",
            "Burned Lands Blue Gem 6/10",
            "Burned Lands Blue Gem 7/10",
            "Burned Lands Blue Gem 8/10",
            "Burned Lands Blue Gem 9/10",
            "Burned Lands Blue Gem 10/10",
            "Burned Lands Health Gem 1/2",
            "Burned Lands Health Gem 2/2",
            "Burned Lands Mana Gem 1/3",
            "Burned Lands Mana Gem 2/3",
            "Burned Lands Mana Gem 3/3",
            "Burned Lands Elite Enemy 1/1",
            "Burned Lands Armor Chest 1/2",
            "Burned Lands Armor Chest 2/2",
            "Burned Lands Cleared"
        ]
    )

    floating_islands_locations = get_location_names_with_ids(
        [
            "Floating Islands Blue Gem 1/18",
            "Floating Islands Blue Gem 2/18",
            "Floating Islands Blue Gem 3/18",
            "Floating Islands Blue Gem 4/18",
            "Floating Islands Blue Gem 5/18",
            "Floating Islands Blue Gem 6/18",
            "Floating Islands Blue Gem 7/18",
            "Floating Islands Blue Gem 8/18",
            "Floating Islands Blue Gem 9/18",
            "Floating Islands Blue Gem 10/18",
            "Floating Islands Blue Gem 11/18",
            "Floating Islands Blue Gem 12/18",
            "Floating Islands Blue Gem 13/18",
            "Floating Islands Blue Gem 14/18",
            "Floating Islands Blue Gem 15/18",
            "Floating Islands Blue Gem 16/18",
            "Floating Islands Blue Gem 17/18",
            "Floating Islands Blue Gem 18/18",
            "Floating Islands Health Gem 1/2",
            "Floating Islands Health Gem 2/2",
            "Floating Islands Mana Gem 1/1",
            "Floating Islands Elite Enemy 1/2",
            "Floating Islands Elite Enemy 2/2",
            "Floating Islands Cleared"
        ]
    )

    catacombs.add_locations(catacombs_locations, DotDLocation)
    twilight_falls.add_locations(twilight_falls_locations, DotDLocation)
    valley_of_avalar.add_locations(valley_of_avalar_locations, DotDLocation)
    dragon_city.add_locations(dragon_city_locations, DotDLocation)
    attack_of_the_golem.add_locations(attack_of_the_golem_locations, DotDLocation)
    ruins_of_warfang.add_locations(ruins_of_warfang_locations, DotDLocation)
    the_dam.add_locations(the_dam_locations, DotDLocation)
    the_destroyer.add_locations(the_destroyer_locations, DotDLocation)
    burned_lands.add_locations(burned_lands_locations, DotDLocation)
    floating_islands.add_locations(floating_islands_locations, DotDLocation)

def create_events(world: DotDWorld):
    # NOTE: Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    pass