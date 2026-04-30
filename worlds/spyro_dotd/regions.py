from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import DotDWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).

def create_and_connect_regions(world: DotDWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: DotDWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    # TODO: Add VoA Hermit Cave + Waterfall Cave?
    # TODO: Separate Dragon City with Dragon City Ramparts
    # TODO: Separate sections of RoW(?)
    # TODO: Separate Upper Destroyer from Lower Destroyer(?)
    catacombs = Region("Catacombs", world.player, world.multiworld)
    twilight_falls = Region("Twilight Falls", world.player, world.multiworld)
    valley_of_avalar = Region("Valley of Avalar", world.player, world.multiworld)
    dragon_city = Region("Dragon City", world.player, world.multiworld)
    attack_of_the_golem = Region("Attack of the Golem", world.player, world.multiworld)
    ruins_of_warfang = Region("Ruins of Warfang", world.player, world.multiworld)
    the_dam = Region("The Dam", world.player, world.multiworld)
    the_destroyer = Region("The Destroyer", world.player, world.multiworld)
    burned_lands = Region("Burned Lands", world.player, world.multiworld)
    floating_islands = Region("Floating Islands", world.player, world.multiworld)
    malefors_lair = Region("Malefor's Lair", world.player, world.multiworld)

    # Let's put all these regions in a list
    regions = [
        catacombs,
        twilight_falls,
        valley_of_avalar,
        dragon_city,
        attack_of_the_golem,
        ruins_of_warfang,
        the_dam,
        the_destroyer,
        burned_lands,
        floating_islands,
        malefors_lair
    ]

    # NOTE: Some regions may only exist if the player enables certain options

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions

def connect_regions(world: DotDWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
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

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # We can use the region.connect helper
    catacombs.connect(twilight_falls, "Chapter 1 to 2")
    twilight_falls.connect(valley_of_avalar, "Chapter 2 to 3")
    valley_of_avalar.connect(dragon_city, "Chapter 3 to 4")
    dragon_city.connect(attack_of_the_golem, "Chapter 4 to 5")
    attack_of_the_golem.connect(ruins_of_warfang, "Chapter 5 to 6")
    ruins_of_warfang.connect(the_dam, "Chapter 6 to 7")
    the_dam.connect(the_destroyer, "Chapter 7 to 8")
    the_destroyer.connect(burned_lands, "Chapter 8 to 9")
    burned_lands.connect(floating_islands, "Chapter 9 to 10")
    floating_islands.connect(malefors_lair, "Chapter 10 to 11")

    # NOTE: The region.connect helper even allows adding a rule immediately
    # NOTE: Some Entrances may only exist if the player enables certain options