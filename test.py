import PIL.Image
import os

from util import *

PASS = "PASS"
FAIL = "FAIL"

class Test:
    def __init__(self, name, *, runtime, rom=None, result=None, gbc=False):
        rom = rom or name
        self.name = name
        self.rom = os.path.join("tests", rom)
        self.gbc = gbc
        self.runtime = runtime

        assert os.path.exists(self.rom)
        if result is None:
            result = os.path.splitext(rom)[0] + ".png"
        result = os.path.join("tests", result)
        
        def tryOpenImage(filename):
            if filename is not None and os.path.exists(filename):
                return PIL.Image.open(filename)
            return None
        self.pass_result_filename = result
        self.pass_result = tryOpenImage(result)
        self.fail_result = tryOpenImage(os.path.splitext(result)[0] + ".fail.png")

    def checkResult(self, screenshot):
        if self.pass_result is not None and compareImage(screenshot, self.pass_result):
            return PASS
        if self.fail_result is not None and compareImage(screenshot, self.fail_result):
            return FAIL
        return None

    def __repr__(self):
        return self.name