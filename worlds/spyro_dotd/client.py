from __future__ import annotations

import asyncio
import time
from typing import Dict, Set, Optional

from worlds.AutoWorld import World
from NetUtils import ClientStatus
from CommonClient import CommonContext, ClientCommandProcessor, server_loop, gui_enabled


from .items import DotDItem
from .options import DotDOptions
from .world import DotDWorld
from .locations import LOCATION_FLAG_ADDRESS_TO_NAME, LOCATION_NAME_TO_ID
from .pcsx2_interface.pine import Pine

# Okay, low-key half of this was written by Claude. I'm trash at netcode and MIPS and have never written for AP before. I am just one guy.
# No one else interested in this project at the time of writing this comment either has the time or the knowledge to contribute to it

# Useful addresses
ADDR_SPYRO_CURRENT_HP = 0x9FEAE0
ADDR_CYNDER_CURRENT_HP = 0x9FEAE8
ADDR_SPYRO_CURRENT_MANA = 0x9FEAF8
ADDR_CYNDER_CURRENT_MANA = 0x9FEB00
ADDR_SPYRO_CONTROLLER = 0x98C195
ADDR_CYNDER_CONTROLLER = 0x98C196
ADDR_HEALTH_GEMS_COLLECTED = 0x9FEB6C
ADDR_MANA_GEMS_COLLECTED = 0x9FEB7C

# EXP Buckets
ADDR_SPYRO_UNSPENT_EXP = 0x9FEB18
ADDR_SPYRO_FIRE_EXP = 0x9FEB20
ADDR_SPYRO_ICE_EXP = 0x9FEB24
ADDR_SPYRO_EARTH_EXP = 0x9FEB28
ADDR_SPYRO_ELEC_EXP = 0x9FEB2C
ADDR_CYNDER_UNSPENT_EXP = 0x9FEB1C
ADDR_CYNDER_POISON_EXP = 0x9FEB34
ADDR_CYNDER_SHADOW_EXP = 0x9FEB38
ADDR_CYNDER_FEAR_EXP = 0x9FEB3C
ADDR_CYNDER_WIND_EXP = 0x9FEB40

# Game completion flag address: is set to 1 when Malefor is defeated
ADDR_FINAL_BOSS_DEFEATED = 0x9FECDE

# Armor addresses
ADDR_SPYRO_HELMET_SILVER = 0xA3E674
ADDR_SPYRO_HELMET_GOLD = 0xA3DDE0
ADDR_SPYRO_HELMET_FURY = 0xA3F070
ADDR_SPYRO_BRACERS_SILVER = 0xA3E1F4
ADDR_SPYRO_BRACERS_GOLD = 0xA3E824
ADDR_SPYRO_BRACERS_FURY = 0xA3DE28
ADDR_SPYRO_TAIL_SILVER = 0xA3DC78
ADDR_SPYRO_TAIL_GOLD = 0xA3E47C
ADDR_SPYRO_TAIL_FURY = 0xA3E218
ADDR_CYNDER_HELMET_SILVER = 0xA3E554
ADDR_CYNDER_HELMET_GOLD = 0xA3E848
ADDR_CYNDER_HELMET_FURY = 0xA3E728
ADDR_CYNDER_BRACERS_SILVER = 0xA3DD98
ADDR_CYNDER_BRACERS_GOLD = 0xA3EB3C
ADDR_CYNDER_BRACERS_FURY = 0xA3E4A0
ADDR_CYNDER_TAIL_SILVER = 0xA3E650
ADDR_CYNDER_TAIL_GOLD = 0xA3DDBC
ADDR_CYNDER_TAIL_FURY = 0xA3F0B8

