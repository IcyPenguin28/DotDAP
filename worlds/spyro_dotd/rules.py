from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import DotDWorld


def set_all_rules(world: DotDWorld) -> None:
    set_all_location_rules(world)
    # TODO: set_completion_condition(world)


def set_all_location_rules(world: DotDWorld) -> None:
    cbg1 = world.get_location("Catacombs Blue Gem 1/10")
    cbg2 = world.get_location("Catacombs Blue Gem 2/10")
    cbg3 = world.get_location("Catacombs Blue Gem 3/10")
    cbg4 = world.get_location("Catacombs Blue Gem 4/10")
    cbg5 = world.get_location("Catacombs Blue Gem 5/10")
    cbg6 = world.get_location("Catacombs Blue Gem 6/10")
    cbg7 = world.get_location("Catacombs Blue Gem 7/10")
    cbg8 = world.get_location("Catacombs Blue Gem 8/10")
    cbg9 = world.get_location("Catacombs Blue Gem 9/10")
    cbg10 = world.get_location("Catacombs Blue Gem 10/10")
    chg1 = world.get_location("Catacombs Health Gem 1/1")
    cmg1 = world.get_location("Catacombs Mana Gem 1/1")
    cee1 = world.get_location("Catacombs Elite Enemy 1/1")
    tfbg1 = world.get_location("Twilight Falls Blue Gem 1/7")
    tfbg2 = world.get_location("Twilight Falls Blue Gem 2/7")
    tfbg3 = world.get_location("Twilight Falls Blue Gem 3/7")
    tfbg4 = world.get_location("Twilight Falls Blue Gem 4/7")
    tfbg5 = world.get_location("Twilight Falls Blue Gem 5/7")
    tfbg6 = world.get_location("Twilight Falls Blue Gem 6/7")
    tfbg7 = world.get_location("Twilight Falls Blue Gem 7/7")
    tfhg1 = world.get_location("Twilight Falls Health Gem 1/1")
    tfmg1 = world.get_location("Twilight Falls Mana Gem 1/2")
    tfmg2 = world.get_location("Twilight Falls Mana Gem 2/2")
    tfee1 = world.get_location("Twilight Falls Elite Enemy 1/1")
    tfac1 = world.get_location("Twilight Falls Armor Chest 1/2")
    tfac2 = world.get_location("Twilight Falls Armor Chest 2/2")

    # TODO: if world.options.learn_to_fly:
