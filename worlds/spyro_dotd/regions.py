from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Region
if TYPE_CHECKING:
    from .world import DotDWorld

def create_and_connect_regions(world: DotDWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: DotDWorld) -> None:
    regions = [
        Region("Menu", world.player, world.multiworld),
        Region("Catacombs", world.player, world.multiworld),
        Region("Twilight Falls", world.player, world.multiworld),
        Region("Valley of Avalar", world.player, world.multiworld),
        Region("Dragon City", world.player, world.multiworld),
        Region("Attack of the Golem", world.player, world.multiworld),
        Region("Ruins of Warfang", world.player, world.multiworld),
        Region("The Dam", world.player, world.multiworld),
        Region("The Destroyer", world.player, world.multiworld),
        Region("Burned Lands", world.player, world.multiworld),
        Region("Floating Islands", world.player, world.multiworld),
        Region("Malefor's Lair", world.player, world.multiworld),
    ]
    world.multiworld.regions += regions

def connect_regions(world: DotDWorld) -> None:
    player = world.player

    menu           = world.get_region("Menu")
    catacombs      = world.get_region("Catacombs")
    twilight_falls = world.get_region("Twilight Falls")
    valley         = world.get_region("Valley of Avalar")
    dragon_city    = world.get_region("Dragon City")
    golem          = world.get_region("Attack of the Golem")
    ruins          = world.get_region("Ruins of Warfang")
    the_dam        = world.get_region("The Dam")
    destroyer      = world.get_region("The Destroyer")
    burned_lands   = world.get_region("Burned Lands")
    floating       = world.get_region("Floating Islands")
    malefor        = world.get_region("Malefor's Lair")

    menu.connect(catacombs)  # always accessible, no key needed

    catacombs.connect(twilight_falls, "Catacombs to Twilight Falls",
        lambda state: state.has("Twilight Falls Key", player))
    twilight_falls.connect(valley, "Twilight Falls to Valley of Avalar",
        lambda state: state.has("Valley of Avalar Key", player))
    valley.connect(dragon_city, "Valley of Avalar to Dragon City",
        lambda state: state.has("Dragon City Key", player))
    dragon_city.connect(golem, "Dragon City to Attack of the Golem",
        lambda state: state.has("Attack of the Golem Key", player))
    golem.connect(ruins, "Attack of the Golem to Ruins of Warfang",
        lambda state: state.has("Ruins of Warfang Key", player))
    ruins.connect(the_dam, "Ruins of Warfang to The Dam",
        lambda state: state.has("The Dam Key", player))
    the_dam.connect(destroyer, "The Dam to The Destroyer",
        lambda state: state.has("The Destroyer Key", player))
    destroyer.connect(burned_lands, "The Destroyer to Burned Lands",
        lambda state: state.has("Burned Lands Key", player))
    burned_lands.connect(floating, "Burned Lands to Floating Islands",
        lambda state: state.has("Floating Islands Key", player))
    floating.connect(malefor, "Floating Islands to Malefor's Lair",
        lambda state: state.has("Malefor's Lair Key", player))