from util import *
from emulator import Emulator
from test import *
import glob
import shutil
import os
import PIL.Image
import PIL.ImageOps
import shutil

class Ares(Emulator):
    def __init__(self):
        super().__init__("ares", "https://ares-emu.net/", startup_time=2.2, features=(PCM,))
        self.title_check = lambda title: "ares" in title

    def setup(self):
        downloadGithubRelease("ares-emulator/ares", "downloads/ares.zip", filter=lambda n: "x64" in n and "windows" in n and n.endswith(".zip"), allow_prerelease=True)
        extract("downloads/ares.zip", "emu/ares")

        if not os.path.exists("emu/ares/ares.exe"):
            src_dir = os.path.join("emu/ares", os.listdir("emu/ares")[0])
            dst_dir = "emu/ares"

            for item in os.listdir(src_dir):
                s = os.path.join(src_dir, item)
                d = os.path.join(dst_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
                    
        setDPIScaling("emu/ares/ares.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "ares-settings.bml"), "emu/ares/settings.bml")

    def startProcess(self, rom, *, model, required_features):
        target = "emu/ares/ares-rom.gb"
        self.cgb = model == CGB
        if self.cgb:
            target += "c"
        shutil.copy(rom, target)
        return subprocess.Popen(["emu/ares/ares.exe", os.path.abspath(target)], cwd="emu/ares")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        screenshot = screenshot.resize((160, 144), PIL.Image.NEAREST)
        if not self.cgb:
            screenshot = screenshot.convert(mode="L", dither=PIL.Image.NONE)
            screenshot = PIL.ImageOps.autocontrast(screenshot)
        return screenshot
