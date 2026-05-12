from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Region
if TYPE_CHECKING:
    from .world import DotDWorld

SHUFFLEABLE_CHAPTERS = [
    "Twilight Falls", "Valley of Avalar", "Dragon City",
    "Attack of the Golem", "Ruins of Warfang", "The Dam",
    "The Destroyer", "Burned Lands", "Floating Islands"
]

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

    if world.options.shuffle_chapter_order:
        shuffled_middle = list(SHUFFLEABLE_CHAPTERS)
        world.random.shuffle(shuffled_middle)
    else:
        shuffled_middle = list(SHUFFLEABLE_CHAPTERS)

    # Catacombs is always first, Malefor's Lair always last
    world.chapter_order = ["Catacombs"] + shuffled_middle

    menu       = world.get_region("Menu")
    catacombs  = world.get_region("Catacombs")
    malefor    = world.get_region("Malefor's Lair")
    middle     = [world.get_region(name) for name in shuffled_middle]

    menu.connect(catacombs)  # always free
    
    catacombs.connect(middle[0], "Catacombs to Chapter 2",
        lambda state: state.count("Progressive Chapter Unlock", player) >= 1)

    for i, region in enumerate(middle):
        next_region = middle[i + 1] if i + 1 < len(middle) else malefor
        required = i + 2  # +2 because catacombs consumed unlock #1
        def make_rule(n):
            return lambda state: state.count("Progressive Chapter Unlock", player) >= n
        region.connect(next_region, f"Chapter {i + 2} to Chapter {i + 3}", make_rule(required))