ARMOR_NAME_TO_ADDRESS = {
    "Spyro Helmet Silver": ADDR_SPYRO_HELMET_SILVER,
    "Spyro Helmet Gold": ADDR_SPYRO_HELMET_GOLD,
    "Spyro Helmet Fury": ADDR_SPYRO_HELMET_FURY,
    "Spyro Bracers Silver": ADDR_SPYRO_BRACERS_SILVER,
    "Spyro Bracers Gold": ADDR_SPYRO_BRACERS_GOLD,
    "Spyro Bracers Fury": ADDR_SPYRO_BRACERS_FURY,
    "Spyro Tail Silver": ADDR_SPYRO_TAIL_SILVER,
    "Spyro Tail Gold": ADDR_SPYRO_TAIL_GOLD,
    "Spyro Tail Fury": ADDR_SPYRO_TAIL_FURY,
    "Cynder Helmet Silver": ADDR_CYNDER_HELMET_SILVER,
    "Cynder Helmet Gold": ADDR_CYNDER_HELMET_GOLD,
    "Cynder Helmet Fury": ADDR_CYNDER_HELMET_FURY,
    "Cynder Bracers Silver": ADDR_CYNDER_BRACERS_SILVER,
    "Cynder Bracers Gold": ADDR_CYNDER_BRACERS_GOLD,
    "Cynder Bracers Fury": ADDR_CYNDER_BRACERS_FURY,
    "Cynder Tail Silver": ADDR_CYNDER_TAIL_SILVER,
    "Cynder Tail Gold": ADDR_CYNDER_TAIL_GOLD,
    "Cynder Tail Fury": ADDR_CYNDER_TAIL_FURY
}

ARMOR_NAME_TO_SCRATCH_ADDRESS = {
    name: addr + 0x05 for name, addr in ARMOR_NAME_TO_ADDRESS.items()
}

# Expected game ID for NTSC-U version of Dawn of the Dragon
# PINE's get_game_id() typically returns the disc serial, e.g. "SLUS-21820"
EXPECTED_GAME_ID = "SLUS-21820"

# Patching
ADDR_ARMOR_OWNERSHIP_CHECK_HOOK = 0x0039C2CC
ADDR_ARMOR_OWNERSHIP_CHECK_ROUTINE = 0x01FFED38


class MemoryReader:
    def __init__(self):
        # Slot 28011 is the PCSX2 default
        self.client = Pine(slot=28011)
        self._connected = False
        self._try_connect()

    def _try_connect(self) -> bool:
        """Attempt to connect (or reconnect) to PCSX2. Returns True on success."""
        try:
            self.client.connect()
            if self.client.is_connected():
                self._connected = True
                print("Connected to PCSX2 via PINE")
                return True
        except Exception as e:
            pass
        self._connected = False
        print("Could not connect to PCSX2. Is PINE enabled in Advanced Settings?")
        return False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _safe_op(self, op):
        """
        Wrap any PINE call so that a broken pipe / closed emulator is caught
        and turns the connection state to disconnected rather than crashing.
        Returns None on failure.
        """
        try:
            result = op()
            self._connected = True
            return result
        except Exception as e:
            if self._connected:
                print(f"[MemoryReader] Lost connection to PCSX2: {e}")
            self._connected = False
            return None

    def read_u32(self, ps2_address: int) -> Optional[int]:
        return self._safe_op(lambda: self.client.read_int32(ps2_address))

    def write_u32(self, ps2_address: int, value: int) -> bool:
        return self._safe_op(lambda: self.client.write_int32(ps2_address, value)) is not None

    def read_s32(self, ps2_address: int) -> Optional[int]:
        return self._safe_op(lambda: self.client.read_int32_signed(ps2_address))

    def write_s32(self, ps2_address: int, value: int) -> bool:
        return self._safe_op(lambda: self.client.write_int32_signed(ps2_address, value)) is not None

    def read_bytes(self, ps2_address: int, length: int) -> Optional[bytes]:
        return self._safe_op(lambda: self.client.read_bytes(ps2_address, length))

    def write_bytes(self, ps2_address: int, data: bytes) -> bool:
        return self._safe_op(lambda: self.client.write_bytes(ps2_address, data)) is not None

    def get_game_id(self) -> Optional[str]:
        return self._safe_op(lambda: self.client.get_game_id())


