from .world import DotDWorld as DotDWorld

from multiprocessing import Process

from worlds.LauncherComponents import Component, components

def run_client():
    from .client import main
    Process(target=main,name="SpyroDotDClient").start()

components.append(Component("Spyro DotD Client", func=run_client))