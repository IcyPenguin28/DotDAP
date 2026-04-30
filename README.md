# The Legend of Spyro: Dawn of the Dragon - Archipelago Client

An Archipelago integration for *The Legend of Spyro: Dawn of the Dragon* (PS2, NTSC-U), allowing item randomization and multiworld support via the PCSX2 emulator.

---

## Item Pool & Locations
### Items
* **Blue Gem Cluster**: +1000 EXP to both Spyro and Cynder (99)
* **Health Gem**: +1 Red Health Crystal to both Spyro and Cynder (20)
* **Mana Gem**: +1 Green Magic Crystal to both Spyro and Cynder (20)
* **[Spyro | Cynder] [Helmet | Bracers | Tail] [Silver | Gold | Fury]**: Grants the specified piece of armor (18)
* **Health Gem S**: Any player-controlled dragon(s) recover 19 HP (Filler)
* **Mana Gem S**: Any player-controlled dragon(s) recover 19 Mana (Filler)
### Locations
* **All 99 Blue Gem Clusters**
* **All 20 Health Gems**
* **All 20 Mana Gems**
* **All 18 Armor Chests**
* **All 8 Elite Enemies**

As all items in this game are effectively optional, progression is not gated.
### Goal Check
Defeat Malefor!

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
After completing one of these three methods, it may be wise to close and re-open any Archipelago windows to ensure the world is able to be recognized by Archipelago.


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

* **Blue Gem EXP duplication on reconnect**
  Reconnecting to the server may reapply EXP from Blue Gems.
  This can result in higher-than-intended EXP totals but does not break progression.

* Additional bugs may exist, as this is a very early release

---

## Troubleshooting

### Client does not connect to PCSX2

* Ensure PINE is enabled
* Make sure PCSX2 is running before the client

### Game version check fails

* Verify you are using the NTSC-U version (`SLUS-21820`)

### Nothing is happening in-game

* Confirm the client is connected to both:

  * Archipelago server
  * PCSX2

### My max health/max mana is not increasing, even when I have 4+ Health/Mana Gems!
* If everything is working correctly, you will not see the update to your HP/mana bars until you recover your HP/mana.

### The game says I have enough (4-5) Red Health Crystals/Green Magic Crystals when I've received zero so far!
* This is simply a quirk of the UI. It perceives zero as having a full bar of these crystals.

### I got 1000 EXP from a blue gem cluster! Shouldn't that have been cancelled out?
* If everything is working correctly, this only happens when one or both dragons have less than 1000 unspent EXP. In this case, after one second has passed, the value should correct itself. To see if the value was updated properly, swap dragons to update their HUD.

---

## Credits

* Primary Contributor: IcyPenguin_
* Consulting and Debugging: Uroogla

---

## Feedback

If you encounter issues or bugs, please open an issue on GitHub or ping `@IcyPenguin_` in the Dawn of the Dragon thread in the Archipelago Discord server.