class DotDContext(CommonContext):
    game = "The Legend of Spyro: Dawn of the Dragon"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        self.memory = MemoryReader()
        self.items_handling = 0b111

        # ---------------------------------------------------------------
        # Idempotency tracking (fix for !collect / reconnect double-apply)
        # ---------------------------------------------------------------
        # Track the highest item index we have already fully applied so that
        # a re-send of ReceivedItems (on reconnect or !collect) never adds
        # the same item twice.
        self._applied_item_index: int = 0
        # Cumulative totals the server *says* we should have right now.
        # Replayed on every ReceivedItems so we always converge to the
        # server's view of the world.
        self._total_blue_gems: int = 0
        self._total_health_gems: int = 0
        self._total_mana_gems: int = 0

        # Item state variables
        self._session_blue_gems_at_connect: int = 0

        # Armor names received — set-based, naturally idempotent
        self._received_armor: Set[str] = set()

        # Default options values
        self.last_death_link: float = 0
        self.death_link_enabled = False

        # Whether game-version check has passed
        self._game_version_ok: bool = False
        # Whether final boss defeat has already been sent to the server
        self._goal_sent: bool = False

    # ------------------------------------------------------------------
    # Game version guard
    # ------------------------------------------------------------------
    def check_game_version(self) -> bool:
        """
        Read the disc serial from PCSX2 and verify it matches the expected
        NTSC-U version. Returns True if OK, False (and prints a message) if not.
        """
        game_id = self.memory.get_game_id()
        if game_id is None:
            print("[Version Check] Could not read game ID from PCSX2 — is the emulator running?")
            return False
        # PINE may return a string like "SLUS-21820 " with trailing whitespace
        game_id = game_id.strip()
        if game_id != EXPECTED_GAME_ID:
            print(
                f"[Version Check] FAILED: expected game ID '{EXPECTED_GAME_ID}' "
                f"but got '{game_id}'. "
                "Only the NTSC-U version is supported. Client will not operate."
            )
            return False
        print(f"[Version Check] OK ({game_id})")
        return True

    # ------------------------------------------------------------------
    # Archipelago hooks
    # ------------------------------------------------------------------
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(DotDContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
        print(f"Checked Locations: {self.checked_locations}")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            print("Connected to Archipelago!")
            # -------------------------------------------------------
            # On (re)connection: reset cumulative counters and re-apply
            # ALL items from scratch so we always match the server's state.
            # -------------------------------------------------------
            self._reset_item_state()
            self.apply_patches()
            self.death_link_enabled = bool(args["slot_data"].get("death_link", 0))

        elif cmd == "ReceivedItems":
            try:
                print("Receiving items...")
                # args["index"] is the server-side starting index of this batch.
                # When the server re-sends from index 0 (reconnect / !collect),
                # we reset and rebuild state from scratch to stay in sync.
                batch_start: int = args.get("index", 0)
                if batch_start == 0:
                    # Full resync from the server — rebuild from zero
                    self._reset_item_state()

                for net_item in args["items"]:
                    print(net_item)
                    item_name = self.item_names.lookup_in_game(net_item.item)
                    print(f"Received {item_name} from player {net_item.player}")
                    self._accumulate_item(item_name)

                # Apply the newly-computed totals to game memory
                self._flush_item_state()

            except Exception as e:
                print(f"on_package encountered exception: {e}")

        elif cmd == "Bounced":
            if "DeathLink" in args.get("tags", []):
                self.last_death_link = args["data"]["time"]
                asyncio.create_task(self.kill_player())

    # ------------------------------------------------------------------
    # Item state — idempotent accumulation + flush
    # ------------------------------------------------------------------
    def _reset_item_state(self):
        """
        Clear all accumulated item counts/flags so they can be rebuilt
        cleanly from a ReceivedItems replay.
        """
        self._total_blue_gems = 0
        self._total_health_gems = 0
        self._total_mana_gems = 0
        self._received_armor = set()

    def _accumulate_item(self, item_name: str):
        """
        Count / flag an item without writing to memory yet.
        All writes happen in _flush_item_state so we can compute net
        deltas and avoid double-applying on !collect / reconnect.
        """
        if "Blue Gem" in item_name:
            self._total_blue_gems += 1
        elif item_name == "Health Gem S":
            self.handle_receive_health_gem_s()   # instant, one-shot
        elif item_name == "Mana Gem S":
            self.handle_receive_mana_gem_s()
        elif "Health Gem" in item_name:
            self._total_health_gems += 1
        elif "Mana Gem" in item_name:
            self._total_mana_gems += 1
        elif any(k in item_name for k in ("Tail", "Bracers", "Helmet")):
            self._received_armor.add(item_name)
        # Instant consumables (Health Gem S / Mana Gem S) are handled inside
        # handle_receive_item because they are meant to be applied once per
        # receipt, not re-applied on reconnect.

    def _flush_item_state(self):
        """
        Write the server-authoritative item state to game memory.
        Called after every ReceivedItems batch so the game always reflects
        what the server says the player should have.
        """
        # Write EXP
        spyro_exp = self.memory.read_u32(ADDR_SPYRO_UNSPENT_EXP) or 0
        cynder_exp = self.memory.read_u32(ADDR_CYNDER_UNSPENT_EXP) or 0
        # Only adjust the server-contributed portion; don't clobber in-world gains.
        # We track the delta between what we last wrote and what we're writing now.
        exp_delta = (self._total_blue_gems - getattr(self, "_last_written_blue_gems", 0)) * 1000
        if exp_delta != 0:
            self.memory.write_u32(ADDR_SPYRO_UNSPENT_EXP, max(0, spyro_exp + exp_delta))
            self.memory.write_u32(ADDR_CYNDER_UNSPENT_EXP, max(0, cynder_exp + exp_delta))
        self._last_written_blue_gems = self._total_blue_gems

        # Gem counts: these are continuously enforced by the setter tasks, so
        # just update the module-level globals that those tasks read.
        global health_gems_collected, mana_gems_collected
        health_gems_collected = self._total_health_gems
        mana_gems_collected = self._total_mana_gems

        # Armor: set scratch flags for everything we've received
        for armor_name in self._received_armor:
            scratch_addr = ARMOR_NAME_TO_SCRATCH_ADDRESS.get(armor_name)
            if scratch_addr:
                self.memory.write_bytes(scratch_addr, b"\x01")

    # ------------------------------------------------------------------
    # Patches
    # ------------------------------------------------------------------
    def apply_patches(self):
        self.memory.write_bytes(ADDR_ARMOR_OWNERSHIP_CHECK_ROUTINE, bytes([
            0x21, 0x00, 0x83, 0x90,  # lbu v1, 0x21(a0)
            0xB4, 0x70, 0x0E, 0x08,  # j 0x0039c2d0
            0x00, 0x00, 0x00, 0x00,  # nop
            0x00, 0x00, 0x00, 0x00,  # nop
        ]))
        self.memory.write_bytes(ADDR_ARMOR_OWNERSHIP_CHECK_HOOK, bytes([
            0x4E, 0xFB, 0x7F, 0x08,  # j 0x01FFED38
        ]))
        print("Game patches applied.")

    def restore_scratch_flags(self):
        for location_name, scratch_addr in ARMOR_NAME_TO_SCRATCH_ADDRESS.items():
            location_id = LOCATION_NAME_TO_ID[location_name]
            if location_id in self.checked_locations:
                self.memory.write_bytes(scratch_addr, b"\x01")
        print("Scratch flags restored.")

    # ------------------------------------------------------------------
    # Death / kill
    # ------------------------------------------------------------------
    async def kill_player(self):
        self.memory.write_u32(ADDR_SPYRO_CURRENT_HP, 0)
        self.memory.write_u32(ADDR_CYNDER_CURRENT_HP, 0)

    # ------------------------------------------------------------------
    # Item send (location-side cancellation) — unchanged logic, kept here
    # ------------------------------------------------------------------
    def handle_send_item(self, loc_name: str):
        id = LOCATION_NAME_TO_ID[loc_name]
        if 1 <= id <= 99:
            asyncio.create_task(self.handle_cancel_blue_gem())
        elif 101 <= id <= 120:
            self.handle_cancel_health_gem()
        elif 201 <= id <= 220:
            self.handle_cancel_mana_gem()
        elif 401 <= id <= 418:
            self.handle_cancel_armor()

    async def handle_cancel_blue_gem(self):
        spyro_unspent_exp = self.memory.read_u32(ADDR_SPYRO_UNSPENT_EXP) or 0
        cynder_unspent_exp = self.memory.read_u32(ADDR_CYNDER_UNSPENT_EXP) or 0
        if spyro_unspent_exp < 1000 or cynder_unspent_exp < 1000:
            await asyncio.sleep(1.0)
            spyro_unspent_exp = self.memory.read_u32(ADDR_SPYRO_UNSPENT_EXP) or 0
            cynder_unspent_exp = self.memory.read_u32(ADDR_CYNDER_UNSPENT_EXP) or 0
        else:
            await asyncio.sleep(0)
        self.memory.write_u32(ADDR_SPYRO_UNSPENT_EXP, max(0, spyro_unspent_exp - 1000))
        self.memory.write_u32(ADDR_CYNDER_UNSPENT_EXP, max(0, cynder_unspent_exp - 1000))

    def handle_cancel_health_gem(self):
        pass  # handled by health_gem_setter

    def handle_cancel_mana_gem(self):
        pass  # handled by mana_gem_setter

    def handle_cancel_armor(self):
        pass  # handled by armor_setter

    # ------------------------------------------------------------------
    # Legacy per-item receive handlers (still used for instant consumables)
    # ------------------------------------------------------------------
    def handle_receive_health_gem_s(self):
        if self.memory.read_bytes(ADDR_SPYRO_CONTROLLER, 1) == b"\x00":
            spyro_hp = self.memory.read_u32(ADDR_SPYRO_CURRENT_HP) or 0
            self.memory.write_u32(ADDR_SPYRO_CURRENT_HP, spyro_hp + 19)
        if self.memory.read_bytes(ADDR_CYNDER_CONTROLLER, 1) == b"\x00":
            cynder_hp = self.memory.read_u32(ADDR_CYNDER_CURRENT_HP) or 0
            self.memory.write_u32(ADDR_CYNDER_CURRENT_HP, cynder_hp + 19)

    def handle_receive_mana_gem_s(self):
        if self.memory.read_bytes(ADDR_SPYRO_CONTROLLER, 1) == b"\x00":
            spyro_mana = self.memory.read_u32(ADDR_SPYRO_CURRENT_MANA) or 0
            self.memory.write_u32(ADDR_SPYRO_CURRENT_MANA, spyro_mana + 19)
        if self.memory.read_bytes(ADDR_CYNDER_CONTROLLER, 1) == b"\x00":
            cynder_mana = self.memory.read_u32(ADDR_CYNDER_CURRENT_MANA) or 0
            self.memory.write_u32(ADDR_CYNDER_CURRENT_MANA, cynder_mana + 19)

    # ------------------------------------------------------------------
    # Goal completion
    # ------------------------------------------------------------------
    async def send_goal_completion(self):
        """Send the game-complete status to the Archipelago server."""
        if not self._goal_sent and self.slot:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self._goal_sent = True
            print("Goal sent: Malefor defeated!")


# ---------------------------------------------------------------------------
# Globals (gem totals mirrored into memory by setter tasks)
# ---------------------------------------------------------------------------
health_gems_collected = 0
mana_gems_collected = 0


# ---------------------------------------------------------------------------
# Background tasks
# ---------------------------------------------------------------------------

async def emulator_watchdog(ctx: DotDContext):
    """
    Periodically tries to reconnect to PCSX2 if the connection was lost.
    Also re-checks the game version and re-applies patches after reconnection.
    """
    while True:
        try:
            currently_connected = ctx.memory.is_connected

            if not currently_connected:
                # Try to reconnect silently
                reconnected = ctx.memory._try_connect()
                if reconnected:
                    print("[Watchdog] Reconnected to PCSX2.")
                    # Re-validate game version on reconnect
                    if not ctx.check_game_version():
                        ctx._game_version_ok = False
                        print("[Watchdog] Wrong game version after reconnect — pausing operations.")
                    else:
                        ctx._game_version_ok = True
                        # Re-apply patches and restore flags since emulator memory was wiped
                        if ctx.slot:
                            ctx.apply_patches()
                            ctx.restore_scratch_flags()
                            ctx._flush_item_state()
        except Exception as e:
            print(f"[Watchdog] Unexpected error: {e}")

        await asyncio.sleep(3.0)


async def location_watcher(ctx: DotDContext):
    while True:
        try:
            if not ctx.memory.is_connected or not ctx._game_version_ok:
                await asyncio.sleep(1.0)
                continue

            for address, location_name in LOCATION_FLAG_ADDRESS_TO_NAME.items():
                try:
                    data = ctx.memory.read_bytes(address, 1)
                    if data is None:
                        continue
                    collected = int.from_bytes(data, byteorder="little")
                except Exception as e:
                    print(f"Error in location_watcher: {e}")
                    continue

                if collected == 1:
                    location_id = LOCATION_NAME_TO_ID[location_name]
                    if location_id not in ctx.checked_locations:
                        print(f"Check found: {location_name}")
                        ctx.checked_locations.add(location_id)
                        await ctx.check_locations([location_id])
                        ctx.handle_send_item(location_name)

            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Fatal error in location_watcher: {e}")
            await asyncio.sleep(1.0)


async def health_gem_setter(ctx: DotDContext):
    while True:
        try:
            if ctx.memory.is_connected and ctx._game_version_ok:
                ctx.memory.write_u32(ADDR_HEALTH_GEMS_COLLECTED, health_gems_collected)
        except Exception as e:
            print(f"Error in health_gem_setter: {e}")
        await asyncio.sleep(0.1)


async def mana_gem_setter(ctx: DotDContext):
    while True:
        try:
            if ctx.memory.is_connected and ctx._game_version_ok:
                ctx.memory.write_u32(ADDR_MANA_GEMS_COLLECTED, mana_gems_collected)
        except Exception as e:
            print(f"Error in mana_gem_setter: {e}")
        await asyncio.sleep(0.1)


async def death_watcher(ctx: DotDContext):
    while True:
        try:
            if ctx.slot and ctx.death_link_enabled and ctx.memory.is_connected and ctx._game_version_ok:
                spyro_hp = ctx.memory.read_u32(ADDR_SPYRO_CURRENT_HP)
                cynder_hp = ctx.memory.read_u32(ADDR_CYNDER_CURRENT_HP)

                # Guard against None (disconnected)
                if spyro_hp is None or cynder_hp is None:
                    await asyncio.sleep(0.1)
                    continue

                if spyro_hp == 0 and cynder_hp == 0:
                    current_time = time.time()
                    if current_time - ctx.last_death_link > 3.0:
                        await ctx.send_death(death_text="Spyro and Cynder have fallen!")
                        ctx.last_death_link = current_time
        except Exception as e:
            print(f"Error in death_watcher: {e}")
        await asyncio.sleep(0.1)


async def goal_watcher(ctx: DotDContext):
    """
    Polls the final boss defeat flag. When set, sends goal completion to the server.
    Only active once connected to the server and game version is confirmed.
    """
    while True:
        try:
            if ctx.slot and ctx.memory.is_connected and ctx._game_version_ok and not ctx._goal_sent:
                data = ctx.memory.read_bytes(ADDR_FINAL_BOSS_DEFEATED, 1)
                if data is not None and int.from_bytes(data, byteorder="little") == 1:
                    await ctx.send_goal_completion()
        except Exception as e:
            print(f"Error in goal_watcher: {e}")
        await asyncio.sleep(0.5)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main(*args: str):
    async def _main(connect: str | None, password: str | None):
        ctx = DotDContext(None, None)

        # Version check before doing anything else
        if ctx.memory.is_connected:
            ctx._game_version_ok = ctx.check_game_version()
            if not ctx._game_version_ok:
                print("Wrong game version detected. Client will run but memory operations are disabled.")
                print("Please load the NTSC-U version of Dawn of the Dragon and restart the client.")
        else:
            # Not connected to PCSX2 yet; the watchdog will check version when it connects
            ctx._game_version_ok = False

        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        watcher_task = asyncio.create_task(location_watcher(ctx), name="location watcher")
        health_gem_task = asyncio.create_task(health_gem_setter(ctx), name="health gem task")
        mana_gem_task = asyncio.create_task(mana_gem_setter(ctx), name="mana gem task")
        death_task = asyncio.create_task(death_watcher(ctx), name="death watcher")
        goal_task = asyncio.create_task(goal_watcher(ctx), name="goal watcher")
        watchdog_task = asyncio.create_task(emulator_watchdog(ctx), name="emulator watchdog")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()

        # Cancel all background tasks
        for task in (watcher_task, health_gem_task, mana_gem_task, death_task, goal_task, watchdog_task):
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        await ctx.shutdown()

    # TODO: Handle command line args
    asyncio.run(_main(None, None))


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])