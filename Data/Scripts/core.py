import os
from time import time
from pathlib import Path
from datetime import timedelta
from shutil import copy2 as copy
from tkinter import Tk, messagebox as MsgBox, filedialog as fd

__author__  = "kubinka0505"
__credits__ = "kubinka0505"

#-=-=-=-#

tk = Tk()
tk.withdraw()

#-=-=-=-#
# Set variables

CLI = 0

if len(os.sys.argv) > 1:
	CLI = 1