# The Legend of Spyro: Dawn of the Dragon - Archipelago Client

An Archipelago integration for *The Legend of Spyro: Dawn of the Dragon* (PS2, NTSC-U), allowing item randomization and multiworld support via the PCSX2 emulator.

---

## Item Pool & Locations
### Items
* **Blue Gem Cluster**: +1000 EXP to both Spyro and Cynder (99, Useful)
* **Red Life Crystal**: +1 Red Life Crystal to both Spyro and Cynder, increasing max HP with enough collected (20, Useful)
* **Green Magic Crystal**: +1 Green Magic Crystal to both Spyro and Cynder, increasing max Mana with enough collected (20, Useful)
* **[Spyro | Cynder] [Helmet | Bracers | Tail] [Silver | Gold | Fury]**: Grants the specified piece of armor (18, Useful)
* **Health Gem S**: Any player-controlled dragon(s) recover 15 HP (Filler)
* **Mana Gem S**: Any player-controlled dragon(s) recover 15 Mana (Filler)
* **Progressive Chapter Unlock**: Grants access to the next chapter in the list, be it vanilla or shuffled (10, Progression)
### Locations
* **All 99 Blue Gem Clusters**
* **All 20 Health Gems**
* **All 20 Mana Gems**
* **All 18 Armor Chests**
* **All 8 Elite Enemies**
* **All 10 Chapter Clears (excluding Malefor's Lair)**
* **Gallery Unlocks**
  * Scenery Gallery Unlock
  * Alliance Gallery Unlock
* **Objectives**
  * Reach the Enchanted Forest
  * Save the Cheetah Village
  * Find Meadow
  * Find the Hermit
  * Find the Supply Cave
  * Find the Raft
  * Bring the Raft to Meadow
  * Extinguish the Fire
  * Fill the Pool with Water
  * Find a Bucket
  * Protect the Catapult
  * Destroy the Siege Tower (first)
  * Escort the Artillery Mole to the Catapult
  * Destroy the Siege Tower (second)
  * Destroy the last two Siege Towers
  * Close the City Gates
  * Open the Gates to the Ruins of Warfang
  * Open the Floodgates to the Dam
  * Open the Main Floodgate
  * Destroy all the crystals of the Destroyer
  * Reach the Volcano
  * Torches Lit 8/8

### Goal Check
Defeat Malefor!

## Options
* **Death Link**: If another player in the multiworld dies, Spyro and Cynder instantly die.
* **Shuffle Chapter Order**: Chapters are unlocked in a random order with the exception of Malefor's Lair which is always unlocked last.
* **Learn Fury**: One or both dragons cannot build the fury bar until it is enabled via an item. Use of fury breath via the Fury Armor's Set Bonus remains unaffected. Fury is required to pass phase 3 of the Malefor final boss fight.

---

## Requirements

* **[Archipelago 0.6.7+](https://github.com/ArchipelagoMW/Archipelago/releases)**
* **[PCSX2](https://pcsx2.net/downloads)**
* PINE enabled in PCSX2
* NTSC-U version of the game

  * Game ID: `SLUS-21820`
  * This is important because this implementation reads from and writes to certain memory addresses that may differ between international versions

---

## Installation
Download the latest release from GitHub and pick _one_ of the following methods below:
1. Double-click the .apworld file
2. Use `ArchipelagoLauncher.exe` and click Install APWorld
3. Place `spyro_dotd.apworld` into your Archipelago `custom_worlds` folder

#### After completing one of these three methods, it may be wise to close and re-open any Archipelago windows to ensure the world is able to be recognized by Archipelago.


---

## Setup (PCSX2)

1. Open PCSX2
2. Go to Settings, then Advanced
3. Enable PINE
4. Ensure that the slot is the default of 28011
5. Launch the game
6. Start the Archipelago client

#### This setup guide assumes you already have the ability to play The Legend of Spyro: Dawn of the Dragon on PCSX2.
#### For additional assistance in ripping your own PS2 games, please see [PCSX2's Disc Dumping Guide](https://pcsx2.net/docs/setup/discs/)
---

## Known Issues

* **Blue Gem EXP duplication on reconnect**: 
  Reconnecting to the server may reapply EXP from Blue Gems.
  This can result in higher-than-intended EXP totals but does not break progression.
* **Health Gem S/Mana Gem S items can briefly allow a dragon's current HP/Mana to exceed their max HP/Mana**
  This is a byproduct of how the game internally handles max HP/Mana. A fix is possible but is not a high priority at the moment because the weakest enemies deal 20 damage and these filler items recover 15.

* Additional bugs may exist, as this is a very early release

---

## Troubleshooting
### Before attempting to troubleshoot, please look for your issue in the "Known Issues" section of this document

### Client does not connect to PCSX2

* Ensure PINE is enabled
* Make sure PCSX2 is running before the client

### Game version check fails

* Verify you are using the NTSC-U version (`SLUS-21820`)

### Nothing is happening in-game

* Confirm the client is connected to both:

  * Archipelago server
  * PCSX2

### The game says I have enough (4-5) Red Life Crystals/Green Magic Crystals when I've received zero so far!
* This is simply a quirk of the UI. It perceives zero as having a full bar of these crystals.

### I got 1000 EXP from a blue gem cluster! Shouldn't that have been cancelled out?
* As of the latest update, blue gem clusters now internally give 0 EXP when collected.
* If this did not fix the EXP value, then it is likely through failing to save in-game that blue gem clusters already marked as checked by the Archipelago server have respawned. Please make sure you consistently save your progress to prevent such desyncs from happening.

---

## Credits

* Primary Contributor: IcyPenguin_
* Consulting and Debugging: Uroogla, Dragonsoul5000
* Special thanks to EVZone on RetroAchievements for finding most relevant memory addresses

---

## Feedback

If you encounter issues or bugs, please open an issue on GitHub or ping `@IcyPenguin_` in the Dawn of the Dragon thread in the Archipelago Discord server.
