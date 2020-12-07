from util import *
from emulator import Emulator
import shutil


class BGB(Emulator):
    def __init__(self):
        super().__init__("bgb", startup_time=0.6)
        self.speed = 1.0

    def setup(self):
        download("https://bgb.bircd.org/bgb.zip", "downloads/bgb.zip")
        extract("downloads/bgb.zip", "emu/bgb")
        setDPIScaling("emu/bgb/bgb.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "bgb.ini"), "emu/bgb/bgb.ini")
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/bgb/bgb.exe", "-set", "Speed=%g" % (self.speed), "-set", "LoadRomWarnings=0", "-set", "Width=160", "-set", "Height=144", "-set", "SoundOut=null", os.path.abspath(rom)], cwd="emu/bgb")